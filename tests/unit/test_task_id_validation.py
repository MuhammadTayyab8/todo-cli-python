"""Unit tests for task ID validation."""

from src.validators import validate_task_id


def test_valid_task_id_1():
    """Test validation of boundary valid ID = 1."""
    is_valid, error_msg, parsed_id = validate_task_id("1")
    assert is_valid is True
    assert error_msg == ""
    assert parsed_id == 1


def test_valid_task_id_100():
    """Test validation of typical valid ID = 100."""
    is_valid, error_msg, parsed_id = validate_task_id("100")
    assert is_valid is True
    assert error_msg == ""
    assert parsed_id == 100


def test_invalid_task_id_0():
    """Test validation rejects ID = 0 (boundary)."""
    is_valid, error_msg, parsed_id = validate_task_id("0")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_negative_1():
    """Test validation rejects negative ID = -1 (boundary)."""
    is_valid, error_msg, parsed_id = validate_task_id("-1")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_negative_100():
    """Test validation rejects negative ID = -100 (typical)."""
    is_valid, error_msg, parsed_id = validate_task_id("-100")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_non_numeric():
    """Test validation rejects non-numeric input 'abc'."""
    is_valid, error_msg, parsed_id = validate_task_id("abc")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_float():
    """Test validation rejects float input '1.5'."""
    is_valid, error_msg, parsed_id = validate_task_id("1.5")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_empty_string():
    """Test validation rejects empty string ''."""
    is_valid, error_msg, parsed_id = validate_task_id("")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None


def test_invalid_task_id_whitespace():
    """Test validation rejects whitespace-only input '   '."""
    is_valid, error_msg, parsed_id = validate_task_id("   ")
    assert is_valid is False
    assert error_msg == "Task ID must be a positive integer"
    assert parsed_id is None
