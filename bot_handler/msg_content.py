# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from mc_server_handler import StatsHandler, SFTPHandler
from boot import config

# Настройка SFTP
SFTP: SFTPHandler = SFTPHandler(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )

# Создание класса статы
SH: StatsHandler = StatsHandler(
   SFTP
)

# Класс сообщений
class Msg:
    def __init__(self):
        self.img = "./assets/icon.png"

    async def start(self) -> dict[str, any]:
        start_text: str = (
            "<b>Привет!</b> Я бот сервера <b><a href='https://aoba.lol'>aoba.lol</a></b>\n\n"
            "Вот что я умею:\n"
            "🕒 <b>Топ по наигранному времени</b>\n"
            "🎵 <b>Загрузка своей музыки</b>\n"
            "(Прикрепи .mp3 к сообщению с командой <code>/file</code>)\n"
            "🗺️ <b>Просмотр карты</b>\n\n"
            "🚧 <b>Планируется:</b>\n"
            "• Скины из TLauncher\n"
            "• Онлайн-статистика\n"
            "• История изменений\n"
            "• Гайды и другое!\n\n"
            "Версия: <a href=\"https://github.com/Zeragorn-ru/AobaTGB\">1.1.2b</a>\n"
            "<i>Dev by @Zeragorn</i>"
        )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🕒 Топ времени", callback_data="top_played_time")],
            [InlineKeyboardButton(text="🗺️ Карта", url="https://aoba.lol/")]
        ])

        return {
            "start_text": start_text,
            "buttons": buttons
        }

    async def top_played_time(self) -> dict:
        played_time: Dict[str, float] = await SH.get_played_time()
        played_time_formated: str = "\n".join([
            f"• <b>{name}</b> — {time:.1f} ч." for name, time in played_time
        ])

        top_played_time_text: str = (
            "<b>🏆 Топ по наигранному времени:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"{played_time_formated}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )

        refresh_start_text = "🔄 Начато обновление статистики. Подождите..."
        refresh_done_text = "✅ Статистика обновлена!"

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh")],
            [InlineKeyboardButton(text="<- Назад", callback_data="start")]
        ])

        return {
            "top_played_time_text": top_played_time_text,
            "buttons": buttons,
            "refresh_start_text": refresh_start_text,
            "refresh_done_text": refresh_done_text
        }

    async def file(self) -> dict[str: str]:
        return {
            "file_not_found": "⚠️ Сообщение не содержит медиафайл",
            "file_2_big": "📦 Файл превышает 20МБ — загрузка невозможна",
            "file_handler": "🛠️ Начата обработка файла...",
            "start_load": "📤 Загрузка файла начата"
        }
