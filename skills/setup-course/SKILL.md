---
name: setup-course
description: "Set up a course repository for the agentic course creation skills: course canvas, personas, resource map, decision log, signals log and checks. Run once per course before the other skills."
disable-model-invocation: true
---

# Set up a course

Scaffold the files every other skill reads. This is prompt-driven, not a script: explore, present what you found, confirm, then write.

The course repository is usually the instructors’ private working repository. A course can also live in a folder of another repository, for example a self-study course in `course/` of a skills repository. Participant-facing pages, templates and code may live elsewhere; `/map-resources` maps them later.

## 1. Explore

Read what exists; assume nothing:

- `git remote -v`, and whether the repository is public or private.
- `AGENTS.md` / `CLAUDE.md`: is there already an `## Agentic course creation` section?
- `COURSE-CANVAS.md`, `PERSONAS.md`, `RESOURCES.md`, `DECISIONS.md`, `SIGNALS.md`, `checks/` at the root or in a course folder (`course/`, `course/planning/`).
- Whether the repository is about something else (skills, software, a book) and the course is one part of it.
- Existing course material: concept documents, session plans, syllabi, slide decks, quizzes; links to other repositories or platforms in READMEs.

## 2. Present findings and ask

Summarise what is present and missing. Then take the sections in order, one answer each, leading with your recommendation. Skip a section when exploration already settled it.

- **A. Folder.** Where the planning files go: the repository root (a course repository) or a folder (recommend `course/planning/`, with participant pages in `course/docs/`, when the repository holds something else). All paths below and in `AGENTS.md` are relative to the repository root and include this folder.
- **B. Format.** Taught in **sessions** (live, with an instructor) or **self-study** (learners work alone through pages). Self-study has no session plans, slides or live quiz; each page carries its exercise, a reference solution to compare with and self-check questions with a collapsible answer.
- **C. Visibility.** Confirm the repository is not public. If it is: for a sessions course, recommend keeping instructor content (sample answers, session plans, quizzes, signals) in a private repository and stop until the user decides. For a public self-study course, solutions to compare with are part of the course; record that in `DECISIONS.md`, and keep learner data (signals with names, submissions) out of the repository.
- **D. Language.** The language of the course and of the planning files. The templates are in English; in another language, translate headings, prompts and comments when you copy them, keeping the structure (block numbers, field names in bold, owner icons) so the other skills can read them.
- **E. Other locations.** Which other repositories or platforms hold course resources (participant pages, template, data, LMS)? A list of names or URLs is enough; `/map-resources` does the rest.
- **F. Course context.** Course name, instructors, the run (term or dates), and in one sentence the change the course should make for learners. Keep the rest for `/grill-course`.
- **G. Unit.** The skills plan, draft, walk through and release the course one **unit** at a time: one session (or day, or module) together with the preparation before it and the tasks after it. Ask what a unit is called in this course and how many there are; recommend from the structure you found (“week” for weekly sessions, “day” for a block course, “module” for self-paced). Also ask whether there is a preparation unit before the first session, numbered 0.
- **H. Tools for learners.** Decide once for the whole course (for self-study, quizzes and slides are usually “none”), recommending from what the course already uses: the **handbook** where participant pages live (for example a GitBook repository) and where files such as slide PDFs go; the **quiz tool** (for example Microsoft Forms or Formbricks; whether answers are scored); the **slide format** (for example a claude.ai Slides artifact or `.pptx`) and whether decks are published to participants. Check which of these tools has a connected connector; otherwise the skills produce import files.

## 3. Write

- Copy the templates in [`templates/`](templates/) to the folder from A, in the language from D. Never overwrite an existing file; report it instead.
- Fill the canvas header; put the one-sentence change into block 1 as a draft; list the locations from E in `RESOURCES.md`. Remove the template columns the format does not use (for self-study: *Instructor*, *Slides*, *Quiz*; add *Self-check*).
- Create `CLAUDE.md` with the single line `@AGENTS.md` if it is missing (Claude Code loads `CLAUDE.md`, other agents `AGENTS.md`).
- Create `checks/README.md` (in the folder from A) listing the checks from `course-checks` that apply, each marked *automated* (with the command) or *walkthrough* or *manual*. Add a link check over all Markdown files if a tool is available (for example `lychee` or a short script); otherwise mark it manual.
- Existing material that already answers a canvas block (a concept with learning goals, a workload table) is linked from that block, not copied.
- Add this section to `AGENTS.md` (create the file if needed):

```markdown
## Agentic course creation

- Canvas: `<folder>/COURSE-CANVAS.md` (read before any course work; update when something is decided)
- Format: <sessions | self-study>; Language: <language of course and planning files>
- Personas: `<folder>/PERSONAS.md`; resource map: `<folder>/RESOURCES.md`
- Decisions: `<folder>/DECISIONS.md`; learner signals: `<folder>/SIGNALS.md`
- Checks: `<folder>/checks/` (<command for automated checks>)
- Other locations: <repos and platforms, with visibility>
- Handbook: <repo or platform>, unit pages in <path>, files in <assets path>
- Quizzes: <source file>, tool <name>, connector <name|none>, scored <yes|no> | none (self-checks on the pages)
- Slides: <format>, <deck location>, <outline location>, <published to participants: yes (PDF in handbook) | no>, template <link> | none
- Unit: <name, e.g. week>; <n> units, numbered <0|1>–<n>. The skills say “unit”; use this name when talking to the instructor and in files.
- Never copy instructor content (sample answers, session plans, quiz answers, signals) into a public location. | Public self-study course: solutions to compare with are part of the course (see `DECISIONS.md`); no learner data in the repository.
```

If the repository already has an `AGENTS.md` for another purpose, add the section without changing the rest, and tell the user if its checks (for example a check for unknown skill names) will need to skip the course folder.

Done when every file exists and the user has confirmed the `AGENTS.md` section. Suggest committing, then `/grill-course`.
