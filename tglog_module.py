# -*- coding: utf-8 -*-
from aiogram import Bot
from asyncio import run

from config_handler import config
from log_module import *

async def tgalert(level:str ,alert:str):
    bot = Bot(token=config["alert_bot_token"])
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, f"[{level}]: {alert}")

def debug(alert:str):
    logging.info(alert)
    if level_table["DEBUG"] >= level_table[config["alert_level"]]:
        run(tgalert("DEBUG",alert))

def info(alert:str):
    logging.info(alert)
    if level_table["INFO"] >= level_table[config["alert_level"]]:
        run(tgalert("INFO",alert))

def warn(alert:str):
    logging.info(alert)
    if level_table["WARN"] >= level_table[config["alert_level"]]:
        run(tgalert("WARN",alert))

def error(alert:str):
    logging.info(alert)
    if level_table["ERROR"] >= level_table[config["alert_level"]]:
        run(tgalert("ERROR",alert))

def critical(alert:str):
    logging.info(alert)
    if level_table["CRITICAL"] >= level_table[config["alert_level"]]:
        run(tgalert("CRITICAL",alert))