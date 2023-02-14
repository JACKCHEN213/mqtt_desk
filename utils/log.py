# -*- coding: utf-8 -*-
import os
import logging
import colorlog
from pathlib import Path
from typing import Union
import time


class Log:
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
    level = logging.INFO

    def __init__(self, name='log', level: Union[str, int] = logging.INFO):
        self.__logger = logging.getLogger(name)
        self.set_level(level)
        if level := os.getenv('LOG_LEVEL', None):
            if isinstance(level, str) and level.upper() in self.log_levels:
                self.set_level(level)

        formatter = ("%(asctime)s %(filename)s [%(levelname)s] "
                     "(%(name)s,file:%(filename)s,func:%(funcName)s,line:%(lineno)s,pid:%(process)s)"
                     " %(message)s")
        color_config = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bg_red',
        }
        console_formatter = colorlog.ColoredFormatter(fmt='%(log_color)s' + formatter, log_colors=color_config)
        file_formatter = logging.Formatter(fmt=formatter)

        console_handler = logging.StreamHandler()
        file_dir = Path('./log')
        file_dir.mkdir(exist_ok=True, parents=True)
        filename = file_dir / f"{name}-{time.strftime('%Y-%m-%d', time.localtime())}.log"
        file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf-8')

        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    @property
    def logger(self):
        return self.__logger

    def set_level(self, level: Union[str, int]):
        if isinstance(level, str):
            level = level.upper()
        level = level if level in self.log_levels else logging.INFO
        self.level = level
        self.logger.setLevel(level)

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)


__all__ = ['Log']
