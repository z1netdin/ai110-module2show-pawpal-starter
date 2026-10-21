# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

For my first design I picked 4 classes, each with its own job:

1. **Owner.** Just me, the user. Holds my name and a list of my pets.
2. **Pet.** Holds the pet's name, species, and a list of its tasks.
3. **Task.** One thing to do, like "morning walk." Holds the title, how long it takes, priority, which pet it's for, and if it's done yet.
4. **Scheduler.** Takes all the tasks plus how much time I have, and puts them in order for the day. This is where the real logic lives.

I split it this way so the UI part (`app.py`) doesn't need to know how the schedule gets built, it just asks the `Scheduler` for the plan and shows it. `Task` and `Pet` are plain data (I used Python dataclasses for those), while `Owner` and `Scheduler` do more of the actual work.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yeah, a couple things changed after I asked my AI assistant to review the skeleton:

1. **Added an `id` to `Task`.** My routine has two "pee break" tasks in one day (morning and evening) with the same title, duration, and priority. Since `Task` is a dataclass, Python checks equality by the field values, so those two tasks would look "equal" even though they're different ones. That would mess up marking one done or removing one later. Adding an auto-generated `id` makes each task instance unique no matter what.
2. **Removed the extra `available_time` from `Scheduler.generate_plan()`.** I originally had it both in `Scheduler`'s constructor and as a method argument, which meant two places could disagree about how much time there is. Since my time budget doesn't change much (no frequent vet appointments or anything like that), I kept it only in the constructor and simplified `generate_plan(tasks)` to just take the tasks.

I also dropped a `Pet.owner` attribute I had at first — since there's only ever one owner in this app, I didn't need a way to go from a pet back to its owner.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My conflict checker (`Scheduler.detect_conflicts()`) only flags two tasks as conflicting if they have the exact same `start_time` string, like two things both set to "09:15". It does not check whether tasks actually overlap in duration, so a 20-minute vet checkup starting at 09:15 and a walk starting at 09:30 would not get flagged, even though the vet checkup is still going on at 09:30.

I think this tradeoff is fine for now because most of my tasks do not have a `start_time` set at all, they just get ordered by priority. The ones that do have a fixed time (like a vet appointment) are rare one-offs, so an exact-match check catches the obvious case (double-booking the same moment) without needing to add real overlap math (comparing start + duration ranges) for a feature that is barely used yet.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for basically every step: brainstorming which classes I needed (Owner, Pet, Task, Scheduler), turning that into the Mermaid UML diagram, generating the class skeletons, converting `Task`/`Pet` to dataclasses, writing the actual scheduling logic, and writing the tests. The most helpful prompt was just asking it to review my own skeleton and point out missing relationships or bottlenecks before I wrote any real logic, that's what caught the duplicate `available_time` parameter and the missing task ID.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI flagged that `Pet` had an `owner` back-reference attribute and suggested removing it since my app only has one owner. At first I said to keep it as-is, I wasn't sure it mattered. After thinking about it more I agreed it was pointless since there's never more than one owner, so I had it removed.

To verify the actual logic worked (not just trusted it), I ran real test commands myself: a quick script creating pets/tasks and checking the printed plan was in the right order, and a specific test where a pee-break task and a same-priority meal task were added in the *wrong* order on purpose, to prove the `depends_on` rule still forced the correct order. I also ran the full `pytest` suite after each change to make sure nothing broke.

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
