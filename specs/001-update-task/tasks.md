# Tasks: Update Task

**Input**: Design documents from `/specs/001-update-task/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete)

**Tests**: TDD approach mandated by spec - tests MUST be written first and fail before implementation (Red-Green-Refactor). 80%+ coverage required.

**Organization**: Tasks organized by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Exact file paths included in descriptions

## Path Conventions

- **Source**: `src/` at repository root
- **Tests**: `tests/unit/`, `tests/integration/`

---

## Phase 1: Setup

**Purpose**: Project initialization - extend existing infrastructure for update feature

- [x] T001 Verify existing project structure supports update feature extension in `src/`
- [x] T002 [P] Create `tests/unit/test_storage_update.py` file structure
- [x] T003 [P] Create `tests/integration/test_update_command.py` file structure

**Checkpoint**: Test files scaffolded, ready for TDD workflow

---

## Phase 2: Foundational (Storage Layer - TDD)

**Purpose**: Add update() method to TaskStorage - BLOCKS all user story implementations

**Goal**: Implement `TaskStorage.update()` method with TDD

**Independent Test**: `uv run pytest tests/unit/test_storage_update.py -v` all pass

### Tests for Storage Layer (RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T004 [P] Write test `test_update_title_only_preserves_description` in `tests/unit/test_storage_update.py`
- [x] T005 [P] Write test `test_update_description_only_preserves_title` in `tests/unit/test_storage_update.py`
- [x] T006 [P] Write test `test_update_both_title_and_description` in `tests/unit/test_storage_update.py`
- [x] T007 [P] Write test `test_update_non_existent_task_returns_none` in `tests/unit/test_storage_update.py`
- [x] T008 [P] Write test `test_update_empty_storage_returns_none` in `tests/unit/test_storage_update.py`
- [x] T009 [P] Write test `test_update_preserves_incomplete_status` in `tests/unit/test_storage_update.py`
- [x] T010 [P] Write test `test_update_preserves_complete_status` in `tests/unit/test_storage_update.py`
- [x] T011 [P] Write test `test_update_preserves_created_at` in `tests/unit/test_storage_update.py`
- [x] T012 [P] Write test `test_update_with_empty_description_clears_it` in `tests/unit/test_storage_update.py`
- [x] T013 [P] Write test `test_update_does_not_affect_other_tasks` in `tests/unit/test_storage_update.py`
- [x] T014 [P] Write test `test_update_returns_updated_task` in `tests/unit/test_storage_update.py`
- [x] T015 [P] Write test `test_update_strips_title_whitespace` in `tests/unit/test_storage_update.py`
- [x] T016 [P] Write test `test_update_preserves_description_whitespace` in `tests/unit/test_storage_update.py`
- [x] T017 Verify all storage tests FAIL (RED) - run `uv run pytest tests/unit/test_storage_update.py -v`

### Implementation for Storage Layer (GREEN Phase)

- [x] T018 Add `update(task_id: int, title: str | None = None, description: str | None = None) -> Task | None` method to `src/storage.py`
- [x] T019 Implement ID lookup logic (linear search through `_tasks` list) in `src/storage.py`
- [x] T020 Handle optional parameters (None = no change, value = replace) in `src/storage.py`
- [x] T021 Create new Task instance with updated values preserving id, status, created_at in `src/storage.py`
- [x] T022 Add Google-style docstring to update() method in `src/storage.py`
- [x] T023 Verify all storage tests PASS (GREEN) - run `uv run pytest tests/unit/test_storage_update.py -v`

**Checkpoint**: Storage layer complete - `TaskStorage.update()` works correctly

---

## Phase 3: User Story 1 - Update Task Title Only (Priority: P1)

**Goal**: User can update only the title of an existing task via `--title` argument

**Independent Test**: Create task, update only title, verify title changed and description preserved

### Tests for User Story 1 (RED Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T024 [P] [US1] Write test `test_update_title_only_success` in `tests/integration/test_update_command.py`
- [x] T025 [P] [US1] Write test `test_update_title_success_message_format` in `tests/integration/test_update_command.py`
- [x] T026 [P] [US1] Write test `test_update_title_success_to_stdout` in `tests/integration/test_update_command.py`
- [x] T027 [P] [US1] Write test `test_update_title_exit_code_0` in `tests/integration/test_update_command.py`
- [x] T028 [P] [US1] Write test `test_update_title_preserves_incomplete_status` in `tests/integration/test_update_command.py`
- [x] T029 [P] [US1] Write test `test_update_title_preserves_complete_status` in `tests/integration/test_update_command.py`
- [x] T030 [P] [US1] Write test `test_update_title_unicode_support` in `tests/integration/test_update_command.py`
- [x] T031 [P] [US1] Write test `test_update_title_boundary_100_chars` in `tests/integration/test_update_command.py`

### Implementation for User Story 1 (GREEN Phase)

- [x] T032 [US1] Add 'update' subparser to `create_parser()` in `src/cli.py`
- [x] T033 [US1] Add task_id positional argument (type=str) to update subparser in `src/cli.py`
- [x] T034 [US1] Add --title optional argument (default=None) to update subparser in `src/cli.py`
- [x] T035 [US1] Create `handle_update_command(args, storage) -> int` function in `src/cli.py`
- [x] T036 [US1] Implement task_id validation using existing `validate_task_id()` in `src/cli.py`
- [x] T037 [US1] Implement title validation using existing `validate_title()` in `src/cli.py`
- [x] T038 [US1] Call `storage.update()` and format success message in `src/cli.py`
- [x] T039 [US1] Add routing for 'update' command in `main.py`
- [x] T040 [US1] Verify User Story 1 tests PASS - run `uv run pytest tests/integration/test_update_command.py -k "title" -v`

**Checkpoint**: User Story 1 complete - `python main.py update <id> --title "text"` works

---

## Phase 4: User Story 2 - Update Task Description Only (Priority: P2)

**Goal**: User can update only the description of an existing task via `--desc` argument

**Independent Test**: Create task, update only description, verify description changed and title preserved

### Tests for User Story 2 (RED Phase)

- [x] T041 [P] [US2] Write test `test_update_description_only_success` in `tests/integration/test_update_command.py`
- [x] T042 [P] [US2] Write test `test_update_description_adds_to_empty` in `tests/integration/test_update_command.py`
- [x] T043 [P] [US2] Write test `test_update_description_clears_with_empty_string` in `tests/integration/test_update_command.py`
- [x] T044 [P] [US2] Write test `test_update_description_boundary_500_chars` in `tests/integration/test_update_command.py`
- [x] T045 [P] [US2] Write test `test_update_description_unicode_support` in `tests/integration/test_update_command.py`

### Implementation for User Story 2 (GREEN Phase)

- [x] T046 [US2] Add --desc optional argument (default=None) to update subparser in `src/cli.py`
- [x] T047 [US2] Add check for at least one of --title or --desc provided in `src/cli.py`
- [x] T048 [US2] Implement description validation using existing `validate_description()` in `src/cli.py`
- [x] T049 [US2] Update success message to display description (or "(none)" if empty) in `src/cli.py`
- [x] T050 [US2] Verify User Story 2 tests PASS - run `uv run pytest tests/integration/test_update_command.py -k "description" -v`

**Checkpoint**: User Story 2 complete - `python main.py update <id> --desc "text"` works

---

## Phase 5: User Story 3 - Update Both Title and Description (Priority: P2)

**Goal**: User can update both title and description simultaneously

**Independent Test**: Create task, update both fields, verify both changed

### Tests for User Story 3 (RED Phase)

- [x] T051 [P] [US3] Write test `test_update_both_title_and_description_success` in `tests/integration/test_update_command.py`
- [x] T052 [P] [US3] Write test `test_update_both_adds_description_to_empty` in `tests/integration/test_update_command.py`
- [x] T053 [P] [US3] Write test `test_update_both_success_message_format` in `tests/integration/test_update_command.py`

### Implementation for User Story 3 (GREEN Phase)

- [x] T054 [US3] Ensure handle_update_command supports both --title and --desc together in `src/cli.py`
- [x] T055 [US3] Verify User Story 3 tests PASS - run `uv run pytest tests/integration/test_update_command.py -k "both" -v`

**Checkpoint**: User Story 3 complete - `python main.py update <id> --title "text" --desc "text"` works

---

## Phase 6: User Story 4 - Error Handling for Non-Existent Tasks (Priority: P3)

**Goal**: User receives clear error messages for invalid operations

**Independent Test**: Attempt update with non-existent ID, verify error message and exit code

### Tests for User Story 4 (RED Phase)

- [x] T056 [P] [US4] Write test `test_update_non_existent_id_error` in `tests/integration/test_update_command.py`
- [x] T057 [P] [US4] Write test `test_update_invalid_id_non_numeric_error` in `tests/integration/test_update_command.py`
- [x] T058 [P] [US4] Write test `test_update_invalid_id_negative_error` in `tests/integration/test_update_command.py`
- [x] T059 [P] [US4] Write test `test_update_invalid_id_zero_error` in `tests/integration/test_update_command.py`
- [x] T060 [P] [US4] Write test `test_update_no_args_error` in `tests/integration/test_update_command.py`
- [x] T061 [P] [US4] Write test `test_update_empty_title_error` in `tests/integration/test_update_command.py`
- [x] T062 [P] [US4] Write test `test_update_whitespace_title_error` in `tests/integration/test_update_command.py`
- [x] T063 [P] [US4] Write test `test_update_title_too_long_error` in `tests/integration/test_update_command.py`
- [x] T064 [P] [US4] Write test `test_update_description_too_long_error` in `tests/integration/test_update_command.py`
- [x] T065 [P] [US4] Write test `test_update_error_to_stderr` in `tests/integration/test_update_command.py`
- [x] T066 [P] [US4] Write test `test_update_error_exit_code_1` in `tests/integration/test_update_command.py`

### Implementation for User Story 4 (GREEN Phase)

- [x] T067 [US4] Add error message "Error: Task not found (ID: {id})" when update returns None in `src/cli.py`
- [x] T068 [US4] Add error message "Error: At least one of --title or --desc must be provided" in `src/cli.py`
- [x] T069 [US4] Ensure all error messages go to stderr with exit code 1 in `src/cli.py`
- [x] T070 [US4] Add Google-style docstring to handle_update_command() in `src/cli.py`
- [x] T071 [US4] Verify User Story 4 tests PASS - run `uv run pytest tests/integration/test_update_command.py -k "error" -v`

**Checkpoint**: User Story 4 complete - all error scenarios handled correctly

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Quality gates, documentation, and final validation

### Quality Gates

- [ ] T072 Run full test suite: `uv run pytest --cov=src --cov-report=term`
- [ ] T073 Verify coverage >= 80% for update-related code
- [ ] T074 Run type checker: `uv run mypy src/ --strict` (fix any errors)
- [ ] T075 Run linter: `uv run ruff check src/ tests/` (fix any violations)
- [ ] T076 [P] Run formatter: `uv run black src/ tests/ --check` (fix any formatting issues)

### Documentation

- [ ] T077 [P] Update README.md with update command usage examples
- [ ] T078 [P] Verify all docstrings are Google-style in modified files
- [ ] T079 Create ADR-005: Update Operation Strategy in `history/adr/ADR-005-update-operation-strategy.md`

### Final Validation

- [ ] T080 Run quickstart.md validation - execute all CLI examples manually
- [ ] T081 Verify all 4 user story acceptance scenarios pass (per spec.md)

**Checkpoint**: Feature complete - ready for merge

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational/Storage)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3-6 (User Stories)**: All depend on Phase 2 completion
  - US1 (P1): Can start after Phase 2
  - US2 (P2): Can start after Phase 2 (parallel with US1 or after)
  - US3 (P2): Depends on US1 and US2 implementations being complete
  - US4 (P3): Can start after Phase 2 (parallel with others)
- **Phase 7 (Polish)**: Depends on all user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation only - No dependencies on other stories
- **User Story 2 (P2)**: Foundation only - No dependencies on other stories
- **User Story 3 (P2)**: Builds on US1 + US2 (requires both --title and --desc to exist)
- **User Story 4 (P3)**: Foundation only - Error handling independent of success paths

### Within Each Phase

- Tests (RED) MUST be written and FAIL before implementation (GREEN)
- Implementation tasks should follow order: validation → storage → formatting
- Verify tests pass after each implementation task

### Parallel Opportunities

Within Phase 1 (Setup):
- T002, T003 can run in parallel (different test files)

Within Phase 2 (Storage Tests):
- T004-T016 can ALL run in parallel (same file, different test functions)

Within Phase 3 (US1 Tests):
- T024-T031 can ALL run in parallel

Within Phase 4 (US2 Tests):
- T041-T045 can ALL run in parallel

Within Phase 5 (US3 Tests):
- T051-T053 can ALL run in parallel

Within Phase 6 (US4 Tests):
- T056-T066 can ALL run in parallel

Within Phase 7 (Polish):
- T076-T078 can run in parallel (different concerns)

---

## Parallel Example: Storage Layer Tests

```bash
# Launch all storage unit tests in parallel (Phase 2, RED):
Task: "Write test test_update_title_only_preserves_description in tests/unit/test_storage_update.py"
Task: "Write test test_update_description_only_preserves_title in tests/unit/test_storage_update.py"
Task: "Write test test_update_both_title_and_description in tests/unit/test_storage_update.py"
Task: "Write test test_update_non_existent_task_returns_none in tests/unit/test_storage_update.py"
# ... (all T004-T016 can run together)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Storage Layer with TDD (T004-T023)
3. Complete Phase 3: User Story 1 - Title Update (T024-T040)
4. **STOP and VALIDATE**: Test `python main.py update 1 --title "New"` works
5. Demo if ready (MVP delivered!)

### Incremental Delivery

1. Setup + Storage → Foundation ready
2. Add User Story 1 (--title) → Demo MVP
3. Add User Story 2 (--desc) → Demo enhanced
4. Add User Story 3 (both) → Demo complete success path
5. Add User Story 4 (errors) → Demo robust error handling
6. Polish → Feature complete

---

## Summary

| Phase | Task Range | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| Phase 1: Setup | T001-T003 | 3 | 2 |
| Phase 2: Storage (TDD) | T004-T023 | 20 | 13 |
| Phase 3: US1 Title (TDD) | T024-T040 | 17 | 8 |
| Phase 4: US2 Description (TDD) | T041-T050 | 10 | 5 |
| Phase 5: US3 Both (TDD) | T051-T055 | 5 | 3 |
| Phase 6: US4 Errors (TDD) | T056-T071 | 16 | 11 |
| Phase 7: Polish | T072-T081 | 10 | 3 |
| **TOTAL** | T001-T081 | **81** | **45** |

**Tasks per User Story**:
- US1 (Title Only): 17 tasks
- US2 (Description Only): 10 tasks
- US3 (Both): 5 tasks
- US4 (Error Handling): 16 tasks

**MVP Scope**: Phase 1-3 (40 tasks) delivers working title-only update

---

## Notes

- All tasks follow TDD: RED (tests fail) → GREEN (tests pass) → REFACTOR
- Reuse existing validators from `src/validators.py`
- Error messages must match spec.md exactly
- Success messages must go to stdout, errors to stderr
- Exit code 0 for success, 1 for errors
- 80%+ test coverage required (per constitution)
