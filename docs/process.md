# The process

The process follows the canvas from left to right, but it is a loop: every unit is drafted, walked through, reviewed and released, and every session feeds signals back.

A **unit** is one session (or day, or module) together with the preparation before it and the tasks after it. The number of units and what they are called (week, day, module) are set once in `/setup-course` and recorded in `AGENTS.md`; the skills then use the course’s own word. A ten-week course has ten weekly units, a three-day block course three day units, a self-paced course one unit per module.

## Main flow

| Step | Skill | Agent does | Stop point (instructor decides) | Canvas |
|---|---|---|---|---|
| 1. Set up | `/setup-course` | Scaffolds files, lists locations | Visibility, locations, unit, handbook, quiz tool, slide format | all |
| 2. Sharpen the purpose | `/grill-course` | Asks in rounds, recommends, looks up facts | Change, learners, goals, evidence, assumed knowledge | 1–4, 6 |
| 3. Map resources | `/map-resources` | Inventories locations, finds conflicts and leaks | Source of truth per fact | 5, 9 |
| 4. Plan | `/to-course-plan` | Unit table, alignment matrix, boundary growth, workload | Sequence, fixes for gaps | 3, 4, 6, 7 |
| 5. Draft a unit | `/draft-unit` | Learner path first, then drafts; computes sample answers | The path; the drafts | 7, 9 |
| 5b. Quiz | `/to-quiz` | Questions on the previous unit, then the quiz in the tool (connector or import file) | The questions | 4, 9 |
| 5c. Slides | `/to-slides` | Outline from the plan’s input blocks, then the deck, PDF to the handbook; runs slide checks | The outline; the deck | 9 |
| 6. Walk through | `/walk-through` | Walks the unit as each persona, executing what it can | Gap in material or boundary entry | 6, 8, 10 |
| 7. Review | `/review-unit` | Alignment and learner axes | Release, fix or hold | 8, 9 |
| 8. Retro | `/course-retro` | Explains signals, proposes fixes, checks, skill rules | Which to adopt | 10, 11 |

Steps 5–7 repeat for every unit (5b and 5c only when the session has a quiz or input), ideally one to two weeks before the unit’s session. Step 8 runs after every session.

## On-ramps

- **A course that already runs**: `/setup-course`, `/map-resources`, then `/walk-through` for the next unit. Fill blocks 1–4 with `/grill-course` when there is time; block 6 and the weakest persona first.
- **Learners got stuck**: `/course-retro`, then `/walk-through` for the next unit with the new boundary entry.
- **The skill set itself missed something**: `/course-retro` drafts the change to the skill as a diff; file it in this repository.

## Files in a course repository

| File | Content | Written by |
|---|---|---|
| `COURSE-CANVAS.md` | The canvas | all skills |
| `PERSONAS.md` | Learner personas | `/grill-course`, `/course-retro` |
| `RESOURCES.md` | Locations, source of truth, resources per unit | `/map-resources`, `/draft-unit`, `/review-unit` |
| `PLAN.md` | Unit table, alignment matrix, boundary growth, workload | `/to-course-plan` |
| `DECISIONS.md` | Dated decisions with reason and alternatives | all skills at stop points |
| `SIGNALS.md` | Walkthroughs and classroom signals | `/walk-through`, `/course-retro` |
| `checks/` | Check list and automated checks | `/setup-course`, `/to-course-plan`, `/course-retro` |

`/setup-course` records the locations in a short section of `AGENTS.md`, so every skill finds them.
