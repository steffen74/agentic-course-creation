# Changelog

## Unreleased

- `/to-slides`: the first slide of each block names its minutes in its kicker, and once the deck exists those minutes are the timing source (instructors edit them on the slides). New script `scripts/deck_timing.py` adds them up for a deck stored as files, fails when they exceed the session length and rewrites the hidden timing slide with `--write-timing`; `course-checks` lists it. Presenter cues such as click counts go into the speaker notes. Feedback from a real course: minutes drifted between deck, timing slide and session plan while the instructor edited the deck.

## 0.3.0 – 2026-11-23

- `/setup-course` asks for the course folder (a course can live in `course/` of another repository), the format (sessions or self-study), the visibility rule that fits it, and the course language (templates are translated, structure kept). The `AGENTS.md` section gets `Format:` and `Language:` lines and paths with the folder.
- Self-study courses: `/draft-unit` writes pages with exercise, reference solution and self-check instead of a session plan; `/to-quiz` and `/to-slides` stop when the course has none. In a public self-study course, solutions are part of the course and the visibility checks look for learner data instead.
- `/draft-unit` takes scripted replies and expected answers from a real run of the tool learners use; new walk-through check that they match the current tool.
- Patterns from the Agentic Skillset Builder: `/grill-course` and `/draft-unit` ask for the instructor's words first and keep rounds short; `/to-quiz` and `/course-retro` copy input pasted in chat into the files; `/map-resources`, `/to-course-plan`, `/walk-through` and `/review-unit` present decisions in batches of at most five; every writing skill offers a commit; `/setup-course` creates `CLAUDE.md`; `/course-retro` writes skill proposals to `SKILL-PROPOSALS.md`.
- Adopted the core of the Agentic Skillset Builder (`.skillset-core.json`): `render_canvas.py` with `--print`/`--pdf` (HTML output unchanged), `scripts/check_skillset.py`, maintainer skill `release-skillset`. The printed canvas is now generated from `COURSE-CANVAS.md` (its prompts moved into `print:` lines), so the template is the single source of the canvas.
- `/show-canvas` also counts decisions logged with `**Canvas block:**` (the decision log format of Agentic Data Science).

## 0.2.0 – 2026-11-05

- New skill `/show-canvas`: renders `COURSE-CANVAS.md` as an HTML page laid out like the printed canvas (`scripts/render_canvas.py`, standard library only). Empty blocks are marked as not decided or not drafted; with `DECISIONS.md`, each block shows its decisions and those newer than the canvas version. `live` re-renders on every change. Also reads the `CANVAS.md` of Agentic Data Science.
- `/to-quiz`: a house style per course (title, text under the title, closing questions every quiz ends with, theme), asked once and kept in the Quizzes line. `export_quiz.py` takes `--description` and `--closing` (choice questions without a correct answer, or open text). Feedback from a real course.
- `/to-slides`: slides show only what the room needs at that moment; links to other units, outlooks, background and where to find things later go into the speaker notes (except on homework and outlook slides). Feedback from a real course.
- `/review-unit` asks its decisions as multiple-choice questions, each with its own context (the finding and where it is, why it matters, constraints, options with consequences, the recommendation first), and asks the verdict last. Feedback from a real course: questions without background left the instructor guessing.

- New skill `/to-quiz`: questions on the previous unit go into one private quiz source; the quiz is created through a connector when one is connected (Formbricks has an official MCP server with OAuth sign-in), otherwise exported with `scripts/export_quiz.py` for Formbricks (survey JSON for the Management API) or Microsoft Forms (Quick Import `.docx` plus answer key). Slides show the quiz link, not the questions.
- `/setup-course` settles the handbook, quiz tool and slide format at the start of the course. `/to-slides` publishes approved decks as PDF to the handbook and links them from the unit page. New checks for quizzes and slide PDFs; `RESOURCES.md` has a quiz column.

- New skill `/to-slides`: builds a unit’s slides from its approved session plan (outline first, then the deck in the format recorded in `AGENTS.md`). Slides are part of the unit cycle: `/draft-unit` suggests them, `/walk-through` treats published decks and task slides as participant material, `/review-unit` and `course-checks` check them, and `RESOURCES.md` has a slides column.
- `/to-slides` revised after its first test run on a real course: opening slides, video-check and live-filled slides, a timing table, where outlines live, keyword-only content and ambiguous tasks become decisions, in-session tasks without a participant page are flagged, and decks are recorded as mirrors so fixes reach them. `/course-retro` fixes every mirror.

- Courses are planned in **units** instead of weeks, so the skills fit weekly courses, block courses and self-paced modules alike. `draft-week` and `review-week` are renamed to `draft-unit` and `review-unit`. `/setup-course` asks what a unit is called and how many there are, and records this in `AGENTS.md`.

## 0.1.0 – 2026-11-03

- First draft: canvas (guide, SVG, PDF, template), process, principles, nine user-invoked skills and three reference skills.
- `walk-through` revised after its first test run on a real course: read the tools learners invoke, check data against task claims, sequential fallback without sub-agents, cross-persona summary and a list of steps walked without finding.
