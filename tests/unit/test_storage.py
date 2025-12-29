"""Unit tests for TaskStorage class."""

from src.storage import TaskStorage


class TestStorageInitialization:
    """Test TaskStorage initialization."""

    def test_storage_initialization(self) -> None:
        """Test that storage initializes with empty list and ID 1."""
        storage = TaskStorage()
        assert storage.count() == 0
        # Internal state check - next ID should be 1
        assert storage._next_id == 1


class TestStorageAdd:
    """Test TaskStorage add method."""

    def test_add_task_title_only(self) -> None:
        """Test adding a task with title only."""
        storage = TaskStorage()
        task = storage.add("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.status == "incomplete"
        assert storage.count() == 1

    def test_add_task_title_and_description(self) -> None:
        """Test adding a task with title and description."""
        storage = TaskStorage()
        task = storage.add("Review PR", "Check tests and security")

        assert task.id == 1
        assert task.title == "Review PR"
        assert task.description == "Check tests and security"
        assert task.status == "incomplete"
        assert storage.count() == 1

    def test_add_task_increments_id(self) -> None:
        """Test that adding multiple tasks increments IDs sequentially."""
        storage = TaskStorage()
        task1 = storage.add("Task 1")
        task2 = storage.add("Task 2")
        task3 = storage.add("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert storage.count() == 3


class TestStorageGet:
    """Test TaskStorage get method."""

    def test_get_existing_task(self) -> None:
        """Test retrieving an existing task by ID."""
        storage = TaskStorage()
        storage.add("Task 1")

        retrieved_task = storage.get(1)
        assert retrieved_task is not None
        assert retrieved_task.id == 1
        assert retrieved_task.title == "Task 1"

    def test_get_non_existent_task(self) -> None:
        """Test that get returns None for non-existent ID."""
        storage = TaskStorage()
        storage.add("Task 1")

        task = storage.get(999)
        assert task is None


class TestStorageExists:
    """Test TaskStorage exists method."""

    def test_exists_returns_true_for_existing(self) -> None:
        """Test that exists returns True for existing task."""
        storage = TaskStorage()
        storage.add("Task 1")

        assert storage.exists(1) is True

    def test_exists_returns_false_for_non_existent(self) -> None:
        """Test that exists returns False for non-existent task."""
        storage = TaskStorage()
        storage.add("Task 1")

        assert storage.exists(999) is False


class TestStorageCount:
    """Test TaskStorage count method."""

    def test_count_returns_correct_total(self) -> None:
        """Test that count returns correct number of tasks."""
        storage = TaskStorage()
        assert storage.count() == 0

        storage.add("Task 1")
        assert storage.count() == 1

        storage.add("Task 2")
        assert storage.count() == 2

        storage.add("Task 3")
        assert storage.count() == 3


class TestStorageListAll:
    """Test TaskStorage list_all method."""

    def test_list_all_returns_all_tasks(self) -> None:
        """Test that list_all returns all tasks."""
        storage = TaskStorage()
        storage.add("Task 1")
        storage.add("Task 2")

        all_tasks = storage.list_all()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2

    def test_list_all_returns_copy(self) -> None:
        """Test that list_all returns a copy to prevent external modification."""
        storage = TaskStorage()
        storage.add("Task 1")

        all_tasks = storage.list_all()
        original_count = storage.count()

        # Modify the returned list
        all_tasks.clear()

        # Storage should be unaffected
        assert storage.count() == original_count
        assert len(storage.list_all()) == original_count
