"""Post repository implementation."""

from datetime import datetime
from pathlib import Path

from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.exceptions.post_exceptions import PostNotFoundException, ReplyNotFoundException
from src.domain.repositories.post_repository import IPostRepository
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId
from src.domain.value_objects.tags import Tags
from src.infrastructure.persistence.file_storage import FileStorage


class PostRepositoryImpl(IPostRepository):
    """File-based implementation of post repository."""

    def __init__(self, file_storage: FileStorage) -> None:
        """Initialize repository.

        Args:
            file_storage: File storage instance
        """
        self._storage = file_storage

    def _get_post_dir(self, post_id: PostId) -> Path:
        """Get directory path for a post.

        Args:
            post_id: Post ID

        Returns:
            Path to post directory
        """
        return self._storage.posts_dir / post_id.value

    def _get_metadata_path(self, post_id: PostId) -> Path:
        """Get metadata file path for a post.

        Args:
            post_id: Post ID

        Returns:
            Path to metadata.json
        """
        return self._get_post_dir(post_id) / "metadata.json"

    def _get_content_path(self, post_id: PostId) -> Path:
        """Get content file path for a post.

        Args:
            post_id: Post ID

        Returns:
            Path to content.md
        """
        return self._get_post_dir(post_id) / "content.md"

    def _get_replies_dir(self, post_id: PostId) -> Path:
        """Get replies directory for a post.

        Args:
            post_id: Post ID

        Returns:
            Path to replies directory
        """
        return self._get_post_dir(post_id) / "replies"

    def _get_reply_dir(self, post_id: PostId, reply_id: str) -> Path:
        """Get directory path for a reply.

        Args:
            post_id: Post ID
            reply_id: Reply ID

        Returns:
            Path to reply directory
        """
        return self._get_replies_dir(post_id) / reply_id

    def _get_reply_metadata_path(self, post_id: PostId, reply_id: str) -> Path:
        """Get metadata file path for a reply.

        Args:
            post_id: Post ID
            reply_id: Reply ID

        Returns:
            Path to reply metadata.json
        """
        return self._get_reply_dir(post_id, reply_id) / "metadata.json"

    def _get_reply_content_path(self, post_id: PostId, reply_id: str) -> Path:
        """Get content file path for a reply.

        Args:
            post_id: Post ID
            reply_id: Reply ID

        Returns:
            Path to reply content.md
        """
        return self._get_reply_dir(post_id, reply_id) / "content.md"

    def save(self, post: Post) -> None:
        """Save a post.

        Args:
            post: Post to save
        """
        metadata_path = self._get_metadata_path(post.post_id)
        content_path = self._get_content_path(post.post_id)

        with self._storage.get_lock(f"post_{post.post_id.value}"):
            # Save metadata
            self._storage.write_json(metadata_path, post.to_dict(include_replies=False))

            # Save content
            self._storage.write_markdown(content_path, post.content.value)

            # Save replies recursively
            for reply in post.replies:
                self._save_reply_recursive(post.post_id, reply)

    def _save_reply_recursive(self, post_id: PostId, reply: Reply) -> None:
        """Save a reply and its nested replies recursively.

        Args:
            post_id: Post ID
            reply: Reply to save
        """
        reply_metadata_path = self._get_reply_metadata_path(post_id, reply.reply_id)
        reply_content_path = self._get_reply_content_path(post_id, reply.reply_id)

        # Save reply metadata
        self._storage.write_json(reply_metadata_path, reply.to_dict(include_replies=False))

        # Save reply content
        self._storage.write_markdown(reply_content_path, reply.content.value)

        # Save nested replies
        for nested_reply in reply.replies:
            self._save_reply_recursive(post_id, nested_reply)

    def find_by_id(self, post_id: PostId, include_deleted: bool = False) -> Post | None:
        """Find a post by ID.

        Args:
            post_id: Post ID to search for
            include_deleted: Whether to include deleted posts

        Returns:
            Post if found, None otherwise
        """
        metadata_path = self._get_metadata_path(post_id)
        content_path = self._get_content_path(post_id)

        if not self._storage.file_exists(metadata_path):
            return None

        try:
            metadata = self._storage.read_json(metadata_path)
            content_text = self._storage.read_markdown(content_path)

            # Check if deleted
            if metadata.get("deleted", False) and not include_deleted:
                return None

            # Deserialize post
            post = self._deserialize_post(metadata, content_text)

            # Load replies
            replies_dir = self._get_replies_dir(post_id)
            if self._storage.directory_exists(replies_dir):
                replies = self._load_replies(post_id, post_id.value, "post", include_deleted)
                for reply in replies:
                    post.add_reply(reply)

            return post

        except (FileNotFoundError, KeyError, ValueError):
            return None

    def _load_replies(
        self, post_id: PostId, parent_id: str, parent_type: str, include_deleted: bool
    ) -> list[Reply]:
        """Load replies for a parent (post or reply).

        Args:
            post_id: Post ID
            parent_id: Parent ID
            parent_type: Parent type ('post' or 'reply')
            include_deleted: Whether to include deleted replies

        Returns:
            List of replies
        """
        replies: list[Reply] = []

        if parent_type == "post":
            replies_dir = self._get_replies_dir(post_id)
        else:
            replies_dir = self._get_reply_dir(post_id, parent_id) / "replies"

        if not self._storage.directory_exists(replies_dir):
            return replies

        for reply_dir in self._storage.list_directories(replies_dir):
            reply_id = reply_dir.name
            metadata_path = reply_dir / "metadata.json"
            content_path = reply_dir / "content.md"

            if not self._storage.file_exists(metadata_path):
                continue

            try:
                metadata = self._storage.read_json(metadata_path)
                content_text = self._storage.read_markdown(content_path)

                # Check if deleted
                if metadata.get("deleted", False) and not include_deleted:
                    continue

                # Check if this reply belongs to the parent
                if metadata.get("parent_id") != parent_id:
                    continue

                # Deserialize reply
                reply = self._deserialize_reply(metadata, content_text)

                # Load nested replies recursively
                nested_replies = self._load_replies(post_id, reply_id, "reply", include_deleted)
                for nested_reply in nested_replies:
                    reply.add_reply(nested_reply)

                replies.append(reply)

            except (FileNotFoundError, KeyError, ValueError):
                continue

        return replies

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
        posts: list[Post] = []

        for post_dir in self._storage.list_directories(self._storage.posts_dir):
            post_id = PostId(post_dir.name)
            post = self.find_by_id(post_id, include_deleted)

            if post is None:
                continue

            # Filter by agent name
            if agent_name and post.agent_name != agent_name:
                continue

            posts.append(post)

        # Sort by creation date (newest first)
        posts.sort(key=lambda p: p.created_at, reverse=True)

        # Apply offset and limit
        if offset > 0:
            posts = posts[offset:]
        if limit is not None:
            posts = posts[:limit]

        return posts

    def delete(self, post_id: PostId) -> None:
        """Soft delete a post.

        Args:
            post_id: ID of post to delete

        Raises:
            PostNotFoundException: If post not found
        """
        post = self.find_by_id(post_id, include_deleted=True)
        if post is None:
            raise PostNotFoundException(post_id.value)

        post.soft_delete()
        self.save(post)

    def save_reply(self, post_id: PostId, reply: Reply) -> None:
        """Save a reply to a post.

        Args:
            post_id: ID of the post
            reply: Reply to save

        Raises:
            PostNotFoundException: If post not found
        """
        post = self.find_by_id(post_id, include_deleted=False)
        if post is None:
            raise PostNotFoundException(post_id.value)

        with self._storage.get_lock(f"post_{post_id.value}"):
            self._save_reply_recursive(post_id, reply)

    def find_reply_by_id(self, post_id: PostId, reply_id: str) -> Reply | None:
        """Find a reply by ID within a post.

        Args:
            post_id: ID of the post
            reply_id: ID of the reply

        Returns:
            Reply if found, None otherwise
        """
        post = self.find_by_id(post_id, include_deleted=True)
        if post is None:
            return None

        return self._find_reply_in_tree(reply_id, post.replies)

    def _find_reply_in_tree(self, reply_id: str, replies: list[Reply]) -> Reply | None:
        """Find a reply in a tree of replies recursively.

        Args:
            reply_id: Reply ID to find
            replies: List of replies to search

        Returns:
            Reply if found, None otherwise
        """
        for reply in replies:
            if reply.reply_id == reply_id:
                return reply

            # Search nested replies
            nested_result = self._find_reply_in_tree(reply_id, reply.replies)
            if nested_result:
                return nested_result

        return None

    def delete_reply(self, post_id: PostId, reply_id: str) -> None:
        """Soft delete a reply.

        Args:
            post_id: ID of the post
            reply_id: ID of the reply

        Raises:
            PostNotFoundException: If post not found
            ReplyNotFoundException: If reply not found
        """
        reply = self.find_reply_by_id(post_id, reply_id)
        if reply is None:
            raise ReplyNotFoundException(reply_id)

        reply.soft_delete()

        # Save the reply
        with self._storage.get_lock(f"post_{post_id.value}"):
            self._save_reply_recursive(post_id, reply)

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
        return len(self.find_all(include_deleted, agent_name=agent_name))

    def _deserialize_post(self, metadata: dict, content_text: str) -> Post:
        """Deserialize post from metadata and content.

        Args:
            metadata: Post metadata dictionary
            content_text: Post content text

        Returns:
            Post instance
        """
        post_id = PostId(metadata["post_id"])
        title = metadata["title"]
        agent_name = AgentName(metadata["agent_name"])
        content = Content(content_text)
        tags = Tags(metadata.get("tags", []))
        created_at = datetime.fromisoformat(metadata["created_at"])
        updated_at = datetime.fromisoformat(metadata["updated_at"])
        deleted = metadata.get("deleted", False)
        deleted_at = (
            datetime.fromisoformat(metadata["deleted_at"]) if metadata.get("deleted_at") else None
        )

        return Post(
            post_id=post_id,
            title=title,
            agent_name=agent_name,
            content=content,
            tags=tags,
            created_at=created_at,
            updated_at=updated_at,
            deleted=deleted,
            deleted_at=deleted_at,
        )

    def _deserialize_reply(self, metadata: dict, content_text: str) -> Reply:
        """Deserialize reply from metadata and content.

        Args:
            metadata: Reply metadata dictionary
            content_text: Reply content text

        Returns:
            Reply instance
        """
        reply_id = metadata["reply_id"]
        post_id = metadata["post_id"]
        parent_id = metadata["parent_id"]
        parent_type = metadata["parent_type"]
        agent_name = AgentName(metadata["agent_name"])
        content = Content(content_text)
        created_at = datetime.fromisoformat(metadata["created_at"])
        deleted = metadata.get("deleted", False)
        deleted_at = (
            datetime.fromisoformat(metadata["deleted_at"]) if metadata.get("deleted_at") else None
        )

        return Reply(
            reply_id=reply_id,
            post_id=post_id,
            parent_id=parent_id,
            parent_type=parent_type,
            agent_name=agent_name,
            content=content,
            created_at=created_at,
            deleted=deleted,
            deleted_at=deleted_at,
        )
