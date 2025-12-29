# Implementation Plan: Delete Task

**Branch**: `002-delete-task` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-delete-task/spec.md`

## Summary

Implement delete task functionality that removes a task from in-memory storage by its ID. The feature extends the existing TaskStorage class with a delete method and adds a new 'delete' CLI subcommand. Implementation follows the established patterns from the add-task feature, maintaining consistency in validation, error handling, and output formatting.

**Primary Requirement**: User can delete a task by providing its ID via CLI command `todo delete <task_id>`

**Technical Approach**:
- Extend TaskStorage with `delete(task_id: int) -> bool` method
- Add task ID validation function mirroring title/description validators
- Add delete subcommand to argparse CLI
- Implement delete command handler following add command pattern
- No changes to Task model or ID generation logic required

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (argparse, dataclasses, datetime, typing)
**Storage**: In-memory list-based TaskStorage (existing from add-task feature)
**Testing**: pytest + pytest-cov (minimum 80% coverage)
**Target Platform**: CLI application (cross-platform via Python)
**Project Type**: Single-file CLI application
**Performance Goals**: Delete operation completes in <2 seconds (per success criteria SC-001)
**Constraints**:
- No external runtime dependencies
- In-memory only (no persistence)
- Must maintain ID sequence integrity (deleted IDs not reused)
**Scale/Scope**: Small feature - 3 new functions, 1 new method, ~100 LOC total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Required Gates (from constitution.md)

- ✅ **Python 3.13+ with Type Hints**: All new code will use type hints (int, bool, str | None)
- ✅ **In-Memory Storage Only**: Delete operates on existing in-memory list, no persistence
- ✅ **UV Package Manager Only**: No new dependencies; uses existing UV environment
- ✅ **Test-Driven Development**: Tests will be written first (Red-Green-Refactor cycle)
- ✅ **Test Coverage Minimum 80%**: Feature designed for high testability; ~30 test cases planned
- ✅ **Zero External Runtime Dependencies**: Uses only argparse (standard library)
- ✅ **Clean Code and SOLID Principles**:
  - Single Responsibility: delete method does one thing
  - Open/Closed: Extends TaskStorage without modifying existing methods
  - Separation of concerns: validation, storage, CLI handling separated
- ✅ **Documentation Standards**: All functions will have Google-style docstrings

### Constitutional Compliance

**Passes All Gates**: Yes

**Justification**:
- Leverages existing architecture from add-task feature
- No new external dependencies
- Minimal code changes (extends existing classes)
- High test coverage achievable with clear validation boundaries
- Follows established patterns for consistency

## Project Structure

### Documentation (this feature)

```text
specs/002-delete-task/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (minimal - patterns established)
├── data-model.md        # Phase 1 output (storage method addition)
├── quickstart.md        # Phase 1 output (usage examples)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Files to Modify**:
```text
src/
├── storage.py           # Add delete() method to TaskStorage class
├── cli.py               # Add delete subcommand parser and handle_delete_command()
└── validators.py        # Add validate_task_id() function
```

**Files to Create**:
```text
tests/
├── unit/
│   ├── test_task_id_validation.py    # NEW: Task ID validation tests
│   └── test_storage_delete.py         # NEW: Storage delete operation tests
└── integration/
    └── test_delete_command.py         # NEW: CLI delete command integration tests
```

**Files Unchanged**:
```text
src/
├── models.py            # No changes - Task model unchanged
└── main.py              # No changes - routing handled by argparse
```

## Architecture & Design Decisions

### ADR-004: Delete Operation Strategy

**Decision**: Use list-based linear search for deletion

**Context**:
- Existing TaskStorage uses `list[Task]` for storage (not dict)
- Current implementation uses linear search in `get()` method (O(n))
- Spec allows for O(n) deletion ("acceptable for CLI scale" per assumptions)
- Feature must integrate with existing architecture

**Options Considered**:

1. **Linear search through list** (CHOSEN)
   - **Pros**: Consistent with existing get() method, simple, no data structure changes
   - **Cons**: O(n) deletion time
   - **Performance**: Acceptable for CLI use case (<1000 tasks typical)

2. **Add dict index (id → Task)**
   - **Pros**: O(1) deletion, faster lookups
   - **Cons**: Requires refactoring existing storage, adds complexity, maintains dual data structures
   - **Rejected**: Over-engineering for current scale; breaks existing patterns

3. **Convert storage to dict-only**
   - **Pros**: O(1) operations, cleaner design
   - **Cons**: Requires refactoring add-task feature, risks regression
   - **Rejected**: Out of scope for this feature; could be future optimization

**Rationale**:
- Consistency with existing codebase trumps theoretical performance gains
- CLI applications typically handle small datasets (<1000 tasks)
- O(n) search acceptable for human-interactive commands
- Avoids premature optimization
- Can be optimized later without API changes if needed

**Consequences**:
- Delete performance: O(n) where n = number of tasks
- Simple implementation: 5-10 lines of code
- Easy to test and maintain
- No changes to existing storage interface

---

### ADR-005: Task ID Validation Strategy

**Decision**: Create dedicated `validate_task_id()` function following existing validator pattern

**Context**:
- Existing validators: `validate_title()` and `validate_description()` return `tuple[bool, str]`
- Task IDs must be positive integers (≥ 1)
- argparse receives string arguments that must be parsed and validated
- Validation must happen before storage lookup

**Options Considered**:

1. **Dedicated validator function** (CHOSEN)
   - **Pattern**: `validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]`
   - **Pros**: Consistent with existing validators, testable in isolation, reusable
   - **Cons**: Returns 3-tuple vs 2-tuple (includes parsed int)
   - **Rationale**: Need to return parsed int to avoid double-parsing; 3-tuple acceptable

2. **Inline validation in command handler**
   - **Pros**: One less function, co-located with usage
   - **Cons**: Not reusable, harder to test, violates separation of concerns
   - **Rejected**: Breaks established pattern, reduces testability

3. **argparse type parameter**
   - **Pattern**: `add_argument('task_id', type=int)`
   - **Pros**: argparse handles parsing automatically
   - **Cons**: Error messages less user-friendly, can't enforce ≥1 constraint, inconsistent with other validators
   - **Rejected**: argparse type errors are less clear than custom validation messages

**Implementation**:
```python
def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """
    Validates task ID according to requirements.

    Args:
        task_id_str: The task ID string from command line

    Returns:
        Tuple of (is_valid: bool, error_message: str, parsed_id: int | None)
    """
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a positive integer", None

    if task_id < 1:
        return False, "Task ID must be a positive integer", None

    return True, "", task_id
```

**Consequences**:
- Consistent validation pattern across codebase
- Clear, user-friendly error messages
- Highly testable (9 unit tests planned)
- Returns parsed int to avoid double-parsing overhead

---

### ADR-006: Delete Command Handler Design

**Decision**: Implement `handle_delete_command()` following the `handle_add_command()` pattern

**Context**:
- Existing `handle_add_command()` establishes command handler pattern
- Handlers receive `args: argparse.Namespace` and `storage: TaskStorage`
- Handlers return int exit code (0 success, 1 error)
- Validation → Storage operation → Format output → Return exit code

**Pattern Established by add-task**:
```python
def handle_add_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    # 1. Validate inputs
    # 2. Perform storage operation
    # 3. Format success/error message
    # 4. Print to stdout/stderr
    # 5. Return exit code
```

**Delete Command Handler Flow**:
```python
def handle_delete_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    # 1. Validate task ID format
    is_valid, error_msg, task_id = validate_task_id(args.task_id)
    if not is_valid:
        print(format_error_message(error_msg), file=sys.stderr)
        return 1

    # 2. Attempt deletion
    was_deleted = storage.delete(task_id)

    # 3. Format and print appropriate message
    if was_deleted:
        print(f"Task deleted successfully (ID: {task_id})")
        return 0
    else:
        print(f"Error: Task not found (ID: {task_id})", file=sys.stderr)
        return 1
```

**Consistency Points**:
- Uses `format_error_message()` helper (reused from add command)
- Prints to stdout for success, stderr for errors
- Returns 0/1 exit codes
- Clear separation: validation → operation → output

**Consequences**:
- Predictable code structure for future commands
- Easy to test (can mock storage, capture stdout/stderr)
- Consistent user experience across commands

---

### ADR-007: Delete Method Return Value

**Decision**: `delete()` returns `bool` indicating success/failure

**Context**:
- Caller (CLI handler) needs to know if task was found and deleted
- Two outcomes: task deleted (success) or task not found (error)
- Python convention: boolean return for success/failure operations

**Options Considered**:

1. **Return bool** (CHOSEN)
   - **Pattern**: `def delete(self, task_id: int) -> bool:`
   - **True**: Task was found and deleted
   - **False**: Task not found (no deletion occurred)
   - **Pros**: Simple, clear semantics, Python convention, easy to test
   - **Cons**: Doesn't provide details about what failed

2. **Return deleted Task | None**
   - **Pattern**: `def delete(self, task_id: int) -> Task | None:`
   - **Pros**: Can show deleted task details to user
   - **Cons**: Spec says only show ID in success message (clarification Q2), unnecessary complexity

3. **Raise exception on not found**
   - **Pattern**: `def delete(self, task_id: int) -> None:` (raises TaskNotFoundError)
   - **Pros**: Forces error handling
   - **Cons**: Exceptions for expected cases is anti-pattern, adds exception class, less Pythonic for "not found"

**Rationale**:
- Boolean return is simplest and sufficient for requirements
- Spec requires showing only ID in success message (no need for Task object)
- "Not found" is expected case, not exceptional (don't use exceptions)
- Consistent with Python's dict.pop() returning success/failure semantics

**Implementation**:
```python
def delete(self, task_id: int) -> bool:
    """
    Delete task by ID.

    Args:
        task_id: The ID of the task to delete

    Returns:
        True if task was deleted, False if task not found
    """
    for i, task in enumerate(self._tasks):
        if task.id == task_id:
            del self._tasks[i]
            return True
    return False
```

**Consequences**:
- Simple to use: `if storage.delete(id):`
- Easy to test: assert return value
- No new exception types needed
- Idiomatic Python

## Component Design

### Modified: `src/storage.py`

**Change Type**: Add method to existing class

**New Method**:
```python
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
```

**Design Notes**:
- Uses enumerate() to find task and get index for deletion
- Linear search consistent with existing get() method
- Returns immediately after deletion (no need to continue loop)
- Does NOT modify `_next_id` (deleted IDs are retired, not reused per FR-010)

**Integration Points**:
- Called by `handle_delete_command()` in cli.py
- No changes to existing methods (add, get, exists, count, list_all)
- No changes to `__init__()` or class attributes

**Testing Strategy**:
- Unit tests in `tests/unit/test_storage_delete.py` (8 tests)
- Test both return values (True/False)
- Test storage state after deletion (count, get)
- Test ID sequence integrity after deletion

---

### Modified: `src/validators.py`

**Change Type**: Add new validation function

**New Function**:
```python
def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    """
    Validate task ID according to requirements.

    Task IDs must be positive integers (≥ 1). This function parses the string
    representation and validates the constraints.

    Args:
        task_id_str: The task ID string from command line

    Returns:
        Tuple of (is_valid: bool, error_message: str, parsed_id: int | None)
        - is_valid: True if validation passed, False otherwise
        - error_message: Empty string if valid, error description if invalid
        - parsed_id: The integer ID if valid, None if invalid

    Examples:
        >>> validate_task_id("5")
        (True, "", 5)
        >>> validate_task_id("0")
        (False, "Task ID must be a positive integer", None)
        >>> validate_task_id("abc")
        (False, "Task ID must be a positive integer", None)
    """
    try:
        task_id = int(task_id_str)
    except ValueError:
        return False, "Task ID must be a positive integer", None

    if task_id < 1:
        return False, "Task ID must be a positive integer", None

    return True, "", task_id
```

**Design Notes**:
- Returns 3-tuple vs 2-tuple of existing validators (includes parsed int)
- Combines parsing and validation in one function
- Consistent error message for all invalid cases (non-numeric, zero, negative)
- No trimming/whitespace handling (argparse handles this)

**Module Constants** (unchanged):
```python
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
# No new constants needed for task ID validation
```

**Testing Strategy**:
- Unit tests in `tests/unit/test_task_id_validation.py` (9 tests)
- Test valid IDs: 1, 100 (boundary and typical)
- Test invalid IDs: 0, -1, "abc", "1.5", "", "   "

---

### Modified: `src/cli.py`

**Change Type**: Add subcommand and command handler

**New Subcommand Registration** (in `create_parser()`):
```python
def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo", description="Simple CLI todo application"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command (existing)
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title (1-100 characters)")
    add_parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Task description (max 500 characters, optional)",
    )

    # Delete command (NEW)
    delete_parser = subparsers.add_parser("delete", help="Delete a task by ID")
    delete_parser.add_argument(
        "task_id",
        type=str,  # String to allow custom validation error messages
        help="Task ID to delete (positive integer)",
    )

    return parser
```

**New Command Handler**:
```python
def handle_delete_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle the delete command.

    Validates the task ID, attempts deletion, and prints appropriate
    success or error messages.

    Args:
        args: Parsed command-line arguments with task_id attribute
        storage: TaskStorage instance to delete from

    Returns:
        Exit code: 0 for success, 1 for error

    Examples:
        >>> from argparse import Namespace
        >>> storage = TaskStorage()
        >>> task = storage.add("Test task")
        >>> args = Namespace(task_id="1")
        >>> handle_delete_command(args, storage)
        Task deleted successfully (ID: 1)
        0
    """
    # Import validator
    from src.validators import validate_task_id

    # Validate task ID format
    is_valid, error_msg, task_id = validate_task_id(args.task_id)
    if not is_valid:
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1

    # Attempt deletion
    was_deleted = storage.delete(task_id)

    # Format and print appropriate message
    if was_deleted:
        success_msg = f"Task deleted successfully (ID: {task_id})"
        print(success_msg)
        return 0
    else:
        error_msg = f"Task not found (ID: {task_id})"
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1
```

**Modified Routing** (in `main.py` - no actual changes needed, handled by argparse):
```python
# main.py already routes dynamically:
# if args.command == "add":
#     return handle_add_command(args, storage)

# Will need to add:
# elif args.command == "delete":
#     return handle_delete_command(args, storage)
```

**Helper Functions** (reused, no changes):
- `format_error_message(error: str) -> str`: Adds "Error: " prefix
- Used by both add and delete commands for consistency

**Testing Strategy**:
- Integration tests in `tests/integration/test_delete_command.py` (12 tests)
- Test successful deletion with ID
- Test non-existent ID error
- Test invalid ID format errors
- Test stdout/stderr routing
- Test exit codes

---

### Modified: `src/main.py`

**Change Type**: Add routing for delete command

**New Routing Code**:
```python
def main() -> int:
    """Main entry point for the todo application."""
    # UTF-8 encoding setup (existing)
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding != "utf-8" and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    # Create storage instance
    storage = TaskStorage()

    # Create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Route to command handler
    if args.command == "add":
        return handle_add_command(args, storage)
    elif args.command == "delete":  # NEW
        return handle_delete_command(args, storage)

    # Unknown command (should not reach here due to argparse validation)
    return 1
```

**Design Notes**:
- Simple elif addition to existing routing
- Consistent pattern with add command
- No other changes to main.py needed

## Implementation Approach

### Phase 1: Storage Layer (Red-Green-Refactor)

**RED - Write Failing Tests First**:
1. Create `tests/unit/test_storage_delete.py`
2. Write 8 unit tests for `TaskStorage.delete()`:
   - `test_delete_existing_task_returns_true()`
   - `test_delete_non_existent_task_returns_false()`
   - `test_delete_from_empty_storage_returns_false()`
   - `test_delete_removes_task_from_storage()`
   - `test_delete_doesnt_affect_other_tasks()`
   - `test_delete_multiple_tasks_in_sequence()`
   - `test_storage_count_decreases_after_delete()`
   - `test_storage_count_unchanged_after_failed_delete()`
3. Run tests → verify ALL FAIL (pytest output shows failures)

**GREEN - Implement Minimum Code**:
1. Add `delete()` method to `TaskStorage` class in `src/storage.py`
2. Run tests → verify ALL PASS
3. Verify coverage for storage.py remains high

**REFACTOR - Improve Code**:
1. Check for code duplication (none expected)
2. Verify docstring completeness
3. Run mypy, ruff, black for code quality
4. Ensure function is concise (<20 lines as per constitution)

---

### Phase 2: Validation Layer (Red-Green-Refactor)

**RED - Write Failing Tests First**:
1. Create `tests/unit/test_task_id_validation.py`
2. Write 9 unit tests for `validate_task_id()`:
   - `test_valid_task_id_1()` - boundary
   - `test_valid_task_id_100()` - typical
   - `test_invalid_task_id_0()` - boundary
   - `test_invalid_task_id_negative_1()`
   - `test_invalid_task_id_negative_100()`
   - `test_invalid_task_id_non_numeric()`
   - `test_invalid_task_id_float()`
   - `test_invalid_task_id_empty_string()`
   - `test_invalid_task_id_whitespace()`
3. Run tests → verify ALL FAIL

**GREEN - Implement Minimum Code**:
1. Add `validate_task_id()` function to `src/validators.py`
2. Run tests → verify ALL PASS
3. Verify coverage for validators.py remains 100%

**REFACTOR - Improve Code**:
1. Check consistency with `validate_title()` and `validate_description()`
2. Verify error messages match spec requirements
3. Run code quality tools

---

### Phase 3: CLI Layer (Red-Green-Refactor)

**RED - Write Failing Tests First**:
1. Create `tests/integration/test_delete_command.py`
2. Write 12 integration tests for delete command:
   - `test_delete_command_success()`
   - `test_delete_command_success_message_format()`
   - `test_delete_command_non_existent_task_error()`
   - `test_delete_from_empty_list_error()`
   - `test_delete_already_deleted_task_error()` (idempotent)
   - `test_delete_middle_task_leaves_others()` (delete 2, verify 1 and 3)
   - `test_delete_invalid_id_format_error()`
   - `test_delete_negative_id_error()`
   - `test_delete_zero_id_error()`
   - `test_delete_missing_id_argument()`
   - `test_delete_error_messages_go_to_stderr()`
   - `test_delete_success_messages_go_to_stdout()`
3. Run tests → verify ALL FAIL

**GREEN - Implement Minimum Code**:
1. Add delete subparser to `create_parser()` in `src/cli.py`
2. Implement `handle_delete_command()` in `src/cli.py`
3. Add routing to `main()` in `src/main.py`
4. Run tests → verify ALL PASS

**REFACTOR - Improve Code**:
1. Check for code duplication with `handle_add_command()`
2. Consider extracting common patterns to helpers if needed
3. Verify error message formatting consistency
4. Run code quality tools

---

### Phase 4: Integration Testing & ID Sequence Verification

**Additional Tests**:
1. Add test in `test_storage_delete.py`:
   - `test_deleting_task_doesnt_affect_id_sequence_for_future_additions()`
   - Verify: add task 1, 2, 3 → delete 2 → add task 4 → task 4 has ID 4 (not 2)

2. Add test in `test_delete_command.py`:
   - `test_delete_all_tasks_leaves_storage_empty()`
   - `test_adding_task_after_deletion_uses_next_sequential_id()`

**Manual Verification**:
1. Run `uv run python -m src.main add "Task 1"`
2. Run `uv run python -m src.main add "Task 2"`
3. Run `uv run python -m src.main add "Task 3"`
4. Run `uv run python -m src.main delete 2`
5. Run `uv run python -m src.main add "Task 4"`
6. Verify: Task 4 should have ID 4 (not reusing 2)

---

### Phase 5: Polish & Quality Checks

**Code Quality**:
1. Run `uv run mypy src/` → verify no errors
2. Run `uv run ruff check src/ tests/` → verify no violations
3. Run `uv run black src/ tests/` → verify formatting

**Test Coverage**:
1. Run `uv run pytest --cov=src --cov-report=term` → verify ≥80% overall
2. Check coverage for new/modified files:
   - `src/storage.py`: Should remain ~100%
   - `src/validators.py`: Should remain 100%
   - `src/cli.py`: Should be ≥95%

**Documentation**:
1. Verify all new functions have complete Google-style docstrings
2. Verify docstrings include Args, Returns, Examples
3. Update README.md with delete command examples (if README exists)

**Final Verification**:
1. Run full test suite: `uv run pytest -v`
2. Verify all 53 existing tests still pass (no regressions)
3. Verify 29 new tests pass (9 + 8 + 12)
4. Total: 82 tests passing

## Testing Strategy

### Test Organization

```text
tests/
├── unit/
│   ├── test_task_id_validation.py    # NEW: 9 tests
│   └── test_storage_delete.py         # NEW: 8 tests
└── integration/
    └── test_delete_command.py         # NEW: 12 tests
```

**Total New Tests**: 29 tests
**Existing Tests**: 53 tests (from add-task feature)
**Total After Implementation**: 82 tests

### Test Coverage Goals

| File | Existing Coverage | Target Coverage | Test Count |
|------|-------------------|-----------------|------------|
| src/storage.py | ~100% | 100% | +8 tests |
| src/validators.py | 100% | 100% | +9 tests |
| src/cli.py | ~96% | ≥95% | +12 tests |
| src/main.py | 0% | 0% | N/A (entry point) |
| **Overall** | 83.65% | ≥85% | +29 tests |

### Test Categories

**Unit Tests - Storage Layer** (8 tests):
- Test delete returns True for existing task
- Test delete returns False for non-existent task
- Test delete from empty storage
- Test task is actually removed from storage
- Test other tasks unaffected by deletion
- Test multiple deletions in sequence
- Test count decreases after successful delete
- Test count unchanged after failed delete

**Unit Tests - Validation Layer** (9 tests):
- Test valid IDs: 1, 100
- Test invalid IDs: 0, -1, -100
- Test non-numeric: "abc", "task1"
- Test floating point: "1.5"
- Test empty/whitespace: "", "   "

**Integration Tests - CLI Layer** (12 tests):
- Test successful deletion (happy path)
- Test success message format matches spec
- Test non-existent task error
- Test empty storage error
- Test idempotent deletion (delete same task twice)
- Test deleting middle task (1,2,3 → delete 2 → 1,3 remain)
- Test invalid ID format errors (abc, -5, 0)
- Test missing ID argument
- Test stdout routing for success
- Test stderr routing for errors
- Test exit codes (0 for success, 1 for errors)

### Test Data & Fixtures

**Reuse Existing Fixtures**:
- `tests/fixtures/sample_tasks.py` (if exists from add-task)
- TaskStorage instance creation
- Sample task data

**New Test Utilities** (if needed):
- Helper to create pre-populated storage
- Helper to capture stdout/stderr

## Risk Assessment

### Low Risk Areas
- ✅ Storage implementation (follows established pattern)
- ✅ Validation (similar to existing validators)
- ✅ CLI integration (extends existing argparse setup)
- ✅ Test coverage (high testability, clear boundaries)

### Medium Risk Areas
- ⚠️ **ID sequence integrity**: Must verify deleted IDs are NOT reused
  - **Mitigation**: Explicit test for ID sequence after deletion
  - **Verification**: Manual testing during Phase 4

- ⚠️ **List iteration during deletion**: Deleting from list while iterating
  - **Mitigation**: Use enumerate() and del by index (safe approach)
  - **Verification**: Multiple deletion sequence tests

### Assumptions
- List-based storage is sufficient (no dict conversion needed)
- O(n) deletion performance acceptable for CLI use case
- No concurrent access concerns (single-user CLI app)
- Deleted IDs managed by NOT modifying `_next_id` counter

### Future Optimization Opportunities
- Convert to dict-based storage for O(1) operations (if scale increases)
- Add bulk delete support (if user requests)
- Add delete confirmation flag (if user feedback suggests need)
- Track deletion statistics (separate feature if needed)

## Dependencies & Prerequisites

### Prerequisites
- ✅ Add Task feature (`001-add-task`) fully implemented and tested
- ✅ TaskStorage class exists with add/get/exists/count/list_all methods
- ✅ Task model exists and validated
- ✅ CLI infrastructure with argparse and command routing
- ✅ Validator pattern established

### External Dependencies
- None (uses only Python standard library)

### Internal Dependencies
- `src/models.py`: Task dataclass (unchanged)
- `src/storage.py`: TaskStorage class (extends with delete method)
- `src/validators.py`: Validation pattern (adds task ID validator)
- `src/cli.py`: Command handler pattern (adds delete handler)

## Success Criteria Mapping

| Success Criterion | Implementation Strategy | Verification Method |
|-------------------|-------------------------|---------------------|
| SC-001: Delete in <2 seconds | Simple O(n) search, no complex operations | Manual timing test |
| SC-002: 100% rejection of invalid IDs | validate_task_id() with comprehensive checks | 9 unit tests |
| SC-003: 100% correct "not found" errors | handle_delete_command() checks return value | 4 integration tests |
| SC-004: Storage integrity maintained | No orphaned data, clean deletion from list | 3 storage tests |
| SC-005: 80%+ test coverage | 29 new tests + existing 53 = 82 total | pytest-cov report |
| SC-006: Constitutional compliance | argparse, stdout/stderr, exit codes | Integration tests |
| SC-007: ID sequence integrity | _next_id never decremented | Explicit test case |

## Timeline Estimate

**Phase 0 (Research)**: 0.5 hours (minimal - patterns established)
**Phase 1 (Storage Layer)**: 1 hour (write tests, implement delete method)
**Phase 2 (Validation Layer)**: 0.5 hours (validator function + tests)
**Phase 3 (CLI Layer)**: 1.5 hours (command handler + integration tests)
**Phase 4 (Integration Testing)**: 0.5 hours (ID sequence verification)
**Phase 5 (Polish & Quality)**: 0.5 hours (code quality, coverage checks)

**Total Estimated Time**: 4-5 hours

**Complexity**: Low (extends existing patterns, no new architecture)

## Next Steps

After plan approval:

1. **Run `/sp.tasks`**: Generate atomic task breakdown in `tasks.md`
2. **Review tasks**: Ensure tasks are prioritized and testable
3. **Begin TDD cycle**: Start with Phase 1 RED tests
4. **Iterate through phases**: Complete each phase before moving to next
5. **Verify coverage**: Check 80%+ coverage after each phase
6. **Create PHR**: Document implementation work when complete

**Ready to proceed with task generation!**
