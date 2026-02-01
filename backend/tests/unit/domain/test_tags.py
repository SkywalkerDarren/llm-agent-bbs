"""Unit tests for Tags value object."""

import pytest

from src.domain.value_objects.tags import Tags


class TestTags:
    """Test cases for Tags value object."""

    def test_valid_tags(self):
        """Test creating valid tags."""
        tags = Tags(["python", "testing", "ddd"])
        assert tags.values == ["python", "testing", "ddd"]

    def test_empty_tags_list(self):
        """Test creating tags with empty list."""
        tags = Tags([])
        assert tags.values == []

    def test_tags_normalized_to_lowercase(self):
        """Test that tags are normalized to lowercase."""
        tags = Tags(["Python", "TESTING", "DDD"])
        assert tags.values == ["python", "testing", "ddd"]

    def test_tags_trimmed(self):
        """Test that tags are trimmed."""
        tags = Tags(["  python  ", " testing ", "ddd"])
        assert tags.values == ["python", "testing", "ddd"]

    def test_too_many_tags_raises_error(self):
        """Test that more than 10 tags raises ValueError."""
        too_many = [f"tag{i}" for i in range(11)]
        with pytest.raises(ValueError, match="Cannot have more than 10 tags"):
            Tags(too_many)

    def test_empty_tag_raises_error(self):
        """Test that empty tag raises ValueError."""
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            Tags(["valid", "", "tags"])

    def test_whitespace_only_tag_raises_error(self):
        """Test that whitespace-only tag raises ValueError."""
        with pytest.raises(ValueError, match="Tag cannot be empty"):
            Tags(["valid", "   ", "tags"])

    def test_too_long_tag_raises_error(self):
        """Test that tag longer than 30 chars raises ValueError."""
        long_tag = "a" * 31
        with pytest.raises(ValueError, match="must be at most 30 characters"):
            Tags([long_tag])

    def test_invalid_tag_characters_raises_error(self):
        """Test that invalid characters in tag raise ValueError."""
        with pytest.raises(ValueError, match="can only contain"):
            Tags(["valid", "invalid tag", "tags"])  # space not allowed

        with pytest.raises(ValueError, match="can only contain"):
            Tags(["valid", "invalid@tag"])  # @ not allowed

    def test_tags_with_hyphens_and_underscores(self):
        """Test tags with hyphens and underscores."""
        tags = Tags(["python-3", "unit_test", "test-case_1"])
        assert "python-3" in tags.values
        assert "unit_test" in tags.values
        assert "test-case_1" in tags.values

    def test_tags_iteration(self):
        """Test that tags can be iterated."""
        tags = Tags(["tag1", "tag2", "tag3"])
        tag_list = list(tags)
        assert tag_list == ["tag1", "tag2", "tag3"]

    def test_tags_length(self):
        """Test getting number of tags."""
        tags = Tags(["tag1", "tag2", "tag3"])
        assert len(tags) == 3

    def test_tags_equality(self):
        """Test tags equality (order-independent)."""
        tags1 = Tags(["python", "testing", "ddd"])
        tags2 = Tags(["ddd", "python", "testing"])  # different order
        tags3 = Tags(["python", "testing"])

        assert tags1 == tags2  # same tags, different order
        assert tags1 != tags3  # different tags

    def test_tags_string_representation(self):
        """Test string representation."""
        tags = Tags(["python", "testing", "ddd"])
        assert str(tags) == "python, testing, ddd"

    def test_tags_repr(self):
        """Test repr representation."""
        tags = Tags(["python", "testing"])
        assert repr(tags) == "Tags(['python', 'testing'])"

    def test_maximum_tags(self):
        """Test maximum number of tags (10)."""
        max_tags = [f"tag{i}" for i in range(10)]
        tags = Tags(max_tags)
        assert len(tags) == 10

    def test_single_tag(self):
        """Test single tag."""
        tags = Tags(["python"])
        assert len(tags) == 1
        assert tags.values == ["python"]

    def test_tags_immutability(self):
        """Test that returned values list is a copy."""
        tags = Tags(["python", "testing"])
        values = tags.values
        values.append("new_tag")

        # Original tags should not be modified
        assert len(tags) == 2
        assert "new_tag" not in tags.values
