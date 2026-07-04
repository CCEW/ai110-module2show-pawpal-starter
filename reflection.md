# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

I would have a main class Pet and under that I would have methods to add pets and variable pet name, and then I would have a Task class that would have methods to add tasks, and then I would have a Scheduler class that would take in the tasks and schedule them based on the owner's preferences and time available. Finally, I would have an Owner class that would hold the owner's preferences and time available.

- What classes did you include, and what responsibilities did you assign to each?

pet class:
    add a pet(pet name)
    pet name var
task class:
    task name var
    task duration var
    task priority var
    add task(task name, task duration, task priority)
scheduler class:
    schedule task(task)
Owner class:
    owner preferences variable
    time available variable


**b. Design changes**

Yes, significant changes were made:

1. **Added Owner.pets list** — Original UML showed Owner o-- Pet (aggregation), but the skeleton lacked a pets list. Refactored Owner to own a list of Pets so one owner can manage multiple animals.

2. **Added Pet.tasks and Task.pet link** — UML showed Pet 1--* Task, but Tasks had no way to know which pet they belonged to. Added Task.pet field so in a multi-pet household, each task is associated with the correct animal.

3. **Created ScheduledTask dataclass** — The original generate_daily_plan() returned List[Task], but this didn't capture *when* tasks run. Added ScheduledTask(start_time, task, end_time) to represent time slots. Includes has_time_conflict() logic to detect overlaps.

4. **Improved Owner.preferences** — Initial design had vague Dict[str, str]. Created structured OwnerPreferences dataclass with fields like prefer_morning_walks, max_tasks_per_day, min_break_between_tasks, and preferred_start_time to support real scheduling constraints.

5. **Updated Scheduler to track scheduled_tasks** — Changed from a generic tasks list to scheduled_tasks: List[ScheduledTask] and made Scheduler depend explicitly on Owner to enforce owner-based constraints.

6. **Added time conflict detection** — New has_time_conflict() method checks for overlapping scheduled tasks, addressing a key bottleneck in constraint satisfaction.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
It considers time, priority, and preferences. It also considers the duration of each task and the time available for the owner to complete tasks.
- How did you decide which constraints mattered most?
I evaluated what the scheduler would need to consider in order to create a realistic daily plan for a pet owner. Time and priority are the most important constraints because they directly affect the feasibility of completing tasks. Preferences are also important because they allow the owner to customize the schedule to their liking.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
I made a tradeoff between scheduling high-priority tasks and respecting the owner's preferred time windows. For example, if a high-priority task is scheduled outside of the owner's preferred time window, the scheduler may choose to delay it to fit within the preferred window, even if it means that a lower-priority task is completed first.
- Why is that tradeoff reasonable for this scenario?
Because it allows the owner to have a schedule that is more aligned with their lifestyle and preferences, which can lead to better adherence to the schedule.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to brainstorm design ideas, generate UML diagrams, and suggest code snippets for the scheduling logic. I also used AI to help with debugging by providing suggestions for fixing errors and improving code structure.
- What kinds of prompts or questions were most helpful?
I found error prompts and specific questions about how to implement certain features or logic to be the most helpful. For example, asking how to implement a time conflict detection method or how to structure the OwnerPreferences dataclass.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
To create the ScheduledTask dataclass, I initially asked the AI to create a class that would hold the task and its start and end times. The AI suggested a simple class with just those fields, but I realized that I also needed to include a method to check for time conflicts between scheduled tasks. I added that method myself after reviewing the AI's suggestion.
- How did you evaluate or verify what the AI suggested?
I run tests to verify that the AI's suggestions worked as expected. Explicitly telling the AI of the edge cases I wanted to test.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested the scheduling logic to ensure that tasks were scheduled correctly based on their priority and duration, and that they did not overlap with each other. I also tested the time conflict detection logic to ensure that it correctly identified overlapping tasks.
- Why were these tests important?
So the scheduler would generate a valid daily plan that respects the constraints and priorities of the owner and pets.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am confident 5 stars
- What edge cases would you test next if you had more time?
I would test edge cases such as tasks that have the same preferred time, tasks that have a duration longer than the available time window, and tasks that have a priority of 0 or negative values. I would also test the scheduler's behavior when there are no tasks to schedule or when all tasks are completed.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The scheduling logic is pretty good and it generated a realistic daily plan for the pet owner. The AI was very helpful in generating ideas and code snippets, which saved a lot of time and effort.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the user interface to make it more user-friendly and intuitive. I would also add more features such as the ability to set reminders for tasks, and to view the schedule in a calendar format.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
Having an AI assistant can be very helpful in generating ideas and code snippets, but it is important to critically evaluate the suggestions and make sure they fit the specific needs of the project.