# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical

router: Router = Router()
bot_content = Msg()

@router.callback_query(F.data == "guides")
async def guides(callback: CallbackQuery):
    await callback.answer("test")