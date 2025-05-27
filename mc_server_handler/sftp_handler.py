# -*- coding: utf-8 -*-
import json
import os
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
import io
import asyncio

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
        self._remote_upload_path = "./plugins/CustomDiscs/musicdata/"

    @asynccontextmanager
    async def _sftp_connection(self):
        """Асинхронный контекстный менеджер для управления SFTP-соединениями."""
        try:
            async with await asyncio.wait_for(connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                known_hosts=None
            ),
                timeout=30
            ) as conn:
                async with conn.start_sftp_client() as sftp:
                    yield sftp
        except Exception as e:
            await error(f"Ошибка подключения SFTP: {e}")
            raise SFTPConnectionError(f"Не удалось подключиться к {self.host}:{self.port}") from e

    async def json_file_load(self, file_path: str) -> None:
        """Асинхронная загрузка JSON-файла с удаленного сервера и его кэширование."""
        try:
            async with self._sftp_connection() as sftp:
                async with sftp.open(file_path, 'r') as remote_file:
                    content = await remote_file.read()
                    self._file_cache[file_path] = json.loads(content)
        except (json.JSONDecodeError, asyncssh.SFTPError, asyncssh.Error) as e:
            await error(f"Не удалось загрузить JSON-файл {file_path}: {e}")
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
                        await warn(f"Не удалось загрузить файл {file_path}: {e}")
                        continue
        except asyncssh.Error as e:
            await error(f"Ошибка при массовой загрузке файлов: {e}")
            raise SFTPConnectionError(f"Ошибка соединения: {e}") from e

    async def upload_mp3_file(self, file: io.BufferedReader, file_name = None) -> None:
        """Асинхронная загрузка MP3-файла на сервер по фиксированному пути."""
        if file_name is None: file_name = file.name

        remote_file_path = f"{self._remote_upload_path}{file_name}"
        try:
            async with self._sftp_connection() as sftp:
                async with sftp.open(remote_file_path, "wb") as remote_file:
                    await remote_file.write(file.read())
                    await info(f"Файл {file} успешно загружен на {remote_file_path}")
        except asyncssh.SFTPError as e:
            await error(f"Ошибка загрузки файла {file} на сервер: {e}")
            raise SFTPConnectionError(f"Не удалось загрузить файл на {file}") from e

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
            await error(f"Не удалось получить список директории {remote_path}: {e}")
            raise

    def clear_cache(self) -> None:
        """Очистка кэша файлов и списка директорий."""
        self._file_cache.clear()
        self._listdir_cache = None