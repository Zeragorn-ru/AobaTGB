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


async def log(level: str, alert: str):
    log_func = getattr(logging, level.lower(), logging.info)
    log_func(alert)

    if level_table[level] >= level_table[config["alert_level"]] and config["alert_enabled"]:
        try:
            await tgalert(level, alert)
        except RuntimeError:
            await tgalert(level, alert)

async def debug(alert: str): await log("DEBUG", alert)
async def info(alert: str): await log("INFO", alert)
async def warn(alert: str): await log("WARN", alert)
async def error(alert: str): await log("ERROR", alert)
async def critical(alert: str): await log("CRITICAL", alert)