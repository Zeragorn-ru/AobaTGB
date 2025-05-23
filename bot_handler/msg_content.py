# -*- coding: utf-8 -*-
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from mc_server_handler import StatsHandler, SFTPHandler
from boot import config, error

# Настройка SFTP
try:
    SFTP: SFTPHandler = SFTPHandler(
                host=config["host"],
                port=config["port"],
                username=config["username"],
                password=config["password"]
            )

    SH: StatsHandler = StatsHandler(
        SFTP
    )
except Exception as e:
    error(f"При создании SFTP соединения произошла ошибка: {e}")
# Создание класса статы


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
            "• Просмотр онлайна\n"
            "• История изменений\n"
            "• Гайды \nИ другое!\n\n"
            "Версия: <a href=\"https://github.com/Zeragorn-ru/AobaTGB\">1.3.3a</a>\n"
            "<i>Dev by @Zeragorn</i>"
        )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🕒 Топ времени", callback_data="top_played_time"),
                InlineKeyboardButton(text="📕 Гайды [WIP]", callback_data="guides")
            ],
            [InlineKeyboardButton(text="❤ Спасибо <3", callback_data="gratitude")],
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

    async def guides(self) -> dict[str: str]:
        text = ("<b>📖 Гайды!</b>\n\n"
                "Полезная информация о не-ванильных механиках сервера:\n"
                "🪄 <b>Гайд по палочке отладки</b>\n\n"
                "📌 В разработке:\n"
                "• Гайд по кастомной музыке\n"
                "• Гайд по скинам\n"
                "• Починка предметов накопленным опытом\n"
                "• Гайд по стойкам для брони\n"
                )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🪄 Палочка отладки", callback_data="debug_stick")],
            [InlineKeyboardButton(text="<- Назад", callback_data="start")]
        ])

        return {
            "text": text,
            "buttons": buttons
        }

    async def debug_stick_craft(self) -> dict[str: str]:
        text = ("🪄 Палочка отладки - <b>Крафт</b>\n\n"
                "Ресурсы:\n"
                "• Алмаз - 1\n"
                "• Палка - 2"
                )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Информация", callback_data="debug_stick"),
             InlineKeyboardButton(text="Применение", callback_data="debug_stick_use"),
             InlineKeyboardButton(text="Пример", callback_data="debug_stick_example")],
            [InlineKeyboardButton(text="Главная", callback_data="start"),
             InlineKeyboardButton(text="Гайды", callback_data="guides")]
        ])

        return {
            "text": text,
            "buttons": buttons
        }
    async def debug_stick(self) -> dict[str: str]:
        text = ("🪄 Палочка отладки - <b>Информация</b>\n\n"
                "Палочка отладки - мощный инструмент в умелых руках. Она может менять состояние болоков, такие как: поворот, затопленость, горение и тд"
                )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Крафт", callback_data="debug_stick_craft"),
             InlineKeyboardButton(text="Применение", callback_data="debug_stick_use"),
             InlineKeyboardButton(text="Пример", callback_data="debug_stick_example")],
            [InlineKeyboardButton(text="Главная", callback_data="start"),
             InlineKeyboardButton(text="Гайды", callback_data="guides")]
        ])

        return {
            "text": text,
            "buttons": buttons
        }

    async def debug_stick_example(self) -> dict[str: str]:
        text = ("🪄 Палочка отладки - <b>Пример</b>\n\n"
                "Как видно на картинке:\n"
                "• Zeragorn выбрал состояние ЛКМ\n"
                "• А затем изменил его с False на True\n\n"
                "Таким образом с западной стороны забора появилось соединение, которое натурально там находиться не могло"
                )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Крафт", callback_data="debug_stick_craft"),
             InlineKeyboardButton(text="Применение", callback_data="debug_stick_use"),
             InlineKeyboardButton(text="Описание", callback_data="debug_stick")],
            [InlineKeyboardButton(text="Главная", callback_data="start"),
             InlineKeyboardButton(text="Гайды", callback_data="guides")]
        ])

        return {
            "text": text,
            "buttons": buttons
        }

    async def debug_stick_use(self) -> dict[str: str]:
        text = ("🪄 Палочка отладки - <b>Применение</b>\n\n"
                "Палочка отладки позволяет менять <a href=\"https://minecraft.fandom.com/ru/wiki/%D0%A1%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F_%D0%B1%D0%BB%D0%BE%D0%BA%D0%BE%D0%B2\">состояния</a> "
                "блоков, что делает ее незаменимым инструментом в декоре и строительстве\n\n"
                "Применение:\n"
                "• При клике ЛКМ по блоку меняется состояние\n"
                "• При клике ПКМ по блоку меняется значение выбранного состояние\n"
                "• При использовании вместе с кнопкой приседания значения и состояния переключаются в обратном порядке"
                )

        buttons = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Крафт", callback_data="debug_stick_craft"),
             InlineKeyboardButton(text="Пример", callback_data="debug_stick_example"),
             InlineKeyboardButton(text="Описание", callback_data="debug_stick")],
            [InlineKeyboardButton(text="Главная", callback_data="start"),
             InlineKeyboardButton(text="Гайды", callback_data="guides")]
        ])

        return {
            "text": text,
            "buttons": buttons
        }
    async def gratitude(self) -> dict[str: str]:
        text = ("""
        Спасибо вам за всё, что вы сделали для меня ❤

• Sonazavar209 — за инструменты и поддержку в разработке проекта
• Pamela — за моральную и финансовую помощь, а также за конструктивную критику
• Clown_505 — за поддержку и тёплые отзывы о моей работе

Отдельное спасибо Omlettik'у — именно ты уговорил запустить первый сервер
        """)

        buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="<- Назад 💜", callback_data="start")]])

        return {
            "text": text,
            "buttons": buttons
        }