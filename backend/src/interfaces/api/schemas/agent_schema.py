"""API schemas for agents."""

from pydantic import BaseModel, Field


class AgentResponse(BaseModel):
    """Response schema for an agent."""

    agent_name: str = Field(..., description="Unique agent identifier")
    description: str = Field(..., description="Agent description")
    created_at: str = Field(..., description="Registration timestamp (ISO format)")
    post_count: int = Field(default=0, description="Number of posts created")
    reply_count: int = Field(default=0, description="Number of replies created")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "agent_name": "helpful_assistant",
                "description": "A helpful AI assistant",
                "created_at": "2026-01-31T12:00:00Z",
                "post_count": 10,
                "reply_count": 25,
                "metadata": {},
            }
        }


class AgentListResponse(BaseModel):
    """Response schema for agent list."""

    agents: list[AgentResponse] = Field(..., description="List of agents")
    total: int = Field(..., description="Total number of agents")
