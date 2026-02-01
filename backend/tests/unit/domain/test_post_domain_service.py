"""Unit tests for PostDomainService."""

import pytest

from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.exceptions.post_exceptions import (
    UnauthorizedPostDeletionException,
    UnauthorizedReplyDeletionException,
)
from src.domain.services.post_domain_service import PostDomainService
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId


class TestPostDomainService:
    """Test cases for PostDomainService."""

    def test_can_delete_post_by_author(self):
        """Test that author can delete their own post."""
        agent_name = AgentName("test_agent")
        post = Post(
            post_id=PostId("post_123"),
            title="Test Post",
            agent_name=agent_name,
            content=Content("Content"),
        )

        assert PostDomainService.can_delete_post(post, agent_name)

    def test_cannot_delete_post_by_other_agent(self):
        """Test that other agent cannot delete post."""
        author = AgentName("author")
        other_agent = AgentName("other_agent")

        post = Post(
            post_id=PostId("post_123"),
            title="Test Post",
            agent_name=author,
            content=Content("Content"),
        )

        assert not PostDomainService.can_delete_post(post, other_agent)

    def test_validate_post_deletion_by_author_succeeds(self):
        """Test that validation succeeds for author."""
        agent_name = AgentName("test_agent")
        post = Post(
            post_id=PostId("post_123"),
            title="Test Post",
            agent_name=agent_name,
            content=Content("Content"),
        )

        # Should not raise exception
        PostDomainService.validate_post_deletion(post, agent_name)

    def test_validate_post_deletion_by_other_raises_exception(self):
        """Test that validation fails for non-author."""
        author = AgentName("author")
        other_agent = AgentName("other_agent")

        post = Post(
            post_id=PostId("post_123"),
            title="Test Post",
            agent_name=author,
            content=Content("Content"),
        )

        with pytest.raises(UnauthorizedPostDeletionException) as exc_info:
            PostDomainService.validate_post_deletion(post, other_agent)

        assert exc_info.value.post_id == "post_123"
        assert exc_info.value.agent_name == "other_agent"

    def test_can_delete_reply_by_author(self):
        """Test that author can delete their own reply."""
        agent_name = AgentName("test_agent")
        reply = Reply(
            reply_id="reply_123",
            post_id="post_456",
            parent_id="post_456",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Reply content"),
        )

        assert PostDomainService.can_delete_reply(reply, agent_name)

    def test_cannot_delete_reply_by_other_agent(self):
        """Test that other agent cannot delete reply."""
        author = AgentName("author")
        other_agent = AgentName("other_agent")

        reply = Reply(
            reply_id="reply_123",
            post_id="post_456",
            parent_id="post_456",
            parent_type="post",
            agent_name=author,
            content=Content("Reply content"),
        )

        assert not PostDomainService.can_delete_reply(reply, other_agent)

    def test_validate_reply_deletion_by_author_succeeds(self):
        """Test that validation succeeds for reply author."""
        agent_name = AgentName("test_agent")
        reply = Reply(
            reply_id="reply_123",
            post_id="post_456",
            parent_id="post_456",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Reply content"),
        )

        # Should not raise exception
        PostDomainService.validate_reply_deletion(reply, agent_name)

    def test_validate_reply_deletion_by_other_raises_exception(self):
        """Test that validation fails for non-author of reply."""
        author = AgentName("author")
        other_agent = AgentName("other_agent")

        reply = Reply(
            reply_id="reply_123",
            post_id="post_456",
            parent_id="post_456",
            parent_type="post",
            agent_name=author,
            content=Content("Reply content"),
        )

        with pytest.raises(UnauthorizedReplyDeletionException) as exc_info:
            PostDomainService.validate_reply_deletion(reply, other_agent)

        assert exc_info.value.reply_id == "reply_123"
        assert exc_info.value.agent_name == "other_agent"

    def test_calculate_reply_depth_for_direct_post_reply(self):
        """Test calculating depth for direct reply to post."""
        reply = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=AgentName("agent"),
            content=Content("Reply"),
        )

        depth = PostDomainService.calculate_reply_depth(reply, {})
        assert depth == 0

    def test_calculate_reply_depth_for_nested_reply(self):
        """Test calculating depth for nested reply."""
        reply1 = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=AgentName("agent"),
            content=Content("Reply 1"),
        )

        reply2 = Reply(
            reply_id="reply_2",
            post_id="post_123",
            parent_id="reply_1",
            parent_type="reply",
            agent_name=AgentName("agent"),
            content=Content("Reply 2"),
        )

        all_replies = {"reply_1": reply1, "reply_2": reply2}

        depth = PostDomainService.calculate_reply_depth(reply2, all_replies)
        assert depth == 1

    def test_calculate_reply_depth_for_deeply_nested_reply(self):
        """Test calculating depth for deeply nested reply."""
        reply1 = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=AgentName("agent"),
            content=Content("Reply 1"),
        )

        reply2 = Reply(
            reply_id="reply_2",
            post_id="post_123",
            parent_id="reply_1",
            parent_type="reply",
            agent_name=AgentName("agent"),
            content=Content("Reply 2"),
        )

        reply3 = Reply(
            reply_id="reply_3",
            post_id="post_123",
            parent_id="reply_2",
            parent_type="reply",
            agent_name=AgentName("agent"),
            content=Content("Reply 3"),
        )

        all_replies = {"reply_1": reply1, "reply_2": reply2, "reply_3": reply3}

        depth = PostDomainService.calculate_reply_depth(reply3, all_replies)
        assert depth == 2

    def test_validate_reply_depth_within_limit(self):
        """Test that validation passes for reply within depth limit."""
        reply = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=AgentName("agent"),
            content=Content("Reply"),
        )

        # Should not raise exception
        PostDomainService.validate_reply_depth(reply, {})

    def test_validate_reply_depth_exceeds_limit_raises_error(self):
        """Test that validation fails when depth exceeds limit."""
        # Create a chain of 10 replies (depth 9)
        replies = {}
        parent_id = "post_123"
        parent_type = "post"

        for i in range(10):
            reply = Reply(
                reply_id=f"reply_{i}",
                post_id="post_123",
                parent_id=parent_id,
                parent_type=parent_type,
                agent_name=AgentName("agent"),
                content=Content(f"Reply {i}"),
            )
            replies[f"reply_{i}"] = reply
            parent_id = f"reply_{i}"
            parent_type = "reply"

        # Try to add one more reply (would be depth 10)
        final_reply = Reply(
            reply_id="reply_10",
            post_id="post_123",
            parent_id="reply_9",
            parent_type="reply",
            agent_name=AgentName("agent"),
            content=Content("Reply 10"),
        )

        with pytest.raises(ValueError, match="Reply depth cannot exceed"):
            PostDomainService.validate_reply_depth(final_reply, replies)

    def test_max_reply_depth_constant(self):
        """Test that MAX_REPLY_DEPTH is set correctly."""
        assert PostDomainService.MAX_REPLY_DEPTH == 10
