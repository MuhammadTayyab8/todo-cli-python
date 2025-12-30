# Implementation Plan: Mark Todo Task Complete/Incomplete

**Feature Branch**: `1-todo-toggle-status`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Create implementation plan for Mark Complete feature. Architectural Decisions: Single 'complete' command with toggle behavior. Component Design: storage.py (add toggle_complete), cli.py (add complete subcommand). Testing Strategy: test toggle status, non-existent ID."

## Technical Context

- **Dependency**: `TaskStorage` in `storage.py` (responsible for task persistence/state).
- **Dependency**: `create_parser` and handlers in `cli.py` (responsible for CLI interaction).
- **Unknowns**: None identified. The existing architecture is clear and modular.

## Constitution Check

- [ ] **Python 3.13+ with Type Hints**: Mandatory for new methods.
- [ ] **In-Memory Storage Only**: The existing `TaskStorage` uses `tasks.json` as a mock persistence layer; I will maintain this pattern unless instructed otherwise, but strictly speaking, the constitution states "In-Memory Storage Only".
- [ ] **Test-Driven Development**: I will write failing tests for storage and CLI before implementation.
- [ ] **Test Coverage Minimum 80%**: New feature must maintain high coverage.
- [ ] **Zero External Runtime Dependencies**: No new libraries will be used.
- [ ] **Clean Code and SOLID**: `TaskStorage` handle state, `cli.py` handles user interaction.

## Phase 0: Research

### research.md

- **Decision**: Implement a single `complete` command that toggles status.
- **Rationale**: User explicitly requested toggle behavior for a single command to simplify usage.
- **Implementation Note**: The `storage.py` already includes a `tasks.json` persistence mechanism. While the constitution says "In-Memory Only", the existing codebase uses JSON files. I will stick to the existing pattern for consistency but ensure the core logic remains decoupled.

## Phase 1: Design & Contracts

### data-model.md

- **Entity**: `Task` (existing)
- **State Transition**:
  - `incomplete` -> `complete`
  - `complete` -> `incomplete`
- **Validation**: Task ID must exist.

### contracts/cli-commands.md

- **Action**: Toggle Status
- **Input**: `task_id` (int)
- **Output (Success)**: Updated `Task` details with message "Task marked as [status] (ID: [id])"
- **Output (Error)**: "Error: Task not found (ID: [id])"

### Architectural Decisions

#### ADR-007: Completion Status Strategy

- **Decision**: Single `complete` command with toggle behavior.
- **Rationale**: Reduces cognitive load for the user. Instead of remembering `complete` and `incomplete`, a single command `complete` (or `toggle`) manages the state.
- **Alternative**: Separate `complete` and `incomplete` commands (more explicit but verbose).

## Implementation Approach

1.  **Storage Layer (`src/storage.py`)**:
    - Add `toggle_status(task_id: int) -> Task | None` to `TaskStorage`.
    - Retrieve task -> Switch status string -> Create updated `Task` (immutable dataclass pattern used in `update`) -> Save -> Return.

2.  **CLI Layer (`src/cli.py`)**:
    - Add `complete` subcommand to `create_parser`.
    - Add `handle_complete_command(args, storage)` handler.
    - Validate `task_id` using `validate_task_id`.
    - Implement `format_toggle_success_message(task)`.

3.  **App Routing (`src/main.py`)**:
    - Route `complete` command to `handle_complete_command`.

## Testing Strategy

### Unit Tests (`tests/unit/test_storage_toggle.py`)
- `test_toggle_incomplete_to_complete`: Task 1 (incomplete) -> Toggle -> Task 1 (complete).
- `test_toggle_complete_to_incomplete`: Task 1 (complete) -> Toggle -> Task 1 (incomplete).
- `test_toggle_non_existent`: Non-existent ID -> returns `None`.

### Integration Tests (`tests/integration/test_complete_command.py`)
- `test_complete_command_success`: Full CLI execution resulting in success message and status change.
- `test_complete_command_toggle`: Running the command twice returns task to original state.
- `test_complete_command_invalid_id`: Error message for non-numeric ID.
- `test_complete_command_missing_id`: Error message for non-existent numeric ID.

## Complexity Tracking

- None currently identified. The change is a standard extension of the existing CRUD pattern.
