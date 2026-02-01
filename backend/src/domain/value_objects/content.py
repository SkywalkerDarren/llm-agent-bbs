"""Content value object for posts and replies."""

from typing import Any


class Content:
    """Value object for markdown content."""

    MIN_LENGTH = 1
    MAX_LENGTH = 50000

    def __init__(self, value: str) -> None:
        """Initialize content with validation.

        Args:
            value: The markdown content

        Raises:
            ValueError: If content is invalid
        """
        self._validate(value)
        self._value = value

    def _validate(self, value: str) -> None:
        """Validate content.

        Args:
            value: The content to validate

        Raises:
            ValueError: If content is invalid
        """
        if not value or not value.strip():
            raise ValueError("Content cannot be empty")

        if len(value) < self.MIN_LENGTH:
            raise ValueError(f"Content must be at least {self.MIN_LENGTH} character")

        if len(value) > self.MAX_LENGTH:
            raise ValueError(f"Content must be at most {self.MAX_LENGTH} characters")

    @property
    def value(self) -> str:
        """Get the content value."""
        return self._value

    def __str__(self) -> str:
        """String representation."""
        return self._value

    def __repr__(self) -> str:
        """Developer representation."""
        preview = self._value[:50] + "..." if len(self._value) > 50 else self._value
        return f"Content('{preview}')"

    def __eq__(self, other: Any) -> bool:
        """Check equality."""
        if not isinstance(other, Content):
            return False
        return self._value == other._value
