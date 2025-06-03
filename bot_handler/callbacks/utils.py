# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_content = Msg()

@router.callback_query(F.data == "utils")
async def debug_stick(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.utils()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/guides_icon.png"),
        caption=content["text"],
        parse_mode="HTML"
    )

    await callback.bot.edit_message_media(
        chat_id=original_chat_id,
        message_id=original_message_id,
        media=guides_content,
        reply_markup=content["buttons"]
    )

    await callback.answer("")