"""File storage foundation for the BBS system."""

import shutil
from pathlib import Path
from typing import Any

from src.infrastructure.utils.file_lock import FileLock
from src.infrastructure.utils.json_serializer import JSONSerializer


class FileStorage:
    """Foundation class for file-based storage operations."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize file storage.

        Args:
            data_dir: Root directory for data storage
        """
        self.data_dir = data_dir
        self.posts_dir = data_dir / "posts"
        self.agents_dir = data_dir / "agents"
        self.index_dir = data_dir / "index"
        self.locks_dir = data_dir / ".locks"

        # Create directories
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.locks_dir.mkdir(parents=True, exist_ok=True)

    def read_json(self, path: Path) -> dict[str, Any]:
        """Read JSON file.

        Args:
            path: Path to JSON file

        Returns:
            Deserialized JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return JSONSerializer.load_file(path)

    def write_json(self, path: Path, data: dict[str, Any]) -> None:
        """Write JSON file atomically.

        Args:
            path: Path to JSON file
            data: Data to write
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file first
        temp_path = path.with_suffix(".tmp")
        JSONSerializer.save_file(temp_path, data)

        # Atomic rename
        temp_path.replace(path)

    def read_markdown(self, path: Path) -> str:
        """Read markdown file.

        Args:
            path: Path to markdown file

        Returns:
            File contents

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.read_text(encoding="utf-8")

    def write_markdown(self, path: Path, content: str) -> None:
        """Write markdown file atomically.

        Args:
            path: Path to markdown file
            content: Content to write
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temporary file first
        temp_path = path.with_suffix(".tmp")
        temp_path.write_text(content, encoding="utf-8")

        # Atomic rename
        temp_path.replace(path)

    def get_lock(self, name: str) -> FileLock:
        """Get a file lock for synchronization.

        Args:
            name: Name of the lock

        Returns:
            FileLock instance
        """
        lock_file = self.locks_dir / f"{name}.lock"
        return FileLock(lock_file)

    def list_directories(self, parent_dir: Path) -> list[Path]:
        """List all directories in a parent directory.

        Args:
            parent_dir: Parent directory to list

        Returns:
            List of directory paths
        """
        if not parent_dir.exists():
            return []
        return [p for p in parent_dir.iterdir() if p.is_dir()]

    def directory_exists(self, path: Path) -> bool:
        """Check if a directory exists.

        Args:
            path: Directory path

        Returns:
            True if directory exists
        """
        return path.exists() and path.is_dir()

    def file_exists(self, path: Path) -> bool:
        """Check if a file exists.

        Args:
            path: File path

        Returns:
            True if file exists
        """
        return path.exists() and path.is_file()

    def delete_directory(self, path: Path) -> None:
        """Delete a directory and all its contents.

        Args:
            path: Directory path to delete
        """
        if path.exists():
            shutil.rmtree(path)
