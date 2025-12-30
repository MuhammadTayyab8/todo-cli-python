---
id: 002
title: Clarify Update Task Specification
stage: spec
date: 2025-12-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-update-task
branch: 001-update-task
user: system
command: /sp.clarify
labels: ["clarification", "update-task", "specification", "output-format"]
links:
  spec: specs/001-update-task/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-update-task/spec.md
tests:
  - null
---

## Prompt

Review "Update Task" specification.

Clarify:
1. Should update require at least one field (title OR description)?
2. Can title be updated to empty string?
3. Should update show before/after values?
4. Timestamp: Do we need updated_at field now?
5. Validation: Same rules as Add (100 chars title, 500 desc)?
6. Should update accept partial matches or exact ID only?

Consider future features and consistency.

## Response snapshot

Performed structured ambiguity analysis against user's 6 questions:

**Already Addressed in Spec (5 of 6)**:
1. Require at least one field → FR-004 (yes, at least --title or --desc required)
2. Title to empty string → Edge Cases (rejected with error)
3. Need updated_at field → Out of Scope (no, not for this feature)
4. Same validation as Add → Assumption #6 (yes, same rules)
5. Partial matches or exact ID → FR-005/FR-006 (exact ID only)

**Clarification Needed (1 of 6)**:
3. Show before/after values → Asked user, answered: Option A (show only final values)

**Decision Recorded**:
- Q: Should update show before/after values or only final state?
- A: Show only final values (consistent with Add/Delete, minimal output, scriptable)

Updated FR-013 to explicitly state "no before/after diff".

## Outcome

- ✅ Impact: Clarified output format decision, updated spec with session record
- 🧪 Tests: No test changes needed (output format already tested as final-only)
- 📁 Files: 1 file modified (spec.md - added Clarifications section, updated FR-013)
- 🔁 Next prompts: /sp.plan to create implementation plan
- 🧠 Reflection: Most questions were already addressed in original spec; only 1 true ambiguity found

## Evaluation notes (flywheel)

- Failure modes observed: None - user questions were well-formed and answerable
- Graders run and results (PASS/FAIL): All 6 questions resolved (5 pre-existing, 1 clarified)
- Prompt variant (if applicable): Standard /sp.clarify flow with user-provided focus questions
- Next experiment (smallest change to try): None needed - proceed to planning phase
