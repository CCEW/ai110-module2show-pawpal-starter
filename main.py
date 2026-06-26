from pawpal_system import Owner, Pet, Scheduler

# Create owner
owner = Owner(name='Alice', time_available=480)  # 8 hours = 480 min

# Create pets
dog = Pet.add_pet('Biscuit')
cat = Pet.add_pet('Whiskers')
owner.add_pet(dog)
owner.add_pet(cat)

# Create scheduler
scheduler = Scheduler(owner)

# Add tasks to pets
scheduler.add_task_to_pet(dog, 'Morning walk', 30, priority=9)
scheduler.add_task_to_pet(dog, 'Feeding', 10, priority=9)
scheduler.add_task_to_pet(cat, 'Litter box cleaning', 5, priority=7)
scheduler.add_task_to_pet(cat, 'Playtime', 20, priority=8)
scheduler.add_task_to_pet(dog, 'Evening walk', 30, priority=8)
scheduler.add_task_to_pet(cat, 'Feeding', 10, priority=9)

# Verify get_all_tasks works
all_tasks = scheduler.get_all_tasks()
print(f'Total tasks: {len(all_tasks)}')
for task in all_tasks:
    print(f'  - {task.name} ({task.pet.name}): {task.duration} min, priority {task.priority}')

# Generate daily plan
plan = scheduler.generate_daily_plan()
print("Today's Schedule")
print(scheduler.get_daily_plan_summary())
