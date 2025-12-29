"""Unit tests for TaskStorage.delete() method."""

from src.storage import TaskStorage


def test_delete_existing_task_returns_true():
    """Test that deleting an existing task returns True."""
    storage = TaskStorage()
    task = storage.add("Test task")

    result = storage.delete(task.id)

    assert result is True


def test_delete_non_existent_task_returns_false():
    """Test that deleting a non-existent task returns False."""
    storage = TaskStorage()
    storage.add("Test task")

    result = storage.delete(999)

    assert result is False


def test_delete_from_empty_storage_returns_false():
    """Test that deleting from empty storage returns False."""
    storage = TaskStorage()

    result = storage.delete(1)

    assert result is False


def test_delete_removes_task_from_storage():
    """Test that delete actually removes the task (verify with get)."""
    storage = TaskStorage()
    task = storage.add("Test task")

    storage.delete(task.id)
    retrieved_task = storage.get(task.id)

    assert retrieved_task is None


def test_delete_doesnt_affect_other_tasks():
    """Test that deleting task 2 from [1,2,3] leaves 1 and 3 intact."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")
    task3 = storage.add("Task 3")

    storage.delete(task2.id)

    assert storage.get(task1.id) is not None
    assert storage.get(task2.id) is None
    assert storage.get(task3.id) is not None


def test_delete_multiple_tasks_in_sequence():
    """Test deleting multiple tasks one by one."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")
    task3 = storage.add("Task 3")

    result1 = storage.delete(task1.id)
    result2 = storage.delete(task2.id)
    result3 = storage.delete(task3.id)

    assert result1 is True
    assert result2 is True
    assert result3 is True
    assert storage.count() == 0


def test_storage_count_decreases_after_delete():
    """Test that count() decrements after successful deletion."""
    storage = TaskStorage()
    storage.add("Task 1")
    task2 = storage.add("Task 2")
    storage.add("Task 3")

    initial_count = storage.count()
    storage.delete(task2.id)
    final_count = storage.count()

    assert final_count == initial_count - 1
    assert final_count == 2


def test_storage_count_unchanged_after_failed_delete():
    """Test that count remains the same when delete fails (not found)."""
    storage = TaskStorage()
    storage.add("Task 1")
    storage.add("Task 2")

    initial_count = storage.count()
    storage.delete(999)
    final_count = storage.count()

    assert final_count == initial_count
    assert final_count == 2


def test_deleting_task_doesnt_affect_id_sequence():
    """Test that deleting a task doesn't affect ID sequence for future additions."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")
    task3 = storage.add("Task 3")

    # Delete task 2
    storage.delete(task2.id)

    # Add a new task - should get ID 4 (not reusing ID 2)
    task4 = storage.add("Task 4")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3
    assert task4.id == 4  # Should be 4, not 2
