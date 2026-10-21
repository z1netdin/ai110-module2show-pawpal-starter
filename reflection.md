# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my first design I thought about the 3 main things a user needs to do, and gave each one its own class:

1. **Add a task.** I made a `Task` class for this. It just holds the info for one task: title, how long it takes (minutes), priority, and which pet it is for. The `Owner`/`Pet` class keeps the list of tasks and lets the user add new ones or edit them. This is basically the "Add task" form part.
2. **Make the schedule.** This is the job of the `Scheduler` class. It takes all the tasks plus the constraints (how much time there is, priority, what the owner prefers) and turns that into an ordered plan for the day. This is where the real logic is, deciding what fits and in what order.
3. **See today's plan.** Once the `Scheduler` makes the plan, it gets shown back to the user so they can see the tasks for today and why they were put in that order.

I split it this way so the UI part (`app.py`) does not need to know how the schedule is actually built, it just asks the `Scheduler` for the plan and shows it.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
