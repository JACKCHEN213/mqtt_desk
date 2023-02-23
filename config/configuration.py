# -*- coding: utf-8 -*-
from config.base import Base, parse_configurator
from config.drive.ini import Ini
from pathlib import Path
from typing import Type


class Configuration(Base):
    @staticmethod
    @parse_configurator
    def load_config(filepath: Path, configurator: Type[Base] = Ini):
        return configurator.load_config(filepath)

    @staticmethod
    @parse_configurator
    def save_config(filepath: Path, config: dict = None, configurator: Type[Base] = Ini):
        configurator.save_config(filepath, config)
