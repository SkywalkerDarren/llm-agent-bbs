"""Get agent profile use case."""

from src.application.dtos.agent_dto import AgentResponseDTO
from src.domain.exceptions.agent_exceptions import AgentNotFoundException
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.value_objects.agent_name import AgentName


class GetAgentProfileUseCase:
    """Use case for getting an agent's profile."""

    def __init__(self, agent_repository: IAgentRepository) -> None:
        """Initialize use case.

        Args:
            agent_repository: Agent repository
        """
        self._agent_repository = agent_repository

    def execute(self, agent_name_str: str) -> AgentResponseDTO:
        """Execute the use case.

        Args:
            agent_name_str: Agent name string

        Returns:
            Agent response DTO

        Raises:
            ValueError: If agent name is invalid
            AgentNotFoundException: If agent not found
        """
        agent_name = AgentName(agent_name_str)
        agent = self._agent_repository.find_by_name(agent_name)

        if agent is None:
            raise AgentNotFoundException(agent_name_str)

        post_count = self._agent_repository.get_post_count(agent_name)
        reply_count = self._agent_repository.get_reply_count(agent_name)

        return AgentResponseDTO(
            agent_name=agent.name.value,
            description=agent.description,
            created_at=agent.created_at.isoformat(),
            metadata=agent.metadata,
            post_count=post_count,
            reply_count=reply_count,
        )
