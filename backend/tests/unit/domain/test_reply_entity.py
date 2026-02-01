"""Unit tests for Reply entity."""

from datetime import datetime

import pytest

from src.domain.entities.reply import Reply
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content


class TestReply:
    """Test cases for Reply entity."""

    def test_create_reply(self):
        """Test creating a reply."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
        )

        assert reply.reply_id == "reply_123_abc"
        assert reply.post_id == "post_456_def"
        assert reply.parent_id == "post_456_def"
        assert reply.parent_type == "post"
        assert reply.agent_name == agent_name
        assert reply.content == content
        assert not reply.deleted
        assert reply.deleted_at is None
        assert isinstance(reply.created_at, datetime)

    def test_create_reply_with_timestamps(self):
        """Test creating reply with specific timestamp."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")
        created_at = datetime(2026, 1, 1, 12, 0, 0)

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
            created_at=created_at,
        )

        assert reply.created_at == created_at

    def test_create_deleted_reply(self):
        """Test creating a reply that is already deleted."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")
        deleted_at = datetime(2026, 1, 1, 12, 0, 0)

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
            deleted=True,
            deleted_at=deleted_at,
        )

        assert reply.deleted
        assert reply.deleted_at == deleted_at

    def test_generate_id(self):
        """Test generating a reply ID."""
        reply_id = Reply.generate_id()

        # Should start with "reply_"
        assert reply_id.startswith("reply_")

        # Should have format: reply_{timestamp}_{uuid}
        parts = reply_id.split("_")
        assert len(parts) == 3
        assert parts[0] == "reply"
        assert parts[1].isdigit()
        assert len(parts[2]) == 8

    def test_generate_unique_ids(self):
        """Test that generated IDs are unique."""
        id1 = Reply.generate_id()
        id2 = Reply.generate_id()

        assert id1 != id2

    def test_add_nested_reply(self):
        """Test adding a nested reply."""
        agent_name = AgentName("test_agent")

        parent_reply = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Parent reply"),
        )

        nested_reply = Reply(
            reply_id="reply_2",
            post_id="post_123",
            parent_id="reply_1",
            parent_type="reply",
            agent_name=agent_name,
            content=Content("Nested reply"),
        )

        parent_reply.add_reply(nested_reply)

        assert len(parent_reply.replies) == 1
        assert parent_reply.replies[0] == nested_reply
        assert parent_reply.reply_count == 1

    def test_reply_count_with_deeply_nested_replies(self):
        """Test reply count with deeply nested replies."""
        agent_name = AgentName("test_agent")

        # Create a chain of replies
        reply1 = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Reply 1"),
        )

        reply2 = Reply(
            reply_id="reply_2",
            post_id="post_123",
            parent_id="reply_1",
            parent_type="reply",
            agent_name=agent_name,
            content=Content("Reply 2"),
        )

        reply3 = Reply(
            reply_id="reply_3",
            post_id="post_123",
            parent_id="reply_2",
            parent_type="reply",
            agent_name=agent_name,
            content=Content("Reply 3"),
        )

        reply2.add_reply(reply3)
        reply1.add_reply(reply2)

        # reply1 should count reply2 and reply3
        assert reply1.reply_count == 2

    def test_soft_delete(self):
        """Test soft deleting a reply."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
        )

        assert not reply.deleted
        assert reply.deleted_at is None

        reply.soft_delete()

        assert reply.deleted
        assert isinstance(reply.deleted_at, datetime)

    def test_soft_delete_already_deleted_raises_error(self):
        """Test that deleting already deleted reply raises error."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
        )

        reply.soft_delete()

        with pytest.raises(ValueError, match="Reply is already deleted"):
            reply.soft_delete()

    def test_to_dict_without_nested_replies(self):
        """Test converting reply to dictionary without nested replies."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
        )

        reply_dict = reply.to_dict(include_replies=False)

        assert reply_dict["reply_id"] == "reply_123_abc"
        assert reply_dict["post_id"] == "post_456_def"
        assert reply_dict["parent_id"] == "post_456_def"
        assert reply_dict["parent_type"] == "post"
        assert reply_dict["agent_name"] == "test_agent"
        assert reply_dict["deleted"] is False
        assert reply_dict["deleted_at"] is None
        assert "replies" not in reply_dict

    def test_to_dict_with_nested_replies(self):
        """Test converting reply to dictionary with nested replies."""
        agent_name = AgentName("test_agent")

        parent_reply = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Parent reply"),
        )

        nested_reply = Reply(
            reply_id="reply_2",
            post_id="post_123",
            parent_id="reply_1",
            parent_type="reply",
            agent_name=agent_name,
            content=Content("Nested reply"),
        )

        parent_reply.add_reply(nested_reply)

        reply_dict = parent_reply.to_dict(include_replies=True)

        assert "replies" in reply_dict
        assert len(reply_dict["replies"]) == 1
        assert reply_dict["replies"][0]["reply_id"] == "reply_2"

    def test_replies_immutability(self):
        """Test that returned replies list is a copy."""
        agent_name = AgentName("test_agent")

        reply = Reply(
            reply_id="reply_1",
            post_id="post_123",
            parent_id="post_123",
            parent_type="post",
            agent_name=agent_name,
            content=Content("Reply"),
        )

        replies = reply.replies
        # Try to modify the returned list
        replies.append(
            Reply(
                reply_id="fake_reply",
                post_id="post_123",
                parent_id="reply_1",
                parent_type="reply",
                agent_name=agent_name,
                content=Content("Fake"),
            )
        )

        # Original reply should not be modified
        assert len(reply.replies) == 0

    def test_reply_repr(self):
        """Test reply string representation."""
        agent_name = AgentName("test_agent")
        content = Content("This is a reply")

        reply = Reply(
            reply_id="reply_123_abc",
            post_id="post_456_def",
            parent_id="post_456_def",
            parent_type="post",
            agent_name=agent_name,
            content=content,
        )

        repr_str = repr(reply)
        assert "Reply" in repr_str
        assert "reply_123_abc" in repr_str
        assert "test_agent" in repr_str
