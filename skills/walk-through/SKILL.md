---
name: walk-through
description: "Walk a unit of participant-facing material as a learner persona, using only what that persona knows, and report every step they could not take. Type the unit (and optionally the persona) after the command."
disable-model-invocation: true
---

# Walk through as a learner

Find out whether a learner can actually do what the material asks, before a real learner finds out in class. Read `COURSE-CANVAS.md` (blocks 2 and 6), `PERSONAS.md` and `RESOURCES.md` first; load `assumed-knowledge`.

## 1. Fix the scope

- **Unit**: the one typed with the command; otherwise ask. A walkthrough of unit *n* starts from the state a learner has at the end of unit *n − 1*.
- **Personas**: the one typed with the command, otherwise every persona in `PERSONAS.md`. Always include the persona closest to the lower edge of the assumed-knowledge boundary.
- **Material**: only what the learner can see, as listed in `RESOURCES.md` with audience *participant* or *public*. Never read instructor notes, sample answers or session plans during the walk: they contain the knowledge the learner lacks. Slides count as participant material when `AGENTS.md` says decks are published to participants; task slides shown in class count always, since learners work from them. A file that is technically public but that a learner would not open (plugin manifests, CI configuration) may be read to check what a step does, never to supply knowledge the learner would need.
- **Tools the learner invokes**: read what each tool, skill or script the material tells learners to run actually does (its instructions, its prompts, the questions it will ask). A step can be clear on the page and still fail inside the tool.
- **Isolation**: run each persona as a separate sub-agent with a fresh context when your environment supports it. When it does not (for example, you are a sub-agent yourself), walk the personas one after the other and keep their knowledge states in separate lists.

## 2. Build the persona’s knowledge state

Write down, before walking, what the persona knows and has:

- Block 6 of the canvas (assumed knowledge at course start), filtered by the persona.
- Everything the material of earlier units taught **and** asked them to do (accounts created, software installed, repositories cloned, concepts covered by the listed videos).
- Nothing else. When the persona would plausibly know something outside this state, note it as an assumption; do not use it silently.

## 3. Walk every step

Go through the participant-facing pages in the order a learner reads them. For every instruction, ask:

1. **Can they find it?** Is every file, repository, link, room or tool the step needs named, with a link or an exact location?
2. **Can they do it?** Does the step need a concept, command, account, permission, installed tool or paid plan that is not in the knowledge state?
3. **Do they know when it worked?** Is there an expected result, and what to do when it fails?
4. **Does it fit together?** Does this step contradict another page (different repo name, different command, different deadline)?

Where you can, **execute** the step in a scratch directory instead of imagining it, in this order: links resolve; repositories clone; commands run; the data supports what the task claims or asks (for example, that the period to compare actually has data); notebooks run. A link that 404s or a command that fails is a finding with evidence. Never run anything that needs the learner’s real accounts or costs money; mark those steps *not executed*.

## 4. Report

One table per persona, ordered by where the learner would get stuck:

| # | Step (where) | Finding | Severity | Missing knowledge or info | Suggested fix |
|---|---|---|---|---|---|

*Where* is a page and line, or several, when the finding comes from two places disagreeing.

Severity:

- **blocker**: the persona cannot finish the task without asking someone.
- **friction**: they can finish, but will lose time or guess.
- **note**: unclear wording, inconsistency without consequences.

Then:

- **Across personas**: one row per finding that appears for more than one persona, with the highest severity. This is the list to fix first.
- **Walked without finding**: the steps that passed, and the evidence (for example “all 6 links resolve, template is marked as template on GitHub”).
- **Executed vs. read**: which steps you executed and which you only read.

End with the knowledge the walk had to assume that is not on the boundary: each item is either a gap in the material or a missing entry in block 6. Which one is the instructor’s decision.

Append a dated entry to `SIGNALS.md` (source: *walkthrough*, persona, unit, counts per severity, link to the report). Done when every participant-facing step of the unit has a row or is listed under *walked without finding*, and the report says which steps were executed. Suggest `/review-unit` for fixes, or `/course-retro` when the gap points to a missing check.
