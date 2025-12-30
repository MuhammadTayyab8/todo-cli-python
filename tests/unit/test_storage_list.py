"""Unit tests for TaskStorage.list_tasks() method."""

import tempfile
from pathlib import Path

from src.models import Task
from src.storage import TaskStorage


def get_temp_storage() -> TaskStorage:
    """Create a TaskStorage with a temporary file that gets deleted after."""
    return TaskStorage(storage_file=Path(tempfile.mktemp(suffix=".json")))


# T004: Test list empty storage returns empty
def test_list_empty_storage_returns_empty() -> None:
    """Test that empty storage returns empty list."""
    storage = get_temp_storage()

    result = storage.list_tasks()

    assert result == []


# T005: Test list single task
def test_list_single_task() -> None:
    """Test that single task returns list with one formatted task."""
    storage = get_temp_storage()
    storage.add("Buy groceries")

    result = storage.list_tasks()

    assert len(result) == 1
    assert "[1]" in result[0]
    assert "Buy groceries" in result[0]


# T006: Test list multiple tasks
def test_list_multiple_tasks() -> None:
    """Test that multiple tasks are all returned."""
    storage = get_temp_storage()
    storage.add("Task 1")
    storage.add("Task 2")
    storage.add("Task 3")

    result = storage.list_tasks()

    assert len(result) == 3


# T007: Test list incomplete task status symbol
def test_list_incomplete_task_status_symbol() -> None:
    """Test that incomplete task shows ✗ symbol."""
    storage = get_temp_storage()
    storage.add("Buy groceries")

    result = storage.list_tasks()

    assert "✗" in result[0]
    assert "✓" not in result[0]


# T008: Test list complete task status symbol
def test_list_complete_task_status_symbol() -> None:
    """Test that complete task shows ✓ symbol."""
    storage = get_temp_storage()

    task = storage.add("Buy groceries")
    # Mark task as complete
    completed_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status="complete",
        created_at=task.created_at,
    )
    storage._tasks[0] = completed_task

    result = storage.list_tasks()

    assert "✓" in result[0]
    assert "✗" not in result[0]


# T009: Test list preserves ID order
def test_list_preserves_id_order() -> None:
    """Test that tasks are in ascending ID order."""
    storage = get_temp_storage()
    storage.add("Third task")  # ID 2
    storage.add("First task")  # ID 1
    storage.add("Second task")  # ID 3 (note: order added is 2,1,3)

    result = storage.list_tasks()

    # Tasks should be in ID order: 1, 2, 3
    assert "[1]" in result[0]
    assert "[2]" in result[1]
    assert "[3]" in result[2]


# T010: Test list includes title
def test_list_includes_title() -> None:
    """Test that formatted output includes title."""
    storage = get_temp_storage()
    storage.add("Buy groceries")
    storage.add("Call dentist")

    result = storage.list_tasks()

    assert "Buy groceries" in result[0]
    assert "Call dentist" in result[1]


# T011: Test list includes description
def test_list_includes_description() -> None:
    """Test that formatted output includes description."""
    storage = get_temp_storage()
    storage.add("Buy groceries", "Milk, eggs, bread")

    result = storage.list_tasks()

    assert "Milk, eggs, bread" in result[0]
