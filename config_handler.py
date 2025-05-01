# -*- coding: utf-8 -*-
import json
import logging
from os.path import exists

from log_module import *

if not exists("config.json"):

    logging.info("config.json not found")

    with open("config.json", "w", encoding="utf-8") as file:
        file.write("""{
  "alert_bot_token": "your_alert_bot_token",
  "alert_recipient": [],
  "alert_level": "ERROR",
  
  "bot_token": "your_bot_token",
  "host": "example.com",
  "port": 22,
  "username": "admin",
  "password": "admin",
  "remote_world_path": "/world/"
}""")
        logging.info("config.json has been created")

try:
    with open("config.json", "r", encoding = "utf-8") as file:
        config = json.load(file)
        logging.info("config.json loaded successfully")

except json.JSONDecodeError as e:
        logging.critical(f"Ошибка при разборе JSON: {e}")
