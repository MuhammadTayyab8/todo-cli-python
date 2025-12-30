# Research: View Tasks Feature

**Feature**: 003-view-tasks
**Date**: 2025-12-29
**Status**: Complete

## Overview

This document captures research findings for implementing the View Tasks (list) feature. Since this feature leverages existing patterns from Add/Update/Delete features, research was focused on confirming existing capabilities and identifying any gaps.

## Key Findings

### Existing Storage Capabilities

**Finding**: TaskStorage already has `list_all()` method
- Returns: `list[Task]` (copy of internal list)
- Order: Already in creation order (ID ascending)
- Behavior: Returns empty list if no tasks

**Decision**: Use `list_all()` directly, no new storage method needed

### Formatting Requirements

**Output Format from spec.md**:
```
TODO LIST:
────────────────────────────────────
[1] ✗ Buy groceries
    Milk, eggs, bread

[2] ✓ Call dentist
    Schedule appointment

Total: 2 tasks (1 completed, 1 pending)
```

**Components needed**:
1. Header: "TODO LIST:" line
2. Divider: "────────────────────────────────────"
3. Task display: "[ID] SYMBOL Title\n    Description"
4. Summary: "Total: N tasks (X completed, Y pending)"

### Status Symbols

**Requirement**: ✓ for complete, ✗ for incomplete

**Implementation**:
```python
def get_status_symbol(status: str) -> str:
    """Return status symbol for display."""
    return "✓" if status == "complete" else "✗"
```

### Empty State Handling

**Requirement**: "No tasks found" message when storage is empty

**Implementation**:
```python
TODO LIST:
────────────────────────────────────
No tasks found
```

## Alternatives Considered

### Option 1: Use existing list_all() (chosen)
- Pros: No new storage methods, reuses existing functionality
- Cons: Formatting logic needed in CLI layer

### Option 2: Add list_tasks() to storage
- Pros: All formatting in one place
- Cons: Storage layer should not handle display concerns (separation of concerns)

### Decision**: Option 1 - Formatting in CLI, storage provides data

## Implementation Implications

1. **No changes to storage.py needed** - existing `list_all()` sufficient
2. **New functions in cli.py**:
   - `format_task_display(task: Task) -> str`
   - `format_list_header() -> str`
   - `format_summary(tasks: list[Task]) -> str`
3. **No validators needed** - list command has no user input
4. **main.py routing** - add "list" command handler

## Summary

- **Research Complete**: All decisions documented in plan.md (ADR-006)
- **No clarifications needed**: Requirements are complete
- **Ready for**: /sp.tasks to generate implementation tasks
