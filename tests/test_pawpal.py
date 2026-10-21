"""Tests for the PawPal+ scheduling logic in pawpal_system.py."""

from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def test_mark_done_changes_completed_status():
    task = Task("Morning walk", 30, "medium")
    assert task.completed is False

    task.mark_done()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Bella", "dog")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task("Feeding", 10, "high"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    pet = Pet("Bella", "dog")
    afternoon = Task("Grooming", 15, "medium", start_time="14:30")
    morning = Task("Breakfast", 10, "high", start_time="07:00")
    midday = Task("Vet checkup", 20, "high", start_time="09:15")
    # Add them out of chronological order on purpose.
    pet.add_task(afternoon)
    pet.add_task(morning)
    pet.add_task(midday)

    scheduler = Scheduler(available_time_minutes=60)
    ordered = scheduler.sort_by_time(pet.get_tasks())

    assert [task.title for task in ordered] == ["Breakfast", "Vet checkup", "Grooming"]


def test_mark_done_on_daily_task_creates_task_for_next_day():
    pet = Pet("Bella", "dog")
    feeding = Task("Feeding", 10, "high", recurrence="daily")
    pet.add_task(feeding)

    next_task = feeding.mark_done(today=date(2026, 10, 21))

    assert next_task is not None
    assert next_task.id != feeding.id
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 10, 22)
    assert next_task in pet.get_tasks()


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner("Jordan")
    bella = Pet("Bella", "dog")
    milo = Pet("Milo", "cat")
    owner.add_pet(bella)
    owner.add_pet(milo)

    bella.add_task(Task("Vet checkup", 20, "high", start_time="09:15"))
    milo.add_task(Task("Grooming", 20, "medium", start_time="09:15"))

    scheduler = Scheduler(available_time_minutes=60)
    conflicts = scheduler.detect_conflicts(owner)

    assert len(conflicts) == 1
    assert "09:15" in conflicts[0]
