# Implementation Plan: View Tasks

**Branch**: `003-view-tasks` | **Date**: 2025-12-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-view-tasks/spec.md`

## Summary

Implement the "View Tasks" feature for the Todo Console Application, enabling users to list all tasks with details. The feature displays tasks in creation order (ID ascending), showing ID, title, description, and status indicator (✓/✗). A summary line shows total tasks with completed/pending counts. Empty storage displays "No tasks found" message.

**Technical Approach**: Extend the existing TaskStorage class to add a `list_tasks()` method that returns formatted task display strings. Add a new `list` subcommand to the CLI using argparse. Create formatting helpers for consistent output. Follow TDD with pytest achieving 80%+ coverage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (argparse, dataclasses, datetime, typing); pytest and pytest-cov for testing
**Storage**: In-memory (list-based storage within existing TaskStorage class)
**Testing**: pytest with pytest-cov for coverage reporting (80%+ target)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: <1 second command execution time, instant in-memory operations
**Constraints**: No external runtime dependencies, no persistence, 80%+ test coverage, in-memory only
**Scale/Scope**: Single-user CLI, unbounded task count

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Python 3.13+ with Type Hints ✅ PASS
- **Requirement**: All code uses Python 3.13+, strict type hints on all functions/classes
- **Status**: Compliant - Using Python 3.13+, all design includes type annotations
- **Evidence**: List method signature: `list_tasks() -> list[str]`

### Principle II: In-Memory Storage Only ✅ PASS
- **Requirement**: No database, file persistence, or external storage
- **Status**: Compliant - TaskStorage uses in-memory list, no I/O operations
- **Evidence**: FR-007 mandates in-memory display of stored tasks

### Principle III: UV Package Manager Only ✅ PASS
- **Requirement**: Use UV exclusively for dependency management
- **Status**: Compliant - Project already uses UV (from Add/Update/Delete features)
- **Evidence**: Existing pyproject.toml and uv.lock in repository

### Principle IV: Test-Driven Development ✅ PASS
- **Requirement**: Tests written first, fail, then implement (Red-Green-Refactor)
- **Status**: Compliant - Implementation plan includes test-first workflow
- **Evidence**: Testing strategy defined, tasks will enforce TDD order

### Principle V: Test Coverage Minimum 80% ✅ PASS
- **Requirement**: 80%+ coverage measured with pytest-cov
- **Status**: Compliant - Targeting 80%+ coverage
- **Evidence**: SC-002 requires 100% task display accuracy, SC-003 requires 100% count accuracy

### Principle VI: Zero External Runtime Dependencies ✅ PASS
- **Requirement**: Only Python stdlib at runtime, pytest for testing only
- **Status**: Compliant - Using argparse (stdlib), existing Task model
- **Evidence**: FR-003 uses existing Task dataclass

### Principle VII: Clean Code and SOLID Principles ✅ PASS
- **Requirement**: Single responsibility, clear separation of concerns
- **Status**: Compliant - Extends existing layered architecture
- **Evidence**: Formatting logic separate from display logic, CLI handles routing

### Principle VIII: Documentation Standards ✅ PASS
- **Requirement**: Google-style docstrings for all modules/classes/functions
- **Status**: Compliant - All code examples include docstrings
- **Evidence**: Existing codebase follows Google-style, will maintain consistency

**Gate Result**: ✅ ALL PRINCIPLES PASS - Proceed to Implementation

---

## Architectural Decision Records

### ADR-006: Display Format Strategy

**Context**: Need to display task information in a readable, formatted way. Need to decide on output structure, status indicators, and summary statistics.

**Options Considered**:

1. **Simple list with status indicators** (chosen)
   - Pros: Clean, readable, matches spec exactly, easy to parse visually
   - Cons: Less structured than table format for programmatic use (not a requirement)

2. **Table-based format with columns**
   - Pros: Structured, aligns columns
   - Cons: Requires fixed-width fonts, harder to wrap long text, more complex

3. **JSON output option**
   - Pros: Machine-readable, useful for scripting
   - Cons: Adds complexity, not in requirements, violates simplicity principle

**Decision**: Simple list with status indicators as specified

**Rationale**:
- Matches the CLI interface examples in spec.md exactly
- Readable for human users (primary target)
- Easy to implement with existing Python string formatting
- Status symbols (✓/✗) provide quick visual scanning
- Summary statistics at bottom provide quick overview

**Implementation**:
```
TODO LIST:
────────────────────────────────────
[1] ✗ Buy groceries
    Milk, eggs, bread

[2] ✓ Call dentist
    Schedule appointment

Total: 2 tasks (1 completed, 1 pending)
```

---

## Component Design

### Architecture Overview (Extends Existing)

```
┌─────────────────────────────────────────┐
│            CLI Layer (cli.py)           │  ← Add 'list' subcommand
│  + handle_list_command()                │  ← New handler
│  + format_task_display()                │  ← New formatter
│  + format_summary()                     │  ← New formatter
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Storage Layer (storage.py)        │  ← Add list_tasks() method
│  + list_tasks() -> list[str]            │  ← New method
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Data Layer (models.py)            │  ← No changes needed
│  - Task dataclass ✓                     │  ← Already exists
└─────────────────────────────────────────┘
```

**Data Flow for `python main.py list`**:

1. **CLI** parses command → `list` subcommand with no args
2. **Storage** returns all tasks via `list_tasks()`
3. **Formatter** converts each Task to display string
4. **Formatter** calculates summary statistics
5. **CLI** prints header, task list, and summary to stdout
6. **Exit** with code 0

### File Changes

```
src/
├── storage.py           # ADD: list_tasks() method (~20 lines)
├── cli.py               # ADD: list subcommand + handler (~40 lines)
├── models.py            # NO CHANGES (reuse existing)
├── validators.py        # NO CHANGES (not needed for list)
└── main.py              # ADD: route to handle_list_command (~5 lines)

tests/
├── unit/
│   └── test_storage_list.py    # NEW: list_tasks method tests (~10 tests)
├── integration/
│   └── test_list_command.py    # NEW: Full CLI list tests (~15 tests)
└── fixtures/
    └── sample_data.py          # UNCHANGED (reuse existing)
```

### Component Details

#### 1. storage.py - Add list_tasks() Method

**Purpose**: Return all tasks in display-ready format.

**New Method**:
```python
def list_tasks(self) -> list[str]:
    """
    Get all tasks formatted for display.

    Returns:
        List of formatted task strings, one per task, in ID order
    """
```

**Design Decisions**:
- Returns list of formatted strings (one per task)
- Tasks already in creation order (list order)
- Formatting done at CLI layer for display control

---

#### 2. cli.py - Add List Subcommand and Handler

**Changes to create_parser()**:
```python
# List command
list_parser = subparsers.add_parser("list", help="List all tasks")
```

**New Handler**:
```python
def handle_list_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle 'python main.py list' command.

    Args:
        args: Parsed arguments (no specific args for list)
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success)
    """
```

**New Formatters**:
```python
def format_task_display(task: Task) -> str:
    """Format single task for list display."""

def format_list_header() -> str:
    """Return list command header."""

def format_summary(tasks: list[Task]) -> str:
    """Return summary line with counts."""
```

---

#### 3. main.py - Add Routing

**Changes**:
```python
from src.cli import handle_add_command, handle_delete_command, handle_update_command, handle_list_command

def main() -> int:
    # ... existing code ...
    elif args.command == "list":
        return handle_list_command(args, storage)
```

---

## Implementation Approach

### Phase 0: Research ✅ (Complete - leveraging existing patterns)

**Objective**: Leverage existing patterns from Add/Update/Delete features.

**Findings**:
1. ✅ TaskStorage already has `list_all()` method returning copy of task list
2. ✅ Validation functions not needed for list (no user input)
3. ✅ CLI pattern established (argparse subcommands, handlers return exit code)
4. ✅ Output formatting already exists for add/update success messages

**Output**: This plan documents decisions.

---

### Phase 1: Storage Layer Update (TDD)

**Objective**: Add list_tasks() method to TaskStorage.

**Order**:
1. **RED**: Write `tests/unit/test_storage_list.py` (all must fail)
2. **GREEN**: Add `list_tasks()` method to `src/storage.py`
3. **REFACTOR**: Clean up, ensure docstrings complete

**Test Cases for storage.list_tasks()**:
- Test returns list with correct number of formatted tasks
- Test tasks are in ascending ID order
- Test empty storage returns empty list
- Test each task includes ID, title, description, status symbol

---

### Phase 2: CLI Layer Update (TDD)

**Objective**: Add list subcommand and handler.

**Order**:
1. **RED**: Write `tests/integration/test_list_command.py` (all must fail)
2. **GREEN**: Add list to `cli.py` and `main.py`
3. **REFACTOR**: Extract common patterns if beneficial

**Test Cases for CLI list command**:
- Test list with multiple tasks shows all tasks
- Test list with empty storage shows "No tasks found"
- Test status symbols: ✗ for incomplete, ✓ for complete
- Test summary line shows correct counts
- Test output format matches specification
- Test Unicode characters display correctly
- Test long text wraps or displays fully

---

### Phase 3: Quality Gates

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

## Testing Strategy

### Test Coverage Goals

- **Target**: 80%+ overall coverage (constitution requirement)
- **Measured with**: pytest-cov

### Test Categories

#### 1. Unit Tests - Storage List (test_storage_list.py)

**Purpose**: Validate TaskStorage.list_tasks() behavior.

**Test Cases** (8 tests):

1. `test_list_empty_storage_returns_empty` - Empty storage returns empty list
2. `test_list_single_task` - Single task returns list with one formatted task
3. `test_list_multiple_tasks` - Multiple tasks return in ID order
4. `test_list_incomplete_task_status_symbol` - Incomplete shows ✗
5. `test_list_complete_task_status_symbol` - Complete shows ✓
6. `test_list_preserves_id_order` - Tasks in ascending ID order
7. `test_list_includes_title` - Formatted output includes title
8. `test_list_includes_description` - Formatted output includes description

**Coverage Target**: 100% of storage.list_tasks() method

---

#### 2. Integration Tests - CLI List (test_list_command.py)

**Purpose**: Validate full CLI list workflow.

**Test Cases** (15 tests):

1. `test_list_empty_shows_no_tasks_message` - Empty storage displays correctly
2. `test_list_single_task` - Single task displays correctly
3. `test_list_multiple_tasks` - Multiple tasks display in order
4. `test_list_incomplete_status_symbol` - Incomplete shows ✗
5. `test_list_complete_status_symbol` - Complete shows ✓
6. `test_list_summary_counts_completed` - Summary counts complete correctly
7. `test_list_summary_counts_pending` - Summary counts pending correctly
8. `test_list_header_format` - Header matches specification
9. `test_list_divider_present` - Divider line present
10. `test_list_singular_task` - Summary uses "1 task" for single task
11. `test_list_unicode_title` - Unicode in title displays correctly
12. `test_list_unicode_description` - Unicode in description displays correctly
13. `test_list_unicode_status_symbols` - Status symbols display correctly
14. `test_list_none_description_shows_none` - Task with no description shows "(none)"
15. `test_list_exit_code_0` - List command returns exit code 0

**Test Helpers** (reuse existing from test_add_command.py):
- `run_cli(args: list[str]) -> tuple[int, str, str]`
- `create_task_with_status()` helper

**Coverage Target**: >90% of cli.py list-related code

---

### Expected Coverage Report

**After View Tasks Implementation**:

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
2. **Documentation**: Update README with list command examples
3. **Demo**: Show working `list` command
4. **Prepare for next feature**: complete/incomplete toggle commands

---

## Open Questions / Decisions Deferred

**None.** All clarifications resolved in spec creation. Requirements are complete and unambiguous.

---

## References

- **Feature Spec**: [spec.md](./spec.md)
- **Add Task Plan**: [../001-add-task/plan.md](../001-add-task/plan.md) (reference for patterns)
- **Update Task Plan**: [../001-update-task/plan.md](../001-update-task/plan.md) (reference for patterns)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Existing Code**: src/storage.py, src/cli.py, src/validators.py

---

**Plan Status**: ✅ Complete - Ready for `/sp.tasks`
