import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome! This app helps you remember what to do for your pet each day,
like walks, feeding, and bathroom breaks — and it builds a simple plan for you.
"""
)

with st.expander("How does this work?", expanded=True):
    st.markdown(
        """
1. Tell us your pet's name.
2. Add a few things you need to do for your pet today.
3. Say how much time you have.
4. Press the button to get your plan for the day!
"""
    )

st.divider()

st.subheader("👋 Let's get started")
owner_name = st.text_input("Your name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(available_time_minutes=60)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.markdown("### 🐾 Your Pets")
pet_name = st.text_input("Pet's name", value="Mochi")
species = st.selectbox("What kind of pet?", ["dog", "cat", "other"])

if st.button("➕ Add this pet"):
    owner.add_pet(Pet(pet_name, species))

if owner.pets:
    st.write("Your pets:", ", ".join(pet.name for pet in owner.pets))
else:
    st.info("You don't have any pets yet. Add one above! 🐶🐱")

st.markdown("### ✅ Things To Do")
st.caption("Add something your pet needs today, like a walk or feeding time.")

PRIORITY_LABELS = {"low": "🟢 Not very important", "medium": "🟡 Somewhat important", "high": "🔴 Very important"}

if owner.pets:
    selected_pet_name = st.selectbox("For which pet?", [pet.name for pet in owner.pets])
    selected_pet = owner.get_pet(selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("What needs to happen?", value="Morning walk")
    with col2:
        duration = st.number_input("How many minutes will it take?", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("How important is it?", ["low", "medium", "high"], index=2, format_func=lambda p: PRIORITY_LABELS[p])
    with col4:
        start_time = st.text_input("What time? (like 9:00) — optional", value="")

    if st.button("➕ Add this task"):
        selected_pet.add_task(Task(task_title, int(duration), priority, start_time=start_time or None))

all_tasks = owner.get_all_tasks()
if all_tasks:
    filter_col, sort_col = st.columns(2)
    with filter_col:
        filter_pet = st.selectbox("Show tasks for", ["Everyone"] + [pet.name for pet in owner.pets])
        filter_status = st.selectbox("Show", ["Everything", "Still to do", "Already done"])
    with sort_col:
        sort_mode = st.radio("Put them in order by", ["No particular order", "Time of day", "How long they take"])

    visible_tasks = owner.filter_tasks(
        pet_name=None if filter_pet == "Everyone" else filter_pet,
        completed=None if filter_status == "Everything" else (filter_status == "Already done"),
    )
    if sort_mode == "Time of day":
        visible_tasks = scheduler.sort_by_time(visible_tasks)
    elif sort_mode == "How long they take":
        visible_tasks = scheduler.sort_by_duration(visible_tasks)

    st.table(
        [
            {
                "Pet": task.pet.name if task.pet else "",
                "What to do": task.title,
                "What time": task.start_time or "any time",
                "Minutes": task.duration_minutes,
                "How important": PRIORITY_LABELS[task.priority],
                "Done?": "✅ Yes" if task.completed else "⬜ Not yet",
            }
            for task in visible_tasks
        ]
    )

    conflicts = scheduler.detect_conflicts(owner)
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ Uh oh, two things are planned for the same time! {warning}. Try picking a different time for one of them.")
    else:
        st.success("👍 Nothing is planned for the same time. You're all set!")
else:
    st.info("No tasks yet. Add a pet and something to do above.")

st.divider()

st.subheader("📅 Make Today's Plan")
available_time = st.number_input("How many minutes do you have today?", min_value=1, max_value=600, value=60)

if st.button("✨ Make my plan"):
    scheduler.available_time_minutes = int(available_time)

    conflicts = scheduler.detect_conflicts(owner)
    for warning in conflicts:
        st.warning(f"⚠️ Before you use this plan: {warning}. You may want to fix that first.")

    plan = scheduler.generate_plan(owner)

    if plan:
        st.success(f"🎉 Here's your plan! {len(plan)} thing(s) will fit in {int(available_time)} minutes.")
        st.table(
            [
                {
                    "Pet": task.pet.name if task.pet else "Unknown",
                    "What to do": task.title,
                    "Minutes": task.duration_minutes,
                    "How important": PRIORITY_LABELS[task.priority],
                    "Why": scheduler.explain_choice(task),
                }
                for task in plan
            ]
        )
    else:
        st.info("Nothing fits in that time yet. Try giving yourself more time, or add fewer things.")
