# Todo Console Application

A simple, robust command-line todo list application built with Python 3.13+ following Test-Driven Development (TDD) principles.

## Features

- **Add tasks** with title and optional description
- **Update tasks** by ID (title, description, or both)
- **Delete tasks** by ID with confirmation messages
- **Toggle completion status** by ID (incomplete ↔ complete)
- **Input validation** with clear error messages
- **Unicode support** for international characters and emojis
- **Sequential ID generation** for easy task tracking (deleted IDs never reused)
- **In-memory storage** for fast operations

## Requirements

- Python 3.13 or higher
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon-2
```

2. Install UV (if not already installed):
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. Install dependencies:
```bash
uv sync
```

## Usage

### Add a task with title only

```bash
uv run python -m src.main add "Buy groceries"
```

Output:
```
Task added successfully!
ID: 1
Title: Buy groceries
Description: (none)
Status: incomplete
```

### Add a task with title and description

```bash
uv run python -m src.main add "Review PR" --description "Check tests and security"
```

Output:
```
Task added successfully!
ID: 2
Title: Review PR
Description: Check tests and security
Status: incomplete
```

### Delete a task by ID

```bash
uv run python -m src.main delete 2
```

Output:
```
Task deleted successfully (ID: 2)
```

### Update a task's title only

```bash
uv run python -m src.main update 1 --title "Buy weekly groceries"
```

Output:
```
Task updated successfully
  ID: 1
  Title: Buy weekly groceries
  Description: (none)
  Status: incomplete
```

### Update a task's description only

```bash
uv run python -m src.main update 1 --desc "Milk, eggs, bread, cheese"
```

### Update both title and description

```bash
uv run python -m src.main update 1 --title "Shopping" --desc "Saturday morning"
```

### Clear a task's description

```bash
uv run python -m src.main update 1 --desc ""
```

### Toggle a task's status (Mark Complete/Incomplete)

Running the `complete` command toggles the status of a task between `complete` (✓) and `incomplete` (✗).

```bash
# Toggle task 1 status
uv run python -m src.main complete 1
```

Output (if switching to complete):
```
✓ Task marked as complete (ID: 1)
```

Output (if switching back to incomplete):
```
✗ Task marked as incomplete (ID: 1)
```

### Unicode support

```bash
uv run python -m src.main add "Café meeting" --description "Discuss 中文 documentation 🎉"
```

### Error handling for add command

The application provides clear error messages for invalid input:

```bash
# Empty title
uv run python -m src.main add ""
# Error: Title is required and cannot be empty

# Title too long (>100 characters)
uv run python -m src.main add "A very long title that exceeds the maximum allowed length..."
# Error: Title must be between 1 and 100 characters (received 101)

# Description too long (>500 characters)
uv run python -m src.main add "Task" --description "A very long description..."
# Error: Description cannot exceed 500 characters (received 501)
```

### Error handling for delete command

```bash
# Non-existent task
uv run python -m src.main delete 999
# Error: Task not found (ID: 999)

# Invalid ID format
uv run python -m src.main delete abc
# Error: Task ID must be a positive integer

# Negative ID
uv run python -m src.main delete -5
# Error: Task ID must be a positive integer
```

### Error handling for update command

```bash
# No update arguments provided
uv run python -m src.main update 1
# Error: At least one of --title or --desc must be provided

# Non-existent task
uv run python -m src.main update 999 --title "New title"
# Error: Task not found (ID: 999)

# Invalid ID format
uv run python -m src.main update abc --title "New title"
# Error: Task ID must be a positive integer

# Empty title
uv run python -m src.main update 1 --title ""
# Error: Title cannot be empty
```

### Error handling for complete command

```bash
# Non-existent task
uv run python -m src.main complete 999
# Error: Task not found (ID: 999)

# Invalid ID format
uv run python -m src.main complete abc
# Error: Task ID must be a positive integer
```

## Development

### Running Tests

Run all tests:
```bash
uv run pytest -v
```

Run with coverage:
```bash
uv run pytest --cov=src --cov-report=html --cov-report=term
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

### Code Quality

Run type checking:
```bash
uv run mypy src/
```

Run linting:
```bash
uv run ruff check src/ tests/
```

Run formatting:
```bash
uv run black src/ tests/
```

Auto-fix linting issues:
```bash
uv run ruff check --fix src/ tests/
```

## Project Structure

```
hackathon-2/
├── src/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── cli.py            # CLI parsing and command handlers
│   ├── models.py         # Task data model
│   ├── storage.py        # In-memory task storage
│   └── validators.py     # Input validation functions
├── tests/
│   ├── unit/             # Unit tests for core components
│   └── integration/      # Integration tests for CLI commands
├── pyproject.toml        # Project configuration
├── .python-version       # Python version pinning
└── README.md             # This file
```

## Architecture

- **Data Model**: Python dataclass with `__post_init__` validation
- **Storage**: In-memory storage with sequential ID generation starting from 1
- **Validation**: Two-layer validation (CLI validators + Task model)
- **CLI Framework**: argparse (no external runtime dependencies)
- **Error Handling**: Errors to stderr with exit code 1, success to stdout with exit code 0
- **Testing**: pytest with 87.90% code coverage (127 tests: 83 unit + 44 integration)

## Test Coverage

- **Total Coverage**: 87.90% (exceeds 80% minimum requirement)
- **127 tests** organized into unit and integration suites
  - 83 unit tests (validation, storage, models)
  - 44 integration tests (CLI commands)
- **Test-Driven Development (TDD)**: All features implemented following Red-Green-Refactor cycle

## Validation Rules

### Title
- Required (cannot be empty or whitespace-only)
- Maximum 100 characters after trimming
- Supports Unicode characters

### Description
- Optional
- Maximum 500 characters
- Supports Unicode characters and multiline text

### Task ID (for delete and update commands)
- Must be a positive integer (≥ 1)
- Deleted IDs are never reused (maintains sequential integrity)

## License

MIT
