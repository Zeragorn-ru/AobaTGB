# -*- coding: utf-8 -*-
import threading

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from boot import config, debug, info, warn, error, critical
from mc_server_handler import StatsHandler, SFTPHandler

# Создание классов для работы бота
dp = Dispatcher(storage = MemoryStorage())
router = Router()
bot = Bot(token = config["bot_token"]) # Создание класса бота

downloader = SFTPHandler(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )

# Класс статистики
SH = StatsHandler(
   downloader
)

@router.message(Command("start"))
async def start_command(message: types.Message):
    played_time = await SH.get_played_time()
    await bot.send_message(message.chat.id, text = f"{played_time}")

@router.message(Command("refresh"))
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Начато обновление статистики, пожалуйста подождите")
    await SH.refresh_stats()
    await bot.send_message(message.chat.id, "Статистика успешно обновлена")

async def main():
    dp.include_router(router)
    await SH.refresh_stats()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

