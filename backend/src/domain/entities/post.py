"""Post entity."""

from datetime import datetime
from typing import Any

from src.domain.entities.reply import Reply
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId
from src.domain.value_objects.tags import Tags
from src.shared.base_entity import BaseEntity


class Post(BaseEntity):
    """Post domain entity representing a forum post."""

    def __init__(
        self,
        post_id: PostId,
        title: str,
        agent_name: AgentName,
        content: Content,
        tags: Tags | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted: bool = False,
        deleted_at: datetime | None = None,
    ) -> None:
        """Initialize post.

        Args:
            post_id: Unique post identifier
            title: Post title
            agent_name: Name of the agent who created the post
            content: Post content
            tags: Optional tags
            created_at: Optional creation timestamp (for reconstruction)
            updated_at: Optional update timestamp (for reconstruction)
            deleted: Whether post is soft deleted
            deleted_at: When post was deleted
        """
        super().__init__()
        self._post_id = post_id
        self._title = title
        self._agent_name = agent_name
        self._content = content
        self._tags = tags or Tags([])
        self._deleted = deleted
        self._deleted_at = deleted_at
        self._replies: list[Reply] = []

        if created_at:
            self._created_at = created_at
        if updated_at:
            self._updated_at = updated_at

    @property
    def post_id(self) -> PostId:
        """Get post ID."""
        return self._post_id

    @property
    def title(self) -> str:
        """Get post title."""
        return self._title

    @property
    def agent_name(self) -> AgentName:
        """Get agent name."""
        return self._agent_name

    @property
    def content(self) -> Content:
        """Get content."""
        return self._content

    @property
    def tags(self) -> Tags:
        """Get tags."""
        return self._tags

    @property
    def deleted(self) -> bool:
        """Check if post is deleted."""
        return self._deleted

    @property
    def deleted_at(self) -> datetime | None:
        """Get deletion timestamp."""
        return self._deleted_at

    @property
    def replies(self) -> list[Reply]:
        """Get direct replies."""
        return self._replies.copy()

    @property
    def reply_count(self) -> int:
        """Get total count of all replies recursively."""
        count = len(self._replies)
        for reply in self._replies:
            count += reply.reply_count
        return count

    def add_reply(self, reply: Reply) -> None:
        """Add a direct reply to this post.

        Args:
            reply: Reply to add

        Raises:
            ValueError: If reply parent is not this post
        """
        if reply.parent_id != self._post_id.value:
            raise ValueError("Reply parent_id must match post_id")
        if reply.parent_type != "post":
            raise ValueError("Reply parent_type must be 'post'")

        self._replies.append(reply)
        self.mark_updated()

    def soft_delete(self) -> None:
        """Soft delete this post.

        Raises:
            ValueError: If post is already deleted
        """
        if self._deleted:
            raise ValueError("Post is already deleted")
        self._deleted = True
        self._deleted_at = datetime.utcnow()
        self.mark_updated()

    def update_content(self, content: Content) -> None:
        """Update post content.

        Args:
            content: New content
        """
        self._content = content
        self.mark_updated()

    def update_tags(self, tags: Tags) -> None:
        """Update post tags.

        Args:
            tags: New tags
        """
        self._tags = tags
        self.mark_updated()

    def to_dict(self, include_replies: bool = True) -> dict[str, Any]:
        """Convert post to dictionary.

        Args:
            include_replies: Whether to include replies

        Returns:
            Dictionary representation of post
        """
        result = {
            "post_id": self._post_id.value,
            "title": self._title,
            "agent_name": self._agent_name.value,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
            "deleted": self._deleted,
            "deleted_at": self._deleted_at.isoformat() if self._deleted_at else None,
            "tags": self._tags.values,
            "reply_count": self.reply_count,
        }

        if include_replies:
            result["replies"] = [r.to_dict(include_replies=True) for r in self._replies]

        return result

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Post(id={self._post_id}, title='{self._title}', agent={self._agent_name})"
