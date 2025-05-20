# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_msg = Msg()

@router.callback_query(F.data == "top_played_time")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.top_played_time()

    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    await callback.bot.edit_message_caption(
        chat_id=original_chat_id,
        message_id=original_message_id,
        caption = start_msg_info["top_played_time_text"],
        reply_markup=start_msg_info["buttons"],
        parse_mode="HTML",
    )
    await callback.answer("")

@router.callback_query(F.data == "refresh")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.top_played_time()

    # Сохраняем исходное сообщение
    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

# Кнопочки убираем
    await callback.bot.edit_message_caption(
        chat_id=original_chat_id,
        message_id=original_message_id,
        caption=start_msg_info["top_played_time_text"],
        parse_mode="HTML"
    )

    # Отправляем новое сообщение о начале обновления
    start_update_msg = await callback.message.answer(start_msg_info["refresh_start_text"])

    # Обновление статистики
    try:
        await SH.refresh_stats()
    except Exception as e:
        await callback.bot.send_message(original_chat_id, f"При обновлении статистики возникла ошибка, сообщите @Zeragorn: {e}")

# Обновление сообщения
    await start_update_msg.delete()
    start_msg_info = await bot_msg.top_played_time()
    await callback.bot.edit_message_caption(
        chat_id=original_chat_id,
        message_id=original_message_id,
        caption=start_msg_info["top_played_time_text"],
        reply_markup=start_msg_info["buttons"],
        parse_mode="HTML"
    )
    await callback.answer(start_msg_info["refresh_done_text"])
