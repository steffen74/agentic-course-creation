# Contributing

Feedback from real courses is the most valuable contribution. Useful issues describe:

- a moment where learners got stuck that no check or walkthrough caught, with what the material said,
- a situation where a skill led the agent astray, with what happened and what you expected,
- a canvas block that was unclear or missing in practice.

`/course-retro` drafts such issues for you, including the proposed change to a skill.

## Conventions for skills

- Follow the structure of [Matt Pocock’s skills](https://github.com/mattpocock/skills) and his `writing-for-agents` guide: short, steps with completion criteria, reference behind pointers.
- User-invoked skills set `disable-model-invocation: true` and have a one-line human-facing description. Reference skills keep a model-facing description with their triggers.
- Every instructor decision is an explicit **stop point**: the agent recommends, the instructor decides, the decision is logged.
- Skills read and write the files named in the `## Agentic course creation` section of `AGENTS.md`; they do not invent new locations.
- The canvas template has a single source: `skills/setup-course/templates/COURSE-CANVAS.md`.
- Keep the block-by-block correspondence with the [Agentic Data Science Canvas](https://github.com/steffen74/agentic-data-science).
