"""Agent index management."""

from datetime import datetime
from typing import Any

from src.infrastructure.persistence.file_storage import FileStorage


class AgentIndex:
    """Manages the agents index for fast lookups."""

    def __init__(self, file_storage: FileStorage) -> None:
        """Initialize agent index.

        Args:
            file_storage: File storage instance
        """
        self._storage = file_storage
        self._index_path = self._storage.index_dir / "agents_index.json"
        self._ensure_index_exists()

    def _ensure_index_exists(self) -> None:
        """Ensure the index file exists."""
        if not self._storage.file_exists(self._index_path):
            self._storage.write_json(
                self._index_path,
                {"agents": [], "last_updated": datetime.utcnow().isoformat()},
            )

    def add_agent(self, agent_data: dict[str, Any]) -> None:
        """Add an agent to the index.

        Args:
            agent_data: Agent data dictionary
        """
        with self._storage.get_lock("agents_index"):
            index = self._storage.read_json(self._index_path)

            # Check if agent already exists
            existing_names = {a["agent_name"] for a in index["agents"]}
            if agent_data["agent_name"] not in existing_names:
                index["agents"].append(agent_data)
                index["last_updated"] = datetime.utcnow().isoformat()
                self._storage.write_json(self._index_path, index)

    def update_agent(self, agent_name: str, agent_data: dict[str, Any]) -> None:
        """Update an agent in the index.

        Args:
            agent_name: Agent name to update
            agent_data: Updated agent data
        """
        with self._storage.get_lock("agents_index"):
            index = self._storage.read_json(self._index_path)

            # Find and update the agent
            for i, agent in enumerate(index["agents"]):
                if agent["agent_name"] == agent_name:
                    index["agents"][i] = agent_data
                    index["last_updated"] = datetime.utcnow().isoformat()
                    self._storage.write_json(self._index_path, index)
                    return

            # If not found, add it
            self.add_agent(agent_data)

    def get_all_agents(self) -> list[dict[str, Any]]:
        """Get all agents from the index.

        Returns:
            List of agent data dictionaries
        """
        index = self._storage.read_json(self._index_path)
        return index["agents"]

    def find_agent(self, agent_name: str) -> dict[str, Any] | None:
        """Find an agent by name in the index.

        Args:
            agent_name: Agent name to find

        Returns:
            Agent data dictionary if found, None otherwise
        """
        agents = self.get_all_agents()
        for agent in agents:
            if agent["agent_name"] == agent_name:
                return agent
        return None

    def rebuild_from_agents(self, agents_data: list[dict[str, Any]]) -> None:
        """Rebuild the entire index from agent data.

        Args:
            agents_data: List of agent data dictionaries
        """
        with self._storage.get_lock("agents_index"):
            index = {
                "agents": agents_data,
                "last_updated": datetime.utcnow().isoformat(),
            }
            self._storage.write_json(self._index_path, index)
