# -*- coding: utf-8 -*-
import os
import sys

from boot.config_handler import config
from boot.alert_module import debug, info, warn, error, critical

def restart_program():
    python = sys.executable
    os.execv(python, [python] + sys.argv)