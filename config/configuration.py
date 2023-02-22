# -*- coding: utf-8 -*-
from config.base import Base, parse_configurator
from config.drive.ini import Ini
from pathlib import Path
from typing import ClassVar


class Configuration(Base):
    @staticmethod
    @parse_configurator
    def load_config(filepath: Path, configurator: ClassVar[Base] = Ini):
        return configurator.load_config(filepath)

    @staticmethod
    @parse_configurator
    def save_config(filepath: Path, config: dict = None, configurator: ClassVar[Base] = Ini):
        configurator.save_config(filepath, config)
