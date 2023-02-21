# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pathlib import Path
import functools


def parse_configurator(func):
    @functools.wraps(func)
    def wrapper(filepath, *args, **kwargs):
        if isinstance(filepath, str):
            filepath = Path(filepath)
        return func(filepath, *args, **kwargs)
    return wrapper


class Base(metaclass=ABCMeta):

    @abstractmethod
    def load_config(self, filepath: Path, *args, **kwargs):
        pass

    @abstractmethod
    def save_config(self, filepath: Path, config: dict, *args, **kwargs):
        pass


__all__ = ['Base', 'parse_configurator']
