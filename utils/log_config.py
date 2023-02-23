# -*- coding: utf-8 -*-
import logging
from typing import Union
from pydantic import BaseModel, Field


class LogConfig(BaseModel):
    level: Union[str, int] = Field(default=logging.INFO, description='日志级别')
