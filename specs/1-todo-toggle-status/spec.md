# Feature Specification: Mark Todo Task Complete/Incomplete

**Feature Branch**: `1-todo-toggle-status`
**Created**: 2025-12-30
**Status**: Draft
**Input**: User description: "Generate specification for Mark Complete feature. Requirements: User can toggle task completion status by ID. Mark incomplete task as complete (✗ → ✓). Mark complete task as incomplete (✓ → ✗). Error if task ID doesn't exist. Show new status after change."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Toggle Task Status (Priority: P1)

As a user, I want to toggle the completion status of an existing task by its ID so that I can easily keep track of what I have finished and what still needs to be done without using multiple commands.

**Why this priority**: Core functionality of the feature. Toggling is the most intuitive single-command interaction for status updates.

**Independent Test**: Can be fully tested by creating a task and toggling its status multiple times.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 is currently "incomplete", **When** the user runs the command to complete task 1, **Then** the task status changes to "complete" and a success message is shown.
2. **Given** a task with ID 1 is currently "complete", **When** the user runs the command to complete task 1, **Then** the task status changes to "incomplete" and a success message is shown.

---

### User Story 2 - Error Handling for Non-existent Tasks (Priority: P2)

As a user, I want to be informed if I try to toggle a task that doesn't exist so that I can correct my input.

**Why this priority**: Critical for usability and preventing confusion.

**Independent Test**: Attempt to toggle a status for an ID that has not been created.

**Acceptance Scenarios**:

1. **Given** no task exists with ID 99, **When** the user runs the command to complete task 99, **Then** an error message is displayed stating the task does not exist.

---

### Edge Cases

- **Invalid ID Format**: How does the system handle an ID that is not a number (e.g., "abc")? -> System should report an invalid ID format error.
- **Empty Task List**: Toggling when no tasks exist at all. -> System should report that the specific ID was not found.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a single command to toggle the status of a task by its numeric ID.
- **FR-002**: System MUST change an incomplete task to complete (✓) when toggled.
- **FR-003**: System MUST change a complete task to incomplete (✗) when toggled.
- **FR-004**: System MUST display a confirmation message indicating the new status and the task ID after a successful toggle.
- **FR-005**: System MUST validate that the provided ID exists in the system before attempting to toggle.
- **FR-006**: System MUST return a clear error message if the ID provided does not exist.

### Key Entities

- **Task**: Represents a todo item.
  - **ID**: Unique numeric identifier.
  - **Status**: The completion state (Complete or Incomplete).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can toggle the status of a task using a single CLI command with one argument (ID).
- **SC-002**: 100% of status changes are persisted accurately across sessions.
- **SC-003**: Error messages for missing IDs are displayed in under 5 seconds (standard CLI expectation).
- **SC-004**: Confirmation messages clearly distinguish between "completed" and "incomplete" states using visual cues (like checkmarks/crosses).
