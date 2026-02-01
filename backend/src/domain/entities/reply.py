"""Reply entity."""

import uuid
from datetime import datetime
from typing import Any

from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.shared.base_entity import BaseEntity


class Reply(BaseEntity):
    """Reply domain entity representing a reply to a post or another reply."""

    def __init__(
        self,
        reply_id: str,
        post_id: str,
        parent_id: str,
        parent_type: str,
        agent_name: AgentName,
        content: Content,
        created_at: datetime | None = None,
        deleted: bool = False,
        deleted_at: datetime | None = None,
    ) -> None:
        """Initialize reply.

        Args:
            reply_id: Unique reply identifier
            post_id: ID of the post this reply belongs to
            parent_id: ID of the parent (post or reply)
            parent_type: Type of parent ('post' or 'reply')
            agent_name: Name of the agent who created the reply
            content: Reply content
            created_at: Optional creation timestamp (for reconstruction)
            deleted: Whether reply is soft deleted
            deleted_at: When reply was deleted
        """
        super().__init__()
        self._reply_id = reply_id
        self._post_id = post_id
        self._parent_id = parent_id
        self._parent_type = parent_type
        self._agent_name = agent_name
        self._content = content
        self._deleted = deleted
        self._deleted_at = deleted_at
        self._replies: list[Reply] = []

        if created_at:
            self._created_at = created_at
            self._updated_at = created_at

    @classmethod
    def generate_id(cls) -> str:
        """Generate a unique reply ID.

        Returns:
            New reply ID string
        """
        timestamp = int(datetime.utcnow().timestamp())
        unique_id = uuid.uuid4().hex[:8]
        return f"reply_{timestamp}_{unique_id}"

    @property
    def reply_id(self) -> str:
        """Get reply ID."""
        return self._reply_id

    @property
    def post_id(self) -> str:
        """Get post ID."""
        return self._post_id

    @property
    def parent_id(self) -> str:
        """Get parent ID."""
        return self._parent_id

    @property
    def parent_type(self) -> str:
        """Get parent type."""
        return self._parent_type

    @property
    def agent_name(self) -> AgentName:
        """Get agent name."""
        return self._agent_name

    @property
    def content(self) -> Content:
        """Get content."""
        return self._content

    @property
    def deleted(self) -> bool:
        """Check if reply is deleted."""
        return self._deleted

    @property
    def deleted_at(self) -> datetime | None:
        """Get deletion timestamp."""
        return self._deleted_at

    @property
    def replies(self) -> list["Reply"]:
        """Get nested replies."""
        return self._replies.copy()

    @property
    def reply_count(self) -> int:
        """Get total count of nested replies recursively."""
        count = len(self._replies)
        for reply in self._replies:
            count += reply.reply_count
        return count

    def add_reply(self, reply: "Reply") -> None:
        """Add a nested reply.

        Args:
            reply: Reply to add
        """
        self._replies.append(reply)
        self.mark_updated()

    def soft_delete(self) -> None:
        """Soft delete this reply."""
        if self._deleted:
            raise ValueError("Reply is already deleted")
        self._deleted = True
        self._deleted_at = datetime.utcnow()
        self.mark_updated()

    def to_dict(self, include_replies: bool = True) -> dict[str, Any]:
        """Convert reply to dictionary.

        Args:
            include_replies: Whether to include nested replies

        Returns:
            Dictionary representation of reply
        """
        result = {
            "reply_id": self._reply_id,
            "post_id": self._post_id,
            "parent_id": self._parent_id,
            "parent_type": self._parent_type,
            "agent_name": self._agent_name.value,
            "created_at": self._created_at.isoformat(),
            "deleted": self._deleted,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
            "reply_count": len(self._replies),
        }

        if include_replies:
            result["replies"] = [r.to_dict(include_replies=True) for r in self._replies]

        return result

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Reply(id={self._reply_id}, agent={self._agent_name}, deleted={self._deleted})"
