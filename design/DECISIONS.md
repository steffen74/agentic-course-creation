# Decisions

One entry per decision, newest first. People decide; the agent proposes and records.

<!--
## YYYY-MM-DD: <decision in one line>

- **Context:** what made the decision necessary
- **Decision:** what was decided
- **Reason:** why
- **Alternatives:** what else was considered, and why not
- **Canvas:** block(s) affected
-->

## 2026-11-23: Recap with the Agentic Skillset Builder

- **Context:** The builder now holds the conventions and core shared by all skillsets; Agentic Course Creation was built before it.
- **Decision:** Adopt the core (`render_canvas.py` replaced by the core version, `show-canvas` and the decision and signal templates kept as adapted copies, `check_skillset.py` and `release-skillset` added), generate the printed canvas from the template, reconstruct `design/` from the existing docs. Work on branch `recap-skillset-builder`.
- **Reason:** Shared files stop drifting; the next use of this skillset (the course for the Agentic Business Model Canvas) should run on the builder's current state.
- **Alternatives:** leave the skillset as it is; rebuild it with the builder from scratch.
- **Canvas:** 7, 11

## 2026-11 (v0.2.0): Courses are planned in units, not weeks (reconstructed)

- **Decision:** `draft-week`/`review-week` became `draft-unit`/`review-unit`; `/setup-course` asks what a unit is called and how many there are.
- **Reason:** weekly courses, block courses and self-paced modules alike.
- **Canvas:** 7

## 2026-11 (v0.2.0): Handbook, quiz tool and slide format are set once per course (reconstructed)

- **Decision:** `/setup-course` settles them; `/to-quiz` uses a connector when there is one, otherwise export files; `/to-slides` builds from the approved session plan, outline first.
- **Canvas:** 5, 9
