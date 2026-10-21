"""Logic layer for PawPal+. Backend classes live here; app.py only handles the UI."""

import itertools
from dataclasses import dataclass, field

_task_id_counter = itertools.count(1)

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    pet: "Pet | None" = None
    recurrence: str | None = None
    completed: bool = False
    depends_on: "Task | None" = None
    id: int = field(default_factory=lambda: next(_task_id_counter))

    def mark_done(self):
        """Mark this task as completed."""
        self.completed = True


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
            if task.depends_on is not None and task.depends_on.id not in scheduled_ids:
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
            ready = [t for t in remaining if t.depends_on is None or t.depends_on.id in placed_ids]
            if not ready:
                ready = remaining
            next_task = min(ready, key=lambda t: (PRIORITY_ORDER.get(t.priority, 99), remaining.index(t)))
            ordered.append(next_task)
            placed_ids.add(next_task.id)
            remaining.remove(next_task)
        return ordered

    def explain_choice(self, task):
        """Return a short human-readable reason this task was (or wasn't) scheduled."""
        if task.completed:
            return f"{task.title} is already done."
        return f"{task.title} was scheduled because it has {task.priority} priority."
