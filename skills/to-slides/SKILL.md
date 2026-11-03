---
name: to-slides
description: Build the slides for one unit from its approved session plan - one section per input block, one slide per group task - in the course's slide format. Type the unit after the command.
disable-model-invocation: true
---

# To slides

Build the slides for one unit. Read `COURSE-CANVAS.md`, `RESOURCES.md`, `DECISIONS.md`, the `## Agentic course creation` section of `AGENTS.md`, and the unit’s approved session plan and participant page. Slides are built from the plan, never the other way round: if the session plan is not approved yet, stop and suggest `/draft-unit`.

## 1. Settle the format once

The format is normally settled in `/setup-course`. If `AGENTS.md` has no `Slides:` line, ask, leading with a recommendation from what exists (earlier decks, the tools in block 5):

- **Format and tool**: for example a claude.ai Slides artifact, `.pptx`, Google Slides, Markdown slides (Marp, reveal.js).
- **Where decks live** and who sees them: shown in class only, or published to participants afterwards. Published decks are participant material.
- **Template**: an existing deck or design system whose look to follow.

- **Where outlines live**: recommend a private folder next to the session plans (for example `slides/<unit>-outline.md`), since outlines hold sample answers.

Write the answer as `- Slides: <format>, <deck location>, <outline location>, <published to participants: yes|no>, template <link>` in `AGENTS.md` and log it in `DECISIONS.md`.

## 2. Outline from the plan

Write the outline to its file before any slide: a timing table (plan minutes, slides and minutes per slide for each block), then one entry per block of the session plan, in its order:

- **Opening**: a cover and an agenda slide with the plan’s blocks and minutes, even though the plan does not list them.

- **Input block**: a section sized to its minutes (as a rule, one content slide per two to three minutes). List the claims each slide makes and where they come from: the session plan, its sample answers, the canvas, the participant page. Numbers come from the plan’s sample answers or are computed again; never invented. When the plan gives only a keyword (“scale types”), do not fill it from your own knowledge: mark the slide *content missing in the plan* and make it a decision.
- **Group work**: one task slide with the task in the same wording as the participant page, the time box, the expected result, where to work (repository, data, starting notebook) and where to post or hand in. Load `learner-instructions`. If the participant page does not contain the task (in-session tasks often live only in the session plan), take the plan’s wording and flag it: the slide is then the only place learners see the task, and it is participant material whether or not the deck is published. Flag every task with more than one reasonable reading (for example “average” over days or over rows) as a decision.
- **Plenary**: one slide with the question or the criteria for feedback. Content produced in the room (groups’ answers, charts) gets an empty frame to fill live.
- **Video check**: the quiz link from `RESOURCES.md` (and a QR code where the format allows), not the questions; answers and explanations in the speaker notes only. If the unit has no quiz yet, suggest `/to-quiz` first.
- **Break, outlook**: one slide each; the outlook repeats the homework in the participant page’s wording.

Mark every slide that would reveal a sample answer before learners have worked on it. Those go after the task slide, as hidden or backup slides, or are left out of the published deck.

End the outline with the decisions it needs (overloaded blocks, missing content, ambiguous tasks, whether the deck is published), each with options and a recommendation, and the result of the slide checks from `course-checks` that can already run on an outline. Show it and wait for the instructor. This is the stop point; edits to content go into the session plan first, then into the outline.

## 3. Build

Build the deck in the settled format and template:

- A title on every slide that states its point (“Most forecast errors fall on public holidays”), not a topic (“Results”).
- Little text; what the instructor says belongs in the speaker notes, taken from the session plan.
- Every link, repository name, command and deadline exactly as in its source of truth in `RESOURCES.md`.
- Live demos get a fallback slide (a screenshot or the expected output) in case the demo fails.

## 4. Check and hand over

Run the slide checks from `course-checks` (consistency with plan and participant page, timing, no early sample answers, links). Fix what fails, then show the deck with a list of the slides you were unsure about.

Decks are mirrors: they repeat facts from the session plan and the participant page, including their gaps. Add each deck to the mirrors of those facts in `RESOURCES.md`, so a fix to a page also reaches the decks that repeat it.

If decks are published to participants, publish the approved deck to the handbook: export it as PDF (when the slide tool can only be exported by hand, ask the instructor to export it and say exactly where to save it), name it after the unit (for example `week-02-slides.pdf`), put it in the handbook’s assets path from `AGENTS.md`, remove speaker notes and hidden answer slides from the export, and link it from the unit’s participant page under its materials. A later change to the deck means a new export; the PDF in the handbook is a mirror of the deck.

Done when the instructor has approved the deck, `RESOURCES.md` lists it for the unit with status *draft*, and its location is linked from the session plan, and, if published, the PDF is linked from the unit’s participant page. If the deck is published to participants, suggest `/walk-through <unit>` next; otherwise `/review-unit <unit>`.
