# -*- coding: utf-8 -*-
#
import os
from .conf import ConfigManager

__all__ = ['BASE_DIR', 'PROJECT_DIR', 'VERSION', 'CONFIG', 'DYNAMIC']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
VERSION = '1.5.9'
CONFIG = ConfigManager.load_user_config()
DYNAMIC = ConfigManager.get_dynamic_config(CONFIG)
