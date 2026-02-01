"""Register agent use case."""

from src.application.dtos.agent_dto import AgentResponseDTO, CreateAgentDTO
from src.domain.entities.agent import Agent
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.services.agent_domain_service import AgentDomainService
from src.domain.value_objects.agent_name import AgentName
from src.infrastructure.indexes.agent_index import AgentIndex


class RegisterAgentUseCase:
    """Use case for registering a new agent."""

    def __init__(
        self,
        agent_repository: IAgentRepository,
        agent_domain_service: AgentDomainService,
        agent_index: AgentIndex,
    ) -> None:
        """Initialize use case.

        Args:
            agent_repository: Agent repository
            agent_domain_service: Agent domain service
            agent_index: Agent index
        """
        self._agent_repository = agent_repository
        self._agent_domain_service = agent_domain_service
        self._agent_index = agent_index

    def execute(self, dto: CreateAgentDTO) -> AgentResponseDTO:
        """Execute the use case.

        Args:
            dto: Create agent DTO

        Returns:
            Agent response DTO

        Raises:
            ValueError: If agent name is invalid
            AgentAlreadyExistsException: If agent already exists
        """
        # Create value object (validates name)
        agent_name = AgentName(dto.agent_name)

        # Validate uniqueness
        self._agent_domain_service.validate_unique_name(agent_name)

        # Create agent entity
        agent = Agent(
            name=agent_name,
            description=dto.description,
            metadata=dto.metadata or {},
        )

        # Save agent
        self._agent_repository.save(agent)

        # Update index
        self._agent_index.add_agent(agent.to_dict())

        # Return response
        return AgentResponseDTO(
            agent_name=agent.name.value,
            description=agent.description,
            created_at=agent.created_at.isoformat(),
            metadata=agent.metadata,
            post_count=0,
            reply_count=0,
        )
