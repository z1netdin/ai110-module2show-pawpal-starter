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

## Implementation Summary

The backend logic lives in `pawpal_system.py`, with four classes:

- **`Task`** — a single care activity (title, duration, priority, optional recurrence, completed flag, and an auto-generated `id`). A `Task` can also point to another task via `depends_on`, so one task can be required to happen before another (e.g. a pee break before a meal).
- **`Pet`** — holds a pet's basic info and its list of `Task`s. `add_task()`/`remove_task()` keep the task's back-link to its pet in sync.
- **`Owner`** — holds a list of `Pet`s and exposes `get_all_tasks()`, which flattens every pet's tasks into one list. This is what lets the system support multiple pets.
- **`Scheduler`** — the planning logic. `generate_plan(owner)` pulls tasks from `owner.get_all_tasks()` (never from a single pet directly), orders them by priority while respecting any `depends_on` constraints, then greedily fits as many as it can into `available_time_minutes`. `explain_choice(task)` gives a one-line reason for each task.

`Task` and `Pet` are implemented as Python dataclasses since they're mostly data; `Owner` and `Scheduler` are regular classes since they do more active work. `main.py` is a small terminal script that wires these classes together and prints the resulting schedule — it's the easiest way to see the logic run without the Streamlit UI. `app.py` is still just the UI shell from the starter template and isn't yet connected to this logic.

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

Terminal output from running `python main.py`:

```
Today's Schedule
------------------------------
[Sohpia] Pee break - 5 min (priority: high)
[Milo] Feeding - 10 min (priority: high)
[Sohpia] Morning walk - 30 min (priority: medium)
```

Note the ordering rules baked into this routine: pee break always happens right before a meal, and the snack comes right after the evening walk but dinner is deliberately later rather than back-to-back.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

|       Feature     |                        Method(s)                           |                                                           Notes                             |
|---------          |------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Task sorting      | `Scheduler.sort_by_time()`, `Scheduler.sort_by_duration()` | Sorts by `start_time` ("HH:MM", untimed tasks last) or by `duration_minutes`. Separate from `generate_plan()`'s own priority/dependency ordering. |
| Filtering         | `Owner.filter_tasks(pet_name=None, completed=None)`        | Narrows tasks by pet name and/or completion status; either filter is optional and they can be combined. |
| Conflict handling |              `Scheduler.detect_conflicts(owner)`           | Groups all of an owner's timed tasks by `start_time` across every pet; any time shared by 2+ tasks returns a warning message (never raises). Tradeoff: checks for an exact `start_time` match, not true overlapping durations — see `reflection.md` section 2b. |
| Recurring tasks   |        `Task.mark_done()`, `Task._spawn_next_occurrence()` | Completing a `"daily"`/`"weekly"` task spawns a brand-new `Task` instance due `today + timedelta(days=1 or 7)`, attached to the same pet. The original instance stays completed as history. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
