"""Logic layer for PawPal+. Backend classes live here; app.py only handles the UI."""

from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    pet: "Pet | None" = None
    recurrence: str | None = None
    completed: bool = False

    def mark_done(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task):
        pass

    def remove_task(self, task):
        pass

    def get_tasks(self):
        pass


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def get_pet(self, name):
        pass


class Scheduler:
    def __init__(self, available_time_minutes):
        self.available_time_minutes = available_time_minutes

    def generate_plan(self, tasks, available_time):
        pass

    def explain_choice(self, task):
        pass
