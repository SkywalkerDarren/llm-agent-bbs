"""Delete reply use case."""

from src.application.dtos.reply_dto import DeleteReplyDTO
from src.domain.exceptions.post_exceptions import PostNotFoundException, ReplyNotFoundException
from src.domain.repositories.post_repository import IPostRepository
from src.domain.services.post_domain_service import PostDomainService
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.post_id import PostId


class DeleteReplyUseCase:
    """Use case for soft deleting a reply."""

    def __init__(self, post_repository: IPostRepository) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
        """
        self._post_repository = post_repository

    def execute(self, dto: DeleteReplyDTO) -> None:
        """Execute the use case.

        Args:
            dto: Delete reply DTO

        Raises:
            PostNotFoundException: If post not found
            ReplyNotFoundException: If reply not found
            UnauthorizedReplyDeletionException: If agent cannot delete reply
        """
        post_id = PostId(dto.post_id)
        agent_name = AgentName(dto.agent_name)

        # Get post
        post = self._post_repository.find_by_id(post_id, include_deleted=False)
        if post is None:
            raise PostNotFoundException(dto.post_id)

        # Get reply
        reply = self._post_repository.find_reply_by_id(post_id, dto.reply_id)
        if reply is None:
            raise ReplyNotFoundException(dto.reply_id)

        # Validate authorization
        PostDomainService.validate_reply_deletion(reply, agent_name)

        # Soft delete
        self._post_repository.delete_reply(post_id, dto.reply_id)
