# Implementation Plan: Update Task

**Branch**: `001-update-task` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-update-task/spec.md`

## Summary

Implement the "Update Task" feature for the Todo Console Application, enabling users to modify existing tasks by ID. Users can update title only (`--title`), description only (`--desc`), or both simultaneously. The feature preserves unchanged fields, maintains immutable properties (ID, status, created_at), and follows the same validation rules as Add Task (title: 1-100 chars, description: max 500 chars). At least one update argument is required.

**Technical Approach**: Extend the existing TaskStorage class with an `update()` method that performs in-place modification. Add a new `update` subcommand to the CLI using argparse. Reuse existing validation functions from validators.py. Follow TDD with pytest achieving 80%+ coverage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (argparse, dataclasses, datetime, typing); pytest and pytest-cov for testing
**Storage**: In-memory (list-based storage within existing TaskStorage class)
**Testing**: pytest with pytest-cov for coverage reporting (80%+ target)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: <2 seconds command execution time, instant in-memory operations
**Constraints**: No external runtime dependencies, no persistence, 80%+ test coverage, in-memory only
**Scale/Scope**: Single-user CLI, unbounded task count

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Python 3.13+ with Type Hints ✅ PASS
- **Requirement**: All code uses Python 3.13+, strict type hints on all functions/classes
- **Status**: Compliant - Using Python 3.13+, all design includes type annotations
- **Evidence**: Update method signature: `update(task_id: int, title: str | None = None, description: str | None = None) -> Task | None`

### Principle II: In-Memory Storage Only ✅ PASS
- **Requirement**: No database, file persistence, or external storage
- **Status**: Compliant - TaskStorage uses in-memory list, no I/O operations
- **Evidence**: FR-019 explicitly mandates in-memory only

### Principle III: UV Package Manager Only ✅ PASS
- **Requirement**: Use UV exclusively for dependency management
- **Status**: Compliant - Project already uses UV (from Add Task feature)
- **Evidence**: Existing pyproject.toml and uv.lock in repository

### Principle IV: Test-Driven Development ✅ PASS
- **Requirement**: Tests written first, fail, then implement (Red-Green-Refactor)
- **Status**: Compliant - Implementation plan includes test-first workflow
- **Evidence**: Testing strategy defined, tasks will enforce TDD order

### Principle V: Test Coverage Minimum 80% ✅ PASS
- **Requirement**: 80%+ coverage measured with pytest-cov
- **Status**: Compliant - Targeting 80%+ coverage
- **Evidence**: SC-008 requires 80%+, testing strategy comprehensive

### Principle VI: Zero External Runtime Dependencies ✅ PASS
- **Requirement**: Only Python stdlib at runtime, pytest for testing only
- **Status**: Compliant - Using argparse (stdlib), existing validators
- **Evidence**: FR-018 mandates argparse, constitution prohibits external deps

### Principle VII: Clean Code and SOLID Principles ✅ PASS
- **Requirement**: Single responsibility, clear separation of concerns
- **Status**: Compliant - Extends existing layered architecture
- **Evidence**: Update logic follows same pattern as Add/Delete (validators → storage → CLI)

### Principle VIII: Documentation Standards ✅ PASS
- **Requirement**: Google-style docstrings for all modules/classes/functions
- **Status**: Compliant - All code examples include docstrings
- **Evidence**: Existing codebase follows Google-style, will maintain consistency

**Gate Result**: ✅ ALL PRINCIPLES PASS - Proceed to Implementation

## Architectural Decision Records

### ADR-005: Update Operation Strategy

**Context**: Need to implement task update functionality that modifies title and/or description while preserving other fields (id, status, created_at).

**Options Considered**:

1. **In-place modification with new Task instance** (chosen)
   - Pros: Maintains immutability semantics (dataclass), clear what changed, consistent with existing patterns
   - Cons: Creates new object even for small changes (negligible for in-memory)

2. **Mutable Task with setters**
   - Pros: True in-place modification, no object creation
   - Cons: Violates immutability best practices, harder to track changes, inconsistent with existing Task dataclass design

3. **Task.copy_with() method**
   - Pros: Functional approach, explicit
   - Cons: Adds complexity to Task model, different pattern than existing code

**Decision**: Create new Task instance with updated values, replace in storage list

**Rationale**:
- Consistent with existing `delete()` pattern (modifies storage, not task)
- Task dataclass remains simple (no copy methods or setters)
- Clear validation boundary (CLI validates, storage just stores)
- Easy to test (compare before/after Task instances)

**Implementation**:
```python
def update(self, task_id: int, title: str | None = None,
           description: str | None = None) -> Task | None:
    """Update task by ID, returning updated Task or None if not found."""
    for i, task in enumerate(self._tasks):
        if task.id == task_id:
            updated_task = Task(
                id=task.id,
                title=title.strip() if title is not None else task.title,
                description=description if description is not None else task.description,
                status=task.status,  # Preserved
                created_at=task.created_at  # Preserved
            )
            self._tasks[i] = updated_task
            return updated_task
    return None
```

---

### ADR-006: Optional Parameter Handling (None vs Sentinel)

**Context**: Update accepts optional `--title` and `--desc`. Need to distinguish between "not provided" (preserve existing) and "explicitly empty" (clear the field for description).

**Options Considered**:

1. **None means "not provided"** (chosen)
   - Pros: Simple, Pythonic, matches argparse defaults
   - Cons: Cannot distinguish "not provided" from "explicitly set to None" for description

2. **Sentinel object pattern**
   - Pros: Can distinguish "not provided" vs "explicitly None"
   - Cons: Overly complex for this use case, description clearing uses empty string `--desc ""`

3. **Separate boolean flags**
   - Pros: Explicit intent
   - Cons: Verbose API, more arguments to track

**Decision**: Use `None` to mean "not provided, preserve existing"

**Rationale**:
- argparse returns `None` by default for unprovided optional args
- Empty string `--desc ""` is the explicit way to clear description
- Title cannot be empty (validation rejects), so no ambiguity there
- Simple, matches existing Add Task pattern

---

## Component Design

### Architecture Overview (Extends Existing)

```
┌─────────────────────────────────────────┐
│            CLI Layer (cli.py)           │  ← Add 'update' subcommand
│  + handle_update_command()              │  ← New handler
│  + format_update_success_message()      │  ← New formatter (or reuse)
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Validation Layer (validators.py)  │  ← Reuse existing
│  - validate_title() ✓                   │  ← Already exists
│  - validate_description() ✓             │  ← Already exists
│  - validate_task_id() ✓                 │  ← Already exists
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Storage Layer (storage.py)        │  ← Add update() method
│  + update(task_id, title, desc) -> Task │  ← New method
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Data Layer (models.py)            │  ← No changes needed
│  - Task dataclass ✓                     │  ← Already exists
└─────────────────────────────────────────┘
```

**Data Flow for `python main.py update 1 --title "New title"`**:

1. **CLI** parses arguments → `{"task_id": "1", "title": "New title", "desc": None}`
2. **Validators** validate task_id → `(True, "", 1)`
3. **Validators** validate title → `(True, "")`
4. **CLI** checks at least one update arg provided → passes
5. **TaskStorage.update(1, "New title", None)** finds task, creates updated Task
6. **Task.__post_init__()** validates new Task → passes
7. **TaskStorage** replaces task in list
8. **CLI** formats success message → prints to stdout, exits with code 0

### File Changes

```
src/
├── storage.py           # ADD: update() method (~25 lines)
├── cli.py               # ADD: update subcommand + handler (~50 lines)
├── validators.py        # NO CHANGES (reuse existing)
├── models.py            # NO CHANGES (reuse existing)
└── main.py              # ADD: route to handle_update_command (~5 lines)

tests/
├── unit/
│   └── test_storage_update.py    # NEW: Update method tests (~20 tests)
├── integration/
│   └── test_update_command.py    # NEW: Full CLI tests (~25 tests)
```

### Component Details

#### 1. storage.py - Add update() Method

**Purpose**: Modify existing task by ID with partial updates.

**New Method**:
```python
def update(self, task_id: int, title: str | None = None,
           description: str | None = None) -> Task | None:
    """
    Update task by ID.

    Args:
        task_id: The ID of the task to update
        title: New title (if provided, replaces existing; validated at CLI layer)
        description: New description (if provided, replaces existing; empty string clears it)

    Returns:
        Updated Task object if found, None if task not found

    Note:
        - At least one of title or description must be provided (enforced at CLI layer)
        - Status and created_at are never modified
        - Validation happens at CLI layer before calling this method
    """
```

**Design Decisions**:
- Linear search to find task (consistent with existing get())
- In-place list replacement (not append/remove)
- Returns updated Task for CLI formatting
- Returns None if not found (consistent with get())
- Title is stripped, description preserved as-is (per spec)

---

#### 2. cli.py - Add Update Subcommand and Handler

**Changes to create_parser()**:
```python
# Update command
update_parser = subparsers.add_parser("update", help="Update a task by ID")
update_parser.add_argument(
    "task_id",
    type=str,
    help="Task ID to update (positive integer)",
)
update_parser.add_argument(
    "--title",
    type=str,
    default=None,
    help="New task title (1-100 characters)",
)
update_parser.add_argument(
    "--desc",
    type=str,
    default=None,
    help="New task description (max 500 characters, empty string clears)",
)
```

**New Handler**:
```python
def handle_update_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle 'python main.py update' command.

    Args:
        args: Parsed arguments with task_id, title, desc
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
```

**Validation Order**:
1. Validate task_id format (positive integer)
2. Check at least one of --title or --desc provided
3. Validate title if provided (non-empty after trim, 1-100 chars)
4. Validate description if provided (max 500 chars)
5. Check task exists
6. Perform update

**Success Message Format** (consistent with Add):
```
Task updated successfully
  ID: 1
  Title: New title
  Description: New description
  Status: incomplete
```

---

#### 3. main.py - Add Routing

**Changes**:
```python
from src.cli import handle_add_command, handle_delete_command, handle_update_command

def main() -> int:
    # ... existing code ...
    elif args.command == "update":
        return handle_update_command(args, storage)
```

---

## Project Structure

### Documentation (this feature)

```text
specs/001-update-task/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0 output (minimal - leveraging existing patterns)
├── data-model.md        # Phase 1 output (Task entity - no changes needed)
├── quickstart.md        # Phase 1 output (usage guide)
├── checklists/
│   └── requirements.md  # Spec quality checklist (complete)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code Changes

```text
src/
├── storage.py           # MODIFY: Add update() method
├── cli.py               # MODIFY: Add update subcommand + handler
├── validators.py        # UNCHANGED (reuse validate_title, validate_description, validate_task_id)
├── models.py            # UNCHANGED (Task dataclass)
└── main.py              # MODIFY: Add routing for update command

tests/
├── unit/
│   ├── test_storage_update.py    # NEW: 15+ tests for storage.update()
│   └── (existing test files)
├── integration/
│   ├── test_update_command.py    # NEW: 20+ tests for CLI update
│   └── (existing test files)
└── fixtures/
    └── sample_data.py            # UNCHANGED (reuse existing)
```

**Structure Decision**: Single project structure (existing). Changes are additive to existing files following established patterns.

**Estimated Changes**:
- storage.py: +25 lines
- cli.py: +60 lines
- main.py: +5 lines
- test_storage_update.py: ~150 lines (new file)
- test_update_command.py: ~250 lines (new file)

---

## Implementation Approach

### Phase Breakdown

#### Phase 0: Research ✅ (Complete)

**Objective**: Leverage existing patterns from Add/Delete features.

**Findings**:
1. ✅ Validation functions already exist (validate_title, validate_description, validate_task_id)
2. ✅ TaskStorage pattern established (linear search, return Task or None)
3. ✅ CLI pattern established (argparse subcommands, handlers return exit code)
4. ✅ Error formatting established (format_error_message function)

**Output**: ADR-005 and ADR-006 documented above.

---

#### Phase 1: Storage Layer Update (TDD)

**Objective**: Add update() method to TaskStorage.

**Order**:
1. **RED**: Write `tests/unit/test_storage_update.py` (all must fail)
2. **GREEN**: Add `update()` method to `src/storage.py`
3. **REFACTOR**: Clean up, ensure docstrings complete

**Test Cases for storage.update()**:
- Test update title only preserves description
- Test update description only preserves title
- Test update both title and description
- Test update non-existent task returns None
- Test update from empty storage returns None
- Test update preserves completion status ("incomplete")
- Test update preserves completion status ("complete")
- Test update preserves created_at timestamp
- Test update with empty description clears it (sets to empty string or None)
- Test update doesn't affect other tasks in storage
- Test update returns the updated Task object
- Test update replaces task in-place (same list position)
- Test title is stripped before storage
- Test description is preserved as-is (no stripping)

**Validation**: `uv run pytest tests/unit/test_storage_update.py -v` all pass

---

#### Phase 2: CLI Layer Update (TDD)

**Objective**: Add update subcommand and handler.

**Order**:
1. **RED**: Write `tests/integration/test_update_command.py` (all must fail)
2. **GREEN**: Add update to `cli.py` and `main.py`
3. **REFACTOR**: Extract common patterns if beneficial

**Test Cases for CLI update command**:
- Test `update 1 --title "New"` updates title only
- Test `update 1 --desc "New"` updates description only
- Test `update 1 --title "New" --desc "New"` updates both
- Test `update 1 --desc ""` clears description
- Test success message format (ID, title, description, status)
- Test success message to stdout
- Test exit code 0 on success
- Test `update 999 --title "New"` returns "Task not found" error
- Test `update abc --title "New"` returns "Task ID must be a positive integer"
- Test `update -5 --title "New"` returns "Task ID must be a positive integer"
- Test `update 0 --title "New"` returns "Task ID must be a positive integer"
- Test `update 1` (no --title or --desc) returns error
- Test `update 1 --title ""` returns "Title cannot be empty"
- Test `update 1 --title "   "` (whitespace only) returns "Title cannot be empty"
- Test `update 1 --title "<101 chars>"` returns length error
- Test `update 1 --desc "<501 chars>"` returns length error
- Test error messages go to stderr
- Test exit code 1 on error
- Test update preserves status (incomplete)
- Test update preserves status (complete)
- Test Unicode title support
- Test Unicode description support
- Test boundary: title exactly 100 chars succeeds
- Test boundary: description exactly 500 chars succeeds

**Validation**: `uv run pytest tests/integration/test_update_command.py -v` all pass

---

#### Phase 3: Quality Gates

**Objective**: Validate coverage and code quality.

**Tasks**:
1. Run full test suite: `uv run pytest --cov=src --cov-report=term`
2. Verify coverage ≥80%
3. Run type checker: `uv run mypy src/ --strict`
4. Run linter: `uv run ruff check src/ tests/`
5. Run formatter: `uv run black src/ tests/ --check`
6. Fix any issues found

**Validation**:
- Coverage ≥80%
- mypy 0 errors
- ruff 0 violations
- black compliant

---

### Dependency Graph

```
Phase 0 (Research) ✅ Complete
    ↓
Phase 1 (Storage Layer)
    ↓
Phase 2 (CLI Layer) ← depends on storage.update()
    ↓
Phase 3 (Quality Gates) ← depends on all code
```

---

## Testing Strategy

### Test Coverage Goals

- **Target**: 80%+ overall coverage (constitution requirement)
- **Measured with**: pytest-cov

### Test Categories

#### 1. Unit Tests - Storage Update (test_storage_update.py)

**Purpose**: Validate TaskStorage.update() behavior.

**Test Cases** (15 tests):

1. `test_update_title_only_preserves_description` - Update title, description unchanged
2. `test_update_description_only_preserves_title` - Update description, title unchanged
3. `test_update_both_title_and_description` - Update both fields
4. `test_update_non_existent_task_returns_none` - ID 999 returns None
5. `test_update_empty_storage_returns_none` - Empty storage returns None
6. `test_update_preserves_incomplete_status` - Status "incomplete" preserved
7. `test_update_preserves_complete_status` - Status "complete" preserved
8. `test_update_preserves_created_at` - Timestamp unchanged
9. `test_update_with_empty_description_clears_it` - `--desc ""` clears description
10. `test_update_does_not_affect_other_tasks` - Only target task modified
11. `test_update_returns_updated_task` - Returns Task object
12. `test_update_replaces_task_in_place` - Same index in list
13. `test_update_strips_title` - Title whitespace trimmed
14. `test_update_preserves_description_whitespace` - Description not trimmed
15. `test_update_with_none_params_preserves_existing` - None means no change

**Coverage Target**: 100% of storage.update() method

---

#### 2. Integration Tests - CLI Update (test_update_command.py)

**Purpose**: Validate full CLI update workflow.

**Test Cases** (22 tests):

1. `test_update_title_only_success` - Update title, check output
2. `test_update_description_only_success` - Update description, check output
3. `test_update_both_success` - Update both, check output
4. `test_update_clear_description` - Clear with `--desc ""`
5. `test_update_success_message_format` - Correct output format
6. `test_update_success_to_stdout` - Output channel
7. `test_update_success_exit_code_0` - Exit code
8. `test_update_non_existent_id_error` - ID 999 error
9. `test_update_invalid_id_non_numeric_error` - "abc" error
10. `test_update_invalid_id_negative_error` - "-5" error
11. `test_update_invalid_id_zero_error` - "0" error
12. `test_update_no_args_error` - No --title or --desc
13. `test_update_empty_title_error` - `--title ""` error
14. `test_update_whitespace_title_error` - `--title "   "` error
15. `test_update_title_too_long_error` - 101 chars error
16. `test_update_description_too_long_error` - 501 chars error
17. `test_update_error_to_stderr` - Error channel
18. `test_update_error_exit_code_1` - Exit code
19. `test_update_preserves_incomplete_status` - Status check
20. `test_update_preserves_complete_status` - Status check
21. `test_update_unicode_title` - Unicode support
22. `test_update_boundary_100_char_title` - Boundary test

**Test Helpers** (reuse existing from test_add_command.py):
- `run_cli(args: list[str]) -> tuple[int, str, str]`
- `create_long_string(length: int) -> str`

**Coverage Target**: >90% of cli.py update-related code

---

### Expected Coverage Report

**After Update Task Implementation**:

```
Name                Stmts   Miss  Cover
---------------------------------------
src/storage.py         XX      X    95%
src/cli.py             XX      X    92%
src/validators.py      XX      X    98%
src/models.py          XX      X    97%
src/main.py            XX      X    93%
---------------------------------------
TOTAL                 XXX     XX    94%
```

**Exceeds**: 94% > 80% minimum ✅

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All 8 constitutional principles pass. No complexity justification required.

---

## Next Steps

### After Planning (Current Stage)

1. **Review this plan** for approval
2. **Run `/sp.tasks`** to generate tasks.md from this plan
3. **Begin Phase 1** (Storage Layer Update) per TDD workflow

### After Implementation

1. **Manual Testing**: Execute CLI commands manually
2. **Documentation**: Update README with update command examples
3. **Demo**: Show working `update` command
4. **Prepare for next feature**: list, complete/incomplete commands

---

## Open Questions / Decisions Deferred

**None.** All clarifications resolved in spec clarification session (2025-12-29).

---

## References

- **Feature Spec**: [spec.md](./spec.md)
- **Add Task Plan**: [../001-add-task/plan.md](../001-add-task/plan.md) (reference for patterns)
- **Delete Task Spec**: [../002-delete-task/spec.md](../002-delete-task/spec.md) (reference for patterns)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Existing Code**: src/storage.py, src/cli.py, src/validators.py

---

**Plan Status**: ✅ Complete - Ready for `/sp.tasks`
