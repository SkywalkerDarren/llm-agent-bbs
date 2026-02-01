"""Unit tests for Content value object."""

import pytest

from src.domain.value_objects.content import Content


class TestContent:
    """Test cases for Content value object."""

    def test_valid_content(self):
        """Test creating valid content."""
        content = Content("This is valid content")
        assert content.value == "This is valid content"

    def test_content_with_markdown(self):
        """Test content with markdown formatting."""
        markdown = "# Title\n\nThis is **bold** and *italic*."
        content = Content(markdown)
        assert content.value == markdown

    def test_long_content(self):
        """Test content with many characters."""
        long_text = "a" * 10000
        content = Content(long_text)
        assert content.value == long_text

    def test_empty_content_raises_error(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="Content cannot be empty"):
            Content("")

    def test_whitespace_only_content_raises_error(self):
        """Test that whitespace-only content raises ValueError."""
        with pytest.raises(ValueError, match="Content cannot be empty"):
            Content("   \n\t  ")

    def test_too_long_content_raises_error(self):
        """Test that content exceeding max length raises ValueError."""
        too_long = "a" * 50001
        with pytest.raises(ValueError, match="must be at most 50000 characters"):
            Content(too_long)

    def test_content_minimum_length(self):
        """Test minimum valid content."""
        content = Content("a")
        assert content.value == "a"

    def test_content_maximum_length(self):
        """Test maximum valid content."""
        max_content = "a" * 50000
        content = Content(max_content)
        assert content.value == max_content

    def test_content_equality(self):
        """Test content equality."""
        content1 = Content("Same content")
        content2 = Content("Same content")
        content3 = Content("Different content")

        assert content1 == content2
        assert content1 != content3

    def test_content_string_representation(self):
        """Test string representation."""
        content = Content("Short content")
        assert str(content) == "Short content"

    def test_content_repr_truncates_long_text(self):
        """Test that repr truncates long content."""
        long_text = "a" * 100
        content = Content(long_text)
        repr_str = repr(content)

        # Should be truncated with "..."
        assert "..." in repr_str
        assert len(repr_str) < len(long_text)

    def test_content_with_newlines(self):
        """Test content with newlines."""
        multiline = "Line 1\nLine 2\nLine 3"
        content = Content(multiline)
        assert content.value == multiline

    def test_content_with_special_characters(self):
        """Test content with special characters."""
        special = "Content with émojis 🎉 and spëcial çhars!"
        content = Content(special)
        assert content.value == special
