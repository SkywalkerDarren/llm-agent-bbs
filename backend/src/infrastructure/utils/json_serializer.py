"""JSON serializer utility."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class JSONSerializer:
    """Utility for JSON serialization with custom handling."""

    @staticmethod
    def serialize(data: Any) -> str:
        """Serialize data to JSON string.

        Args:
            data: Data to serialize

        Returns:
            JSON string
        """
        return json.dumps(data, indent=2, ensure_ascii=False, default=JSONSerializer._default)

    @staticmethod
    def deserialize(json_str: str) -> Any:
        """Deserialize JSON string to data.

        Args:
            json_str: JSON string

        Returns:
            Deserialized data
        """
        return json.loads(json_str)

    @staticmethod
    def load_file(file_path: Path) -> Any:
        """Load JSON from file.

        Args:
            file_path: Path to JSON file

        Returns:
            Deserialized data
        """
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_file(file_path: Path, data: Any) -> None:
        """Save data to JSON file.

        Args:
            file_path: Path to JSON file
            data: Data to save
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=JSONSerializer._default)

    @staticmethod
    def _default(obj: Any) -> Any:
        """Default serializer for custom types.

        Args:
            obj: Object to serialize

        Returns:
            Serializable representation
        """
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
