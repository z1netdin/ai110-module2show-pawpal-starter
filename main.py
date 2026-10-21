"""Temporary testing ground for pawpal_system.py. Run this to check your logic in the terminal."""

from pawpal_system import Owner, Pet, Task, Scheduler


def print_plan(scheduler, owner):
    plan = scheduler.generate_plan(owner)

    print("Today's Schedule")
    print("-" * 30)
    for task in plan:
        pet_name = task.pet.name if task.pet else "Unknown"
        print(f"[{pet_name}] {task.title} - {task.duration_minutes} min (priority: {task.priority})")

    scheduled_ids = {task.id for task in plan}
    skipped = [t for t in owner.get_all_tasks() if not t.completed and t.id not in scheduled_ids]
    if skipped:
        print("\nSkipped (did not fit in the available time):")
        for task in skipped:
            pet_name = task.pet.name if task.pet else "Unknown"
            print(f"  [{pet_name}] {task.title}")

    return plan


owner = Owner("Jordan")

sohpia = Pet("Sohpia", "dog")
milo = Pet("Milo", "cat")
owner.add_pet(sohpia)
owner.add_pet(milo)

pee_break = Task("Pee break", 5, "high")
breakfast = Task("Breakfast", 10, "high", depends_on=pee_break)
morning_walk = Task("Morning walk", 30, "medium")
feeding = Task("Feeding", 10, "high")

sohpia.add_task(pee_break)
sohpia.add_task(breakfast)
sohpia.add_task(morning_walk)
milo.add_task(feeding)

# Tight budget on purpose: proves the scheduler actually drops tasks that don't
# fit, even high-priority ones, instead of always scheduling everything.
scheduler = Scheduler(available_time_minutes=20)
print_plan(scheduler, owner)

# Demonstrate mark_done(): a completed dependency should still let its
# dependent task (breakfast) be scheduled on the next run.
pee_break.mark_done()
print("\nAfter marking 'Pee break' done, the next plan is:")
print_plan(scheduler, owner)

# --- Sorting and filtering demo ---
# Add these out of order on purpose (afternoon, then morning, then evening) to
# prove sort_by_time() actually reorders them instead of just echoing insertion order.
grooming = Task("Grooming", 15, "medium", start_time="14:30")
vet_checkup = Task("Vet checkup", 20, "high", start_time="09:15")
evening_walk = Task("Evening walk", 30, "medium", start_time="18:00")
sohpia.add_task(grooming)
sohpia.add_task(vet_checkup)
sohpia.add_task(evening_walk)

print("\n--- Sorted by time ---")
for task in scheduler.sort_by_time(sohpia.get_tasks()):
    print(f"{task.start_time} - {task.title}")

print("\n--- Sorted by duration ---")
for task in scheduler.sort_by_duration(sohpia.get_tasks()):
    print(f"{task.duration_minutes} min - {task.title}")

print("\n--- Filtered: Sohpia's tasks only ---")
for task in owner.filter_tasks(pet_name="Sohpia"):
    print(f"[Sohpia] {task.title}")

print("\n--- Filtered: completed tasks only ---")
for task in owner.filter_tasks(completed=True):
    pet_name = task.pet.name if task.pet else "Unknown"
    print(f"[{pet_name}] {task.title}")

# --- Conflict detection demo ---
# Milo's grooming is scheduled for the same clock time as Sohpia's vet checkup
# (09:15) across two different pets -- one owner can't be in two places at once.
milo_grooming = Task("Milo's grooming", 20, "medium", start_time="09:15")
milo.add_task(milo_grooming)

print("\n--- Conflict check ---")
conflicts = scheduler.detect_conflicts(owner)
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts found.")
