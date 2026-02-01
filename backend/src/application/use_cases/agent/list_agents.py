"""List agents use case."""

from src.application.dtos.agent_dto import AgentListItemDTO
from src.domain.repositories.agent_repository import IAgentRepository


class ListAgentsUseCase:
    """Use case for listing all agents."""

    def __init__(self, agent_repository: IAgentRepository) -> None:
        """Initialize use case.

        Args:
            agent_repository: Agent repository
        """
        self._agent_repository = agent_repository

    def execute(self) -> list[AgentListItemDTO]:
        """Execute the use case.

        Returns:
            List of agent list item DTOs
        """
        agents = self._agent_repository.list_all()

        return [
            AgentListItemDTO(
                agent_name=agent.name.value,
                description=agent.description,
                created_at=agent.created_at.isoformat(),
                post_count=self._agent_repository.get_post_count(agent.name),
                reply_count=self._agent_repository.get_reply_count(agent.name),
            )
            for agent in agents
        ]
