"""Task data model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single to-do item.

    Attributes:
        id: Unique integer identifier (auto-generated, sequential)
        title: Task title (1-100 characters after trimming, required)
        description: Optional task description (max 500 characters)
        status: Completion status ("complete" or "incomplete")
        created_at: Timestamp when task was created (naive datetime)
    """

    id: int
    title: str
    description: str | None
    status: str
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        # Validate ID
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        # Validate title
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Task title is required and cannot be empty")

        if len(self.title) > 100:
            raise ValueError(
                f"Task title cannot exceed 100 characters (got {len(self.title)})"
            )

        # Validate description
        if self.description is not None and len(self.description) > 500:
            desc_len = len(self.description)
            raise ValueError(
                f"Task description cannot exceed 500 characters " f"(got {desc_len})"
            )

        # Validate status
        if self.status not in ("complete", "incomplete"):
            raise ValueError(
                f"Task status must be 'complete' or 'incomplete' (got '{self.status}')"
            )
