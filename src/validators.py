"""Input validation functions for task data."""

MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title according to requirements.

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str).
        error_message is empty string if valid.
    """
    if not title:
        return False, "Title is required and cannot be empty"

    trimmed = title.strip()
    if not trimmed:
        return False, "Title is required and cannot be empty"

    if len(trimmed) > MAX_TITLE_LENGTH:
        trimmed_len = len(trimmed)
        return (
            False,
            f"Title must be between 1 and {MAX_TITLE_LENGTH} characters "
            f"(received {trimmed_len})",
        )

    return True, ""


def validate_description(description: str | None) -> tuple[bool, str]:
    """
    Validate task description according to requirements.

    Args:
        description: The description string to validate, or None if not provided

    Returns:
        Tuple of (is_valid: bool, error_message: str).
        error_message is empty string if valid.
    """
    if description is None:
        return True, ""  # Optional field

    if len(description) > MAX_DESCRIPTION_LENGTH:
        desc_len = len(description)
        return (
            False,
            f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters "
            f"(received {desc_len})",
        )

    return True, ""


def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """
    Validate task ID according to requirements.

    Task IDs must be positive integers (≥ 1). This function parses the string
    representation and validates the constraints.

    Args:
        task_id_str: The task ID string from command line

    Returns:
        Tuple of (is_valid: bool, error_message: str, parsed_id: int | None)
        - is_valid: True if validation passed, False otherwise
        - error_message: Empty string if valid, error description if invalid
        - parsed_id: The integer ID if valid, None if invalid

    Examples:
        >>> validate_task_id("5")
        (True, "", 5)
        >>> validate_task_id("0")
        (False, "Task ID must be a positive integer", None)
        >>> validate_task_id("abc")
        (False, "Task ID must be a positive integer", None)
    """
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a positive integer", None

    if task_id < 1:
        return False, "Task ID must be a positive integer", None

    return True, "", task_id
