---
name: course-checks
description: Rules and a catalogue of checks that course material must pass before learners see it - alignment, boundary, workload, consistency, visibility, links and setup. Use when planning checks, reviewing a unit, or turning a classroom problem into a check.
---

# Course checks

Course material fails quietly: a missing step, a renamed repository or a sample answer in a public file causes no error until a learner meets it. A **check** is an invariant that must hold before material counts as released, with an expected value from an independent source.

## Rules

- **Independent source.** The expected value comes from somewhere other than the material under check: the canvas, the plan, the source-of-truth file in `RESOURCES.md`, the platform itself (does the link resolve, does the repository exist), or a learner walkthrough.
- **Cheapest type that works.** Prefer *automated* (a script or command), then *walkthrough* (`/walk-through`), then *manual* (a named person ticks it). Record the type in `checks/README.md`.
- **Never loosen a check to pass.** If a check is wrong, change it with a decision in `DECISIONS.md`.
- **Every classroom problem becomes a check**, or a recorded decision that it is not worth one.

## Catalogue

| Check | Expected value from | Typical type |
|---|---|---|
| Every learning goal is assessed at least once | Block 3, `PLAN.md` matrix | automated or manual |
| Every deliverable serves a goal | `PLAN.md` matrix | manual |
| Every step lies inside the boundary at that point | Block 6, `PLAN.md` boundary growth | walkthrough |
| Every object a step refers to (repository, file, room, account) has a creation step or a link | Earlier steps, `RESOURCES.md` | walkthrough |
| Workload per unit adds up and is within plan | Listed lengths, block 5 budget | automated |
| Shared facts match their source of truth | `RESOURCES.md` source-of-truth table | automated (search) |
| No instructor content in public locations | `RESOURCES.md` visibility column | automated (search for markers such as “sample answer”, “instructor notes”) |
| Links resolve | The web | automated |
| Setup works from scratch on each supported system | A clean machine or container per system | walkthrough or manual |
| Sample answers match the current data | Running the code | automated |
| Tasks name where to work (repository, folder, file) | — | walkthrough |
| Paid features are marked, with the free alternative | Block 5 tool costs | manual |
| Slides match the session plan and participant page (task wording, links, commands, deadlines) | Session plan, `RESOURCES.md` | automated (search) or manual |
| Slide timing fits the plan (slides per input block vs. its minutes) | Session plan | manual |
| Session plan blocks add up to the session length; quiz with discussion about 4 min per item, live demo twice its rehearsed time; one block marked to cut, homework before it | Session plan | automated (sum), manual (rest) |
| No sample answer appears on a slide before the task it answers | Session plan order | manual |
| Every in-session task uses only what learners met before it (earlier units, or an input or demo earlier in the session); no slide or note presents later homework as already seen | Session plan, video notes, `RESOURCES.md` | manual (outline) or walkthrough |
| The slide PDF in the handbook is the current deck, without speaker notes or hidden answer slides | Deck version, `RESOURCES.md` | manual |
| Quiz questions cover only content learners met before the session | Previous unit’s material | walkthrough or manual |
| The listed videos teach what the tasks and the quiz rely on, without assuming material outside the course | Video notes from the transcripts | walkthrough |
| Quiz answers and explanations appear only in the private source and the tool’s answer settings | `RESOURCES.md` visibility column | automated (search) |
| The quiz link on the slides and in `RESOURCES.md` opens the quiz for this unit | The tool | manual |

## Where checks live

`checks/README.md` lists each check with its type, its command or owner, and the units it applies to. Automated checks are scripts under `checks/`, run with one command. `/review-unit` runs them; `/course-retro` adds new ones.
