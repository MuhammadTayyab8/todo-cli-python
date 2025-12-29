"""Unit tests for Task dataclass."""

from datetime import datetime

import pytest

from src.models import Task


class TestTaskCreation:
    """Test Task instantiation with valid data."""

    def test_task_creation_with_all_fields(self) -> None:
        """Test creating a task with all fields populated."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="incomplete",
            created_at=now,
        )
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == "incomplete"
        assert task.created_at == now

    def test_task_creation_with_minimal_fields(self) -> None:
        """Test creating a task with only required fields."""
        now = datetime.now()
        task = Task(
            id=2,
            title="Schedule meeting",
            description=None,
            status="incomplete",
            created_at=now,
        )
        assert task.id == 2
        assert task.title == "Schedule meeting"
        assert task.description is None
        assert task.status == "incomplete"


class TestTaskValidation:
    """Test Task validation in __post_init__."""

    def test_task_invalid_id_zero(self) -> None:
        """Test that ID of 0 raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(
                id=0,
                title="Task",
                description=None,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_invalid_id_negative(self) -> None:
        """Test that negative ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(
                id=-1,
                title="Task",
                description=None,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_invalid_title_empty(self) -> None:
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title is required"):
            Task(
                id=1,
                title="",
                description=None,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_invalid_title_whitespace_only(self) -> None:
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title is required"):
            Task(
                id=1,
                title="   ",
                description=None,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_invalid_title_too_long(self) -> None:
        """Test that title >100 chars raises ValueError."""
        long_title = "A" * 101
        with pytest.raises(ValueError, match="Task title cannot exceed 100 characters"):
            Task(
                id=1,
                title=long_title,
                description=None,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_valid_title_boundary_100_chars(self) -> None:
        """Test that title with exactly 100 chars is valid."""
        title_100 = "A" * 100
        task = Task(
            id=1,
            title=title_100,
            description=None,
            status="incomplete",
            created_at=datetime.now(),
        )
        assert task.title == title_100

    def test_task_invalid_description_too_long(self) -> None:
        """Test that description >500 chars raises ValueError."""
        long_desc = "A" * 501
        with pytest.raises(
            ValueError, match="Task description cannot exceed 500 characters"
        ):
            Task(
                id=1,
                title="Task",
                description=long_desc,
                status="incomplete",
                created_at=datetime.now(),
            )

    def test_task_valid_description_boundary_500_chars(self) -> None:
        """Test that description with exactly 500 chars is valid."""
        desc_500 = "A" * 500
        task = Task(
            id=1,
            title="Task",
            description=desc_500,
            status="incomplete",
            created_at=datetime.now(),
        )
        assert task.description == desc_500

    def test_task_valid_description_none(self) -> None:
        """Test that None description is valid."""
        task = Task(
            id=1,
            title="Task",
            description=None,
            status="incomplete",
            created_at=datetime.now(),
        )
        assert task.description is None

    def test_task_invalid_status_unknown(self) -> None:
        """Test that invalid status raises ValueError."""
        with pytest.raises(
            ValueError, match="Task status must be 'complete' or 'incomplete'"
        ):
            Task(
                id=1,
                title="Task",
                description=None,
                status="done",
                created_at=datetime.now(),
            )

    def test_task_created_at_is_datetime(self) -> None:
        """Test that created_at is datetime instance."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Task",
            description=None,
            status="incomplete",
            created_at=now,
        )
        assert isinstance(task.created_at, datetime)
        assert task.created_at == now
