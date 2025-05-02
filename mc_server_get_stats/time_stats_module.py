# -*- coding: utf-8 -*-
import paramiko
import json
from io import BytesIO

from config_handler import config

def get_play_time_hours(stats_json):
    try:
        ticks = stats_json['stats']['minecraft:custom']['minecraft:play_time']
        return round(ticks / 72000, 2)  # 20 тиков в секунду, 3600 сек в час => 20*3600=72000
    except KeyError:
        return 0

def fetch_stats_and_usernames(sftp, remote_path="."):
    # Загрузка usercache.json
    usercache_file = sftp.file(f"./usercache.json", "r")
    usercache = json.load(usercache_file)

    # Загрузка всех файлов из папки stats
    stats_dir = f"{remote_path}/stats"
    files = sftp.listdir(stats_dir)

    uuid_to_nick = {entry["uuid"]: entry["name"] for entry in usercache}

    for filename in files:
        if filename.endswith(".json"):
            uuid = filename.replace(".json", "")
            with sftp.file(f"{stats_dir}/{filename}", "r") as f:
                stats = json.load(f)
                hours = get_play_time_hours(stats)
                name = uuid_to_nick.get(uuid, "(неизвестно)")
                print(f"{name}: {hours} ч")


def get_play_time()->list:
    transport = paramiko.Transport((config["host"], config["port"]))
    transport.connect(username = config["username"], password = config["password"])
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Выполнение
    fetch_stats_and_usernames(sftp, config["remote_world_path"])

    # Завершение
    sftp.close()
    transport.close()
