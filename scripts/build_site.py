#!/usr/bin/env python3
"""Assemble the website of a skillset (MkDocs Material) from the repository: README as start page, the course,
the canvas guide with the printed canvas and an interactive blank canvas, and the docs.

  python3 scripts/build_site.py              # writes build/site-src/ and build/mkdocs.yml
  mkdocs build -f build/mkdocs.yml           # writes build/site/   (needs: pip install mkdocs-material)

Links to files that are not part of the site (skills, LICENSE, design/, examples/ …) become links to the
repository on GitHub, taken from `repository` in .claude-plugin/plugin.json. Language from the
`- Language:` line of the `## Agentic skillset builder` section in AGENTS.md. Standard library only.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path.cwd()
OUT = ROOT / "build"
SRC = OUT / "site-src"
LINK = re.compile(r"(\]\()([^)\s#]+)(#[^)\s]*)?(\))")


def agents_lines():
    path = ROOT / "AGENTS.md"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    body = text.split("## Agentic skillset builder", 1)[1] if "## Agentic skillset builder" in text else ""
    body = re.split(r"^## ", body, flags=re.M)[0]
    return {m.group(1).strip().lower(): m.group(2).strip() for m in re.finditer(r"^- ([^:]+):\s*(.+)$", body, re.M)}


def repo_url():
    plugin = ROOT / ".claude-plugin" / "plugin.json"
    url = json.loads(plugin.read_text(encoding="utf-8")).get("repository", "") if plugin.exists() else ""
    return url.rstrip("/")


def rewrite(text, src_rel, dst_rel, published, repo):
    """Keep links to published files (relative to the new place), send all others to GitHub."""
    def fix(m):
        target = m.group(2)
        if re.match(r"[a-z]+:", target) or target.startswith("/"):
            return m.group(0)
        resolved = (pathlib.PurePosixPath(src_rel).parent / target)
        parts = []
        for p in resolved.parts:
            if p == "..":
                parts = parts[:-1]
            elif p != ".":
                parts.append(p)
        resolved = "/".join(parts)
        key = resolved.rstrip("/")
        if key in published:
            new = published[key]
            depth = len(pathlib.PurePosixPath(dst_rel).parent.parts)
            rel = "../" * depth + new
            return f"{m.group(1)}{rel}{m.group(3) or ''}{m.group(4)}"
        if not repo:
            return m.group(0)
        kind = "tree" if target.endswith("/") or (ROOT / resolved).is_dir() else "blob"
        return f"{m.group(1)}{repo}/{kind}/main/{resolved}{m.group(3) or ''}{m.group(4)}"
    return LINK.sub(fix, text)


def main():
    if OUT.exists():
        shutil.rmtree(SRC, ignore_errors=True)
    SRC.mkdir(parents=True, exist_ok=True)
    lines = agents_lines()
    lang = lines.get("language", "en").split()[0]
    repo = repo_url()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", readme, re.M).group(1).strip()

    # What gets published, and where: source path -> site path.
    pages = {"README.md": "index.md"}
    for folder in ("canvas", "docs", "course/docs"):
        for md in sorted((ROOT / folder).glob("*.md")) if (ROOT / folder).exists() else []:
            pages[str(md.relative_to(ROOT))] = str(md.relative_to(ROOT))
    assets = {}
    for f in sorted((ROOT / "canvas").glob("*")) if (ROOT / "canvas").exists() else []:
        if f.suffix in (".svg", ".pdf", ".png"):
            assets[str(f.relative_to(ROOT))] = str(f.relative_to(ROOT))
    published = {**pages, **assets}
    published.update({k.rsplit("/", 1)[0]: v.rsplit("/", 1)[0] + "/"
                      for k, v in pages.items() if k.endswith("/index.md")})
    published.update({"course/docs": "course/docs/", "canvas": "canvas/"})

    for src, dst in pages.items():
        text = (ROOT / src).read_text(encoding="utf-8")
        (SRC / dst).parent.mkdir(parents=True, exist_ok=True)
        (SRC / dst).write_text(rewrite(text, src, dst, published, repo), encoding="utf-8")
    for src, dst in assets.items():
        (SRC / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / src, SRC / dst)
    if "canvas/README.md" in pages:
        shutil.move(str(SRC / "canvas/README.md"), str(SRC / "canvas/index.md"))
        pages["canvas/README.md"] = "canvas/index.md"

    # The interactive blank canvas, rendered by the core renderer.
    template = lines.get("canvas template", "")
    tpl = re.search(r"`([^`]+)`", template)
    renderer = ROOT / "skills/show-canvas/scripts/render_canvas.py"
    if tpl and renderer.exists() and (ROOT / tpl.group(1)).exists():
        subprocess.run([sys.executable, str(renderer), tpl.group(1), "--lang", lang,
                        "--out", str(SRC / "canvas/leer.html")], check=True, stdout=subprocess.DEVNULL)

    # Navigation.
    nav = [f"  - {'Start' if lang == 'de' else 'Home'}: index.md"]
    course = sorted(p for s, p in pages.items() if s.startswith("course/docs/"))
    if course:
        first = [p for p in course if p.endswith("/index.md")]
        nav.append(f"  - {'Kurs' if lang == 'de' else 'Course'}:")
        nav += [f"      - {p}" for p in first + [p for p in course if p not in first]]
    if "canvas/README.md" in pages:
        nav.append("  - Canvas: canvas/index.md")
    docs = sorted(p for s, p in pages.items() if s.startswith("docs/"))
    if docs:
        nav.append(f"  - {'Doku' if lang == 'de' else 'Docs'}:")
        nav += [f"      - {p}" for p in docs]

    (OUT / "mkdocs.yml").write_text(f"""site_name: {json.dumps(title, ensure_ascii=False)}
site_url: ""
repo_url: {repo or '""'}
docs_dir: site-src
site_dir: site
theme:
  name: material
  language: {lang}
  features: [navigation.sections, navigation.footer, content.code.copy, search.highlight]
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle: {{icon: material/brightness-7, name: Dark}}
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle: {{icon: material/brightness-4, name: Light}}
markdown_extensions:
  - admonition
  - attr_list
  - tables
  - toc: {{permalink: true}}
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.keys
  - pymdownx.tabbed: {{alternate_style: true}}
  - pymdownx.tasklist: {{custom_checkbox: true}}
validation:
  links: {{not_found: warn, unrecognized_links: info, anchors: info}}
nav:
{chr(10).join(nav)}
""", encoding="utf-8")
    print(f"Wrote {SRC.relative_to(ROOT)} ({len(pages)} pages, {len(assets)} files) and build/mkdocs.yml")


if __name__ == "__main__":
    main()
