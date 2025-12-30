"""Unit tests for TaskStorage.update() method."""

import tempfile
from pathlib import Path

from src.models import Task
from src.storage import TaskStorage


def get_temp_storage() -> TaskStorage:
    """Create a TaskStorage with a temporary file that gets deleted after."""
    return TaskStorage(storage_file=Path(tempfile.mktemp(suffix=".json")))


# T004: Test update title only preserves description
def test_update_title_only_preserves_description():
    """Test that updating only the title preserves the existing description."""
    storage = get_temp_storage()
    task = storage.add("Original title", "Original description")

    updated_task = storage.update(task.id, title="New title")

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "Original description"


# T005: Test update description only preserves title
def test_update_description_only_preserves_title():
    """Test that updating only the description preserves the existing title."""
    storage = get_temp_storage()
    task = storage.add("Original title", "Original description")

    updated_task = storage.update(task.id, description="New description")

    assert updated_task is not None
    assert updated_task.title == "Original title"
    assert updated_task.description == "New description"


# T006: Test update both title and description
def test_update_both_title_and_description():
    """Test that updating both title and description works correctly."""
    storage = get_temp_storage()
    task = storage.add("Original title", "Original description")

    updated_task = storage.update(
        task.id, title="New title", description="New description"
    )

    assert updated_task is not None
    assert updated_task.title == "New title"
    assert updated_task.description == "New description"


# T007: Test update non-existent task returns None
def test_update_non_existent_task_returns_none():
    """Test that updating a non-existent task returns None."""
    storage = get_temp_storage()
    storage.add("Existing task")

    result = storage.update(999, title="New title")

    assert result is None


# T008: Test update empty storage returns None
def test_update_empty_storage_returns_none():
    """Test that updating from empty storage returns None."""
    storage = get_temp_storage()

    result = storage.update(1, title="New title")

    assert result is None


# T009: Test update preserves incomplete status
def test_update_preserves_incomplete_status():
    """Test that updating a task preserves 'incomplete' status."""
    storage = get_temp_storage()
    task = storage.add("Original title")
    assert task.status == "incomplete"

    updated_task = storage.update(task.id, title="New title")

    assert updated_task is not None
    assert updated_task.status == "incomplete"


# T010: Test update preserves complete status
def test_update_preserves_complete_status():
    """Test that updating a task preserves 'complete' status."""
    storage = get_temp_storage()
    task = storage.add("Original title")

    completed_task = Task(
        id=task.id,
        title=task.title,
        description=task.description,
        status="complete",
        created_at=task.created_at,
    )
    # Replace in storage
    storage._tasks[0] = completed_task

    updated_task = storage.update(task.id, title="New title")

    assert updated_task is not None
    assert updated_task.status == "complete"


# T011: Test update preserves created_at timestamp
def test_update_preserves_created_at():
    """Test that updating a task preserves the created_at timestamp."""
    storage = get_temp_storage()
    task = storage.add("Original title")
    original_created_at = task.created_at

    updated_task = storage.update(task.id, title="New title")

    assert updated_task is not None
    assert updated_task.created_at == original_created_at


# T012: Test update with empty description clears it
def test_update_with_empty_description_clears_it():
    """Test that updating with empty string clears the description."""
    storage = get_temp_storage()
    task = storage.add("Original title", "Original description")

    updated_task = storage.update(task.id, description="")

    assert updated_task is not None
    assert updated_task.description == ""


# T013: Test update does not affect other tasks
def test_update_does_not_affect_other_tasks():
    """Test that updating one task doesn't affect other tasks."""
    storage = get_temp_storage()
    task1 = storage.add("Task 1", "Description 1")
    task2 = storage.add("Task 2", "Description 2")
    task3 = storage.add("Task 3", "Description 3")

    storage.update(task2.id, title="Updated Task 2")

    # Verify task1 and task3 are unchanged
    retrieved_task1 = storage.get(task1.id)
    retrieved_task3 = storage.get(task3.id)

    assert retrieved_task1 is not None
    assert retrieved_task1.title == "Task 1"
    assert retrieved_task1.description == "Description 1"

    assert retrieved_task3 is not None
    assert retrieved_task3.title == "Task 3"
    assert retrieved_task3.description == "Description 3"


# T014: Test update returns updated task
def test_update_returns_updated_task():
    """Test that update returns the updated Task object."""
    storage = get_temp_storage()
    task = storage.add("Original title", "Original description")

    updated_task = storage.update(task.id, title="New title")

    assert updated_task is not None
    assert updated_task.id == task.id
    assert updated_task.title == "New title"
    # Verify the returned task is the same as what's in storage
    stored_task = storage.get(task.id)
    assert stored_task is not None
    assert stored_task.title == "New title"


# T015: Test update strips title whitespace
def test_update_strips_title_whitespace():
    """Test that title whitespace is stripped during update."""
    storage = get_temp_storage()
    task = storage.add("Original title")

    updated_task = storage.update(task.id, title="  New title with spaces  ")

    assert updated_task is not None
    assert updated_task.title == "New title with spaces"


# T016: Test update preserves description whitespace
def test_update_preserves_description_whitespace():
    """Test that description whitespace is preserved during update."""
    storage = get_temp_storage()
    task = storage.add("Original title")

    updated_task = storage.update(task.id, description="  Description with spaces  ")

    assert updated_task is not None
    assert updated_task.description == "  Description with spaces  "
