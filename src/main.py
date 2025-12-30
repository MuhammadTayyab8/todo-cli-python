"""Main entry point for the todo application."""

import sys

from src.cli import (
    create_parser,
    handle_add_command,
    handle_delete_command,
    handle_list_command,
    handle_update_command,
)
from src.storage import TaskStorage


def main() -> int:
    """
    Main entry point for the todo application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Ensure UTF-8 encoding for stdout/stderr (Windows compatibility)
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.stderr.encoding != "utf-8" and hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    # Create storage instance
    storage = TaskStorage()

    # Create parser and parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Route to command handler
    if args.command == "add":
        return handle_add_command(args, storage)
    elif args.command == "delete":
        return handle_delete_command(args, storage)
    elif args.command == "update":
        return handle_update_command(args, storage)
    elif args.command == "list":
        return handle_list_command(args, storage)
    elif args.command == "complete":
        from src.cli import handle_complete_command

        return handle_complete_command(args, storage)

    # Unknown command (should not reach here due to argparse validation)
    return 1


if __name__ == "__main__":
    sys.exit(main())
