---
name: draft-unit
description: Draft the resources for one unit (instructor session plan, participant page, template or code changes) from the course plan, writing the learner's expected path before the content. Type the unit after the command.
disable-model-invocation: true
---

# Draft a unit

Draft one unit’s resources. Read `COURSE-CANVAS.md`, `PLAN.md`, `PERSONAS.md`, `RESOURCES.md`, `DECISIONS.md` and the material of the previous unit. Use the existing structure of the course’s files (headings, tables, tone); if the course has none yet, propose one and wait for confirmation.

## 1. Write the path first

Before any content, write the **learner path** for the unit as a numbered list in the session file’s instructor notes: every step a learner takes from opening the participant page to handing in the deliverable, each with

- what they need (concept, tool, file, link, account) and where that came from (boundary, earlier unit, this page),
- the expected result they can see.

Load `assumed-knowledge`. A step whose need has no origin is a gap: resolve it now by adding a step, a link or an explanation, or put it to the instructor. Show the path and wait for confirmation; this is the specification the material is checked against.

## 2. Draft

Draft what the unit needs according to `RESOURCES.md`, each in its own location:

- **Instructor**: session plan with timings, input, group work, sample answers and discussion points. Timings follow what sessions really take: a quiz with discussion about 4 minutes per item, closing questions included; a live demo twice its rehearsed time. The blocks add up to the session length; mark one block as the one to cut and put the homework before it. A tool learners use in the homework is demonstrated live in the session before it, early enough not to be the block that gets cut. Write the input blocks as content (claims, numbers, examples) with speaker notes in mind; slides are built from them later by `/to-slides`.
- **Participant**: goals, tasks, deliverable, material with lengths. Load `learner-instructions`.
- **Template or code**: notebooks, data, configuration the tasks rely on.

Compute sample answers by running the code on the course data, never from memory. Quote numbers with how they were computed.

## 3. Stop point

Show the drafts with a short list of choices you made (task wording, which video, how much is optional) and what you were unsure about. The instructor edits or approves. Log choices that affect other units in `DECISIONS.md`.

Done when the instructor has approved the drafts and `RESOURCES.md` lists the unit as *draft*. Suggest `/to-slides <unit>` if the session has input blocks, then `/walk-through <unit>`; never mark a unit *released* in this skill.
