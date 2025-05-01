# -*- coding: utf-8 -*-
import logging

file_log = logging.FileHandler('./Log.log')
console_out = logging.StreamHandler()

level_table = {
    "DEBUG": 0,
    "INFO": 1,
    "WARN": 2,
    "ERROR": 3,
    "CRITICAL": 4
}

logging.basicConfig(
    handlers = (file_log, console_out),
    level= "INFO",
    format = "[%(asctime)s][%(module)s][%(levelname)s]: %(message)s"
)