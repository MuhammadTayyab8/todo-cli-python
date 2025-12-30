# Tasks: View Tasks

**Input**: Design documents from `/specs/003-view-task/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete)

**Tests**: TDD approach mandated by spec - tests MUST be written first and fail before implementation (Red-Green-Refactor). 80%+ coverage required.

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Exact file paths included in descriptions

## Path Conventions

- **Source**: `src/` at repository root
- **Tests**: `tests/unit/`, `tests/integration/`

---

## Phase 1: Setup

**Purpose**: Project initialization - extend existing infrastructure for list feature

- [x] T001 Verify existing project structure supports list feature extension in `src/`
- [x] T002 [P] Create `tests/unit/test_storage_list.py` file structure
- [x] T003 [P] Create `tests/integration/test_list_command.py` file structure

**Checkpoint**: Test files scaffolded, ready for TDD workflow

---

## Phase 2: Foundational (Storage Layer - TDD)

**Purpose**: Add list_tasks() method to TaskStorage - BLOCKS all user story implementations

**Goal**: Implement `TaskStorage.list_tasks()` method with TDD

**Independent Test**: `uv run pytest tests/unit/test_storage_list.py -v` all pass

### Tests for Storage Layer (RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] Write test `test_list_empty_storage_returns_empty` in `tests/unit/test_storage_list.py`
- [x] T005 [P] Write test `test_list_single_task` in `tests/unit/test_storage_list.py`
- [x] T006 [P] Write test `test_list_multiple_tasks` in `tests/unit/test_storage_list.py`
- [x] T007 [P] Write test `test_list_incomplete_task_status_symbol` in `tests/unit/test_storage_list.py`
- [x] T008 [P] Write test `test_list_complete_task_status_symbol` in `tests/unit/test_storage_list.py`
- [x] T009 [P] Write test `test_list_preserves_id_order` in `tests/unit/test_storage_list.py`
- [x] T010 [P] Write test `test_list_includes_title` in `tests/unit/test_storage_list.py`
- [x] T011 [P] Write test `test_list_includes_description` in `tests/unit/test_storage_list.py`
- [x] T012 Verify all storage tests FAIL (RED) - run `uv run pytest tests/unit/test_storage_list.py -v`

### Implementation for Storage Layer (GREEN Phase)

- [x] T013 Add `list_tasks(self) -> list[str]` method to `src/storage.py`
- [x] T014 Return list of formatted task strings using existing `list_all()` in `src/storage.py`
- [x] T015 Format each task with `[ID] SYMBOL Title\n    Description` pattern in `src/storage.py`
- [x] T016 Add Google-style docstring to list_tasks() method in `src/storage.py`
- [x] T017 Verify all storage tests PASS (GREEN) - run `uv run pytest tests/unit/test_storage_list.py -v`

**Checkpoint**: Storage layer complete - `TaskStorage.list_tasks()` works correctly

---

## Phase 3: User Story 1 - List All Tasks (Priority: P1)

**Goal**: User can list all tasks with details - the core list functionality

**Independent Test**: Create tasks, run list, verify all tasks displayed with correct format

### Tests for User Story 1 (RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T018 [P] [US1] Write test `test_list_empty_shows_no_tasks_message` in `tests/integration/test_list_command.py`
- [x] T019 [P] [US1] Write test `test_list_single_task` in `tests/integration/test_list_command.py`
- [x] T020 [P] [US1] Write test `test_list_multiple_tasks` in `tests/integration/test_list_command.py`
- [x] T021 [P] [US1] Write test `test_list_multiple_tasks_display_order` in `tests/integration/test_list_command.py`
- [x] T022 [P] [US1] Write test `test_list_header_format` in `tests/integration/test_list_command.py`
- [x] T023 [P] [US1] Write test `test_list_divider_present` in `tests/integration/test_list_command.py`
- [x] T024 [P] [US1] Write test `test_list_exit_code_0` in `tests/integration/test_list_command.py`

### Implementation for User Story 1 (GREEN Phase)

- [x] T025 [US1] Add 'list' subparser to `create_parser()` in `src/cli.py`
- [x] T026 [US1] Create `handle_list_command(args, storage) -> int` function in `src/cli.py`
- [x] T027 [US1] Add routing for 'list' command in `main.py`
- [x] T028 [US1] Verify User Story 1 tests PASS - run `uv run pytest tests/integration/test_list_command.py -v`

**Checkpoint**: User Story 1 complete - `python main.py list` works with tasks

---

## Phase 4: User Story 2 - Read Task Details (Priority: P2)

**Goal**: Tasks display with clear, readable formatting including title and description

**Independent Test**: Create tasks with various descriptions, verify formatting is readable

### Tests for User Story 2 (RED Phase)

- [x] T029 [P] [US2] Write test `test_list_none_description_shows_none` in `tests/integration/test_list_command.py`
- [x] T030 [P] [US2] Write test `test_list_title_100_chars` in `tests/integration/test_list_command.py`
- [x] T031 [P] [US2] Write test `test_list_description_500_chars` in `tests/integration/test_list_command.py`

### Implementation for User Story 2 (GREEN Phase)

- [x] T032 [US2] Implement `format_task_display(task: Task) -> str` in `src/cli.py` (already implemented in storage.list_tasks())
- [x] T033 [US2] Handle None description by showing "(none)" in `src/cli.py` (already implemented)
- [x] T034 [US2] Add Google-style docstrings to formatting functions in `src/cli.py` (already done)
- [x] T035 [US2] Verify User Story 2 tests PASS - run `uv run pytest tests/integration/test_list_command.py -v "description or chars"`

**Checkpoint**: User Story 2 complete - task details display clearly

---

## Phase 5: User Story 3 - Identify Task Status (Priority: P2)

**Goal**: Users can distinguish complete from incomplete tasks via status symbols

**Independent Test**: Create complete and incomplete tasks, verify correct ✓/✗ symbols

### Tests for User Story 3 (RED Phase)

- [x] T036 [P] [US3] Write test `test_list_incomplete_status_symbol` in `tests/integration/test_list_command.py`
- [x] T037 [P] [US3] Write test `test_list_complete_status_symbol` in `tests/integration/test_list_command.py`
- [x] T038 [P] [US3] Write test `test_list_summary_counts_completed` in `tests/integration/test_list_command.py`
- [x] T039 [P] [US3] Write test `test_list_summary_counts_pending` in `tests/integration/test_list_command.py`
- [x] T040 [P] [US3] Write test `test_list_singular_task` in `tests/integration/test_list_command.py`

### Implementation for User Story 3 (GREEN Phase)

- [x] T041 [US3] Implement status symbol helper `get_status_symbol(status: str) -> str` in `src/cli.py` (already in storage.list_tasks())
- [x] T042 [US3] Implement `format_summary(tasks: list[Task]) -> str` in `src/cli.py`
- [x] T043 [US3] Handle singular/plural "task"/"tasks" in summary in `src/cli.py`
- [x] T044 [US3] Verify User Story 3 tests PASS - run `uv run pytest tests/integration/test_list_command.py -v "status or summary"`

**Checkpoint**: User Story 3 complete - status symbols and summary work correctly

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, documentation, and final validation

### Quality Gates

- [x] T045 Run full test suite: `uv run pytest --cov=src --cov-report=term`
- [x] T046 Verify coverage >= 80% for list-related code
- [x] T047 Run type checker: `uv run mypy src/ --strict` (fix any errors)
- [x] T048 Run linter: `uv run ruff check src/ tests/` (fix any violations)
- [x] T049 [P] Run formatter: `uv run black src/ tests/ --check` (fix any formatting issues)

### Documentation

- [x] T050 [P] Update README.md with list command usage examples
- [x] T051 [P] Verify all docstrings are Google-style in modified files

### Final Validation

- [x] T052 Run quickstart.md validation - execute all CLI examples manually
- [x] T053 Verify all 3 user story acceptance scenarios pass (per spec.md)

**Checkpoint**: Feature complete - ready for merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational/Storage)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3-5 (User Stories)**: All depend on Phase 2 completion
  - US1 (P1): Can start after Phase 2
  - US2 (P2): Can start after Phase 2 (parallel with US1 or after)
  - US3 (P2): Can start after Phase 2 (parallel with US1/US2)
- **Phase 6 (Polish)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation only - No dependencies on other stories
- **User Story 2 (P2)**: Foundation only - No dependencies on other stories
- **User Story 3 (P2)**: Foundation only - No dependencies on other stories

### Within Each Phase

- Tests (RED) MUST be written and FAIL before implementation (GREEN)
- Implementation tasks should follow order: storage → formatting → routing
- Verify tests pass after each implementation task

### Parallel Opportunities

Within Phase 1 (Setup):
- T002, T003 can run in parallel (different test files)

Within Phase 2 (Storage Tests):
- T004-T011 can ALL run in parallel (same file, different test functions)

Within Phase 3 (US1 Tests):
- T018-T024 can ALL run in parallel

Within Phase 4 (US2 Tests):
- T029-T031 can ALL run in parallel

Within Phase 5 (US3 Tests):
- T036-T040 can ALL run in parallel

Within Phase 6 (Polish):
- T050-T051 can run in parallel (different concerns)

---

## Parallel Example: Storage Layer Tests

```bash
# Launch all storage unit tests in parallel (Phase 2, RED):
Task: "Write test test_list_empty_storage_returns_empty in tests/unit/test_storage_list.py"
Task: "Write test test_list_single_task in tests/unit/test_storage_list.py"
Task: "Write test test_list_multiple_tasks in tests/unit/test_storage_list.py"
# ... (all T004-T011 can run together)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Storage Layer with TDD (T004-T017)
3. Complete Phase 3: User Story 1 (T018-T028)
4. **STOP and VALIDATE**: Test `python main.py list` works
5. Demo if ready (MVP delivered!)

### Incremental Delivery

1. Setup + Storage → Foundation ready
2. Add User Story 1 (list all tasks) → Demo basic list
3. Add User Story 2 (readable details) → Demo formatted output
4. Add User Story 3 (status symbols) → Demo complete feature
5. Polish → Feature complete

---

## Summary

| Phase | Task Range | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| Phase 1: Setup | T001-T003 | 3 | 2 |
| Phase 2: Storage (TDD) | T004-T017 | 14 | 8 |
| Phase 3: US1 List (TDD) | T018-T028 | 11 | 7 |
| Phase 4: US2 Details (TDD) | T029-T035 | 7 | 3 |
| Phase 5: US3 Status (TDD) | T036-T044 | 9 | 5 |
| Phase 6: Polish | T045-T053 | 9 | 2 |
| **TOTAL** | T001-T053 | **53** | **27** |

**Tasks per User Story**:
- US1 (List All Tasks): 11 tasks
- US2 (Read Details): 7 tasks
- US3 (Identify Status): 9 tasks

**MVP Scope**: Phase 1-3 (28 tasks) delivers working list command

---

## Notes

- All tasks follow TDD: RED (tests fail) → GREEN (tests pass) → REFACTOR
- No validators needed for list command (no user input)
- No changes to Task model (already exists)
- Error messages not needed - list always succeeds (even empty)
- 80%+ test coverage required (per constitution)
