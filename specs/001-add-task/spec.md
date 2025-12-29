# Feature Specification: Add Task

**Feature Branch**: `001-add-task`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Feature: Add Todo Task - User can add a new task with title and description"

## Clarifications

### Session 2025-12-28

- Q: Should task IDs be sequential integers or UUIDs? → A: Sequential integers (1, 2, 3...)
- Q: Should we truncate or reject titles exceeding 100 chars? → A: Reject with error message
- Q: Do we need timestamps (created_at, updated_at)? → A: Only created_at (naive datetime)
- Q: Should description support multi-line input? → A: Support via shell quoting
- Q: Exit codes for success/failure? → A: 0 for success, 1 for all errors

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Task with Title Only (Priority: P1)

As a user, I want to quickly add a task with just a title so that I can capture to-do items without needing to provide detailed descriptions.

**Why this priority**: This is the minimum viable feature for task creation. Users often need to quickly capture tasks and add details later. This represents the core value proposition of the add feature.

**Independent Test**: Can be fully tested by running the add command with only a title argument and verifying the task is created with auto-generated ID, incomplete status, and empty description.

**Acceptance Scenarios**:

1. **Given** the todo application is running, **When** I execute `todo add "Buy groceries"`, **Then** the system creates a new task with title "Buy groceries", auto-generated unique ID (e.g., 1), status "incomplete", empty description, and displays success message with task ID
2. **Given** the todo application is running, **When** I execute `todo add "Schedule dentist appointment"`, **Then** the system creates a new task with a different auto-generated ID (e.g., 2) and confirms creation
3. **Given** I have added 5 tasks, **When** I add a 6th task with title "Review PR", **Then** the system generates the next sequential ID (e.g., 6) and creates the task successfully

---

### User Story 2 - Add Task with Title and Description (Priority: P2)

As a user, I want to add a task with both a title and a detailed description so that I can capture comprehensive information about what needs to be done.

**Why this priority**: While title-only is MVP, descriptions add significant value by allowing users to capture context, requirements, or notes. This is the expected full-featured behavior.

**Independent Test**: Can be tested by running the add command with both title and description arguments, verifying both fields are stored and displayed correctly.

**Acceptance Scenarios**:

1. **Given** the todo application is running, **When** I execute `todo add "Buy groceries" --description "Get milk, eggs, bread from Whole Foods"`, **Then** the system creates a task with title "Buy groceries", description "Get milk, eggs, bread from Whole Foods", auto-generated ID, status "incomplete", and displays full task details
2. **Given** the todo application is running, **When** I execute `todo add "Fix bug #123" --description "Null pointer exception in user service when email is empty"`, **Then** the system creates the task with both fields populated and confirms creation with all details
3. **Given** I want to add multi-word descriptions, **When** I execute `todo add "Meeting" --description "Discuss Q1 roadmap, review budget, assign action items"`, **Then** the system correctly stores the entire description without truncation

---

### User Story 3 - Validation Feedback (Priority: P3)

As a user, I want to receive clear, actionable error messages when I provide invalid input so that I can correct my mistakes and successfully create tasks.

**Why this priority**: Good error handling improves user experience but is not blocking for the core functionality. Users can still add tasks successfully when input is valid.

**Independent Test**: Can be tested by providing various invalid inputs (empty title, too-long title, too-long description) and verifying appropriate error messages are displayed.

**Acceptance Scenarios**:

1. **Given** the todo application is running, **When** I execute `todo add ""` (empty title), **Then** the system returns an error "Error: Title is required and cannot be empty" and does not create a task
2. **Given** the todo application is running, **When** I execute `todo add` with a title exceeding 100 characters, **Then** the system returns an error "Error: Title must be between 1 and 100 characters" and does not create a task
3. **Given** the todo application is running, **When** I execute `todo add "Valid title" --description` with a description exceeding 500 characters, **Then** the system returns an error "Error: Description cannot exceed 500 characters" and does not create a task
4. **Given** I attempt to add a task with missing required argument, **When** I execute `todo add`, **Then** the system displays usage help showing correct command format

---

### Edge Cases

- **Empty title**: System rejects with error "Title is required and cannot be empty"
- **Title with only whitespace**: System treats as empty and rejects
- **Title exactly 100 characters**: System accepts (boundary condition - valid)
- **Title with 101 characters**: System rejects with length error
- **Description exactly 500 characters**: System accepts (boundary condition - valid)
- **Description with 501 characters**: System rejects with length error
- **Special characters in title/description**: System accepts all Unicode characters (e.g., "Café meeting", "Task №5", "Review 中文 docs")
- **Duplicate titles**: System allows (titles are not unique identifiers; IDs are)
- **Maximum integer ID overflow**: System uses standard Python integers (unbounded), so no overflow concern for in-memory implementation
- **Concurrent adds** (if multi-threaded): Out of scope for single-user CLI app; not addressed in current design
- **Title/description with newlines**: System preserves newlines as entered via shell quoting; user can use `\n` or actual newlines in quoted strings
- **Title/description with quotes**: System handles via argparse string parsing; user must escape or use proper shell quoting

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a title argument as the primary input for task creation
- **FR-002**: System MUST validate that title is not empty (after trimming whitespace)
- **FR-003**: System MUST enforce title length between 1 and 100 characters (inclusive); titles exceeding 100 characters MUST be rejected with error message (not truncated)
- **FR-004**: System MUST accept an optional `--description` flag with text argument
- **FR-005**: System MUST enforce description length maximum of 500 characters (if provided); multi-line descriptions supported via shell quoting (e.g., "Line1\nLine2")
- **FR-006**: System MUST auto-generate a unique integer ID for each new task
- **FR-007**: System MUST set task status to "incomplete" by default for new tasks
- **FR-008**: System MUST store the created task in memory (no persistence required)
- **FR-009**: System MUST return a success message displaying the created task's ID, title, description, and status
- **FR-010**: System MUST return clear error messages to stderr with non-zero exit code for validation failures
- **FR-011**: System MUST support Unicode characters in both title and description fields
- **FR-012**: System MUST allow duplicate titles (uniqueness enforced only by ID, not title)
- **FR-013**: System MUST use argparse for CLI argument parsing (per constitution)
- **FR-014**: System MUST NOT persist tasks to files, databases, or external storage (in-memory only per constitution)

### Key Entities

- **Task**: Represents a single to-do item with the following attributes:
  - `id` (integer): Unique identifier, auto-generated, sequential starting from 1 (confirmed: integers not UUIDs)
  - `title` (string): Required, 1-100 characters, describes the task
  - `description` (string): Optional, max 500 characters, provides additional context
  - `status` (string/enum): Either "complete" or "incomplete", defaults to "incomplete"
  - `created_at` (datetime): Timestamp when task was created, naive datetime (no timezone), for future sorting/filtering

- **TaskRepository/TaskStore**: In-memory collection managing all tasks
  - Stores tasks in a data structure (e.g., dictionary keyed by ID)
  - Provides ID generation mechanism (e.g., incrementing counter)
  - Ensures thread-safety if needed (not required for single-user CLI)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully add a task with only a title in under 5 seconds (command execution time)
- **SC-002**: User can successfully add a task with title and description in under 5 seconds
- **SC-003**: System correctly rejects 100% of invalid inputs (empty title, oversized fields) with clear error messages
- **SC-004**: System generates unique IDs for all tasks with zero collisions across any number of additions
- **SC-005**: All task additions maintain 80%+ test coverage (per constitution requirement)
- **SC-006**: CLI interface matches constitutional requirements (argparse, stdout/stderr, exit codes)

## CLI Interface Examples

### Command Format

```bash
todo add <title> [--description <text>]
```

### Successful Additions

**Example 1: Title only**
```bash
$ todo add "Buy groceries"
✓ Task created successfully
  ID: 1
  Title: Buy groceries
  Description: (none)
  Status: incomplete
```

**Example 2: Title with description**
```bash
$ todo add "Review PR #456" --description "Check for security vulnerabilities and test coverage"
✓ Task created successfully
  ID: 2
  Title: Review PR #456
  Description: Check for security vulnerabilities and test coverage
  Status: incomplete
```

**Example 3: Title with special characters**
```bash
$ todo add "Café meeting @ 3pm" --description "Discuss Q4 roadmap & budget 💼"
✓ Task created successfully
  ID: 3
  Title: Café meeting @ 3pm
  Description: Discuss Q4 roadmap & budget 💼
  Status: incomplete
```

**Example 4: Long title (100 chars)**
```bash
$ todo add "This is a very long task title that goes up to exactly one hundred characters for boundary test"
✓ Task created successfully
  ID: 4
  Title: This is a very long task title that goes up to exactly one hundred characters for boundary test
  Description: (none)
  Status: incomplete
```

### Validation Errors

**Example 1: Empty title**
```bash
$ todo add ""
Error: Title is required and cannot be empty
Usage: todo add <title> [--description <text>]
Exit code: 1
```

**Example 2: Title too long (101 chars)**
```bash
$ todo add "This is a very long task title that exceeds one hundred characters and should trigger validation"
Error: Title must be between 1 and 100 characters (received 101)
Exit code: 1
```

**Example 3: Description too long (501 chars)**
```bash
$ todo add "Valid title" --description "Lorem ipsum dolor sit amet, consectetur adipiscing elit... [501 characters total]"
Error: Description cannot exceed 500 characters (received 501)
Exit code: 1
```

**Example 4: Missing title argument**
```bash
$ todo add
Error: Missing required argument: title
Usage: todo add <title> [--description <text>]
Exit code: 1
```

**Example 5: Whitespace-only title**
```bash
$ todo add "   "
Error: Title is required and cannot be empty
Exit code: 1
```

## Input Validation Rules

### Title Validation

1. **Required**: Title argument must be provided
2. **Non-empty**: After stripping leading/trailing whitespace, title must have at least 1 character
3. **Length**: Title must be between 1 and 100 characters (inclusive) after trimming whitespace
4. **Character set**: All Unicode characters allowed (no restrictions)
5. **Processing**: Trim leading/trailing whitespace before validation and storage

**Validation Logic**:
```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Validates task title according to requirements.

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str)
        error_message is empty string if valid
    """
    if not title:
        return False, "Title is required and cannot be empty"

    trimmed = title.strip()
    if not trimmed:
        return False, "Title is required and cannot be empty"

    if len(trimmed) > 100:
        return False, f"Title must be between 1 and 100 characters (received {len(trimmed)})"

    return True, ""
```

### Description Validation

1. **Optional**: Description is not required; can be omitted entirely
2. **Length**: If provided, description cannot exceed 500 characters
3. **Empty allowed**: Empty string is valid for description
4. **Character set**: All Unicode characters allowed (no restrictions)
5. **Multi-line support**: Newlines preserved via shell quoting (e.g., `--description "Line 1\nLine 2"`)
6. **Processing**: No trimming; preserve exact input including leading/trailing whitespace and newlines

**Validation Logic**:
```python
def validate_description(description: str | None) -> tuple[bool, str]:
    """
    Validates task description according to requirements.

    Args:
        description: The description string to validate, or None if not provided

    Returns:
        Tuple of (is_valid: bool, error_message: str)
        error_message is empty string if valid
    """
    if description is None:
        return True, ""  # Optional field

    if len(description) > 500:
        return False, f"Description cannot exceed 500 characters (received {len(description)})"

    return True, ""
```

### ID Generation

1. **Automatic**: System generates IDs; user never provides ID for new tasks
2. **Uniqueness**: Each task must have a unique integer ID
3. **Sequential**: IDs start at 1 and increment by 1 for each new task
4. **Immutable**: Once assigned, a task's ID never changes
5. **No reuse**: Deleted task IDs are not reused (maintain monotonic sequence)

**ID Generation Logic**:
```python
class TaskIDGenerator:
    """Generates unique, sequential task IDs."""

    def __init__(self):
        self._next_id: int = 1

    def generate(self) -> int:
        """Generate next unique ID."""
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

## Error Handling

### Error Types and Responses

| Error Scenario | Error Message | Exit Code | Output Channel |
|---------------|---------------|-----------|----------------|
| Empty title | "Error: Title is required and cannot be empty" | 1 | stderr |
| Title too long | "Error: Title must be between 1 and 100 characters (received {actual})" | 1 | stderr |
| Description too long | "Error: Description cannot exceed 500 characters (received {actual})" | 1 | stderr |
| Missing title argument | "Error: Missing required argument: title\nUsage: todo add <title> [--description <text>]" | 1 | stderr |
| Invalid flag/option | "Error: Unrecognized option: {flag}\nUsage: todo add <title> [--description <text>]" | 1 | stderr |

### Error Handling Principles

1. **Clear messages**: Errors must clearly state what went wrong and what was expected
2. **Actionable**: Include guidance on how to fix the error (e.g., usage examples)
3. **Specific values**: Include actual values received when relevant (e.g., "received 101 characters")
4. **Consistent format**: All errors start with "Error: " prefix
5. **Proper channels**: Errors to stderr, success messages to stdout
6. **Exit codes**: Exit code 0 for success, exit code 1 for all errors (simple two-state model per CLI best practices)
7. **No partial creation**: If validation fails, no task is created or stored
8. **No exceptions to user**: Catch all exceptions internally; display user-friendly messages

## Testing Requirements

### Test Coverage Mandate

Per constitution requirement: Minimum 80% test coverage for all code

### Test Categories

#### 1. Unit Tests (models, validation, ID generation)

**Test Suite: Task Model**
- Test task initialization with all fields
- Test task initialization with required fields only
- Test task default status is "incomplete"
- Test task attribute access and immutability (if applicable)

**Test Suite: Title Validation**
- Test valid title (1 character) - boundary
- Test valid title (50 characters) - middle
- Test valid title (100 characters) - boundary
- Test invalid title (empty string)
- Test invalid title (whitespace only: "   ")
- Test invalid title (101 characters) - boundary
- Test title with Unicode characters
- Test title trimming behavior

**Test Suite: Description Validation**
- Test valid description (None/not provided)
- Test valid description (empty string)
- Test valid description (250 characters) - middle
- Test valid description (500 characters) - boundary
- Test invalid description (501 characters) - boundary
- Test description with Unicode characters
- Test description preserves whitespace

**Test Suite: ID Generation**
- Test first ID is 1
- Test IDs increment sequentially
- Test 1000 sequential IDs for uniqueness
- Test ID generator is independent across instances (if applicable)

#### 2. Integration Tests (CLI command workflow)

**Test Suite: Add Command Integration**
- Test `todo add "Task"` creates task with ID 1
- Test `todo add "Task" --description "Desc"` creates task with both fields
- Test adding multiple tasks generates sequential IDs (1, 2, 3)
- Test adding task returns success message with correct details
- Test adding task with duplicate title succeeds (uniqueness not enforced)
- Test empty title returns error and exit code 1
- Test oversized title returns error and exit code 1
- Test oversized description returns error and exit code 1
- Test error messages go to stderr
- Test success messages go to stdout

#### 3. Edge Case Tests

**Test Suite: Boundary Conditions**
- Test title exactly 1 character
- Test title exactly 100 characters
- Test title exactly 101 characters (should fail)
- Test description exactly 500 characters
- Test description exactly 501 characters (should fail)

**Test Suite: Special Characters**
- Test title with emoji: "Task 🎉"
- Test title with accents: "Café meeting"
- Test title with symbols: "Review PR #123 @ 3pm"
- Test title with non-Latin scripts: "任务列表"
- Test description with newlines: "Line 1\nLine 2"
- Test description with tabs: "Item\tValue"

**Test Suite: Error Scenarios**
- Test missing title argument
- Test invalid command-line flag
- Test whitespace-only title
- Test None/null title (if applicable from API usage)

### Test Organization Structure

```
tests/
├── unit/
│   ├── test_task_model.py          # Task entity tests
│   ├── test_validators.py          # Title/description validation tests
│   └── test_id_generator.py        # ID generation tests
├── integration/
│   ├── test_add_command.py         # Full CLI workflow tests
│   └── test_error_handling.py      # Error scenario integration tests
└── fixtures/
    └── sample_tasks.py              # Shared test data
```

### Test Execution Requirements

1. **Pre-implementation**: Tests MUST be written before implementation (TDD)
2. **Failure verification**: Tests MUST fail initially (Red phase)
3. **Minimum coverage**: 80% coverage required to pass (pytest-cov)
4. **CI validation**: All tests must pass before merge
5. **Isolation**: Each test is independent; no shared state between tests
6. **Fast execution**: Full test suite should complete in under 10 seconds

## Data Model

### Task Entity

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """
    Represents a single to-do item.

    Attributes:
        id: Unique integer identifier (auto-generated)
        title: Task title (1-100 characters, required)
        description: Task description (max 500 characters, optional)
        status: Completion status ("complete" or "incomplete")
        created_at: Timestamp when task was created (naive datetime)
    """
    id: int
    title: str
    description: Optional[str]
    status: str  # "complete" or "incomplete"
    created_at: datetime

    def __post_init__(self):
        """Validate task attributes after initialization."""
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Task title is required and cannot be empty")

        if len(self.title) > 100:
            raise ValueError(f"Task title cannot exceed 100 characters (got {len(self.title)})")

        if self.description is not None and len(self.description) > 500:
            raise ValueError(f"Task description cannot exceed 500 characters (got {len(self.description)})")

        if self.status not in ("complete", "incomplete"):
            raise ValueError(f"Task status must be 'complete' or 'incomplete' (got '{self.status}')")
```

### TaskRepository (In-Memory Store)

```python
from typing import Dict, Optional

class TaskRepository:
    """
    In-memory repository for managing tasks.

    Stores tasks in a dictionary keyed by task ID.
    Provides CRUD operations and ID generation.
    """

    def __init__(self):
        """Initialize empty task repository."""
        self._tasks: Dict[int, Task] = {}
        self._id_generator = TaskIDGenerator()

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create and store a new task.

        Args:
            title: Task title (validated externally)
            description: Optional task description (validated externally)

        Returns:
            The created Task object with auto-generated ID
        """
        task_id = self._id_generator.generate()
        now = datetime.now()

        task = Task(
            id=task_id,
            title=title.strip(),  # Trim whitespace
            description=description,
            status="incomplete",
            created_at=now
        )

        self._tasks[task_id] = task
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID."""
        return self._tasks.get(task_id)

    def exists(self, task_id: int) -> bool:
        """Check if task with given ID exists."""
        return task_id in self._tasks

    def count(self) -> int:
        """Return total number of tasks."""
        return len(self._tasks)
```

### Design Considerations

1. **Immutability**: Consider making Task a frozen dataclass for immutability (prevents accidental modification)
2. **Type safety**: Use type hints throughout (per constitution requirement)
3. **Validation**: Validation happens at CLI layer before reaching repository (separation of concerns)
4. **Timestamps**: Include created_at only (naive datetime) for future sorting/filtering; updated_at not needed until edit feature exists (YAGNI principle)
5. **Status enum**: Consider using Python Enum for status instead of string literals (type safety)
6. **Thread safety**: Not required for single-user CLI; omit locks/synchronization for simplicity

## Dependencies and Constraints

### Dependencies (Per Constitution)

- **Python Standard Library Only**: argparse, dataclasses, datetime, typing
- **No External Runtime Dependencies**: No third-party packages allowed
- **Testing Only**: pytest, pytest-cov (development dependencies)

### Constraints (Per Constitution)

- **In-Memory Only**: No file I/O, no database, no persistence
- **Type Hints Mandatory**: All functions and classes must have type annotations
- **Docstrings Required**: Google-style docstrings for all public APIs
- **SOLID Principles**: Single responsibility, clear separation of concerns
- **TDD Required**: Tests written first, verified to fail, then implemented
- **80% Coverage**: Minimum test coverage threshold

## Out of Scope

The following are explicitly excluded from this feature:

- **Persistence**: Tasks are not saved to disk; lost when application exits
- **Task editing**: Updating existing tasks (separate feature: update-task)
- **Task deletion**: Removing tasks (separate feature: delete-task)
- **Task listing**: Viewing all tasks (separate feature: list-tasks)
- **Status toggling**: Marking tasks complete/incomplete (separate feature: toggle-status)
- **Task sorting**: Ordering tasks by any criteria
- **Task filtering**: Finding tasks by attributes
- **Interactive mode**: Prompting user for inputs (CLI arguments only)
- **Configuration**: No config files, environment variables, or customization
- **Logging**: No file-based logging (stdout/stderr only per constitution)
- **Concurrency**: No multi-threading or async support
- **Authentication**: No user accounts or access control
- **Undo/redo**: No operation history or rollback

## Next Steps

After spec approval:

1. **Create implementation plan** (`/sp.plan`): Define technical architecture, file structure, class design
2. **Generate task breakdown** (`/sp.tasks`): Break into atomic, testable tasks with TDD workflow
3. **Write tests first** (Red phase): Implement all test cases, verify failures
4. **Implement feature** (Green phase): Write minimum code to pass tests
5. **Refactor** (Refactor phase): Improve code quality while maintaining passing tests
6. **Validate coverage**: Ensure ≥80% coverage with pytest-cov
7. **Manual testing**: Execute CLI commands to verify user experience
8. **Create PHR**: Document the implementation work

## Questions for User

1. **Timestamp granularity**: Should `created_at`/`updated_at` use timezone-aware datetime or naive datetime?
2. **Success message format**: Is the proposed multi-line format acceptable, or prefer single-line?
3. **ID starting value**: Confirm IDs should start at 1 (not 0)?
4. **Whitespace handling**: Confirm title should be trimmed but description preserved as-is?
5. **Unicode support**: Confirm all Unicode characters should be supported (no ASCII-only restriction)?
