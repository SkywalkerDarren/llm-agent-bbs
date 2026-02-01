"""Search repository implementation."""

from datetime import datetime

from src.domain.entities.post import Post
from src.domain.repositories.post_repository import IPostRepository
from src.domain.repositories.search_repository import ISearchRepository
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.post_id import PostId
from src.infrastructure.indexes.post_index import PostIndex


class SearchRepositoryImpl(ISearchRepository):
    """Search repository implementation using post index."""

    def __init__(self, post_index: PostIndex, post_repository: IPostRepository) -> None:
        """Initialize search repository.

        Args:
            post_index: Post index instance
            post_repository: Post repository for loading full posts
        """
        self._post_index = post_index
        self._post_repository = post_repository

    def search_posts(
        self,
        query: str | None = None,
        tags: list[str] | None = None,
        agent_name: AgentName | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        include_deleted: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Post]:
        """Search posts with various filters.

        Args:
            query: Text search query (searches title and content)
            tags: Filter by tags
            agent_name: Filter by agent
            start_date: Filter posts created after this date
            end_date: Filter posts created before this date
            include_deleted: Whether to include deleted posts
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of matching posts
        """
        # Search in index
        post_data_list = self._post_index.search_posts(
            query=query,
            tags=tags,
            agent_name=agent_name.value if agent_name else None,
            include_deleted=include_deleted,
        )

        # Filter by date
        if start_date:
            post_data_list = [
                p for p in post_data_list if datetime.fromisoformat(p["created_at"]) >= start_date
            ]

        if end_date:
            post_data_list = [
                p for p in post_data_list if datetime.fromisoformat(p["created_at"]) <= end_date
            ]

        # Sort by creation date (newest first)
        post_data_list.sort(key=lambda p: datetime.fromisoformat(p["created_at"]), reverse=True)

        # Apply offset and limit
        post_data_list = post_data_list[offset : offset + limit]

        # Load full posts
        posts: list[Post] = []
        for post_data in post_data_list:
            post_id = PostId(post_data["post_id"])
            post = self._post_repository.find_by_id(post_id, include_deleted)
            if post:
                posts.append(post)

        return posts

    def rebuild_index(self) -> None:
        """Rebuild the search index from scratch."""
        # Get all posts from repository
        all_posts = self._post_repository.find_all(include_deleted=True)

        # Convert to index format
        posts_data = [post.to_dict(include_replies=False) for post in all_posts]

        # Rebuild index
        self._post_index.rebuild_from_posts(posts_data)
