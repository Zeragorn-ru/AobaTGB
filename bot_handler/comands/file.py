# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import Command

from bot_handler.msg_content import Msg, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_msg = Msg()

@router.message(Command("file"))
async def file_command(message: Message) -> None:
    bot = message.bot
    start_msg_info = await bot_msg.file()

    if not message.audio:
        await message.delete()
        await bot.send_message(message.chat.id, text=start_msg_info["file_not_found"], parse_mode="HTML",
                               reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]),)
        return

    if message.audio.file_size > 20 * 1024 * 1024:
        await message.delete()
        await bot.send_message(message.chat.id, text=start_msg_info["file_2_big"], parse_mode="HTML",
                               reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]))
        return

    file_handler = await bot.send_message(message.chat.id, text=start_msg_info["file_handler"], parse_mode="HTML")
    file: Audio = message.audio
    file_obj: File = await bot.get_file(file.file_id)
    file_path: str = file_obj.file_path
    downloaded_file: io.BufferedReader = await bot.download_file(file_path)
    file_name: str = file.file_name.replace(" ", "_")

    try:
        start_load = await bot.send_message(message.chat.id, text=start_msg_info["start_load"], parse_mode="HTML")
        await SFTP.upload_mp3_file(downloaded_file, file_name)
        await bot.send_message(
            message.chat.id,
            text=
            f"Файл\n \"{file_name}\" \nуспешно загружен",
            reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]),
            parse_mode="HTML"
        )

        await file_handler.delete()
        await start_load.delete()
        await message.delete()

    except Exception as e:
        await message.delete()
        await bot.send_message(message.chat.id, f"При загрузке файла произошла ошибка: {e}", reply_markup=InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text="Удалить сообщение", callback_data="delete")]]))
