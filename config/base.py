# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from pathlib import Path


class Base(metaclass=ABCMeta):

    @abstractmethod
    def load_config(self, filepath: Path):
        pass

    @abstractmethod
    def save_config(self, filepath: Path, config: dict):
        pass


__all__ = ['Base']
