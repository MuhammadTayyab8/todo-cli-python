# Implementation Plan: Add Task

**Branch**: `001-add-task` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-add-task/spec.md`

## Summary

Implement the "Add Task" feature for the Todo Console Application, enabling users to create new tasks with a required title (1-100 chars) and optional description (max 500 chars). Tasks are assigned auto-generated sequential integer IDs starting from 1, default to "incomplete" status, and are stored in-memory with a created_at timestamp. The CLI uses argparse for argument parsing, validates all inputs, and provides clear error messages to stderr with exit code 1 for failures and exit code 0 for success.

**Technical Approach**: Use Python 3.13+ with dataclasses for the Task model, a custom TaskStorage class managing a list of tasks with sequential ID generation, argparse for CLI parsing, and comprehensive validation at the CLI layer before storage. Follow TDD with pytest achieving 90%+ coverage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (argparse, dataclasses, datetime, typing); pytest and pytest-cov for testing
**Storage**: In-memory (list-based storage within TaskStorage class)
**Testing**: pytest with pytest-cov for coverage reporting (90%+ target)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**: <5 seconds command execution time, instant in-memory operations
**Constraints**: No external runtime dependencies, no persistence, 80%+ test coverage (targeting 90%+), in-memory only
**Scale/Scope**: Single-user CLI, unbounded task count (Python integers support arbitrary size)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Python 3.13+ with Type Hints ✅ PASS
- **Requirement**: All code uses Python 3.13+, strict type hints on all functions/classes
- **Status**: Compliant - Using Python 3.13+, all design includes type annotations
- **Evidence**: Task dataclass, validation functions, and CLI handlers will all use type hints

### Principle II: In-Memory Storage Only ✅ PASS
- **Requirement**: No database, file persistence, or external storage
- **Status**: Compliant - TaskStorage uses in-memory list, no I/O operations
- **Evidence**: FR-008, FR-014 explicitly mandate in-memory only

### Principle III: UV Package Manager Only ✅ PASS
- **Requirement**: Use UV exclusively for dependency management
- **Status**: Compliant - Project will use UV for setup and dependency management
- **Evidence**: pyproject.toml will specify dependencies, UV will manage environment

### Principle IV: Test-Driven Development ✅ PASS
- **Requirement**: Tests written first, fail, then implement (Red-Green-Refactor)
- **Status**: Compliant - Implementation plan includes test-first workflow
- **Evidence**: Testing strategy defined, tasks will enforce TDD order

### Principle V: Test Coverage Minimum 80% ✅ PASS
- **Requirement**: 80%+ coverage measured with pytest-cov
- **Status**: Compliant - Targeting 90%+ coverage
- **Evidence**: SC-005 requires 80%+, testing strategy comprehensive

### Principle VI: Zero External Runtime Dependencies ✅ PASS
- **Requirement**: Only Python stdlib at runtime, pytest for testing only
- **Status**: Compliant - Using argparse, dataclasses, datetime (all stdlib)
- **Evidence**: FR-013 mandates argparse, constitution prohibits external deps

### Principle VII: Clean Code and SOLID Principles ✅ PASS
- **Requirement**: Single responsibility, clear separation of concerns
- **Status**: Compliant - Layered architecture (models, storage, validators, CLI)
- **Evidence**: Design separates concerns: Task (data), TaskStorage (storage), validators (validation), CLI (interface)

### Principle VIII: Documentation Standards ✅ PASS
- **Requirement**: Google-style docstrings for all modules/classes/functions
- **Status**: Compliant - All code examples include docstrings
- **Evidence**: Spec includes docstring examples, plan mandates documentation

**Gate Result**: ✅ ALL PRINCIPLES PASS - Proceed to Phase 0

## Architectural Decision Records

### ADR-001: Task Data Model - Dataclass

**Context**: Need to represent a Task entity with typed fields (id, title, description, status, created_at).

**Options Considered**:

1. **dataclass** (chosen)
   - Pros: Built-in (no deps), auto-generates `__init__` and `__repr__`, supports type hints, `__post_init__` for validation, frozen option for immutability
   - Cons: Slightly more verbose than NamedTuple, requires Python 3.7+

2. **NamedTuple**
   - Pros: Immutable by default, lightweight, tuple-like access
   - Cons: Less flexible (immutable makes updates harder), no `__post_init__` for validation logic, less intuitive for complex objects

3. **Pydantic BaseModel**
   - Pros: Automatic validation, great for APIs/serialization, rich ecosystem
   - Cons: **External dependency (violates Principle VI)**, overkill for in-memory CLI

**Decision**: Use `@dataclass` from Python standard library

**Rationale**:
- Complies with zero external dependencies principle (Principle VI)
- Type hints natively supported (Principle I)
- `__post_init__` enables validation at construction (data integrity)
- Can optionally make frozen for immutability
- Clear, readable, Pythonic syntax
- Well-documented and widely adopted

**Implementation**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a single to-do item."""
    id: int
    title: str
    description: Optional[str]
    status: str  # "complete" or "incomplete"
    created_at: datetime
```

---

### ADR-002: Storage Strategy - TaskStorage Class with List

**Context**: Need in-memory storage for tasks with ID generation, retrieval, and potential future operations (update, delete, list, filter).

**Options Considered**:

1. **TaskStorage class with list** (chosen)
   - Pros: Encapsulates storage logic, maintains insertion order, simple iteration for filtering/sorting, clear API (add/get/exists), ID generation co-located
   - Cons: O(n) lookup by ID (acceptable for in-memory CLI with expected small dataset)

2. **TaskStorage class with dict (keyed by ID)**
   - Pros: O(1) lookup by ID, efficient retrieval
   - Cons: No guaranteed order (though Python 3.7+ dicts maintain insertion order), slight mental overhead (dict vs list)

3. **Global list/dict (no class)**
   - Pros: Simplest possible approach
   - Cons: **Violates Single Responsibility and encapsulation (Principle VII)**, harder to test, no clear API, global state management issues

**Decision**: Use `TaskStorage` class with internal list (`self._tasks: list[Task]`)

**Rationale**:
- Encapsulation (Principle VII): Storage logic isolated in single class
- Testability: Easy to instantiate and test in isolation
- Maintainability: Clear contract (public methods: add, get, exists, count, list, etc.)
- Performance: List iteration is fast for expected use case (CLI, not web-scale)
- Ordering: Preserves insertion order naturally (useful for "list" command later)
- ID generation: Co-located with storage (single responsibility: manage tasks and IDs)
- Future-proof: Easy to add methods (delete, update, filter) without touching other code

**ID Generation Approach**:
- Maintain `self._next_id: int` counter starting at 1
- Increment after each task creation (monotonic, no reuse)
- Sequential IDs (1, 2, 3, ...) per clarification decision

**Implementation**:
```python
from typing import Optional

class TaskStorage:
    """In-memory storage for tasks with ID generation."""

    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add(self, title: str, description: Optional[str] = None) -> Task:
        """Create and store a new task."""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            status="incomplete",
            created_at=datetime.now()
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve task by ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def exists(self, task_id: int) -> bool:
        """Check if task with given ID exists."""
        return self.get(task_id) is not None

    def count(self) -> int:
        """Return total number of tasks."""
        return len(self._tasks)

    def list_all(self) -> list[Task]:
        """Return all tasks."""
        return self._tasks.copy()  # Return copy to prevent external modification
```

---

### ADR-003: CLI Framework - argparse

**Context**: Need CLI argument parsing for `todo add <title> [--description <text>]`.

**Options Considered**:

1. **argparse** (chosen)
   - Pros: Built-in standard library (no deps), well-documented, handles complex arg patterns, automatic help generation, supports subcommands
   - Cons: More verbose than modern alternatives, older API design

2. **click**
   - Pros: Modern decorator-based API, cleaner syntax, excellent for multi-command CLIs
   - Cons: **External dependency (violates Principle VI)**

3. **typer**
   - Pros: Type-hint driven (fits Python 3.13+ perfectly), modern, built on click
   - Cons: **External dependency (violates Principle VI)**

**Decision**: Use `argparse` from Python standard library

**Rationale**:
- **Zero external dependencies** (Principle VI non-negotiable)
- FR-013 explicitly mandates argparse per constitution
- Mature, stable, well-tested (20+ years in stdlib)
- Supports all required features: positional args, optional flags, validation, help text, exit codes
- Sufficient for simple CLI (`todo add <title> [--description <text>]`)
- Wide familiarity in Python community

**Implementation**:
```python
import argparse
import sys

def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Simple CLI todo application"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title (1-100 characters)")
    add_parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Task description (max 500 characters, optional)"
    )

    return parser
```

---

## Component Design

### Architecture Overview

The application follows a layered architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│            CLI Layer (cli.py)           │  ← User interaction, arg parsing
│  - ArgumentParser setup                 │
│  - Command handlers (handle_add_command)│
│  - Output formatting                    │
│  - Error handling and exit codes        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Validation Layer (validators.py)  │  ← Input validation
│  - validate_title()                     │
│  - validate_description()               │
│  - Return (is_valid, error_message)     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Storage Layer (storage.py)        │  ← Business logic & state
│  - TaskStorage class                    │
│  - add() / get() / exists()             │
│  - ID generation                        │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Data Layer (models.py)            │  ← Data structures
│  - Task dataclass                       │
│  - Field definitions                    │
│  - Validation in __post_init__          │
└─────────────────────────────────────────┘
```

**Data Flow for `todo add "Buy milk" --description "2% milk"`**:

1. **CLI** parses arguments → `{"title": "Buy milk", "description": "2% milk"}`
2. **Validators** validate title and description → `(True, "")` for both
3. **TaskStorage.add()** creates Task → `Task(id=1, title="Buy milk", description="2% milk", status="incomplete", created_at=<now>)`
4. **Task.__post_init__()** validates on construction → passes
5. **TaskStorage** appends to list, increments ID counter
6. **CLI** formats success message → prints to stdout, exits with code 0

### File Structure

```
src/
├── __init__.py
├── models.py          # Task dataclass
├── storage.py         # TaskStorage class
├── validators.py      # Input validation functions
├── cli.py             # CLI argument parsing and command handlers
└── main.py            # Entry point

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py       # Task dataclass tests
│   ├── test_validators.py       # Validation function tests
│   └── test_storage.py          # TaskStorage tests
├── integration/
│   ├── __init__.py
│   └── test_add_command.py      # Full CLI workflow tests
└── fixtures/
    ├── __init__.py
    └── sample_data.py           # Shared test data
```

### Component Details

#### 1. models.py - Task Dataclass

**Purpose**: Define the Task data structure with validation.

**Responsibilities**:
- Define Task fields with type hints
- Validate field constraints in `__post_init__` (defensive programming)
- Provide clear error messages for invalid construction

**Key Methods**:
- `__init__` (auto-generated by dataclass)
- `__post_init__`: Validates id, title, description, status constraints

**Design Decisions**:
- Use `Optional[str]` for description (explicit optionality)
- Validate in `__post_init__` as last line of defense (validation also at CLI layer)
- Consider `frozen=True` for immutability (decide during implementation)

**Type Signature**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
```

---

#### 2. storage.py - TaskStorage Class

**Purpose**: Manage in-memory task storage and ID generation.

**Responsibilities**:
- Store tasks in memory (list)
- Generate unique sequential IDs
- Provide CRUD operations (currently: Create and Read)
- Ensure data integrity

**Key Methods**:
- `__init__()`: Initialize empty list and ID counter
- `add(title, description) -> Task`: Create and store task
- `get(task_id) -> Optional[Task]`: Retrieve by ID
- `exists(task_id) -> bool`: Check existence
- `count() -> int`: Total task count
- `list_all() -> list[Task]`: Return all tasks (copy)

**Design Decisions**:
- Use list (not dict) per ADR-002
- Return copy of list in `list_all()` to prevent external mutation
- Linear search in `get()` acceptable for expected scale
- ID counter never decrements (no ID reuse per spec)

**Type Signature**:
```python
class TaskStorage:
    _tasks: list[Task]
    _next_id: int

    def add(self, title: str, description: Optional[str] = None) -> Task: ...
    def get(self, task_id: int) -> Optional[Task]: ...
    def exists(self, task_id: int) -> bool: ...
    def count(self) -> int: ...
    def list_all(self) -> list[Task]: ...
```

---

#### 3. validators.py - Input Validation

**Purpose**: Validate user input (title and description) with clear error messages.

**Responsibilities**:
- Validate title: non-empty after trim, 1-100 chars
- Validate description: max 500 chars if provided
- Return `(is_valid: bool, error_message: str)` tuples

**Key Functions**:
- `validate_title(title: str) -> tuple[bool, str]`
- `validate_description(description: Optional[str]) -> tuple[bool, str]`

**Design Decisions**:
- Pure functions (no side effects, easy to test)
- Return tuple (not raise exceptions) for flow control
- Trim title whitespace before validation
- Preserve description as-is (no trimming per spec)
- Empty description is valid, None is valid

**Type Signature**:
```python
def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title.

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    ...

def validate_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate task description.

    Args:
        description: The description string to validate, or None

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    ...
```

---

#### 4. cli.py - CLI Interface

**Purpose**: Parse command-line arguments, handle commands, format output.

**Responsibilities**:
- Create argparse parser with subcommands
- Validate inputs using validators.py
- Call TaskStorage methods
- Format success/error messages
- Write to stdout (success) or stderr (errors)
- Return exit codes (0 success, 1 error)

**Key Functions**:
- `create_parser() -> ArgumentParser`: Configure argparse
- `handle_add_command(args, storage) -> int`: Execute add logic
- `format_success_message(task) -> str`: Format task details
- `format_error_message(error) -> str`: Format error with "Error: " prefix

**Design Decisions**:
- Validate at CLI layer before calling storage (fail fast)
- Use `sys.stdout.write()` and `sys.stderr.write()` for explicit channel control
- Return exit codes (not sys.exit()) for testability
- Multi-line success message format (per spec examples)

**Type Signature**:
```python
def create_parser() -> argparse.ArgumentParser: ...

def handle_add_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle 'todo add' command.

    Args:
        args: Parsed arguments from argparse
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    ...

def format_success_message(task: Task) -> str: ...
def format_error_message(error: str) -> str: ...
```

---

#### 5. main.py - Entry Point

**Purpose**: Application entry point, wires components together.

**Responsibilities**:
- Create TaskStorage instance (application state)
- Create parser
- Parse sys.argv
- Route to appropriate command handler
- Exit with returned exit code

**Key Function**:
- `main() -> int`: Main application logic

**Design Decisions**:
- Single global TaskStorage instance (simple for single-command run)
- For multi-command sessions (future interactive mode), TaskStorage would persist
- Keep minimal (just wiring, no business logic)

**Type Signature**:
```python
def main() -> int:
    """
    Main entry point for the todo application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    ...

if __name__ == "__main__":
    sys.exit(main())
```

---

## Project Structure

### Documentation (this feature)

```text
specs/001-add-task/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (decisions, rationale)
├── data-model.md        # Phase 1 output (Task entity details)
├── quickstart.md        # Phase 1 output (getting started guide)
├── contracts/           # Phase 1 output (not applicable for CLI)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── models.py            # Task dataclass (40 lines est.)
├── storage.py           # TaskStorage class (80 lines est.)
├── validators.py        # Validation functions (50 lines est.)
├── cli.py               # CLI parsing and handlers (120 lines est.)
└── main.py              # Entry point (30 lines est.)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task_model.py       # 15 tests (150 lines)
│   ├── test_validators.py       # 12 tests (120 lines)
│   └── test_storage.py          # 10 tests (100 lines)
├── integration/
│   ├── __init__.py
│   └── test_add_command.py      # 15 tests (200 lines)
└── fixtures/
    ├── __init__.py
    └── sample_data.py           # Test data generators (50 lines)

pyproject.toml           # UV project configuration
uv.lock                  # Dependency lock file
.python-version          # Python 3.13 requirement
README.md                # Project documentation
```

**Structure Decision**: Single project structure selected (Option 1 from template). This is a CLI application with clear separation: `src/` for production code, `tests/` for test code. The structure mirrors constitution standards and supports future feature additions (update, delete, list, complete commands can be added to cli.py and storage.py without restructuring).

**Estimated Totals**:
- Production code: ~320 lines
- Test code: ~620 lines
- Test-to-code ratio: ~2:1 (comprehensive coverage)

---

## Implementation Approach

### Phase Breakdown

#### Phase 0: Research and Planning ✅ (Complete)

**Objective**: Resolve all technical unknowns and finalize design decisions.

**Activities**:
1. ✅ Research dataclass vs NamedTuple vs Pydantic → **Decision: dataclass**
2. ✅ Research storage strategies (list vs dict) → **Decision: TaskStorage with list**
3. ✅ Research CLI frameworks (argparse vs click vs typer) → **Decision: argparse**
4. ✅ Validate constitution compliance → **All 8 principles pass**

**Output**: ADRs documented in this plan.md

---

#### Phase 1: Environment Setup

**Objective**: Initialize Python project with UV, configure tooling.

**Tasks**:
1. Initialize UV project: `uv init`
2. Set Python version: `uv python pin 3.13`
3. Add dev dependencies: `uv add --dev pytest pytest-cov`
4. Configure pyproject.toml (test paths, coverage settings)
5. Create directory structure (src/, tests/)
6. Create empty `__init__.py` files

**Dependencies**: None (starting point)

**Validation**: `uv run pytest --version` succeeds

**Estimated Time**: 15 minutes

---

#### Phase 2: Data Model Implementation (TDD)

**Objective**: Implement Task dataclass with validation.

**Order**:
1. **RED**: Write `test_task_model.py` tests (all must fail)
   - Test valid task creation
   - Test invalid ID (negative, zero, non-integer)
   - Test invalid title (empty, too long, whitespace-only)
   - Test invalid description (too long)
   - Test invalid status (not "complete" or "incomplete")
   - Test default values
   - Test boundary conditions (100 char title, 500 char description)

2. **GREEN**: Implement `models.py`
   - Create Task dataclass
   - Implement `__post_init__` validation
   - Raise ValueError with clear messages

3. **REFACTOR**: Clean up, add docstrings, type hints

**Dependencies**: Phase 1 complete

**Validation**: `uv run pytest tests/unit/test_task_model.py -v` all pass, coverage >90%

**Estimated Time**: 1 hour

---

#### Phase 3: Validation Layer Implementation (TDD)

**Objective**: Implement input validation functions.

**Order**:
1. **RED**: Write `test_validators.py` tests (all must fail)
   - Test validate_title: valid cases (1 char, 50 chars, 100 chars)
   - Test validate_title: invalid cases (empty, whitespace, 101 chars)
   - Test validate_title: trimming behavior
   - Test validate_title: Unicode characters
   - Test validate_description: valid cases (None, empty, 250 chars, 500 chars)
   - Test validate_description: invalid cases (501 chars)
   - Test validate_description: preserves whitespace

2. **GREEN**: Implement `validators.py`
   - Implement validate_title()
   - Implement validate_description()
   - Return (bool, str) tuples

3. **REFACTOR**: Extract constants (MAX_TITLE_LEN = 100, MAX_DESC_LEN = 500)

**Dependencies**: Phase 2 complete (uses Task model in some tests)

**Validation**: `uv run pytest tests/unit/test_validators.py -v` all pass, coverage 100%

**Estimated Time**: 45 minutes

---

#### Phase 4: Storage Layer Implementation (TDD)

**Objective**: Implement TaskStorage class with ID generation.

**Order**:
1. **RED**: Write `test_storage.py` tests (all must fail)
   - Test storage initialization (empty, ID starts at 1)
   - Test add() creates task with correct ID
   - Test add() increments ID sequentially
   - Test add() stores task in list
   - Test add() with title only
   - Test add() with title and description
   - Test get() retrieves task by ID
   - Test get() returns None for non-existent ID
   - Test exists() returns True/False correctly
   - Test count() returns correct total
   - Test list_all() returns all tasks
   - Test list_all() returns copy (mutations don't affect storage)

2. **GREEN**: Implement `storage.py`
   - Create TaskStorage class
   - Implement __init__, add, get, exists, count, list_all

3. **REFACTOR**: Consider edge cases, optimize get() if needed

**Dependencies**: Phase 2 and 3 complete (uses Task model and potentially validators)

**Validation**: `uv run pytest tests/unit/test_storage.py -v` all pass, coverage >95%

**Estimated Time**: 1.5 hours

---

#### Phase 5: CLI Layer Implementation (TDD)

**Objective**: Implement CLI parsing and command handling.

**Order**:
1. **RED**: Write `test_add_command.py` integration tests (all must fail)
   - Test successful add with title only
   - Test successful add with title and description
   - Test error: empty title
   - Test error: title too long (101 chars)
   - Test error: description too long (501 chars)
   - Test error: whitespace-only title
   - Test success message format
   - Test error message format
   - Test output channels (stdout for success, stderr for errors)
   - Test exit codes (0 for success, 1 for errors)
   - Test Unicode support
   - Test multi-line description (newlines preserved)
   - Test boundary conditions (100 char title, 500 char description)

2. **GREEN**: Implement `cli.py`
   - Implement create_parser()
   - Implement handle_add_command()
   - Implement format_success_message()
   - Implement format_error_message()

3. **REFACTOR**: Extract constants, improve readability

**Dependencies**: Phases 2, 3, 4 complete (uses all previous components)

**Validation**: `uv run pytest tests/integration/test_add_command.py -v` all pass, coverage >90%

**Estimated Time**: 2 hours

---

#### Phase 6: Main Entry Point Implementation

**Objective**: Wire all components together in main.py.

**Order**:
1. **GREEN**: Implement `main.py` (no separate tests, covered by integration tests)
   - Create main() function
   - Instantiate TaskStorage
   - Create parser
   - Parse arguments
   - Route to handle_add_command
   - Return exit code

2. **MANUAL TEST**: Run actual CLI commands
   - `uv run python src/main.py add "Buy milk"`
   - `uv run python src/main.py add "Review PR" --description "Check tests"`
   - Test error cases manually

**Dependencies**: Phase 5 complete

**Validation**: Manual CLI execution succeeds, integration tests pass

**Estimated Time**: 30 minutes

---

#### Phase 7: Coverage and Quality Gates

**Objective**: Validate coverage, run linters, ensure constitution compliance.

**Tasks**:
1. Run full test suite with coverage: `uv run pytest --cov=src --cov-report=html --cov-report=term`
2. Verify coverage ≥90% (target) or ≥80% (minimum)
3. Run type checker: `uv run mypy src/ --strict`
4. Run linter: `uv run ruff check src/ tests/`
5. Run formatter: `uv run black src/ tests/ --check`
6. Fix any issues found
7. Re-run all tests

**Dependencies**: Phase 6 complete

**Validation**:
- Coverage ≥90%
- mypy 0 errors
- ruff 0 violations
- black formatting compliant

**Estimated Time**: 1 hour

---

### Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Data Model)
    ↓
Phase 3 (Validators) ← depends on Task model
    ↓
Phase 4 (Storage) ← depends on Task model and validators
    ↓
Phase 5 (CLI) ← depends on all previous (Task, validators, storage)
    ↓
Phase 6 (Main) ← depends on CLI
    ↓
Phase 7 (Quality Gates) ← depends on all code
```

**Critical Path**: Sequential implementation due to dependencies. Cannot parallelize phases, but within each phase, tests can be written in any order.

---

## Testing Strategy

### Test Coverage Goals

- **Target**: 90%+ overall coverage
- **Minimum**: 80% (constitution requirement)
- **Measured with**: pytest-cov

### Test Categories

#### 1. Unit Tests - Data Model (test_task_model.py)

**Purpose**: Validate Task dataclass construction and validation.

**Test Cases** (15 tests):

1. `test_task_creation_with_all_fields` - Valid task with all fields
2. `test_task_creation_with_minimal_fields` - Valid task with required fields only
3. `test_task_default_status_is_incomplete` - Status defaults to "incomplete"
4. `test_task_invalid_id_negative` - ID < 1 raises ValueError
5. `test_task_invalid_id_zero` - ID = 0 raises ValueError
6. `test_task_invalid_title_empty` - Empty title raises ValueError
7. `test_task_invalid_title_whitespace_only` - "   " raises ValueError
8. `test_task_invalid_title_too_long` - 101+ chars raises ValueError
9. `test_task_valid_title_boundary_100_chars` - Exactly 100 chars succeeds
10. `test_task_invalid_description_too_long` - 501+ chars raises ValueError
11. `test_task_valid_description_boundary_500_chars` - Exactly 500 chars succeeds
12. `test_task_valid_description_none` - None description succeeds
13. `test_task_invalid_status_unknown` - Status not "complete"/"incomplete" raises ValueError
14. `test_task_created_at_is_datetime` - created_at is datetime instance
15. `test_task_repr` - String representation includes key fields

**Coverage Target**: 100% of models.py

---

#### 2. Unit Tests - Validators (test_validators.py)

**Purpose**: Validate input validation functions.

**Test Cases** (12 tests):

1. `test_validate_title_valid_1_char` - Title "A" is valid
2. `test_validate_title_valid_50_chars` - Title with 50 chars is valid
3. `test_validate_title_valid_100_chars` - Title with exactly 100 chars is valid
4. `test_validate_title_invalid_empty` - Empty title returns (False, "Title is required...")
5. `test_validate_title_invalid_whitespace_only` - "   " returns (False, "Title is required...")
6. `test_validate_title_invalid_101_chars` - 101 chars returns (False, "Title must be between...")
7. `test_validate_title_trimming` - "  Hello  " becomes "Hello" (5 chars, valid)
8. `test_validate_title_unicode` - "Café 中文" is valid
9. `test_validate_description_valid_none` - None returns (True, "")
10. `test_validate_description_valid_empty_string` - "" returns (True, "")
11. `test_validate_description_valid_500_chars` - 500 chars returns (True, "")
12. `test_validate_description_invalid_501_chars` - 501 chars returns (False, "Description cannot exceed...")

**Coverage Target**: 100% of validators.py

---

#### 3. Unit Tests - Storage (test_storage.py)

**Purpose**: Validate TaskStorage class behavior.

**Test Cases** (10 tests):

1. `test_storage_initialization` - Empty storage, count=0, next_id=1
2. `test_add_task_title_only` - add("Task") creates task with ID 1
3. `test_add_task_title_and_description` - add("Task", "Desc") creates task with both fields
4. `test_add_task_increments_id` - Adding 3 tasks yields IDs 1, 2, 3
5. `test_get_existing_task` - get(1) returns task with ID 1
6. `test_get_non_existent_task` - get(999) returns None
7. `test_exists_returns_true_for_existing` - exists(1) returns True
8. `test_exists_returns_false_for_non_existent` - exists(999) returns False
9. `test_count_returns_correct_total` - count() returns 3 after adding 3 tasks
10. `test_list_all_returns_copy` - Modifying returned list doesn't affect storage

**Coverage Target**: 100% of storage.py

---

#### 4. Integration Tests - CLI (test_add_command.py)

**Purpose**: Validate full CLI workflow end-to-end.

**Test Cases** (15 tests):

1. `test_add_command_success_title_only` - `add "Task"` succeeds, prints success, exit 0
2. `test_add_command_success_title_and_description` - `add "Task" --description "Desc"` succeeds
3. `test_add_command_success_message_format` - Success message includes ID, title, description, status
4. `test_add_command_empty_title_error` - `add ""` prints error to stderr, exit 1
5. `test_add_command_whitespace_only_title_error` - `add "   "` prints error to stderr, exit 1
6. `test_add_command_title_too_long_error` - `add "<101 chars>"` prints error to stderr, exit 1
7. `test_add_command_description_too_long_error` - `add "Task" --description "<501 chars>"` error
8. `test_add_command_title_boundary_100_chars_success` - `add "<100 chars>"` succeeds
9. `test_add_command_description_boundary_500_chars_success` - `add "Task" --description "<500 chars>"` succeeds
10. `test_add_command_unicode_title` - `add "Café 中文"` succeeds
11. `test_add_command_unicode_description` - `add "Task" --description "中文 描述"` succeeds
12. `test_add_command_multiline_description` - `add "Task" --description "Line1\nLine2"` preserves newlines
13. `test_add_command_sequential_ids` - Adding 3 tasks yields IDs 1, 2, 3 in success messages
14. `test_add_command_duplicate_titles_allowed` - Adding "Task" twice succeeds with different IDs
15. `test_add_command_output_channels` - Success to stdout, errors to stderr

**Test Helpers**:
- `run_cli(args: list[str]) -> tuple[int, str, str]`: Executes CLI, returns (exit_code, stdout, stderr)
- `create_long_string(length: int) -> str`: Generates strings of exact length for boundary tests

**Coverage Target**: >90% of cli.py and main.py

---

### Test Data (fixtures/sample_data.py)

**Purpose**: Provide reusable test data generators.

**Functions**:
- `valid_task_data() -> dict`: Returns valid Task constructor args
- `valid_title() -> str`: Returns valid 20-char title
- `long_title(length: int) -> str`: Returns title of exact length
- `long_description(length: int) -> str`: Returns description of exact length
- `unicode_title() -> str`: Returns title with Unicode characters

---

### Expected Coverage Report

**After Full Implementation**:

```
Name                Stmts   Miss  Cover
---------------------------------------
src/__init__.py         0      0   100%
src/models.py          30      1    97%
src/validators.py      20      0   100%
src/storage.py         40      2    95%
src/cli.py             60      3    95%
src/main.py            15      1    93%
---------------------------------------
TOTAL                 165      7    96%
```

**Exceeds**: 96% > 90% target > 80% minimum ✅

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected.** All 8 constitutional principles pass. No complexity justification required.

---

## Next Steps

### After Planning (Current Stage)

1. **Review this plan** with stakeholders for approval
2. **Run `/sp.tasks`** to generate tasks.md from this plan
3. **Begin Phase 1** (Environment Setup) per Implementation Approach

### After Implementation

1. **Manual Testing**: Execute CLI commands manually to verify UX
2. **Documentation**: Update README with usage examples
3. **Demo**: Show working `todo add` command to user
4. **Prepare for next feature**: Update, delete, list, complete commands

---

## Open Questions / Decisions Deferred

**None.** All clarifications resolved in spec clarification session (2025-12-28).

---

## References

- **Feature Spec**: [spec.md](./spec.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Clarifications**: See spec.md § Clarifications § Session 2025-12-28
- **Python dataclasses**: https://docs.python.org/3/library/dataclasses.html
- **argparse**: https://docs.python.org/3/library/argparse.html
- **pytest**: https://docs.pytest.org/
- **pytest-cov**: https://pytest-cov.readthedocs.io/

---

**Plan Status**: ✅ Complete - Ready for `/sp.tasks`
