# -*- coding: utf-8 -*-
from bot_handler.msg_content import SH

from bot_handler.bot_demon import dp
from bot_handler.bot_demon import router as demon
from bot_handler.comands.start import router as start
from bot_handler.comands.file import router as file

from bot_handler.callbacks.top_played_time import router as players_top
from bot_handler.callbacks.guides import router as guides

from bot_handler.callbacks.debug_stick import router as debug_stick
from bot_handler.callbacks.gratitude import router as gratitude
from bot_handler.callbacks.utils import router as utils
from bot_handler.callbacks.tlauncher import router as tlauncher

routers = [start, demon, players_top, file, guides, debug_stick, gratitude, utils, tlauncher]