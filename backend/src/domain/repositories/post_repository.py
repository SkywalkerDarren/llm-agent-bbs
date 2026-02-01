"""Post repository interface."""

from abc import ABC, abstractmethod

from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.post_id import PostId


class IPostRepository(ABC):
    """Interface for post repository."""

    @abstractmethod
    def save(self, post: Post) -> None:
        """Save a post.

        Args:
            post: Post to save
        """
        pass

    @abstractmethod
    def find_by_id(self, post_id: PostId, include_deleted: bool = False) -> Post | None:
        """Find a post by ID.

        Args:
            post_id: Post ID to search for
            include_deleted: Whether to include deleted posts

        Returns:
            Post if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(
        self,
        include_deleted: bool = False,
        limit: int | None = None,
        offset: int = 0,
        agent_name: AgentName | None = None,
    ) -> list[Post]:
        """Find all posts with optional filtering.

        Args:
            include_deleted: Whether to include deleted posts
            limit: Maximum number of posts to return
            offset: Number of posts to skip
            agent_name: Filter by agent name

        Returns:
            List of posts
        """
        pass

    @abstractmethod
    def delete(self, post_id: PostId) -> None:
        """Soft delete a post.

        Args:
            post_id: ID of post to delete

        Raises:
            PostNotFoundException: If post not found
        """
        pass

    @abstractmethod
    def save_reply(self, post_id: PostId, reply: Reply) -> None:
        """Save a reply to a post.

        Args:
            post_id: ID of the post
            reply: Reply to save

        Raises:
            PostNotFoundException: If post not found
        """
        pass

    @abstractmethod
    def find_reply_by_id(self, post_id: PostId, reply_id: str) -> Reply | None:
        """Find a reply by ID within a post.

        Args:
            post_id: ID of the post
            reply_id: ID of the reply

        Returns:
            Reply if found, None otherwise
        """
        pass

    @abstractmethod
    def delete_reply(self, post_id: PostId, reply_id: str) -> None:
        """Soft delete a reply.

        Args:
            post_id: ID of the post
            reply_id: ID of the reply

        Raises:
            PostNotFoundException: If post not found
            ReplyNotFoundException: If reply not found
        """
        pass

    @abstractmethod
    def count_posts(
        self, agent_name: AgentName | None = None, include_deleted: bool = False
    ) -> int:
        """Count posts.

        Args:
            agent_name: Optional filter by agent
            include_deleted: Whether to include deleted posts

        Returns:
            Number of posts
        """
        pass
