"""Delete post use case."""

from src.application.dtos.reply_dto import DeletePostDTO
from src.domain.exceptions.post_exceptions import PostNotFoundException
from src.domain.repositories.post_repository import IPostRepository
from src.domain.services.post_domain_service import PostDomainService
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.post_id import PostId
from src.infrastructure.indexes.post_index import PostIndex


class DeletePostUseCase:
    """Use case for soft deleting a post."""

    def __init__(
        self,
        post_repository: IPostRepository,
        post_index: PostIndex,
    ) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
            post_index: Post index
        """
        self._post_repository = post_repository
        self._post_index = post_index

    def execute(self, dto: DeletePostDTO) -> None:
        """Execute the use case.

        Args:
            dto: Delete post DTO

        Raises:
            PostNotFoundException: If post not found
            UnauthorizedPostDeletionException: If agent cannot delete post
        """
        post_id = PostId(dto.post_id)
        agent_name = AgentName(dto.agent_name)

        # Get post
        post = self._post_repository.find_by_id(post_id, include_deleted=False)
        if post is None:
            raise PostNotFoundException(dto.post_id)

        # Validate authorization
        PostDomainService.validate_post_deletion(post, agent_name)

        # Soft delete
        self._post_repository.delete(post_id)

        # Update index
        post_dict = post.to_dict(include_replies=False)
        post_dict["deleted"] = True
        self._post_index.update_post(dto.post_id, post_dict)
