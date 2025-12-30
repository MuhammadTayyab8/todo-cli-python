"""Integration tests for the 'complete' command."""

import pytest
from src.cli import create_parser, handle_complete_command
from src.storage import TaskStorage
from argparse import Namespace

def test_complete_command_success(tmp_path, capsys):
    """Test full CLI flow for toggling a task status."""
    storage_file = tmp_path / "tasks.json"
    storage = TaskStorage(storage_file=storage_file)
    task = storage.add("Test task")

    # Mock args for 'todo complete 1'
    args = Namespace(command="complete", task_id="1")
    exit_code = handle_complete_command(args, storage)

    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Task marked as complete" in captured.out
    assert "(ID: 1)" in captured.out

    # Verify state in storage
    assert storage.get(1).status == "complete"

def test_complete_command_toggle_behavior(tmp_path, capsys):
    """Test that running the command twice toggles status back."""
    storage_file = tmp_path / "tasks.json"
    storage = TaskStorage(storage_file=storage_file)
    task = storage.add("Test task")

    args = Namespace(command="complete", task_id="1")

    # Toggle to complete
    handle_complete_command(args, storage)
    capsys.readouterr()

    # Toggle to incomplete
    exit_code = handle_complete_command(args, storage)
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "Task marked as incomplete" in captured.out
    assert storage.get(1).status == "incomplete"

def test_complete_command_non_existent_id(tmp_path, capsys):
    """Test error message for non-existent numeric ID."""
    storage_file = tmp_path / "tasks.json"
    storage = TaskStorage(storage_file=storage_file)

    args = Namespace(command="complete", task_id="999")
    exit_code = handle_complete_command(args, storage)

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error: Task not found (ID: 999)" in captured.err

def test_complete_command_invalid_id_format(tmp_path, capsys):
    """Test error message for non-numeric ID."""
    storage = TaskStorage(storage_file=tmp_path / "tasks.json")

    args = Namespace(command="complete", task_id="abc")
    exit_code = handle_complete_command(args, storage)

    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error:" in captured.err
