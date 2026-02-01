"""Unit tests for PostId value object."""

import pytest

from src.domain.value_objects.post_id import PostId


class TestPostId:
    """Test cases for PostId value object."""

    def test_create_post_id_with_value(self):
        """Test creating a post ID with a value."""
        post_id = PostId("post_1234567890_abc123")
        assert post_id.value == "post_1234567890_abc123"

    def test_empty_post_id_raises_error(self):
        """Test that empty post ID raises ValueError."""
        with pytest.raises(ValueError, match="Post ID cannot be empty"):
            PostId("")

    def test_generate_post_id(self):
        """Test generating a new post ID."""
        post_id = PostId.generate()

        # Should start with "post_"
        assert post_id.value.startswith("post_")

        # Should have format: post_{timestamp}_{uuid}
        parts = post_id.value.split("_")
        assert len(parts) == 3
        assert parts[0] == "post"
        assert parts[1].isdigit()  # timestamp
        assert len(parts[2]) == 8  # uuid part

    def test_generate_unique_post_ids(self):
        """Test that generated post IDs are unique."""
        post_id1 = PostId.generate()
        post_id2 = PostId.generate()

        assert post_id1 != post_id2
        assert post_id1.value != post_id2.value

    def test_post_id_equality(self):
        """Test post ID equality."""
        post_id1 = PostId("post_123_abc")
        post_id2 = PostId("post_123_abc")
        post_id3 = PostId("post_456_def")

        assert post_id1 == post_id2
        assert post_id1 != post_id3

    def test_post_id_hash(self):
        """Test post ID can be used in sets and dicts."""
        post_id1 = PostId("post_123_abc")
        post_id2 = PostId("post_123_abc")
        post_id3 = PostId("post_456_def")

        # Should be able to use in set
        id_set = {post_id1, post_id2, post_id3}
        assert len(id_set) == 2

        # Should be able to use as dict key
        id_dict = {post_id1: "value1", post_id3: "value2"}
        assert id_dict[post_id2] == "value1"

    def test_post_id_string_representation(self):
        """Test string representation."""
        post_id = PostId("post_123_abc")
        assert str(post_id) == "post_123_abc"
        assert repr(post_id) == "PostId('post_123_abc')"
