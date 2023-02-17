# -*- coding: utf-8 -*-
from config.base import Base
from config.drive.ini import Ini
from model.mqtt import MqttConfig
from pathlib import Path
import functools


default_configurator = Ini()


def parse_configurator(func):
    @functools.wraps(func)
    def wrapper(filepath, configurator=None, *args, **kwargs):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if configurator is None:
            configurator = default_configurator
        return func(filepath, configurator, *args, **kwargs)
    return wrapper


class MqttConfiguration:

    @staticmethod
    @parse_configurator
    def get_config(filepath: Path, configurator: Base = None):
        config = configurator.load_config(filepath)
        return MqttConfig(**config.get('mqtt', dict()), config_file=filepath.__str__())

    @staticmethod
    @parse_configurator
    def set_config(filepath: Path, configurator: Base = None, config: dict = None):
        configurator.save_config(filepath, config)
