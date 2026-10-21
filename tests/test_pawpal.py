"""Tests for the PawPal+ scheduling logic in pawpal_system.py."""

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
