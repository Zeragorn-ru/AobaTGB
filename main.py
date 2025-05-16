# -*- coding: utf-8 -*-
import io
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

from boot import config, debug, info, warn, error, critical, restart_program
from mc_server_handler import StatsHandler, SFTPHandler
from bot_handler import SH, router
# Создание классов для работы бота
dp: Dispatcher= Dispatcher(storage = MemoryStorage())
bot: Bot = Bot(token = config["bot_token"]) # Создание класса бота

async def admin_alert(alert: str):
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, text=alert)

async def on_startup(dispatcher: Dispatcher):
    await admin_alert("Бот запущен")

@router.message(Command("kill"))
async def kill_command(message: Message):
    if message.chat.id not in config["alert_recipient"]:
        await bot.send_message(message.chat.id, "403, not enough permissions",
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]), )
        await message.delete()
        return None
    await bot.send_message(message.chat.id, "Бот выключен")
    await critical("Бот убит")
    await dp.stop_polling()
    raise sys.exit(0)

async def main():
    dp.startup.register(on_startup)
    dp.include_router(router)
    await SH.refresh_stats()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

