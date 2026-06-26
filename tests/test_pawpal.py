import pytest

from pawpal_system import Pet, Task


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
