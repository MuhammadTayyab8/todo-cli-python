"""Integration tests for the 'update' CLI command."""

import sys
import tempfile
from io import StringIO
from pathlib import Path

from src.cli import create_parser, handle_update_command
from src.models import Task
from src.storage import TaskStorage


def get_temp_storage() -> TaskStorage:
    """Create a TaskStorage with a temporary file that gets deleted after."""
    return TaskStorage(storage_file=Path(tempfile.mktemp(suffix=".json")))


class TestUpdateTitleOnly:
    """Test updating tasks with title only (User Story 1)."""

    # T024: Test update title only success
    def test_update_title_only_success(self) -> None:
        """Test successful task update with title only."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "New title"])

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exit code
        assert exit_code == 0

        # Verify task was updated
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.title == "New title"
        assert updated_task.description == "Original description"  # Preserved

        # Verify output
        assert "Task updated successfully" in output
        assert "Title: New title" in output

    # T025: Test update title success message format
    def test_update_title_success_message_format(self) -> None:
        """Test that success message includes all required fields."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "Updated title"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        assert "Task updated successfully" in output
        assert f"ID: {task.id}" in output
        assert "Title: Updated title" in output
        assert "Description: Original description" in output
        assert "Status: incomplete" in output

    # T026: Test update title success to stdout
    def test_update_title_success_to_stdout(self) -> None:
        """Test that success message goes to stdout, not stderr."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "New title"])

        captured_stdout = StringIO()
        captured_stderr = StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_output = captured_stdout.getvalue()
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 0
        assert "Task updated successfully" in stdout_output
        assert stderr_output == ""

    # T027: Test update title exit code 0
    def test_update_title_exit_code_0(self) -> None:
        """Test that successful update returns exit code 0."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "New title"])

        # Suppress output
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0

    # T028: Test update title preserves incomplete status
    def test_update_title_preserves_incomplete_status(self) -> None:
        """Test that updating title preserves 'incomplete' status."""
        storage = get_temp_storage()
        task = storage.add("Original title")
        assert task.status == "incomplete"

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "New title"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.status == "incomplete"
        assert "Status: incomplete" in output

    # T029: Test update title preserves complete status
    def test_update_title_preserves_complete_status(self) -> None:
        """Test that updating title preserves 'complete' status."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        # Manually set status to complete for testing
        completed_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status="complete",
            created_at=task.created_at,
        )
        storage._tasks[0] = completed_task

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "New title"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.status == "complete"
        assert "Status: complete" in output

    # T030: Test update title unicode support
    def test_update_title_unicode_support(self) -> None:
        """Test that Unicode characters in title are supported."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "Café 中文 🎉"])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.title == "Café 中文 🎉"
        assert "Title: Café 中文 🎉" in output

    # T031: Test update title boundary 100 chars
    def test_update_title_boundary_100_chars(self) -> None:
        """Test that exactly 100 chars title succeeds."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        title_100 = "A" * 100
        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", title_100])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert len(updated_task.title) == 100


class TestUpdateDescriptionOnly:
    """Test updating tasks with description only (User Story 2)."""

    # T041: Test update description only success
    def test_update_description_only_success(self) -> None:
        """Test successful task update with description only."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--desc", "New description"])

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exit code
        assert exit_code == 0

        # Verify task was updated
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.title == "Original title"  # Preserved
        assert updated_task.description == "New description"

        # Verify output
        assert "Task updated successfully" in output
        assert "Title: Original title" in output
        assert "Description: New description" in output

    # T042: Test update description adds to empty
    def test_update_description_adds_to_empty(self) -> None:
        """Test adding description to task that had no description."""
        storage = get_temp_storage()
        task = storage.add("Original title")  # No description
        assert task.description is None

        parser = create_parser()
        args = parser.parse_args(
            ["update", str(task.id), "--desc", "Added description"]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.description == "Added description"
        assert "Description: Added description" in output

    # T043: Test update description clears with empty string
    def test_update_description_clears_with_empty_string(self) -> None:
        """Test that --desc '' clears the description."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--desc", ""])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.description == ""
        assert "Description: (none)" in output

    # T044: Test update description boundary 500 chars
    def test_update_description_boundary_500_chars(self) -> None:
        """Test that exactly 500 chars description succeeds."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        desc_500 = "A" * 500
        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--desc", desc_500])

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert len(updated_task.description) == 500

    # T045: Test update description unicode support
    def test_update_description_unicode_support(self) -> None:
        """Test that Unicode characters in description are supported."""
        storage = get_temp_storage()
        task = storage.add("Original title")

        parser = create_parser()
        args = parser.parse_args(
            ["update", str(task.id), "--desc", "中文 描述 with émojis 🎉"]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.description == "中文 描述 with émojis 🎉"
        assert "Description: 中文 描述 with émojis 🎉" in output


class TestUpdateBothTitleAndDescription:
    """Test updating tasks with both title and description (User Story 3)."""

    # T051: Test update both title and description success
    def test_update_both_title_and_description_success(self) -> None:
        """Test successful task update with both title and description."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(
            [
                "update",
                str(task.id),
                "--title",
                "New title",
                "--desc",
                "New description",
            ]
        )

        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Verify exit code
        assert exit_code == 0

        # Verify task was updated
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.title == "New title"
        assert updated_task.description == "New description"

        # Verify output
        assert "Task updated successfully" in output
        assert "Title: New title" in output
        assert "Description: New description" in output

    # T052: Test update both adds description to empty
    def test_update_both_adds_description_to_empty(self) -> None:
        """Test updating both fields when task originally had no description."""
        storage = get_temp_storage()
        task = storage.add("Original title")  # No description
        assert task.description is None

        parser = create_parser()
        args = parser.parse_args(
            [
                "update",
                str(task.id),
                "--title",
                "New title",
                "--desc",
                "Added description",
            ]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        updated_task = storage.get(task.id)
        assert updated_task is not None
        assert updated_task.title == "New title"
        assert updated_task.description == "Added description"
        assert "Title: New title" in output
        assert "Description: Added description" in output

    # T053: Test update both success message format
    def test_update_both_success_message_format(self) -> None:
        """Test that success message includes all required fields when updating both."""
        storage = get_temp_storage()
        task = storage.add("Original title", "Original description")

        parser = create_parser()
        args = parser.parse_args(
            [
                "update",
                str(task.id),
                "--title",
                "Updated title",
                "--desc",
                "Updated description",
            ]
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        assert exit_code == 0
        assert "Task updated successfully" in output
        assert f"ID: {task.id}" in output
        assert "Title: Updated title" in output
        assert "Description: Updated description" in output
        assert "Status: incomplete" in output


class TestUpdateErrorHandling:
    """Test error handling for update command (User Story 4)."""

    # T056: Test update non-existent id error
    def test_update_non_existent_id_error(self) -> None:
        """Test that updating a non-existent task ID returns error."""
        storage = get_temp_storage()
        storage.add("Existing task")  # ID 1 exists

        parser = create_parser()
        args = parser.parse_args(["update", "999", "--title", "New title"])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Task not found (ID: 999)" in stderr_output

    # T057: Test update invalid id non-numeric error
    def test_update_invalid_id_non_numeric_error(self) -> None:
        """Test that non-numeric task ID returns error."""
        storage = get_temp_storage()
        storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", "abc", "--title", "New title"])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Task ID must be a positive integer" in stderr_output

    # T058: Test update invalid id negative error
    def test_update_invalid_id_negative_error(self) -> None:
        """Test that negative task ID returns error."""
        storage = get_temp_storage()
        storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", "-5", "--title", "New title"])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Task ID must be a positive integer" in stderr_output

    # T059: Test update invalid id zero error
    def test_update_invalid_id_zero_error(self) -> None:
        """Test that task ID 0 returns error."""
        storage = get_temp_storage()
        storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", "0", "--title", "New title"])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Task ID must be a positive integer" in stderr_output

    # T060: Test update no args error
    def test_update_no_args_error(self) -> None:
        """Test that update without --title or --desc returns error."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id)])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "At least one of --title or --desc must be provided" in stderr_output

    # T061: Test update empty title error
    def test_update_empty_title_error(self) -> None:
        """Test that empty title returns error."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", ""])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title is required" in stderr_output

    # T062: Test update whitespace title error
    def test_update_whitespace_title_error(self) -> None:
        """Test that whitespace-only title returns error."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", "   "])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title is required" in stderr_output

    # T063: Test update title too long error
    def test_update_title_too_long_error(self) -> None:
        """Test that title >100 chars returns error with length."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        long_title = "A" * 101
        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--title", long_title])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Title must be between 1 and 100 characters" in stderr_output
        assert "received 101" in stderr_output

    # T064: Test update description too long error
    def test_update_description_too_long_error(self) -> None:
        """Test that description >500 chars returns error."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        long_desc = "A" * 501
        parser = create_parser()
        args = parser.parse_args(["update", str(task.id), "--desc", long_desc])

        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert "Error:" in stderr_output
        assert "Description cannot exceed 500 characters" in stderr_output
        assert "received 501" in stderr_output

    # T065: Test update error to stderr
    def test_update_error_to_stderr(self) -> None:
        """Test that errors go to stderr, not stdout."""
        storage = get_temp_storage()
        task = storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", str(task.id)])  # No --title or --desc

        captured_stdout = StringIO()
        captured_stderr = StringIO()
        sys.stdout = captured_stdout
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        stdout_output = captured_stdout.getvalue()
        stderr_output = captured_stderr.getvalue()

        assert exit_code == 1
        assert stdout_output == ""  # No output to stdout
        assert "Error:" in stderr_output  # Error to stderr

    # T066: Test update error exit code 1
    def test_update_error_exit_code_1(self) -> None:
        """Test that errors return exit code 1."""
        storage = get_temp_storage()
        storage.add("Existing task")

        parser = create_parser()
        args = parser.parse_args(["update", "999", "--title", "New title"])

        # Suppress stderr
        captured_stderr = StringIO()
        sys.stderr = captured_stderr

        exit_code = handle_update_command(args, storage)

        sys.stderr = sys.__stderr__

        assert exit_code == 1
