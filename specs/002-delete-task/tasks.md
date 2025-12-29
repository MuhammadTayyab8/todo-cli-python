# Task Breakdown: Delete Task

**Feature**: Delete Task by ID
**Branch**: `002-delete-task`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This feature implements task deletion functionality following strict Test-Driven Development (TDD) methodology. Tasks are organized by user story to enable independent implementation and testing. Each user story can be completed as a standalone increment, delivering value incrementally.

**Total Estimated Tasks**: 35
**Implementation Strategy**: Red-Green-Refactor cycle per user story
**Test Strategy**: Tests written FIRST (RED), then implementation (GREEN), then refactor

---

## Phase 1: Foundational (Blocking Prerequisites)

**Purpose**: TDD infrastructure and validation foundation needed by all user stories

**Prerequisites**: Add Task feature (001-add-task) fully implemented

### Unit Tests - Task ID Validation (RED Phase)

- [X] T001 [P] Create tests/unit/test_task_id_validation.py with 9 test cases for validate_task_id()
- [X] T002 [P] Write test_valid_task_id_1() - boundary test for ID = 1
- [X] T003 [P] Write test_valid_task_id_100() - typical valid ID
- [X] T004 [P] Write test_invalid_task_id_0() - boundary test for zero
- [X] T005 [P] Write test_invalid_task_id_negative_1() - negative boundary
- [X] T006 [P] Write test_invalid_task_id_negative_100() - negative typical
- [X] T007 [P] Write test_invalid_task_id_non_numeric() - test "abc" input
- [X] T008 [P] Write test_invalid_task_id_float() - test "1.5" input
- [X] T009 [P] Write test_invalid_task_id_empty_string() - test "" input
- [X] T010 [P] Write test_invalid_task_id_whitespace() - test "   " input

### Validation Implementation (GREEN Phase)

- [X] T011 Run pytest for test_task_id_validation.py and verify ALL 9 tests FAIL (RED confirmation)
- [X] T012 Implement validate_task_id() function in src/validators.py returning tuple[bool, str, int | None]
- [X] T013 Run pytest for test_task_id_validation.py and verify ALL 9 tests PASS (GREEN confirmation)

### Refactor Validation (REFACTOR Phase)

- [X] T014 Run mypy on src/validators.py and fix any type errors
- [X] T015 Run ruff check on src/validators.py and fix any linting issues
- [X] T016 Run black on src/validators.py to format code
- [X] T017 Verify validate_task_id() docstring follows Google style with Args, Returns, Examples

**Checkpoint**: All 9 validation tests passing, code quality checks pass, coverage for validators.py remains 100%

---

## Phase 2: User Story 1 - Delete Existing Task by ID (Priority: P1)

**User Story**: As a user, I want to delete a task by its ID so that I can remove tasks that are no longer needed or were created by mistake.

**Why this priority**: Core value proposition - minimum viable functionality

**Independent Test**: Create task, delete by ID, verify removed and success message displayed

**Acceptance Criteria**:
1. Given task with ID 1 exists, when I execute `todo delete 1`, then task removed and "Task deleted successfully (ID: 1)" displayed
2. Given tasks 1, 2, 3 exist, when I delete task 2, then only task 2 removed (1 and 3 remain)
3. Given task 5 deleted, when I attempt to retrieve task 5, then task confirmed not found

### Unit Tests - Storage Delete (RED Phase)

- [X] T018 [P] [US1] Create tests/unit/test_storage_delete.py with 8 test cases for TaskStorage.delete()
- [X] T019 [P] [US1] Write test_delete_existing_task_returns_true() - happy path verification
- [X] T020 [P] [US1] Write test_delete_non_existent_task_returns_false() - not found returns False
- [X] T021 [P] [US1] Write test_delete_from_empty_storage_returns_false() - empty list edge case
- [X] T022 [P] [US1] Write test_delete_removes_task_from_storage() - verify task actually removed (use get)
- [X] T023 [P] [US1] Write test_delete_doesnt_affect_other_tasks() - delete ID 2, verify IDs 1 and 3 exist
- [X] T024 [P] [US1] Write test_delete_multiple_tasks_in_sequence() - delete 3 tasks one by one
- [X] T025 [P] [US1] Write test_storage_count_decreases_after_delete() - verify count() decrements
- [X] T026 [P] [US1] Write test_storage_count_unchanged_after_failed_delete() - count same on not found

### Storage Implementation (GREEN Phase)

- [X] T027 [US1] Run pytest for test_storage_delete.py and verify ALL 8 tests FAIL (RED confirmation)
- [X] T028 [US1] Implement delete(task_id: int) -> bool method in src/storage.py using enumerate() and del
- [X] T029 [US1] Run pytest for test_storage_delete.py and verify ALL 8 tests PASS (GREEN confirmation)

### Integration Tests - CLI Delete Command (RED Phase)

- [X] T030 [P] [US1] Create tests/integration/test_delete_command.py with delete command integration tests
- [X] T031 [P] [US1] Write test_delete_command_success() - successful deletion returns exit code 0
- [X] T032 [P] [US1] Write test_delete_command_success_message_format() - verify "Task deleted successfully (ID: 1)" format
- [X] T033 [P] [US1] Write test_delete_command_output_to_stdout() - success message goes to stdout not stderr
- [X] T034 [P] [US1] Write test_delete_command_exit_code_success() - verify exit code 0 for successful delete

### CLI Implementation (GREEN Phase)

- [X] T035 [US1] Run pytest for test_delete_command.py and verify US1 tests FAIL (RED confirmation)
- [X] T036 [US1] Add delete subparser to create_parser() in src/cli.py with task_id argument (type=str)
- [X] T037 [US1] Implement handle_delete_command(args, storage) -> int in src/cli.py following add command pattern
- [X] T038 [US1] Add delete command routing to main() in src/main.py (elif args.command == "delete")
- [X] T039 [US1] Run pytest for test_delete_command.py US1 tests and verify ALL PASS (GREEN confirmation)

### Refactor User Story 1 (REFACTOR Phase)

- [X] T040 [US1] Run mypy on src/storage.py, src/cli.py, src/main.py and fix any type errors
- [X] T041 [US1] Run ruff check on modified files and fix any linting issues
- [X] T042 [US1] Run black on modified files to format code
- [X] T043 [US1] Verify delete() method docstring follows Google style with Args, Returns, Examples
- [X] T044 [US1] Verify handle_delete_command() docstring follows Google style

**Checkpoint**: User Story 1 complete - user can delete existing task by ID, all 12 tests passing (8 storage + 4 integration), code quality checks pass

---

## Phase 3: User Story 2 - Error Handling for Non-Existent Tasks (Priority: P2)

**User Story**: As a user, I want to receive a clear error message when attempting to delete a task that doesn't exist so that I understand why the operation failed.

**Why this priority**: Good UX but not blocking - users can still delete existing tasks

**Independent Test**: Attempt to delete non-existent ID, verify error message displayed

**Acceptance Criteria**:
1. Given ID 999 doesn't exist, when I execute `todo delete 999`, then error "Error: Task not found (ID: 999)" displayed
2. Given empty task list, when I execute `todo delete 1`, then error "Error: Task not found (ID: 1)"
3. Given task 5 deleted, when I execute `todo delete 5` again, then error "Error: Task not found (ID: 5)" (idempotent)

### Integration Tests - Error Handling (RED Phase)

- [X] T045 [P] [US2] Write test_delete_command_non_existent_task_error() - delete ID 999 returns "Task not found"
- [X] T046 [P] [US2] Write test_delete_from_empty_list_error() - delete from empty storage returns error
- [X] T047 [P] [US2] Write test_delete_already_deleted_task_error() - idempotent deletion (delete same ID twice)
- [X] T048 [P] [US2] Write test_delete_middle_task_leaves_others() - delete task 2 from [1,2,3], verify 1 and 3 exist
- [X] T049 [P] [US2] Write test_delete_error_messages_go_to_stderr() - verify errors output to stderr not stdout
- [X] T050 [P] [US2] Write test_delete_command_exit_code_error() - verify exit code 1 for errors

### Error Handling Implementation (GREEN Phase)

- [X] T051 [US2] Run pytest for US2 tests in test_delete_command.py and verify ALL FAIL (RED confirmation) - Tests passed immediately (error handling already implemented in Phase 2)
- [X] T052 [US2] Update handle_delete_command() to handle storage.delete() returning False (task not found case) - Already implemented in Phase 2
- [X] T053 [US2] Add "Task not found (ID: {id})" error message formatting using format_error_message() - Already implemented in Phase 2
- [X] T054 [US2] Ensure error messages printed to stderr with exit code 1 - Already implemented in Phase 2
- [X] T055 [US2] Run pytest for US2 tests and verify ALL PASS (GREEN confirmation)

### Refactor User Story 2 (REFACTOR Phase)

- [X] T056 [US2] Run code quality checks (mypy, ruff, black) on src/cli.py
- [X] T057 [US2] Verify error message consistency with add command error patterns

**Checkpoint**: User Story 2 complete - users receive clear "Task not found" errors, all 6 tests passing, exit codes correct

---

## Phase 4: User Story 3 - Validation for Invalid Task IDs (Priority: P3)

**User Story**: As a user, I want to receive clear error messages when I provide an invalid task ID so that I understand the correct format and can successfully delete tasks.

**Why this priority**: Polish feature - users with valid IDs can still use feature

**Independent Test**: Provide invalid ID formats (abc, -5, 0), verify error messages

**Acceptance Criteria**:
1. Given I execute `todo delete abc`, then error "Error: Task ID must be a positive integer"
2. Given I execute `todo delete -5`, then error "Error: Task ID must be a positive integer"
3. Given I execute `todo delete 0`, then error "Error: Task ID must be a positive integer"
4. Given I execute `todo delete` with no ID, then usage help displayed

### Integration Tests - Validation (RED Phase)

- [X] T058 [P] [US3] Write test_delete_invalid_id_format_error() - test "abc" input returns validation error
- [X] T059 [P] [US3] Write test_delete_negative_id_error() - test "-5" input returns validation error
- [X] T060 [P] [US3] Write test_delete_zero_id_error() - test "0" input returns validation error
- [X] T061 [P] [US3] Write test_delete_missing_id_argument() - test no argument shows usage help

### Validation Integration (GREEN Phase)

- [X] T062 [US3] Run pytest for US3 tests in test_delete_command.py and verify ALL FAIL (RED confirmation) - Tests passed immediately (validation already implemented in Phase 2)
- [X] T063 [US3] Import validate_task_id from src.validators in handle_delete_command() - Already implemented in Phase 2 (line 144)
- [X] T064 [US3] Add validation check at start of handle_delete_command() before storage.delete() - Already implemented in Phase 2 (lines 147-151)
- [X] T065 [US3] Print validation error to stderr with exit code 1 if invalid ID format - Already implemented in Phase 2 (lines 149-151)
- [X] T066 [US3] Run pytest for US3 tests and verify ALL PASS (GREEN confirmation)

### Refactor User Story 3 (REFACTOR Phase)

- [X] T067 [US3] Run code quality checks (mypy, ruff, black) on src/cli.py
- [X] T068 [US3] Verify validation error messages match spec exactly

**Checkpoint**: User Story 3 complete - invalid IDs rejected with clear messages, all 4 tests passing

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks, documentation, and verification

### ID Sequence Integrity Testing

- [X] T069 [P] Write test_deleting_task_doesnt_affect_id_sequence() in test_storage_delete.py - add 1,2,3 → delete 2 → add 4 → verify ID=4
- [X] T070 [P] Write test_delete_all_tasks_leaves_storage_empty() in test_delete_command.py - delete all, verify count=0
- [X] T071 [P] Write test_adding_task_after_deletion_uses_next_sequential_id() in test_delete_command.py
- [X] T072 Run pytest for ID sequence tests and verify ALL PASS

### Code Quality & Coverage

- [X] T073 [P] Run mypy --strict on src/ and verify no type errors
- [X] T074 [P] Run ruff check src/ tests/ and verify no linting violations
- [X] T075 [P] Run black src/ tests/ and verify code formatting
- [X] T076 Run pytest --cov=src --cov-report=term and verify ≥80% coverage (target ≥85%) - Achieved 85.44%
- [X] T077 Verify coverage for src/storage.py is 100% - Confirmed 100%
- [X] T078 Verify coverage for src/validators.py is 100% - Confirmed 100%
- [X] T079 Verify coverage for src/cli.py is ≥95% - Confirmed 97.22%

### Documentation & Final Verification

- [X] T080 [P] Verify all new functions have complete Google-style docstrings (Args, Returns, Examples) - All docstrings verified
- [X] T081 [P] Update README.md with delete command usage examples (if README exists) - Updated with delete examples
- [X] T082 Run full test suite `uv run pytest -v` and verify ALL 87 tests pass (58 existing + 29 new from delete feature)
- [X] T083 Manual test: Add tasks 1,2,3 → delete 2 → verify task 2 gone, tasks 1 and 3 remain - Verified via test_delete_middle_task_leaves_others
- [X] T084 Manual test: Delete non-existent task → verify "Task not found" error - Verified via test_delete_command_non_existent_task_error
- [X] T085 Manual test: Delete with invalid ID "abc" → verify validation error - Verified via test_delete_invalid_id_format_error
- [X] T086 Verify all acceptance criteria from spec.md are met for all 3 user stories - All acceptance criteria met

**Checkpoint**: Feature complete, tested, documented, and ready for review

---

## Dependencies & Parallelization

### User Story Dependencies

```text
Phase 1 (Foundational)
    ↓
Phase 2 (US1) → Independent (can implement alone)
    ↓
Phase 3 (US2) → Depends on US1 (needs delete handler)
    ↓
Phase 4 (US3) → Depends on US1 (needs delete handler)
    ↓
Phase 5 (Polish)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 (all sequential due to shared handler)

**Note**: US2 and US3 depend on US1's CLI handler implementation, so they cannot be parallelized

### Parallel Opportunities Within Phases

**Phase 1 - Foundational** (Highly Parallelizable):
- T001-T010 [P]: All 9 test writing tasks can be done in parallel (different test functions)
- T014-T016 [P]: Code quality checks (mypy, ruff, black) can run in parallel

**Phase 2 - User Story 1** (Moderately Parallelizable):
- T018-T026 [P]: All 8 storage test writing tasks can be done in parallel
- T030-T034 [P]: All 5 CLI test writing tasks can be done in parallel
- T040-T042 [P]: Code quality checks can run in parallel

**Phase 3 - User Story 2** (Moderately Parallelizable):
- T045-T050 [P]: All 6 error handling test tasks can be done in parallel
- T056 [P]: Code quality checks

**Phase 4 - User Story 3** (Moderately Parallelizable):
- T058-T061 [P]: All 4 validation test tasks can be done in parallel
- T067 [P]: Code quality checks

**Phase 5 - Polish** (Highly Parallelizable):
- T069-T071 [P]: All 3 ID sequence test tasks can be done in parallel
- T073-T075 [P]: Code quality checks can run in parallel
- T080-T081 [P]: Documentation tasks can be done in parallel

**Estimated Parallel Developer Capacity**:
1. Phase 1: 3 developers can work in parallel (tests, implementation, quality)
2. Phase 2: 2 developers (storage layer, CLI layer split)
3. Phase 3-4: 2 developers (tests, implementation)
4. Phase 5: 3 developers (tests, quality, documentation)

---

## Implementation Strategy

### MVP (Minimum Viable Product)

**Scope**: Phase 1 + Phase 2 (User Story 1 only)
- User can delete existing tasks by ID
- Basic success message displayed
- No error handling for edge cases yet
- No validation for invalid IDs yet

**Value Delivered**: Core deletion functionality working
**Tests Passing**: 21 tests (9 validation + 8 storage + 4 integration)
**Time Estimate**: 2-3 hours

### Full Feature (All User Stories)

**Scope**: Phase 1 + Phase 2 + Phase 3 + Phase 4 + Phase 5
- Complete error handling for non-existent tasks
- Full validation for invalid ID formats
- All edge cases covered
- Documentation complete

**Value Delivered**: Production-ready delete feature
**Tests Passing**: 35 tests total (including ID sequence + polish)
**Time Estimate**: 4-5 hours total

### Incremental Delivery Plan

1. **Iteration 1** (MVP): Phase 1 + Phase 2 → Deploy happy path deletion
2. **Iteration 2** (Error Handling): Add Phase 3 → Deploy error messages
3. **Iteration 3** (Validation): Add Phase 4 → Deploy input validation
4. **Iteration 4** (Polish): Add Phase 5 → Final quality and docs

Each iteration delivers working, testable functionality that builds on the previous iteration.

---

## Test Organization Summary

### Unit Tests (17 tests total)

**tests/unit/test_task_id_validation.py** (9 tests):
- Valid IDs: 1, 100
- Invalid IDs: 0, -1, -100, "abc", "1.5", "", "   "

**tests/unit/test_storage_delete.py** (8 tests + 1 ID sequence):
- Delete existing task returns True
- Delete non-existent returns False
- Delete from empty storage
- Task actually removed (verify with get)
- Other tasks unaffected
- Multiple deletions in sequence
- Count decreases/unchanged
- ID sequence integrity after deletion

### Integration Tests (14 tests + 2 ID sequence)

**tests/integration/test_delete_command.py** (14 tests):
- **US1** (4 tests): success, message format, stdout routing, exit code 0
- **US2** (6 tests): non-existent error, empty list, idempotent, middle task, stderr routing, exit code 1
- **US3** (4 tests): invalid format, negative ID, zero ID, missing argument
- **Polish** (2 tests): delete all tasks, adding after deletion

**Total New Tests**: 29 tests (17 unit + 12 integration)
**Existing Tests**: 53 tests (from add-task feature)
**Total After Implementation**: 82 tests

---

## Success Criteria Verification

| Success Criterion | Tasks Addressing | Verification Method |
|-------------------|------------------|---------------------|
| SC-001: Delete in <2 seconds | T028 (simple O(n) implementation) | T083 manual timing test |
| SC-002: 100% invalid ID rejection | T012, T064-T065 (validation) | T001-T010, T058-T061 tests |
| SC-003: 100% "not found" errors | T052-T054 (error handling) | T045-T050 tests |
| SC-004: Storage integrity | T028 (clean deletion) | T022-T023, T069 tests |
| SC-005: 80%+ coverage | T076-T079 (coverage checks) | pytest-cov report |
| SC-006: Constitutional compliance | All tasks (TDD, type hints, argparse) | T073-T075, T082 |
| SC-007: ID sequence integrity | T028 (never modify _next_id) | T069, T071 tests |

---

## Risk Mitigation

### Risk 1: ID Sequence Integrity

**Risk**: Deleted IDs might be accidentally reused
**Mitigation Tasks**: T069, T071 - Explicit tests for ID sequence
**Verification**: T083 manual test (add 1,2,3 → delete 2 → add 4 → verify ID=4)

### Risk 2: List Deletion Safety

**Risk**: Deleting from list during iteration could cause issues
**Mitigation**: T028 - Use enumerate() and del by index (safe approach)
**Verification**: T024 (multiple deletions), T023 (other tasks unaffected)

---

## Next Steps After Task Completion

1. **Run `/sp.implement`** or begin manual TDD implementation starting with T001
2. **Follow RED-GREEN-REFACTOR** cycle strictly for each phase
3. **Verify checkpoint criteria** after each phase before proceeding
4. **Create PHR** after completing each major phase or when switching contexts
5. **Update tasks.md** to mark completed tasks (change `[ ]` to `[x]`)

**Ready to begin implementation with T001!**
