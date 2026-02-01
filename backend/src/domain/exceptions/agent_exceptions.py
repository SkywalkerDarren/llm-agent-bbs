"""Domain exceptions for agents."""


class AgentException(Exception):
    """Base exception for agent-related errors."""

    pass


class AgentAlreadyExistsException(AgentException):
    """Raised when trying to create an agent that already exists."""

    def __init__(self, agent_name: str) -> None:
        """Initialize exception.

        Args:
            agent_name: Name of the agent that already exists
        """
        super().__init__(f"Agent '{agent_name}' already exists")
        self.agent_name = agent_name


class AgentNotFoundException(AgentException):
    """Raised when an agent is not found."""

    def __init__(self, agent_name: str) -> None:
        """Initialize exception.

        Args:
            agent_name: Name of the agent that was not found
        """
        super().__init__(f"Agent '{agent_name}' not found")
        self.agent_name = agent_name
