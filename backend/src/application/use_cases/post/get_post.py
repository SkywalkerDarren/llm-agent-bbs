"""Get post use case."""

from src.application.dtos.post_dto import PostResponseDTO, ReplyResponseDTO
from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.exceptions.post_exceptions import PostNotFoundException
from src.domain.repositories.post_repository import IPostRepository
from src.domain.value_objects.post_id import PostId


class GetPostUseCase:
    """Use case for getting a post with all replies."""

    def __init__(self, post_repository: IPostRepository) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
        """
        self._post_repository = post_repository

    def execute(self, post_id_str: str, include_deleted: bool = False) -> PostResponseDTO:
        """Execute the use case.

        Args:
            post_id_str: Post ID string
            include_deleted: Whether to include deleted content

        Returns:
            Post response DTO with replies

        Raises:
            PostNotFoundException: If post not found
        """
        post_id = PostId(post_id_str)
        post = self._post_repository.find_by_id(post_id, include_deleted)

        if post is None:
            raise PostNotFoundException(post_id_str)

        return self._to_response_dto(post, include_replies=True)

    def _to_response_dto(self, post: Post, include_replies: bool = True) -> PostResponseDTO:
        """Convert post to response DTO.

        Args:
            post: Post entity
            include_replies: Whether to include replies

        Returns:
            Post response DTO
        """
        replies_dto = None
        if include_replies:
            replies_dto = [self._reply_to_dto(reply) for reply in post.replies]

        return PostResponseDTO(
            post_id=post.post_id.value,
            title=post.title,
            agent_name=post.agent_name.value,
            content=post.content.value,
            tags=post.tags.values,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            deleted=post.deleted,
            deleted_at=post.deleted_at.isoformat() if post.deleted_at else None,
            reply_count=post.reply_count,
            replies=replies_dto,
        )

    def _reply_to_dto(self, reply: Reply) -> ReplyResponseDTO:
        """Convert reply to DTO recursively.

        Args:
            reply: Reply entity

        Returns:
            Reply response DTO
        """
        nested_replies = [self._reply_to_dto(r) for r in reply.replies]

        return ReplyResponseDTO(
            reply_id=reply.reply_id,
            post_id=reply.post_id,
            parent_id=reply.parent_id,
            parent_type=reply.parent_type,
            agent_name=reply.agent_name.value,
            content=reply.content.value,
            created_at=reply.created_at.isoformat(),
            deleted=reply.deleted,
            deleted_at=reply.deleted_at.isoformat() if reply.deleted_at else None,
            reply_count=reply.reply_count,
            replies=nested_replies if nested_replies else None,
        )
