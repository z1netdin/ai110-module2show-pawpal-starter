"""Logic layer for PawPal+. Backend classes live here; app.py only handles the UI."""

import itertools
from dataclasses import dataclass, field
from datetime import date, timedelta

_task_id_counter = itertools.count(1)

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
RECURRENCE_INTERVAL_DAYS = {"daily": 1, "weekly": 7}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    pet: "Pet | None" = None
    recurrence: str | None = None
    start_time: str | None = None
    completed: bool = False
    depends_on: "Task | None" = None
    last_completed_on: "date | None" = None
    due_date: "date | None" = None
    id: int = field(default_factory=lambda: next(_task_id_counter))

    def mark_done(self, today=None):
        """Mark this task as completed; a daily/weekly task spawns its next occurrence."""
        today = today or date.today()
        self.completed = True
        self.last_completed_on = today
        return self._spawn_next_occurrence(today)

    def _spawn_next_occurrence(self, today):
        """Create and attach a fresh instance of this task due on its next occurrence, if recurring."""
        if self.recurrence not in RECURRENCE_INTERVAL_DAYS:
            return None

        next_due_date = today + timedelta(days=RECURRENCE_INTERVAL_DAYS[self.recurrence])
        next_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurrence=self.recurrence,
            start_time=self.start_time,
            depends_on=self.depends_on,
            due_date=next_due_date,
        )
        if self.pet is not None:
            self.pet.add_task(next_task)
        return next_task


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet and link the task back to this pet."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a task from this pet and clear its back-link."""
        self.tasks = [t for t in self.tasks if t.id != task.id]
        if task.pet is self:
            task.pet = None

    def get_tasks(self):
        """Return this pet's list of tasks."""
        return self.tasks


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name):
        """Return the pet with this name, or None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self):
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def filter_tasks(self, pet_name=None, completed=None):
        """Return tasks across all pets, optionally narrowed by pet name and/or completion status."""
        tasks = self.get_tasks_by_pet(pet_name) if pet_name is not None else self.get_all_tasks()
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def get_tasks_by_pet(self, pet_name):
        """Return the tasks belonging to one named pet."""
        pet = self.get_pet(pet_name)
        return pet.get_tasks() if pet else []


class Scheduler:
    def __init__(self, available_time_minutes):
        self.available_time_minutes = available_time_minutes

    def generate_plan(self, owner):
        """Build an ordered daily plan from all of the owner's pending tasks that fits the time budget."""
        pending = [task for task in owner.get_all_tasks() if not task.completed]
        ordered = self._order_by_priority_and_dependencies(pending)

        plan = []
        scheduled_ids = set()
        remaining_time = self.available_time_minutes
        for task in ordered:
            dependency_satisfied = (
                task.depends_on is None
                or task.depends_on.completed
                or task.depends_on.id in scheduled_ids
            )
            if not dependency_satisfied:
                continue
            if task.duration_minutes <= remaining_time:
                plan.append(task)
                scheduled_ids.add(task.id)
                remaining_time -= task.duration_minutes

        return plan

    def _order_by_priority_and_dependencies(self, tasks):
        """Order tasks by priority while keeping each task after whatever it depends on."""
        remaining = list(tasks)
        placed_ids = set()
        ordered = []
        while remaining:
            ready = [
                t
                for t in remaining
                if t.depends_on is None or t.depends_on.completed or t.depends_on.id in placed_ids
            ]
            if not ready:
                ready = remaining
            next_task = min(ready, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), remaining.index(t)))
            ordered.append(next_task)
            placed_ids.add(next_task.id)
            remaining.remove(next_task)
        return ordered

    def detect_conflicts(self, owner):
        """Return a warning message for each start_time shared by more than one task, across all pets."""
        tasks_by_time = {}
        for task in owner.get_all_tasks():
            if task.start_time is None:
                continue
            tasks_by_time.setdefault(task.start_time, []).append(task)

        warnings = []
        for start_time, tasks in tasks_by_time.items():
            if len(tasks) > 1:
                names = ", ".join(f"{t.title} ({t.pet.name if t.pet else 'Unknown'})" for t in tasks)
                warnings.append(f"Conflict at {start_time}: {names}")
        return warnings

    def sort_by_duration(self, tasks, descending=False):
        """Return tasks sorted by how long they take."""
        return sorted(tasks, key=lambda task: task.duration_minutes, reverse=descending)

    def sort_by_time(self, tasks):
        """Return tasks sorted by their start_time ("HH:MM"), tasks with no start_time last."""
        return sorted(tasks, key=lambda task: (task.start_time is None, task.start_time))

    def explain_choice(self, task):
        """Return a short human-readable reason this task was (or wasn't) scheduled."""
        if task.completed:
            return f"{task.title} is already done."
        return f"{task.title} was scheduled because it has {task.priority} priority."
