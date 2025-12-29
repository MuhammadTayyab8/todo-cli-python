# Feature Specification: Delete Task

**Feature Branch**: `002-delete-task`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Feature: Delete Todo Task - User can delete a task by its ID"

## Clarifications

### Session 2025-12-29

- Q: Should we ask for confirmation before deleting? → A: No confirmation prompts - Direct deletion for fast, scriptable CLI (follows Unix philosophy)
- Q: Should delete show task details before removal? → A: Show only ID in success message - "Task deleted successfully (ID: 1)" for concise output
- Q: Should deletion update any task counters/stats? → A: No statistics tracking - Only remove task from storage (simple, stateless design)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Delete Existing Task by ID (Priority: P1)

As a user, I want to delete a task by its ID so that I can remove tasks that are no longer needed or were created by mistake.

**Why this priority**: This is the core value proposition of the delete feature. Users need to be able to remove unwanted tasks to keep their todo list clean and manageable. This represents the minimum viable functionality.

**Independent Test**: Can be fully tested by creating a task, deleting it by ID, and verifying the task no longer exists and a success message is displayed.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1, **When** I execute `todo delete 1`, **Then** the system removes the task from storage and displays "Task deleted successfully (ID: 1)"
2. **Given** I have tasks with IDs 1, 2, and 3, **When** I execute `todo delete 2`, **Then** the system removes only task 2, leaving tasks 1 and 3 intact
3. **Given** I have deleted task 5, **When** I attempt to retrieve task 5, **Then** the system confirms the task no longer exists

---

### User Story 2 - Error Handling for Non-Existent Tasks (Priority: P2)

As a user, I want to receive a clear error message when attempting to delete a task that doesn't exist so that I understand why the operation failed.

**Why this priority**: Good error handling improves user experience but is not blocking for core functionality. Users can still successfully delete existing tasks even without this.

**Independent Test**: Can be tested by attempting to delete a task ID that doesn't exist and verifying the appropriate error message is displayed.

**Acceptance Scenarios**:

1. **Given** no task with ID 999 exists, **When** I execute `todo delete 999`, **Then** the system returns error "Error: Task not found (ID: 999)" and does not modify storage
2. **Given** an empty task list, **When** I execute `todo delete 1`, **Then** the system returns error "Error: Task not found (ID: 1)"
3. **Given** I have deleted task 5, **When** I execute `todo delete 5` again, **Then** the system returns error "Error: Task not found (ID: 5)" (cannot delete twice)

---

### User Story 3 - Validation for Invalid Task IDs (Priority: P3)

As a user, I want to receive clear error messages when I provide an invalid task ID so that I understand the correct format and can successfully delete tasks.

**Why this priority**: Input validation improves user experience but users who provide valid IDs can still use the feature successfully. This is a polish feature.

**Independent Test**: Can be tested by providing various invalid ID formats (non-numeric, negative, zero) and verifying appropriate error messages.

**Acceptance Scenarios**:

1. **Given** the todo application is running, **When** I execute `todo delete abc`, **Then** the system returns error "Error: Task ID must be a positive integer"
2. **Given** the todo application is running, **When** I execute `todo delete -5`, **Then** the system returns error "Error: Task ID must be a positive integer"
3. **Given** the todo application is running, **When** I execute `todo delete 0`, **Then** the system returns error "Error: Task ID must be a positive integer"
4. **Given** the todo application is running, **When** I execute `todo delete` with no ID argument, **Then** the system displays usage help showing correct command format

---

### Edge Cases

- **Non-existent task ID**: System returns error "Task not found (ID: {id})"
- **Already deleted task**: System returns same "Task not found" error (idempotent failure)
- **Empty storage**: Attempting to delete from empty list returns "Task not found" error
- **Invalid ID format (non-numeric)**: System returns "Task ID must be a positive integer"
- **Negative task ID**: System returns "Task ID must be a positive integer"
- **Zero task ID**: System returns "Task ID must be a positive integer" (IDs start at 1)
- **Floating point ID** (e.g., 1.5): System returns "Task ID must be a positive integer"
- **Very large task ID** (e.g., 999999): System checks existence and returns "Task not found" if doesn't exist
- **Missing ID argument**: System displays usage help
- **Multiple ID arguments** (e.g., `todo delete 1 2 3`): Out of scope; delete one task at a time (system treats as error or takes first argument)
- **Whitespace in ID** (e.g., " 5 "): System should trim and parse or reject
- **ID reuse**: Deleted task IDs are not reused; deletion doesn't affect ID sequence for future additions
- **Concurrent deletion** (if multi-threaded): Out of scope for single-user CLI app

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task ID as the required argument for deletion
- **FR-002**: System MUST validate that the task ID is a positive integer (1 or greater)
- **FR-003**: System MUST check if a task with the given ID exists in storage
- **FR-004**: System MUST remove the task from storage if it exists
- **FR-005**: System MUST return a success message displaying the deleted task's ID
- **FR-006**: System MUST return error message "Task not found (ID: {id})" if task doesn't exist
- **FR-007**: System MUST return error message "Task ID must be a positive integer" for invalid ID formats
- **FR-008**: System MUST return success messages to stdout with exit code 0
- **FR-009**: System MUST return error messages to stderr with exit code 1
- **FR-010**: System MUST NOT reuse deleted task IDs for future additions (maintain monotonic ID sequence)
- **FR-011**: System MUST support deletion as a permanent, non-reversible operation (no undo)
- **FR-012**: System MUST NOT prompt for confirmation before deletion (direct deletion for scriptability)
- **FR-013**: System MUST display usage help when ID argument is missing
- **FR-014**: System MUST use argparse for CLI argument parsing (per constitution)
- **FR-015**: Deletion operates on in-memory storage only (no file system changes)
- **FR-016**: System MUST NOT track deletion statistics, counters, or history (stateless design)

### Key Entities

- **Task**: (Existing entity from add-task feature)
  - `id` (integer): Unique identifier used for deletion
  - `title`, `description`, `status`, `created_at`: Not directly used by delete operation but removed along with task

- **TaskRepository/TaskStorage**: (Existing entity from add-task feature)
  - **New method**: `delete(task_id: int) -> bool`: Removes task from storage, returns True if deleted, False if not found
  - Storage structure must support efficient deletion (O(1) for dict-based storage)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully delete an existing task in under 2 seconds (command execution time)
- **SC-002**: System correctly rejects 100% of invalid task IDs (non-numeric, negative, zero) with clear error messages
- **SC-003**: System correctly handles 100% of non-existent task ID requests with "Task not found" error
- **SC-004**: Deletion operation maintains storage integrity (no orphaned data, no corruption)
- **SC-005**: All delete functionality maintains 80%+ test coverage (per constitution requirement)
- **SC-006**: CLI interface matches constitutional requirements (argparse, stdout/stderr, exit codes)
- **SC-007**: Deleted task IDs are never reused in subsequent task additions (ID sequence integrity maintained)

## CLI Interface Examples

### Command Format

```bash
todo delete <task_id>
```

### Successful Deletion

**Example 1: Delete existing task**
```bash
$ todo delete 1
Task deleted successfully (ID: 1)
```

**Example 2: Delete from multiple tasks**
```bash
# Before: tasks 1, 2, 3 exist
$ todo delete 2
Task deleted successfully (ID: 2)
# After: tasks 1, 3 remain
```

### Error Scenarios

**Example 1: Non-existent task ID**
```bash
$ todo delete 999
Error: Task not found (ID: 999)
Exit code: 1
```

**Example 2: Empty task list**
```bash
$ todo delete 1
Error: Task not found (ID: 1)
Exit code: 1
```

**Example 3: Already deleted task**
```bash
$ todo delete 5
Task deleted successfully (ID: 5)

$ todo delete 5
Error: Task not found (ID: 5)
Exit code: 1
```

**Example 4: Invalid ID format (non-numeric)**
```bash
$ todo delete abc
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 5: Negative task ID**
```bash
$ todo delete -5
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 6: Zero task ID**
```bash
$ todo delete 0
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 7: Missing ID argument**
```bash
$ todo delete
Error: Missing required argument: task_id
Usage: todo delete <task_id>
Exit code: 1
```

## Input Validation Rules

### Task ID Validation

1. **Required**: Task ID argument must be provided
2. **Type**: Must be convertible to integer
3. **Range**: Must be a positive integer (≥ 1)
4. **Existence check**: After validation, system checks if task exists in storage

**Validation Logic**:
```python
def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """
    Validates task ID according to requirements.

    Args:
        task_id_str: The task ID string from command line

    Returns:
        Tuple of (is_valid: bool, error_message: str, parsed_id: int | None)
        error_message is empty string if valid
        parsed_id is the integer ID if valid, None otherwise
    """
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a positive integer", None

    if task_id < 1:
        return False, "Task ID must be a positive integer", None

    return True, "", task_id
```

## Error Handling

### Error Types and Responses

| Error Scenario          | Error Message                                                                 | Exit Code | Output Channel |
|-------------------------|-------------------------------------------------------------------------------|-----------|----------------|
| Task not found          | "Error: Task not found (ID: {id})"                                           | 1         | stderr         |
| Invalid ID format       | "Error: Task ID must be a positive integer"                                  | 1         | stderr         |
| Negative/zero ID        | "Error: Task ID must be a positive integer"                                  | 1         | stderr         |
| Missing ID argument     | "Error: Missing required argument: task_id\nUsage: todo delete <task_id>"   | 1         | stderr         |

### Error Handling Principles

1. **Clear messages**: Errors clearly state what went wrong
2. **Specific values**: Include the problematic ID in error messages when relevant
3. **Consistent format**: All errors start with "Error: " prefix
4. **Proper channels**: Errors to stderr, success messages to stdout
5. **Exit codes**: Exit code 0 for success, exit code 1 for all errors
6. **No partial deletion**: If validation fails, no storage changes occur
7. **Idempotent failures**: Deleting non-existent task returns same error every time

## Testing Requirements

### Test Coverage Mandate

Per constitution requirement: Minimum 80% test coverage for all code

### Test Categories

#### 1. Unit Tests (validation, storage operations)

**Test Suite: Task ID Validation**
- Test valid task ID (1) - boundary
- Test valid task ID (100) - typical
- Test invalid task ID (0) - boundary
- Test invalid task ID (-1) - negative
- Test invalid task ID (-100) - negative
- Test invalid task ID (non-numeric string: "abc")
- Test invalid task ID (floating point string: "1.5")
- Test invalid task ID (empty string)
- Test invalid task ID (whitespace: "   ")

**Test Suite: TaskStorage Delete Method**
- Test delete existing task returns True
- Test delete non-existent task returns False
- Test delete from empty storage returns False
- Test delete removes task from storage (verify with get)
- Test delete doesn't affect other tasks
- Test delete multiple tasks in sequence
- Test storage count decreases after successful delete
- Test storage count unchanged after failed delete

#### 2. Integration Tests (CLI command workflow)

**Test Suite: Delete Command Integration**
- Test `todo delete 1` deletes existing task with ID 1
- Test `todo delete 1` returns success message with ID
- Test `todo delete 999` returns "Task not found" error
- Test deleting from empty list returns error
- Test deleting already-deleted task returns error (idempotent)
- Test deleting middle task leaves others intact (delete 2, verify 1 and 3 exist)
- Test invalid ID format returns error and exit code 1
- Test negative ID returns error and exit code 1
- Test zero ID returns error and exit code 1
- Test missing ID argument returns error and usage help
- Test error messages go to stderr
- Test success messages go to stdout

#### 3. Edge Case Tests

**Test Suite: Boundary Conditions**
- Test delete task with ID 1 (minimum valid)
- Test delete task with very large ID (e.g., 999999 - not found)
- Test delete task ID 0 (invalid boundary)
- Test delete task ID -1 (invalid boundary)

**Test Suite: Storage Integrity**
- Test deleting task doesn't affect ID sequence for future additions
- Test deleting all tasks leaves storage empty (count = 0)
- Test adding task after deletion uses next sequential ID (doesn't reuse)

**Test Suite: Error Scenarios**
- Test non-numeric ID: "abc", "task1", "delete"
- Test floating point ID: "1.5", "2.7"
- Test whitespace ID: "  ", "\t", "\n"
- Test special characters: "#1", "!5"

### Test Organization Structure

```
tests/
├── unit/
│   ├── test_task_id_validation.py    # ID validation tests
│   └── test_storage_delete.py        # Storage delete operation tests
├── integration/
│   ├── test_delete_command.py        # Full CLI workflow tests
│   └── test_delete_error_handling.py # Error scenario integration tests
└── fixtures/
    └── sample_tasks.py               # Shared test data (reused from add-task)
```

### Test Execution Requirements

1. **Pre-implementation**: Tests MUST be written before implementation (TDD)
2. **Failure verification**: Tests MUST fail initially (Red phase)
3. **Minimum coverage**: 80% coverage required to pass (pytest-cov)
4. **CI validation**: All tests must pass before merge
5. **Isolation**: Each test is independent; no shared state between tests
6. **Fast execution**: Full test suite should complete in under 10 seconds

## Data Model Changes

### TaskStorage Updates

**New Method**:
```python
def delete(self, task_id: int) -> bool:
    """
    Delete task by ID.

    Args:
        task_id: The ID of the task to delete

    Returns:
        True if task was deleted, False if task not found
    """
    if task_id in self._tasks:
        del self._tasks[task_id]
        return True
    return False
```

**No changes to**:
- Task dataclass (delete operates on existing structure)
- ID generation logic (deleted IDs never reused; sequence continues)
- Existing add/get/exists/count methods

## Dependencies and Constraints

### Dependencies (Per Constitution)

- **Python Standard Library Only**: argparse (existing dependency from add-task)
- **No External Runtime Dependencies**: No third-party packages
- **Testing Only**: pytest, pytest-cov (existing development dependencies)

### Constraints (Per Constitution)

- **In-Memory Only**: No file I/O, no database, deletion only affects memory
- **Type Hints Mandatory**: All functions must have type annotations
- **Docstrings Required**: Google-style docstrings for all public APIs
- **TDD Required**: Tests written first, verified to fail, then implemented
- **80% Coverage**: Minimum test coverage threshold

## Out of Scope

The following are explicitly excluded from this feature:

- **Undo/undelete**: Deletion is permanent; no recovery mechanism
- **Bulk deletion**: Deleting multiple tasks at once (e.g., `delete 1 2 3`)
- **Confirmation prompts**: No interactive "Are you sure?" dialog or --force flags (confirmed: direct deletion for scriptability)
- **Soft delete**: No "trash" or "archived" status; tasks are permanently removed
- **Task detail display**: Success message shows only ID, not full task details (confirmed: concise output)
- **Deletion by title**: Must use task ID, not title/description search
- **Cascading deletion**: No related data to cascade (in-memory, no relationships)
- **Audit trail**: No logging of deletion events beyond CLI output
- **Permission checks**: No access control (single-user app)
- **ID reuse**: Deleted task IDs remain retired (not reused for new tasks)
- **Statistics/counters**: No tracking of deletion counts, history, or metrics (confirmed: stateless design)

## Assumptions

1. **Prerequisite**: Add Task feature (`001-add-task`) is fully implemented and working
2. **Storage implementation**: TaskStorage uses dict-based storage enabling O(1) deletion
3. **ID format**: Task IDs are always positive integers (guaranteed by add feature)
4. **Single deletion**: Users delete one task at a time (no batch operations)
5. **No recovery needed**: Users accept deletion is permanent (or will use external backups/undo at OS level)
6. **Error tolerance**: Users can handle "Task not found" errors gracefully

## Next Steps

After spec approval:

1. **Run `/sp.clarify`** (if needed): Ask targeted questions to resolve any ambiguities
2. **Create implementation plan** (`/sp.plan`): Define technical changes to existing codebase, integration points
3. **Generate task breakdown** (`/sp.tasks`): Break into atomic, testable tasks with TDD workflow
4. **Write tests first** (Red phase): Implement all test cases, verify failures
5. **Implement feature** (Green phase): Add delete method to storage, add CLI command handler
6. **Refactor** (Refactor phase): Improve code quality while maintaining passing tests
7. **Validate coverage**: Ensure ≥80% coverage with pytest-cov
8. **Manual testing**: Execute CLI commands to verify user experience
9. **Create PHR**: Document the implementation work
