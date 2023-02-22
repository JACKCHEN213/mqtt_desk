# -*- coding: utf-8 -*-
from config.base import Base
from configparser import ConfigParser
from pathlib import Path


class Ini(Base):

    @staticmethod
    def save_config(filepath: Path, config: dict, *args, **kwargs):
        configurator = ConfigParser()
        if filepath.is_file():
            configurator.read(filepath, encoding='utf8')
        for section, item in config.items():
            if not isinstance(item, dict):
                continue
            if section not in configurator.sections():
                configurator.add_section(section)
            for option, value in item.items():
                configurator.set(section, option, value.__str__())
        configurator.write(open(filepath, 'w', encoding='utf8'))

    @staticmethod
    def load_config(filepath: Path, *args, **kwargs) -> dict:
        ret = {}
        if filepath.is_file():
            configurator = ConfigParser()
            configurator.read(filepath, encoding='utf8')
            for section, item in configurator.items():
                ret[section] = {}
                for option in item:
                    ret[section][option] = configurator.get(section, option)
        return ret


__all__ = ['Ini']
