---
name: grill-course
description: Interview the instructor until the change, learners, learning goals, evidence and assumed knowledge of a course are sharp. Writes the canvas, personas and decision log as answers come in.
disable-model-invocation: true
---

# Grill the course

Interview the instructor relentlessly until blocks 1–4 and 6 of `COURSE-CANVAS.md` and `PERSONAS.md` are sharp. Read `COURSE-CANVAS.md`, `PERSONAS.md`, `DECISIONS.md` and any existing concept documents first; never re-ask what is already decided or written down.

## How to interview

Map the open points as a **decision tree**: the change (block 1) gates the learners (2) and the goals (3); goals gate the evidence (4); learners gate the assumed knowledge (6).

Work in **rounds**. The **frontier** is every point whose prerequisites are settled. Ask the whole frontier in one round, number each question, and give your recommended answer:

```
❓ **Q1** - **<title>**: <question, with options where useful>

➡️ <your recommended answer, and why>
```

Wait for the answers, write them down (below), recompute the frontier, and ask the next round.

**Facts are your job; decisions are the instructor’s.** Workload numbers, video lengths, what a linked page says, which tools a template installs: look them up. Never ask for something you can find.

## What to probe

- **Change**: what learners can do afterwards that they could not before, in which real situation. Who benefits besides the learner.
- **Learners**: background, goals, time they really have (per week, or in total for a block course), equipment and rights, language, what they pay for. Ask for the weakest learner the course still wants to serve, and write that persona first. Where real data exists (registrations, previous cohorts), use it and name it as source.
- **Learning goals**: observable (“can explain”, “can build”, “can decide”), few at course level. What the course does **not** cover.
- **Evidence**: for every goal, which deliverable or observation shows it, and the criterion. Goals without evidence are either dropped or given evidence; ask which.
- **Assumed knowledge**: load `assumed-knowledge`. Go through concepts, things learners have, things they have done, where things are, and conventions. For each, settle: assumed, taught (where), or provided (how). Invent concrete scenarios from the first unit that force a precise answer (“the task says *open your clone of the template*: has the weakest persona made one, and how?”).

Sharpen fuzzy terms as they come up (“participants”, “project”, “repository”: which one?) and write precise meanings into `DECISIONS.md` or the canvas.

## Write as you go

- Each settled answer goes into its canvas block immediately, in a few lines.
- Each persona goes into `PERSONAS.md`.
- Each choice between alternatives goes into `DECISIONS.md` with reason and alternatives.
- Anything left open goes to **Open questions** on the canvas, with who resolves it.

Done when the frontier is empty: blocks 1–4 and 6 each hold a settled answer or an explicit open question, and at least the weakest persona exists. Show the updated blocks and ask the instructor to confirm before suggesting `/map-resources`.
