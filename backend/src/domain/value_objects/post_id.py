"""Post ID value object."""

import uuid
from datetime import datetime
from typing import Any


class PostId:
    """Value object for post IDs."""

    def __init__(self, value: str) -> None:
        """Initialize post ID.

        Args:
            value: The post ID string
        """
        if not value:
            raise ValueError("Post ID cannot be empty")
        self._value = value

    @classmethod
    def generate(cls) -> "PostId":
        """Generate a new unique post ID.

        Returns:
            A new PostId instance
        """
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = uuid.uuid4().hex[:8]
        return cls(f"post_{timestamp}_{unique_id}")

    @property
    def value(self) -> str:
        """Get the post ID value."""
        return self._value

    def __str__(self) -> str:
        """String representation."""
        return self._value

    def __repr__(self) -> str:
        """Developer representation."""
        return f"PostId('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        """Check equality."""
        if not isinstance(other, PostId):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self._value)
