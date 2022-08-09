"""
    Base modules for various projects:

    ## log
    Basic log wrapper for structlog and json-logger, and contains an argument/return
    decorator.

    ## tempfile
    A decorator to manage the contents of a temporary folder, which is automatically
    removed when the code block is done.

    ## timer
    A decorator and contextmanager to time a code block.

    file  : src/base/__init__.py
    since : 2022-07-04
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version

from .timer import Timer
from .tempfile import TempfileManager
from .debug import debug


try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    try:
        from ._version import version as __version__
    except ModuleNotFoundError:
        __version__: str = "unknown version"
