"""Unit tests for Post entity."""

from datetime import datetime

import pytest

from src.domain.entities.post import Post
from src.domain.entities.reply import Reply
from src.domain.value_objects.agent_name import AgentName
from src.domain.value_objects.content import Content
from src.domain.value_objects.post_id import PostId
from src.domain.value_objects.tags import Tags


class TestPost:
    """Test cases for Post entity."""

    def test_create_post(self):
        """Test creating a post."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")
        tags = Tags(["test", "unit"])

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
            tags=tags,
        )

        assert post.post_id == post_id
        assert post.title == "Test Post"
        assert post.agent_name == agent_name
        assert post.content == content
        assert post.tags == tags
        assert not post.deleted
        assert post.deleted_at is None
        assert isinstance(post.created_at, datetime)
        assert isinstance(post.updated_at, datetime)

    def test_create_post_without_tags(self):
        """Test creating post without tags."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        assert len(post.tags) == 0

    def test_create_post_with_timestamps(self):
        """Test creating post with specific timestamps."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")
        created_at = datetime(2026, 1, 1, 12, 0, 0)
        updated_at = datetime(2026, 1, 2, 12, 0, 0)

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
        )

        assert post.created_at == created_at
        assert post.updated_at == updated_at

    def test_add_reply(self):
        """Test adding a reply to a post."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        # Create a reply
        reply = Reply(
            reply_id="reply_456_def",
            post_id=post_id.value,
            parent_id=post_id.value,
            parent_type="post",
            agent_name=agent_name,
            content=Content("This is a reply"),
        )

        post.add_reply(reply)

        assert len(post.replies) == 1
        assert post.replies[0] == reply
        assert post.reply_count == 1

    def test_add_reply_with_wrong_parent_id_raises_error(self):
        """Test that adding reply with wrong parent_id raises error."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        # Create a reply with wrong parent_id
        reply = Reply(
            reply_id="reply_456_def",
            post_id=post_id.value,
            parent_id="wrong_parent_id",
            parent_type="post",
            agent_name=agent_name,
            content=Content("This is a reply"),
        )

        with pytest.raises(ValueError, match="Reply parent_id must match post_id"):
            post.add_reply(reply)

    def test_add_reply_with_wrong_parent_type_raises_error(self):
        """Test that adding reply with wrong parent_type raises error."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        # Create a reply with wrong parent_type
        reply = Reply(
            reply_id="reply_456_def",
            post_id=post_id.value,
            parent_id=post_id.value,
            parent_type="reply",  # should be "post"
            agent_name=agent_name,
            content=Content("This is a reply"),
        )

        with pytest.raises(ValueError, match="Reply parent_type must be 'post'"):
            post.add_reply(reply)

    def test_reply_count_with_nested_replies(self):
        """Test reply count includes nested replies."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        # Add first-level reply
        reply1 = Reply(
            reply_id="reply_1",
            post_id=post_id.value,
            parent_id=post_id.value,
            parent_type="post",
            agent_name=agent_name,
            content=Content("Reply 1"),
        )

        # Add nested reply to reply1
        reply2 = Reply(
            reply_id="reply_2",
            post_id=post_id.value,
            parent_id="reply_1",
            parent_type="reply",
            agent_name=agent_name,
            content=Content("Reply 2"),
        )
        reply1.add_reply(reply2)

        post.add_reply(reply1)

        # Should count both replies
        assert post.reply_count == 2

    def test_soft_delete(self):
        """Test soft deleting a post."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        assert not post.deleted
        assert post.deleted_at is None

        post.soft_delete()

        assert post.deleted
        assert isinstance(post.deleted_at, datetime)

    def test_soft_delete_already_deleted_raises_error(self):
        """Test that deleting already deleted post raises error."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        post.soft_delete()

        with pytest.raises(ValueError, match="Post is already deleted"):
            post.soft_delete()

    def test_update_content(self):
        """Test updating post content."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("Original content")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        original_updated_at = post.updated_at

        new_content = Content("Updated content")
        post.update_content(new_content)

        assert post.content == new_content
        assert post.updated_at > original_updated_at

    def test_update_tags(self):
        """Test updating post tags."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")
        tags = Tags(["old", "tags"])

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
            tags=tags,
        )

        original_updated_at = post.updated_at

        new_tags = Tags(["new", "tags"])
        post.update_tags(new_tags)

        assert post.tags == new_tags
        assert post.updated_at > original_updated_at

    def test_to_dict_without_replies(self):
        """Test converting post to dictionary without replies."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")
        tags = Tags(["test"])

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
            tags=tags,
        )

        post_dict = post.to_dict(include_replies=False)

        assert post_dict["post_id"] == "post_123_abc"
        assert post_dict["title"] == "Test Post"
        assert post_dict["agent_name"] == "test_agent"
        assert post_dict["tags"] == ["test"]
        assert post_dict["deleted"] is False
        assert post_dict["deleted_at"] is None
        assert "replies" not in post_dict

    def test_to_dict_with_replies(self):
        """Test converting post to dictionary with replies."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        # Add a reply
        reply = Reply(
            reply_id="reply_456_def",
            post_id=post_id.value,
            parent_id=post_id.value,
            parent_type="post",
            agent_name=agent_name,
            content=Content("This is a reply"),
        )
        post.add_reply(reply)

        post_dict = post.to_dict(include_replies=True)

        assert "replies" in post_dict
        assert len(post_dict["replies"]) == 1
        assert post_dict["replies"][0]["reply_id"] == "reply_456_def"

    def test_replies_immutability(self):
        """Test that returned replies list is a copy."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        replies = post.replies
        # Try to modify the returned list
        replies.append(
            Reply(
                reply_id="fake_reply",
                post_id=post_id.value,
                parent_id=post_id.value,
                parent_type="post",
                agent_name=agent_name,
                content=Content("Fake reply"),
            )
        )

        # Original post should not be modified
        assert len(post.replies) == 0

    def test_post_repr(self):
        """Test post string representation."""
        post_id = PostId("post_123_abc")
        agent_name = AgentName("test_agent")
        content = Content("This is a test post")

        post = Post(
            post_id=post_id,
            title="Test Post",
            agent_name=agent_name,
            content=content,
        )

        repr_str = repr(post)
        assert "Post" in repr_str
        assert "post_123_abc" in repr_str
        assert "Test Post" in repr_str
        assert "test_agent" in repr_str
