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


try:
    __version__ = version(__name__)
except PackageNotFoundError:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown version"
