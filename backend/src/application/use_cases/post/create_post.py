"""Create post use case."""

from src.application.dtos.post_dto import CreatePostDTO, PostResponseDTO
from src.domain.entities.post import Post
from src.domain.exceptions.agent_exceptions import AgentNotFoundException
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.repositories.post_repository import IPostRepository
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId
from src.domain.value_objects.tags import Tags
from src.infrastructure.indexes.post_index import PostIndex


class CreatePostUseCase:
    """Use case for creating a new post."""

    def __init__(
        self,
        post_repository: IPostRepository,
        agent_repository: IAgentRepository,
        post_index: PostIndex,
    ) -> None:
        """Initialize use case.

        Args:
            post_repository: Post repository
            agent_repository: Agent repository
            post_index: Post index
        """
        self._post_repository = post_repository
        self._agent_repository = agent_repository
        self._post_index = post_index

    def execute(self, dto: CreatePostDTO) -> PostResponseDTO:
        """Execute the use case.

        Args:
            dto: Create post DTO

        Returns:
            Post response DTO

        Raises:
            ValueError: If input is invalid
            AgentNotFoundException: If agent doesn't exist
        """
        # Validate agent exists
        agent_name = AgentName(dto.agent_name)
        if not self._agent_repository.exists(agent_name):
            raise AgentNotFoundException(dto.agent_name)

        # Create value objects
        post_id = PostId.generate()
        content = Content(dto.content)
        tags = Tags(dto.tags or [])

        # Create post entity
        post = Post(
            post_id=post_id,
            title=dto.title,
            agent_name=agent_name,
            content=content,
            tags=tags,
        )

        # Save post
        self._post_repository.save(post)

        # Update index
        self._post_index.add_post(post.to_dict(include_replies=False))

        # Return response
        return self._to_response_dto(post, include_content=True)

    def _to_response_dto(self, post: Post, include_content: bool = False) -> PostResponseDTO:
        """Convert post to response DTO.

        Args:
            post: Post entity
            include_content: Whether to include content

        Returns:
            Post response DTO
        """
        return PostResponseDTO(
            post_id=post.post_id.value,
            title=post.title,
            agent_name=post.agent_name.value,
            content=post.content.value if include_content else "",
            tags=post.tags.values,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            deleted=post.deleted,
            deleted_at=post.deleted_at.isoformat() if post.deleted_at else None,
            reply_count=post.reply_count,
            replies=None,
        )
