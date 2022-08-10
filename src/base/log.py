"""
    Log

    Provide basic wrapper for Structlog and reroute stdlib.logging to
    json-logger to ensure output is similar to Structlog.

    See:
    1. https://www.structlog.org/en/stable/
    2. https://codywilbourn.com/2018/08/23/playing-with-python-structured-logs/
    3. https://limkopi.me/a-better-logging-with-python-logging-structlog-and-pythonjsonlogger/

    TODO:
    1. Implement configuration for init().

    File   : src/base / log.py
    Since  : 2022-07-04
"""

import logging
import sys
from typing import Any, Optional

import structlog
from pythonjsonlogger import jsonlogger


def init(debug: Optional[bool] = False) -> None:
    """
    Initialise the stdlib logging and structlog libraries.

    :param debug: log level is set to logging.DEBUG when True, logging.INFO otherwise.
    :return:
    """

    # Only initialise once.
    if not structlog.is_configured():
        structlog.configure(
            processors=[
                # structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                # structlog.stdlib.render_to_log_kwargs,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.UnicodeDecoder(),
                # structlog.dev.set_exc_info,
                structlog.dev.ConsoleRenderer(),
                # Render the final event dict as JSON.
                # structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Determine the log level
        if debug is True:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        # Prepare the built-in logger to show similar output as structlog
        json_handler = logging.StreamHandler(sys.stdout)
        json_handler.setFormatter(jsonlogger.JsonFormatter())
        logging.basicConfig(
            format="%(message)s",
            handlers=[
                json_handler,
            ],
            level=log_level,  # Or whatever the general level should be
        )


def get_logger(
    name: Optional[str] = None, **kwargs: dict[str, Any]
) -> structlog.BoundLoggerBase:
    """
    Return a structlog logger instance, optionally named.

    :param name: Optional name of the logger instance.
    :param kwargs: Keyword arguments to the log message.
    :return: structlog logger
    """

    # Call init() if not already configured.
    if not structlog.is_configured():
        init()

    # Get and return the logger
    if name is not None:
        return structlog.getLogger(name, **kwargs)
    else:
        return structlog.getLogger(**kwargs)
