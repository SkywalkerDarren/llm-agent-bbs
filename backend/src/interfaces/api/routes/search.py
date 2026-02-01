"""Search API routes."""

from pathlib import Path

from fastapi import APIRouter, Query

from ....application.dtos.post_dto import SearchPostsDTO
from ....application.use_cases.post.search_posts import SearchPostsUseCase
from ....infrastructure.indexes.post_index import PostIndex
from ....infrastructure.persistence.file_storage import FileStorage
from ....infrastructure.persistence.post_repository_impl import PostRepositoryImpl
from ....infrastructure.persistence.search_repository_impl import (
    SearchRepositoryImpl,
)
from ..schemas.post_schema import PostResponse
from ..schemas.search_schema import SearchResponse


def create_search_router(data_dir: Path) -> APIRouter:
    """Create search router with dependencies.

    Args:
        data_dir: Data directory path

    Returns:
        Configured APIRouter
    """
    router = APIRouter(prefix="/search", tags=["search"])

    # Initialize dependencies
    storage = FileStorage(data_dir)
    post_repo = PostRepositoryImpl(storage)
    post_index = PostIndex(storage)
    search_repo = SearchRepositoryImpl(post_index, post_repo)

    @router.get("", response_model=SearchResponse)
    async def search_posts(
        q: str | None = Query(None, description="Search query"),
        agent: str | None = Query(None, description="Filter by agent name"),
        tags: str | None = Query(None, description="Filter by tags (comma-separated)"),
        include_deleted: bool = Query(False, description="Include deleted posts"),
    ):
        """Search posts by query, agent, or tags.

        Args:
            q: Search query (searches in title and content)
            agent: Filter by agent name
            tags: Filter by tags (comma-separated)
            include_deleted: Whether to include deleted posts

        Returns:
            Search results
        """
        use_case = SearchPostsUseCase(search_repo)

        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None

        dto = SearchPostsDTO(
            query=q,
            agent_name=agent,
            tags=tag_list,
            include_deleted=include_deleted,
        )

        posts_dto = use_case.execute(dto)

        posts = [
            PostResponse(
                post_id=post.post_id,
                title=post.title,
                content="",  # Search results don't include full content
                agent_name=post.agent_name,
                created_at=post.created_at,
                updated_at=post.updated_at,
                deleted=post.deleted,
                deleted_at=None,
                tags=post.tags,
                reply_count=post.reply_count,
            )
            for post in posts_dto
        ]

        filters = {}
        if q:
            filters["query"] = q
        if agent:
            filters["agent"] = agent
        if tags:
            filters["tags"] = tag_list

        return SearchResponse(
            results=posts,
            total=len(posts),
            query=q or "",
            filters=filters,
        )

    return router
