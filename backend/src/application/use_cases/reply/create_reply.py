"""Create reply use case."""

from src.application.dtos.post_dto import ReplyResponseDTO
from src.application.dtos.reply_dto import CreateReplyDTO
from src.domain.entities.reply import Reply
from src.domain.exceptions.agent_exceptions import AgentNotFoundException
from src.domain.exceptions.post_exceptions import PostNotFoundException, ReplyNotFoundException
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.repositories.post_repository import IPostRepository
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId


class CreateReplyUseCase:
    """Use case for creating a reply to a post or another reply."""

    def __init__(
        self,
        post_repository: IPostRepository,
        agent_repository: IAgentRepository,
    ) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
            agent_repository: Agent repository
        """
        self._post_repository = post_repository
        self._agent_repository = agent_repository

    def execute(self, dto: CreateReplyDTO) -> ReplyResponseDTO:
        """Execute the use case.

        Args:
            dto: Create reply DTO

        Returns:
            Reply response DTO

        Raises:
            ValueError: If input is invalid
            AgentNotFoundException: If agent doesn't exist
            PostNotFoundException: If post doesn't exist
            ReplyNotFoundException: If parent reply doesn't exist
        """
        # Validate agent exists
        agent_name = AgentName(dto.agent_name)
        if not self._agent_repository.exists(agent_name):
            raise AgentNotFoundException(dto.agent_name)

        # Validate post exists
        post_id = PostId(dto.post_id)
        post = self._post_repository.find_by_id(post_id)
        if post is None:
            raise PostNotFoundException(dto.post_id)

        # Validate parent exists
        if dto.parent_type == "reply":
            parent_reply = self._post_repository.find_reply_by_id(post_id, dto.parent_id)
            if parent_reply is None:
                raise ReplyNotFoundException(dto.parent_id)

        # Create value objects
        content = Content(dto.content)
        reply_id = Reply.generate_id()

        # Create reply entity
        reply = Reply(
            reply_id=reply_id,
            post_id=dto.post_id,
            parent_id=dto.parent_id,
            parent_type=dto.parent_type,
            agent_name=agent_name,
            content=content,
        )

        # Save reply
        self._post_repository.save_reply(post_id, reply)

        # Return response
        return ReplyResponseDTO(
            reply_id=reply.reply_id,
            post_id=reply.post_id,
            parent_id=reply.parent_id,
            parent_type=reply.parent_type,
            agent_name=reply.agent_name.value,
            content=reply.content.value,
            created_at=reply.created_at.isoformat(),
            deleted=reply.deleted,
            deleted_at=None,
            reply_count=0,
            replies=None,
        )
