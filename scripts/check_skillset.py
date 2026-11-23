#!/usr/bin/env python3
"""Check a skillset repository against the conventions of the agentic skillset builder.

Run from the repository root:  python3 scripts/check_skillset.py   (exit code 1 if a check fails)

Checks:
  plugin-list    every skills/**/SKILL.md is listed in .claude-plugin/plugin.json, and every listed path exists
  frontmatter    every SKILL.md has name (equal to its folder) and description; descriptions fit the 1024-char limit
  skill-refs     every `/skill-name` written in backticks in Markdown names a skill of this repo or of the builder
                 (folders named in the AGENTS.md line "- Other skillsets in: `path/`" are skipped)
  agents         AGENTS.md has a `## Agentic skillset builder` section with Language, Canvas template, Printed canvas
  printed-canvas the printed canvas SVG was made from the current canvas template
  core           verbatim core files listed in .skillset-core.json are unchanged since the last sync

Standard library only.
"""
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path.cwd()
SECTION = "## Agentic skillset builder"
# Agent built-in commands and placeholders that are not skills.
BUILTIN = {"mcp", "help", "clear", "compact", "config", "init", "model", "plugin", "plugins", "agents", "permissions",
           "memory", "review", "skills", "status", "login", "logout", "command", "skill", "name"}
# Skills of the Agentic Skillset Builder: skillset repos refer to them in design/, AGENTS.md and the release skill.
BUILDER_SKILLS = {"setup-skillset", "ask-builder", "grill-practice", "map-sources", "design-canvas", "to-skill-map",
                  "draft-skill", "dry-run", "review-skillset", "skillset-retro", "sync-core", "show-canvas"}
results = []


def report(check, ok, message):
    results.append((check, ok, message))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).splitlines():
        if (kv := re.match(r"([A-Za-z0-9_-]+):\s*(.*)", line)) and not line.startswith(" "):
            key, value = kv.group(1), kv.group(2).strip()
            fields[key] = value.strip('"').strip("'")
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def agents_section():
    path = ROOT / "AGENTS.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if SECTION not in text:
        return None
    body = text.split(SECTION, 1)[1]
    body = re.split(r"^## ", body, flags=re.M)[0]
    lines = {}
    for m in re.finditer(r"^- ([^:]+):\s*(.+)$", body, re.M):
        lines[m.group(1).strip().lower()] = m.group(2).strip()
    return lines


def first_path(value):
    m = re.search(r"`([^`]+)`", value)
    return m.group(1).split()[0] if m else value.split()[0]


def main():
    skills = {p.parent for p in (ROOT / "skills").rglob("SKILL.md")} if (ROOT / "skills").exists() else set()
    names = set()

    # plugin-list
    plugin = ROOT / ".claude-plugin" / "plugin.json"
    if plugin.exists():
        listed = {(ROOT / s).resolve() for s in json.loads(plugin.read_text(encoding="utf-8")).get("skills", [])}
        present = {s.resolve() for s in skills}
        missing = sorted(str(p.relative_to(ROOT)) for p in present - listed)
        dangling = sorted(str(p) for p in listed - present)
        report("plugin-list", not missing and not dangling,
               "all skills listed" if not missing and not dangling else
               f"not in plugin.json: {missing or '-'}; listed but missing: {dangling or '-'}")
    else:
        report("plugin-list", False, ".claude-plugin/plugin.json not found")

    # frontmatter
    problems = []
    for folder in sorted(skills | {p.parent for p in (ROOT / ".claude" / "skills").rglob("SKILL.md")}):
        fm = frontmatter(folder / "SKILL.md")
        rel = folder.relative_to(ROOT)
        if fm is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        names.add(fm.get("name", ""))
        if fm.get("name") != folder.name:
            problems.append(f"{rel}: name '{fm.get('name')}' differs from folder")
        if not fm.get("description"):
            problems.append(f"{rel}: no description")
        elif len(fm["description"]) > 1024:
            problems.append(f"{rel}: description longer than 1024 characters")
    report("frontmatter", not problems, "; ".join(problems) or f"{len(skills)} skills ok")

    # skill-refs (folders listed in the AGENTS line "Other skillsets in" use another skillset's commands)
    other = [ROOT / p for p in re.findall(r"`([^`]+)`", (agents_section() or {}).get("other skillsets in", ""))]
    unknown = {}
    for md in ROOT.rglob("*.md"):
        if any(part in (".git", "node_modules", "build") for part in md.parts):
            continue
        if any(o in md.parents for o in other):
            continue
        for ref in re.findall(r"`/([a-z][a-z0-9-]*)(?=[\s`])", md.read_text(encoding="utf-8")):
            if ref not in names | BUILDER_SKILLS | BUILTIN:
                unknown.setdefault(ref, set()).add(str(md.relative_to(ROOT)))
    report("skill-refs", not unknown,
           "; ".join(f"/{r} in {', '.join(sorted(f))}" for r, f in sorted(unknown.items())) or "all skill references resolve")

    # agents
    section = agents_section()
    needed = ("language", "canvas template", "printed canvas")
    if section is None:
        report("agents", False, f"AGENTS.md has no '{SECTION}' section")
    else:
        absent = [n for n in needed if n not in section]
        report("agents", not absent, f"missing lines: {', '.join(absent)}" if absent else "section complete")

    # printed-canvas
    if section and "canvas template" in section and "printed canvas" in section:
        template = ROOT / first_path(section["canvas template"])
        svgs = re.findall(r"[\w./-]+\.svg", section["printed canvas"])
        if not template.exists():
            report("printed-canvas", False, f"canvas template {template.relative_to(ROOT)} not found")
        elif not svgs or not (ROOT / svgs[0]).exists():
            report("printed-canvas", False, "printed canvas SVG not found")
        else:
            m = re.search(r"template-sha256:([0-9a-f]+)", (ROOT / svgs[0]).read_text(encoding="utf-8"))
            current = hashlib.sha256(template.read_text(encoding="utf-8").encode("utf-8")).hexdigest()[:12]
            report("printed-canvas", bool(m) and m.group(1) == current,
                   "printed canvas matches the template" if m and m.group(1) == current else
                   f"{svgs[0]} is older than {template.relative_to(ROOT)}: re-render with render_canvas.py --print")

    # core
    lock = ROOT / ".skillset-core.json"
    if lock.exists():
        changed = []
        for f in json.loads(lock.read_text(encoding="utf-8")).get("files", []):
            path = ROOT / f["path"]
            if f.get("mode") == "verbatim" and (not path.exists() or sha(path) != f.get("sha")):
                changed.append(f["path"])
        report("core", not changed, f"verbatim core files changed locally: {', '.join(changed)} "
               "(move the change into the builder's core, or record a decision)" if changed else "core files unchanged")
    else:
        report("core", False, ".skillset-core.json not found: run /sync-core from the agentic skillset builder")

    width = max(len(c) for c, _, _ in results)
    for check, ok, message in results:
        print(f"{'PASS' if ok else 'FAIL'}  {check.ljust(width)}  {message}")
    sys.exit(0 if all(ok for _, ok, _ in results) else 1)


if __name__ == "__main__":
    main()
