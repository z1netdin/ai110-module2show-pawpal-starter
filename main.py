from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Jordan")

sohpia = Pet("Sohpia", "dog")
milo = Pet("Milo", "cat")
owner.add_pet(sohpia)
owner.add_pet(milo)

sohpia.add_task(Task("Morning walk", 30, "medium"))
sohpia.add_task(Task("Pee break", 5, "high"))
milo.add_task(Task("Feeding", 10, "high"))

scheduler = Scheduler(available_time_minutes=60)
plan = scheduler.generate_plan(owner)

print("Today's Schedule")
print("-" * 30)
for task in plan:
    pet_name = task.pet.name if task.pet else "Unknown"
    print(f"[{pet_name}] {task.title} - {task.duration_minutes} min (priority: {task.priority})")
