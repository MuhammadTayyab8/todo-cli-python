# Data Model: View Tasks Feature

**Feature**: 003-view-tasks
**Date**: 2025-12-29
**Status**: No Changes Required

## Overview

The View Tasks feature uses the existing Task dataclass without modifications. This document describes how the list operation interacts with the existing data model.

## Existing Entity: Task

**Location**: `src/models.py`

```python
@dataclass
class Task:
    id: int                    # Displayed as [ID]
    title: str                 # Displayed after status symbol
    description: str | None    # Displayed under title, or "(none)"
    status: str                # Determines symbol: "complete" → ✓, "incomplete" → ✗
    created_at: datetime       # Not displayed in list (only ID, title, description, status)
```

### Field Display Behavior

| Field | Displayed | Format |
|-------|-----------|--------|
| `id` | Yes | `[ID]` with brackets |
| `title` | Yes | After status symbol |
| `description` | Yes | Under title, "(none)" if None |
| `status` | Yes | Symbol: "✓" or "✗" |
| `created_at` | No | Not shown in list |

## Display Format

### Single Task Display

```
[1] ✗ Buy groceries
    Milk, eggs, bread
```

Components:
- `[ID]` - Task ID in brackets
- `SYMBOL` - ✓ or ✗ based on status
- `Title` - Task title (preserved as-is)
- `Description` - Indented under title, "(none)" if empty

### Summary Line

```
Total: 2 tasks (1 completed, 1 pending)
```

Calculation:
- Total: `len(tasks)`
- Completed: `sum(1 for t in tasks if t.status == "complete")`
- Pending: `sum(1 for t in tasks if t.status == "incomplete")`

## Empty State

When no tasks exist:

```
TODO LIST:
────────────────────────────────────
No tasks found
```

## Data Flow

```
main.py (handle "list" command)
    ↓
cli.py (handle_list_command)
    ↓
storage.list_all() → list[Task]
    ↓
format_task_display() for each Task
    ↓
format_summary() for counts
    ↓
Print header + tasks + summary
```

## No New Entities

The View Tasks feature does not introduce new data entities. It only reads from the existing Task storage.
