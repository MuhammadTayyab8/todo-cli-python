# Quickstart: Update Task Feature

**Feature**: 001-update-task
**Date**: 2025-12-29

## Command Format

```bash
python main.py update <task_id> [--title <text>] [--desc <text>]
```

## Basic Usage

### Update Title Only

```bash
# Update task 1's title
python main.py update 1 --title "New task title"
```

### Update Description Only

```bash
# Update task 1's description
python main.py update 1 --desc "New detailed description"
```

### Update Both Title and Description

```bash
# Update both fields at once
python main.py update 1 --title "New title" --desc "New description"
```

### Clear Description

```bash
# Clear the description (set to empty)
python main.py update 1 --desc ""
```

## Example Session

```bash
# First, add a task
$ python main.py add "Buy groceries"
Task added successfully!
ID: 1
Title: Buy groceries
Description: (none)
Status: incomplete

# Update the title
$ python main.py update 1 --title "Buy weekly groceries"
Task updated successfully
  ID: 1
  Title: Buy weekly groceries
  Description: (none)
  Status: incomplete

# Add a description
$ python main.py update 1 --desc "Milk, eggs, bread, cheese"
Task updated successfully
  ID: 1
  Title: Buy weekly groceries
  Description: Milk, eggs, bread, cheese
  Status: incomplete

# Update both
$ python main.py update 1 --title "Shopping" --desc "Saturday morning shopping"
Task updated successfully
  ID: 1
  Title: Shopping
  Description: Saturday morning shopping
  Status: incomplete
```

## Error Handling

### Task Not Found

```bash
$ python main.py update 999 --title "New title"
Error: Task not found (ID: 999)
```

### Invalid Task ID

```bash
$ python main.py update abc --title "New title"
Error: Task ID must be a positive integer
```

### No Update Arguments

```bash
$ python main.py update 1
Error: At least one of --title or --desc must be provided
```

### Empty Title

```bash
$ python main.py update 1 --title ""
Error: Title cannot be empty
```

### Title Too Long

```bash
$ python main.py update 1 --title "[101+ characters...]"
Error: Title must be between 1 and 100 characters (received 101)
```

### Description Too Long

```bash
$ python main.py update 1 --desc "[501+ characters...]"
Error: Description cannot exceed 500 characters (received 501)
```

## Key Points

1. **At least one argument required**: Must provide `--title`, `--desc`, or both
2. **Partial updates**: Unchanged fields are preserved
3. **Status preserved**: Update never changes completion status
4. **Title trimmed**: Leading/trailing whitespace removed from title
5. **Description preserved**: Whitespace in description is kept as-is
6. **Clear description**: Use `--desc ""` to clear description

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (validation, not found, etc.) |

## See Also

- `python main.py add` - Add new tasks
- `python main.py delete` - Delete tasks
- Feature spec: `specs/001-update-task/spec.md`
