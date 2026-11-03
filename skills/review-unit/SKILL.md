---
name: review-unit
description: "Review one unit's resources before release on two axes: Alignment (goals, evidence, workload, consistency, visibility) and Learner (can every persona follow it, based on a walkthrough). Ends with release, fix or hold. Type the unit after the command."
disable-model-invocation: true
---

# Review a unit

Two-axis review of one unit before learners see it. Run each axis as a separate sub-agent with a fresh context when your environment supports it; otherwise one after the other. Then aggregate.

Inputs: the unit’s resources (from `RESOURCES.md`), `COURSE-CANVAS.md`, `PLAN.md`, `PERSONAS.md`, `DECISIONS.md`, `checks/README.md`, and the latest walkthrough report for this unit in `SIGNALS.md`.

## Axis 1: Alignment

Load `course-checks` and run every check that applies to a unit:

- **Goals and evidence**: does the unit serve the goals `PLAN.md` assigns to it? Does the deliverable produce the evidence?
- **Workload**: do the listed lengths add up, and is the unit within its planned hours?
- **Consistency**: do repository names, links, commands, dates and skill names match the source of truth in `RESOURCES.md`, across instructor and participant files?
- **Visibility**: no sample answers, session plans or quiz solutions in a participant-facing or public file.
- **Correctness**: sample answers re-computed where the code exists; links resolve.
- **Slides** (if the unit has a deck): the slide checks from `course-checks`. A deck older than the last change to its session plan is re-checked, not assumed current.

## Axis 2: Learner

If no walkthrough for this unit exists, or the material changed after it, run `/walk-through <unit>` first. Then check:

- Every blocker and friction finding is fixed, or accepted by the instructor with a reason.
- The fixes did not move the problem: re-walk only the steps that changed.
- Tasks are written for the audience: load `learner-instructions`.

## Report

One list, each finding marked **blocking** (learners would get stuck or see instructor content) or **note**, with evidence and a suggested fix. End with a recommendation: **release**, **fix then release** (list the fixes) or **hold**.

The verdict is the instructor’s. Apply only the fixes they pick, then rerun the failed checks. Record the verdict in `DECISIONS.md` and set the unit’s status in `RESOURCES.md`.
