import asyncio
import json
from typing import Optional
import logging
import pkg_resources

import websockets
from websockets.http import Headers
from cmd_client.commands.settings import WebSocketSettings
from cmd_client.console import console

logger = logging.getLogger(__name__)


class WebsocketClient(object):
    def __init__(self, settings: WebSocketSettings):
        self.settings = settings
        self.websocket = None
        self.do_listen = True
        self.queue = asyncio.Queue()
        self._connected = False

    def get_queue(self):
        return self.queue

    async def is_connected(self):
        while self._connected is False:
            await asyncio.sleep(0.5)

    @property
    def user_agent(self):
        return {
            "user-agent": f"3Di-cmd-client/{pkg_resources.get_distribution('3Di-cmd-client').version}"
        }

    async def listen(self, endpoint_uri: str):
        uri = f"{self.settings.proto}://{self.settings.host}/{self.settings.api_version}/{endpoint_uri}"
        console.print(f"• Trying to connect to {uri} now...")
        headers = Headers(authorization=f"{self.settings.token}")
        headers.update(**self.user_agent)
        sim_time: Optional[int] = None
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            console.print(f"•  Connected to {uri}")
            self._connected = True
            async for message in websocket:
                try:
                    message = json.loads(message)
                    try:
                        sim_time = message["data"]["time"]
                    except (KeyError, TypeError):
                        pass
                    if sim_time is not None:
                        message["sim_time"] = sim_time
                    await self.queue.put(message)
                except websockets.exceptions.ConnectionClosedOK:
                    self.do_listen = False
        console.print("• Websocket connection closed")

    async def close(self):
        self.do_listen = False
        if self.websocket:
            await self.websocket.close()
