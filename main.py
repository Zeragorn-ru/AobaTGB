# -*- coding: utf-8 -*-
from os import getenv, path

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
import asyncio

from boot import config, debug, info, warn, error, critical

# Создание классов для работы бота
dp = Dispatcher()
router = Router()
bot = Bot(token = config["bot_token"]) # Создание класса бота

debug("debug layer test")
critical("Alert test")

@router.message(Command("Start"))
def start_command(message):
    bot.send_message(message.chat_id, "aoba.lol")