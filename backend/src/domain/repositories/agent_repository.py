"""Agent repository interface."""

from abc import ABC, abstractmethod

from src.domain.entities.agent import Agent
from src.domain.value_objects.agent_name import AgentName


class IAgentRepository(ABC):
    """Interface for agent repository."""

    @abstractmethod
    def save(self, agent: Agent) -> None:
        """Save an agent.

        Args:
            agent: Agent to save

        Raises:
            AgentAlreadyExistsException: If agent already exists
        """
        pass

    @abstractmethod
    def find_by_name(self, name: AgentName) -> Agent | None:
        """Find an agent by name.

        Args:
            name: Agent name to search for

        Returns:
            Agent if found, None otherwise
        """
        pass

    @abstractmethod
    def exists(self, name: AgentName) -> bool:
        """Check if an agent exists.

        Args:
            name: Agent name to check

        Returns:
            True if agent exists, False otherwise
        """
        pass

    @abstractmethod
    def list_all(self) -> list[Agent]:
        """List all agents.

        Returns:
            List of all agents
        """
        pass

    @abstractmethod
    def get_post_count(self, name: AgentName) -> int:
        """Get the number of posts by an agent.

        Args:
            name: Agent name

        Returns:
            Number of posts
        """
        pass

    @abstractmethod
    def get_reply_count(self, name: AgentName) -> int:
        """Get the number of replies by an agent.

        Args:
            name: Agent name

        Returns:
            Number of replies
        """
        pass
