# -*- coding: utf-8 -*-
import logging
from typing import Union
from dataclasses import dataclass, field


@dataclass
class LogConfig:
    level: Union[str, int] = field(default=logging.INFO)  # '日志级别'
