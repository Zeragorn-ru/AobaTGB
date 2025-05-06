# -*- coding: utf-8 -*-
import json
import os
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any

import asyncssh
from asyncssh import connect

from boot import info, warn, error


class SFTPConnectionError(Exception):
    """Пользовательское исключение для проблем с SFTP-соединением."""
    pass

class SFTPHandler:
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._file_cache: Dict[str, Any] = {}
        self._listdir_cache: Optional[List[str]] = None
        self._remote_upload_path = "/remote/path/to/upload/"

    @asynccontextmanager
    async def _sftp_connection(self):
        """Асинхронный контекстный менеджер для управления SFTP-соединениями."""
        try:
            async with connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                known_hosts=None
            ) as conn:
                async with conn.start_sftp_client() as sftp:
                    yield sftp
        except asyncssh.Error as e:
            error(f"Ошибка подключения SFTP: {e}")
            raise SFTPConnectionError(f"Не удалось подключиться к {self.host}:{self.port}") from e

    async def json_file_load(self, file_path: str) -> None:
        """Асинхронная загрузка JSON-файла с удаленного сервера и его кэширование."""
        try:
            async with self._sftp_connection() as sftp:
                async with sftp.open(file_path, 'r') as remote_file:
                    content = await remote_file.read()
                    self._file_cache[file_path] = json.loads(content)
        except (json.JSONDecodeError, asyncssh.SFTPError, asyncssh.Error) as e:
            error(f"Не удалось загрузить JSON-файл {file_path}: {e}")
            raise

    async def bulk_json_load(self, file_paths: List[str]) -> None:
        """Асинхронная массовая загрузка JSON-файлов за одно соединение."""
        try:
            async with self._sftp_connection() as sftp:
                for file_path in file_paths:
                    try:
                        async with sftp.open(file_path, 'r') as remote_file:
                            content = await remote_file.read()
                            self._file_cache[file_path] = json.loads(content)
                    except (json.JSONDecodeError, asyncssh.SFTPError) as e:
                        warn(f"Не удалось загрузить файл {file_path}: {e}")
                        continue
        except asyncssh.Error as e:
            error(f"Ошибка при массовой загрузке файлов: {e}")
            raise SFTPConnectionError(f"Ошибка соединения: {e}") from e

    async def upload_mp3_file(self, local_file_path: str) -> None:
        """Асинхронная загрузка MP3-файла на сервер по фиксированному пути."""
        if not os.path.isfile(local_file_path):
            error(f"Файл {local_file_path} не существует")
            raise ValueError(f"Файл {local_file_path} не существует")
        if not local_file_path.lower().endswith(".mp3"):
            error(f"Файл {local_file_path} не является MP3-файлом")
            raise ValueError(f"Файл должен иметь расширение .mp3")

        file_name = os.path.basename(local_file_path)
        remote_file_path = f"{self._remote_upload_path}{file_name}"

        try:
            async with self._sftp_connection() as sftp:
                await sftp.put(local_file_path, remote_file_path)
                info(f"Файл {local_file_path} успешно загружен на {remote_file_path}")
        except asyncssh.SFTPError as e:
            error(f"Ошибка загрузки файла {local_file_path} на сервер: {e}")
            raise SFTPConnectionError(f"Не удалось загрузить файл на {remote_file_path}") from e

    def get_file(self, file_path: str) -> Dict[str, Any]:
        """Возвращает содержимое кэшированного файла по пути."""
        if file_path not in self._file_cache:
            raise ValueError(f"Файл {file_path} не загружен.")
        return self._file_cache[file_path]

    async def get_listdir(self, remote_path: str) -> List[str]:
        """Асинхронное получение списка файлов в удаленной директории и его кэширование."""
        try:
            async with self._sftp_connection() as sftp:
                self._listdir_cache = await sftp.listdir(remote_path)
                return self._listdir_cache
        except asyncssh.SFTPError as e:
            error(f"Не удалось получить список директории {remote_path}: {e}")
            raise

    def clear_cache(self) -> None:
        """Очистка кэша файлов и списка директорий."""
        self._file_cache.clear()
        self._listdir_cache = None