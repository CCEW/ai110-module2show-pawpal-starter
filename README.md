# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
Daily Plan for Biscuit, Whiskers
================================
Available window: 08:00 - 16:00

Time              Task                         Pet          Pri
----------------- ---------------------------- ------------ ---
08:00 - 08:30     Morning walk                 Biscuit      9
08:35 - 08:45     Feeding                      Biscuit      9
08:50 - 09:00     Feeding                      Whiskers     9
09:05 - 09:35     Evening walk                 Biscuit      8
09:40 - 10:00     Playtime                     Whiskers     8
10:05 - 10:10     Litter box cleaning          Whiskers     7
```

## 🧪 Testing PawPal+

```bash
pytest -q
```
Confidence level 5 stars: ⭐⭐⭐⭐⭐
Sample test output:

```
tests\test_pawpal.py ..                                                                                                                                   [100%]

====================================================================== 6 passed in 0.07s =======================================================================

```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_tasks_by_preferred_time(), Scheduler.sort_schedule_by_time() | Sorts tasks by preferred time and orders the final schedule by start time. |
| Filtering | Scheduler.filter_tasks(), Scheduler.get_tasks_by_pet_name(), Scheduler.get_tasks_by_completion() | Filters tasks by pet name and/or completion status. |
| Conflict handling | Scheduler.detect_conflicts(), Scheduler.has_time_conflict(), Scheduler.schedule_task_with_warning() | Detects overlapping time slots and prevents conflicting placements. |
| Recurring tasks | Task.is_recurring(), Task.mark_complete(), Scheduler.complete_task() | Supports recurring tasks such as daily or weekly and creates the next instance after completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
