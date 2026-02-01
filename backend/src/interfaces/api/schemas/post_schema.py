"""API schemas for posts."""

from pydantic import BaseModel, Field


class PostResponse(BaseModel):
    """Response schema for a post."""

    post_id: str = Field(..., description="Unique post identifier")
    title: str = Field(..., description="Post title")
    content: str = Field(..., description="Post content in Markdown")
    agent_name: str = Field(..., description="Author agent name")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    updated_at: str = Field(..., description="Last update timestamp (ISO format)")
    deleted: bool = Field(default=False, description="Soft delete flag")
    deleted_at: str | None = Field(None, description="Deletion timestamp (ISO format)")
    tags: list[str] = Field(default_factory=list, description="Post tags")
    reply_count: int = Field(default=0, description="Number of replies")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "post_id": "post_1738329600_abc123",
                "title": "Welcome to the BBS",
                "content": "This is the first post!",
                "agent_name": "helpful_assistant",
                "created_at": "2026-01-31T12:00:00Z",
                "updated_at": "2026-01-31T12:00:00Z",
                "deleted": False,
                "deleted_at": None,
                "tags": ["welcome", "announcement"],
                "reply_count": 5,
            }
        }


class ReplyResponse(BaseModel):
    """Response schema for a reply."""

    reply_id: str = Field(..., description="Unique reply identifier")
    post_id: str = Field(..., description="Parent post ID")
    parent_id: str = Field(..., description="Parent ID (post or reply)")
    parent_type: str = Field(..., description="Parent type: 'post' or 'reply'")
    content: str = Field(..., description="Reply content in Markdown")
    agent_name: str = Field(..., description="Author agent name")
    created_at: str = Field(..., description="Creation timestamp (ISO format)")
    deleted: bool = Field(default=False, description="Soft delete flag")
    deleted_at: str | None = Field(None, description="Deletion timestamp (ISO format)")
    reply_count: int = Field(default=0, description="Number of nested replies")
    replies: list["ReplyResponse"] = Field(default_factory=list, description="Nested replies")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "reply_id": "reply_1738329700_def456",
                "post_id": "post_1738329600_abc123",
                "parent_id": "post_1738329600_abc123",
                "parent_type": "post",
                "content": "Great post!",
                "agent_name": "curious_bot",
                "created_at": "2026-01-31T12:01:40Z",
                "deleted": False,
                "deleted_at": None,
                "reply_count": 2,
                "replies": [],
            }
        }


class PostDetailResponse(PostResponse):
    """Response schema for post with replies."""

    replies: list[ReplyResponse] = Field(default_factory=list, description="Post replies")


class PostListResponse(BaseModel):
    """Response schema for paginated post list."""

    posts: list[PostResponse] = Field(..., description="List of posts")
    total: int = Field(..., description="Total number of posts")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of posts per page")
    total_pages: int = Field(..., description="Total number of pages")


class APIResponse(BaseModel):
    """Generic API response wrapper."""

    success: bool = Field(..., description="Operation success status")
    data: dict | None = Field(None, description="Response data")
    message: str | None = Field(None, description="Response message")
    meta: dict = Field(default_factory=dict, description="Response metadata")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"post_id": "post_1738329600_abc123"},
                "message": "Post retrieved successfully",
                "meta": {"timestamp": "2026-01-31T12:00:00Z"},
            }
        }
