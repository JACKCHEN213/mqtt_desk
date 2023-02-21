# -*- coding: utf-8 -*-
from config.base import Base
from pathlib import Path
import json


class Json(Base):
    @staticmethod
    def load_config(filepath: Path, *args, **kwargs):
        if not filepath.is_file():
            return {}
        with open(filepath, 'r') as fp:
            return json.load(fp)

    @staticmethod
    def save_config(filepath: Path, config: dict, *args, **kwargs):
        if not filepath.is_file():
            with open(filepath, 'w+') as fp:
                json.dump(config, fp)
        else:
            content = Json.load_config(filepath)
            if not isinstance(content, dict):
                with open(filepath, 'w+') as fp:
                    json.dump(config, fp)
            else:
                for key, value in config.items():
                    content[key] = value
                with open(filepath, 'w+') as fp:
                    json.dump(content, fp)


__all__ = ['Json']
