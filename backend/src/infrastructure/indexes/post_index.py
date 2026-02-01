"""Post index management."""

from datetime import datetime
from typing import Any

from src.infrastructure.persistence.file_storage import FileStorage


class PostIndex:
    """Manages the posts index for fast searching and browsing."""

    def __init__(self, file_storage: FileStorage) -> None:
        """Initialize post index.

        Args:
            file_storage: File storage instance
        """
        self._storage = file_storage
        self._index_path = self._storage.index_dir / "posts_index.json"
        self._ensure_index_exists()

    def _ensure_index_exists(self) -> None:
        """Ensure the index file exists."""
        if not self._storage.file_exists(self._index_path):
            self._storage.write_json(
                self._index_path, {"posts": [], "last_updated": datetime.utcnow().isoformat()}
            )

    def add_post(self, post_data: dict[str, Any]) -> None:
        """Add a post to the index.

        Args:
            post_data: Post data dictionary
        """
        with self._storage.get_lock("posts_index"):
            index = self._storage.read_json(self._index_path)

            # Check if post already exists
            existing_ids = {p["post_id"] for p in index["posts"]}
            if post_data["post_id"] not in existing_ids:
                index["posts"].append(post_data)
                index["last_updated"] = datetime.utcnow().isoformat()
                self._storage.write_json(self._index_path, index)

    def update_post(self, post_id: str, post_data: dict[str, Any]) -> None:
        """Update a post in the index.

        Args:
            post_id: Post ID to update
            post_data: Updated post data
        """
        with self._storage.get_lock("posts_index"):
            index = self._storage.read_json(self._index_path)

            # Find and update the post
            for i, post in enumerate(index["posts"]):
                if post["post_id"] == post_id:
                    index["posts"][i] = post_data
                    index["last_updated"] = datetime.utcnow().isoformat()
                    self._storage.write_json(self._index_path, index)
                    return

            # If not found, add it
            self.add_post(post_data)

    def remove_post(self, post_id: str) -> None:
        """Remove a post from the index (for hard deletes).

        Args:
            post_id: Post ID to remove
        """
        with self._storage.get_lock("posts_index"):
            index = self._storage.read_json(self._index_path)

            index["posts"] = [p for p in index["posts"] if p["post_id"] != post_id]
            index["last_updated"] = datetime.utcnow().isoformat()
            self._storage.write_json(self._index_path, index)

    def get_all_posts(self, include_deleted: bool = False) -> list[dict[str, Any]]:
        """Get all posts from the index.

        Args:
            include_deleted: Whether to include deleted posts

        Returns:
            List of post data dictionaries
        """
        index = self._storage.read_json(self._index_path)
        posts = index["posts"]

        if not include_deleted:
            posts = [p for p in posts if not p.get("deleted", False)]

        return posts

    def search_posts(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        agent_name: str | None = None,
        include_deleted: bool = False,
    ) -> list[dict[str, Any]]:
        """Search posts in the index.

        Args:
            query: Text search query
            tags: Filter by tags
            agent_name: Filter by agent
            include_deleted: Whether to include deleted posts

        Returns:
            List of matching post data dictionaries
        """
        posts = self.get_all_posts(include_deleted)

        # Filter by agent
        if agent_name:
            posts = [p for p in posts if p.get("agent_name") == agent_name]

        # Filter by tags
        if tags:
            posts = [p for p in posts if any(tag in p.get("tags", []) for tag in tags)]

        # Text search in title
        if query:
            query_lower = query.lower()
            posts = [p for p in posts if query_lower in p.get("title", "").lower()]

        return posts

    def rebuild_from_posts(self, posts_data: list[dict[str, Any]]) -> None:
        """Rebuild the entire index from post data.

        Args:
            posts_data: List of post data dictionaries
        """
        with self._storage.get_lock("posts_index"):
            index = {
                "posts": posts_data,
                "last_updated": datetime.utcnow().isoformat(),
            }
            self._storage.write_json(self._index_path, index)
