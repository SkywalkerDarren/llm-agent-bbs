"""Tags value object."""

from typing import Any


class Tags:
    """Value object for post tags."""

    MAX_TAGS = 10
    MAX_TAG_LENGTH = 30

    def __init__(self, values: list[str]) -> None:
        """Initialize tags with validation.

        Args:
            values: List of tag strings

        Raises:
            ValueError: If tags are invalid
        """
        self._validate(values)
        self._values = [tag.strip().lower() for tag in values]

    def _validate(self, values: list[str]) -> None:
        """Validate tags.

        Args:
            values: List of tags to validate

        Raises:
            ValueError: If tags are invalid
        """
        if len(values) > self.MAX_TAGS:
            raise ValueError(f"Cannot have more than {self.MAX_TAGS} tags")

        for tag in values:
            # Trim the tag for validation
            trimmed_tag = tag.strip()

            if not trimmed_tag:
                raise ValueError("Tag cannot be empty")

            if len(trimmed_tag) > self.MAX_TAG_LENGTH:
                raise ValueError(f"Tag must be at most {self.MAX_TAG_LENGTH} characters")

            if not trimmed_tag.replace("-", "").replace("_", "").isalnum():
                raise ValueError("Tags can only contain letters, numbers, hyphens, and underscores")

    @property
    def values(self) -> list[str]:
        """Get the list of tags."""
        return self._values.copy()

    def __iter__(self):
        """Make tags iterable."""
        return iter(self._values)

    def __len__(self) -> int:
        """Get number of tags."""
        return len(self._values)

    def __str__(self) -> str:
        """String representation."""
        return ", ".join(self._values)

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Tags({self._values})"

    def __eq__(self, other: Any) -> bool:
        """Check equality."""
        if not isinstance(other, Tags):
            return False
        return set(self._values) == set(other._values)
