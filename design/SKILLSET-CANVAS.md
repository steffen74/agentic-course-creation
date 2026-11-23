# Skillset Canvas

**Skillset:** Agentic Course Creation
**Maintainers:** Steffen Brandt
**Language:** en
**Version:** 2026-11-23

> Owners: 👤 maintainer decides · 🤖 agent drafts, maintainer approves.
> Reconstructed on 2026-11-23 from README, docs, canvas guide and changelog (recap with the Agentic Skillset Builder). Entries marked *(to confirm)* need the maintainer's yes.

---

## Practice

### 1. Practice 👤
Designing, building and improving a course with a coding agent, without handing over the teaching judgement. Without skills, agents produce plausible material fast, but miss what learners don't know, have or have done; ten pages in three repositories drift apart; and lessons from session 1 do not reach session 2. Failure story: a homework asks learners to work in "your copy of the template repository", but no page tells them to make one.

### 2. Users 👤
Instructors at opencampus.sh and similar, running a course with participant pages, repositories and platforms; comfortable with a coding agent and Git. Built while running "Introduction to Data Science and Machine Learning". See `PERSONAS.md`. *(to confirm: whether co-instructors without agent experience are in scope)*

### 3. Outcomes 👤
- A course repository with canvas, personas, resource map, plan, decisions, signals and checks.
- Units drafted from a learner path, with quizzes and slides where the session has them.
- Material walked through as each persona and released only after review.
- Classroom signals turned into fixes, checks, boundary entries and skill rules.

Not: writing the content for the instructor without review; grading learners.

### 4. Evidence 👤
- Every unit released only after `/walk-through` and `/review-unit`; blockers fixed or accepted with a reason.
- Fewer "learners got stuck" signals per run; each one traced to a check or boundary entry.
- Feedback from real courses (changelog entries "Feedback from a real course"). *(to confirm: a concrete criterion)*

---

## Design

### 5. Sources 🤖
Backward design (Wiggins and McTighe), constructive alignment (Biggs), research on simulated learners, Matt Pocock's skills, Agentic Data Science. See `SOURCES.md`.

### 6. Judgement boundary 👤
Agent: facts that can be looked up (video lengths, links, what pages say, which facts disagree) and steps that can be tried (cloning, running setup, following instructions). Instructor: who the course is for, what to assume, what to leave out, whether to release. Typical slip: the agent treats knowledge it has as knowledge the learner has, so a missing step looks fine.

### 7. Process and stop points 👤
setup → grill → map resources → plan → draft unit → quiz, slides → walk through → review → release; signals → fix; retro → checks, boundary, personas, skill rules. Stop point at the end of every step. See `SKILL-MAP.md` and `docs/process.md`.

### 8. Checks 🤖
On the users' work: `course-checks` catalogue (alignment, boundary, workload, consistency, visibility, links, setup, slides, quizzes). On the skillset: `scripts/check_skillset.py` (core); no dry run yet.

---

## Build and improve

### 9. Skills 🤖
12 user-invoked skills and 3 reference skills, released as v0.2.0. See `SKILL-MAP.md`.

### 10. Dry-run signals 🤖
No dry run on a fictitious case yet. Signals so far come from one real course (see `SIGNALS.md`).

### 11. Improvements 👤
Recap with the Agentic Skillset Builder (2026-11-23): core adopted, design files reconstructed. Next: builder patterns in the skills, an example case and a dry run, then the course for the Agentic Business Model Canvas.

---

## Open questions
- Personas and evidence criteria marked *(to confirm)*. (Steffen)
- Example case for dry runs (a fictitious course). (Steffen, in the recap)

## Decision log
See `design/DECISIONS.md`.
