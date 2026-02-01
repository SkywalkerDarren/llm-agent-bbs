"""Agents API routes."""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from ....application.use_cases.agent.get_agent_profile import GetAgentProfileUseCase
from ....application.use_cases.agent.list_agents import ListAgentsUseCase
from ....domain.exceptions.agent_exceptions import AgentNotFoundException
from ....infrastructure.persistence.agent_repository_impl import (
    AgentRepositoryImpl,
)
from ....infrastructure.persistence.file_storage import FileStorage
from ....infrastructure.persistence.post_repository_impl import PostRepositoryImpl
from ..schemas.agent_schema import AgentListResponse, AgentResponse
from ..schemas.post_schema import PostListResponse, PostResponse


def create_agents_router(data_dir: Path) -> APIRouter:
    """Create agents router with dependencies.

    Args:
        data_dir: Data directory path

    Returns:
        Configured APIRouter
    """
    router = APIRouter(prefix="/agents", tags=["agents"])

    # Initialize dependencies
    storage = FileStorage(data_dir)
    agent_repo = AgentRepositoryImpl(storage)
    post_repo = PostRepositoryImpl(storage)

    @router.get("", response_model=AgentListResponse)
    async def list_agents():
        """List all registered agents.

        Returns:
            List of all agents with statistics
        """
        use_case = ListAgentsUseCase(agent_repo)
        agents_dto = use_case.execute()

        agents = [
            AgentResponse(
                agent_name=agent.agent_name,
                description=agent.description,
                created_at=agent.created_at,
                post_count=agent.post_count,
                reply_count=agent.reply_count,
                metadata={},
            )
            for agent in agents_dto
        ]

        return AgentListResponse(agents=agents, total=len(agents))

    @router.get("/{agent_name}", response_model=AgentResponse)
    async def get_agent(agent_name: str):
        """Get agent profile by name.

        Args:
            agent_name: Agent name

        Returns:
            Agent profile with statistics

        Raises:
            HTTPException: If agent not found
        """
        use_case = GetAgentProfileUseCase(agent_repo)

        try:
            agent_dto = use_case.execute(agent_name)
        except AgentNotFoundException:
            raise HTTPException(status_code=404, detail="Agent not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return AgentResponse(
            agent_name=agent_dto.agent_name,
            description=agent_dto.description,
            created_at=agent_dto.created_at,
            post_count=agent_dto.post_count,
            reply_count=agent_dto.reply_count,
            metadata=agent_dto.metadata,
        )

    @router.get("/{agent_name}/posts", response_model=PostListResponse)
    async def get_agent_posts(agent_name: str):
        """Get all posts by an agent.

        Args:
            agent_name: Agent name

        Returns:
            List of posts by the agent

        Raises:
            HTTPException: If agent not found
        """
        # Check if agent exists
        use_case = GetAgentProfileUseCase(agent_repo)
        try:
            use_case.execute(agent_name)
        except AgentNotFoundException:
            raise HTTPException(status_code=404, detail="Agent not found")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Get all posts by this agent
        all_posts = post_repo.find_all(include_deleted=False)
        agent_posts = [post for post in all_posts if post.agent_name.value == agent_name]

        posts = [
            PostResponse(
                post_id=post.post_id.value,
                title=post.title,
                content=post.content.value,
                agent_name=post.agent_name.value,
                created_at=post.created_at.isoformat(),
                updated_at=post.updated_at.isoformat(),
                deleted=post.deleted,
                deleted_at=post.deleted_at.isoformat() if post.deleted_at else None,
                tags=post.tags.values,
                reply_count=len(post.replies),
            )
            for post in agent_posts
        ]

        return PostListResponse(
            posts=posts,
            total=len(posts),
            page=1,
            page_size=len(posts),
            total_pages=1,
        )

    return router
