"""Dependency injection container for the BBS system."""

from pathlib import Path

from src.application.use_cases.agent.get_agent_profile import GetAgentProfileUseCase
from src.application.use_cases.agent.list_agents import ListAgentsUseCase
from src.application.use_cases.agent.register_agent import RegisterAgentUseCase
from src.application.use_cases.post.browse_posts import BrowsePostsUseCase
from src.application.use_cases.post.create_post import CreatePostUseCase
from src.application.use_cases.post.delete_post import DeletePostUseCase
from src.application.use_cases.post.get_post import GetPostUseCase
from src.application.use_cases.post.search_posts import SearchPostsUseCase
from src.application.use_cases.reply.create_reply import CreateReplyUseCase
from src.application.use_cases.reply.delete_reply import DeleteReplyUseCase
from src.domain.services.agent_domain_service import AgentDomainService
from src.infrastructure.indexes.agent_index import AgentIndex
from src.infrastructure.indexes.post_index import PostIndex
from src.infrastructure.persistence.agent_repository_impl import AgentRepositoryImpl
from src.infrastructure.persistence.file_storage import FileStorage
from src.infrastructure.persistence.post_repository_impl import PostRepositoryImpl
from src.infrastructure.persistence.search_repository_impl import SearchRepositoryImpl


class Container:
    """Dependency injection container."""

    def __init__(self, data_dir: Path) -> None:
        """Initialize container.

        Args:
            data_dir: Root directory for data storage
        """
        # Infrastructure
        self.file_storage = FileStorage(data_dir)

        # Indexes
        self.post_index = PostIndex(self.file_storage)
        self.agent_index = AgentIndex(self.file_storage)

        # Repositories
        self.agent_repository = AgentRepositoryImpl(self.file_storage)
        self.post_repository = PostRepositoryImpl(self.file_storage)
        self.search_repository = SearchRepositoryImpl(self.post_index, self.post_repository)

        # Domain Services
        self.agent_domain_service = AgentDomainService(self.agent_repository)

        # Use Cases - Agent
        self.register_agent_use_case = RegisterAgentUseCase(
            self.agent_repository,
            self.agent_domain_service,
            self.agent_index,
        )
        self.get_agent_profile_use_case = GetAgentProfileUseCase(self.agent_repository)
        self.list_agents_use_case = ListAgentsUseCase(self.agent_repository)

        # Use Cases - Post
        self.create_post_use_case = CreatePostUseCase(
            self.post_repository,
            self.agent_repository,
            self.post_index,
        )
        self.get_post_use_case = GetPostUseCase(self.post_repository)
        self.browse_posts_use_case = BrowsePostsUseCase(self.post_repository)
        self.search_posts_use_case = SearchPostsUseCase(self.search_repository)
        self.delete_post_use_case = DeletePostUseCase(self.post_repository, self.post_index)

        # Use Cases - Reply
        self.create_reply_use_case = CreateReplyUseCase(
            self.post_repository,
            self.agent_repository,
        )
        self.delete_reply_use_case = DeleteReplyUseCase(self.post_repository)
