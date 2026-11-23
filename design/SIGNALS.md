# Signals

Everything that shows how the work is going: dry runs and checks before something counts, and what happened after. Newest first. The retro skill turns signals into fixes, checks and rules.

<!--
## YYYY-MM-DD · <scope> · <source: dry run | check | session | feedback | other>

- **What happened:** facts, with numbers where possible
- **Who:** role or persona (no personal names)
- **Severity:** blocker | friction | note
- **Status:** open | fixed in <commit/file> | turned into check <name>
-->

## 2026-11 · to-slides, to-quiz, review-unit, walk-through · real course (reconstructed from CHANGELOG)

- **What happened:** first test runs on a real course led to: `walk-through` reads the tools learners invoke and checks data against task claims; `to-slides` keeps slides to what the room needs; `to-quiz` gets a house style; `review-unit` asks decisions as multiple-choice questions with their own context (questions without background left the instructor guessing).
- **Who:** instructor (maintainer)
- **Severity:** friction
- **Status:** fixed in v0.1.0–v0.2.0

## 2026-11-23 · setup-course · test run (self-study course of the Agentic Business Model Canvas)

- **What happened:** (1) `/setup-course` assumes the course repository root; the course lives in `course/` of a skillset repository, so planning went to `course/planning/` and the `AGENTS.md` paths were adapted by hand. (2) No mechanism for a course language other than English: templates were translated by hand (German). (3) A self-study course has no sessions, quiz tool or slides; `/to-quiz` and `/to-slides` do not apply, self-check questions live on the pages, and the template columns for slides and quizzes are unused. (4) "Instructor content must stay private" does not fit a public self-study course where solutions are part of the course; recorded as a decision. (5) The skillset repo's `check_skillset.py` flagged the course's commands as unknown skills (fixed in builder core 0.1.4).
- **Who:** maintainer
- **Severity:** friction
- **Status:** open – to address after the course: `setup-course` asks for the course folder and language; a "self-study" format with self-checks instead of quizzes/slides; visibility rule for public self-study courses.
