# AGENTS.md

Instructions for agents working on this repository (the skills themselves, not a course that uses them).

- Skill conventions: see [CONTRIBUTING.md](CONTRIBUTING.md).
- When a change affects users of the skills or the canvas (anything under `skills/`, `.claude-plugin/` or `canvas/`), add an entry under `## Unreleased` in `CHANGELOG.md`.
- New skills under `skills/` must also be added to the `skills` list in `.claude-plugin/plugin.json`.
- The canvas template `skills/setup-course/templates/COURSE-CANVAS.md` is the single source of the canvas. The printed SVG and PDF are generated from it (command below); `canvas/README.md` is the guide. Change block names and order in the template and the guide, then regenerate.
- Files listed in `.skillset-core.json` come from the core of the Agentic Skillset Builder; change verbatim ones there, then sync with `/sync-core`.
- Never put instructor content of a real course (sample answers, session plans, quiz solutions, signals with participant details) into this public repository.

## Agentic skillset builder

- Canvas: `design/SKILLSET-CANVAS.md` (read before any work on this skillset; update when something is decided)
- Language: en
- Design files: `design/` (personas, sources, skill map, decisions, signals)
- Canvas template: `skills/setup-course/templates/COURSE-CANVAS.md`
- Printed canvas: `canvas/agentic-course-creation-canvas.svg` and `.pdf`, made with `python3 skills/show-canvas/scripts/render_canvas.py skills/setup-course/templates/COURSE-CANVAS.md --print --lang en --out canvas/agentic-course-creation-canvas.svg --pdf canvas/agentic-course-creation-canvas.pdf --subtitle "The agent walks the learner’s path, the instructor decides, checks come before release." --footer "Agentic Course Creation Canvas v0.2 · CC BY 4.0 · github.com/steffen74/agentic-course-creation"`
- Example case: the self-study course of the Agentic Business Model Canvas (first run after the recap)
- Checks: `python3 scripts/check_skillset.py`
- Core: `.skillset-core.json`, synced with `/sync-core` from the Agentic Skillset Builder
