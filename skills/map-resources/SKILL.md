---
name: map-resources
description: Inventory every repository, page and platform of a course - who sees what, which copy is the source of truth, what exists per unit - and surface the decisions that need an owner.
disable-model-invocation: true
---

# Map resources

Build the factual inventory behind canvas blocks 5 and 9. Read `COURSE-CANVAS.md`, `RESOURCES.md` and the `## Agentic course creation` section of `AGENTS.md` first.

## 1. Collect

For every location listed in `RESOURCES.md` and every location linked from those (one level deep):

- **Visibility and audience**: public, private, behind a login. Who is meant to read it.
- **Content per unit**: which files belong to which unit or session.
- **Constraints** (block 5): number and length of sessions, credits and workload, dates, platforms, tools with their cost and plan limits, licenses of data and videos. Copy numbers with their source, never estimate them.
- **Shared facts**: anything stated in more than one place (repository names and URLs, setup commands, deadlines, workload, video lists, skill names). Record each occurrence.

Use local clones when they exist; otherwise read from the platform. Never guess the content of a page you could not open: list it as *not read*.

## 2. Find conflicts

Compare the occurrences of each shared fact. Report:

- **Conflicts**: two places say different things (a different repository, command, deadline or number).
- **Orphans**: a resource nobody links to, or a link to something that does not exist.
- **Leaks**: instructor content (sample answers, session plans, quiz solutions, signals) in a public location. Report these first, as blocking.
- **Missing per unit**: a unit with a plan but no participant page, or a page without the template or data it refers to.

## 3. Stop point: decisions

Present the findings as a numbered list. For each conflict, recommend which copy becomes the **source of truth** and how mirrors stay in sync (generated, checked by `course-checks`, or edited by hand with a check). The instructor decides; log each decision in `DECISIONS.md`.

## 4. Write

Update `RESOURCES.md` (locations, source-of-truth table, resources per unit), canvas block 5 (constraints, short, with links) and block 9 (one line per unit with status). Never fix a conflict in the material yourself in this skill; list it under **Open questions** or hand it to `/review-unit`.

Done when every location is either mapped or marked *not read*, and every conflict has a decision or an open question with an owner.
