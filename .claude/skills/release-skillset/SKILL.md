---
name: release-skillset
description: Cut a release of this skillset repository - decide the version bump from the changes since the last tag, update plugin.json, CHANGELOG.md and the printed canvas, run the checks, then tag and publish a GitHub release. Use when skill or canvas changes are ready to reach users, when the user asks to release, publish or bump the version, or after changes to skills/ or canvas/ have been merged.
metadata:
  internal: true
---

# Release skillset

Maintainer skill for this repository only. `metadata.internal` keeps `npx skills` from installing it, and `plugin.json` does not list it. Paths below come from the `## Agentic skillset builder` section of `AGENTS.md`.

The version lives in one place: `version` in `.claude-plugin/plugin.json`. Git tags (`vX.Y.Z`), the `CHANGELOG.md` heading, the printed canvas footer and the GitHub release always match it. Installed plugins only update when this version changes, so every change that should reach users needs a release.

## 1. Find what changed

- Last release: `git describe --tags --abbrev=0`. Check that it matches the version in `plugin.json`; if not, stop and report the mismatch. No tag yet: this is the first release, and the version in `plugin.json` is the one to publish.
- Changes: `git log --oneline <tag>..HEAD` and `git diff --stat <tag>..HEAD`.
- Release-relevant paths: `skills/`, `.claude-plugin/`, `canvas/`. Changes only in `README.md`, `docs/`, `design/`, `examples/` or repository files do not need a release; tell the user and stop unless they want one anyway.

Done when you have a list of user-facing changes, each tied to commits.

## 2. Decide the bump

| Bump | When | Examples |
|---|---|---|
| Major | Breaking for existing users or projects | skill removed or renamed; project files renamed or restructured; canvas blocks renumbered |
| Minor | New capability, nothing breaks | new skill; new step or stop point in a skill; new canvas prompt or block |
| Patch | Same behaviour, better wording or a fix | clarified instructions; fixed wrong reference; typo |

While the version is below 1.0.0, a breaking change bumps the minor version instead of the major.

Present the proposed version with the reason for each relevant change. **Stop point**: the user confirms or picks another version.

## 3. Update the files

1. `.claude-plugin/plugin.json`: set `version`.
2. `CHANGELOG.md`: turn `## Unreleased` into `## X.Y.Z (YYYY-MM-DD)`, or add that heading if there is none, and add a fresh empty `## Unreleased` above it. Every change from step 1 has an entry, written for users of the skills, not as commit messages.
3. Printed canvas: re-render it from the canvas template with the new version in the footer, using the command in the `- Printed canvas:` line of `AGENTS.md` (`render_canvas.py --print … --pdf …`). Look at the new PDF before going on.

## 4. Check

- `python3 scripts/check_skillset.py` passes.
- `claude plugin validate .` passes, if the `claude` CLI is available (an icon warning is fine).
- The new version appears in `plugin.json`, the `CHANGELOG.md` heading and the canvas footer; no other file names the old version as current.
- The latest dry run in `design/SIGNALS.md` is newer than the last change to any skill, or the user accepts releasing without one (record that in `design/DECISIONS.md`).

## 5. Publish

**Stop point**: show the diff and the release notes, and get the user's go-ahead. No `origin` remote yet: offer to create the GitHub repository first (`gh repo create <owner>/<name> --private --source . --push`), as `/setup-skillset` would. Then:

```bash
git commit -am "chore: release vX.Y.Z"
git tag -a vX.Y.Z -m "vX.Y.Z"
git push --follow-tags
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<the CHANGELOG section for X.Y.Z>"
```

Done when the tag and the GitHub release exist. Tell the user how installed copies update: `claude plugin marketplace update <marketplace>` followed by `claude plugin update <plugin>@<marketplace>`, or `npx skills update` for project copies.
