"""Unit tests for Agent entity."""

from datetime import datetime

from src.domain.entities.agent import Agent
from src.domain.value_objects.agent_name import AgentName


class TestAgent:
    """Test cases for Agent entity."""

    def test_create_agent(self):
        """Test creating an agent."""
        name = AgentName("test_agent")
        agent = Agent(
            name=name,
            description="A test agent",
            metadata={"version": "1.0"},
        )

        assert agent.name == name
        assert agent.description == "A test agent"
        assert agent.metadata == {"version": "1.0"}
        assert isinstance(agent.created_at, datetime)
        assert isinstance(agent.updated_at, datetime)

    def test_create_agent_without_metadata(self):
        """Test creating agent without metadata."""
        name = AgentName("test_agent")
        agent = Agent(name=name, description="A test agent")

        assert agent.metadata == {}

    def test_create_agent_with_created_at(self):
        """Test creating agent with specific created_at timestamp."""
        name = AgentName("test_agent")
        created_at = datetime(2026, 1, 1, 12, 0, 0)
        agent = Agent(
            name=name,
            description="A test agent",
            created_at=created_at,
        )

        assert agent.created_at == created_at
        assert agent.updated_at == created_at

    def test_update_description(self):
        """Test updating agent description."""
        name = AgentName("test_agent")
        agent = Agent(name=name, description="Original description")

        original_updated_at = agent.updated_at

        # Update description
        agent.update_description("New description")

        assert agent.description == "New description"
        assert agent.updated_at > original_updated_at

    def test_update_metadata(self):
        """Test updating agent metadata."""
        name = AgentName("test_agent")
        agent = Agent(
            name=name,
            description="A test agent",
            metadata={"version": "1.0"},
        )

        original_updated_at = agent.updated_at

        # Update metadata
        new_metadata = {"version": "2.0", "feature": "new"}
        agent.update_metadata(new_metadata)

        assert agent.metadata == new_metadata
        assert agent.updated_at > original_updated_at

    def test_to_dict(self):
        """Test converting agent to dictionary."""
        name = AgentName("test_agent")
        agent = Agent(
            name=name,
            description="A test agent",
            metadata={"version": "1.0"},
        )

        agent_dict = agent.to_dict()

        assert agent_dict["agent_name"] == "test_agent"
        assert agent_dict["description"] == "A test agent"
        assert agent_dict["metadata"] == {"version": "1.0"}
        assert "created_at" in agent_dict
        assert isinstance(agent_dict["created_at"], str)

    def test_metadata_immutability(self):
        """Test that returned metadata is a copy."""
        name = AgentName("test_agent")
        agent = Agent(
            name=name,
            description="A test agent",
            metadata={"version": "1.0"},
        )

        metadata = agent.metadata
        metadata["new_key"] = "new_value"

        # Original metadata should not be modified
        assert "new_key" not in agent.metadata

    def test_agent_repr(self):
        """Test agent string representation."""
        name = AgentName("test_agent")
        agent = Agent(name=name, description="A test agent with a long description")

        repr_str = repr(agent)
        assert "test_agent" in repr_str
        assert "Agent" in repr_str
