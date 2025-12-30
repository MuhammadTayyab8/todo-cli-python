# Quickstart: View Tasks Feature

**Feature**: 003-view-tasks
**Date**: 2025-12-29

## Command Format

```bash
python main.py list
```

## Basic Usage

### List All Tasks

```bash
$ python main.py list

TODO LIST:
────────────────────────────────────
[1] ✗ Buy groceries
    Milk, eggs, bread

[2] ✓ Call dentist
    Schedule appointment

Total: 2 tasks (1 completed, 1 pending)
```

### Empty Task List

```bash
$ python main.py list

TODO LIST:
────────────────────────────────────
No tasks found
```

### Single Task

```bash
$ python main.py list

TODO LIST:
────────────────────────────────────
[1] ✗ Weekly review
    Complete all pending tasks

Total: 1 task (0 completed, 1 pending)
```

### With Unicode

```bash
$ python main.py list

TODO LIST:
────────────────────────────────────
[1] ✗ Café meeting
    Discuss 中文 documentation 🎉

Total: 1 task (0 completed, 1 pending)
```

## Key Points

1. **Order**: Tasks shown in creation order (ID ascending)
2. **Status Symbols**: ✓ for complete, ✗ for incomplete
3. **Empty Description**: Shows "(none)" instead of blank
4. **Summary**: Shows total count with completed/pending breakdown
5. **Singular/Plural**: Uses "task" for 1, "tasks" for 0 or 2+

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (always, even for empty list) |

## See Also

- `python main.py add` - Add new tasks
- `python main.py update` - Update tasks
- `python main.py delete` - Delete tasks
- Feature spec: `specs/003-view-tasks/spec.md`
