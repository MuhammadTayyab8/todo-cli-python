# Tasks: Mark Todo Task Complete/Incomplete

**Input**: Design documents from `specs/1-todo-toggle-status/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Tests**: Tests are MANDATORY as per Constitution Principle IV (TDD).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize feature branch and directories (Completed manually)

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T002 Research existing storage and CLI patterns (Completed in Phase 0/1)

## Phase 3: User Story 1 - Toggle Task Status (Priority: P1) 🎯 MVP

**Goal**: Implement the core toggle logic in storage and CLI.

**Independent Test**: Create a task, toggle it to "complete", then toggle it back to "incomplete" using the CLI.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T003 [P] [US1] Create unit tests for toggle status in `tests/unit/test_storage_toggle.py`
- [x] T004 [P] [US1] Create integration tests for complete command in `tests/integration/test_complete_command.py`

### Implementation for User Story 1

- [x] T005 [US1] Implement `toggle_status(task_id: int)` method in `src/storage.py`
- [x] T006 [US1] Implement `handle_complete_command(args, storage)` and success formatting in `src/cli.py`
- [x] T007 [US1] Add `complete` subcommand to `create_parser()` in `src/cli.py`
- [x] T008 [US1] Update `main()` to route the `complete` command in `src/main.py`

**Checkpoint**: Core toggle functionality is complete and passes all status transition tests.

---

## Phase 4: User Story 2 - Error Handling for Non-existent Tasks (Priority: P2)

**Goal**: Ensure robust error reporting for missing or invalid task IDs.

**Independent Test**: Run `todo complete 999` (non-existent) or `todo complete abc` (invalid) and verify error messages.

### Tests for User Story 2

- [x] T009 [P] [US2] Add unit test for non-existent ID toggle in `tests/unit/test_storage_toggle.py`
- [x] T010 [P] [US2] Add integration tests for missing and invalid IDs in `tests/integration/test_complete_command.py`

### Implementation for User Story 2

- [x] T011 [US2] Ensure `toggle_status` returns `None` for missing IDs in `src/storage.py`
- [x] T012 [US2] Implement error handling and formatting for non-existent/invalid IDs in `src/cli.py`

**Checkpoint**: Error handling is fully integrated and tested.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [x] T013 Update documentation
- [x] T014 Run full test suite to ensure no regressions in other commands
- [x] T015 Verify test coverage is ≥80% using `pytest-cov`

---

## Phase 6: Documentation

- [x] T016 Update README.md file with proper commands for this task


## Dependencies & Execution Order

- **User Story 1**: Foundation for the feature.
- **User Story 2**: Built on top of US1 to add robustness.

## Parallel Execution Examples

```bash
# Unit and Integration tests for US1 can be written in parallel
Task: "Create unit tests for toggle status in tests/unit/test_storage_toggle.py"
Task: "Create integration tests for complete command in tests/integration/test_complete_command.py"
```

## Implementation Strategy

1. **MVP**: Complete User Story 1 first.
2. **Robustness**: Complete User Story 2.
3. **Validation**: Run full suite and check coverage.
