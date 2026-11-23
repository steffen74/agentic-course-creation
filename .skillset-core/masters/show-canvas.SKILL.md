---
name: show-canvas
description: Show the current canvas as a page in the browser, laid out like the printed canvas, with empty blocks and decisions newer than the canvas marked. Add "live" to keep it updating while you work.
disable-model-invocation: true
---

# Show canvas

Render the canvas as one HTML page with [`scripts/render_canvas.py`](scripts/render_canvas.py). The script needs only the canvas grammar (`## Section` columns between `---` rules, `### N. Block 👤|🤖` blocks), so it reads the canvas of every agentic skillset.

## 1. Render

On Windows, Python is usually called `python` (or `py`); `python3` there may open the Microsoft Store instead. Use whichever runs.

Find the section this skillset added to `AGENTS.md` (the one with a `- Canvas:` line). Run the script on that canvas, with the language from its `- Language:` line (default `en`):

```
python3 <skill dir>/scripts/render_canvas.py <canvas> --lang <language> --out build/canvas.html
```

It reads `DECISIONS.md` next to the canvas when it exists (`--decisions <file>` otherwise). If `build/` is not in `.gitignore`, say so and offer to add it: the page is a view, the canvas stays the source.

With **live** after the command, add `--watch` and start it as a background process: it re-renders whenever the canvas or the decision log changes, and the open page reloads itself every few seconds. Tell the user how to stop it.

If no Python is available, say so in one sentence, show the canvas file itself instead (its blocks in order, empty ones marked), and offer to help install Python 3.

Done when the page exists and the user has its path (or it is open in a browser pane, if your agent has one), or the canvas was shown as text because Python is missing.

## 2. Point out what the page shows

In at most three lines, from the page's own markers:

- **Empty blocks** (dashed, “Not decided yet” / “Not drafted yet”), by number. An empty 👤 block is a decision nobody has made yet; recommend the skill that fills it, as the skillset's router skill would.
- **Decisions newer than the canvas** (from the *Version* date): the blocks they touch may be out of date. Offer to update those blocks; the person who owns the block approves each change.
- **Open questions** without an owner or date.

Change the canvas in this skill only after a yes. Treat the page like the canvas itself: it stays wherever the canvas lives and is never published elsewhere.
