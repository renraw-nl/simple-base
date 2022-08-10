"""
    file  : src/base/debug.py
    since : 2022-08-09
"""

import functools
from typing import Any, Callable, Optional

from . import log


def debug(func: Callable, name: Optional[str] = "Argument logger") -> Callable:
    """
    Decorator to log arguments and results passed to a method.
    """
    logger = log.get_logger(name)

    @functools.wraps(func)
    def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        logger.debug(f"Logging arguments for {func.__name__}", args=args, kwargs=kwargs)

        results = func(*args, **kwargs)

        logger.debug(f"\u21B3 Logging results for {func.__name__}", results=results)
        return results

    return wrapper
