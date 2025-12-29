# Research: Add Task Feature

**Date**: 2025-12-28
**Branch**: `001-add-task`
**Status**: Complete

## Overview

This document captures the research and architectural decisions made during the planning phase for the "Add Task" feature. All decisions are documented as Architectural Decision Records (ADRs) in plan.md, with this file serving as a summary and rationale reference.

## Research Questions and Decisions

### 1. Task Data Model Representation

**Question**: What Python data structure should represent the Task entity?

**Options Evaluated**:
- dataclass (Python standard library)
- NamedTuple (Python standard library)
- Pydantic BaseModel (external library)
- Plain class with custom `__init__`

**Decision**: dataclass

**Rationale**:
- **Zero external dependencies** (Principle VI): dataclass is built into Python 3.7+, no external packages required
- **Type hints support** (Principle I): Native type hint integration with modern Python tooling (mypy, pyright)
- **Validation hook**: `__post_init__` method provides clean validation point after initialization
- **Flexibility**: Supports frozen=True for immutability, field defaults, repr customization
- **Pythonic**: Widely adopted standard library feature with excellent IDE support
- **No overhead**: Pydantic would be overkill for simple in-memory CLI with no serialization needs

**Alternatives Rejected**:
- NamedTuple: Immutability makes it harder to evolve (though not needed now, future features may want mutable tasks)
- Pydantic: External dependency violation, unnecessary complexity for this use case
- Plain class: More boilerplate than dataclass, no benefit

---

### 2. In-Memory Storage Strategy

**Question**: How should tasks be stored in memory with ID generation and retrieval?

**Options Evaluated**:
- TaskStorage class with list
- TaskStorage class with dict (keyed by ID)
- Global list variable
- Global dict variable

**Decision**: TaskStorage class with internal list

**Rationale**:
- **Encapsulation** (Principle VII): All storage logic in one class (single responsibility)
- **Testability**: Easy to instantiate fresh storage for each test, no global state pollution
- **API clarity**: Public methods (add, get, exists, count, list_all) form clear contract
- **Ordering preservation**: List maintains insertion order naturally (useful for future "list" command sorted by creation)
- **Performance acceptable**: O(n) lookup is fine for expected CLI usage (not web-scale), list iteration is very fast in Python
- **Future-proof**: Easy to add update, delete, filter methods without affecting other code
- **ID generation co-located**: Counter lives with storage, ensuring tight coupling of ID allocation and task creation

**Alternatives Rejected**:
- Dict storage: O(1) lookup is faster but unnecessary for CLI scale; list is simpler and more intuitive
- Global variables: Violates encapsulation, makes testing harder, creates coupling

**ID Generation Approach**:
- Simple counter: `self._next_id: int` starting at 1
- Monotonic increment: No ID reuse even after deletion (per spec clarification)
- Sequential IDs (1, 2, 3, ...) per clarification decision
- No UUID complexity needed for in-memory CLI

---

### 3. CLI Framework Selection

**Question**: Which command-line argument parsing library should be used?

**Options Evaluated**:
- argparse (Python standard library)
- click (external library)
- typer (external library)
- docopt (external library)
- Manual sys.argv parsing

**Decision**: argparse

**Rationale**:
- **Zero external dependencies** (Principle VI): Built into Python standard library
- **Constitution mandate**: FR-013 explicitly requires argparse per constitution
- **Feature-complete**: Supports positional args, optional flags, subcommands, help generation, type validation, exit codes
- **Mature and stable**: 20+ years in stdlib, battle-tested, well-documented
- **Sufficient for requirements**: Simple CLI (`todo add <title> [--description <text>]`) doesn't need advanced features
- **Wide familiarity**: Most Python developers know argparse, reduces onboarding friction

**Alternatives Rejected**:
- click: Modern and ergonomic but violates Principle VI (external dependency)
- typer: Type-hint driven (great fit for Python 3.13+) but violates Principle VI (external dependency)
- docopt: Parses help text to generate parser, clever but external dependency and less flexible
- Manual parsing: Reinventing the wheel, would miss edge cases (quoting, escaping, help text)

---

### 4. Validation Strategy

**Question**: Where and how should input validation occur?

**Options Evaluated**:
- Validation at CLI layer only
- Validation at Task model layer only (__post_init__)
- Validation at both layers (defense in depth)
- Validation in dedicated validators module

**Decision**: Validation at both CLI layer (validators.py) and Task model layer (__post_init__)

**Rationale**:
- **Defense in depth**: CLI validates user input early (fail fast), Task validates construction invariants (defensive programming)
- **Separation of concerns** (Principle VII): validators.py contains pure validation logic, reusable and testable
- **Clear error messages**: CLI layer can provide user-friendly messages before reaching model layer
- **Data integrity**: Task.__post_init__ ensures tasks are never in invalid state, even if created programmatically
- **Testability**: Each layer testable independently (unit tests for validators, unit tests for Task)

**Validation Functions Design**:
- Pure functions: No side effects, easy to test
- Return tuples: `(is_valid: bool, error_message: str)` for flow control (not exceptions at validation layer)
- Trim title whitespace: Normalize before validation (per spec)
- Preserve description whitespace: No trimming (per spec clarification)

---

### 5. Testing Framework and Strategy

**Question**: What testing framework and coverage strategy should be used?

**Options Evaluated**:
- pytest + pytest-cov
- unittest (stdlib)
- nose2
- Coverage target: 80% vs 90% vs 100%

**Decision**: pytest with pytest-cov, targeting 90%+ coverage (minimum 80%)

**Rationale**:
- **pytest advantages**: Better test discovery, fixtures, parametrization, cleaner assert syntax, powerful plugin ecosystem
- **pytest-cov**: Industry standard for coverage reporting, integrates seamlessly with pytest
- **90% target**: Exceeds constitution minimum (80%), provides high confidence without diminishing returns of 100%
- **Constitution compliance** (Principle V): 80% minimum mandated, 90% demonstrates thoroughness

**Testing Strategy**:
- **Unit tests**: models, validators, storage (100% coverage possible and desirable)
- **Integration tests**: Full CLI workflows end-to-end (validates component interactions)
- **Edge cases**: Boundary conditions (1/100/101 chars), Unicode, newlines, errors
- **TDD mandatory** (Principle IV): Red-Green-Refactor cycle strictly enforced

---

### 6. Type Checking and Code Quality Tools

**Question**: What tooling should enforce type safety and code quality?

**Options Evaluated**:
- mypy (type checker)
- pyright (type checker)
- ruff (linter)
- pylint (linter)
- black (formatter)
- isort (import sorter)

**Decision**: mypy (strict mode), ruff, black

**Rationale**:
- **mypy**: De facto standard for Python type checking, excellent Python 3.13+ support, strict mode enforces highest rigor
- **ruff**: Modern, fast, comprehensive linter (combines pyflakes, pycodestyle, isort, and more), single tool replaces multiple
- **black**: Opinionated auto-formatter, eliminates bikeshedding, widely adopted
- **Simplicity**: Three tools cover type checking, linting, and formatting (minimal toolchain)

---

## Best Practices Applied

### Python 3.13+ Features
- **Type hints**: `Optional[str]`, `list[Task]`, `tuple[bool, str]` (modern syntax, no `typing.List`)
- **Dataclasses**: Leverage `__post_init__`, field defaults
- **Pattern matching** (if useful): Not needed for this feature but available for future enhancements

### CLI Best Practices
- **Exit codes**: 0 for success, 1 for all errors (simple two-state model per clarification)
- **Output channels**: stdout for success, stderr for errors
- **Help text**: Automatic via argparse with clear descriptions
- **Error messages**: "Error: " prefix, specific values (e.g., "received 101 characters"), usage guidance

### Testing Best Practices
- **Arrange-Act-Assert**: Clear test structure
- **Test independence**: No shared state between tests
- **Descriptive names**: `test_add_task_increments_id_sequentially` (explicit expectation)
- **Boundary testing**: 1/100/101 chars for title, 500/501 chars for description
- **Test helpers**: Reusable functions (create_long_string, run_cli) in fixtures

### SOLID Principles Applied
- **Single Responsibility**: Task (data), TaskStorage (storage), validators (validation), CLI (interface)
- **Open/Closed**: TaskStorage can be extended with new methods (update, delete) without modification
- **Liskov Substitution**: Not applicable (no inheritance used)
- **Interface Segregation**: Not applicable (no interfaces/protocols defined yet)
- **Dependency Inversion**: CLI depends on TaskStorage abstraction (could interface later if needed)

---

## Technology Stack Summary

| Category | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.13+ | Constitution mandate, modern type hints |
| Data Model | dataclass | stdlib, type hints, validation hook |
| Storage | TaskStorage class (list) | Encapsulation, testability, ordering |
| CLI Parsing | argparse | stdlib, constitution mandate, sufficient |
| Validation | validators.py + Task.__post_init__ | Defense in depth, separation of concerns |
| Testing | pytest + pytest-cov | Best-in-class, fixtures, coverage |
| Type Checking | mypy (strict) | Industry standard, strict mode rigor |
| Linting | ruff | Modern, fast, comprehensive |
| Formatting | black | Opinionated, zero config |
| Coverage Target | 90% (min 80%) | Exceeds constitution requirement |

---

## Open Questions Resolved

**All questions have been resolved.** The spec clarification session (2025-12-28) addressed:
- Task IDs: Sequential integers ✅
- Title validation: Reject (not truncate) ✅
- Timestamps: Only created_at (naive datetime) ✅
- Multi-line descriptions: Supported via shell quoting ✅
- Exit codes: 0 for success, 1 for all errors ✅

---

## References

- Python dataclasses documentation: https://docs.python.org/3/library/dataclasses.html
- argparse documentation: https://docs.python.org/3/library/argparse.html
- pytest documentation: https://docs.pytest.org/
- mypy documentation: https://mypy.readthedocs.io/
- ruff documentation: https://docs.astral.sh/ruff/
- black documentation: https://black.readthedocs.io/

---

**Research Status**: ✅ Complete - All ADRs documented in plan.md
