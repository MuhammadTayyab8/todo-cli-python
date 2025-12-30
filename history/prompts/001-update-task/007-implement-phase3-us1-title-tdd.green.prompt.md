---
id: 007
title: Implement Phase 3 US1 Title Update TDD
stage: green
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-update-task
branch: 001-update-task
user: system
command: /sp.implement
labels: ["implementation", "tdd", "cli", "us1", "phase3"]
links:
  spec: specs/001-update-task/spec.md
  ticket: null
  adr: specs/001-update-task/plan.md#adr-005
  pr: null
files:
  - src/cli.py
  - src/main.py
  - tests/integration/test_update_command.py
  - specs/001-update-task/tasks.md
tests:
  - tests/integration/test_update_command.py
---

## Prompt

Phase 3: User Story 1 - Update Task Title Only (Priority: P1)

## Response snapshot

Executed Phase 3: User Story 1 - Update Task Title Only with full TDD workflow:

**RED Phase (T024-T031)** - Wrote 8 failing integration tests:
- test_update_title_only_success
- test_update_title_success_message_format
- test_update_title_success_to_stdout
- test_update_title_exit_code_0
- test_update_title_preserves_incomplete_status
- test_update_title_preserves_complete_status
- test_update_title_unicode_support
- test_update_title_boundary_100_chars

All tests failed with `ImportError: cannot import name 'handle_update_command' from 'src.cli'`

**GREEN Phase (T032-T040)** - Implemented CLI update command:
- Added 'update' subparser to `create_parser()` with task_id, --title, --desc arguments
- Created `handle_update_command(args, storage) -> int` function
- Implemented task_id validation using existing `validate_task_id()`
- Implemented title validation using existing `validate_title()`
- Created `format_update_success_message(task)` for consistent output
- Added routing for 'update' command in `main.py`

All 8 tests now PASS.

## Outcome

- Impact: User Story 1 complete - `python main.py update <id> --title "text"` works
- Tests: 8 integration tests passing (test_update_command.py)
- Files: src/cli.py (+105 lines), src/main.py (+5 lines), tests/integration/test_update_command.py (215 lines)
- Next prompts: Execute Phase 4 (User Story 2 - Description Update)
- Reflection: Clean TDD cycle - tests written first, verified to fail, implementation passes all

## Evaluation notes (flywheel)

- Failure modes observed: None - clean TDD cycle
- Graders run and results (PASS/FAIL): pytest 8/8 PASS
- Prompt variant (if applicable): Standard /sp.implement with phase filter
- Next experiment: Begin Phase 4 US2 description update tests
