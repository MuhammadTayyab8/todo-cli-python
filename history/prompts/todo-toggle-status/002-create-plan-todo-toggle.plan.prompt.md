---
id: 2
title: Create implementation plan for Todo toggle
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-toggle-status
branch: 1-todo-toggle-status
user: global
command: sp.plan
labels: [todo, plan, architecture, status-toggle]
links:
  spec: specs/1-todo-toggle-status/spec.md
  ticket: null
  adr: history/adr/007-completion-status-strategy.md
  pr: null
files:
 - specs/1-todo-toggle-status/plan.md
 - specs/1-todo-toggle-status/research.md
 - specs/1-todo-toggle-status/data-model.md
tests:
 - null
---

## Prompt

Create implementation plan for "Mark Complete" feature.

Generate plan.md with:

1. Architectural Decisions:
   ADR-007: Completion Status Strategy
   - Decision: Single 'complete' command with toggle behavior
   - Rationale: Simpler, fewer commands to remember
   - Alternative: Separate complete/incomplete commands

2. Component Design:
   - storage.py: Add toggle_complete(id: int) method
   - cli.py: Add 'complete' subcommand
   - Return Task with new status

3. Implementation Approach:
   - Find task by ID
   - Toggle completed boolean
   - Return updated task

4. Testing Strategy:
   - Test mark incomplete → complete
   - Test mark complete → incomplete
   - Test non-existent ID
   - Test toggle multiple times

Simplest approach: toggle boolean flag.

## Response snapshot

Created a detailed implementation plan including ADR-007, data model changes, and a comprehensive testing strategy. Research.md confirms the toggle behavior and string-based status management to align with existing code. Components affected: storage.py, cli.py, and main.py.

## Outcome

- ✅ Impact: Provided a clear technical roadmap for the toggle feature.
- 🧪 Tests: Detailed unit and integration test cases defined.
- 📁 Files: Created plan.md, research.md, and data-model.md.
- 🔁 Next prompts: Run /sp.tasks to generate the task list.
- 🧠 Reflection: Aligning with the existing string-based status vs a boolean flag (as requested by user) preserves model consistency while still delivering the requested toggle behavior.

## Evaluation notes (flywheel)

- Failure modes observed: None in this stage.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
