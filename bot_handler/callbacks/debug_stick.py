# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_content = Msg()

@router.callback_query(F.data == "debug_stick")
async def debug_stick(callback: CallbackQuery):
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.debug_stick()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/debug_stick.png"),
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

@router.callback_query(F.data == "debug_stick_craft")
async def debug_stick(callback: CallbackQuery):
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.debug_stick_craft()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/debug_stick_craft.png"),
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

@router.callback_query(F.data == "debug_stick_example")
async def debug_stick(callback: CallbackQuery):
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.debug_stick_example()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/debug_stick_example.png"),
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

@router.callback_query(F.data == "debug_stick_use")
async def debug_stick(callback: CallbackQuery):
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.debug_stick_use()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/debug_stick_att.png"),
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