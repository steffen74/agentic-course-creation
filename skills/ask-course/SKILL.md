---
name: ask-course
description: Ask which course creation skill fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask course

Read `COURSE-CANVAS.md` (and the `## Agentic course creation` section of `AGENTS.md`). If either is missing, the answer is `/setup-course`.

Then recommend **one** next skill, with one sentence on why, based on the first gap you find:

| If … | Recommend |
|---|---|
| Blocks 1–4 or 6, or `PERSONAS.md`, are empty or vague | `/grill-course` |
| Block 5 or 9 is empty, or a repository or platform was added | `/map-resources` |
| Goals are sharp but there is no unit-by-unit plan with an alignment matrix | `/to-course-plan` |
| A unit in the plan has no material yet | `/draft-unit <unit>` |
| A unit’s session plan has a video check or quiz but no quiz in the tool | `/to-quiz <unit>` |
| A unit’s session plan is approved but its input blocks have no slides | `/to-slides <unit>` |
| Material for a unit exists but has not been walked through | `/walk-through <unit>` |
| A walkthrough is done, but the unit is not released | `/review-unit <unit>` |
| A session just took place, or learners got stuck | `/course-retro` |

If the user describes a situation instead, map it to the table. When two rows apply, recommend the earlier one, except that a unit whose session is within the next seven days goes first: then recommend `/walk-through` for that unit.
