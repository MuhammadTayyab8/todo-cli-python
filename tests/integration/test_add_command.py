"""Integration tests for the 'add' command."""

import sys
from io import StringIO

from src.cli import create_parser, handle_add_command
from src.storage import TaskStorage


class TestAddCommandTitleOnly:
    """Test adding tasks with title only (User Story 1)."""

    def test_add_command_success_title_only(self) -> None:
        """Test successful task creation with title only."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "Buy groceries"])

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exit code
        assert exit_code == 0

        # Verify task was created
        assert storage.count() == 1
        task = storage.get(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description is None
        assert task.status == "incomplete"

        # Verify output format
        assert "Task added successfully" in output
        assert "ID: 1" in output
        assert "Title: Buy groceries" in output

    def test_add_command_success_message_format(self) -> None:
        """Test that success message includes all required fields."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "Review PR"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        assert "Task added successfully" in output
        assert "ID: 1" in output
        assert "Title: Review PR" in output
        assert "Description: (none)" in output or "Description:" not in output
        assert "Status: incomplete" in output

    def test_add_command_sequential_ids(self) -> None:
        """Test that adding multiple tasks generates sequential IDs."""
        storage = TaskStorage()
        parser = create_parser()

        # Add three tasks
        for i, title in enumerate(["Task 1", "Task 2", "Task 3"], start=1):
            args = parser.parse_args(["add", title])
            captured_output = StringIO()
            sys.stdout = captured_output

            exit_code = handle_add_command(args, storage)

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            assert exit_code == 0
            assert f"ID: {i}" in output

        # Verify all three tasks exist with correct IDs
        assert storage.count() == 3
        assert storage.get(1) is not None
        assert storage.get(2) is not None
        assert storage.get(3) is not None

    def test_add_command_output_to_stdout(self) -> None:
        """Test that success message goes to stdout, not stderr."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "Test task"])

        captured_stdout = StringIO()
        captured_stderr = StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_output = captured_stdout.getvalue()
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 0
        assert "Task added successfully" in stdout_output
        assert stderr_output == ""

    def test_add_command_exit_code_success(self) -> None:
        """Test that successful add returns exit code 0."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "Test task"])

        # Suppress output
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0


class TestAddCommandTitleAndDescription:
    """Test adding tasks with title and description (User Story 2)."""

    def test_add_command_success_title_and_description(self) -> None:
        """Test successful task creation with both title and description."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(
            ["add", "Review PR", "--description", "Check tests and security"]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exit code
        assert exit_code == 0

        # Verify task was created with both fields
        assert storage.count() == 1
        task = storage.get(1)
        assert task is not None
        assert task.id == 1
        assert task.title == "Review PR"
        assert task.description == "Check tests and security"
        assert task.status == "incomplete"

        # Verify output includes both fields
        assert "Task added successfully" in output
        assert "ID: 1" in output
        assert "Title: Review PR" in output
        assert "Description: Check tests and security" in output
        assert "Status: incomplete" in output

    def test_add_command_unicode_title(self) -> None:
        """Test that Unicode characters in title are supported."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "Café 中文"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        task = storage.get(1)
        assert task is not None
        assert task.title == "Café 中文"
        assert "Title: Café 中文" in output

    def test_add_command_unicode_description(self) -> None:
        """Test that Unicode characters in description are supported."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(
            ["add", "Task", "--description", "中文 描述 with émojis 🎉"]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        task = storage.get(1)
        assert task is not None
        assert task.description == "中文 描述 with émojis 🎉"
        assert "Description: 中文 描述 with émojis 🎉" in output

    def test_add_command_multiline_description(self) -> None:
        """Test that multiline descriptions with newlines are preserved."""
        storage = TaskStorage()
        parser = create_parser()
        description = "Line 1\nLine 2\nLine 3"
        args = parser.parse_args(["add", "Task", "--description", description])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0
        task = storage.get(1)
        assert task is not None
        assert task.description == description
        assert "\n" in task.description

    def test_add_command_duplicate_titles_allowed(self) -> None:
        """Test that duplicate titles with different descriptions are allowed."""
        storage = TaskStorage()
        parser = create_parser()

        # Add first task
        args1 = parser.parse_args(["add", "Task", "--description", "First"])
        captured_output = StringIO()
        sys.stdout = captured_output
        exit_code1 = handle_add_command(args1, storage)
        sys.stdout = sys.__stdout__

        # Add second task with same title but different description
        args2 = parser.parse_args(["add", "Task", "--description", "Second"])
        captured_output = StringIO()
        sys.stdout = captured_output
        exit_code2 = handle_add_command(args2, storage)
        sys.stdout = sys.__stdout__

        assert exit_code1 == 0
        assert exit_code2 == 0
        assert storage.count() == 2

        task1 = storage.get(1)
        task2 = storage.get(2)
        assert task1 is not None
        assert task2 is not None
        assert task1.title == task2.title == "Task"
        assert task1.description == "First"
        assert task2.description == "Second"
        assert task1.id != task2.id


class TestAddCommandValidation:
    """Test validation error scenarios (User Story 3)."""

    def test_add_command_empty_title_error(self) -> None:
        """Test that empty title shows error message."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", ""])

        captured_stdout = StringIO()
        captured_stderr = StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title is required" in stderr_output
        assert storage.count() == 0  # No task should be created

    def test_add_command_whitespace_only_title_error(self) -> None:
        """Test that whitespace-only title shows error."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", "   "])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title is required" in stderr_output
        assert storage.count() == 0

    def test_add_command_title_too_long_error(self) -> None:
        """Test that title >100 chars shows error with length."""
        storage = TaskStorage()
        parser = create_parser()
        long_title = "A" * 101
        args = parser.parse_args(["add", long_title])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title must be between 1 and 100 characters" in stderr_output
        assert "received 101" in stderr_output
        assert storage.count() == 0

    def test_add_command_description_too_long_error(self) -> None:
        """Test that description >500 chars shows error."""
        storage = TaskStorage()
        parser = create_parser()
        long_desc = "A" * 501
        args = parser.parse_args(["add", "Task", "--description", long_desc])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Description cannot exceed 500 characters" in stderr_output
        assert "received 501" in stderr_output
        assert storage.count() == 0

    def test_add_command_title_boundary_100_chars_success(self) -> None:
        """Test that exactly 100 chars title succeeds."""
        storage = TaskStorage()
        parser = create_parser()
        title_100 = "A" * 100
        args = parser.parse_args(["add", title_100])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0
        assert storage.count() == 1
        task = storage.get(1)
        assert task is not None
        assert len(task.title) == 100

    def test_add_command_description_boundary_500_chars_success(self) -> None:
        """Test that exactly 500 chars description succeeds."""
        storage = TaskStorage()
        parser = create_parser()
        desc_500 = "A" * 500
        args = parser.parse_args(["add", "Task", "--description", desc_500])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0
        assert storage.count() == 1
        task = storage.get(1)
        assert task is not None
        assert len(task.description) == 500

    def test_add_command_error_output_to_stderr(self) -> None:
        """Test that errors go to stderr not stdout."""
        storage = TaskStorage()
        parser = create_parser()
        args = parser.parse_args(["add", ""])

        captured_stdout = StringIO()
        captured_stderr = StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = handle_add_command(args, storage)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_output = captured_stdout.getvalue()
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert stdout_output == ""  # No output to stdout
        assert "Error:" in stderr_output  # Error to stderr
