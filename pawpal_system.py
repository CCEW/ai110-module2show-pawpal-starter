from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class OwnerPreferences:
    """Structured owner preferences for scheduling."""
    prefer_morning_walks: bool = True
    max_tasks_per_day: int = 10
    min_break_between_tasks: int = 5  # minutes
    preferred_start_time: int = 480  # 8:00 AM in minutes

    def to_dict(self) -> dict:
        """Convert preferences to dictionary."""
        return {
            "prefer_morning_walks": self.prefer_morning_walks,
            "max_tasks_per_day": self.max_tasks_per_day,
            "min_break_between_tasks": self.min_break_between_tasks,
            "preferred_start_time": self.preferred_start_time,
        }


@dataclass
class Owner:
    name: str
    preferences: OwnerPreferences = field(default_factory=OwnerPreferences)
    time_available: int = 0  # total available minutes per day

    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a Pet to this Owner's household."""
        pet.owner = self
        self.pets.append(pet)

    def update_preferences(self, **kwargs) -> None:
        """Update one or more preference fields."""
        for key, value in kwargs.items():
            if hasattr(self.preferences, key):
                setattr(self.preferences, key, value)


@dataclass
class Pet:
    name: str
    owner: Optional[Owner] = None

    tasks: List["Task"] = field(default_factory=list)

    @classmethod
    def add_pet(cls, name: str) -> "Pet":
        """Factory method to create a new Pet."""
        return cls(name=name)

    def add_task(self, task: "Task") -> None:
        """Add a Task to this Pet."""
        task.pet = self
        self.tasks.append(task)


@dataclass
class Task:
    name: str
    duration: int  # minutes
    priority: int  # higher number = higher priority
    pet: Optional[Pet] = None
    completed: bool = False

    @classmethod
    def add_task(cls, name: str, duration: int, priority: int, pet: Optional[Pet] = None) -> "Task":
        """Factory method to create a new Task."""
        return cls(name=name, duration=duration, priority=priority, pet=pet)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class ScheduledTask:
    """A Task placed in a specific time slot."""
    start_time: int  # minutes from start of day (e.g., 480 = 8:00 AM)
    task: Task
    end_time: int = field(init=False)

    def __post_init__(self) -> None:
        """Calculate end_time based on task duration."""
        self.end_time = self.start_time + self.task.duration

    def get_time_range(self) -> str:
        """Return human-readable time range (HH:MM - HH:MM)."""
        start_h, start_m = divmod(self.start_time, 60)
        end_h, end_m = divmod(self.end_time, 60)
        return f"{start_h:02d}:{start_m:02d} - {end_h:02d}:{end_m:02d}"


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.scheduled_tasks: List[ScheduledTask] = []

    def add_task_to_pet(self, pet: Pet, task_name: str, duration: int, priority: int) -> Task:
        """Create and add a Task to a Pet."""
        task = Task.add_task(task_name, duration, priority, pet)
        pet.add_task(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all Owner's pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_schedule_end_time(self) -> int:
        """Compute the absolute end time for the owner's available schedule."""
        return self.owner.preferences.preferred_start_time + self.owner.time_available

    def schedule_task(self, task: Task, start_time: int) -> Optional[ScheduledTask]:
        """Place a Task at a specific start_time, respecting constraints.
        
        Returns: ScheduledTask if successful, None if placement fails due to conflicts.
        """
        # Check time conflict
        if self.has_time_conflict(start_time, task.duration):
            return None

        # Check time bounds (within owner's available time window)
        schedule_end = self.get_schedule_end_time()
        if start_time + task.duration > schedule_end:
            return None

        # Check max tasks per day
        if len(self.scheduled_tasks) >= self.owner.preferences.max_tasks_per_day:
            return None

        # If all checks pass, create and add the scheduled task
        scheduled = ScheduledTask(start_time=start_time, task=task)
        self.scheduled_tasks.append(scheduled)
        return scheduled

    def generate_daily_plan(self) -> List[ScheduledTask]:
        """Produce an ordered list of ScheduledTasks for the day.
        
        Strategy: Greedy by priority (high to low), fit tasks into available time.
        Respects owner constraints: time_available, max_tasks_per_day, min_break_between_tasks.
        """
        self.scheduled_tasks = []  # Reset schedule

        # Get all tasks from all pets and sort by priority (descending)
        all_tasks = self.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: t.priority, reverse=True)

        current_time = self.owner.preferences.preferred_start_time
        schedule_end = self.get_schedule_end_time()

        for task in sorted_tasks:
            # Stop if we've reached max tasks per day
            if len(self.scheduled_tasks) >= self.owner.preferences.max_tasks_per_day:
                break

            # Check if task fits in remaining time
            if current_time + task.duration > schedule_end:
                continue

            # Try to schedule the task at current_time
            scheduled = self.schedule_task(task, current_time)
            if scheduled:
                current_time = scheduled.end_time + self.owner.preferences.min_break_between_tasks
            # If schedule_task fails, skip this task (don't advance time)

        return self.scheduled_tasks

    def has_time_conflict(self, start_time: int, duration: int) -> bool:
        """Check if a time slot conflicts with existing scheduled tasks."""
        proposed_end = start_time + duration
        for scheduled in self.scheduled_tasks:
            # Check overlap: proposed [start, end) vs. scheduled [start, end)
            if not (proposed_end <= scheduled.start_time or start_time >= scheduled.end_time):
                return True
        return False

    def get_daily_plan_summary(self) -> str:
        """Return a nicely formatted terminal summary of the daily plan."""
        if not self.scheduled_tasks:
            return "No tasks scheduled for today."

        header = f"Daily Plan for {', '.join(p.name for p in self.owner.pets)}"
        separator = "=" * len(header)
        lines = [header, separator]
        lines.append(f"Available window: {self._format_time(self.owner.preferences.preferred_start_time)} - {self._format_time(self.get_schedule_end_time())}")
        lines.append("")
        lines.append(f"{'Time':<17} {'Task':<28} {'Pet':<12} {'Pri'}")
        lines.append(f"{'-' * 17} {'-' * 28} {'-' * 12} {'-' * 3}")

        for scheduled in sorted(self.scheduled_tasks, key=lambda s: s.start_time):
            time_range = scheduled.get_time_range()
            task_name = scheduled.task.name
            pet_name = scheduled.task.pet.name if scheduled.task.pet else "Unknown"
            priority = scheduled.task.priority
            lines.append(f"{time_range:<17} {task_name:<28} {pet_name:<12} {priority}")

        return "\n".join(lines)

    @staticmethod
    def _format_time(minutes: int) -> str:
        hours, mins = divmod(minutes, 60)
        return f"{hours:02d}:{mins:02d}"

