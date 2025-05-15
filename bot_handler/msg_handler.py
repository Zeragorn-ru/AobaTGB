import asyncio
from aiogram import Bot, Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

from bot_handler.msg_content import Msg, SH, SFTP
from boot import debug, info, warn, error, critical, restart_program, config

router: Router = Router()
bot_msg = Msg()

@router.message(Command("start"))
async def start_command(message: types.Message):
    bot = message.bot
    start_msg_info = await bot_msg.start()

    await bot.send_message(message.chat.id,
                           text = start_msg_info["start_text"],
                           reply_markup = start_msg_info["buttons"],
                           parse_mode="HTML",
                           disable_web_page_preview=True
                           )

@router.callback_query(F.data == "start")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.start()

    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    await callback.bot.edit_message_text(
        chat_id=original_chat_id,
        message_id=original_message_id,
        text = start_msg_info["start_text"],
        reply_markup=start_msg_info["buttons"],
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@router.callback_query(F.data == "top_played_time")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.top_played_time()

    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    await callback.bot.edit_message_text(
        chat_id=original_chat_id,
        message_id=original_message_id,
        text = start_msg_info["top_played_time_text"],
        reply_markup=start_msg_info["buttons"],
        parse_mode="HTML",
    )

@router.callback_query(F.data == "refresh")
async def refresh_button(callback: CallbackQuery):
    start_msg_info = await bot_msg.top_played_time()
    # Сохраняем исходное сообщение
    original_message_id = callback.message.message_id
    original_chat_id = callback.message.chat.id

    await callback.bot.edit_message_text(
        chat_id=original_chat_id,
        message_id=original_message_id,
        text=start_msg_info["top_played_time_text"],
        parse_mode="HTML"
    )

    # Отправляем новое сообщение о начале обновления
    start_update_msg = await callback.message.answer(start_msg_info["refresh_start_text"])

    # Обновление статистики
    await SH.refresh_stats()

    # Удаляем сообщение о процессе
    await start_update_msg.delete()

    # Уведомление пользователя о завершении обновления
    await callback.answer(start_msg_info["refresh_done_text"])

    # Редактируем исходное сообщение
    await callback.bot.edit_message_text(
        chat_id=original_chat_id,
        message_id=original_message_id,
        text = start_msg_info["top_played_time_text"],
        reply_markup=start_msg_info["buttons"],
        parse_mode="HTML"
    )


@router.message(Command("file"))
async def file_command(message: types.Message):
    bot = message.bot
    start_msg_info = await bot_msg.file()

    if not message.audio:
        await bot.send_message(message.chat.id, text=start_msg_info["file_not_found"],
        parse_mode="HTML")
        return

    if message.audio.file_size > 20 * 1024 * 1024:
        await bot.send_message(message.chat.id, text=start_msg_info["file_2_big"],
        parse_mode="HTML")
        return

    file_handler = await bot.send_message(message.chat.id, text=start_msg_info["file_handler"],
        parse_mode="HTML")
    file:Audio = message.audio
    file_obj: File = await bot.get_file(file.file_id)
    file_path:str = file_obj.file_path
    downloaded_file:io.BufferedReader = await bot.download_file(file_path)
    file_name:str = file.file_name.replace(" ", "_")

    try:
        start_load = await bot.send_message(message.chat.id, text=start_msg_info["start_load"],
        parse_mode="HTML")
        await SFTP.upload_mp3_file(downloaded_file, file_name)
        end_load = await bot.send_message(message.chat.id, f"Файл\n \"{file_name}\" \nуспешно загружен\n\n"
                                                              "!Это сообщение будет удалено через 10 секунд!",
                                          parse_mode="HTML"
                                          )

        await file_handler.delete()
        await start_load.delete()
        await message.delete()
        await asyncio.sleep(10)
        await end_load.delete()

    except Exception as e:
        await bot.send_message(message.chat.id, f"При загрузке файла произошла ошибка: {e}")

@router.message(Command("kill"))
async def kill_command(message: types.Message):
    bot = message.bot
    if message.chat.id not in config["alert_recipient"]:
        await bot.send_message(message.chat.id, "403, not enough permissions")
        await message.delete()
        return None
    await bot.send_message(message.chat.id, "Бот выключен")
    await critical("Бот убит")
    sys.exit(-1)

@router.message(Command("restart"))
async def kill_command(message: types.Message):
    bot = message.bot
    if message.chat.id not in config["alert_recipient"]:
        await bot.send_message(message.chat.id, "403, not enough permissions")
        await message.delete()
        return None
    await bot.send_message(message.chat.id, "Бот перезапускается")
    await critical("Бот остановлен")
    restart_program()