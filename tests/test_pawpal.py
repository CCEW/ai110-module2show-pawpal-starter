import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status():
    task = Task.add_task(name='Feeding', duration=10, priority=9)
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count():
    pet = Pet.add_pet('Biscuit')
    assert len(pet.tasks) == 0

    task = Task.add_task(name='Walk', duration=30, priority=8, pet=pet)
    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_task_filtering_and_sorting_by_preferred_time():
    owner = Owner(name='Test Owner', time_available=120)
    dog = Pet.add_pet('Biscuit')
    owner.add_pet(dog)
    scheduler = Scheduler(owner)

    scheduler.add_task_to_pet(dog, 'Morning walk', 30, priority=9, preferred_time='08:00')
    scheduler.add_task_to_pet(dog, 'Evening play', 30, priority=8, preferred_time='18:00')
    scheduler.add_task_to_pet(dog, 'Midday snack', 15, priority=5, preferred_time='12:30')

    filtered = scheduler.get_tasks_by_pet_name('Biscuit')
    assert len(filtered) == 3

    sorted_tasks = scheduler.sort_tasks_by_preferred_time(filtered)
    assert [task.name for task in sorted_tasks] == ['Morning walk', 'Midday snack', 'Evening play']


def test_recurring_tasks_are_scheduled_even_if_completed():
    from datetime import date, timedelta

    owner = Owner(name='Test Owner', time_available=120)
    cat = Pet.add_pet('Whiskers')
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    today = date.today()
    recurring = scheduler.add_task_to_pet(cat, 'Daily feeding', 15, priority=9, recurrence='daily', due_date=today)
    next_task = recurring.mark_complete()
    one_time = scheduler.add_task_to_pet(cat, 'Nail trim', 20, priority=6)
    one_time.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    plan = scheduler.generate_daily_plan()
    assert all(s.task.name != 'Nail trim' for s in plan)
    assert all(s.task.name != 'Daily feeding' for s in plan)


def test_conflict_detection_prevents_overlapping_schedule():
    owner = Owner(name='Test Owner', time_available=120)
    dog = Pet.add_pet('Biscuit')
    owner.add_pet(dog)
    scheduler = Scheduler(owner)

    task1 = scheduler.add_task_to_pet(dog, 'Walk', 30, priority=9)
    task2 = scheduler.add_task_to_pet(dog, 'Grooming', 30, priority=8)

    scheduled1 = scheduler.schedule_task(task1, 480)
    assert scheduled1 is not None

    scheduled2 = scheduler.schedule_task(task2, 495)
    assert scheduled2 is None
    assert scheduler.has_time_conflict(495, 30) is True


def test_recurring_task_completion_creates_next_due_date():
    from datetime import date, timedelta

    owner = Owner(name='Test Owner', time_available=120)
    cat = Pet.add_pet('Whiskers')
    owner.add_pet(cat)
    scheduler = Scheduler(owner)

    today = date.today()
    recurring = scheduler.add_task_to_pet(
        cat,
        'Daily feeding',
        15,
        priority=9,
        recurrence='daily',
        due_date=today,
    )

    next_instance = scheduler.complete_task(recurring)
    assert recurring.completed is True
    assert next_instance is not None
    assert next_instance.recurrence == 'daily'
    assert next_instance.due_date == today + timedelta(days=1)
    assert next_instance.completed is False
    assert next_instance in cat.tasks
