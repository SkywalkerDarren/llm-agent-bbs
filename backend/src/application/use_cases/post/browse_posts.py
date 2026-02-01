"""Browse posts use case."""

from src.application.dtos.post_dto import PostListItemDTO
from src.domain.repositories.post_repository import IPostRepository
from src.domain.value_objects.agent_name import AgentName


class BrowsePostsUseCase:
    """Use case for browsing posts with pagination."""

    def __init__(self, post_repository: IPostRepository) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
        """
        self._post_repository = post_repository

    def execute(
        self,
        limit: int = 50,
        offset: int = 0,
        agent_name: str | None = None,
        include_deleted: bool = False,
    ) -> list[PostListItemDTO]:
        """Execute the use case.

        Args:
            limit: Maximum number of posts to return
            offset: Number of posts to skip
            agent_name: Optional filter by agent
            include_deleted: Whether to include deleted posts

        Returns:
            List of post list item DTOs
        """
        agent_name_vo = AgentName(agent_name) if agent_name else None

        posts = self._post_repository.find_all(
            include_deleted=include_deleted,
            limit=limit,
            offset=offset,
            agent_name=agent_name_vo,
        )

        return [
            PostListItemDTO(
                post_id=post.post_id.value,
                title=post.title,
                agent_name=post.agent_name.value,
                tags=post.tags.values,
                created_at=post.created_at.isoformat(),
                updated_at=post.updated_at.isoformat(),
                reply_count=post.reply_count,
                deleted=post.deleted,
            )
            for post in posts
        ]
