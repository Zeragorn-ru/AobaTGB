# -*- coding: utf-8 -*-
from typing import Dict, List
import json

from mc_server_get_stats.sftp_get_file import RemoteFileDownloader, SFTPConnectionError

from boot import config, debug, info, warn, error, critical

class StatsHandler:
    def __init__(self, downloader: RemoteFileDownloader = None):
        self.downloader = downloader or RemoteFileDownloader(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )
        self.users: Dict[str, str] = {}
        self.users_stats: List[str] = []
        self._load_all_data()

    def _load_all_data(self) -> None:
        """Загрузка всех данных (пользователи и статистика) за одно SFTP-соединение."""
        try:
            # Очистка кэша перед загрузкой
            self.downloader.clear_cache()

            # Загрузка списка файлов статистики
            stats_path = f"./{config['remote_world_name']}/stats"
            self.users_stats = [
                x.removesuffix(".json")
                for x in self.downloader.get_listdir(stats_path)
            ]

            # Формирование списка всех файлов для загрузки
             # Формирование списка всех файлов для загрузки
            file_paths = ["usercache.json"] + [
                f"{stats_path}/{user_stats}.json"
                for user_stats in self.users_stats
            ]

            # Массовая загрузка всех JSON-файлов
            self.downloader.bulk_json_load(file_paths)

            # Обработка usercache.json
            usercache = self.downloader.get_file("usercache.json")
            self.users = {
                user["uuid"]: user["name"]
                for user in usercache
            }

        except (ValueError, json.JSONDecodeError, SFTPConnectionError, IOError) as e:
            error(f"Не удалось загрузить данные: {e}")
            raise

    def refresh_stats(self) -> None:
        """Обновление всех данных статистики с удаленного сервера."""
        try:
            # Очистка текущих данных
            self.users.clear()
            self.users_stats.clear()

            # Повторная загрузка всех данных
            self._load_all_data()
            info("Статистика успешно обновлена")
        except (ValueError, json.JSONDecodeError, SFTPConnectionError, IOError) as e:
            error(f"Не удалось обновить статистику: {e}")
            raise

    def get_played_time(self) -> Dict[str, float]:
        """Расчет времени игры для каждого пользователя в часах."""
        stats: Dict[str, float] = {}
        stats_path = f"./{config['remote_world_name']}/stats"
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