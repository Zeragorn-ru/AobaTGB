# -*- coding: utf-8 -*-
import io
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

from boot import config, debug, info, warn, error, critical, restart_program
from mc_server_handler import StatsHandler, SFTPHandler
from bot_handler import SH, routers, dp
# Создание классов для работы бота
bot: Bot = Bot(token = config["bot_token"]) # Создание класса бота

async def admin_alert(alert: str):
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, text=alert)

async def on_startup(dispatcher: Dispatcher):
    await admin_alert("Бот запущен")

def routers_register(routers: list):
    for router in routers:
        dp.include_router(router)

async def main():
    dp.startup.register(on_startup)
    routers_register(routers)
    try:
        await SH.refresh_stats()
    except Exception as e:
        await admin_alert(f"При загрузке статистики произошла ошибка:{e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

