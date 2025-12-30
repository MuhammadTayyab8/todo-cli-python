"""In-memory storage for tasks with ID generation."""

from datetime import datetime

from src.models import Task


class TaskStorage:
    """In-memory storage for tasks with ID generation."""

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: str | None = None) -> Task:
        """
        Create and store a new task.

        Args:
            title: Task title (required)
            description: Task description (optional)

        Returns:
            The created Task instance
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status="incomplete",
            created_at=datetime.now(),
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task | None:
        """
        Retrieve task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task instance if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def exists(self, task_id: int) -> bool:
        """
        Check if task with given ID exists.

        Args:
            task_id: The ID to check

        Returns:
            True if task exists, False otherwise
        """
        return self.get(task_id) is not None

    def count(self) -> int:
        """
        Return total number of tasks.

        Returns:
            Number of tasks in storage
        """
        return len(self._tasks)

    def list_all(self) -> list[Task]:
        """
        Return all tasks.

        Returns:
            Copy of the task list to prevent external modification
        """
        return self._tasks.copy()

    def delete(self, task_id: int) -> bool:
        """
        Delete task by ID.

        Removes the task from storage if it exists. Does not reuse the deleted ID
        for future task additions (ID sequence remains monotonic).

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if task was deleted, False if task not found

        Examples:
            >>> storage = TaskStorage()
            >>> task = storage.add("Buy milk")
            >>> storage.delete(task.id)
            True
            >>> storage.delete(999)
            False
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def update(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> Task | None:
        """
        Update task by ID.

        Updates the title and/or description of an existing task. At least one
        of title or description should be provided (enforced at CLI layer).
        The task's ID, status, and created_at timestamp are always preserved.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided, replaces existing; whitespace is stripped)
            description: New description (if provided, replaces existing;
                        empty string clears it; whitespace is preserved)

        Returns:
            Updated Task object if found, None if task not found

        Note:
            - At least one of title or description must be provided
              (enforced at CLI layer)
            - Status and created_at are never modified
            - Validation happens at CLI layer before calling this method
            - Title whitespace is stripped, description whitespace is preserved

        Examples:
            >>> storage = TaskStorage()
            >>> task = storage.add("Buy milk", "From the store")
            >>> updated = storage.update(task.id, title="Buy groceries")
            >>> updated.title
            'Buy groceries'
            >>> updated.description
            'From the store'
            >>> storage.update(999, title="New title")  # Non-existent
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                updated_task = Task(
                    id=task.id,
                    title=title.strip() if title is not None else task.title,
                    description=(
                        description if description is not None else task.description
                    ),
                    status=task.status,
                    created_at=task.created_at,
                )
                self._tasks[i] = updated_task
                return updated_task
        return None
