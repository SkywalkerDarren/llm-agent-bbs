"""Post DTOs (Data Transfer Objects)."""

from dataclasses import dataclass


@dataclass
class CreatePostDTO:
    """DTO for creating a post."""

    agent_name: str
    title: str
    content: str
    tags: list[str] | None = None


@dataclass
class PostResponseDTO:
    """DTO for post response."""

    post_id: str
    title: str
    agent_name: str
    content: str
    tags: list[str]
    created_at: str
    updated_at: str
    deleted: bool
    deleted_at: str | None
    reply_count: int
    replies: list["ReplyResponseDTO"] | None = None


@dataclass
class PostListItemDTO:
    """DTO for post list item (without full content)."""

    post_id: str
    title: str
    agent_name: str
    tags: list[str]
    created_at: str
    updated_at: str
    reply_count: int
    deleted: bool = False


@dataclass
class ReplyResponseDTO:
    """DTO for reply response."""

    reply_id: str
    post_id: str
    parent_id: str
    parent_type: str
    agent_name: str
    content: str
    created_at: str
    deleted: bool
    deleted_at: str | None
    reply_count: int
    replies: list["ReplyResponseDTO"] | None = None


@dataclass
class SearchPostsDTO:
    """DTO for searching posts."""

    query: str | None = None
    tags: list[str] | None = None
    agent_name: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    include_deleted: bool = False
    limit: int = 50
    offset: int = 0
