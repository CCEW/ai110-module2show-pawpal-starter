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

### Features

- Sorting by time: tasks are ordered by preferred time using Scheduler.sort_tasks_by_preferred_time() and the final plan is sorted chronologically with Scheduler.sort_schedule_by_time().
- Filtering by pet or status: the scheduler can show tasks for a specific pet or only pending/completed tasks with Scheduler.filter_tasks().
- Conflict warnings: overlapping tasks are detected with Scheduler.detect_conflicts() and Scheduler.has_time_conflict(), and the UI warns the owner when a schedule would overlap.
- Daily recurrence: recurring tasks can be marked complete and will generate the next instance for the following day with Task.mark_complete().
- Daily plan generation: Scheduler.generate_daily_plan() builds a practical schedule by prioritizing higher-value tasks and respecting the owner’s available window.

## 📸 Demo Walkthrough

The PawPal+ app lets an owner manage pet care tasks and preview a realistic daily plan in a few simple steps:

1. Open the Streamlit app and enter the owner name, pet name, and a few care tasks such as a walk, feeding, or grooming.
2. Add tasks with a duration, priority, and optional preferred time. The task list is filtered for the selected pet and sorted by preferred time.
3. Click “Generate schedule” to create a daily plan. The scheduler orders tasks by importance and time preferences, then places them into the available window.
4. Review the generated schedule and any conflict warnings. If two tasks overlap, the app explains the conflict and suggests changing the task time or availability.
5. Use the built-in conflict adjustment option to change a task’s preferred time and regenerate the plan until it fits the day smoothly.

The scheduler also demonstrates key behaviors in the CLI demo by showing sorting, filtering, conflict detection, and daily plan generation.

```text
$ python main.py
Total tasks: 6
  - Evening walk (Biscuit) [18:00] 30 min, priority 8, done
  - Morning feeding (Biscuit) [08:15] 10 min, priority 9, pending
  - Afternoon brushing (Biscuit) [15:30] 15 min, priority 6, pending
  - Midday play (Whiskers) [12:00] 20 min, priority 8, pending
  - Litter box cleaning (Whiskers) [09:45] 5 min, priority 7, pending
  - Evening feeding (Whiskers) [19:00] 10 min, priority 9, pending

Tasks sorted by preferred time:
  - 08:15 Morning feeding (Biscuit)
  - 09:45 Litter box cleaning (Whiskers)
  - 12:00 Midday play (Whiskers)
  - 15:30 Afternoon brushing (Biscuit)
  - 18:00 Evening walk (Biscuit)
  - 19:00 Evening feeding (Whiskers)

Warning:
Conflict detected: 'Conflicting bath' for 'Whiskers' overlaps an existing scheduled task at 08:00.

Today's Schedule
Daily Plan for Biscuit, Whiskers
================================
Available window: 08:00 - 16:00

Time              Task                         Pet          Pri
----------------- ---------------------------- ------------ ---
08:00 - 08:10     Morning feeding              Biscuit      9
08:15 - 08:25     Evening feeding              Whiskers     9
08:30 - 08:50     Midday play                  Whiskers     8
08:55 - 09:00     Litter box cleaning          Whiskers     7
09:05 - 09:20     Afternoon brushing           Biscuit      6