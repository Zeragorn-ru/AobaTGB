# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot

from boot.config_handler import config
from boot.log_module import level_table, logging

if config["alert_enabled"]:
    bot = Bot(token=config["alert_bot_token"])


async def tgalert(level: str, alert: str):
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, f"[{level}]: {alert}")


def log(level: str, alert: str):
    log_func = getattr(logging, level.lower(), logging.info)
    log_func(alert)

    if level_table[level] >= level_table[config["alert_level"]] and config["alert_enabled"]:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(tgalert(level, alert))
        except RuntimeError:
            asyncio.run(tgalert(level, alert))

def debug(alert: str): log("DEBUG", alert)
def info(alert: str): log("INFO", alert)
def warn(alert: str): log("WARN", alert)
def error(alert: str): log("ERROR", alert)
def critical(alert: str): log("CRITICAL", alert)