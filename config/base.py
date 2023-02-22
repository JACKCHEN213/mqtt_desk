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

    @staticmethod
    @abstractmethod
    def load_config(filepath: Path, *args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def save_config(filepath: Path, config: dict, *args, **kwargs):
        pass


__all__ = ['Base', 'parse_configurator']
