import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", time_available=480)
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler


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
owner_name = st.text_input("Owner name", value=owner.name, key="owner_name")
pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="species")

# Update owner name if changed
if owner.name != owner_name:
    owner.name = owner_name

# Initialize pet if not already in owner's pets
if not owner.pets:
    pet = Pet.add_pet(pet_name)
    owner.add_pet(pet)
else:
    pet = owner.pets[0]  # Use first pet for demo

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="task_duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")

# Map priority string to number
priority_map = {"low": 1, "medium": 5, "high": 9}
priority_num = priority_map[priority]

if st.button("Add task"):
    if task_title not in [t["title"] for t in st.session_state.tasks]:
        st.session_state.tasks.append(
            {"title": task_title, "duration_minutes": int(duration), "priority": priority, "priority_num": priority_num}
        )
        # Also add to scheduler
        scheduler.add_task_to_pet(pet, task_title, int(duration), priority_num)
        st.success(f"Added '{task_title}' to {pet.name}'s tasks")
    else:
        st.warning(f"Task '{task_title}' already exists")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily schedule based on tasks, priority, and owner preferences.")

col1, col2 = st.columns(2)
with col1:
    time_available = st.number_input(
        "Available time (minutes)",
        min_value=30,
        max_value=1440,
        value=owner.time_available,
        key="time_available"
    )
    if owner.time_available != time_available:
        owner.time_available = time_available

with col2:
    start_time = st.number_input(
        "Start time (minutes from midnight, e.g., 480 = 8:00 AM)",
        min_value=0,
        max_value=1440,
        value=owner.preferences.preferred_start_time,
        key="start_time"
    )
    if owner.preferences.preferred_start_time != start_time:
        owner.preferences.preferred_start_time = start_time

if st.button("Generate schedule", type="primary"):
    if not st.session_state.tasks:
        st.error("No tasks to schedule. Add at least one task above.")
    else:
        # Generate the daily plan
        plan = scheduler.generate_daily_plan()
        
        if plan:
            st.success("Schedule generated!")
            st.code(scheduler.get_daily_plan_summary(), language="text")
            
            # Display as a table for readability
            st.subheader("Schedule Details")
            schedule_data = []
            for scheduled in sorted(plan, key=lambda s: s.start_time):
                time_range = scheduled.get_time_range()
                pet_name = scheduled.task.pet.name if scheduled.task.pet else "Unknown"
                schedule_data.append({
                    "Time": time_range,
                    "Task": scheduled.task.name,
                    "Pet": pet_name,
                    "Duration": f"{scheduled.task.duration} min",
                    "Priority": scheduled.task.priority
                })
            st.dataframe(schedule_data, use_container_width=True)
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Tasks Scheduled", len(plan))
            with col2:
                total_time = sum(s.task.duration for s in plan)
                st.metric("Total Time", f"{total_time} min")
            with col3:
                st.metric("Utilization", f"{(total_time / owner.time_available * 100):.1f}%")
        else:
            st.warning("Could not generate schedule. Check task duration and available time.")
