# -*- coding: utf-8 -*-
import io
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from boot import config, debug, info, warn, error, critical, restart_program
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

class msg:
    def __init__(self):
        pass

    async def start(self):

        played_time: Dict[str, float] = await SH.get_played_time()
        played_time_formated:str = "\n".join([f"{name} - {time} ч." for name, time in played_time])

        start_text = ("Я бот сервера aoba.lol\n"
                 "Краткая статистика задротинга:\n\n"
                 f"{played_time_formated}")

        start_buttons = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Обновить статистику", callback_data="refresh")],
            [InlineKeyboardButton(text="Карта", url='http://map.aoba.lol:23748/')]
        ]
        )

        start_msg = {
            "text": start_text,
            "buttons": start_buttons
        }
        return start_msg

bot_msg = msg()

async def admin_alert(alert: str):
    for recipient in config["alert_recipient"]:
        await bot.send_message(recipient, text=alert)

@router.message(Command("start"))
async def start_command(message: types.Message):

    start_msg_info = await bot_msg.start()

    await bot.send_message(message.chat.id,
                           text = start_msg_info["text"],
                           reply_markup = start_msg_info["buttons"])

@router.callback_query(F.data == "refresh")
async def refresh_button(callback: CallbackQuery):
    # Сохраняем исходное сообщение
    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    # Отправляем новое сообщение о начале обновления
    start_update_msg = await callback.message.answer("Начато обновление статистики, пожалуйста подождите")

    # Обновление статистики
    await SH.refresh_stats()

    # Удаляем сообщение о процессе
    await start_update_msg.delete()

    # Уведомление пользователя о завершении обновления
    await callback.answer("Статистика успешно обновлена")

    buttons = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Карта", url='http://map.aoba.lol:23748/')],
        [InlineKeyboardButton(text="Обновить статистику", callback_data="refresh")]
    ]
    )

    # Редактируем исходное сообщение
    await callback.bot.edit_message_text(
        chat_id=original_chat_id,
        message_id=original_message_id,
        text = await bot_msg.start(),
        reply_markup=buttons
    )


@router.message(Command("file"))
async def file_command(message: types.Message):

    if not message.audio:
        await bot.send_message(message.chat.id,"Сообщение не содержит медиа файл")
        return

    if message.audio.file_size > 20 * 1024 * 1024:
        await bot.send_message(message.chat.id, "Файл больше 20МБ, увы я не могу его загрузить")
        return

    file_handler = await bot.send_message(message.chat.id, "Обработка файла")
    file:Audio = message.audio
    file_obj: File = await bot.get_file(file.file_id)
    file_path:str = file_obj.file_path
    downloaded_file:io.BufferedReader = await bot.download_file(file_path)
    file_name:str = file.file_name.replace(" ", "_")

    try:
        start_handler = await bot.send_message(message.chat.id, "Начата загрузка файла")
        await DL.upload_mp3_file(downloaded_file, file_name)
        end_handler = await bot.send_message(message.chat.id, f"Файл\n \"{file_name}\" \nуспешно загружен\n\n"
                                                              "!Это сообщение будет удалено через 10 секунд!")

        await file_handler.delete()
        await start_handler.delete()
        await message.delete()
        await asyncio.sleep(10)
        await end_handler.delete()

    except Exception as e:
        await bot.send_message(message.chat.id, f"При загрузке файла произошла ошибка: {e}")

@router.message(Command("kill"))
async def kill_command(message: types.Message):
    await bot.send_message(message.chat.id, "Бот выключен")
    await critical("Бот убит")
    sys.exit(0)

@router.message(Command("restart"))
async def kill_command(message: types.Message):
    await bot.send_message(message.chat.id, "Бот остановлен")
    await critical("Бот остановлен")
    restart_program()

async def main():
    dp.include_router(router)
    await SH.refresh_stats()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

