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
