# -*- coding: utf-8 -*-
import io

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from boot import config, debug, info, warn, error, critical
from mc_server_handler import StatsHandler, SFTPHandler

# Создание классов для работы бота
dp: Dispatcher= Dispatcher(storage = MemoryStorage())
router: Router = Router()
bot: Bot = Bot(token = config["bot_token"]) # Создание класса бота

DL = SFTPHandler(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )

# Класс статистики
SH: StatsHandler = StatsHandler(
   DL
)


@router.message(Command("start"))
async def start_command(message: types.Message):
    played_time: Dict[str, float] = await SH.get_played_time()
    await bot.send_message(message.chat.id, text = f"{played_time}")

@router.message(Command("refresh"))
async def start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Начато обновление статистики, пожалуйста подождите")
    await SH.refresh_stats()
    await bot.send_message(message.chat.id, "Статистика успешно обновлена")

@router.message(Command("file"))
async def file_command(message: types.Message):

    if not message.audio:
        await bot.send_message(message.chat.id,"Сообщение не содержит медиа файл")
        return

    if message.audio.file_size > 20 * 1024 * 1024:
        await bot.send_message(message.chat.id, "Файл больше 20МБ, увы я не могу его загрузить")
        return

    await bot.send_message(message.chat.id, "Обработка файла")
    file:Audio = message.audio
    file_obj: File = await bot.get_file(file.file_id)
    file_path:str = file_obj.file_path
    downloaded_file:io.BufferedReader = await bot.download_file(file_path)
    file_name:str = file.file_name.replace(" ", "_")

    try:
        await bot.send_message(message.chat.id, "Начата загрузка файла")
        await DL.upload_mp3_file(downloaded_file, file_name)
        await bot.send_message(message.chat.id, "Файл успешно загружен")

    except Exception as e:
        await bot.send_message(message.chat.id, f"При загрузке файла произошла ошибка: {e}")

async def main():
    dp.include_router(router)
    await SH.refresh_stats()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

