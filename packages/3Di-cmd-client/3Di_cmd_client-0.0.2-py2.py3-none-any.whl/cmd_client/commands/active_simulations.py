import asyncio
import click
from datetime import datetime
from cmd_client.console import console
from cmd_client.models.monitor import ActiveSimulations

from cmd_client.commands.settings import (
    Settings,
    EndpointOption,
    refresh_api_key,
    get_settings,
)


async def monitor_active_simulations(endpoint):
    """
    runs the ActiveSimlations "run-run_monitor" task in the background
    """
    active_simulations = ActiveSimulations(endpoint)
    result = await asyncio.gather(
        active_simulations.run_monitor(), return_exceptions=True
    )
    if result:
        console.print(result, style="error")


@click.command(help="Show currently running simulations")
@click.option(
    "--endpoint",
    type=click.Choice(EndpointOption.__members__.keys()),
    default=EndpointOption.localhost.name,
    help="The endpoint where commands are run against",
)
@click.pass_context
def cli(ctx: click.Context, endpoint: str):
    settings = get_settings(endpoint)
    ctx.obj = settings
    refresh_api_key(settings.api_client.configuration)
    ctx.call_on_close(Settings.save_settings)
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        console.print(f"[{start_time}] Starting active simulations worker")
        asyncio.run(monitor_active_simulations(endpoint))
    except KeyboardInterrupt:
        pass
    else:
        console.print(
            f":sparkles: Bye bye, hope to see you soon! :sparkles:",
            style="success",
        )


if __name__ == "__main__":
    cli()
