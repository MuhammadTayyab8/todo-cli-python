<!--
Sync Impact Report:
- Version Change: 1.0.0 → 1.0.0 (initial constitution)
- Modified Principles: N/A (initial creation)
- Added Sections: All core principles, technology stack, development workflow, governance
- Removed Sections: N/A
- Templates Requiring Updates:
  ✅ plan-template.md: No updates required (Constitution Check section already flexible)
  ✅ spec-template.md: No updates required (requirements aligned with constitution)
  ✅ tasks-template.md: No updates required (task structure supports TDD and atomic commits)
  ✅ Command files: No agent-specific references to update
- Follow-up TODOs: None
-->

# Todo Console Application Constitution

## Core Principles

### I. Python 3.13+ with Type Hints (MANDATORY)

All code MUST use Python 3.13 or higher with strict type hints. Type hints are mandatory for all function signatures, class attributes, and variable declarations where type inference is not obvious. Code without proper type hints will not be accepted.

**Rationale**: Type hints enable early error detection, improve IDE support, facilitate refactoring, and serve as living documentation. They are essential for maintaining code quality as the project grows.

### II. In-Memory Storage Only (NON-NEGOTIABLE)

The application MUST use only in-memory data structures for storage. No database connections, file persistence, or external storage systems are permitted. All data exists only during the runtime of the application and is lost when the application terminates.

**Rationale**: This constraint simplifies the architecture, eliminates external dependencies, and focuses development on core business logic and CLI interaction patterns. It makes the application portable and easy to test.

### III. UV Package Manager Only (STRICT)

All dependency management, virtual environment creation, and project scaffolding MUST use UV package manager exclusively. The use of pip, poetry, pipenv, or any other Python package management tool is prohibited.

**Rationale**: UV is modern, fast, and provides consistent dependency resolution. Using a single package manager across the project eliminates environment inconsistencies and simplifies onboarding.

### IV. Test-Driven Development (NON-NEGOTIABLE)

TDD is mandatory. Tests MUST be written FIRST, reviewed and approved by the user, and MUST fail before implementation begins. The Red-Green-Refactor cycle is strictly enforced:

1. **Red**: Write failing tests that define desired behavior
2. **Green**: Implement minimum code to pass tests
3. **Refactor**: Improve code while keeping tests passing

No implementation work begins until tests exist and fail. Tests serve as executable specifications.

**Rationale**: TDD ensures code correctness, prevents regression, provides living documentation, and encourages simple, testable designs. Writing tests first clarifies requirements before implementation.

### V. Test Coverage Minimum 80%

All production code MUST maintain a minimum of 80% test coverage. Coverage is measured using pytest-cov. Features that reduce overall coverage below 80% will not be accepted.

**Coverage Requirements**:
- Unit tests: All business logic and models
- Integration tests: CLI command workflows
- Edge cases: Error handling, validation, boundary conditions

**Rationale**: High test coverage provides confidence in code correctness, facilitates refactoring, and catches regressions early. 80% is a pragmatic balance between thoroughness and development speed.

### VI. Zero External Runtime Dependencies

The application MUST NOT depend on any external packages or libraries at runtime except:
- Python standard library
- pytest and pytest-cov (development/testing only)

No third-party libraries for CLI parsing, data validation, serialization, or any other runtime functionality are permitted.

**Rationale**: Zero dependencies eliminate version conflicts, security vulnerabilities from third-party code, and simplify deployment. It forces reliance on Python's robust standard library and keeps the application lightweight.

### VII. Clean Code and SOLID Principles (MANDATORY)

All code MUST adhere to clean code principles and SOLID design:

- **Single Responsibility**: Each class/function has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: Clients should not depend on unused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

**Additional Requirements**:
- Functions should be small (ideally < 20 lines)
- Descriptive names (no abbreviations except standard ones)
- No magic numbers (use named constants)
- DRY principle (Don't Repeat Yourself)
- Clear separation of concerns

**Rationale**: SOLID principles create maintainable, extensible, and testable code. They reduce coupling, increase cohesion, and make the codebase easier to understand and modify.

### VIII. Documentation Standards (MANDATORY)

All modules, classes, and functions MUST include docstrings following Google style convention:

**Required Elements**:
- One-line summary
- Detailed description (if needed)
- Args: All parameters with types and descriptions
- Returns: Return value type and description
- Raises: All exceptions that can be raised
- Examples: Usage examples for public APIs

**Rationale**: Comprehensive documentation serves as a contract for each component, aids in understanding complex logic, and helps new developers onboard quickly. Google style is widely adopted and well-supported by tools.

## Technology Stack Rules

### Language and Version

- **Language**: Python 3.13+
- **Type Checking**: mypy (strict mode)
- **Code Formatting**: black (line length 88)
- **Linting**: ruff (with strict rules)

### CLI Interface

- **Parser**: argparse (Python standard library)
- **Interface Style**: Command-based (e.g., `todo add`, `todo list`)
- **Input**: Command-line arguments only
- **Output**: Human-readable formatted text to stdout
- **Errors**: Clear error messages to stderr with non-zero exit codes

### Testing Stack

- **Test Framework**: pytest
- **Coverage Tool**: pytest-cov
- **Test Organization**: Mirror source structure in `/tests`
- **Test Types**: Unit tests, integration tests, edge case tests

### Development Tools

- **Package Manager**: UV exclusively
- **Virtual Environment**: Managed by UV
- **Python Version Management**: UV's Python version selection
- **Dependency Locking**: UV's lock file (uv.lock)

## Project Structure Standards

### Directory Layout

```
todo-console-app/
├── src/
│   ├── __init__.py
│   ├── models/          # Data models (Task, TaskList)
│   ├── services/        # Business logic (TaskService)
│   ├── cli/             # CLI interface (ArgumentParser, Commands)
│   └── utils/           # Utilities (validators, formatters)
├── tests/
│   ├── __init__.py
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test fixtures and helpers
├── specs/
│   └── <feature-name>/  # Feature specifications
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── history/
│   ├── prompts/         # Prompt History Records
│   │   ├── constitution/
│   │   ├── general/
│   │   └── <feature-name>/
│   └── adr/             # Architecture Decision Records
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # This file
│   └── templates/       # Specification templates
├── pyproject.toml       # UV project configuration
├── uv.lock              # UV dependency lock
├── .python-version      # Python version for UV
└── CLAUDE.md            # Agent instructions
```

### File Organization Rules

- **One class per file**: Each model/service in its own file
- **Flat structure**: Avoid deep nesting (max 2 levels under src/)
- **Test mirroring**: tests/ structure mirrors src/ exactly
- **Feature isolation**: Each feature gets own spec folder
- **Clear naming**: File names match class names (snake_case)

## Development Workflow Standards

### Feature Development Process

1. **Specification Phase** (`/sp.specify`):
   - Create feature spec in `specs/<feature-name>/spec.md`
   - Define user scenarios, requirements, success criteria
   - Get user approval before proceeding

2. **Planning Phase** (`/sp.plan`):
   - Create implementation plan in `specs/<feature-name>/plan.md`
   - Define technical approach, architecture, interfaces
   - Identify architectural decisions (flag for ADR if significant)

3. **Task Breakdown** (`/sp.tasks`):
   - Generate task list in `specs/<feature-name>/tasks.md`
   - Ensure tasks are atomic, testable, and ordered
   - Group by user story priority

4. **Implementation Phase** (`/sp.implement`):
   - Follow TDD: Write tests → Verify failure → Implement → Pass tests
   - One feature = one spec folder
   - Commit after each completed task or logical group

5. **Review Phase**:
   - Run full test suite (must pass)
   - Check coverage (≥80%)
   - Validate against spec requirements
   - Create PHR documenting the work

### Checkpoint-Driven Implementation

Development proceeds through explicit checkpoints:

- **Checkpoint 1**: Spec approved, plan created
- **Checkpoint 2**: Tests written and failing
- **Checkpoint 3**: Implementation complete, tests passing
- **Checkpoint 4**: Coverage verified, code reviewed
- **Checkpoint 5**: Feature validated against success criteria

Each checkpoint must be validated before proceeding to the next.

### Atomic Commit Standards

All commits MUST be atomic and follow these rules:

- **One logical change per commit**: Single task or closely related tasks
- **Tests included**: Commits include both implementation and tests
- **Descriptive messages**: Clear, concise commit messages
- **No broken states**: Each commit leaves codebase in working state
- **Format**: `<type>: <description>` (e.g., `feat: add task creation`, `fix: handle empty task list`)

**Commit Types**:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Test additions/changes
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation updates
- `chore`: Build, tooling, dependencies

### Code Review Requirements

All code changes require validation:

1. **Type checking**: mypy passes with no errors
2. **Linting**: ruff passes with no violations
3. **Formatting**: black formatting applied
4. **Tests**: All tests pass, coverage ≥80%
5. **Documentation**: All new code documented
6. **Spec alignment**: Implementation matches requirements

## Feature Requirements

The Todo Console Application MUST support exactly 5 core operations:

### 1. Add Task
- **Command**: `todo add <title> [--description <text>]`
- **Requirements**:
  - Title is mandatory (non-empty string)
  - Description is optional
  - Auto-generate unique task ID
  - New tasks default to incomplete status
  - Return and display created task details

### 2. Delete Task
- **Command**: `todo delete <id>`
- **Requirements**:
  - ID is mandatory
  - Validate ID exists before deletion
  - Provide clear error if ID not found
  - Confirm deletion or return success message

### 3. Update Task
- **Command**: `todo update <id> [--title <text>] [--description <text>]`
- **Requirements**:
  - ID is mandatory
  - At least one update field required (title or description)
  - Validate ID exists
  - Update only provided fields, leave others unchanged
  - Return updated task details

### 4. View All Tasks
- **Command**: `todo list [--status <complete|incomplete|all>]`
- **Requirements**:
  - Display all tasks by default
  - Support filtering by status
  - Show ID, title, description, and completion status
  - Format as readable table or list
  - Handle empty task list gracefully

### 5. Mark Complete/Incomplete
- **Command**: `todo complete <id>` and `todo incomplete <id>`
- **Requirements**:
  - ID is mandatory
  - Validate ID exists
  - Toggle completion status
  - Provide clear error if ID not found
  - Confirm status change

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines. All code, tests, documentation, and processes must comply with the principles defined herein.

### Amendment Process

Constitutional amendments require:

1. **Proposal**: Document proposed changes with rationale
2. **Impact Analysis**: Identify affected code, tests, templates
3. **Version Increment**: Follow semantic versioning (MAJOR.MINOR.PATCH)
4. **Migration Plan**: Define steps to bring existing code into compliance
5. **User Approval**: Explicit consent before adoption
6. **PHR Creation**: Document the amendment in prompt history

### Compliance Verification

All pull requests, code reviews, and implementations must verify:

- ✅ Type hints present and correct (mypy validates)
- ✅ Tests written first and achieve ≥80% coverage
- ✅ No external runtime dependencies introduced
- ✅ UV used exclusively for package management
- ✅ In-memory storage only (no persistence)
- ✅ Docstrings present for all public APIs
- ✅ SOLID principles followed
- ✅ Atomic commits with clear messages
- ✅ All checkpoints validated

### Complexity Justification

Any deviation from simplicity must be explicitly justified:

- Complex abstractions require documented rationale
- New patterns must explain why simpler alternatives insufficient
- Architectural decisions documented in ADRs
- Violations tracked in plan.md Complexity Tracking section
- Implementation MUST NOT introduce behavior not defined in specs.

### Version Control

All constitution changes tracked in git history. The Sync Impact Report (HTML comment at top of file) summarizes each amendment for quick reference.

### Runtime Guidance

For day-to-day development guidance, agents should reference:
- This constitution for principles and standards
- `CLAUDE.md` for agent-specific execution instructions
- Spec templates in `.specify/templates/` for artifact structure
- PHRs in `history/prompts/` for prior decision context

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
