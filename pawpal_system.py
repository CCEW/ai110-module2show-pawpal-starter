from dataclasses import dataclass, field
from datetime import date, timedelta
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
    preferred_time: Optional[str] = None  # "HH:MM" format for preferred scheduling
    recurrence: Optional[str] = None  # e.g. "daily", "weekly"
    due_date: Optional[date] = None

    @classmethod
    def add_task(
        cls,
        name: str,
        duration: int,
        priority: int,
        pet: Optional[Pet] = None,
        preferred_time: Optional[str] = None,
        recurrence: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> "Task":
        """Factory method to create a new Task."""
        return cls(
            name=name,
            duration=duration,
            priority=priority,
            pet=pet,
            preferred_time=preferred_time,
            recurrence=recurrence,
            due_date=due_date,
        )

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and create the next recurring task if needed."""
        self.completed = True

        if self.recurrence in {"daily", "weekly"}:
            current_due = self.due_date or date.today()
            increment = timedelta(days=1 if self.recurrence == "daily" else 7)
            next_due = current_due + increment

            next_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                pet=self.pet,
                completed=False,
                preferred_time=self.preferred_time,
                recurrence=self.recurrence,
                due_date=next_due,
            )
            if self.pet:
                self.pet.tasks.append(next_task)
            return next_task

        return None

    @property
    def is_recurring(self) -> bool:
        return self.recurrence is not None

    def needs_scheduling(self, today: Optional[date] = None) -> bool:
        """Determine whether the task should be considered for today's schedule."""
        if today is None:
            today = date.today()
        if self.completed:
            return False
        if self.due_date is None:
            return True
        return self.due_date <= today


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

    def add_task_to_pet(
        self,
        pet: Pet,
        task_name: str,
        duration: int,
        priority: int,
        preferred_time: Optional[str] = None,
        recurrence: Optional[str] = None,
        due_date: Optional[date] = None,
    ) -> Task:
        """Create and add a Task to a Pet."""
        task = Task.add_task(
            task_name,
            duration,
            priority,
            pet,
            preferred_time=preferred_time,
            recurrence=recurrence,
            due_date=due_date,
        )
        pet.add_task(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all Owner's pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks filtered by pet name and/or completion status."""
        tasks = self.get_all_tasks()
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet and task.pet.name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [task for task in tasks if task.completed is completed]
        return tasks

    def get_tasks_by_pet_name(self, pet_name: str) -> List[Task]:
        return self.filter_tasks(pet_name=pet_name)

    def get_tasks_by_completion(self, completed: bool) -> List[Task]:
        return self.filter_tasks(completed=completed)

    def sort_tasks_by_preferred_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by preferred time string in HH:MM format."""
        return sorted(tasks, key=lambda task: task.preferred_time or "23:59")

    def get_schedule_end_time(self) -> int:
        """Compute the absolute end time for the owner's available schedule."""
        return self.owner.preferences.preferred_start_time + self.owner.time_available

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and return the next recurrence instance if created."""
        return task.mark_complete()

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

    def schedule_task_with_warning(
        self,
        task: Task,
        start_time: int,
        allow_conflict: bool = False,
    ) -> tuple[Optional[ScheduledTask], Optional[str]]:
        """Attempt to schedule a task and return a warning message if it conflicts."""
        if self.has_time_conflict(start_time, task.duration):
            warning = (
                f"Conflict detected: '{task.name}' for '{task.pet.name if task.pet else 'Unknown'}' "
                f"overlaps an existing scheduled task at {self._format_time(start_time)}."
            )
            if not allow_conflict:
                return None, warning

            scheduled = ScheduledTask(start_time=start_time, task=task)
            self.scheduled_tasks.append(scheduled)
            return scheduled, warning

        return self.schedule_task(task, start_time), None

    def detect_conflicts(self) -> List[str]:
        """Return warnings for any overlapping scheduled tasks."""
        warnings: List[str] = []
        scheduled = sorted(self.scheduled_tasks, key=lambda s: s.start_time)

        for i, current in enumerate(scheduled):
            for later in scheduled[i + 1 :]:
                if later.start_time < current.end_time:
                    warnings.append(
                        f"Conflict: '{current.task.name}' ({current.task.pet.name if current.task.pet else 'Unknown'}) "
                        f"overlaps with '{later.task.name}' ({later.task.pet.name if later.task.pet else 'Unknown'}) "
                        f"during {current.get_time_range()}."
                    )
                else:
                    break

        return warnings

    def generate_daily_plan(self) -> List[ScheduledTask]:
        """Produce an ordered list of ScheduledTasks for the day.
        
        Strategy: Greedy by priority, respecting preferred times, recurring tasks, and conflicts.
        """
        self.scheduled_tasks = []  # Reset schedule

        all_tasks = [task for task in self.get_all_tasks() if task.needs_scheduling()]
        sorted_tasks = sorted(
            all_tasks,
            key=lambda t: (-t.priority, t.preferred_time or "23:59"),
        )

        current_time = self.owner.preferences.preferred_start_time
        schedule_end = self.get_schedule_end_time()

        for task in sorted_tasks:
            if len(self.scheduled_tasks) >= self.owner.preferences.max_tasks_per_day:
                break

            available_start = self.find_next_available_slot(task.duration, current_time)
            if available_start is None or available_start + task.duration > schedule_end:
                continue

            scheduled = self.schedule_task(task, available_start)
            if scheduled:
                current_time = scheduled.end_time + self.owner.preferences.min_break_between_tasks

        return self.sort_schedule_by_time()

    def find_next_available_slot(self, duration: int, earliest_start: int) -> Optional[int]:
        """Find the earliest available start time for a task after a given time."""
        current_start = earliest_start
        schedule_end = self.get_schedule_end_time()

        while current_start + duration <= schedule_end:
            if not self.has_time_conflict(current_start, duration):
                return current_start
            current_start += 1

        return None

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

        for scheduled in sorted(self.scheduled_tasks, key=lambda s: s.get_time_range().split(' - ')[0]):
            time_range = scheduled.get_time_range()
            task_name = scheduled.task.name
            pet_name = scheduled.task.pet.name if scheduled.task.pet else "Unknown"
            priority = scheduled.task.priority
            lines.append(f"{time_range:<17} {task_name:<28} {pet_name:<12} {priority}")

        return "\n".join(lines)

    def sort_schedule_by_time(self) -> List[ScheduledTask]:
        """Return scheduled tasks sorted by their start time string (HH:MM)."""
        return sorted(self.scheduled_tasks, key=lambda scheduled: scheduled.get_time_range().split(' - ')[0])

    @staticmethod
    def _format_time(minutes: int) -> str:
        hours, mins = divmod(minutes, 60)
        return f"{hours:02d}:{mins:02d}"

