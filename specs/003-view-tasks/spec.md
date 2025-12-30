# Feature Specification: View All Todo Tasks

**Feature Branch**: `003-view-tasks`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Feature: View All Todo Tasks..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - List All Tasks (Priority: P1)

As a user, I want to see all my tasks with their details so that I can review what needs to be done.

**Why this priority**: Viewing tasks is the primary way users interact with their todo list. Without this feature, users cannot see their tasks at all. This is the foundational feature for task management.

**Independent Test**: Can be fully tested by running `python main.py list` with varying task states and verifying the output format and content.

**Acceptance Scenarios**:

1. **Given** the user has 2 tasks (one incomplete, one complete), **When** they run `list`, **Then** both tasks are displayed in ID order with correct status indicators
2. **Given** the user has no tasks, **When** they run `list`, **Then** they see "No tasks found" message
3. **Given** the user has 5 tasks, **When** they run `list`, **Then** a summary line shows "Total: 5 tasks (X completed, Y pending)"

---

### User Story 2 - Read Task Details (Priority: P2)

As a user, I want to see each task's title and description clearly formatted so that I can easily read and understand my tasks.

**Why this priority**: Clear presentation of task details helps users quickly scan and find what they need. This is essential for task review and prioritization.

**Independent Test**: Can be tested by creating tasks with long titles and descriptions, then verifying the output remains readable.

**Acceptance Scenarios**:

1. **Given** a task has title "Buy groceries" and description "Milk, eggs, bread", **When** displayed in list, **Then** both are shown in readable format
2. **Given** a task has a title of 100 characters, **When** displayed in list, **Then** the title is fully visible without truncation
3. **Given** a task has no description, **When** displayed in list, **Then** "(none)" is shown instead of blank

---

### User Story 3 - Identify Task Status (Priority: P2)

As a user, I want to quickly see which tasks are complete and which are pending so that I can focus on what remains.

**Why this priority**: Status visibility is crucial for task management. Users need to distinguish completed from pending tasks at a glance.

**Independent Test**: Can be tested by creating tasks with both statuses and verifying correct symbols are displayed.

**Acceptance Scenarios**:

1. **Given** an incomplete task, **When** displayed in list, **Then** it shows "[ID] ✗" with empty circle or cross
2. **Given** a complete task, **When** displayed in list, **Then** it shows "[ID] ✓" with checkmark
3. **Given** mixed tasks, **When** displayed in list, **Then** the summary correctly counts completed and pending

---

### Edge Cases

- **Empty storage**: System displays "No tasks found" message when no tasks exist
- **Long titles**: Titles are fully visible (no truncation) - display wraps or scrolls gracefully
- **Long descriptions**: Descriptions are fully visible (no truncation) - display wraps gracefully
- **Only completed tasks**: List shows all with ✓, summary counts all as completed
- **Only incomplete tasks**: List shows all with ✗, summary counts all as pending
- **Unicode characters**: Task titles and descriptions with international characters display correctly
- **Special characters**: Emojis and special symbols in titles/descriptions display correctly

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display all tasks when `list` command is executed
- **FR-002**: System MUST show tasks in ascending order by ID (creation order)
- **FR-003**: System MUST display for each task: ID number, title, description, and status indicator
- **FR-004**: System MUST use "✓" symbol for completed tasks and "✗" symbol for incomplete tasks
- **FR-005**: System MUST display a summary line showing total tasks, completed count, and pending count
- **FR-006**: System MUST display "(none)" when a task has no description
- **FR-007**: System MUST display "No tasks found" message when storage is empty
- **FR-008**: System MUST wrap long titles and descriptions to maintain readability
- **FR-009**: System MUST support Unicode characters in titles and descriptions

### Key Entities

- **Task**: Existing entity with id, title, description, status, created_at attributes (no changes needed)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view all tasks in under 1 second (command execution time)
- **SC-002**: 100% of tasks are displayed with correct information (ID, title, description, status)
- **SC-003**: Summary counts match actual task states 100% of the time
- **SC-004**: Empty list displays "No tasks found" message correctly
- **SC-005**: Output format matches specification for all edge cases (empty, long text, Unicode)
- **SC-006**: List command works with any combination of task states (all complete, all incomplete, mixed)

## CLI Interface Examples

### Command Format

```bash
python main.py list
```

### Successful Output (with tasks)

```
TODO LIST:
────────────────────────────────────
[1] ✗ Buy groceries
    Milk, eggs, bread

[2] ✓ Call dentist
    Schedule appointment

Total: 2 tasks (1 completed, 1 pending)
```

### Successful Output (empty)

```
TODO LIST:
────────────────────────────────────
No tasks found
```

### Output with Unicode

```
TODO LIST:
────────────────────────────────────
[1] ✗ Café meeting
    Discuss 中文 documentation 🎉

Total: 1 task (0 completed, 1 pending)
```

## Dependencies & Assumptions

### Dependencies

- TaskStorage.list_all() method returns all tasks in creation order
- Task dataclass with id, title, description, status fields
- Existing CLI infrastructure (argparse, command routing)

### Assumptions

- Tasks are already stored in memory (in-memory storage)
- Output format is flexible; exact spacing may vary but follows readability principle
- Summary uses format: "Total: N tasks (X completed, Y pending)" or singular "task" when N=1
- Status symbols: "✓" for complete, "✗" for incomplete (Unicode checkmark and cross marks)
