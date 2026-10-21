import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner = st.session_state.owner

st.markdown("### Pets")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species))

if owner.pets:
    st.write("Current pets:", ", ".join(pet.name for pet in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into the scheduler.")

if owner.pets:
    selected_pet_name = st.selectbox("Which pet is this task for?", [pet.name for pet in owner.pets])
    selected_pet = owner.get_pet(selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        selected_pet.add_task(Task(task_title, int(duration), priority))

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": task.pet.name if task.pet else "",
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add a pet and a task above.")

st.divider()

st.subheader("Build Schedule")
available_time = st.number_input("Available time today (minutes)", min_value=1, max_value=600, value=60)

if st.button("Generate schedule"):
    scheduler = Scheduler(available_time_minutes=int(available_time))
    plan = scheduler.generate_plan(owner)

    if plan:
        st.write("Today's Schedule:")
        for task in plan:
            pet_label = task.pet.name if task.pet else "Unknown"
            st.write(f"**[{pet_label}] {task.title}** — {task.duration_minutes} min (priority: {task.priority})")
            st.caption(scheduler.explain_choice(task))
    else:
        st.info("No tasks fit in the available time yet.")
