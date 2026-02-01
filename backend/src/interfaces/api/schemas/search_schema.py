"""API schemas for search."""

from pydantic import BaseModel, Field

from .post_schema import PostResponse


class SearchResponse(BaseModel):
    """Response schema for search results."""

    results: list[PostResponse] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of results")
    query: str = Field(..., description="Search query")
    filters: dict = Field(default_factory=dict, description="Applied filters")
