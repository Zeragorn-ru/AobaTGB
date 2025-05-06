# -*- coding: utf-8 -*-
from typing import Dict, List
import json

import asyncio

from mc_server_handler.sftp_handler import SFTPHandler, SFTPConnectionError
from boot import debug, info, warn, error, critical

class StatsHandler:
    def __init__(self, downloader: SFTPHandler = None, remote_world_name: str = "world"):
        self.downloader: SFTPHandler = downloader
        self.users: Dict[str, str] = {}
        self.users_stats: List[str] = []
        self.remote_world_name: str = remote_world_name

    async def _load_all_data(self) -> None:
        try:
            self.downloader.clear_cache

            stats_path = f"./{self.remote_world_name}/stats"
            self.users_stats.clear()
            self.users_stats = [x.removesuffix(".json") for x in await self.downloader.get_listdir(stats_path)]

            file_paths = ["usercache.json"] + [f"{stats_path}/{user_stats}.json" for user_stats in self.users_stats]

            await self.downloader.bulk_json_load(file_paths)

            usercache = self.downloader.get_file("usercache.json")
            self.users.clear()
            self.users = {
                user["uuid"]: user["name"]
                for user in usercache
            }

        except (ValueError, json.JSONDecodeError, SFTPConnectionError, IOError) as e:
            error(f"Не удалось загрузить данные: {e}")
            raise

    async def refresh_stats(self) -> None:
        try:
            await self._load_all_data()
            info("Статистика успешно обновлена")
        except (ValueError, json.JSONDecodeError, SFTPConnectionError, IOError) as e:
            error(f"Не удалось обновить статистику: {e}")
            raise

    async def get_played_time(self) -> Dict[str, float]:
        """Расчет времени игры для каждого пользователя в часах."""
        stats: Dict[str: float] = {}
        stats_path = f"./{self.remote_world_name}/stats"
        for user_stats in self.users_stats:
            try:
                file_path = f"{stats_path}/{user_stats}.json"
                data = self.downloader.get_file(file_path)
                play_time = data.get('stats', {}).get('minecraft:custom', {}).get('minecraft:play_time', 0)
                stats[self.users[user_stats]] = round(play_time / 20 / 3600, 2)
            except (KeyError, ValueError) as e:
                warn(f"Не удалось обработать статистику для {user_stats}: {e}")
                continue
        return stats