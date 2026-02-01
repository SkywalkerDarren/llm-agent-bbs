"""Post domain service."""

from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.exceptions.post_exceptions import (
    UnauthorizedPostDeletionException,
    UnauthorizedReplyDeletionException,
)
from src.domain.value_objects.agent_name import AgentName


class PostDomainService:
    """Domain service for post-related business logic."""

    MAX_REPLY_DEPTH = 10

    @staticmethod
    def can_delete_post(post: Post, agent_name: AgentName) -> bool:
        """Check if an agent can delete a post.

        Args:
            post: Post to check
            agent_name: Agent attempting deletion

        Returns:
            True if agent can delete, False otherwise
        """
        return post.agent_name == agent_name

    @staticmethod
    def validate_post_deletion(post: Post, agent_name: AgentName) -> None:
        """Validate post deletion authorization.

        Args:
            post: Post to delete
            agent_name: Agent attempting deletion

        Raises:
            UnauthorizedPostDeletionException: If agent cannot delete post
        """
        if not PostDomainService.can_delete_post(post, agent_name):
            raise UnauthorizedPostDeletionException(post.post_id.value, agent_name.value)

    @staticmethod
    def can_delete_reply(reply: Reply, agent_name: AgentName) -> bool:
        """Check if an agent can delete a reply.

        Args:
            reply: Reply to check
            agent_name: Agent attempting deletion

        Returns:
            True if agent can delete, False otherwise
        """
        return reply.agent_name == agent_name

    @staticmethod
    def validate_reply_deletion(reply: Reply, agent_name: AgentName) -> None:
        """Validate reply deletion authorization.

        Args:
            reply: Reply to delete
            agent_name: Agent attempting deletion

        Raises:
            UnauthorizedReplyDeletionException: If agent cannot delete reply
        """
        if not PostDomainService.can_delete_reply(reply, agent_name):
            raise UnauthorizedReplyDeletionException(reply.reply_id, agent_name.value)

    @staticmethod
    def calculate_reply_depth(reply: Reply, all_replies: dict[str, Reply]) -> int:
        """Calculate the depth of a reply in the reply tree.

        Args:
            reply: Reply to calculate depth for
            all_replies: Dictionary of all replies by ID

        Returns:
            Depth of the reply (0 for direct post replies)
        """
        depth = 0
        current = reply

        while current.parent_type == "reply":
            depth += 1
            parent = all_replies.get(current.parent_id)
            if not parent:
                break
            current = parent

        return depth

    @staticmethod
    def validate_reply_depth(reply: Reply, all_replies: dict[str, Reply]) -> None:
        """Validate that reply depth doesn't exceed maximum.

        Args:
            reply: Reply to validate
            all_replies: Dictionary of all replies by ID

        Raises:
            ValueError: If reply depth exceeds maximum
        """
        depth = PostDomainService.calculate_reply_depth(reply, all_replies)
        if depth >= PostDomainService.MAX_REPLY_DEPTH:
            raise ValueError(f"Reply depth cannot exceed {PostDomainService.MAX_REPLY_DEPTH}")
