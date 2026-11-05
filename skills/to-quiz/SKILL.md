---
name: to-quiz
description: Write the quiz for one unit (for example a video check at the start of the session) into the course's quiz source, then create it in the course's quiz tool - through a connector if one is connected, otherwise as an import file. Type the unit after the command.
disable-model-invocation: true
---

# To quiz

Write and publish the quiz for one unit. Read `COURSE-CANVAS.md`, `PLAN.md`, `RESOURCES.md`, `DECISIONS.md`, the `## Agentic course creation` section of `AGENTS.md`, and the material of the unit before (the videos and tasks the quiz covers). Load `assumed-knowledge`.

## 1. Tool and source

`AGENTS.md` should have a line `- Quizzes: <source file>, tool <name>, connector <name|none>`, set in `/setup-course`. If it is missing, ask once, recommend, and write it:

- **Source**: one file in the private course repository holds every question with options, correct answer and explanation (a CSV with the columns `session, type, question, option_a, option_b, option_c[, option_d], correct, explanation`, or Markdown that mirrors it). The quiz tool is a copy, never the source.
- **Tool**: chosen once per course, for example Microsoft Forms or Formbricks. Scoring is optional; most video checks only need the distribution of answers to discuss in class.
- **House style**, asked once with the tool: how quizzes are titled (for example `Session <n> · <unit title>`), the text under the title, closing questions every quiz ends with (feedback on the week, whether the homework got done; a small CSV with `question, options`, options separated by ` | `, empty for open text), and the look (theme, background). Ask for a screenshot of an earlier quiz. Write it into the Quizzes line, for example `…, title "Session <n> · <unit title>", closing questions <file>, theme <how it is applied>`.

## 2. Write the questions

Draft three to five questions for the unit, each with:

- a question about something learners met **before** the session: the videos and tasks of the previous unit. Never ask about content the session itself introduces.
- three or four options, one correct; wrong options are the misunderstandings learners actually have (from `SIGNALS.md` where available), not trick questions.
- an explanation of one or two sentences, for the instructor to use in class.
- a type: *video*, *task* or *skill*, with its source.

Base questions on what the material actually says. When a question rests on a video you cannot read, mark it *from the title only* in the explanation; the instructor checks it against the video.

Show the questions and wait for the instructor. Then write them into the source.

## 3. Create in the tool

- **Connector connected** for the tool: show the quiz as it will be created, wait for a yes, create it as a draft, and record its share link. Build the request from the quiz source in the connector’s own schema (read its tool descriptions; schemas change between versions), and use its validation tool first when it has one.
  - Formbricks has an official MCP server with OAuth sign-in (`https://app.formbricks.com/api/mcp`, or `https://<domain>/api/mcp` when self-hosted; tools include `list_workspaces`, `validate_survey`, `create_survey`). If the course uses Formbricks and it is not connected, give the instructor the command to add it to their agent (in Claude Code: `claude mcp add --transport http formbricks https://app.formbricks.com/api/mcp`, then sign in via `/mcp`); do not change their agent configuration yourself.
  - Microsoft Forms has no API for creating quizzes and no official connector; use the export below.
- **No connector**: export with [`scripts/export_quiz.py`](scripts/export_quiz.py) from the CSV source:
  - Formbricks: `--format formbricks` writes a survey body for the Management API and prints the `curl` command. The instructor runs it with their own API key from an environment variable; never ask for the key or write it into a file.
  - Microsoft Forms: `--format forms` writes a `.docx` for *Quick Import* and an answer key. Quick Import does not take correct answers, *Required* or a theme; the instructor ticks answers from the key (only needed when scoring is used), sets *Required* on closing questions and applies the theme under *Style*.
  - Pass the house style: `--name` (the title), `--description` and `--closing <file>`.
  - Another tool: write the closest import format it accepts, or a plain list to paste.

Answers and explanations never appear in a participant-facing file or in a public location.

## 4. Hand over

Record the quiz link in `RESOURCES.md` for the unit (column *Quiz*). The slides show the link (and a QR code, where the slide format allows), not the questions; `/to-slides` takes it from `RESOURCES.md`.

Done when the questions are in the source, the quiz exists in the tool as a draft or an import file is ready with instructions, and its link or status is in `RESOURCES.md`.
