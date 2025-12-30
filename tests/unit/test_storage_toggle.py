"""Unit tests for task status toggling."""

import pytest
from src.storage import TaskStorage
from src.models import Task

def test_toggle_incomplete_to_complete(tmp_path):
    """Test switching status from incomplete to complete."""
    storage_file = tmp_path / "tasks.json"
    storage = TaskStorage(storage_file=storage_file)
    task = storage.add("Test task")
    assert task.status == "incomplete"

    updated_task = storage.toggle_status(task.id)
    assert updated_task is not None
    assert updated_task.status == "complete"

    # Verify persistence
    storage2 = TaskStorage(storage_file=storage_file)
    assert storage2.get(task.id).status == "complete"

def test_toggle_complete_to_incomplete(tmp_path):
    """Test switching status from complete back to incomplete."""
    storage_file = tmp_path / "tasks.json"
    storage = TaskStorage(storage_file=storage_file)
    task = storage.add("Test task")

    # First toggle to complete
    storage.toggle_status(task.id)

    # Second toggle back to incomplete
    updated_task = storage.toggle_status(task.id)
    assert updated_task is not None
    assert updated_task.status == "incomplete"

def test_toggle_non_existent_id():
    """Test toggling a status for an ID that does not exist."""
    storage = TaskStorage(storage_file=None)  # Use default or empty
    result = storage.toggle_status(999)
    assert result is None
