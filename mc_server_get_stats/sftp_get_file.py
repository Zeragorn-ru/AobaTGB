# -*- coding: utf-8 -*-
import json

import paramiko

from boot import debug, info, warn, error, critical

class RemoteFileDownloader:
    def __init__(self, host:str, username:str, password:str, port:int = 22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.file = None
        self.listdir = None

    def json_file_load(self, file_path:str):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username = self.username, password = self.password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            with sftp.open(file_path, 'r') as remote_file:
                self.file = json.load(remote_file)

        except Exception as e:
            error(e)

        finally:
            sftp.close()
            transport.close()

    def get_file(self):
        if self.file is None:
            raise ValueError("file don't downloaded")
        return self.file

    def get_listdir(self, remote_path:str):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        try:
            self.listdir = sftp.listdir(remote_path)

        except Exception as e:
            error(e)

        sftp.close()
        transport.close()

        return self.listdir