---
name: learner-instructions
description: Rules for writing participant-facing instructions, tasks and setup steps that a learner can follow alone. Use when writing or editing participant pages, task descriptions, setup guides, READMEs of templates, or announcements to learners.
---

# Learner instructions

A learner reads instructions alone, often late in the evening, without the context the instructor has. Write so that the weakest persona in `PERSONAS.md` can follow each step without asking.

## Every step

- **Starts with a verb** and does one thing.
- **Names the object exactly**, with a link: not “your repository” but “your copy of [repo-template-…](link), created in step 2”.
- **Says where**: which repository, folder, file, window or app.
- **Shows the expected result**: what the learner sees when it worked (“`CANVAS.md` now exists in the folder”).
- **Says what to do when it fails**: where to ask, or a fallback.
- **Gives the exact text** when the learner types something (a command, an agent prompt) in a code block they can copy.

## Every task

- Starts from the question or situation, then the steps, then the deliverable.
- Says how much time it should take, and which part is optional.
- Puts what learners need to watch or read **before** the task that needs it.
- Says what to hand in or bring, where, and by when.

## Words

- Use one name per thing across all pages; check the source of truth in `RESOURCES.md`.
- Explain a term at first use, or link where it was taught.
- For tools that differ between options (agents, operating systems, free and paid plans), give the variants side by side, or say which one the instructions assume.

## Before you finish

Read the page as the weakest persona: would they know where to start, where they are, and when they are done? If not sure, run `/walk-through`.
