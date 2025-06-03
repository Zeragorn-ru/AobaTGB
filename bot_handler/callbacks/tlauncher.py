# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import aiohttp

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_content = Msg()

class InputState(StatesGroup):
    tlauncher = State()

@router.callback_query(F.data == "tlauncher")
async def debug_stick(callback: CallbackQuery, state: FSMContext) -> None:
    original_chat_id = callback.message.chat.id
    original_message_id = callback.message.message_id
    content = await bot_content.tlauncher()

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/icon.png"),
        caption=content["text"],
        parse_mode="HTML"
    )

    await callback.bot.edit_message_media(
        chat_id=original_chat_id,
        message_id=original_message_id,
        media=guides_content,
        reply_markup=content["buttons"]
    )

    await state.set_state(InputState.tlauncher)
    await state.update_data(last=callback)

    await callback.answer("")

@router.message(StateFilter(InputState.tlauncher))
async def handle_input(message: Message, state: FSMContext):
    text: str = message.text
    user_message: Message = message
    content = await bot_content.tlauncher()
    last = (await state.get_data()).get("last")

    guides_content = InputMediaPhoto(
        media=FSInputFile("./assets/icon.png"),
        caption=(
            "<b>👔 Загрузка скинов из TLauncher\'a!</b>\n\n"
            f"Ссылка для скачивания: https://tlauncher.ru/catalog/nickname/download/tlauncher_{text}.png\n\n"
            "А так же команды для установки скина на сервере:\n"
            "Стандартные руки:\n"
            f"<code>/skin url https://tlauncher.ru/catalog/nickname/download/tlauncher_{text}.png</code>\n\n"
            "Тонкие руки (slim)\n"
            f"<code>/skin url https://tlauncher.ru/catalog/nickname/download/tlauncher_{text}.png slim</code>"
            ),
        parse_mode="HTML"
    )
    try:
        await message.bot.edit_message_media(
            chat_id=last.message.chat.id,
            message_id=last.message.message_id,
            media=guides_content,
            reply_markup=content["buttons"]
        )
    except Exception:
        pass

    await user_message.delete()
