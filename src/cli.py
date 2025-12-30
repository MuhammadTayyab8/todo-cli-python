"""CLI argument parsing and command handlers."""

import argparse
import sys

from src.models import Task
from src.storage import TaskStorage
from src.validators import validate_description, validate_title


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="todo", description="Simple CLI todo application"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title (1-100 characters)")
    add_parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Task description (max 500 characters, optional)",
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task by ID")
    delete_parser.add_argument(
        "task_id",
        type=str,
        help="Task ID to delete (positive integer)",
    )

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task by ID")
    update_parser.add_argument(
        "task_id",
        type=str,
        help="Task ID to update (positive integer)",
    )
    update_parser.add_argument(
        "--title",
        type=str,
        default=None,
        help="New task title (1-100 characters)",
    )
    update_parser.add_argument(
        "--desc",
        type=str,
        default=None,
        help="New task description (max 500 characters, empty string clears)",
    )

    # List command
    subparsers.add_parser("list", help="List all tasks")

    return parser


def format_success_message(task: Task) -> str:
    """
    Format task details as success message.

    Args:
        task: The Task instance to format

    Returns:
        Formatted multi-line success message
    """
    lines = [
        "Task added successfully!",
        f"ID: {task.id}",
        f"Title: {task.title}",
    ]

    if task.description:
        lines.append(f"Description: {task.description}")
    else:
        lines.append("Description: (none)")

    lines.append(f"Status: {task.status}")

    return "\n".join(lines)


def format_error_message(error: str) -> str:
    """
    Format error message with 'Error: ' prefix.

    Args:
        error: The error message

    Returns:
        Formatted error message
    """
    if error.startswith("Error: "):
        return error
    return f"Error: {error}"


def handle_add_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle 'todo add' command.

    Args:
        args: Parsed arguments from argparse
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate title
    title_valid, title_error = validate_title(args.title)
    if not title_valid:
        error_msg = format_error_message(title_error)
        print(error_msg, file=sys.stderr)
        return 1

    # Validate description if provided
    if args.description is not None:
        desc_valid, desc_error = validate_description(args.description)
        if not desc_valid:
            error_msg = format_error_message(desc_error)
            print(error_msg, file=sys.stderr)
            return 1

    # Create task
    task = storage.add(args.title.strip(), args.description)

    # Print success message to stdout
    success_msg = format_success_message(task)
    print(success_msg)

    return 0


def handle_delete_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle the delete command.

    Validates the task ID, attempts deletion, and prints appropriate
    success or error messages.

    Args:
        args: Parsed command-line arguments with task_id attribute
        storage: TaskStorage instance to delete from

    Returns:
        Exit code: 0 for success, 1 for error

    Examples:
        >>> from argparse import Namespace
        >>> storage = TaskStorage()
        >>> task = storage.add("Test task")
        >>> args = Namespace(task_id="1")
        >>> handle_delete_command(args, storage)
        Task deleted successfully (ID: 1)
        0
    """
    from src.validators import validate_task_id

    # Validate task ID format
    is_valid, error_msg, task_id = validate_task_id(args.task_id)
    if not is_valid:
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1

    # At this point, task_id is guaranteed to be int (not None) due to validation
    assert task_id is not None

    # Attempt deletion
    was_deleted = storage.delete(task_id)

    # Format and print appropriate message
    if was_deleted:
        success_msg = f"Task deleted successfully (ID: {task_id})"
        print(success_msg)
        return 0
    else:
        error_msg = f"Task not found (ID: {task_id})"
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1


def format_update_success_message(task: Task) -> str:
    """
    Format task details as update success message.

    Args:
        task: The updated Task instance to format

    Returns:
        Formatted multi-line success message
    """
    lines = [
        "Task updated successfully",
        f"ID: {task.id}",
        f"Title: {task.title}",
    ]

    if task.description:
        lines.append(f"Description: {task.description}")
    else:
        lines.append("Description: (none)")

    lines.append(f"Status: {task.status}")

    return "\n".join(lines)


def handle_update_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle the update command.

    Validates the task ID and update arguments, performs the update, and prints
    appropriate success or error messages.

    Args:
        args: Parsed command-line arguments with task_id, title, desc attributes
        storage: TaskStorage instance to update in

    Returns:
        Exit code: 0 for success, 1 for error

    Examples:
        >>> from argparse import Namespace
        >>> storage = TaskStorage()
        >>> task = storage.add("Test task", "Original description")
        >>> args = Namespace(task_id="1", title="Updated task", desc=None)
        >>> handle_update_command(args, storage)
        Task updated successfully
        ID: 1
        Title: Updated task
        Description: Original description
        Status: incomplete
        0
    """
    from src.validators import validate_task_id

    # Validate task ID format
    is_valid, error_msg, task_id = validate_task_id(args.task_id)
    if not is_valid:
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1

    # At this point, task_id is guaranteed to be int (not None) due to validation
    assert task_id is not None

    # Check at least one of --title or --desc is provided
    if args.title is None and args.desc is None:
        error_output = format_error_message(
            "At least one of --title or --desc must be provided"
        )
        print(error_output, file=sys.stderr)
        return 1

    # Validate title if provided
    if args.title is not None:
        title_valid, title_error = validate_title(args.title)
        if not title_valid:
            error_output = format_error_message(title_error)
            print(error_output, file=sys.stderr)
            return 1

    # Validate description if provided
    if args.desc is not None:
        desc_valid, desc_error = validate_description(args.desc)
        if not desc_valid:
            error_output = format_error_message(desc_error)
            print(error_output, file=sys.stderr)
            return 1

    # Attempt update
    updated_task = storage.update(task_id, title=args.title, description=args.desc)

    # Format and print appropriate message
    if updated_task is not None:
        success_msg = format_update_success_message(updated_task)
        print(success_msg)
        return 0
    else:
        error_msg = f"Task not found (ID: {task_id})"
        error_output = format_error_message(error_msg)
        print(error_output, file=sys.stderr)
        return 1


def format_list_header() -> str:
    """
    Format the list command header.

    Returns:
        Formatted header with divider line
    """
    return "TODO LIST:\n────────────────────────────────────"


def format_list_empty() -> str:
    """
    Format the empty list message.

    Returns:
        Formatted empty list message
    """
    return "No tasks found"


def format_summary(tasks: list[Task]) -> str:
    """
    Format task summary with counts.

    Args:
        tasks: List of Task objects to summarize

    Returns:
        Formatted summary string like "Total: 3 tasks (1 completed, 2 pending)"
    """
    total = len(tasks)
    completed = sum(1 for task in tasks if task.status == "complete")
    pending = total - completed

    # Handle singular/plural for total
    if total == 1:
        total_str = "1 task"
    else:
        total_str = f"{total} tasks"

    return f"Total: {total_str} ({completed} completed, {pending} pending)"


def format_list_output(tasks: list[str], summary: str = "") -> str:
    """
    Format the full list output.

    Args:
        tasks: List of formatted task strings
        summary: Summary string to append (optional)

    Returns:
        Complete formatted list output
    """
    if not tasks:
        return format_list_header() + "\n" + format_list_empty()

    header = format_list_header()
    output = header + "\n" + "\n".join(tasks)

    if summary:
        output += "\n" + summary

    return output


def handle_list_command(args: argparse.Namespace, storage: TaskStorage) -> int:
    """
    Handle 'todo list' command.

    Lists all tasks with their details in a readable format.

    Args:
        args: Parsed arguments (no specific args for list)
        storage: TaskStorage instance

    Returns:
        Exit code (0 for success, list command always succeeds)

    Examples:
        >>> from argparse import Namespace
        >>> storage = TaskStorage()
        >>> storage.add("Buy groceries", "Milk and eggs")
        >>> args = Namespace()
        >>> handle_list_command(args, storage)
        TODO LIST:
        ───────────────────────────────────
        [1] ✗ Buy groceries
            Milk and eggs
        Total: 1 task (0 completed, 1 pending)
        0
    """
    # Get all tasks formatted for display
    task_lines = storage.list_tasks()

    # Get all tasks for summary
    all_tasks = storage.list_all()

    # Generate summary
    summary = format_summary(all_tasks) if all_tasks else ""

    # Format and print the output
    output = format_list_output(task_lines, summary)
    print(output)

    return 0
