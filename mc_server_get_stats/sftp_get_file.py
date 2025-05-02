# -*- coding: utf-8 -*-
import json
from contextlib import contextmanager
from typing import List, Optional, Dict, Any

import paramiko

from boot import debug, info, warn, error, critical

class SFTPConnectionError(Exception):
    """Пользовательское исключение для проблем с SFTP-соединением."""
    pass

class RemoteFileDownloader:
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._file_cache: Dict[str, Any] = {}
        self._listdir_cache: Optional[List[str]] = None

    @contextmanager
    def _sftp_connection(self):
        """Контекстный менеджер для управления SFTP-соединениями."""
        transport = paramiko.Transport((self.host, self.port))
        try:
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            yield sftp
        except paramiko.SSHException as e:
            error(f"Ошибка подключения SFTP: {e}")
            raise SFTPConnectionError(f"Не удалось подключиться к {self.host}:{self.port}") from e
        finally:
            try:
                sftp.close()
            except Exception as e:
                warn(f"Ошибка закрытия SFTP-соединения: {e}")
            try:
                transport.close()
            except Exception as e:
                warn(f"Ошибка закрытия транспорта: {e}")

    def json_file_load(self, file_path: str) -> None:
        """Загрузка JSON-файла с удаленного сервера и его кэширование."""
        try:
            with self._sftp_connection() as sftp:
                with sftp.open(file_path, 'r') as remote_file:
                    self._file_cache[file_path] = json.load(remote_file)
        except (json.JSONDecodeError, IOError) as e:
            error(f"Не удалось загрузить JSON-файл {file_path}: {e}")
            raise

    def bulk_json_load(self, file_paths: List[str]) -> None:
        """Массовая загрузка JSON-файлов за одно соединение."""
        try:
            with self._sftp_connection() as sftp:
                for file_path in file_paths:
                    try:
                        with sftp.open(file_path, 'r') as remote_file:
                            self._file_cache[file_path] = json.load(remote_file)
                    except (json.JSONDecodeError, IOError) as e:
                        warn(f"Не удалось загрузить файл {file_path}: {e}")
                        continue
        except SFTPConnectionError as e:
            error(f"Ошибка при массовой загрузке файлов: {e}")
            raise

    def get_file(self, file_path: str) -> Dict[str, Any]:
        """Возвращает содержимое кэшированного файла по пути."""
        if file_path not in self._file_cache:
            raise ValueError(f"Файл {file_path} не загружен.")
        return self._file_cache[file_path]

    def get_listdir(self, remote_path: str) -> List[str]:
        """Получение списка файлов в удаленной директории и его кэширование."""
        try:
            with self._sftp_connection() as sftp:
                self._listdir_cache = sftp.listdir(remote_path)
            return self._listdir_cache
        except IOError as e:
            error(f"Не удалось получить список директории {remote_path}: {e}")
            raise

    def clear_cache(self) -> None:
        """Очистка кэша файлов и списка директорий."""
        self._file_cache.clear()
        self._listdir_cache = None