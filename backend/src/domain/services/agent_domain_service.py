"""Agent domain service."""

from src.domain.exceptions.agent_exceptions import AgentAlreadyExistsException
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.value_objects.agent_name import AgentName


class AgentDomainService:
    """Domain service for agent-related business logic."""

    def __init__(self, agent_repository: IAgentRepository) -> None:
        """Initialize service.

        Args:
            agent_repository: Agent repository
        """
        self._agent_repository = agent_repository

    def validate_unique_name(self, name: AgentName) -> None:
        """Validate that an agent name is unique.

        Args:
            name: Agent name to validate

        Raises:
            AgentAlreadyExistsException: If agent name already exists
        """
        if self._agent_repository.exists(name):
            raise AgentAlreadyExistsException(name.value)
