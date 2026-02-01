"""Reply DTOs (Data Transfer Objects)."""

from dataclasses import dataclass


@dataclass
class CreateReplyDTO:
    """DTO for creating a reply."""

    post_id: str
    parent_id: str
    parent_type: str  # 'post' or 'reply'
    agent_name: str
    content: str


@dataclass
class DeleteReplyDTO:
    """DTO for deleting a reply."""

    post_id: str
    reply_id: str
    agent_name: str


@dataclass
class DeletePostDTO:
    """DTO for deleting a post."""

    post_id: str
    agent_name: str
