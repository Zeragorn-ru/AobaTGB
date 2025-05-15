from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from mc_server_handler import StatsHandler, SFTPHandler
from boot import config

SFTP: SFTPHandler = SFTPHandler(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )

# Класс статистики
SH: StatsHandler = StatsHandler(
   SFTP
)

class Msg:
    async def start(self) -> dict[str: any]:
        start_text:str = (
            "Привет, я бот сервера <b>aoba.lol</b>\n\n"
            "С помощью меня ты можешь:\n"
            "• Посмотреть топ наигранного времени\n"
            "• Загрузить СВОЮ музыку на сервер\n(Прикрепите mp3 к сообщению \"/file\")\n"
            "• Просмотр карты\n"
            "Планируется добавить:\n"
            "• Получение скинов из TLauncher\'a\n"
            "• Просмотр онлайна\n"
            "• Change log\n"
            "• Гайды"
            "и многое другое!\n\n"
            "Версия: <a href=\"https://github.com/Zeragorn-ru/AobaTGB\">1.0.2a</a> \nDev by <b>@Zeragorn</b>"
        )

        buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Топ наигранного времени", callback_data="top_played_time")],
            [InlineKeyboardButton(text="Карта", url="https://aoba.lol")]
        ]
        )

        return {
            "start_text": start_text,
            "buttons": buttons
        }

    async def top_played_time(self) -> dict:

        played_time: Dict[str, float] = await SH.get_played_time()
        played_time_formated: str = "\n".join([f"{name} - {time} ч." for name, time in played_time])

        top_played_time_text: str = (
            "Топ наигранного времени:\n"
            "===========================\n"
            f"{played_time_formated}\n"
            "===========================\n"
        )

        refresh_start_text = "Начато обновление статистики, пожалуйста подождите"
        refresh_done_text = "Статистика успешно обновлена"

        buttons: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=
        [
            [InlineKeyboardButton(text="Обновить статистику", callback_data="refresh")],
            [InlineKeyboardButton(text="<- Назад", callback_data="start")]
        ]
        )

        start_msg: dict[str: Any] = {
            "top_played_time_text": top_played_time_text,
            "buttons": buttons,
            "refresh_start_text": refresh_start_text,
            "refresh_done_text": refresh_done_text
        }
        return start_msg

    async def file(self) -> dict[str: str]:
        file_not_found: str = "Сообщение не содержит медиа файл"
        file_2_big: str = "Файл больше 20МБ, увы я не могу его загрузить"
        file_handler: str = "Обработка файла"
        start_load: str = "Начата загрузка файла"

        return {
            "file_not_found": file_not_found,
            "file_2_big": file_2_big,
            "file_handler": file_handler,
            "start_load": start_load
        }
