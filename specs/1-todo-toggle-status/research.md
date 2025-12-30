# Research: Mark Todo Task Complete/Incomplete

## Technical Context Analysis

The existing `Task` model used a string literal `"complete"` and `"incomplete"`.
The `TaskStorage` implements a pseudo-immutable update pattern where a new `Task` instance is created upon update.

## Findings

1. **Storage state**: Status is currently managed as a string.
2. **Persistence**: `TaskStorage` saves to `tasks.json`.
3. **Existing commands**: `add`, `delete`, `update`, `list`. All follow a consistent sub-command pattern using `argparse`.

## Decision Summary

- **Status Management**: We will continue using strings `"complete"` and `"incomplete"` to maintain compatibility with the existing `Task` model validation.
- **Command Name**: `complete`. While it's a toggle, the user requested the command name `complete` in their implementation notes.

## Alternatives Considered

1. **Enum for Status**: Refactoring to an `Enum` would be cleaner but is out of scope for a "Smallest Viable Change" as it might require updating all existing tests and handlers.
2. **Boolean `is_completed`**: Similar to above, requires model refactoring.
