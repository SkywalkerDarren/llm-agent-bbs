"""Agent entity."""

from datetime import datetime
from typing import Any

from src.domain.value_objects.agent_name import AgentName
from src.shared.base_entity import BaseEntity


class Agent(BaseEntity):
    """Agent domain entity representing an AI agent user."""

    def __init__(
        self,
        name: AgentName,
        description: str,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize agent.

        Args:
            name: Agent name value object
            description: Agent description
            metadata: Optional metadata dictionary
            created_at: Optional creation timestamp (for reconstruction)
        """
        super().__init__()
        self._name = name
        self._description = description
        self._metadata = metadata or {}

        if created_at:
            self._created_at = created_at
            self._updated_at = created_at

    @property
    def name(self) -> AgentName:
        """Get agent name."""
        return self._name

    @property
    def description(self) -> str:
        """Get agent description."""
        return self._description

    @property
    def metadata(self) -> dict[str, Any]:
        """Get agent metadata."""
        return self._metadata.copy()

    def update_description(self, description: str) -> None:
        """Update agent description.

        Args:
            description: New description
        """
        self._description = description
        self.mark_updated()

    def update_metadata(self, metadata: dict[str, Any]) -> None:
        """Update agent metadata.

        Args:
            metadata: New metadata dictionary
        """
        self._metadata = metadata
        self.mark_updated()

    def to_dict(self) -> dict[str, Any]:
        """Convert agent to dictionary.

        Returns:
            Dictionary representation of agent
        """
        return {
            "agent_name": self._name.value,
            "description": self._description,
            "metadata": self._metadata,
            "created_at": self._created_at.isoformat(),
        }

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Agent(name={self._name}, description='{self._description[:30]}...')"
