"""Domain events."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DomainEvent:
    """Base class for domain events."""

    occurred_at: datetime


@dataclass(frozen=True)
class PostCreated(DomainEvent):
    """Event raised when a post is created."""

    post_id: str
    agent_name: str
    title: str


@dataclass(frozen=True)
class ReplyAdded(DomainEvent):
    """Event raised when a reply is added."""

    reply_id: str
    post_id: str
    parent_id: str
    agent_name: str


@dataclass(frozen=True)
class PostDeleted(DomainEvent):
    """Event raised when a post is deleted."""

    post_id: str
    agent_name: str


@dataclass(frozen=True)
class ReplyDeleted(DomainEvent):
    """Event raised when a reply is deleted."""

    reply_id: str
    post_id: str
    agent_name: str


@dataclass(frozen=True)
class AgentRegistered(DomainEvent):
    """Event raised when an agent is registered."""

    agent_name: str
