"""
    A Decorator to time methods of parts of code within a Context (e.g. with Timer as t)

    https://realpython.com/python-timer/

    File   : src/base / timer.py
    Since  : 2022-07-04
"""

import time
from contextlib import ContextDecorator
from typing import Any, Optional

import structlog

from . import log


class Timer(ContextDecorator):
    """
    Timer context decorator

    ```py
    from base import Timer
    from time import sleep

    @Timer('a message', logger)
    def run_long_code():
        sleep(30)
    ```
    """

    start: float
    logger: structlog.BoundLoggerBase
    msg: str = "Timed duration"

    def __init__(
        self,
        msg: Optional[str] = None,
        logger: Optional[structlog.BoundLoggerBase] = None,
    ) -> None:
        self.__start(msg, logger)

    def __start(
        self,
        msg: Optional[str] = None,
        logger: Optional[structlog.BoundLoggerBase] = None,
    ) -> None:
        if msg:
            self.msg = msg

        if isinstance(logger, structlog.BoundLoggerBase):
            self.logger = logger
        else:
            self.logger = log.get_logger(self.__class__.__name__)

    def __enter__(
        self,
        msg: Optional[str] = None,
        logger: Optional[structlog.BoundLoggerBase] = None,
    ) -> "Timer":
        self.__start(msg, logger)
        self.start = time.perf_counter()

        return self

    def __exit__(self, *exc_info: tuple[Any]) -> None:
        stop = time.perf_counter()
        self.logger.debug(self.msg, timed_duration=round((stop - self.start), 3))
