"""Search posts use case."""

from datetime import datetime

from src.application.dtos.post_dto import PostListItemDTO, SearchPostsDTO
from src.domain.repositories.search_repository import ISearchRepository
from src.domain.value_objects.agent_name import AgentName


class SearchPostsUseCase:
    """Use case for searching posts."""

    def __init__(self, search_repository: ISearchRepository) -> None:
        """Initialize use case.

        Args:
            search_repository: Search repository
        """
        self._search_repository = search_repository

    def execute(self, dto: SearchPostsDTO) -> list[PostListItemDTO]:
        """Execute the use case.

        Args:
            dto: Search posts DTO

        Returns:
            List of matching post list item DTOs
        """
        agent_name = AgentName(dto.agent_name) if dto.agent_name else None
        start_date = datetime.fromisoformat(dto.start_date) if dto.start_date else None
        end_date = datetime.fromisoformat(dto.end_date) if dto.end_date else None

        posts = self._search_repository.search_posts(
            query=dto.query,
            tags=dto.tags,
            agent_name=agent_name,
            start_date=start_date,
            end_date=end_date,
            include_deleted=dto.include_deleted,
            limit=dto.limit,
            offset=dto.offset,
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
