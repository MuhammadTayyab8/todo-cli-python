# Manual Test Commands

Run these commands one by one to test all CRUD operations. Tasks are now saved to `tasks.json` and persist between commands.

---

## CREATE (Add Tasks)

```powershell
# Create task 1: Buy groceries
uv run python -m src.main add "Buy groceries" --description "Milk, eggs, bread"

# Create task 2: Call dentist
uv run python -m src.main add "Call dentist" --description "Schedule appointment"

# Create task 3: Write report
uv run python -m src.main add "Write report" --description "Q4 performance review"
```

---

## READ (View Tasks)

```powershell
# View all tasks
uv run python -m src.main list
```

**Expected Output:**
```
TODO LIST:
────────────────────────────────────
[1] ✗ Buy groceries
    Milk, eggs, bread
[2] ✗ Call dentist
    Schedule appointment
[3] ✗ Write report
    Q4 performance review

Total: 3 tasks (0 completed, 3 pending)
```

---

## UPDATE (Edit Tasks)

```powershell
# Update task 2 - change description
uv run python -m src.main update 2 --desc "Appointment scheduled for next week"

# Update task 3 - change title
uv run python -m src.main update 3 --title "Write quarterly report"
```

---

## DELETE (Remove Tasks)

```powershell
# Delete task 1
uv run python -m src.main delete 1
```

---

## Full Workflow Test

```powershell
# 1. Add tasks
uv run python -m src.main add "Buy groceries" --description "Milk, eggs, bread"
uv run python -m src.main add "Call dentist" --description "Schedule appointment"

# 2. View tasks
uv run python -m src.main list

# 3. Update task 2
uv run python -m src.main update 2 --desc "Appointment confirmed"

# 4. View updated list
uv run python -m src.main list

# 5. Delete task 1
uv run python -m src.main delete 1

# 6. View final list
uv run python -m src.main list
```

---

## Test Edge Cases

```powershell
# Create task with no description
uv run python -m src.main add "Simple task"

# View task with "(none)" description
uv run python -m src.main list
```

---

## Clear All Data

```powershell
# Delete tasks.json to reset all data
Remove-Item tasks.json
```
