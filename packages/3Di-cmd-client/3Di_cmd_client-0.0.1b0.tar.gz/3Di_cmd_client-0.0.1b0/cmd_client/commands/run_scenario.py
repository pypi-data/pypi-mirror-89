import asyncio
import logging
import pathlib
import sys
from datetime import datetime

import click
from openapi_client import Configuration, ApiException
from openapi_client.api.simulations_api import SimulationsApi
from openapi_client.api.organisations_api import OrganisationsApi
from openapi_client.api.threedimodels_api import ThreedimodelsApi
from rich.table import Table
from rich import box
from rich.prompt import Confirm
from rich.prompt import Prompt
from rich.padding import Padding
from rich.panel import Panel

from cmd_client.commands.settings import (
    Settings,
    EndpointOption,
    refresh_api_key,
    get_settings,
)
from cmd_client.commands.utils import download_files
from cmd_client.parser import ScenarioParser
from cmd_client.console import console
from cmd_client.errors import ExitCodes
from cmd_client.models.errors import ApiModelError
from cmd_client.models.scenario import ResolveError
from cmd_client.models.scenario import FailedStep
from cmd_client.errors import LoadScenarioError


# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(f" > %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

DEFAULT_PAGER_SIZE = 20


@click.group()
@click.option(
    "--endpoint",
    type=click.Choice(EndpointOption.__members__.keys()),
    default=EndpointOption.production.name,
    help="The endpoint where commands are run against (defaults to production --> https://api.3di.live/v3.0). "
    "The other endpoints are only useful for staff members.",
)
@click.pass_context
def cli(ctx: click.Context, endpoint: str):
    settings = get_settings(endpoint)
    ctx.obj = settings
    ctx.call_on_close(Settings.save_settings)


@cli.command()
@click.pass_obj
def auth(settings: Settings):
    """Provide authentication details"""
    try:
        configuration = Configuration(settings.endpoint)
        refresh_api_key(configuration)
        console.print(
            f":unlock: Authenticated as {settings.username}", style="success"
        )
    except ApiException as e:
        console.print(
            f":lock: Failed to authenticate: {e.reason}", style="warning"
        )
        sys.exit(ExitCodes.AUTHENTICATION_FAILED.value)


@cli.command()
@click.pass_obj
def models(settings: Settings):
    """List available threedimodels"""
    threedi_models_api = ThreedimodelsApi(settings.api_client)
    threedi_models = threedi_models_api.threedimodels_list()

    table = Table(
        show_header=True,
        box=box.HORIZONTALS,
        show_lines=False,
        width=(console.width * 80) / 100,
    )
    table.add_column("Id", width=5)
    table.add_column(
        "Name",
        width=20,
        justify="left",
        style="bold cyan",
        header_style="bold cyan",
    )
    table.add_column("Revision", justify="left")
    table.add_column("Inp success", justify="left")

    remaining = threedi_models.count
    limit = min(DEFAULT_PAGER_SIZE, remaining)

    while remaining == threedi_models.count or (
        remaining > 0 and Confirm.ask("Show more?")
    ):
        threedi_models = threedi_models_api.threedimodels_list(
            limit=limit, offset=remaining - limit
        )
        for i, model in enumerate(threedi_models.results):
            if model.inp_success is True:
                txt = f":heavy_check_mark: [bold green]{model.inp_success}[/bold green] "
            else:
                txt = f"[bold red]{model.inp_success}[/bold red]"
            table.add_row(
                f"{model.id}", f"{model.name}", f"{model.revision_hash}", txt
            )
        remaining -= limit
        limit = min(remaining, DEFAULT_PAGER_SIZE)
        console.print(table)


@cli.command()
@click.pass_obj
def organisations(settings: Settings):
    """List available organisations"""
    organisations_api = OrganisationsApi(settings.api_client)
    organisations = organisations_api.organisations_list()
    table = Table(
        show_header=True,
        box=box.HORIZONTALS,
        show_lines=False,
        width=(console.width * 80) / 100,
    )
    table.add_column("Unique Id", width=15)
    table.add_column(
        "Name",
        width=20,
        justify="left",
        style="bold cyan",
        header_style="bold cyan",
    )

    remaining = organisations.count
    limit = min(DEFAULT_PAGER_SIZE, remaining)

    while remaining == organisations.count or (
        remaining > 0 and Confirm.ask("Show more?")
    ):
        organisations = organisations_api.organisations_list(
            limit=limit, offset=remaining - limit
        )
        for i, org in enumerate(organisations.results):
            table.add_row(f"{org.unique_id}", f"{org.name}")
        remaining -= limit
        limit = min(remaining, DEFAULT_PAGER_SIZE)
        console.print(table)


@cli.command()
@click.pass_obj
def simulations(settings: Settings):
    """List simulations"""
    simulations_api = SimulationsApi(settings.api_client)
    simulations = simulations_api.simulations_list()

    table = Table(
        show_header=True,
        box=box.HORIZONTALS,
        show_lines=False,
        width=(console.width * 80) / 100,
    )
    table.add_column(
        "Id", width=5
    )  # , style="dark_green", header_style="bold dark_green")
    table.add_column("Name", width=20, justify="left")
    table.add_column("Status", justify="left")

    remaining = simulations.count
    limit = min(DEFAULT_PAGER_SIZE, remaining)
    while remaining == simulations.count or (
        remaining > 0 and Confirm.ask("Show more?")
    ):
        simulations = simulations_api.simulations_list(
            limit=limit, offset=remaining - limit
        )
        for i, simulation in enumerate(reversed(simulations.results)):
            status = simulations_api.simulations_status_list(simulation.id)
            if status.name == "finished":
                txt = f":heavy_check_mark: [bold green]{status.name}[/bold green] "
            elif status.name == "created":
                txt = f"[dim grey27]{status.name}[/dim grey27] "
            elif status.name == "initialized":
                txt = f"[bold dark_violet]{status.name}[/bold dark_violet] "
            else:
                txt = f"[bold red]{status.name}[/bold red]"
            table.add_row(f"{simulation.id}", f"{simulation.name}", txt)
        console.print(table)
        remaining -= limit
        limit = min(remaining, DEFAULT_PAGER_SIZE)


@cli.command()
@click.pass_obj
def scenarios(settings: Settings):
    """List local scenarios"""
    table = Table(show_header=True, box=box.HORIZONTALS, show_lines=True)
    table.add_column(
        "Id", width=5
    )  # , style="dark_green", header_style="bold dark_green")
    table.add_column(
        "Name",
        width=20,
        justify="left",
        style="bold cyan",
        header_style="bold cyan",
    )
    table.add_column("Description", justify="left", no_wrap=False)
    table.add_column(
        "Caution", justify="left", style="orange3", header_style="bold orange3"
    )
    table.add_column(
        "yaml", justify="left", style="dim blue", header_style="bold blue"
    )

    for i, scenario in enumerate(settings.scenarios, start=0):
        if isinstance(scenario, dict):
            s = ""
            if scenario.get("known_constraints"):
                for k, v in scenario["known_constraints"].items():
                    s += f"{k}: {v} \n"
            table.add_row(
                f"{i}",
                f"{scenario['name']}",
                f"{scenario['description']}",
                f"{s}",
                f"{scenario['file'].stem}",
            )
    console.print(table)


@cli.command()
@click.option(
    "--organisation",
    type=str,
    help="Unique-id of the organisation to set as default",
)
@click.option(
    "--result-folder",
    type=click.Path(dir_okay=True, writable=True, resolve_path=True),
)
@click.pass_obj
@click.pass_context
def settings(ctx, settings: Settings, organisation, result_folder):
    """Set default settings"""
    console.rule(
        ":wrench: Configuring defaults for the 3Di cli", style="bold blue"
    )
    console.print(Padding("", (1, 0)))
    ctx.invoke(auth)
    if organisation is None:
        console.rule("Please choose an organisation", style="bold blue")
        if (
            settings.organisation_uuid
            and Confirm.ask(
                f"Change current organisation {settings.organisation_uuid}?"
            )
            or not settings.organisation_uuid
        ):
            ctx.invoke(organisations)
            console.rule(":pencil2:", style="bold blue")
            organisation = Prompt.ask(
                "Set default organisation. UNIQUE_ID",
                default=settings.organisation_uuid,
            )
        else:
            organisation = settings.organisation_uuid
    if not result_folder:
        result_folder = click.prompt(
            "Set default result folder",
            default=settings.result_folder or "./results",
            type=click.Path(dir_okay=True, writable=True, resolve_path=True),
        )

    settings.organisation_uuid = organisation
    settings.result_folder = result_folder
    console.print(
        f":heavy_check_mark: Default settings are saved in {settings.config_file}"
    )


@cli.command(help="Run a given scenario")
@click.option(
    "--scenario",
    type=int,
    help="The ID of the scenario, as returned by the 'scenarios' command",
)
@click.option(
    "--model",
    type=int,
    help="The ID of the model you want to use, as returned by the 'models' command",
)
@click.option(
    "--organisation",
    type=str,
    help="The UUID of the organisation you want to run the scenario for, "
    "as returned by the 'organisations' command",
)
@click.pass_obj
@click.pass_context
def run(ctx, settings: Settings, scenario: int, model: int, organisation):
    """Run a scenario"""

    if scenario is None:
        ctx.invoke(scenarios)
        scenario = click.prompt(
            "Which scenario do you want to run? ID", type=int
        )

    if model is None:
        ctx.invoke(models)
        model = click.prompt("Which model do you want to run? ID", type=int)

    if not organisation:
        organisation = settings.organisation_uuid

    scenario_to_run = settings.scenarios[scenario]["file"]
    name = settings.scenarios[scenario]["name"]
    context = {
        "threedimodel_id": model,
        "organisation_uuid": organisation,
        "simulation_name": name,
        "datetime_now": datetime.utcnow().isoformat(),
    }
    parser = ScenarioParser(scenario_to_run, context)
    try:
        scenario = parser.parse(
            settings.api_client, settings.websocket_settings
        )
    except (ResolveError, ApiModelError, LoadScenarioError) as err:
        console.print(f":collision: {err}", style="error")
        sys.exit(ExitCodes.SCENARIO_CONFIG_ERROR.value)

    console.rule(f"Loading scenario {name}", style="bold blue")
    scenario.simulation.save()
    console.print(f":link: URL: {scenario.simulation.instance.url}")
    import websockets

    try:
        console.rule(f"Starting scenario run...", style="bold blue")
        asyncio.run(scenario.execute())
    except KeyboardInterrupt:
        pass
    except FailedStep as err:
        console.print(f"{err}", style="error")
        sys.exit(ExitCodes.RUN_SCENARIO_ERROR.value)
    except websockets.exceptions.InvalidStatusCode as err:
        console.print(f"{err}", style="error")
        sys.exit(ExitCodes.CONNECTION_ERROR.value)
    else:
        success_panel = Panel(
            f"Run for scenario {name} successful",
            expand=True,
            box=box.DOUBLE,
            border_style="bold spring_green4",
            title=f":sparkles: Finished :sparkles:",
        )
        console.print(success_panel, justify="center")


@cli.command(help="Download results of a simulation")
@click.option("--simulation", type=int, help="ID of the simulation")
@click.option(
    "--folder",
    type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    help="Absolute path to the where the files will be stored",
)
@click.pass_obj
@click.pass_context
def results(ctx, settings: Settings, simulation: int, folder):
    """Download results of a simulation"""
    console.rule(
        ":arrow_heading_down:  Download simulation results", style="bold blue"
    )
    console.print(Padding("", (1, 0)))

    if simulation is None:
        console.rule("Please choose a simulation", style="bold blue")
        ctx.invoke(simulations)
        simulation = click.prompt(
            "Which simulation do you want download? ID", type=int
        )
    if not folder:
        folder = click.prompt(
            "Where do you want to store the results files?",
            default=f"{settings.result_folder}/simulation-{simulation}",
            type=click.Path(dir_okay=True, writable=True, resolve_path=True),
        )

    output_folder = pathlib.Path(folder)
    try:
        output_folder.mkdir(parents=True)
    except FileExistsError:
        click.confirm(
            "Output folder already exists, we might override files in the folder. "
            "Do you want to continue?",
            abort=True,
        )

    simulations_api = SimulationsApi(settings.api_client)
    threedimodels_api = ThreedimodelsApi(settings.api_client)

    simulation = simulations_api.simulations_read(id=simulation)
    threedi_model_id = simulation.threedimodel_id

    gridadmin_download = threedimodels_api.threedimodels_gridadmin_download(
        threedi_model_id
    )
    f = [gridadmin_download]

    result_files = simulations_api.simulations_results_files_list(
        simulation.id
    )
    for result in result_files.results:
        if result.file.state in ["error", "removed"]:
            console.print(
                f"{result.filename} is in state {result.file.state} and will be skipped.",
                style="warning",
            )
            continue

        result_download = simulations_api.simulations_results_files_download(
            id=result.id, simulation_pk=simulation.id
        )
        f.append(result_download)
    success = download_files(f, output_folder)
    if success:
        console.print(
            ":heavy_check_mark: Finished downloading results", style="success"
        )
    else:
        console.print(
            ":collision: Not all files could be downloaded", style="error"
        )


if __name__ == "__main__":
    cli()
