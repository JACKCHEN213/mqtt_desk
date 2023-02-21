# -*- coding: utf-8 -*-
from config.base import Base, parse_configurator
from config.drive.ini import Ini
from model.mqtt import MqttConfig
from pathlib import Path


class MqttConfiguration(Base):
    @staticmethod
    @parse_configurator
    def load_config(filepath: Path, configurator: Base = Ini()):
        config = configurator.load_config(filepath)
        return MqttConfig(**config.get('mqtt', dict()), config_file=filepath.__str__())

    @staticmethod
    @parse_configurator
    def save_config(filepath: Path, config: dict = None, configurator: Base = Ini()):
        configurator.save_config(filepath, config)
