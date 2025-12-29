"""Unit tests for input validation functions."""

from src.validators import validate_description, validate_title


class TestValidateTitle:
    """Test validate_title function."""

    def test_valid_title_1_char(self) -> None:
        """Test that 1-character title is valid."""
        is_valid, error = validate_title("A")
        assert is_valid is True
        assert error == ""

    def test_valid_title_50_chars(self) -> None:
        """Test that 50-character title is valid."""
        title = "A" * 50
        is_valid, error = validate_title(title)
        assert is_valid is True
        assert error == ""

    def test_valid_title_100_chars(self) -> None:
        """Test that exactly 100-character title is valid."""
        title = "A" * 100
        is_valid, error = validate_title(title)
        assert is_valid is True
        assert error == ""

    def test_invalid_title_empty(self) -> None:
        """Test that empty title is invalid."""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert "Title is required" in error

    def test_invalid_title_whitespace_only(self) -> None:
        """Test that whitespace-only title is invalid."""
        is_valid, error = validate_title("   ")
        assert is_valid is False
        assert "Title is required" in error

    def test_invalid_title_101_chars(self) -> None:
        """Test that title >100 chars is invalid."""
        title = "A" * 101
        is_valid, error = validate_title(title)
        assert is_valid is False
        assert "Title must be between 1 and 100 characters" in error
        assert "received 101" in error

    def test_title_trimming(self) -> None:
        """Test that title is trimmed before validation."""
        is_valid, error = validate_title("  Hello  ")
        assert is_valid is True
        assert error == ""

    def test_title_unicode(self) -> None:
        """Test that Unicode characters are valid."""
        is_valid, error = validate_title("Café 中文")
        assert is_valid is True
        assert error == ""


class TestValidateDescription:
    """Test validate_description function."""

    def test_valid_description_none(self) -> None:
        """Test that None description is valid."""
        is_valid, error = validate_description(None)
        assert is_valid is True
        assert error == ""

    def test_valid_description_empty_string(self) -> None:
        """Test that empty string description is valid."""
        is_valid, error = validate_description("")
        assert is_valid is True
        assert error == ""

    def test_valid_description_500_chars(self) -> None:
        """Test that exactly 500-character description is valid."""
        desc = "A" * 500
        is_valid, error = validate_description(desc)
        assert is_valid is True
        assert error == ""

    def test_invalid_description_501_chars(self) -> None:
        """Test that description >500 chars is invalid."""
        desc = "A" * 501
        is_valid, error = validate_description(desc)
        assert is_valid is False
        assert "Description cannot exceed 500 characters" in error
        assert "received 501" in error
