---
name: assumed-knowledge
description: Rules for the prerequisite boundary of a course - what learners can be assumed to know and have at each point, and how to tell a gap from a fair assumption. Use when writing or reviewing participant-facing instructions, tasks, setup steps or quizzes, and when a learner got stuck.
---

# Assumed knowledge

The **boundary** is what a learner can be assumed to know, have and be able to do at a given point of the course. Canvas block 6 holds it for the course start; the material of each unit extends it. Every step a learner is asked to take must lie inside the boundary at that point. A step outside it is a **gap**: the learner gets stuck, guesses or asks.

## What the boundary covers

Not only concepts. Gaps come at least as often from:

- **Things they have**: accounts, subscriptions, installed software, admin rights, a laptop of their own, a repository of their own.
- **Things they have done**: a clone, a fork, a `uv sync`, joining a chat room, accepting an invitation.
- **Where things are**: which repository, which folder, which link. “Your clone of the template repository” assumes they made one.
- **Conventions**: what a command prompt is, what “run” means in a notebook, that `/command` is typed into the agent.

## Rules

- The boundary is the instructor’s decision. When it is unclear whether something can be assumed, ask; do not decide.
- Something becomes known only when the material taught it **before** it is used, or asked learners to do it with instructions they could follow. Being in a video listed for the same unit counts only if the video comes before the task.
- A tool doing it for the learner (an agent, a setup script) counts only if the learner is told to use it at that step, with the exact prompt or command.
- Every artifact a step relies on needs an origin: a step that created it, or a link to where it lives.
- Optional material never extends the boundary.
- When two personas differ, the boundary follows the weaker one, unless block 6 explicitly excludes them.

## Typical gaps

- An instruction refers to an object (repository, file, room, account) whose creation step is missing or only implied.
- Two pages name different repositories or folders for the same step.
- A command works only from a specific folder, and the page does not say which.
- A tool the step depends on is free in one plan and paid in another; the page assumes the paid one.
- A task needs a concept that is scheduled for a later unit.

## Red flags in class

The same question from several learners; learners waiting for the instructor before they can start; a deliverable missing for a whole group. Treat each as a boundary violation until shown otherwise, and load `course-checks` to turn it into a check.
