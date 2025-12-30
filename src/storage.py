"""In-memory storage for tasks with ID generation."""

import json
from datetime import datetime
from pathlib import Path

from src.models import Task

# Default storage file path
STORAGE_FILE = Path("tasks.json")


class TaskStorage:
    """In-memory storage for tasks with ID generation and file persistence."""

    def __init__(self, storage_file: Path | None = None) -> None:
        """Initialize task storage, loading from file if exists.

        Args:
            storage_file: Optional path to storage file (default: tasks.json)
        """
        self._storage_file = storage_file or STORAGE_FILE
        self._tasks: list[Task] = []
        self._next_id: int = 1
        self._load()

    def _load(self) -> None:
        """Load tasks from JSON file."""
        if self._storage_file.exists():
            try:
                data = json.loads(self._storage_file.read_text())
                self._next_id = data.get("next_id", 1)
                for task_data in data.get("tasks", []):
                    task = Task(
                        id=task_data["id"],
                        title=task_data["title"],
                        description=task_data.get("description"),
                        status=task_data.get("status", "incomplete"),
                        created_at=datetime.fromisoformat(task_data["created_at"]),
                    )
                    self._tasks.append(task)
            except (json.JSONDecodeError, KeyError, OSError):
                # If file is corrupted, start fresh
                self._tasks = []
                self._next_id = 1

    def _save(self) -> None:
        """Save tasks to JSON file."""
        data = {
            "next_id": self._next_id,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                }
                for task in self._tasks
            ],
        }
        self._storage_file.write_text(json.dumps(data, indent=2))

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
        self._save()
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

    def list_tasks(self) -> list[str]:
        """
        Get all tasks formatted for display.

        Each task is formatted as:
            [ID] SYMBOL Title
                Description (or "(none)")

        Where SYMBOL is "✓" for complete or "✗" for incomplete.

        Tasks are returned in ascending ID order (creation order).

        Returns:
            List of formatted task strings, one per task, in ID order

        Examples:
            >>> storage = TaskStorage()
            >>> storage.add("Buy groceries", "Milk, eggs")
            >>> storage.add("Call dentist")
            >>> storage.list_tasks()
            ['[1] ✗ Buy groceries\\n    Milk, eggs', '[2] ✗ Call dentist\\n    (none)']
        """
        result: list[str] = []
        # Sort tasks by ID to ensure ascending order
        sorted_tasks = sorted(self._tasks, key=lambda t: t.id)
        for task in sorted_tasks:
            # Determine status symbol
            symbol = "✓" if task.status == "complete" else "✗"

            # Format description
            description = task.description if task.description is not None else "(none)"

            # Format single task line
            task_lines = [
                f"[{task.id}] {symbol} {task.title}",
                f"    {description}",
            ]
            result.append("\n".join(task_lines))

        return result

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
                self._save()
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
                self._save()
                return updated_task
        return None

    def toggle_status(self, task_id: int) -> Task | None:
        """
        Toggle the completion status of a task by ID.

        Switches from 'incomplete' to 'complete' and vice-versa.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Updated Task object if found, None if task not found

        Examples:
            >>> storage = TaskStorage()
            >>> task = storage.add("Test")
            >>> storage.toggle_status(task.id).status
            'complete'
            >>> storage.toggle_status(task.id).status
            'incomplete'
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                new_status = (
                    "complete" if task.status == "incomplete" else "incomplete"
                )
                updated_task = Task(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    status=new_status,
                    created_at=task.created_at,
                )
                self._tasks[i] = updated_task
                self._save()
                return updated_task
        return None
