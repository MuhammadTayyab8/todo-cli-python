# Data Model: Update Task Feature

**Feature**: 001-update-task
**Date**: 2025-12-29
**Status**: No Changes Required

## Overview

The Update Task feature uses the existing Task dataclass without modifications. This document describes how the update operation interacts with the existing data model.

## Existing Entity: Task

**Location**: `src/models.py`

```python
@dataclass
class Task:
    id: int                    # Immutable - never modified by update
    title: str                 # Updatable via --title
    description: str | None    # Updatable via --desc
    status: str                # Immutable - never modified by update
    created_at: datetime       # Immutable - never modified by update
```

### Field Update Behavior

| Field | Updatable | Behavior |
|-------|-----------|----------|
| `id` | No | Preserved, used for lookup |
| `title` | Yes | Replaced if `--title` provided; stripped before storage |
| `description` | Yes | Replaced if `--desc` provided; empty string clears |
| `status` | No | Preserved ("complete" or "incomplete") |
| `created_at` | No | Preserved (original timestamp) |

### Validation Rules (Enforced at CLI Layer)

**Title** (when provided):
- Non-empty after trimming whitespace
- Length: 1-100 characters (inclusive)
- All Unicode characters allowed

**Description** (when provided):
- Length: 0-500 characters (empty string allowed)
- All Unicode characters allowed
- Whitespace preserved (not trimmed)

## Storage Method: update()

**Location**: `src/storage.py` (new method)

```python
def update(self, task_id: int, title: str | None = None,
           description: str | None = None) -> Task | None:
    """
    Update task by ID.

    Args:
        task_id: The ID of the task to update
        title: New title (None = preserve existing)
        description: New description (None = preserve existing)

    Returns:
        Updated Task if found, None if not found
    """
```

### State Transitions

The update operation creates a new Task instance with:
- Same `id`, `status`, `created_at` (preserved)
- New `title` (if provided) or existing `title`
- New `description` (if provided) or existing `description`

```
Before: Task(id=1, title="Old", description="Old desc", status="incomplete", created_at=t1)
                                    ↓
         update(1, title="New", description=None)
                                    ↓
After:  Task(id=1, title="New", description="Old desc", status="incomplete", created_at=t1)
```

## Relationship to Other Operations

| Operation | Creates Task | Modifies Task | Deletes Task |
|-----------|--------------|---------------|--------------|
| add | Yes | No | No |
| update | No | Yes | No |
| delete | No | No | Yes |

## Data Integrity Guarantees

1. **ID Uniqueness**: Preserved (update doesn't change IDs)
2. **ID Monotonicity**: Preserved (update doesn't affect ID sequence)
3. **Status Immutability**: Status can only be changed by toggle operation (not update)
4. **Timestamp Immutability**: created_at never changes after task creation
