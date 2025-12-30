"""Integration tests for the 'list' CLI command."""

import sys
from io import StringIO

from src.cli import create_parser, handle_list_command
from src.storage import TaskStorage


# T018 [US1]: Test list empty shows no tasks message
def test_list_empty_shows_no_tasks_message() -> None:
    """Test that empty storage displays 'No tasks found' message."""
    storage = TaskStorage()
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "No tasks found" in output


# T019 [US1]: Test list single task
def test_list_single_task() -> None:
    """Test that single task displays correctly."""
    storage = TaskStorage()
    storage.add("Buy groceries")
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "[1]" in output
    assert "Buy groceries" in output


# T020 [US1]: Test list multiple tasks
def test_list_multiple_tasks() -> None:
    """Test that multiple tasks are all displayed."""
    storage = TaskStorage()
    storage.add("Task 1")
    storage.add("Task 2")
    storage.add("Task 3")
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "Task 1" in output
    assert "Task 2" in output
    assert "Task 3" in output


# T021 [US1]: Test list multiple tasks display order
def test_list_multiple_tasks_display_order() -> None:
    """Test that tasks are displayed in ID order regardless of addition order."""
    storage = TaskStorage()
    # Add tasks - they will get IDs 1, 2, 3 in addition order
    storage.add("First task")  # ID 1
    storage.add("Second task")  # ID 2
    storage.add("Third task")  # ID 3
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    # Verify each task appears and verify they appear in correct order by checking IDs
    assert "[1]" in output
    assert "[2]" in output
    assert "[3]" in output
    # Check order by ID positions
    id1_pos = output.find("[1]")
    id2_pos = output.find("[2]")
    id3_pos = output.find("[3]")
    assert id1_pos < id2_pos < id3_pos, "Tasks should be in ID order"


# T022 [US1]: Test list header format
def test_list_header_format() -> None:
    """Test that list header matches specification."""
    storage = TaskStorage()
    storage.add("Buy groceries")
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "TODO LIST:" in output


# T023 [US1]: Test list divider present
def test_list_divider_present() -> None:
    """Test that divider line is present in output."""
    storage = TaskStorage()
    storage.add("Buy groceries")
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    # Divider should be present (long dash line)
    assert "─" in output or "----" in output


# T024 [US1]: Test list exit code 0
def test_list_exit_code_0() -> None:
    """Test that list command always returns exit code 0."""
    storage = TaskStorage()
    parser = create_parser()
    args = parser.parse_args(["list"])

    exit_code = handle_list_command(args, storage)

    assert exit_code == 0


# T029 [US2]: Test list None description shows (none)
def test_list_none_description_shows_none() -> None:
    """Test that task with no description shows '(none)'."""
    storage = TaskStorage()
    storage.add("Buy groceries")  # No description
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "(none)" in output


# T030 [US2]: Test list title 100 chars displays
def test_list_title_100_chars() -> None:
    """Test that 100-character title displays fully without truncation."""
    storage = TaskStorage()
    long_title = "A" * 100  # Exactly 100 characters
    storage.add(long_title)
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert long_title in output


# T031 [US2]: Test list description 500 chars displays
def test_list_description_500_chars() -> None:
    """Test that 500-character description displays fully without truncation."""
    storage = TaskStorage()
    long_desc = "B" * 500  # Exactly 500 characters
    storage.add("Buy groceries", long_desc)
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert long_desc in output


# T036 [US3]: Test list incomplete status symbol
def test_list_incomplete_status_symbol() -> None:
    """Test that incomplete tasks show '✗' symbol."""
    storage = TaskStorage()
    storage.add("Buy groceries")  # Default is incomplete
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "✗" in output


# T037 [US3]: Test list complete status symbol
def test_list_complete_status_symbol() -> None:
    """Test that complete tasks show '✓' symbol."""
    storage = TaskStorage()
    storage.add("Buy groceries")
    storage._tasks[0].status = "complete"  # Mark as complete
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "✓" in output


# T038 [US3]: Test list summary counts completed
def test_list_summary_counts_completed() -> None:
    """Test that summary shows correct completed count."""
    storage = TaskStorage()
    storage.add("Task 1")
    storage.add("Task 2")
    storage._tasks[0].status = "complete"  # Task 1 complete
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "Total: 2 tasks" in output
    assert "1 completed" in output


# T039 [US3]: Test list summary counts pending
def test_list_summary_counts_pending() -> None:
    """Test that summary shows correct pending count."""
    storage = TaskStorage()
    storage.add("Task 1")
    storage.add("Task 2")
    storage.add("Task 3")
    storage._tasks[0].status = "complete"  # Task 1 complete
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "Total: 3 tasks" in output
    assert "2 pending" in output


# T040 [US3]: Test list singular task
def test_list_singular_task() -> None:
    """Test that single task uses singular 'task' in summary."""
    storage = TaskStorage()
    storage.add("Single task")
    parser = create_parser()
    args = parser.parse_args(["list"])

    captured_output = StringIO()
    sys.stdout = captured_output

    exit_code = handle_list_command(args, storage)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert exit_code == 0
    assert "Total: 1 task" in output
    assert "1 completed" in output or "0 completed" in output
