# -*- coding: utf-8 -*-
import inspect
from utils.log import Log

logger = Log()


def caller(func):
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()
        while True:
            try:
                frame = frame.f_back
                logger.debug(frame)
            except Exception as e:
                repr(e)
                break
        return func(*args, **kwargs)

    return wrapper
