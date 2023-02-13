# -*- coding: utf-8 -*-
from config.base import Base
from configparser import ConfigParser
from pathlib import Path


class Ini(Base):

    __driver: ConfigParser = None

    @property
    def configurator(self) -> ConfigParser:
        if self.__driver is None:
            self.__driver = ConfigParser()
        return self.__driver

    def save_config(self, filepath: Path, config: dict):
        if filepath.is_file():
            self.configurator.read(filepath)
        for section, item in config.items():
            if not isinstance(item, dict):
                continue
            if section not in self.configurator.sections():
                self.configurator.add_section(section)
            for option, value in item.items():
                self.configurator.set(section, option, value.__str__())
        self.configurator.write(open(filepath, 'w'))

    def load_config(self, filepath: Path) -> dict:
        ret = {}
        if filepath.is_file():
            self.configurator.read(filepath)
            for section, item in self.configurator.items():
                ret[section] = {}
                for option in item:
                    ret[section][option] = self.configurator.get(section, option)
        return ret


__all__ = ['Ini']
