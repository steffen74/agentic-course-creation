---
name: to-course-plan
description: Turn the canvas into a unit-by-unit course plan with an alignment matrix (goals × units × evidence), the growth of assumed knowledge, and a workload table.
disable-model-invocation: true
---

# To course plan

Write the plan that every unit’s material is built from. Read `COURSE-CANVAS.md`, `PERSONAS.md`, `RESOURCES.md` and `DECISIONS.md`. Do not interview again; if blocks 1–4 or 6 are empty, stop and suggest `/grill-course`.

## 1. Draft

Write `PLAN.md` (or the file named in `AGENTS.md`) with four parts:

1. **Unit table**: per unit the topic, the question or task that drives it, the learning goals it serves, the deliverable, and the material learners need beforehand.
2. **Alignment matrix**: rows are the learning goals from block 3, columns are the units; each cell says *introduced*, *practised* or *assessed*. Below it, list every goal that is never assessed and every deliverable that serves no goal.
3. **Boundary growth**: per unit, what is added to the assumed knowledge (concepts, tools, accounts, repositories, conventions), and which step adds it. Load `assumed-knowledge`. Every item used in unit *n* must be on the boundary at course start or added in a unit before *n*, or in unit *n* before the step that uses it.
4. **Workload**: per unit the hours for session, learning material and tasks, with how each number was computed. Compare the total with the budget from block 5.

## 2. Stop point

Present the plan with the problems you found first: unassessed goals, items used before they are added to the boundary, units over budget, uneven load. For each, recommend a fix. The instructor decides; log structural choices (sequence, project, where a topic goes) in `DECISIONS.md` and update block 7.

## 3. Checks

Add to `checks/README.md` the plan-level checks the instructor confirmed (for example: every goal is assessed; workload per unit within ± 30 % of the mean; total within budget). Load `course-checks` for the format.

Done when the instructor has confirmed `PLAN.md` and every problem is fixed or listed under **Open questions**. Suggest `/draft-unit` for the first unit without material.
