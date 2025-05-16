# -*- coding: utf-8 -*-
from mcipc.rcon.je import Client
import asyncio

from boot import error

class RCONClient:
    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

    async def send(self, command: str) -> str:
        def _sync_rcon():
            with Client(self.host, self.port) as client:
                client.login(self.password)
                return client.run(command)
        try:
            return await asyncio.to_thread(_sync_rcon)
        except Exception as e:
            await error(f"{e}")