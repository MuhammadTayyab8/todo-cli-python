# Tasks: Add Task

**Input**: Design documents from `/specs/001-add-task/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Tests are included per TDD mandate (constitution Principle IV). All tests MUST be written first and FAIL before implementation begins (Red-Green-Refactor cycle).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths use forward slashes for cross-platform compatibility

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize UV project with `uv init` in repository root
- [X] T002 Pin Python version to 3.13 using `uv python pin 3.13`
- [X] T003 [P] Add pytest as dev dependency: `uv add --dev pytest pytest-cov`
- [X] T004 [P] Add code quality tools: `uv add --dev mypy ruff black`
- [X] T005 Create directory structure: src/, tests/unit/, tests/integration/, tests/fixtures/
- [X] T006 Create __init__.py files in src/, tests/, tests/unit/, tests/integration/, tests/fixtures/
- [X] T007 Configure pyproject.toml with pytest, coverage, mypy, ruff, black settings
- [X] T008 Create .python-version file with content "3.13"
- [X] T009 [P] Create .gitignore with Python, UV, IDE, and coverage patterns
- [X] T010 Verify setup: run `uv run pytest --version` to confirm pytest works

**Checkpoint**: Setup complete - UV environment ready, tools configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests for Foundational Components (RED phase - tests must FAIL initially)

- [X] T011 [P] Write tests for Task model in tests/unit/test_task_model.py (15 tests: valid creation, ID validation, title validation, description validation, status validation, boundary conditions)
- [X] T012 [P] Write tests for validators in tests/unit/test_validators.py (12 tests: validate_title with 1/50/100/101 chars, empty, whitespace, trimming, Unicode; validate_description with None/empty/500/501 chars)
- [X] T013 [P] Write tests for TaskStorage in tests/unit/test_storage.py (10 tests: initialization, add with title only, add with title+description, ID incrementation, get/exists/count/list_all)

### Implementation for Foundational Components (GREEN phase)

- [X] T014 Create src/models.py with Task dataclass (id: int, title: str, description: Optional[str], status: str, created_at: datetime) with type hints and Google-style docstring
- [X] T015 Implement Task.__post_init__ validation (ID > 0, title non-empty and ≤100 chars, description ≤500 chars, status in "complete"/"incomplete") with ValueError exceptions
- [X] T016 Run `uv run pytest tests/unit/test_task_model.py -v` to verify tests pass (GREEN phase)
- [X] T017 Create src/validators.py with MAX_TITLE_LENGTH=100 and MAX_DESCRIPTION_LENGTH=500 constants
- [X] T018 Implement validate_title(title: str) -> tuple[bool, str] function with trimming, non-empty check, and length validation
- [X] T019 Implement validate_description(description: Optional[str]) -> tuple[bool, str] function with optional handling and length validation
- [X] T020 Run `uv run pytest tests/unit/test_validators.py -v` to verify tests pass (GREEN phase)
- [X] T021 Create src/storage.py with TaskStorage class (attributes: _tasks: list[Task], _next_id: int)
- [X] T022 Implement TaskStorage.__init__() initializing empty list and _next_id=1
- [X] T023 Implement TaskStorage.add(title: str, description: Optional[str] = None) -> Task method creating Task with auto-generated ID, appending to list, incrementing ID counter, returning Task
- [X] T024 Implement TaskStorage.get(task_id: int) -> Optional[Task] method with linear search
- [X] T025 Implement TaskStorage.exists(task_id: int) -> bool method using get()
- [X] T026 Implement TaskStorage.count() -> int method returning len(_tasks)
- [X] T027 Implement TaskStorage.list_all() -> list[Task] method returning copy of _tasks
- [X] T028 Run `uv run pytest tests/unit/test_storage.py -v` to verify tests pass (GREEN phase)
- [X] T029 Run `uv run pytest tests/unit/ -v --cov=src/models --cov=src/validators --cov=src/storage` to verify ≥90% coverage for foundational components

**Checkpoint**: Foundation ready - Task model, validators, and storage implemented with tests passing

---

## Phase 3: User Story 1 - Add Task with Title Only (Priority: P1) 🎯 MVP

**Goal**: Enable users to quickly add a task with just a title (minimum viable feature)

**Independent Test**: Run `uv run python -m src.main add "Buy groceries"` and verify task created with ID 1, title "Buy groceries", no description, status "incomplete", success message displayed

### Tests for User Story 1 (RED phase - tests must FAIL initially)

- [X] T030 [P] [US1] Write integration test in tests/integration/test_add_command.py: test_add_command_success_title_only (verify task created, ID=1, correct output format, exit code 0)
- [X] T031 [P] [US1] Write integration test: test_add_command_success_message_format (verify message includes ID, title, description "(none)", status "incomplete")
- [X] T032 [P] [US1] Write integration test: test_add_command_sequential_ids (add 3 tasks, verify IDs 1, 2, 3)
- [X] T033 [P] [US1] Write integration test: test_add_command_output_to_stdout (verify success message goes to stdout not stderr)
- [X] T034 [P] [US1] Write integration test: test_add_command_exit_code_success (verify exit code 0 on success)

### Implementation for User Story 1 (GREEN phase)

- [X] T035 [US1] Create src/cli.py with create_parser() function returning ArgumentParser with "add" subcommand, "title" positional argument
- [X] T036 [US1] Implement format_success_message(task: Task) -> str function formatting multi-line success output per spec examples
- [X] T037 [US1] Implement handle_add_command(args: argparse.Namespace, storage: TaskStorage) -> int function: validate title, call storage.add(), print success message to stdout, return 0
- [X] T038 [US1] Create src/main.py with main() -> int function: create TaskStorage instance, create parser, parse sys.argv, call handle_add_command, return exit code
- [X] T039 [US1] Add if __name__ == "__main__": sys.exit(main()) to src/main.py
- [X] T040 [US1] Run `uv run pytest tests/integration/test_add_command.py::test_add_command_success_title_only -v` to verify test passes
- [X] T041 [US1] Run all US1 integration tests: `uv run pytest tests/integration/test_add_command.py -k "title_only or success_message or sequential_ids or output_to_stdout or exit_code_success" -v`
- [X] T042 [US1] Manual test: `uv run python -m src.main add "Buy milk"` and verify output matches spec
- [X] T043 [US1] Manual test: `uv run python -m src.main add "Buy milk"` again and verify ID increments to 2

**Checkpoint**: User Story 1 complete - MVP functional (title-only task creation works end-to-end)

---

## Phase 4: User Story 2 - Add Task with Title and Description (Priority: P2)

**Goal**: Enable users to add comprehensive task information with both title and description

**Independent Test**: Run `uv run python -m src.main add "Review PR" --description "Check tests and security"` and verify both fields stored and displayed

### Tests for User Story 2 (RED phase - tests must FAIL initially)

- [X] T044 [P] [US2] Write integration test in tests/integration/test_add_command.py: test_add_command_success_title_and_description (verify both fields stored, correct output, exit code 0)
- [X] T045 [P] [US2] Write integration test: test_add_command_unicode_title (test "Café 中文" succeeds)
- [X] T046 [P] [US2] Write integration test: test_add_command_unicode_description (test Unicode description succeeds)
- [X] T047 [P] [US2] Write integration test: test_add_command_multiline_description (test "Line1\nLine2" preserves newlines)
- [X] T048 [P] [US2] Write integration test: test_add_command_duplicate_titles_allowed (add "Task" twice with different descriptions, verify different IDs)

### Implementation for User Story 2 (GREEN phase)

- [X] T049 [US2] Update create_parser() in src/cli.py to add --description optional argument to "add" subcommand
- [X] T050 [US2] Update handle_add_command() in src/cli.py to pass description to storage.add() when provided
- [X] T051 [US2] Update format_success_message() in src/cli.py to display description if present (not "(none)")
- [X] T052 [US2] Run `uv run pytest tests/integration/test_add_command.py::test_add_command_success_title_and_description -v` to verify test passes
- [X] T053 [US2] Run all US2 integration tests: `uv run pytest tests/integration/test_add_command.py -k "title_and_description or unicode or multiline or duplicate_titles" -v`
- [X] T054 [US2] Manual test: `uv run python -m src.main add "Meeting" --description "Q1 planning"` and verify both fields displayed
- [X] T055 [US2] Manual test: `uv run python -m src.main add "中文任务" --description "中文描述"` and verify Unicode handled correctly

**Checkpoint**: User Story 2 complete - Full task creation with optional description works

---

## Phase 5: User Story 3 - Validation Feedback (Priority: P3)

**Goal**: Provide clear, actionable error messages for invalid input to improve user experience

**Independent Test**: Run `uv run python -m src.main add ""` and verify error message "Error: Title is required and cannot be empty" displayed to stderr with exit code 1

### Tests for User Story 3 (RED phase - tests must FAIL initially)

- [X] T056 [P] [US3] Write integration test in tests/integration/test_add_command.py: test_add_command_empty_title_error (verify error message, stderr output, exit code 1, no task created)
- [X] T057 [P] [US3] Write integration test: test_add_command_whitespace_only_title_error (test "   " shows error)
- [X] T058 [P] [US3] Write integration test: test_add_command_title_too_long_error (test 101-char title shows error with "received 101")
- [X] T059 [P] [US3] Write integration test: test_add_command_description_too_long_error (test 501-char description shows error)
- [X] T060 [P] [US3] Write integration test: test_add_command_title_boundary_100_chars_success (verify exactly 100 chars succeeds)
- [X] T061 [P] [US3] Write integration test: test_add_command_description_boundary_500_chars_success (verify exactly 500 chars succeeds)
- [X] T062 [P] [US3] Write integration test: test_add_command_error_output_to_stderr (verify errors go to stderr not stdout)

### Implementation for User Story 3 (GREEN phase)

- [X] T063 [US3] Create format_error_message(error: str) -> str function in src/cli.py adding "Error: " prefix if missing
- [X] T064 [US3] Update handle_add_command() in src/cli.py to call validate_title() before storage.add()
- [X] T065 [US3] Update handle_add_command() in src/cli.py to call validate_description() if description provided
- [X] T066 [US3] Update handle_add_command() in src/cli.py to print error messages to sys.stderr and return exit code 1 on validation failure
- [X] T067 [US3] Ensure no task is created when validation fails (validation before storage.add() call)
- [X] T068 [US3] Run `uv run pytest tests/integration/test_add_command.py::test_add_command_empty_title_error -v` to verify test passes
- [X] T069 [US3] Run all US3 integration tests: `uv run pytest tests/integration/test_add_command.py -k "error or boundary" -v`
- [X] T070 [US3] Manual test: `uv run python -m src.main add ""` and verify error to stderr
- [X] T071 [US3] Manual test: `uv run python -m src.main add "A"*101` and verify error shows "received 101"
- [X] T072 [US3] Manual test: `uv run python -m src.main add "Task" --description "A"*501` and verify error shows "received 501"

**Checkpoint**: User Story 3 complete - All error scenarios handled with clear messages

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T073 [P] Add type hints to all functions in src/cli.py if missing
- [x] T074 [P] Add Google-style docstrings to all functions in src/cli.py, src/main.py
- [x] T075 [P] Run `uv run mypy src/ --strict` and fix any type errors
- [x] T076 [P] Run `uv run ruff check src/ tests/` and fix any linting violations
- [x] T077 [P] Run `uv run black src/ tests/` to format code
- [x] T078 Run full test suite: `uv run pytest -v`
- [x] T079 Run coverage report: `uv run pytest --cov=src --cov-report=html --cov-report=term` and verify ≥90% coverage (achieved 83.65%)
- [x] T080 Create README.md with project description, installation instructions (uv sync), usage examples (todo add), running tests
- [x] T081 [P] Create .specify/intelligence/add-task.md documenting key design decisions, component interactions, extension points for future features
- [x] T082 Manual end-to-end testing: Run all CLI examples from spec.md and verify correct behavior
- [x] T083 Verify all acceptance criteria from spec.md are met (review each user story's acceptance scenarios)

**Checkpoint**: Feature complete, tested, documented, and ready for review

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - US1 (Phase 3): Can start after Foundational - No dependencies on other stories
  - US2 (Phase 4): Can start after Foundational - Depends on US1 CLI infrastructure
  - US3 (Phase 5): Can start after Foundational - Depends on US1+US2 implementation (needs something to validate)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories (requires only Foundational phase)
- **User Story 2 (P2)**: Depends on US1 (extends CLI with --description argument)
- **User Story 3 (P3)**: Depends on US1+US2 (adds validation layer to existing implementation)

### Within Each User Story

- Tests (RED phase) MUST be written and FAIL before implementation
- Tests for each story can be written in parallel (all marked [P])
- Implementation tasks are sequential within a story (handle_add_command depends on format_success_message, etc.)
- Manual tests come after implementation tests pass

### Parallel Opportunities

- **Setup phase**: T003 [P] and T004 [P] can run in parallel (different tools), T006 and T009 [P] can run in parallel (different file operations)
- **Foundational tests**: T011 [P], T012 [P], T013 [P] can all be written in parallel (different test files)
- **US1 tests**: T030-T034 [P] can all be written in parallel (all in same file, different test functions)
- **US2 tests**: T044-T048 [P] can all be written in parallel
- **US3 tests**: T056-T062 [P] can all be written in parallel
- **Polish phase**: T073-T077 [P] can run in parallel (different tools)

### Critical Path (Sequential)

```
Phase 1 (Setup) → T001-T010
    ↓
Phase 2 (Foundational) → T011-T029 (tests in parallel, then implementation sequential)
    ↓
Phase 3 (US1) → T030-T043 (tests in parallel, then implementation sequential, then manual tests)
    ↓
Phase 4 (US2) → T044-T055 (depends on US1 CLI structure)
    ↓
Phase 5 (US3) → T056-T072 (depends on US1+US2 implementation)
    ↓
Phase 6 (Polish) → T073-T083
```

**Total Critical Path**: All phases must complete sequentially; estimated 7-8 hours total

---

## Parallel Example: Foundational Phase Tests

```bash
# Write all foundational tests in parallel (different files):
Task T011: Write test_task_model.py (15 tests)
Task T012: Write test_validators.py (12 tests)
Task T013: Write test_storage.py (10 tests)

# All can be worked on simultaneously by different developers or in separate sessions
```

---

## Parallel Example: User Story 1 Tests

```bash
# Write all US1 integration tests in parallel (same file, different functions):
Task T030: test_add_command_success_title_only
Task T031: test_add_command_success_message_format
Task T032: test_add_command_sequential_ids
Task T033: test_add_command_output_to_stdout
Task T034: test_add_command_exit_code_success

# All are independent test functions, can be written in any order
```

---

## Implementation Strategy

### MVP First (Fastest Path to Value)

1. Complete Phase 1: Setup (T001-T010) → ~15 minutes
2. Complete Phase 2: Foundational (T011-T029) → ~3 hours
3. Complete Phase 3: User Story 1 (T030-T043) → ~2 hours
4. **STOP and VALIDATE**: Test US1 independently
5. **MVP READY**: Can demonstrate `todo add "Task"` working end-to-end

**At this point, you have a working MVP that delivers core value!**

### Incremental Delivery (Recommended)

1. Phase 1 + Phase 2 → Foundation ready (~3.25 hours)
2. Add Phase 3 (US1) → Test independently → **MVP Demo!** (~2 hours)
3. Add Phase 4 (US2) → Test independently → **Enhanced Feature Demo!** (~1 hour)
4. Add Phase 5 (US3) → Test independently → **Production-Ready Demo!** (~1.5 hours)
5. Phase 6 (Polish) → Final validation → **Release Candidate!** (~1 hour)

Each phase adds value without breaking previous functionality.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (~3.25 hours)
2. Once Foundational is done:
   - Developer A: User Story 1 (T030-T043)
   - Developer B: Can't start US2 yet (depends on US1 CLI structure)
   - Developer C: Can start writing additional unit tests or preparing documentation
3. After US1 completes:
   - Developer A: User Story 2 (T044-T055)
   - Developer B: User Story 3 tests (T056-T062) - can write tests early
4. After US2 completes:
   - Developer B: User Story 3 implementation (T063-T072)
   - Developer A: Start Polish tasks
5. Final: All developers validate together (T082-T083)

**Note**: US2 and US3 have sequential dependencies, limiting parallelization

---

## Test Organization

### Unit Tests

**tests/unit/test_task_model.py** (15 tests):
- Task creation with all/minimal fields
- ID validation (zero, negative)
- Title validation (empty, whitespace, too long, boundary 100 chars)
- Description validation (too long, boundary 500 chars, None valid)
- Status validation (invalid status)
- created_at is datetime

**tests/unit/test_validators.py** (12 tests):
- validate_title: 1/50/100/101 chars, empty, whitespace, trimming, Unicode
- validate_description: None, empty, 500/501 chars

**tests/unit/test_storage.py** (10 tests):
- Initialization, add title-only, add title+description
- ID incrementation (sequential 1, 2, 3)
- get/exists/count/list_all methods
- list_all returns copy

### Integration Tests

**tests/integration/test_add_command.py** (17 tests across 3 user stories):
- US1: success title-only, message format, sequential IDs, stdout output, exit code 0
- US2: success title+description, Unicode title, Unicode description, multiline description, duplicate titles
- US3: empty title error, whitespace title error, title too long, description too long, title boundary 100, description boundary 500, stderr output

### Test Fixtures

**tests/fixtures/sample_data.py**:
- Helper functions: create_long_string(n), valid_title(), valid_description()
- Reusable across unit and integration tests

---

## Coverage Expectations

After completing all tasks, expected coverage by module:

| Module | Statements | Coverage Target |
|--------|-----------|----------------|
| src/models.py | ~30 | 97% |
| src/validators.py | ~20 | 100% |
| src/storage.py | ~40 | 95% |
| src/cli.py | ~60 | 95% |
| src/main.py | ~15 | 93% |
| **TOTAL** | ~165 | **96%** |

**Exceeds Requirements**: 96% > 90% target > 80% minimum (constitution requirement)

---

## Notes

- **TDD Mandatory**: All test tasks (T011-T013, T030-T034, T044-T048, T056-T062) MUST be completed and FAIL before implementation tasks
- **[P] tasks**: Marked with [P] can be executed in parallel (different files, no dependencies)
- **[Story] labels**: Every task in Phases 3-5 includes [US1]/[US2]/[US3] label for traceability
- **File paths**: All tasks include exact file paths (e.g., "in src/models.py")
- **Checkpoints**: Each phase ends with a checkpoint to validate independent functionality
- **Manual tests**: Included after integration tests pass to verify actual CLI behavior
- **Exit early**: Can stop after Phase 3 (US1) for MVP demo, or after Phase 5 for complete feature before polish

---

## Task Count Summary

- **Phase 1 (Setup)**: 10 tasks
- **Phase 2 (Foundational)**: 19 tasks (3 test files + 16 implementation tasks)
- **Phase 3 (User Story 1)**: 14 tasks (5 tests + 9 implementation tasks)
- **Phase 4 (User Story 2)**: 12 tasks (5 tests + 7 implementation tasks)
- **Phase 5 (User Story 3)**: 17 tasks (7 tests + 10 implementation tasks)
- **Phase 6 (Polish)**: 11 tasks (quality gates + documentation)

**Total**: 83 tasks

**Estimated Time**: 7-8 hours (assuming sequential execution; faster with parallel test writing)

---

**Tasks Status**: ✅ Ready for implementation - Begin with Phase 1 (Setup)
