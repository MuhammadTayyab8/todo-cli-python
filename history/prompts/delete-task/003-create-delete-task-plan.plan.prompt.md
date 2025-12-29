---
id: 003
title: Create Delete Task Implementation Plan
stage: plan
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5
feature: delete-task
branch: 002-delete-task
user: Tayyab
command: /sp.plan
labels: ["implementation-plan", "architecture", "tdd", "design-decisions"]
links:
  spec: specs/002-delete-task/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-delete-task/plan.md
tests:
 - N/A (planning phase - no code written)
---

## Prompt

```
/sp.plan Create implementation plan for "Delete Task" feature.

Generate plan.md with:

1. Architectural Decisions:
   ADR-004: Delete Operation Strategy
   - Approach: Remove from list by ID lookup
   - Error handling approach
   - Return value design

2. Component Design:
   - storage.py: Add delete_task(id: int) method
   - cli.py: Add 'delete' subcommand
   - Error handling strategy

3. Implementation Approach:
   - Extend existing TaskStorage class
   - Reuse Task model (no changes needed)
   - Add CLI delete subcommand

4. Testing Strategy:
   - Test delete existing task
   - Test delete non-existent task
   - Test delete from empty storage
   - Test invalid ID input

Leverage existing patterns from Add Task implementation.
```

## Response snapshot

Generated comprehensive implementation plan for Delete Task feature (872 lines) following established SDD methodology:

**Setup & Context Loading**:
- Ran `.specify/scripts/powershell/setup-plan.ps1 -Json` to get feature paths
- Loaded constitution.md to verify compliance
- Analyzed existing add-task implementation (storage.py, cli.py, validators.py) to understand patterns

**Plan Structure Created**:

**1. Technical Context**:
- Language: Python 3.13+, Standard library only
- Storage: In-memory list-based TaskStorage (existing)
- Testing: pytest + pytest-cov (≥80% coverage)
- Performance: <2 seconds (per SC-001)
- Scope: Small feature (~100 LOC, 3 functions, 1 method)

**2. Constitution Check** (✅ ALL PASSED):
- Python 3.13+ with type hints
- In-memory storage only
- UV package manager (no new dependencies)
- TDD (Red-Green-Refactor cycle)
- 80%+ test coverage (29 tests planned)
- Zero external runtime dependencies
- SOLID principles compliance

**3. Architecture & Design Decisions** (4 ADRs):

**ADR-004: Delete Operation Strategy**
- Decision: Use list-based linear search (O(n))
- Rationale: Consistency with existing get() method, simple, no data structure changes
- Rejected: Dict index (over-engineering), dict-only conversion (risks regression)
- Consequence: Simple 5-10 line implementation, acceptable for CLI scale

**ADR-005: Task ID Validation Strategy**
- Decision: Dedicated `validate_task_id()` function returns 3-tuple (bool, str, int | None)
- Rationale: Consistent with existing validators, testable, reusable, includes parsed int
- Rejected: Inline validation (not reusable), argparse type (less friendly errors)
- Consequence: 9 unit tests planned, clear error messages

**ADR-006: Delete Command Handler Design**
- Decision: Follow `handle_add_command()` pattern
- Flow: Validate → Storage operation → Format output → Return exit code
- Rationale: Consistency, predictable structure, easy to test
- Consequence: Consistent UX across commands

**ADR-007: Delete Method Return Value**
- Decision: Return `bool` (True = deleted, False = not found)
- Rationale: Simplest sufficient solution, Python convention, spec requires only ID in message
- Rejected: Return Task | None (unnecessary), raise exception (anti-pattern for expected case)
- Consequence: Simple to use and test, no new exception types

**4. Component Design** (3 files modified):

**src/storage.py** (Add method):
```python
def delete(self, task_id: int) -> bool:
    # Uses enumerate() for safe deletion
    # Returns True if deleted, False if not found
    # Does NOT modify _next_id (IDs not reused)
```

**src/validators.py** (Add function):
```python
def validate_task_id(task_id_str: str) -> tuple[bool, str, int | None]:
    # Parses and validates task ID (≥1)
    # Returns 3-tuple with parsed int or None
    # Consistent error message for all invalid cases
```

**src/cli.py** (Add subcommand + handler):
```python
# Add delete subparser to create_parser()
# Implement handle_delete_command() following add pattern
# Reuse format_error_message() helper
```

**src/main.py** (Add routing):
```python
elif args.command == "delete":
    return handle_delete_command(args, storage)
```

**5. Implementation Approach** (5 phases):
- Phase 1: Storage Layer (RED: 8 tests → GREEN: delete method → REFACTOR)
- Phase 2: Validation Layer (RED: 9 tests → GREEN: validate_task_id → REFACTOR)
- Phase 3: CLI Layer (RED: 12 tests → GREEN: handler + routing → REFACTOR)
- Phase 4: Integration Testing (ID sequence verification, manual testing)
- Phase 5: Polish & Quality (mypy, ruff, black, coverage ≥80%)

**6. Testing Strategy**:
- **29 new tests**: 9 validation + 8 storage + 12 integration
- **Total after**: 82 tests (53 existing + 29 new)
- **Coverage target**: ≥85% overall (up from 83.65%)
- **Test organization**: tests/unit/, tests/integration/

**7. Success Criteria Mapping**:
- SC-001: Delete <2s → Simple O(n), manual timing
- SC-002: 100% invalid rejection → 9 unit tests
- SC-003: 100% "not found" → 4 integration tests
- SC-004: Storage integrity → 3 storage tests
- SC-005: 80%+ coverage → 82 total tests
- SC-006: Constitutional → Integration tests verify
- SC-007: ID sequence integrity → Explicit test case

**8. Risk Assessment**:
- **Low risk**: Storage, validation, CLI (follows patterns)
- **Medium risk**: ID sequence integrity (mitigated with explicit test), list deletion (mitigated with enumerate)
- **Assumptions**: List sufficient, O(n) acceptable, no concurrency

**Key Insights**:
- Discovered storage uses `list[Task]` not dict (spec assumption incorrect)
- ADR-004 justifies linear search vs dict conversion
- Minimal changes: Extends existing classes without modification
- High reuse: Leverages add-task patterns throughout
- Timeline: 4-5 hours estimated (low complexity)

## Outcome

- ✅ Impact: Created detailed implementation plan with 4 ADRs, component designs, 5-phase approach, and 29-test strategy
- 🧪 Tests: N/A (planning phase - 29 tests designed but not written)
- 📁 Files: Created specs/002-delete-task/plan.md (872 lines)
- 🔁 Next prompts: Ready for `/sp.tasks` to generate atomic task breakdown, then implementation
- 🧠 Reflection: Plan successfully balances simplicity with thoroughness. ADRs document key decisions (list vs dict, bool return, validation pattern) with clear rationales. Implementation approach leverages existing patterns for consistency. All constitutional gates pass. Risk assessment identifies ID sequence integrity as key verification point. Timeline realistic (4-5 hours) given low complexity and established patterns.

## Evaluation notes (flywheel)

- Failure modes observed: None - plan generation successful
- Graders run and results (PASS/FAIL): Constitution Check - PASSED (all 8 gates), Plan completeness - PASSED (all required sections)
- Prompt variant (if applicable): Standard /sp.plan workflow with ADR focus
- Next experiment (smallest change to try): N/A - proceed to task generation with /sp.tasks
