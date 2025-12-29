"""Integration tests for the 'delete' command."""

import sys
from io import StringIO

from src.cli import create_parser, handle_delete_command
from src.storage import TaskStorage


def test_delete_command_success():
    """Test successful deletion returns exit code 0."""
    storage = TaskStorage()
    task = storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task.id)])

    exit_code = handle_delete_command(args, storage)

    assert exit_code == 0


def test_delete_command_success_message_format():
    """Test success message format matches spec."""
    storage = TaskStorage()
    task = storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task.id)])

    captured_output = StringIO()
    sys.stdout = captured_output

    handle_delete_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    expected_message = f"Task deleted successfully (ID: {task.id})"
    assert output == expected_message


def test_delete_command_output_to_stdout():
    """Test success message goes to stdout not stderr."""
    storage = TaskStorage()
    task = storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task.id)])

    captured_stdout = StringIO()
    captured_stderr = StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr

    handle_delete_command(args, storage)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    stdout_output = captured_stdout.getvalue().strip()
    stderr_output = captured_stderr.getvalue().strip()

    assert len(stdout_output) > 0
    assert len(stderr_output) == 0


def test_delete_command_exit_code_success():
    """Test exit code 0 for successful delete."""
    storage = TaskStorage()
    task = storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task.id)])

    exit_code = handle_delete_command(args, storage)

    assert exit_code == 0


# User Story 2: Error Handling Tests


def test_delete_command_non_existent_task_error():
    """Test deleting non-existent task ID 999 returns 'Task not found' error."""
    storage = TaskStorage()
    storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", "999"])

    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code == 1
    assert "Error: Task not found (ID: 999)" in error_output


def test_delete_from_empty_list_error():
    """Test deleting from empty storage returns error."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "1"])

    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code == 1
    assert "Error: Task not found (ID: 1)" in error_output


def test_delete_already_deleted_task_error():
    """Test idempotent deletion - deleting same task twice returns error."""
    storage = TaskStorage()
    task = storage.add("Test task")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task.id)])

    # First deletion should succeed
    exit_code1 = handle_delete_command(args, storage)
    assert exit_code1 == 0

    # Second deletion should fail with error
    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code2 = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code2 == 1
    assert f"Error: Task not found (ID: {task.id})" in error_output


def test_delete_middle_task_leaves_others():
    """Test deleting task 2 from [1,2,3] leaves tasks 1 and 3 intact."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")
    task3 = storage.add("Task 3")

    parser = create_parser()
    args = parser.parse_args(["delete", str(task2.id)])

    exit_code = handle_delete_command(args, storage)

    assert exit_code == 0
    assert storage.get(task1.id) is not None
    assert storage.get(task2.id) is None
    assert storage.get(task3.id) is not None


def test_delete_error_messages_go_to_stderr():
    """Test error messages are output to stderr not stdout."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "999"])

    captured_stdout = StringIO()
    captured_stderr = StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr

    handle_delete_command(args, storage)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    stdout_output = captured_stdout.getvalue().strip()
    stderr_output = captured_stderr.getvalue().strip()

    assert len(stdout_output) == 0
    assert len(stderr_output) > 0
    assert "Error:" in stderr_output


def test_delete_command_exit_code_error():
    """Test exit code 1 for error cases."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "999"])

    exit_code = handle_delete_command(args, storage)

    assert exit_code == 1


# User Story 3: Validation Tests


def test_delete_invalid_id_format_error():
    """Test invalid ID format 'abc' returns validation error."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "abc"])

    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code == 1
    assert "Error: Task ID must be a positive integer" in error_output


def test_delete_negative_id_error():
    """Test negative ID '-5' returns validation error."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "-5"])

    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code == 1
    assert "Error: Task ID must be a positive integer" in error_output


def test_delete_zero_id_error():
    """Test zero ID '0' returns validation error."""
    storage = TaskStorage()

    parser = create_parser()
    args = parser.parse_args(["delete", "0"])

    captured_stderr = StringIO()
    sys.stderr = captured_stderr

    exit_code = handle_delete_command(args, storage)

    sys.stderr = sys.__stderr__
    error_output = captured_stderr.getvalue().strip()

    assert exit_code == 1
    assert "Error: Task ID must be a positive integer" in error_output


def test_delete_missing_id_argument():
    """Test missing ID argument shows usage help."""
    import subprocess
    import sys

    # Run the command without task_id argument
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "delete"],
        capture_output=True,
        text=True,
    )

    # Should exit with error code 2 (argparse error)
    assert result.returncode == 2
    # Should show usage help
    assert "usage:" in result.stderr.lower() or "error:" in result.stderr.lower()


# Phase 5: ID Sequence Integrity Tests


def test_delete_all_tasks_leaves_storage_empty():
    """Test deleting all tasks leaves storage with count=0."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")
    task3 = storage.add("Task 3")

    parser = create_parser()

    # Delete all tasks
    handle_delete_command(parser.parse_args(["delete", str(task1.id)]), storage)
    handle_delete_command(parser.parse_args(["delete", str(task2.id)]), storage)
    handle_delete_command(parser.parse_args(["delete", str(task3.id)]), storage)

    assert storage.count() == 0


def test_adding_task_after_deletion_uses_next_sequential_id():
    """Test that adding a task after deletion uses the next sequential ID."""
    storage = TaskStorage()
    task1 = storage.add("Task 1")
    task2 = storage.add("Task 2")

    # Delete task 1
    parser = create_parser()
    handle_delete_command(parser.parse_args(["delete", str(task1.id)]), storage)

    # Add a new task - should get ID 3 (not reusing ID 1)
    task3 = storage.add("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3  # Should be 3, not 1
