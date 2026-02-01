"""Base entity class for all domain entities."""

from datetime import datetime
from typing import Any


class BaseEntity:
    """Base class for all domain entities with common attributes."""

    def __init__(self) -> None:
        """Initialize base entity."""
        self._created_at: datetime = datetime.utcnow()
        self._updated_at: datetime = datetime.utcnow()

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at

    def mark_updated(self) -> None:
        """Mark entity as updated."""
        self._updated_at = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }
