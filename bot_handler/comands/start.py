# -*- coding: utf-8 -*-
import sys

import asyncio
from aiogram import Bot, Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command

from bot_handler.msg_content import Msg
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_msg = Msg()
file = FSInputFile(bot_msg.img)

@router.message(Command("start"))
async def start_command(message: types.Message):
    bot = message.bot
    start_msg_info = await bot_msg.start()

    await bot.send_photo(
        message.chat.id,
        photo=file,
        caption = start_msg_info["start_text"],
        reply_markup = start_msg_info["buttons"],
        parse_mode="HTML"
    )

@router.callback_query(F.data == "start")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.start()

    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    start_content = InputMediaPhoto(
        media=file,
        caption=start_msg_info["start_text"],
        parse_mode="HTML"
    )

    await callback.bot.edit_message_media(
        chat_id=original_chat_id,
        message_id=original_message_id,
        media=start_content,
        reply_markup=start_msg_info["buttons"]
    )