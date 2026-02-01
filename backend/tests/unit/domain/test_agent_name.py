"""Unit tests for AgentName value object."""

import pytest

from src.domain.value_objects.agent_name import AgentName


class TestAgentName:
    """Test cases for AgentName value object."""

    def test_valid_agent_name(self):
        """Test creating a valid agent name."""
        name = AgentName("test_agent_123")
        assert name.value == "test_agent_123"

    def test_agent_name_with_hyphens(self):
        """Test agent name with hyphens."""
        name = AgentName("test-agent-123")
        assert name.value == "test-agent-123"

    def test_agent_name_with_underscores(self):
        """Test agent name with underscores."""
        name = AgentName("test_agent_123")
        assert name.value == "test_agent_123"

    def test_agent_name_alphanumeric(self):
        """Test alphanumeric agent name."""
        name = AgentName("TestAgent123")
        assert name.value == "TestAgent123"

    def test_empty_agent_name_raises_error(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Agent name cannot be empty"):
            AgentName("")

    def test_too_short_agent_name_raises_error(self):
        """Test that name shorter than 3 chars raises ValueError."""
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            AgentName("ab")

    def test_too_long_agent_name_raises_error(self):
        """Test that name longer than 50 chars raises ValueError."""
        long_name = "a" * 51
        with pytest.raises(ValueError, match="must be at most 50 characters"):
            AgentName(long_name)

    def test_invalid_characters_raises_error(self):
        """Test that invalid characters raise ValueError."""
        with pytest.raises(ValueError, match="can only contain"):
            AgentName("test agent")  # space not allowed

        with pytest.raises(ValueError, match="can only contain"):
            AgentName("test@agent")  # @ not allowed

        with pytest.raises(ValueError, match="can only contain"):
            AgentName("test.agent")  # . not allowed

    def test_agent_name_equality(self):
        """Test agent name equality."""
        name1 = AgentName("test_agent")
        name2 = AgentName("test_agent")
        name3 = AgentName("other_agent")

        assert name1 == name2
        assert name1 != name3

    def test_agent_name_hash(self):
        """Test agent name can be used in sets and dicts."""
        name1 = AgentName("test_agent")
        name2 = AgentName("test_agent")
        name3 = AgentName("other_agent")

        # Should be able to use in set
        name_set = {name1, name2, name3}
        assert len(name_set) == 2  # name1 and name2 are equal

        # Should be able to use as dict key
        name_dict = {name1: "value1", name3: "value2"}
        assert name_dict[name2] == "value1"  # name2 equals name1

    def test_agent_name_string_representation(self):
        """Test string representation."""
        name = AgentName("test_agent")
        assert str(name) == "test_agent"
        assert repr(name) == "AgentName('test_agent')"

    def test_agent_name_minimum_length(self):
        """Test minimum valid length."""
        name = AgentName("abc")  # exactly 3 chars
        assert name.value == "abc"

    def test_agent_name_maximum_length(self):
        """Test maximum valid length."""
        max_name = "a" * 50  # exactly 50 chars
        name = AgentName(max_name)
        assert name.value == max_name
