# Principles

Eight habits the canvas and the skills encode.

## 1. The agent finds facts and walks the path, the instructor decides

Anything that can be looked up (video lengths, what a linked page says, whether a link resolves, which facts two pages disagree on) and anything that can be tried (cloning, running the setup, following the steps) is the agent’s job. Anything that involves a trade-off (who the course is for, what to assume, what to leave out, whether to release) is put to the instructor with a recommendation.

## 2. Change before goals, goals before content

Start from what learners should be able to do afterwards, derive goals and the evidence for each, and only then choose content (backward design). Every goal is assessed; every deliverable serves a goal (constructive alignment).

## 3. Assumed knowledge is a decision, not a detail

What learners know, have and have done at each point is written down, not assumed. Every step a learner is asked to take must lie inside that boundary. Most “the students did not do the homework” moments are boundary violations: a step that needed something nobody provided.

## 4. You cannot check your own material by reading it

The author knows every missing step, so the author does not see it. Material is checked against the canvas, the source of truth, and a **walkthrough** by an agent that knows only what a persona knows and executes the steps it can. This replaces “I read it again before posting”.

## 5. Checks come before release

Material passes explicit checks before learners see it: alignment, boundary, workload, consistency, visibility, links, setup. A check has an expected value from an independent source. A unit is *released* only after `/review-unit`.

## 6. One source of truth per fact

Courses spread over repositories, platforms and handbooks. Every fact that appears in more than one place has one source; mirrors are generated or checked. Instructor content never reaches a public location.

## 7. Every classroom surprise becomes a check

When learners get stuck, fix it for them now, then ask why no check caught it. The answer becomes a check, a boundary entry, a persona, or a rule in a skill. The skill set improves with every course that uses it.

## 8. The canvas is the shared state

Canvas, personas, resource map, decisions and signals live in the course repository. The agent reads them at the start of every skill and updates them when something is decided. Nothing important lives only in a chat window or in the instructor’s head.

## Related work

- **Backward design** (Wiggins and McTighe, *Understanding by Design*) and **constructive alignment** (Biggs): blocks 1–4 and the alignment matrix of `/to-course-plan`.
- **ADDIE**-based multi-agent course generation, for example [Instructional Agents](https://arxiv.org/html/2508.19611v3), and LMS course-building agents: these automate production; this canvas focuses on decisions, the prerequisite boundary and checks.
- **Simulated learners**: research on LLM-simulated students for testing materials (for example [Generative Students](https://arxiv.org/pdf/2511.06078), reviewed there) supports `/walk-through`, with a known limit: simulated learners tend to be too capable. The walkthrough therefore restricts the persona to an explicit knowledge state and prefers executing steps to imagining them.
