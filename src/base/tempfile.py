"""
    Tempfile Context Manager

    To provide a temporary directory and generator for temp file names.

    file  : src/base/ tempfile.py
    since : 2022-07-04
"""

import shutil
from contextlib import ContextDecorator
from pathlib import Path
import tempfile
import os
from typing import Optional, Any

from .utils import get_uuid


class TempfileManager(ContextDecorator):
    tmp_dir: Path
    clean_on_exit: bool = True

    def __init__(
        self,
        tmp_sub_dir: Optional[str] = None,
        clean_on_exit: Optional[bool] = True,
    ) -> None:

        if not tmp_sub_dir:
            tmp_sub_dir = get_uuid()

        tmp_dir = Path(tempfile.tempdir) / tmp_sub_dir
        tmp_dir.resolve(strict=True)
        if not tmp_dir.is_relative_to(tempfile.tempdir):
            raise ValueError(
                f"Given `tmp_sub_dir`({tmp_sub_dir}) results in a dir"
                f"outside of the system's `tempfile.tempdir`"
                f"({tempfile.tempdir})"
            )

        self.tmp_dir = tmp_dir
        self._ensure_tmp_dir()

        self.clean_on_exit = clean_on_exit

    def _ensure_tmp_dir(self) -> None:
        if not self.tmp_dir.exists() or not self.tmp_dir.is_dir():
            self.tmp_dir.mkdir(parents=False, exist_ok=False)

        if not os.access(self.tmp_dir, os.W_OK):
            raise PermissionError(
                f"Unable to write to temporary folder ({self.tmp_dir})"
            )

    def clean_tmp_dir(self) -> None:
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def __enter__(self) -> "TempfileManager":
        self._ensure_tmp_dir()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.clean_on_exit:
            self.clean_tmp_dir()

    def __del__(self) -> None:
        self.clean_tmp_dir()

    def tmp_fn(
        self, prepend: Optional[str] = None, suffix: Optional[str] = None
    ) -> Path:
        self._ensure_tmp_dir()

        prepend = prepend.strip()
        if prepend:
            prepend = f"{prepend} "

        if suffix and suffix[0] != ".":
            suffix = f".{suffix}"

        return Path(self.tmp_dir) / f"{prepend}{get_uuid()}{suffix}"
