---
id: 1
title: Generate spec for Todo toggling
stage: spec
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-toggle-status
branch: 1-todo-toggle-status
user: global
command: sp.specify
labels: [todo, specification, status-toggle]
links:
  spec: specs/1-todo-toggle-status/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-todo-toggle-status/spec.md
 - specs/1-todo-toggle-status/checklists/requirements.md
tests:
 - null
---

## Prompt

Feature: Mark Todo Task Complete/Incomplete

Generate specification for "Mark Complete" feature.

Requirements:
- User can toggle task completion status by ID
- Mark incomplete task as complete (✗ → ✓)
- Mark complete task as incomplete (✓ → ✗)
- Error if task ID doesn't exist
- Show new status after change

Include:
1. User Story
2. Acceptance Criteria:
   - Mark incomplete → complete: Success
   - Mark complete → incomplete: Success (toggle)
   - Mark non-existent ID → Error
3. CLI Interface examples:
```bash
   $ python main.py complete 1
   ✓ Task marked as complete (ID: 1)

   $ python main.py complete 1
   ✗ Task marked as incomplete (ID: 1)

   # OR separate commands:
   $ python main.py complete 1
   $ python main.py incomplete 1
```
4. Design Decision:
   - Single toggle command OR separate complete/incomplete commands?
5. Edge Cases:
   - Invalid ID
   - Already in desired state (warn or silent success?)
6. Testing Requirements

Choose approach that's most intuitive for users.

## Response snapshot

Generated a comprehensive feature specification (spec.md) and quality checklist (requirements.md) for toggling todo task status. The design favors a single toggle command for better CLI ergonomics. Created branch 1-todo-toggle-status and initialized the folder structure.

## Outcome

- ✅ Impact: Established a clear, testable specification for the status toggle feature.
- 🧪 Tests: No tests run yet; testing requirements defined in spec.
- 📁 Files: Created spec.md and requirements.md.
- 🔁 Next prompts: Run /sp.plan to design the implementation.
- 🧠 Reflection: Using a single toggle command simplifies the CLI interface while still covering both "complete" and "incomplete" transitions.

## Evaluation notes (flywheel)

- Failure modes observed: pwsh script failed due to missing pwsh in environment; handled via manual setup.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
