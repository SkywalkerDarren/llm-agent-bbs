"""Agent repository implementation."""

from datetime import datetime
from pathlib import Path

from src.domain.entities.agent import Agent
from src.domain.exceptions.agent_exceptions import AgentAlreadyExistsException
from src.domain.repositories.agent_repository import IAgentRepository
from src.domain.value_objects.agent_name import AgentName
from src.infrastructure.persistence.file_storage import FileStorage


class AgentRepositoryImpl(IAgentRepository):
    """File-based implementation of agent repository."""

    def __init__(self, file_storage: FileStorage) -> None:
        """Initialize repository.

        Args:
            file_storage: File storage instance
        """
        self._storage = file_storage

    def _get_agent_dir(self, name: AgentName) -> Path:
        """Get directory path for an agent.

        Args:
            name: Agent name

        Returns:
            Path to agent directory
        """
        return self._storage.agents_dir / name.value

    def _get_profile_path(self, name: AgentName) -> Path:
        """Get profile file path for an agent.

        Args:
            name: Agent name

        Returns:
            Path to profile.json
        """
        return self._get_agent_dir(name) / "profile.json"

    def save(self, agent: Agent) -> None:
        """Save an agent.

        Args:
            agent: Agent to save

        Raises:
            AgentAlreadyExistsException: If agent already exists
        """
        if self.exists(agent.name):
            raise AgentAlreadyExistsException(agent.name.value)

        profile_path = self._get_profile_path(agent.name)

        with self._storage.get_lock(f"agent_{agent.name.value}"):
            self._storage.write_json(profile_path, agent.to_dict())

    def find_by_name(self, name: AgentName) -> Agent | None:
        """Find an agent by name.

        Args:
            name: Agent name to search for

        Returns:
            Agent if found, None otherwise
        """
        profile_path = self._get_profile_path(name)

        if not self._storage.file_exists(profile_path):
            return None

        try:
            data = self._storage.read_json(profile_path)
            return self._deserialize_agent(data)
        except FileNotFoundError:
            return None

    def exists(self, name: AgentName) -> bool:
        """Check if an agent exists.

        Args:
            name: Agent name to check

        Returns:
            True if agent exists, False otherwise
        """
        profile_path = self._get_profile_path(name)
        return self._storage.file_exists(profile_path)

    def list_all(self) -> list[Agent]:
        """List all agents.

        Returns:
            List of all agents
        """
        agents: list[Agent] = []

        for agent_dir in self._storage.list_directories(self._storage.agents_dir):
            profile_path = agent_dir / "profile.json"
            if self._storage.file_exists(profile_path):
                try:
                    data = self._storage.read_json(profile_path)
                    agent = self._deserialize_agent(data)
                    agents.append(agent)
                except Exception:
                    # Skip invalid agents
                    continue

        return agents

    def get_post_count(self, name: AgentName) -> int:
        """Get the number of posts by an agent.

        Args:
            name: Agent name

        Returns:
            Number of posts
        """
        count = 0
        for post_dir in self._storage.list_directories(self._storage.posts_dir):
            metadata_path = post_dir / "metadata.json"
            if self._storage.file_exists(metadata_path):
                try:
                    data = self._storage.read_json(metadata_path)
                    if data.get("agent_name") == name.value and not data.get("deleted", False):
                        count += 1
                except Exception:
                    continue
        return count

    def get_reply_count(self, name: AgentName) -> int:
        """Get the number of replies by an agent.

        Args:
            name: Agent name

        Returns:
            Number of replies
        """
        count = 0
        # Iterate through all posts
        for post_dir in self._storage.list_directories(self._storage.posts_dir):
            replies_dir = post_dir / "replies"
            if self._storage.directory_exists(replies_dir):
                count += self._count_replies_recursive(replies_dir, name)
        return count

    def _count_replies_recursive(self, replies_dir, agent_name: AgentName) -> int:
        """Recursively count replies by an agent.

        Args:
            replies_dir: Directory containing replies
            agent_name: Agent name to count

        Returns:
            Number of replies by the agent
        """
        count = 0
        for reply_dir in self._storage.list_directories(replies_dir):
            metadata_path = reply_dir / "metadata.json"
            if self._storage.file_exists(metadata_path):
                try:
                    data = self._storage.read_json(metadata_path)
                    if data.get("agent_name") == agent_name.value and not data.get(
                        "deleted", False
                    ):
                        count += 1
                    # Count nested replies
                    nested_replies_dir = reply_dir / "replies"
                    if self._storage.directory_exists(nested_replies_dir):
                        count += self._count_replies_recursive(nested_replies_dir, agent_name)
                except Exception:
                    continue
        return count

    def _deserialize_agent(self, data: dict) -> Agent:
        """Deserialize agent from dictionary.

        Args:
            data: Agent data dictionary

        Returns:
            Agent instance
        """
        name = AgentName(data["agent_name"])
        description = data["description"]
        metadata = data.get("metadata", {})
        created_at = datetime.fromisoformat(data["created_at"])

        return Agent(
            name=name,
            description=description,
            metadata=metadata,
            created_at=created_at,
        )
