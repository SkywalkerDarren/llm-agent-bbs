"""Agent DTOs (Data Transfer Objects)."""

from dataclasses import dataclass
from typing import Any


@dataclass
class CreateAgentDTO:
    """DTO for creating an agent."""

    agent_name: str
    description: str
    metadata: dict[str, Any] | None = None


@dataclass
class AgentResponseDTO:
    """DTO for agent response."""

    agent_name: str
    description: str
    created_at: str
    metadata: dict[str, Any]
    post_count: int = 0
    reply_count: int = 0


@dataclass
class AgentListItemDTO:
    """DTO for agent list item."""

    agent_name: str
    description: str
    created_at: str
    post_count: int = 0
    reply_count: int = 0
