# Quickstart: Add Task Feature

**Date**: 2025-12-28
**Branch**: `001-add-task`
**Status**: Ready for Implementation

## Overview

This quickstart guide provides step-by-step instructions for implementing the "Add Task" feature following the Test-Driven Development (TDD) approach defined in the project constitution.

---

## Prerequisites

### System Requirements
- **Python**: 3.13 or higher
- **UV**: Latest version (install from https://github.com/astral-sh/uv)
- **Git**: For version control
- **Editor**: VS Code, PyCharm, or any editor with Python support

### Knowledge Requirements
- Python 3.13+ syntax (type hints, dataclasses)
- TDD methodology (Red-Green-Refactor)
- pytest basics
- CLI development basics

---

## Phase 1: Environment Setup (15 minutes)

### Step 1.1: Initialize UV Project

```bash
# Navigate to project root
cd D:\Tayyab\AI-Hackathon\hackathon-2

# Initialize UV project (if not already done)
uv init

# Pin Python version to 3.13
uv python pin 3.13
```

**Expected Output**:
```
Pinned `.python-version` to `3.13`
```

### Step 1.2: Install Development Dependencies

```bash
# Add pytest and pytest-cov as development dependencies
uv add --dev pytest pytest-cov

# Add linting and formatting tools
uv add --dev mypy ruff black
```

**Expected Output**:
```
Resolved X packages in Ys
Installed X packages in Zms
```

### Step 1.3: Create Project Structure

```bash
# Create source directories
mkdir -p src/models
mkdir -p src/storage
mkdir -p src/validators
mkdir -p src/cli

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/fixtures/__init__.py
```

### Step 1.4: Configure pyproject.toml

Add/update the following in `pyproject.toml`:

```toml
[project]
name = "todo-console-app"
version = "0.1.0"
description = "Simple CLI todo application with in-memory storage"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
    "black>=24.0.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 80

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 88
target-version = "py313"
select = ["E", "F", "W", "I", "N", "UP"]

[tool.black]
line-length = 88
target-version = ['py313']
```

### Step 1.5: Verify Setup

```bash
# Verify pytest works
uv run pytest --version

# Verify mypy works
uv run mypy --version

# Verify ruff works
uv run ruff --version

# Verify black works
uv run black --version
```

**Checkpoint**: All tools should report their versions without errors.

---

## Phase 2: Data Model Implementation (1 hour)

### Step 2.1: Write Tests First (RED Phase)

Create `tests/unit/test_task_model.py`:

```python
"""Unit tests for Task dataclass."""

from datetime import datetime
import pytest
from src.models import Task


class TestTaskCreation:
    """Test Task instantiation with valid data."""

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields populated."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Buy groceries",
            description="Milk, eggs, bread",
            status="incomplete",
            created_at=now
        )
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk, eggs, bread"
        assert task.status == "incomplete"
        assert task.created_at == now

    def test_task_creation_with_minimal_fields(self):
        """Test creating a task with only required fields."""
        now = datetime.now()
        task = Task(
            id=2,
            title="Schedule meeting",
            description=None,
            status="incomplete",
            created_at=now
        )
        assert task.id == 2
        assert task.title == "Schedule meeting"
        assert task.description is None
        assert task.status == "incomplete"


class TestTaskValidation:
    """Test Task validation in __post_init__."""

    def test_task_invalid_id_zero(self):
        """Test that ID of 0 raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(
                id=0,
                title="Task",
                description=None,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_invalid_id_negative(self):
        """Test that negative ID raises ValueError."""
        with pytest.raises(ValueError, match="Task ID must be a positive integer"):
            Task(
                id=-1,
                title="Task",
                description=None,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_invalid_title_empty(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title is required"):
            Task(
                id=1,
                title="",
                description=None,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_invalid_title_whitespace_only(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title is required"):
            Task(
                id=1,
                title="   ",
                description=None,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_invalid_title_too_long(self):
        """Test that title >100 chars raises ValueError."""
        long_title = "A" * 101
        with pytest.raises(ValueError, match="Task title cannot exceed 100 characters"):
            Task(
                id=1,
                title=long_title,
                description=None,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_valid_title_boundary_100_chars(self):
        """Test that title with exactly 100 chars is valid."""
        title_100 = "A" * 100
        task = Task(
            id=1,
            title=title_100,
            description=None,
            status="incomplete",
            created_at=datetime.now()
        )
        assert task.title == title_100

    def test_task_invalid_description_too_long(self):
        """Test that description >500 chars raises ValueError."""
        long_desc = "A" * 501
        with pytest.raises(ValueError, match="Task description cannot exceed 500 characters"):
            Task(
                id=1,
                title="Task",
                description=long_desc,
                status="incomplete",
                created_at=datetime.now()
            )

    def test_task_valid_description_boundary_500_chars(self):
        """Test that description with exactly 500 chars is valid."""
        desc_500 = "A" * 500
        task = Task(
            id=1,
            title="Task",
            description=desc_500,
            status="incomplete",
            created_at=datetime.now()
        )
        assert task.description == desc_500

    def test_task_invalid_status_unknown(self):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Task status must be 'complete' or 'incomplete'"):
            Task(
                id=1,
                title="Task",
                description=None,
                status="done",
                created_at=datetime.now()
            )
```

### Step 2.2: Run Tests (Verify RED)

```bash
uv run pytest tests/unit/test_task_model.py -v
```

**Expected Output**: All tests should FAIL (RED phase) because `src/models.py` doesn't exist yet.

### Step 2.3: Implement Task Model (GREEN Phase)

Create `src/models.py`:

```python
"""Task data model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single to-do item.

    Attributes:
        id: Unique integer identifier (auto-generated, sequential)
        title: Task title (1-100 characters after trimming, required)
        description: Optional task description (max 500 characters)
        status: Completion status ("complete" or "incomplete")
        created_at: Timestamp when task was created (naive datetime)
    """

    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime

    def __post_init__(self) -> None:
        """Validate task attributes after initialization."""
        # Validate ID
        if not isinstance(self.id, int) or self.id < 1:
            raise ValueError("Task ID must be a positive integer")

        # Validate title
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Task title is required and cannot be empty")

        if len(self.title) > 100:
            raise ValueError(f"Task title cannot exceed 100 characters (got {len(self.title)})")

        # Validate description
        if self.description is not None and len(self.description) > 500:
            raise ValueError(f"Task description cannot exceed 500 characters (got {len(self.description)})")

        # Validate status
        if self.status not in ("complete", "incomplete"):
            raise ValueError(f"Task status must be 'complete' or 'incomplete' (got '{self.status}')")
```

### Step 2.4: Run Tests (Verify GREEN)

```bash
uv run pytest tests/unit/test_task_model.py -v --cov=src/models
```

**Expected Output**: All tests should PASS (GREEN phase) with >90% coverage.

### Step 2.5: Refactor (REFACTOR Phase)

Review code for improvements:
- Add type hints if missing
- Improve docstrings
- Extract magic numbers to constants if needed

**Checkpoint**: Phase 2 complete ✅ - Task model implemented with tests passing

---

## Phase 3: Validation Layer (45 minutes)

### Step 3.1: Write Validator Tests (RED)

Create `tests/unit/test_validators.py`:

```python
"""Unit tests for input validation functions."""

import pytest
from src.validators import validate_title, validate_description


class TestValidateTitle:
    """Test validate_title function."""

    def test_valid_title_1_char(self):
        """Test that 1-character title is valid."""
        is_valid, error = validate_title("A")
        assert is_valid is True
        assert error == ""

    def test_valid_title_50_chars(self):
        """Test that 50-character title is valid."""
        title = "A" * 50
        is_valid, error = validate_title(title)
        assert is_valid is True
        assert error == ""

    def test_valid_title_100_chars(self):
        """Test that exactly 100-character title is valid."""
        title = "A" * 100
        is_valid, error = validate_title(title)
        assert is_valid is True
        assert error == ""

    def test_invalid_title_empty(self):
        """Test that empty title is invalid."""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert "Title is required" in error

    def test_invalid_title_whitespace_only(self):
        """Test that whitespace-only title is invalid."""
        is_valid, error = validate_title("   ")
        assert is_valid is False
        assert "Title is required" in error

    def test_invalid_title_101_chars(self):
        """Test that title >100 chars is invalid."""
        title = "A" * 101
        is_valid, error = validate_title(title)
        assert is_valid is False
        assert "Title must be between 1 and 100 characters" in error
        assert "received 101" in error

    def test_title_trimming(self):
        """Test that title is trimmed before validation."""
        is_valid, error = validate_title("  Hello  ")
        assert is_valid is True
        assert error == ""

    def test_title_unicode(self):
        """Test that Unicode characters are valid."""
        is_valid, error = validate_title("Café 中文")
        assert is_valid is True
        assert error == ""


class TestValidateDescription:
    """Test validate_description function."""

    def test_valid_description_none(self):
        """Test that None description is valid."""
        is_valid, error = validate_description(None)
        assert is_valid is True
        assert error == ""

    def test_valid_description_empty_string(self):
        """Test that empty string description is valid."""
        is_valid, error = validate_description("")
        assert is_valid is True
        assert error == ""

    def test_valid_description_500_chars(self):
        """Test that exactly 500-character description is valid."""
        desc = "A" * 500
        is_valid, error = validate_description(desc)
        assert is_valid is True
        assert error == ""

    def test_invalid_description_501_chars(self):
        """Test that description >500 chars is invalid."""
        desc = "A" * 501
        is_valid, error = validate_description(desc)
        assert is_valid is False
        assert "Description cannot exceed 500 characters" in error
        assert "received 501" in error
```

### Step 3.2: Implement Validators (GREEN)

Create `src/validators.py`:

```python
"""Input validation functions for task data."""

from typing import Optional

MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500


def validate_title(title: str) -> tuple[bool, str]:
    """
    Validate task title according to requirements.

    Args:
        title: The title string to validate

    Returns:
        Tuple of (is_valid: bool, error_message: str).
        error_message is empty string if valid.
    """
    if not title:
        return False, "Title is required and cannot be empty"

    trimmed = title.strip()
    if not trimmed:
        return False, "Title is required and cannot be empty"

    if len(trimmed) > MAX_TITLE_LENGTH:
        return False, f"Title must be between 1 and {MAX_TITLE_LENGTH} characters (received {len(trimmed)})"

    return True, ""


def validate_description(description: Optional[str]) -> tuple[bool, str]:
    """
    Validate task description according to requirements.

    Args:
        description: The description string to validate, or None if not provided

    Returns:
        Tuple of (is_valid: bool, error_message: str).
        error_message is empty string if valid.
    """
    if description is None:
        return True, ""  # Optional field

    if len(description) > MAX_DESCRIPTION_LENGTH:
        return False, f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters (received {len(description)})"

    return True, ""
```

### Step 3.3: Run Tests (Verify GREEN)

```bash
uv run pytest tests/unit/test_validators.py -v --cov=src/validators
```

**Expected Output**: All tests should PASS with 100% coverage.

**Checkpoint**: Phase 3 complete ✅ - Validators implemented with tests passing

---

## Next Phases

Continue with:
- **Phase 4**: Storage Layer Implementation (1.5 hours)
- **Phase 5**: CLI Layer Implementation (2 hours)
- **Phase 6**: Main Entry Point (30 minutes)
- **Phase 7**: Coverage and Quality Gates (1 hour)

See `plan.md` for detailed instructions for each phase.

---

## Running Tests

### Run All Tests

```bash
uv run pytest -v
```

### Run Specific Test File

```bash
uv run pytest tests/unit/test_task_model.py -v
```

### Run with Coverage

```bash
uv run pytest --cov=src --cov-report=html --cov-report=term
```

### Run Type Checking

```bash
uv run mypy src/ --strict
```

### Run Linter

```bash
uv run ruff check src/ tests/
```

### Run Formatter

```bash
uv run black src/ tests/
```

---

## Troubleshooting

### UV Command Not Found

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Python 3.13 Not Available

```bash
# UV will automatically download Python 3.13
uv python install 3.13
```

### pytest Import Errors

```bash
# Ensure UV environment is activated
uv sync
uv run pytest --version
```

### Module Not Found Errors

```bash
# Add project root to PYTHONPATH (VS Code)
# Create .env file:
echo "PYTHONPATH=${PWD}" > .env
```

---

## Development Workflow Summary

1. **Checkout feature branch**: `git checkout 001-add-task`
2. **Write tests first** (RED): Define behavior with failing tests
3. **Run tests**: `uv run pytest` - verify tests fail
4. **Implement code** (GREEN): Write minimum code to pass tests
5. **Run tests**: `uv run pytest` - verify tests pass
6. **Refactor** (REFACTOR): Improve code while keeping tests green
7. **Run coverage**: `uv run pytest --cov` - verify ≥90%
8. **Run quality tools**: mypy, ruff, black
9. **Commit**: `git add . && git commit -m "feat: implement <feature>"`
10. **Repeat**: Move to next phase

---

## Resources

- **Python 3.13 Documentation**: https://docs.python.org/3.13/
- **UV Documentation**: https://github.com/astral-sh/uv
- **pytest Documentation**: https://docs.pytest.org/
- **mypy Documentation**: https://mypy.readthedocs.io/
- **Project Constitution**: `.specify/memory/constitution.md`
- **Feature Spec**: `specs/001-add-task/spec.md`
- **Implementation Plan**: `specs/001-add-task/plan.md`

---

**Quickstart Status**: ✅ Ready - Begin implementation with Phase 1
