# -*- coding: utf-8 -*-
import sys

import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

from bot_handler.msg_content import Msg
from boot import debug, info, warn, error, critical, config, restart_program

router: Router = Router()
bot_msg = Msg()

dp: Dispatcher= Dispatcher(storage = MemoryStorage())

@router.message(Command("kill"))
async def kill_command(message: Message):
    if message.chat.id not in config["alert_recipient"]:
        await message.bot.send_message(message.chat.id, "403, not enough permissions",
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]), )
        await message.delete()
        return None
    await message.bot.send_message(message.chat.id, "Бот выключен")
    await critical("Бот убит")
    await dp.stop_polling()
    raise sys.exit(0)

@router.callback_query(F.data == "delete")
async def delete(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        await error(e)

@router.message(Command("restart"))
async def kill_command(message: Message):
    bot = message.bot
    if message.chat.id not in config["alert_recipient"]:
        await bot.send_message(message.chat.id, "403, not enough permissions",
                               reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]),)
        await message.delete()
        return None
    await bot.send_message(message.chat.id, "Бот перезапускается")
    await critical("Бот остановлен")
    restart_program()