"""Search repository interface."""

from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.entities.post import Post
from src.domain.value_objects.agent_name import AgentName


class ISearchRepository(ABC):
    """Interface for search repository."""

    @abstractmethod
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
        pass

    @abstractmethod
    def rebuild_index(self) -> None:
        """Rebuild the search index from scratch."""
        pass
