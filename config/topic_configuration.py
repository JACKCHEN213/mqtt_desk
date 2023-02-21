# -*- coding: utf-8 -*-
from config.base import Base, parse_configurator
from config.drive import Json
from pathlib import Path


class TopicConfiguration(Base):
    @staticmethod
    @parse_configurator
    def load_config(filepath: Path):
        return Json.load_config(filepath)

    @staticmethod
    @parse_configurator
    def save_config(filepath: Path, config: dict = None):
        Json.save_config(filepath, config)
