# AGENTS.md

Instructions for agents working on this repository (the skills themselves, not a course that uses them).

- Skill conventions: see [CONTRIBUTING.md](CONTRIBUTING.md).
- When a change affects users of the skills or the canvas (anything under `skills/`, `.claude-plugin/` or `canvas/`), add an entry under `## Unreleased` in `CHANGELOG.md`.
- New skills under `skills/` must also be added to the `skills` list in `.claude-plugin/plugin.json`.
- The canvas exists three times: `canvas/README.md` (guide), `canvas/agentic-course-creation-canvas.svg` (+ PDF) and `skills/setup-course/templates/COURSE-CANVAS.md`. Change block names and order in all three.
- Never put instructor content of a real course (sample answers, session plans, quiz solutions, signals with participant details) into this public repository.
