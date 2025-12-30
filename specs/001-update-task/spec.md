# Feature Specification: Update Task

**Feature Branch**: `001-update-task`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Feature: Update Todo Task - User can update task title and/or description by ID"

## Clarifications

### Session 2025-12-29

- Q: Should update show before/after values or only final state? → A: Show only final values (consistent with Add/Delete, minimal output, scriptable)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update Task Title Only (Priority: P1)

As a user, I want to update only the title of an existing task so that I can correct mistakes or improve task descriptions without losing other information.

**Why this priority**: This is the most common update scenario. Users often need to fix typos, clarify task names, or update titles as requirements evolve. This represents the core value proposition of the update feature.

**Independent Test**: Can be fully tested by creating a task, updating only its title, and verifying the title changed while the description remained unchanged.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1, title "Buy groceries", and description "Get milk and eggs", **When** I execute `python main.py update 1 --title "Buy weekly groceries"`, **Then** the system updates the title to "Buy weekly groceries", keeps description "Get milk and eggs" unchanged, and displays success message with updated task details
2. **Given** I have a task with ID 2, title "Review PR", and no description, **When** I execute `python main.py update 2 --title "Review PR #456"`, **Then** the system updates the title and confirms the description remains empty
3. **Given** I have a completed task with ID 3, **When** I execute `python main.py update 3 --title "New title"`, **Then** the system updates the title and the completed status remains unchanged

---

### User Story 2 - Update Task Description Only (Priority: P2)

As a user, I want to update only the description of an existing task so that I can add details or context without modifying the task title.

**Why this priority**: Adding or updating descriptions is common when users need to expand on task details. This complements the title-only update and together they form the complete partial update capability.

**Independent Test**: Can be tested by creating a task, updating only its description, and verifying the description changed while the title remained unchanged.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1, title "Buy groceries", and no description, **When** I execute `python main.py update 1 --desc "Get milk, eggs, and bread from the store"`, **Then** the system adds the description while keeping the title unchanged
2. **Given** I have a task with ID 2, title "Review PR", and description "Check for bugs", **When** I execute `python main.py update 2 --desc "Check for bugs and security vulnerabilities"`, **Then** the system replaces the description with the new value and keeps the title unchanged
3. **Given** I have a task with existing description, **When** I execute `python main.py update 1 --desc ""`, **Then** the system clears the description (sets to empty) while keeping the title unchanged

---

### User Story 3 - Update Both Title and Description (Priority: P2)

As a user, I want to update both the title and description of a task in a single command so that I can efficiently make comprehensive changes.

**Why this priority**: Same priority as description-only since both provide complete update flexibility. This enables efficiency when both fields need changes.

**Independent Test**: Can be tested by creating a task, updating both fields, and verifying both changed to the new values.

**Acceptance Scenarios**:

1. **Given** I have a task with ID 1, title "Old title", and description "Old description", **When** I execute `python main.py update 1 --title "New title" --desc "New description"`, **Then** the system updates both fields and displays success message with all updated values
2. **Given** I have a task with ID 2, title "Meeting", and no description, **When** I execute `python main.py update 2 --title "Team Meeting" --desc "Discuss Q1 roadmap"`, **Then** the system updates the title and adds the description

---

### User Story 4 - Error Handling for Non-Existent Tasks (Priority: P3)

As a user, I want to receive a clear error message when attempting to update a task that doesn't exist so that I understand why the operation failed.

**Why this priority**: Good error handling improves user experience but is not blocking for core functionality. Users can still successfully update existing tasks.

**Independent Test**: Can be tested by attempting to update a task ID that doesn't exist and verifying the appropriate error message is displayed.

**Acceptance Scenarios**:

1. **Given** no task with ID 999 exists, **When** I execute `python main.py update 999 --title "New title"`, **Then** the system returns error "Error: Task not found (ID: 999)" and does not modify storage
2. **Given** an empty task list, **When** I execute `python main.py update 1 --desc "New description"`, **Then** the system returns error "Error: Task not found (ID: 1)"
3. **Given** I have deleted task 5, **When** I execute `python main.py update 5 --title "New title"`, **Then** the system returns error "Error: Task not found (ID: 5)"

---

### Edge Cases

- **Non-existent task ID**: System returns error "Task not found (ID: {id})"
- **Invalid ID format (non-numeric)**: System returns "Task ID must be a positive integer"
- **Negative task ID**: System returns "Task ID must be a positive integer"
- **Zero task ID**: System returns "Task ID must be a positive integer" (IDs start at 1)
- **No update arguments provided**: System returns error "Error: At least one of --title or --desc must be provided"
- **Empty title after trimming**: System returns error "Title cannot be empty" (same validation as add)
- **Title exceeds 100 characters**: System returns error "Title must be between 1 and 100 characters"
- **Description exceeds 500 characters**: System returns error "Description cannot exceed 500 characters"
- **Update completed task**: Status remains unchanged (update only affects title/description)
- **Update with identical values**: System accepts and returns success (idempotent operation)
- **Missing ID argument**: System displays usage help showing correct command format
- **Title with only whitespace**: System treats as empty and rejects
- **Clear description with empty string**: Allowed - sets description to empty/None

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a task ID as the required first argument for update
- **FR-002**: System MUST accept an optional `--title` flag with text argument
- **FR-003**: System MUST accept an optional `--desc` flag with text argument
- **FR-004**: System MUST require at least one of `--title` or `--desc` to be provided
- **FR-005**: System MUST validate that the task ID is a positive integer (1 or greater)
- **FR-006**: System MUST check if a task with the given ID exists in storage
- **FR-007**: System MUST validate title length between 1 and 100 characters (if provided)
- **FR-008**: System MUST validate description length maximum of 500 characters (if provided)
- **FR-009**: System MUST preserve unchanged fields when only partial update is requested
- **FR-010**: System MUST NOT modify the task's completion status during update
- **FR-011**: System MUST NOT modify the task's creation timestamp during update
- **FR-012**: System MUST NOT modify the task's ID during update
- **FR-013**: System MUST return a success message displaying only the final state of the updated task (ID, title, description, status) - no before/after diff
- **FR-014**: System MUST return error message "Task not found (ID: {id})" if task doesn't exist
- **FR-015**: System MUST return error message "Task ID must be a positive integer" for invalid ID formats
- **FR-016**: System MUST return success messages to stdout with exit code 0
- **FR-017**: System MUST return error messages to stderr with exit code 1
- **FR-018**: System MUST use argparse for CLI argument parsing (per constitution)
- **FR-019**: Update operates on in-memory storage only (no file system changes)
- **FR-020**: System MUST allow clearing description by passing empty string `--desc ""`

### Key Entities

- **Task**: (Existing entity from add-task feature)
  - `id` (integer): Unique identifier used for locating task to update (immutable)
  - `title` (string): Can be updated if `--title` is provided
  - `description` (string): Can be updated if `--desc` is provided
  - `status` (string): NOT modified by update operation (preserved)
  - `created_at` (datetime): NOT modified by update operation (preserved)

- **TaskRepository/TaskStorage**: (Existing entity from add-task feature)
  - **New method**: `update(task_id: int, title: str | None = None, description: str | None = None) -> Task | None`: Updates task fields, returns updated task or None if not found

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully update a task title in under 2 seconds (command execution time)
- **SC-002**: User can successfully update a task description in under 2 seconds
- **SC-003**: User can successfully update both title and description in under 2 seconds
- **SC-004**: System correctly preserves 100% of unchanged fields during partial updates
- **SC-005**: System correctly rejects 100% of invalid task IDs (non-numeric, negative, zero) with clear error messages
- **SC-006**: System correctly handles 100% of non-existent task ID requests with "Task not found" error
- **SC-007**: Completion status is never modified by update operations (100% preservation)
- **SC-008**: All update functionality maintains 80%+ test coverage (per constitution requirement)
- **SC-009**: CLI interface matches constitutional requirements (argparse, stdout/stderr, exit codes)

## CLI Interface Examples

### Command Format

```bash
python main.py update <task_id> [--title <text>] [--desc <text>]
```

### Successful Updates

**Example 1: Update title only**
```bash
$ python main.py update 1 --title "Buy weekly groceries"
Task updated successfully
  ID: 1
  Title: Buy weekly groceries
  Description: Get milk and eggs
  Status: incomplete
```

**Example 2: Update description only**
```bash
$ python main.py update 1 --desc "Get milk, eggs, bread, and cheese"
Task updated successfully
  ID: 1
  Title: Buy groceries
  Description: Get milk, eggs, bread, and cheese
  Status: incomplete
```

**Example 3: Update both title and description**
```bash
$ python main.py update 1 --title "Weekly grocery shopping" --desc "Saturday morning shopping list"
Task updated successfully
  ID: 1
  Title: Weekly grocery shopping
  Description: Saturday morning shopping list
  Status: incomplete
```

**Example 4: Clear description**
```bash
$ python main.py update 1 --desc ""
Task updated successfully
  ID: 1
  Title: Buy groceries
  Description: (none)
  Status: incomplete
```

**Example 5: Update completed task (status preserved)**
```bash
$ python main.py update 3 --title "Completed task - updated title"
Task updated successfully
  ID: 3
  Title: Completed task - updated title
  Description: Some description
  Status: complete
```

### Error Scenarios

**Example 1: Non-existent task ID**
```bash
$ python main.py update 999 --title "New title"
Error: Task not found (ID: 999)
Exit code: 1
```

**Example 2: Invalid ID format (non-numeric)**
```bash
$ python main.py update abc --title "New title"
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 3: Negative task ID**
```bash
$ python main.py update -5 --title "New title"
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 4: Zero task ID**
```bash
$ python main.py update 0 --title "New title"
Error: Task ID must be a positive integer
Exit code: 1
```

**Example 5: No update arguments**
```bash
$ python main.py update 1
Error: At least one of --title or --desc must be provided
Usage: python main.py update <task_id> [--title <text>] [--desc <text>]
Exit code: 1
```

**Example 6: Empty title**
```bash
$ python main.py update 1 --title ""
Error: Title cannot be empty
Exit code: 1
```

**Example 7: Title too long**
```bash
$ python main.py update 1 --title "This is a very long title that exceeds one hundred characters and should trigger validation error..."
Error: Title must be between 1 and 100 characters (received 101)
Exit code: 1
```

**Example 8: Description too long**
```bash
$ python main.py update 1 --desc "[501+ characters...]"
Error: Description cannot exceed 500 characters (received 501)
Exit code: 1
```

**Example 9: Missing ID argument**
```bash
$ python main.py update
Error: Missing required argument: task_id
Usage: python main.py update <task_id> [--title <text>] [--desc <text>]
Exit code: 1
```

## Input Validation Rules

### Task ID Validation

1. **Required**: Task ID argument must be provided
2. **Type**: Must be convertible to integer
3. **Range**: Must be a positive integer (>= 1)
4. **Existence check**: After validation, system checks if task exists in storage

### Title Validation (when provided)

1. **Non-empty**: After stripping leading/trailing whitespace, title must have at least 1 character
2. **Length**: Title must be between 1 and 100 characters (inclusive) after trimming
3. **Character set**: All Unicode characters allowed
4. **Processing**: Trim leading/trailing whitespace before validation and storage

### Description Validation (when provided)

1. **Empty allowed**: Empty string is valid (clears description)
2. **Length**: If provided, description cannot exceed 500 characters
3. **Character set**: All Unicode characters allowed
4. **Processing**: No trimming; preserve exact input

### Update Arguments Validation

1. **At least one required**: Either `--title` or `--desc` (or both) must be provided
2. **Order independent**: Arguments can be provided in any order

## Error Handling

### Error Types and Responses

| Error Scenario              | Error Message                                                                          | Exit Code | Output Channel |
|-----------------------------|----------------------------------------------------------------------------------------|-----------|----------------|
| Task not found              | "Error: Task not found (ID: {id})"                                                    | 1         | stderr         |
| Invalid ID format           | "Error: Task ID must be a positive integer"                                           | 1         | stderr         |
| Negative/zero ID            | "Error: Task ID must be a positive integer"                                           | 1         | stderr         |
| Missing ID argument         | "Error: Missing required argument: task_id\nUsage: python main.py update <task_id> [--title <text>] [--desc <text>]" | 1 | stderr |
| No update args              | "Error: At least one of --title or --desc must be provided"                           | 1         | stderr         |
| Empty title                 | "Error: Title cannot be empty"                                                        | 1         | stderr         |
| Title too long              | "Error: Title must be between 1 and 100 characters (received {actual})"               | 1         | stderr         |
| Description too long        | "Error: Description cannot exceed 500 characters (received {actual})"                 | 1         | stderr         |

### Error Handling Principles

1. **Clear messages**: Errors clearly state what went wrong
2. **Specific values**: Include the problematic values when relevant
3. **Consistent format**: All errors start with "Error: " prefix
4. **Proper channels**: Errors to stderr, success messages to stdout
5. **Exit codes**: Exit code 0 for success, exit code 1 for all errors
6. **No partial update**: If validation fails, no task fields are modified
7. **Validation order**: Validate ID first, then existence, then field values

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
- Test invalid task ID (non-numeric string: "abc")
- Test invalid task ID (floating point string: "1.5")

**Test Suite: Title Validation for Update**
- Test valid title (1 character) - boundary
- Test valid title (50 characters) - middle
- Test valid title (100 characters) - boundary
- Test invalid title (empty string after trim)
- Test invalid title (whitespace only)
- Test invalid title (101 characters) - boundary
- Test title with Unicode characters

**Test Suite: Description Validation for Update**
- Test valid description (empty string - clears description)
- Test valid description (250 characters) - middle
- Test valid description (500 characters) - boundary
- Test invalid description (501 characters) - boundary
- Test description with Unicode characters

**Test Suite: TaskStorage Update Method**
- Test update title only preserves description
- Test update description only preserves title
- Test update both title and description
- Test update non-existent task returns None
- Test update from empty storage returns None
- Test update preserves completion status
- Test update preserves created_at timestamp
- Test update with empty description clears it
- Test update doesn't affect other tasks

#### 2. Integration Tests (CLI command workflow)

**Test Suite: Update Command Integration**
- Test `python main.py update 1 --title "New"` updates title only
- Test `python main.py update 1 --desc "New"` updates description only
- Test `python main.py update 1 --title "New" --desc "New"` updates both
- Test update returns success message with correct details
- Test update 999 returns "Task not found" error
- Test update with no --title or --desc returns error
- Test invalid ID format returns error and exit code 1
- Test empty title returns error
- Test oversized title returns error
- Test oversized description returns error
- Test error messages go to stderr
- Test success messages go to stdout
- Test update preserves completed status

#### 3. Edge Case Tests

**Test Suite: Boundary Conditions**
- Test update title exactly 1 character
- Test update title exactly 100 characters
- Test update title exactly 101 characters (should fail)
- Test update description exactly 500 characters
- Test update description exactly 501 characters (should fail)
- Test update with empty description clears it

**Test Suite: Special Characters**
- Test title with emoji: "Task updated"
- Test title with accents: "Cafe meeting"
- Test title with non-Latin scripts: "updated task"
- Test description with newlines
- Test description with special characters

**Test Suite: State Preservation**
- Test update incomplete task preserves status
- Test update complete task preserves status
- Test update doesn't modify ID
- Test update doesn't modify created_at
- Test update with identical values succeeds (idempotent)

### Test Organization Structure

```
tests/
├── unit/
│   ├── test_update_validation.py      # Update-specific validation tests
│   └── test_storage_update.py         # Storage update operation tests
├── integration/
│   ├── test_update_command.py         # Full CLI workflow tests
│   └── test_update_error_handling.py  # Error scenario integration tests
└── fixtures/
    └── sample_tasks.py                # Shared test data (reused from add-task)
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
def update(self, task_id: int, title: str | None = None, description: str | None = None) -> Task | None:
    """
    Update task by ID.

    Args:
        task_id: The ID of the task to update
        title: New title (if provided, replaces existing; must be validated before calling)
        description: New description (if provided, replaces existing; empty string clears it)

    Returns:
        Updated Task object if found, None if task not found

    Note:
        - At least one of title or description must be provided (enforced at CLI layer)
        - Status and created_at are never modified
        - Validation happens at CLI layer before calling this method
    """
    if task_id not in self._tasks:
        return None

    task = self._tasks[task_id]

    # Create updated task with new values or preserved existing values
    updated_task = Task(
        id=task.id,
        title=title.strip() if title is not None else task.title,
        description=description if description is not None else task.description,
        status=task.status,  # Preserved
        created_at=task.created_at  # Preserved
    )

    self._tasks[task_id] = updated_task
    return updated_task
```

**No changes to**:
- Task dataclass (update operates on existing structure)
- ID generation logic (update doesn't affect IDs)
- Existing add/get/exists/count/delete methods

## Dependencies and Constraints

### Dependencies (Per Constitution)

- **Python Standard Library Only**: argparse (existing dependency)
- **No External Runtime Dependencies**: No third-party packages
- **Testing Only**: pytest, pytest-cov (existing development dependencies)

### Constraints (Per Constitution)

- **In-Memory Only**: No file I/O, no database, updates only affect memory
- **Type Hints Mandatory**: All functions must have type annotations
- **Docstrings Required**: Google-style docstrings for all public APIs
- **TDD Required**: Tests written first, verified to fail, then implemented
- **80% Coverage**: Minimum test coverage threshold

## Out of Scope

The following are explicitly excluded from this feature:

- **Bulk update**: Updating multiple tasks at once
- **Update by title search**: Must use task ID, not title/description search
- **Status modification**: Changing completion status (separate feature: toggle-status)
- **ID modification**: Task IDs are immutable
- **Timestamp modification**: created_at is immutable; no updated_at field currently
- **Confirmation prompts**: No interactive dialogs
- **Undo/rollback**: No operation history
- **Field history**: No tracking of previous values
- **Partial field update** (e.g., append to description): Full field replacement only
- **Validation relaxation**: Same validation rules as add (no special leniency for updates)

## Assumptions

1. **Prerequisite**: Add Task feature (`001-add-task`) is fully implemented and working
2. **Storage implementation**: TaskStorage uses dict-based storage enabling O(1) lookup
3. **ID format**: Task IDs are always positive integers (guaranteed by add feature)
4. **Single update**: Users update one task at a time (no batch operations)
5. **Field replacement**: Updates replace entire field values, not partial modifications
6. **Validation consistency**: Same validation rules apply for update as for add (title 1-100 chars, desc max 500 chars)

## Next Steps

After spec approval:

1. **Run `/sp.clarify`** (if needed): Ask targeted questions to resolve any ambiguities
2. **Create implementation plan** (`/sp.plan`): Define technical changes to existing codebase, integration points
3. **Generate task breakdown** (`/sp.tasks`): Break into atomic, testable tasks with TDD workflow
4. **Write tests first** (Red phase): Implement all test cases, verify failures
5. **Implement feature** (Green phase): Add update method to storage, add CLI command handler
6. **Refactor** (Refactor phase): Improve code quality while maintaining passing tests
7. **Validate coverage**: Ensure >= 80% coverage with pytest-cov
8. **Manual testing**: Execute CLI commands to verify user experience
9. **Create PHR**: Document the implementation work
