from pawpal_system import Owner, Pet, Scheduler, Task

# Create owner
owner = Owner(name='Alice', time_available=480)  # 8 hours = 480 min

# Create pets
dog = Pet.add_pet('Biscuit')
cat = Pet.add_pet('Whiskers')
owner.add_pet(dog)
owner.add_pet(cat)

# Create scheduler
scheduler = Scheduler(owner)

# Add tasks to pets out of logical order to demonstrate sorting
scheduler.add_task_to_pet(dog, 'Evening walk', 30, priority=8, preferred_time='18:00')
scheduler.add_task_to_pet(dog, 'Morning feeding', 10, priority=9, preferred_time='08:15')
scheduler.add_task_to_pet(cat, 'Midday play', 20, priority=8, preferred_time='12:00')
scheduler.add_task_to_pet(dog, 'Afternoon brushing', 15, priority=6, preferred_time='15:30')
scheduler.add_task_to_pet(cat, 'Litter box cleaning', 5, priority=7, preferred_time='09:45')
scheduler.add_task_to_pet(cat, 'Evening feeding', 10, priority=9, preferred_time='19:00')

# Mark a task as completed for filtering
all_tasks = scheduler.get_all_tasks()
if all_tasks:
    all_tasks[0].mark_complete()

# Verify get_all_tasks works
print(f'Total tasks: {len(all_tasks)}')
for task in all_tasks:
    status = 'done' if task.completed else 'pending'
    preferred = task.preferred_time or 'none'
    pet_name = task.pet.name if task.pet else 'Unknown'
    print(f'  - {task.name} ({pet_name}) [{preferred}] {task.duration} min, priority {task.priority}, {status}')

# Demonstrate sorting by preferred time
print('\nTasks sorted by preferred time:')
sorted_tasks = scheduler.sort_tasks_by_preferred_time(all_tasks)
for task in sorted_tasks:
    pet_name = task.pet.name if task.pet else 'Unknown'
    print(f'  - {task.preferred_time or "zz:zz"} {task.name} ({pet_name})')

# Demonstrate filtering by pet name
biscuit_tasks = scheduler.get_tasks_by_pet_name('Biscuit')
print(f'\nTasks for Biscuit: {len(biscuit_tasks)}')
for task in biscuit_tasks:
    print(f'  - {task.name} ({task.preferred_time or "none"})')

# Demonstrate filtering by completion status
pending_tasks = scheduler.get_tasks_by_completion(False)
print(f'\nPending tasks: {len(pending_tasks)}')
for task in pending_tasks:
    pet_name = task.pet.name if task.pet else 'Unknown'
    print(f'  - {task.name} ({pet_name})')

# Demonstrate lightweight conflict detection in a separate scheduler
conflict_owner = Owner(name='Conflict Demo', time_available=120)
conflict_dog = Pet.add_pet('Biscuit')
conflict_cat = Pet.add_pet('Whiskers')
conflict_owner.add_pet(conflict_dog)
conflict_owner.add_pet(conflict_cat)
conflict_scheduler = Scheduler(conflict_owner)

conflict_task1 = conflict_scheduler.add_task_to_pet(conflict_dog, 'Conflicting walk', 20, priority=5, preferred_time='08:15')
conflict_task2 = conflict_scheduler.add_task_to_pet(conflict_cat, 'Conflicting bath', 20, priority=4, preferred_time='08:15')

print('\nConflict demo tasks:')
for task in conflict_scheduler.get_all_tasks():
    print(f'  - {task.name} ({task.pet.name if task.pet else "Unknown"}) [{task.preferred_time or "none"}]')

conflict_scheduler.schedule_task(conflict_task1, 480)
_, warning = conflict_scheduler.schedule_task_with_warning(conflict_task2, 480)

if warning:
    print(f'\nWarning:\n{warning}')

conflict_warnings = conflict_scheduler.detect_conflicts()
if conflict_warnings:
    print('\nDetected conflict warnings:')
    for conflict in conflict_warnings:
        print(conflict)
else:
    print('\nConflicting tasks not scheduled. No conflicts detected in the demo schedule.')

# Generate daily plan
plan = scheduler.generate_daily_plan()
print("\nToday's Schedule")
print(scheduler.get_daily_plan_summary())
