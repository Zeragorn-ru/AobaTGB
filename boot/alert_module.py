# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot

from boot.config_handler import config
from boot.log_module import level_table, logging

if config["alert_enabled"]:
    bot = Bot(token=config["alert_bot_token"])


async def tgalert(level: str, alert: str) -> None:
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, f"[{level}]: {alert}")


async def log(level: str, alert: str, send_alert: bool = True) -> None:
    log_func = getattr(logging, level.lower(), logging.info)
    log_func(alert)

    if level_table[level] >= level_table[config["alert_level"]] and config["alert_enabled"] and send_alert:
        try:
            await tgalert(level, alert)
        except RuntimeError:
            await tgalert(level, alert)

async def debug(alert: str, send_alert: bool = True) -> None: await log("DEBUG", alert, send_alert)
async def info(alert: str, send_alert: bool = True) -> None: await log("INFO", alert, send_alert)
async def warn(alert: str, send_alert: bool = True) -> None: await log("WARN", alert, send_alert)
async def error(alert: str, send_alert: bool = True) -> None: await log("ERROR", alert, send_alert)
async def critical(alert: str, send_alert: bool = True) -> None: await log("CRITICAL", alert, send_alert)