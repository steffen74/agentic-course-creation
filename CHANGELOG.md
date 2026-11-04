# Changelog

## Unreleased

- `/review-unit` asks its decisions as multiple-choice questions, each with its own context (the finding and where it is, why it matters, constraints, options with consequences, the recommendation first), and asks the verdict last. Feedback from a real course: questions without background left the instructor guessing.

- New skill `/to-quiz`: questions on the previous unit go into one private quiz source; the quiz is created through a connector when one is connected (Formbricks has an official MCP server with OAuth sign-in), otherwise exported with `scripts/export_quiz.py` for Formbricks (survey JSON for the Management API) or Microsoft Forms (Quick Import `.docx` plus answer key). Slides show the quiz link, not the questions.
- `/setup-course` settles the handbook, quiz tool and slide format at the start of the course. `/to-slides` publishes approved decks as PDF to the handbook and links them from the unit page. New checks for quizzes and slide PDFs; `RESOURCES.md` has a quiz column.

- New skill `/to-slides`: builds a unit’s slides from its approved session plan (outline first, then the deck in the format recorded in `AGENTS.md`). Slides are part of the unit cycle: `/draft-unit` suggests them, `/walk-through` treats published decks and task slides as participant material, `/review-unit` and `course-checks` check them, and `RESOURCES.md` has a slides column.
- `/to-slides` revised after its first test run on a real course: opening slides, video-check and live-filled slides, a timing table, where outlines live, keyword-only content and ambiguous tasks become decisions, in-session tasks without a participant page are flagged, and decks are recorded as mirrors so fixes reach them. `/course-retro` fixes every mirror.

- Courses are planned in **units** instead of weeks, so the skills fit weekly courses, block courses and self-paced modules alike. `draft-week` and `review-week` are renamed to `draft-unit` and `review-unit`. `/setup-course` asks what a unit is called and how many there are, and records this in `AGENTS.md`.

## 0.1.0 – 2026-11-03

- First draft: canvas (guide, SVG, PDF, template), process, principles, nine user-invoked skills and three reference skills.
- `walk-through` revised after its first test run on a real course: read the tools learners invoke, check data against task claims, sequential fallback without sub-agents, cross-persona summary and a list of steps walked without finding.
