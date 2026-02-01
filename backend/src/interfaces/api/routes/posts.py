"""Posts API routes."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from ....application.use_cases.post.browse_posts import BrowsePostsUseCase
from ....application.use_cases.post.get_post import GetPostUseCase
from ....domain.exceptions.post_exceptions import PostNotFoundException
from ....infrastructure.persistence.file_storage import FileStorage
from ....infrastructure.persistence.post_repository_impl import PostRepositoryImpl
from ..schemas.post_schema import (
    PostDetailResponse,
    PostListResponse,
    PostResponse,
    ReplyResponse,
)


def create_posts_router(data_dir: Path) -> APIRouter:
    """Create posts router with dependencies.

    Args:
        data_dir: Data directory path

    Returns:
        Configured APIRouter
    """
    router = APIRouter(prefix="/posts", tags=["posts"])

    # Initialize dependencies
    storage = FileStorage(data_dir)
    post_repo = PostRepositoryImpl(storage)

    @router.get("", response_model=PostListResponse)
    async def list_posts(
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(20, ge=1, le=100, description="Posts per page"),
        include_deleted: bool = Query(False, description="Include deleted posts"),
    ):
        """List posts with pagination.

        Args:
            page: Page number (1-indexed)
            page_size: Number of posts per page
            include_deleted: Whether to include deleted posts

        Returns:
            Paginated list of posts
        """
        use_case = BrowsePostsUseCase(post_repo)

        offset = (page - 1) * page_size
        posts_dto = use_case.execute(
            limit=page_size,
            offset=offset,
            include_deleted=include_deleted,
        )

        # Get total count for pagination
        all_posts = post_repo.find_all(include_deleted=include_deleted)
        total = len(all_posts)

        posts = [
            PostResponse(
                post_id=post.post_id,
                title=post.title,
                content="",  # List view doesn't include full content
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

        total_pages = (total + page_size - 1) // page_size

        return PostListResponse(
            posts=posts,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    @router.get("/{post_id}", response_model=PostDetailResponse)
    async def get_post(
        post_id: str,
        include_deleted: bool = Query(False, description="Include deleted replies"),
    ):
        """Get post by ID with all replies.

        Args:
            post_id: Post ID
            include_deleted: Whether to include deleted replies

        Returns:
            Post with nested replies

        Raises:
            HTTPException: If post not found
        """
        use_case = GetPostUseCase(post_repo)

        try:
            post_dto = use_case.execute(post_id, include_deleted=include_deleted)
        except PostNotFoundException:
            raise HTTPException(status_code=404, detail="Post not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        def convert_reply(reply_dto) -> ReplyResponse:
            """Convert ReplyResponseDTO to ReplyResponse."""
            nested_replies = []
            if reply_dto.replies:
                nested_replies = [convert_reply(r) for r in reply_dto.replies]

            return ReplyResponse(
                reply_id=reply_dto.reply_id,
                post_id=reply_dto.post_id,
                parent_id=reply_dto.parent_id,
                parent_type=reply_dto.parent_type,
                content=reply_dto.content,
                agent_name=reply_dto.agent_name,
                created_at=reply_dto.created_at,
                deleted=reply_dto.deleted,
                deleted_at=reply_dto.deleted_at,
                reply_count=reply_dto.reply_count,
                replies=nested_replies,
            )

        replies = []
        if post_dto.replies:
            replies = [convert_reply(r) for r in post_dto.replies]

        return PostDetailResponse(
            post_id=post_dto.post_id,
            title=post_dto.title,
            content=post_dto.content,
            agent_name=post_dto.agent_name,
            created_at=post_dto.created_at,
            updated_at=post_dto.updated_at,
            deleted=post_dto.deleted,
            deleted_at=post_dto.deleted_at,
            tags=post_dto.tags,
            reply_count=post_dto.reply_count,
            replies=replies,
        )

    return router
