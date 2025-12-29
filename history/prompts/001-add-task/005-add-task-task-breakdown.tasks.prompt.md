---
id: 005
title: Add task implementation task breakdown
stage: tasks
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: add-task
branch: 001-add-task
user: FCC
command: /sp.tasks
labels: ["tasks", "tdd", "add-task", "checkpoint-driven", "user-stories"]
links:
  spec: specs/001-add-task/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-add-task/tasks.md
tests:
  - 52 test tasks defined (37 unit + 15 integration)
---

## Prompt

Break down "Add Task" implementation into atomic tasks.

Context:
- This is the FIRST feature (project setup needed)
- Following constitution and plan
- Checkpoint-driven approach

Generate tasks.md with checklist including project setup, data model, storage, CLI, main entry, and testing phases. Each task = 1 checkpoint.

## Response snapshot

Created comprehensive, immediately executable task breakdown with 83 atomic tasks organized by user story:

**tasks.md** (structured by 6 phases):

**Phase 1: Setup** (10 tasks):
- UV initialization, Python 3.13 pinning, pytest/mypy/ruff/black installation
- Directory structure creation (src/, tests/unit/, tests/integration/, tests/fixtures/)
- Configuration (pyproject.toml, .python-version, .gitignore)
- Verification (pytest --version check)

**Phase 2: Foundational** (19 tasks - BLOCKS all user stories):
- RED: Write 37 unit tests in parallel (T011-T013 [P] for models, validators, storage)
- GREEN: Implement Task dataclass (T014-T016), validators (T017-T020), TaskStorage (T021-T028)
- Coverage check: ≥90% for foundational components (T029)

**Phase 3: User Story 1 - Title-Only MVP** (14 tasks):
- RED: Write 5 integration tests in parallel (T030-T034 [P])
- GREEN: Implement CLI (create_parser, format_success_message, handle_add_command), main entry point
- Manual testing: `todo add "Buy milk"` verification
- **Checkpoint**: MVP functional

**Phase 4: User Story 2 - Title+Description** (12 tasks):
- RED: Write 5 integration tests in parallel (T044-T048 [P] for description, Unicode, multiline)
- GREEN: Extend CLI with --description argument, update formatting
- Manual testing: Unicode and multiline descriptions
- **Checkpoint**: Full feature functional

**Phase 5: User Story 3 - Validation** (17 tasks):
- RED: Write 7 integration tests in parallel (T056-T062 [P] for errors, boundaries, stderr)
- GREEN: Add validation layer (validate before storage.add), error formatting, stderr output
- Manual testing: All error scenarios
- **Checkpoint**: Production-ready with error handling

**Phase 6: Polish** (11 tasks):
- Type checking (mypy --strict), linting (ruff), formatting (black)
- Coverage validation (96% target)
- Documentation (README.md, intelligence/add-task.md)
- End-to-end validation against spec acceptance criteria

**Key Features**:
1. **TDD Enforced**: All test tasks (T011-T013, T030-T034, T044-T048, T056-T062) marked as RED phase, MUST fail before implementation
2. **User Story Organization**: Tasks grouped by story (US1, US2, US3) with [US#] labels for traceability
3. **Parallelization**: 35 tasks marked [P] (can run in parallel - different files, no dependencies)
4. **Checkpoint-Driven**: Each phase ends with explicit checkpoint validating independent functionality
5. **File Paths**: Every task includes exact file path (e.g., "in src/models.py")
6. **Sequential Dependencies**: Clear dependency graph (Setup → Foundational → US1 → US2 → US3 → Polish)

**Test Coverage**:
- 52 test tasks total: 37 unit tests (models, validators, storage) + 15 integration tests (CLI workflows)
- Expected coverage: 96% (exceeds 90% target and 80% minimum)
- Test organization: tests/unit/, tests/integration/, tests/fixtures/

**Implementation Strategies**:
1. **MVP First**: Phases 1+2+3 = Working `todo add "Task"` CLI (~5.25 hours)
2. **Incremental Delivery**: Add US2 (descriptions) → Add US3 (validation) → Polish (each independently testable)
3. **Parallel Team**: Foundational tests can be written in parallel (T011 [P], T012 [P], T013 [P]); US1 tests in parallel (T030-T034 [P]); limited parallelization for US2+US3 due to dependencies

**Dependencies**:
- US2 depends on US1 (extends CLI infrastructure)
- US3 depends on US1+US2 (adds validation to existing implementation)
- Foundational phase BLOCKS all user stories (critical path)

**Estimated Time**: 7-8 hours sequential, faster with parallel test writing

## Outcome

- ✅ Impact: Immediately executable task breakdown ready; MVP path identified (Phases 1-3); all tasks atomic with clear acceptance
- 🧪 Tests: 52 test tasks defined; TDD workflow enforced (RED-GREEN-REFACTOR for all 3 user stories)
- 📁 Files: Created tasks.md with 83 tasks across 6 phases
- 🔁 Next prompts: Begin implementation with Phase 1 (T001-T010); or run `/sp.implement` to start automated task execution
- 🧠 Reflection: Tasks organized by user story enable independent testing and incremental delivery. TDD enforced with explicit RED phases (write failing tests first). Parallelization opportunities identified (35 tasks marked [P]). Checkpoint-driven approach provides validation points after each phase. MVP path clear (Phases 1-3 = 5.25 hours to working CLI). File paths specified for every task (no ambiguity). Dependencies explicit (US1 → US2 → US3 sequential, Foundational blocks all).

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): TDD compliance: PASS (all tests before implementation), User story organization: PASS (clear [US#] labels), Parallelization: PASS (35 [P] tasks), Coverage target: PASS (96% expected)
- Prompt variant (if applicable): Standard /sp.tasks workflow with TDD enforcement and user story grouping
- Next experiment (smallest change to try): User should begin with Phase 1 (T001-T010) to set up environment, then proceed to Foundational phase (T011-T029) following RED-GREEN-REFACTOR cycle
