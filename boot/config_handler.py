# -*- coding: utf-8 -*-
import json
import logging
from os.path import exists
from boot.log_module import *

if not exists("config.json"):
    logging.info("config.json not found")

    try:
        with open("./boot/default_config.json", "r", encoding="utf-8") as src_file:
            config_data = src_file.read()

        with open("config.json", "w", encoding="utf-8") as dst_file:
            dst_file.write(config_data)

        logging.info("config.json has been created")

    except FileNotFoundError:
        logging.critical("default_config.json not found in ./boot/")
    except Exception as e:
        logging.error(f"Failed to create config.json: {e}")

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        logging.info("config.json loaded successfully")

except FileNotFoundError:
    logging.critical("config.json not found.")
except json.JSONDecodeError as e:
    logging.critical(f"Error parsing JSON: {e}")
except Exception as e:
    logging.critical(f"Unexpected error while loading config.json: {e}")

