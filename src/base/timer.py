"""
    A Decorator to time methods of parts of code within a Context (eg with Timer as t)

    https://realpython.com/python-timer/

    File   : src/base / timer.py
    Since  : 2022-07-04
"""

import time
import typing as t
from contextlib import ContextDecorator

import structlog

from . import log


class Timer(ContextDecorator):
    start: float
    logger: structlog.BoundLoggerBase
    msg: str = "Timed duration"

    def __init__(self, msg: t.Optional[str] = None):
        if msg:
            self.msg = msg

        self.logger = log.get_logger(self.__class__.__name__)

    def __enter__(self, msg: t.Optional[str] = None) -> "Timer":
        self.start = time.perf_counter()

        if msg:
            self.msg = msg

        return self

    def __exit__(self, *exc_info):
        stop = time.perf_counter()
        self.logger.debug(self.msg, timed_duration=round((stop - self.start), 3))
