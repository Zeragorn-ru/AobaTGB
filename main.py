# -*- coding: utf-8 -*-
from os import getenv, path

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
import asyncio

# Загрузка конфига
from config_handler import config

# Настройки логирования
from tglog_module import debug, info, warn, error, critical

# Создание классов для работы бота
dp = Dispatcher()
router = Router()
bot = Bot(token = config["bot_token"]) # Создание класса бота

debug("sosal?")

@router.message(Command("Start"))
def start_command(message):
    bot.send_message(message.chat_id, "aoba.lol")