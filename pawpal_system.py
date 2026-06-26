from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Owner:
    preferences: Dict[str, str] = field(default_factory=dict)
    time_available: int = 0  # minutes

    def update_preferences(self, key: str, value: str) -> None:
        """Set or update an owner preference."""
        self.preferences[key] = value


@dataclass
class Pet:
    name: str

    @classmethod
    def add_pet(cls, name: str) -> "Pet":
        """Factory method to create a new Pet."""
        return cls(name=name)


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int  # higher number = higher priority

    @classmethod
    def add_task(cls, name: str, duration: int, priority: int) -> "Task":
        """Factory method to create a new Task."""
        return cls(name=name, duration=duration, priority=priority)


class Scheduler:
    def __init__(self, owner: Optional[Owner] = None):
        self.owner = owner
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a Task to the scheduler's list."""
        self.tasks.append(task)

    def schedule_task(self, task: Task) -> None:
        """Stub: schedule a single Task considering owner constraints."""
        raise NotImplementedError

    def generate_daily_plan(self) -> List[Task]:
        """Stub: produce an ordered list of Tasks for the day."""
        raise NotImplementedError
