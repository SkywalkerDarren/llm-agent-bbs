"""Agent name value object."""

import re
from typing import Any


class AgentName:
    """Value object for agent names with validation."""

    MIN_LENGTH = 3
    MAX_LENGTH = 50
    PATTERN = re.compile(r"^[a-zA-Z0-9_-]+$")

    def __init__(self, value: str) -> None:
        """Initialize agent name with validation.

        Args:
            value: The agent name string

        Raises:
            ValueError: If name is invalid
        """
        self._validate(value)
        self._value = value

    def _validate(self, value: str) -> None:
        """Validate agent name.

        Args:
            value: The agent name to validate

        Raises:
            ValueError: If name is invalid
        """
        if not value:
            raise ValueError("Agent name cannot be empty")

        if len(value) < self.MIN_LENGTH:
            raise ValueError(f"Agent name must be at least {self.MIN_LENGTH} characters")

        if len(value) > self.MAX_LENGTH:
            raise ValueError(f"Agent name must be at most {self.MAX_LENGTH} characters")

        if not self.PATTERN.match(value):
            raise ValueError(
                "Agent name can only contain letters, numbers, hyphens, and underscores"
            )

    @property
    def value(self) -> str:
        """Get the agent name value."""
        return self._value

    def __str__(self) -> str:
        """String representation."""
        return self._value

    def __repr__(self) -> str:
        """Developer representation."""
        return f"AgentName('{self._value}')"

    def __eq__(self, other: Any) -> bool:
        """Check equality."""
        if not isinstance(other, AgentName):
            return False
        return self._value == other._value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self._value)
