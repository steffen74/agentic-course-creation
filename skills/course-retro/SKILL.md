---
name: course-retro
description: After a session or when learners got stuck - turn what happened into fixes for this run, checks, boundary entries, persona updates and improvements to the skills themselves.
disable-model-invocation: true
---

# Course retro

Make the next unit, the next run and the skill set better from what happened. Read `SIGNALS.md`, `COURSE-CANVAS.md`, `PERSONAS.md`, `checks/README.md` and the material of the units concerned.

## 1. Collect signals

Ask the instructor what happened, in one round: what went differently than planned, where learners got stuck, which questions came up more than once, which deliverables were missing. Add facts you can look up yourself (chat questions the instructor pastes, quiz results, deliverables in repositories). Write each as an entry in `SIGNALS.md`; no names of participants.

## 2. Explain each signal

For every signal, find the cause before proposing anything. Load `assumed-knowledge`. Typical causes: a step outside the boundary, two pages that disagree, a link that changed, a persona missing from `PERSONAS.md`, a workload estimate that was too low. Then ask: **why did no check or walkthrough catch it?** That answer matters more than the fix.

## 3. Propose

A numbered list, each with evidence and a recommendation, in these categories:

- **Fix now**: what learners of this run need, before the next session (an announcement, a corrected page). Draft the exact text, and fix every mirror listed in `RESOURCES.md`, including earlier slide decks.
- **Check**: the check that would have caught it, with its type (automated, walkthrough, manual). A mistake caught by a learner is a check waiting to be written.
- **Boundary and personas**: an entry for block 6, or a persona that was missing or wrong.
- **Canvas and plan**: blocks or plan items that turned out wrong.
- **Skill rule**: a change to a skill in this skill set (for example a new typical gap in `assumed-knowledge`, a new question in `walk-through`). Prefer a check over a rule. Write it as a diff against the skill file, and suggest filing it as an issue or pull request in the skill repository so other courses benefit.

## 4. Apply

Apply only what the instructor picks. Update the status of each signal in `SIGNALS.md` and block 11 of the canvas (now / next run). Done when every picked item is written to its file and every signal has a status.
