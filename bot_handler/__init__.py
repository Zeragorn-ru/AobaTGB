# -*- coding: utf-8 -*-
from bot_handler.msg_content import SH

from bot_handler.bot_demon import dp
from bot_handler.bot_demon import router as demon
from bot_handler.comands.start import router as start
from bot_handler.callbacks.top_played_time import router as players_top
from bot_handler.comands.file import router as file


routers = [start, demon, players_top, file]