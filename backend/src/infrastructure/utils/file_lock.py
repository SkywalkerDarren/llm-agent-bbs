"""File lock utility for preventing concurrent writes."""

import fcntl
import os
from pathlib import Path
from typing import Any


class FileLock:
    """Context manager for file locking."""

    def __init__(self, lock_file: Path) -> None:
        """Initialize file lock.

        Args:
            lock_file: Path to lock file
        """
        self.lock_file = lock_file
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        self._fd: int | None = None

    def __enter__(self) -> "FileLock":
        """Acquire the lock."""
        self._fd = os.open(self.lock_file, os.O_CREAT | os.O_RDWR)
        fcntl.flock(self._fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Release the lock."""
        if self._fd is not None:
            fcntl.flock(self._fd, fcntl.LOCK_UN)
            os.close(self._fd)
            self._fd = None
