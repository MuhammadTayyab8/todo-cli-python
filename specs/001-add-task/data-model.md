# Data Model: Add Task Feature

**Date**: 2025-12-28
**Branch**: `001-add-task`
**Status**: Complete

## Overview

This document defines the data model for the "Add Task" feature, including entities, attributes, validation rules, and relationships. The model is designed for in-memory storage with no persistence requirements.

---

## Entities

### 1. Task

**Purpose**: Represents a single to-do item in the application.

**Attributes**:

| Attribute | Type | Required | Constraints | Default | Description |
|-----------|------|----------|-------------|---------|-------------|
| `id` | `int` | Yes | > 0, unique | Auto-generated | Unique identifier, sequential starting from 1 |
| `title` | `str` | Yes | 1-100 chars (trimmed) | - | Task title, describes what needs to be done |
| `description` | `Optional[str]` | No | Max 500 chars if provided | `None` | Optional detailed description, supports multi-line via newlines |
| `status` | `str` | Yes | Must be "complete" or "incomplete" | `"incomplete"` | Task completion status |
| `created_at` | `datetime` | Yes | Naive datetime | `datetime.now()` | Timestamp when task was created (no timezone) |

**Python Type Signature**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

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
    description: Optional[str]
    status: str
    created_at: datetime
```

---

## Validation Rules

### Task Entity Validation (enforced in `Task.__post_init__`)

#### ID Validation
- **Rule**: Must be a positive integer (> 0)
- **Invalid Examples**: 0, -1, 1.5, "1"
- **Error**: `ValueError("Task ID must be a positive integer")`
- **Rationale**: IDs are sequential starting from 1; zero or negative IDs are invalid

#### Title Validation
- **Rule 1**: Must not be empty after stripping whitespace
- **Rule 2**: Length must be between 1 and 100 characters (after trimming)
- **Invalid Examples**: `""`, `"   "`, `"A" * 101`
- **Trimming**: Leading/trailing whitespace removed before validation
- **Errors**:
  - Empty: `ValueError("Task title is required and cannot be empty")`
  - Too long: `ValueError("Task title cannot exceed 100 characters (got {len})")`
- **Rationale**: Title is the primary identifier for users; must be readable and not too long

#### Description Validation
- **Rule 1**: Optional (None is valid)
- **Rule 2**: If provided, max 500 characters (no trimming)
- **Invalid Examples**: `"A" * 501`
- **Valid Examples**: `None`, `""`, `"A" * 500`, `"Line1\nLine2"`
- **Error**: `ValueError("Task description cannot exceed 500 characters (got {len})")`
- **Rationale**: Descriptions provide context; 500 chars sufficient for notes while preventing abuse

#### Status Validation
- **Rule**: Must be exactly "complete" or "incomplete"
- **Invalid Examples**: `"COMPLETE"`, `"done"`, `"pending"`, `""`
- **Error**: `ValueError("Task status must be 'complete' or 'incomplete' (got '{status}')")`
- **Rationale**: Only two states defined; exact match ensures consistency

#### created_at Validation
- **Rule**: Must be a datetime instance (naive, no timezone)
- **Invalid Examples**: `"2025-12-28"`, `None`, `datetime.now(tz=timezone.utc)`
- **Error**: Implicit (Python type system will catch non-datetime)
- **Rationale**: Naive datetime sufficient for local CLI usage

---

### Input Validation (enforced in `validators.py` before Task creation)

#### validate_title(title: str) -> tuple[bool, str]

**Purpose**: Validate user-provided title before task creation.

**Rules**:
1. Title must not be None or empty string
2. After trimming whitespace, must have at least 1 character
3. After trimming, length must be ≤ 100 characters
4. All Unicode characters allowed

**Process**:
1. Check if title is None or empty → error
2. Trim leading/trailing whitespace: `title.strip()`
3. Check if trimmed title is empty → error
4. Check length of trimmed title → error if > 100

**Return Values**:
- Valid: `(True, "")`
- Invalid: `(False, "Error: Title is required and cannot be empty")` or `(False, "Error: Title must be between 1 and 100 characters (received {len})")`

**Examples**:
- `validate_title("Buy milk")` → `(True, "")`
- `validate_title("  Hello  ")` → `(True, "")` (trimmed to "Hello")
- `validate_title("")` → `(False, "Error: Title is required and cannot be empty")`
- `validate_title("   ")` → `(False, "Error: Title is required and cannot be empty")`
- `validate_title("A" * 101)` → `(False, "Error: Title must be between 1 and 100 characters (received 101)")`

---

#### validate_description(description: Optional[str]) -> tuple[bool, str]

**Purpose**: Validate user-provided description before task creation.

**Rules**:
1. Description is optional (None is valid)
2. If provided, max 500 characters (no trimming)
3. Empty string is valid
4. All Unicode characters allowed
5. Newlines preserved (multi-line support)

**Process**:
1. Check if description is None → valid (return True)
2. Check length → error if > 500

**Return Values**:
- Valid: `(True, "")`
- Invalid: `(False, "Error: Description cannot exceed 500 characters (received {len})")`

**Examples**:
- `validate_description(None)` → `(True, "")`
- `validate_description("")` → `(True, "")`
- `validate_description("Meeting notes")` → `(True, "")`
- `validate_description("Line1\nLine2")` → `(True, "")` (newlines preserved)
- `validate_description("A" * 500)` → `(True, "")`
- `validate_description("A" * 501)` → `(False, "Error: Description cannot exceed 500 characters (received 501)")`

---

## ID Generation

### Strategy: Sequential Counter

**Implementation**: `TaskStorage` class maintains a monotonic counter `_next_id: int`.

**Rules**:
- IDs start at 1 (not 0)
- IDs increment by 1 for each new task
- IDs are never reused (even after deletion)
- IDs are unique across all tasks
- IDs are integers (not UUIDs, not strings)

**Process**:
1. TaskStorage initializes with `self._next_id = 1`
2. When `add()` is called:
   - Assign `task.id = self._next_id`
   - Increment `self._next_id += 1`
   - Append task to list
3. ID counter never decrements

**Example Sequence**:
```python
storage = TaskStorage()  # _next_id = 1

task1 = storage.add("Task 1")       # task1.id = 1, _next_id = 2
task2 = storage.add("Task 2")       # task2.id = 2, _next_id = 3
task3 = storage.add("Task 3")       # task3.id = 3, _next_id = 4
# Even if task2 is deleted, next ID is still 4 (no reuse)
task4 = storage.add("Task 4")       # task4.id = 4, _next_id = 5
```

**Rationale**:
- **Simplicity**: Monotonic counter is trivial to implement and test
- **Uniqueness**: Sequential IDs guarantee uniqueness without collision risk
- **Human-readable**: Users can easily reference tasks by ID (1, 2, 3)
- **No reuse**: Prevents confusion if tasks are deleted then re-added
- **Database-friendly**: Sequential integers are efficient primary keys for future persistence

---

## Entity Relationships

### Current State (Add Task Feature Only)

**Task ← (created by) → TaskStorage**
- Task is a value object (data container)
- TaskStorage manages Task instances (lifecycle, storage, retrieval)
- No relationships between Task instances (no parent/child, no dependencies)

**Cardinality**:
- TaskStorage : Task = 1 : N (one storage holds many tasks)

### Future Extensions (Out of Scope for This Feature)

Potential relationships for future features:
- **Task → Category**: Many-to-one (tasks belong to categories)
- **Task → Tag**: Many-to-many (tasks can have multiple tags)
- **Task → Subtask**: One-to-many (tasks can have subtasks)
- **Task → User**: Many-to-one (if multi-user support added)

---

## State Transitions

### Task Status Lifecycle

```
              [Created]
                  ↓
          status = "incomplete"
                  ↓
         [User marks complete] ← Future: "complete" command
                  ↓
          status = "complete"
                  ↓
      [User marks incomplete] ← Future: "incomplete" command
                  ↓
          status = "incomplete"
                  ↓
              [Deleted] ← Future: "delete" command
```

**Current Feature (Add Task)**:
- Tasks are created with status = "incomplete"
- No state transitions (complete/incomplete toggling is a future feature)

**Future State Transitions**:
- `incomplete → complete`: Mark task as done
- `complete → incomplete`: Reopen task
- `any state → deleted`: Remove task

---

## Data Integrity Constraints

### Enforced at Task Level (Task.__post_init__)
1. ID must be positive integer
2. Title must be non-empty and ≤ 100 chars (after trim)
3. Description must be ≤ 500 chars if provided
4. Status must be "complete" or "incomplete"
5. created_at must be datetime instance

### Enforced at Storage Level (TaskStorage)
1. IDs must be unique (guaranteed by sequential counter)
2. Tasks cannot be added without title (validation before add())
3. Tasks are stored in immutable order (list append only)

### Enforced at CLI Level (CLI validation)
1. User input validated before reaching storage
2. Clear error messages for invalid input
3. No task creation if validation fails

---

## Data Examples

### Valid Task Examples

**Minimal Task (title only)**:
```python
Task(
    id=1,
    title="Buy groceries",
    description=None,
    status="incomplete",
    created_at=datetime(2025, 12, 28, 10, 30, 0)
)
```

**Full Task (title + description)**:
```python
Task(
    id=2,
    title="Review PR #456",
    description="Check for security vulnerabilities and test coverage",
    status="incomplete",
    created_at=datetime(2025, 12, 28, 11, 15, 0)
)
```

**Task with Unicode**:
```python
Task(
    id=3,
    title="Café meeting @ 3pm",
    description="Discuss Q4 roadmap & budget 💼\n中文 notes here",
    status="incomplete",
    created_at=datetime(2025, 12, 28, 14, 0, 0)
)
```

**Task with boundary length title**:
```python
Task(
    id=4,
    title="A" * 100,  # Exactly 100 characters
    description=None,
    status="incomplete",
    created_at=datetime(2025, 12, 28, 15, 0, 0)
)
```

---

### Invalid Task Examples (would raise ValueError)

```python
# Invalid ID
Task(id=0, title="Task", description=None, status="incomplete", created_at=datetime.now())
# Error: ValueError("Task ID must be a positive integer")

# Invalid title (empty)
Task(id=1, title="", description=None, status="incomplete", created_at=datetime.now())
# Error: ValueError("Task title is required and cannot be empty")

# Invalid title (too long)
Task(id=1, title="A" * 101, description=None, status="incomplete", created_at=datetime.now())
# Error: ValueError("Task title cannot exceed 100 characters (got 101)")

# Invalid description (too long)
Task(id=1, title="Task", description="A" * 501, status="incomplete", created_at=datetime.now())
# Error: ValueError("Task description cannot exceed 500 characters (got 501)")

# Invalid status
Task(id=1, title="Task", description=None, status="done", created_at=datetime.now())
# Error: ValueError("Task status must be 'complete' or 'incomplete' (got 'done')")
```

---

## Database Schema (Future Migration)

When migrating to persistent storage (database), the following schema would be suitable:

### SQL Schema (PostgreSQL/SQLite)

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- or SERIAL in PostgreSQL
    title VARCHAR(100) NOT NULL CHECK (LENGTH(TRIM(title)) > 0),
    description VARCHAR(500),
    status VARCHAR(20) NOT NULL CHECK (status IN ('complete', 'incomplete')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**Migration Notes**:
- Sequential integer ID maps directly to database AUTOINCREMENT/SERIAL
- VARCHAR lengths match validation rules (100 for title, 500 for description)
- CHECK constraints enforce status values
- Naive datetime maps to TIMESTAMP (can add timezone later)
- Indexes on status and created_at for future list/filter features

---

## Constants and Configuration

### Validation Constants (defined in validators.py)

```python
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
VALID_STATUSES = {"complete", "incomplete"}
```

---

## Summary

**Entity Count**: 1 (Task)
**Attributes**: 5 (id, title, description, status, created_at)
**Validation Rules**: 8 (ID, title non-empty, title length, description length, status values, created_at type, trimming, no reuse)
**Relationships**: 1 (TaskStorage → Task: 1:N)
**State Transitions**: 1 (creation only; future: complete/incomplete toggle, deletion)

**Data Model Status**: ✅ Complete - Ready for implementation
