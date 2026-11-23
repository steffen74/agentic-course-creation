#!/usr/bin/env python3
"""Render a canvas file (the canvas of any agentic skillset) as an HTML page, or as a printable A4 SVG/PDF.

Canvas grammar: `# Title`, header fields `**Field:** value`, an owner legend `> Owners: 👤 … · 🤖 …`,
columns as `## Section` between `---` rules, blocks as `### N. Block 👤|🤖`, and sections after the last
rule (open questions, decision log) below the grid. HTML comments in a block are its hint; a comment
`<!-- print: first line | second line -->` holds the two short prompts of the printed canvas.

Page mode (default): one card per block. Empty blocks show their hint and are marked as not decided (👤)
or not drafted (🤖). With a decision log (DECISIONS.md next to the canvas, entries `## YYYY-MM-DD: title`
with a line `**Canvas:** 3, 5` or `**Canvas block:** 3`), each block shows how many decisions touch it and
those newer than the canvas version date.

Print mode (--print): the blank canvas as an A4 landscape SVG, from the template. --pdf also prints it to
PDF with a local Chrome or Chromium. The SVG records the hash of the template it was made from, so a check
can tell when the printed canvas is out of date.

  render_canvas.py CANVAS.md                                   # writes build/canvas.html
  render_canvas.py CANVAS.md --out build/canvas.html --decisions DECISIONS.md --lang de
  render_canvas.py CANVAS.md --watch                           # re-render on every change; the page reloads itself
  render_canvas.py templates/CANVAS.md --print --out canvas/x-canvas.svg --pdf canvas/x-canvas.pdf \\
      --subtitle "One line under the title" --footer "X Canvas v0.1 · CC BY 4.0 · github.com/…"

Standard library only.
"""
import argparse
import datetime
import hashlib
import html
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time

OWNERS = {"👤": "human", "🤖": "agent"}
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
PRINT = re.compile(r"<!--\s*print:(.*?)-->", re.S | re.I)

LABELS = {
    "en": {"decides": "{role} decides", "drafts": "Agent drafts", "approves": "Agent drafts, {role} approves",
           "role": "human", "not_decided": "Not decided yet", "not_drafted": "Not drafted yet",
           "filled": "{n} of {total} blocks filled", "version": "version", "decision": "decision",
           "decisions": "decisions", "newer": "newer than the canvas", "new": "new", "nothing": "Nothing yet.",
           "older": "{n} older decisions in the log.", "rendered": "Rendered from"},
    "de": {"decides": "{role} entscheidet", "drafts": "Agent entwirft", "approves": "Agent entwirft, {role} bestätigt",
           "role": "Mensch", "not_decided": "Noch nicht entschieden", "not_drafted": "Noch nicht entworfen",
           "filled": "{n} von {total} Blöcken ausgefüllt", "version": "Version", "decision": "Entscheidung",
           "decisions": "Entscheidungen", "newer": "neuer als das Canvas", "new": "neu", "nothing": "Noch nichts.",
           "older": "{n} ältere Entscheidungen im Log.", "rendered": "Erzeugt aus"},
}


def inline(text):
    # Escape first, then the few inline marks canvases use.
    s = html.escape(text, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', s)
    return s


def markdown(lines):
    """Paragraphs, lists and quotes: enough for canvas blocks, nothing more."""
    out, para, items = [], [], []

    def flush():
        if para:
            out.append("<p>" + "<br>".join(inline(l) for l in para) + "</p>")
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    for line in lines:
        line = line.rstrip()
        if not line.strip():
            flush()
        elif re.match(r"\s*[-*] ", line):
            if para:
                flush()
            items.append(re.sub(r"^\s*[-*] ", "", line))
        elif line.startswith(">"):
            flush()
            out.append(f"<blockquote>{inline(line.lstrip('> '))}</blockquote>")
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return "\n".join(out)


def strip_comments(text):
    """Return (text without comments, hint, print lines)."""
    prints = [p.strip() for m in PRINT.findall(text) for p in m.split("|") if p.strip()]
    text = PRINT.sub("", text)
    hints = [h.strip() for h in re.findall(r"<!--(.*?)-->", text, re.S)]
    return re.sub(r"<!--.*?-->", "", text, flags=re.S), " ".join(hints), prints


def parse_legend(legend):
    """'👤 instructor decides · 🤖 agent drafts, instructor approves' -> labels for both owners."""
    parts = {}
    for part in re.split(r"\s+·\s+", legend):
        for emoji, owner in OWNERS.items():
            if part.strip().startswith(emoji):
                parts[owner] = part.strip()[len(emoji):].strip().rstrip(".")
    return parts


def parse_canvas(text):
    title, fields, legend = "Canvas", [], ""
    groups, tail = [], []          # groups: columns between rules; tail: sections after the last rule
    current = None                 # the section ("##") being filled
    block = None                   # the block ("###") being filled
    seen_rule = False

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("# ") and not groups and not seen_rule:
            title = line[2:].strip()
        elif not seen_rule and (m := re.match(r"\*\*(.+?):\*\*\s*(.*)", line)):
            fields.append((m.group(1), strip_comments(m.group(2))[0].strip()))
        elif not seen_rule and line.startswith("> Owners:"):
            legend = line[len("> Owners:"):].strip()
        elif line.strip() == "---":
            seen_rule = True
            block = None
            current = None
        elif line.startswith("## "):
            current = {"name": line[3:].strip(), "blocks": [], "lines": []}
            block = None
            groups.append(current)
        elif line.startswith("### ") and current is not None:
            m = re.match(r"###\s+(\d+)\.?\s+(.*?)\s*(👤|🤖)?\s*$", line)
            number, name, owner = (m.group(1), m.group(2), m.group(3)) if m else ("", line[4:], None)
            block = {"number": number, "name": name, "owner": OWNERS.get(owner), "lines": []}
            current["blocks"].append(block)
        elif block is not None:
            block["lines"].append(line)
        elif current is not None:
            current["lines"].append(line)

    # Sections without blocks after the columns (open questions, decision log) go below the grid.
    while groups and not groups[-1]["blocks"]:
        tail.insert(0, groups.pop())
    for g in groups + tail:
        for b in g["blocks"]:
            body, b["hint"], b["print"] = strip_comments("\n".join(b["lines"]))
            b["html"], b["empty"] = markdown(body.splitlines()), not body.strip()
        body, g["hint"], g["print"] = strip_comments("\n".join(g["lines"]))
        g["html"], g["empty"] = markdown(body.splitlines()), not body.strip()
    return {"title": title, "fields": fields, "legend": legend, "owners": parse_legend(legend),
            "columns": groups, "tail": tail}


def parse_decisions(path):
    if not path or not path.exists():
        return []
    text = strip_comments(path.read_text(encoding="utf-8"))[0]
    decisions = []
    for chunk in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        date = DATE.search(head)
        title = head.split(":", 1)[1].strip() if ":" in head else head.strip()
        blocks = re.search(r"\*\*Canvas(?: blocks?)?:\*\*\s*(.+)", body)
        decisions.append({"date": date.group(0) if date else "", "title": title,
                          "blocks": set(re.findall(r"\d+", blocks.group(1))) if blocks else set()})
    return decisions


def version_date(fields):
    for key, value in fields:
        if key.lower() in ("version", "updated", "last update", "stand") and (m := DATE.search(value)):
            return m.group(0)
    return ""


def labels_for(canvas, lang):
    """Badge and legend texts: from the canvas's own owner legend where it has one."""
    L = dict(LABELS.get(lang, LABELS["en"]))
    role = L["role"]
    if "instructor" in canvas["legend"]:      # Agentic Course Creation canvases before the legend parser
        role = "instructor"
    human = canvas["owners"].get("human") or L["decides"].format(role=role)
    agent = canvas["owners"].get("agent") or L["approves"].format(role=role)
    return L, human[:1].upper() + human[1:], agent[:1].upper() + agent[1:]


def card(b, decisions, since, L, human):
    touching = [d for d in decisions if b["number"] in d["blocks"]]
    newer = [d for d in touching if since and d["date"] > since]
    owner = b["owner"] or "human"
    badge = human if owner == "human" else L["drafts"]
    state = ""
    if b["empty"]:
        state = '<p class="state">' + (L["not_decided"] if owner == "human" else L["not_drafted"]) + "</p>"
    meta = []
    if touching:
        meta.append(f'{len(touching)} {L["decision"] if len(touching) == 1 else L["decisions"]}')
    if newer:
        titles = "&#10;".join(html.escape(f'{d["date"]}: {d["title"]}') for d in newer)
        meta.append(f'<span class="newer" title="{titles}">{len(newer)} {L["newer"]}</span>')
    hint = f' title="{html.escape(b["hint"])}"' if b["hint"] else ""
    body = b["html"] if not b["empty"] else f'<p class="hint">{html.escape(b["hint"])}</p>'
    return f"""<section class="block {owner}{' empty' if b['empty'] else ''}"{hint}>
  <header><h3><span class="num">{b['number']}</span> {inline(b['name'])}</h3><span class="badge">{html.escape(badge)}</span></header>
  {state}<div class="body">{body}</div>
  {'<footer>' + ' · '.join(meta) + '</footer>' if meta else ''}
</section>"""


def is_log(section):
    name = section["name"].lower()
    return "decision" in name or "entscheid" in name


def render(canvas, decisions, source, watch, lang):
    since = version_date(canvas["fields"])
    L, human, agent = labels_for(canvas, lang)
    rows = max((len(c["blocks"]) for c in canvas["columns"]), default=1)
    columns = []
    for c in canvas["columns"]:
        cards = []
        for i, b in enumerate(c["blocks"]):
            span = rows - i if i == len(c["blocks"]) - 1 else 1   # the last block fills its column
            cards.append(f'<div style="grid-row: span {span}">{card(b, decisions, since, L, human)}</div>')
        columns.append(f'<div class="column"><h2>{inline(c["name"])}</h2>'
                       f'<div class="cards" style="grid-template-rows: repeat({rows}, auto)">{"".join(cards)}</div></div>')

    tail = []
    for t in canvas["tail"]:
        if is_log(t) and decisions:
            items = "".join(
                f'<li><time>{d["date"]}</time> {inline(d["title"])}'
                f'{" <span class=blocks>" + ", ".join(sorted(d["blocks"], key=int)) + "</span>" if d["blocks"] else ""}'
                f'{" <span class=newer>" + L["new"] + "</span>" if since and d["date"] > since else ""}</li>'
                for d in decisions[:8])
            more = f'<p class="hint">{L["older"].format(n=len(decisions) - 8)}</p>' if len(decisions) > 8 else ""
            body = f"<ul class=log>{items}</ul>{more}"
        elif t["empty"]:
            body = f'<p class="hint">{html.escape(t["hint"]) or L["nothing"]}</p>'
        else:
            body = t["html"]
        tail.append(f'<section class="note"><h3>{inline(t["name"])}</h3>{body}</section>')

    filled = sum(not b["empty"] for c in canvas["columns"] for b in c["blocks"])
    total = sum(len(c["blocks"]) for c in canvas["columns"])
    fields = "".join(f"<div><dt>{inline(k)}</dt><dd>{inline(v) or '–'}</dd></div>" for k, v in canvas["fields"])
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    refresh = '<meta http-equiv="refresh" content="3">' if watch else ""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{refresh}
<title>{html.escape(canvas['title'])}</title>
<style>{CSS}</style></head>
<body>
<header class="top">
  <div><h1>{inline(canvas['title'])}</h1>
  <p class="sub">{L['filled'].format(n=filled, total=total)}{' · ' + L['version'] + ' ' + since if since else ''}</p></div>
  <dl>{fields}</dl>
</header>
<main class="grid" style="grid-template-columns: repeat({len(columns)}, minmax(0, 1fr))">{''.join(columns)}</main>
<div class="tail">{''.join(tail)}</div>
<footer class="legend">
  <span><i class="sw human"></i>{html.escape(human)}</span>
  <span><i class="sw agent"></i>{html.escape(agent)}</span>
  <span class="src">{L['rendered']} <code>{html.escape(source.name)}</code> · {stamp}</span>
</footer>
</body></html>
"""


CSS = """
:root { --bg:#fff; --ink:#2C2C2A; --muted:#5F5E5A; --rule:#B4B2A9;
  --h-bg:#EEEDFE; --h-line:#534AB7; --h-ink:#3C3489; --a-bg:#E1F5EE; --a-line:#0F6E56; --a-ink:#085041;
  --n-bg:#F1EFE8; --n-line:#888780; --warn:#B4531F; }
@media (prefers-color-scheme: dark) { :root { --bg:#1B1B1A; --ink:#E8E6DF; --muted:#A6A49C; --rule:#4A4944;
  --h-bg:#26234A; --h-line:#8F87E8; --h-ink:#CFCBFF; --a-bg:#12352C; --a-line:#4CB894; --a-ink:#BFEBDC;
  --n-bg:#2A2926; --n-line:#77756E; --warn:#F0A06A; } }
* { box-sizing: border-box; }
body { margin: 0; padding: 24px 30px; background: var(--bg); color: var(--ink);
  font: 13px/1.45 Helvetica, Arial, sans-serif; }
.top { display: flex; justify-content: space-between; gap: 24px; flex-wrap: wrap; align-items: flex-start; }
h1 { margin: 0; font-size: 26px; }
.sub { margin: 4px 0 0; color: var(--muted); }
dl { display: flex; gap: 28px; margin: 0; flex-wrap: wrap; }
dt { font-size: 11px; color: var(--muted); } dd { margin: 2px 0 0; border-top: 1px solid var(--rule); padding-top: 3px; }
.grid { display: grid; gap: 18px; margin-top: 18px; }
.column h2 { font-size: 15px; margin: 0 0 8px; }
.cards { display: grid; gap: 12px; height: calc(100% - 28px); }
.cards > div { display: flex; } .block { flex: 1; }
.block { border: 1px solid; border-radius: 8px; padding: 10px 14px 12px; display: flex; flex-direction: column; }
.block.human { background: var(--h-bg); border-color: var(--h-line); color: var(--h-ink); }
.block.agent { background: var(--a-bg); border-color: var(--a-line); color: var(--a-ink); }
.block.empty { border-style: dashed; border-width: 2px; }
.block header { display: flex; justify-content: space-between; gap: 8px; align-items: baseline; }
h3 { margin: 0; font-size: 16px; } .num { opacity: .7; margin-right: 4px; }
.badge { font-size: 11px; border: 1px solid currentColor; border-radius: 10px; padding: 1px 8px; background: var(--bg); white-space: nowrap; }
.body { color: var(--ink); } .body p { margin: 6px 0; } .body ul { margin: 6px 0; padding-left: 18px; }
.hint { color: var(--muted); font-style: italic; }
.state { margin: 6px 0 0; font-weight: 700; color: var(--warn); }
.block footer { margin-top: auto; padding-top: 6px; font-size: 11px; color: var(--muted); }
.newer { color: var(--warn); font-weight: 700; }
code { font-size: 12px; }
a { color: inherit; }
blockquote { margin: 6px 0; padding-left: 8px; border-left: 3px solid var(--rule); color: var(--muted); }
.tail { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 18px; }
.note { background: var(--n-bg); border: 1px solid var(--n-line); border-radius: 8px; padding: 10px 14px; }
.note h3 { font-size: 15px; }
.log { list-style: none; padding: 0; margin: 6px 0; } .log li { margin: 3px 0; }
.log time { color: var(--muted); font-variant-numeric: tabular-nums; margin-right: 6px; }
.blocks { font-size: 11px; border: 1px solid var(--rule); border-radius: 8px; padding: 0 6px; color: var(--muted); }
.legend { display: flex; gap: 20px; margin-top: 16px; font-size: 11.5px; flex-wrap: wrap; }
.sw { display: inline-block; width: 13px; height: 13px; border-radius: 3px; border: 1px solid; vertical-align: -2px; margin-right: 6px; }
.sw.human { background: var(--h-bg); border-color: var(--h-line); } .sw.agent { background: var(--a-bg); border-color: var(--a-line); }
.src { margin-left: auto; color: var(--muted); }
@media (max-width: 900px) { body { padding: 16px; } .grid, .tail { grid-template-columns: 1fr !important; }
  .cards { grid-template-rows: none !important; height: auto; } .cards > div { grid-row: auto !important; } }
@media print { @page { size: A3 landscape; margin: 10mm; } body { padding: 0; } .block { break-inside: avoid; } }
"""


# ---------------------------------------------------------------- print mode (A4 landscape SVG)

W, H, M = 1188, 840, 30                 # viewBox in px at 4 px/mm; margin
COL = {"human": ("#EEEDFE", "#534AB7", "#3C3489"), "agent": ("#E1F5EE", "#0F6E56", "#085041")}


def esc(s):
    return html.escape(s, quote=True)


def badge_width(text):
    return round(len(text) * 6.0 + 22)


def wrap(text, width):
    return textwrap.wrap(text, width) if text else []


def svg(canvas, source_text, subtitle, footer, lang):
    L, human, agent = labels_for(canvas, lang)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="210mm" viewBox="0 0 {W} {H}" '
           f'font-family="Helvetica, Arial, sans-serif">',
           f'<title>{esc(canvas["title"])}</title>',
           f'<desc>template-sha256:{hashlib.sha256(source_text.encode("utf-8")).hexdigest()[:12]}</desc>',
           f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>',
           f'<text x="{M}" y="58" font-size="26" font-weight="700" fill="#2C2C2A">{esc(canvas["title"])}</text>']
    if subtitle:                               # shrink a long subtitle so it stays left of the header fields
        sub_size = 13 if len(subtitle) * 6.6 <= 590 else max(9, round(13 * 590 / (len(subtitle) * 6.6), 1))
        out.append(f'<text x="{M}" y="82" font-size="{sub_size}" fill="#5F5E5A">{esc(subtitle)}</text>')

    # Header fields as labelled lines on the right, at most three (Version is printed in the footer).
    fields = [k for k, _ in canvas["fields"] if k.lower() not in ("version", "stand")][:3]
    x, right = 640, W - M
    slot = (right - x) / max(len(fields), 1)
    for i, name in enumerate(fields):
        fx = x + i * slot
        out.append(f'<text x="{fx:.0f}" y="50" font-size="11" fill="#5F5E5A">{esc(name)}</text>'
                   f'<line x1="{fx:.0f}" y1="78" x2="{fx + slot - 30:.0f}" y2="78" stroke="#B4B2A9" stroke-width="1"/>')

    cols = canvas["columns"]
    gap = 18
    cw = (W - 2 * M - gap * (len(cols) - 1)) / max(len(cols), 1)
    top, tail_h = 125, (80 if canvas["tail"] else 0)
    bottom = H - 50 - (tail_h + 16 if tail_h else 0)
    rows = max((len(c["blocks"]) for c in cols), default=1)
    bh = (bottom - top - 12 * (rows - 1)) / rows
    chars = int(cw / 6.4)
    for ci, c in enumerate(cols):
        cx = M + ci * (cw + gap)
        out.append(f'<text x="{cx:.0f}" y="112" font-size="15" font-weight="700" fill="#2C2C2A">{esc(c["name"])}</text>')
        for i, b in enumerate(c["blocks"]):
            owner = b["owner"] or "human"
            fill, line, ink = COL[owner]
            y = top + i * (bh + 12)
            h = bottom - y if i == len(c["blocks"]) - 1 else bh
            text = human if owner == "human" else L["drafts"]
            text = text[:1].lower() + text[1:] if lang == "en" else text
            bw = badge_width(text)
            out.append(f'<rect x="{cx:.0f}" y="{y:.0f}" width="{cw:.0f}" height="{h:.0f}" rx="8" fill="{fill}" stroke="{line}" stroke-width="1"/>')
            title = f'{b["number"]}  {b["name"]}'
            room = cw - bw - 34                       # space left of the badge
            size = 17 if len(title) * 9.0 <= room else max(11, int(17 * room / (len(title) * 9.0)))
            out.append(f'<text x="{cx + 14:.0f}" y="{y + 26:.0f}" font-size="{size}" font-weight="700" fill="{ink}">'
                       f'{esc(b["number"])}  {esc(b["name"])}</text>')
            out.append(f'<rect x="{cx + cw - 10 - bw:.0f}" y="{y + 11:.0f}" width="{bw}" height="20" rx="10" fill="#FFFFFF" stroke="{line}" stroke-width="0.8"/>'
                       f'<text x="{cx + cw - 10 - bw / 2:.1f}" y="{y + 25:.0f}" font-size="11" text-anchor="middle" fill="{ink}">{esc(text)}</text>')
            prompts = b["print"]
            if not prompts:
                lines = wrap(b["hint"], chars)
                prompts = lines[:2]
                if len(lines) > 2:
                    prompts[-1] = prompts[-1].rstrip(" ,;") + " …"
            for k, p in enumerate(prompts[:int((h - 40) // 16)]):
                out.append(f'<text x="{cx + 14:.0f}" y="{y + 48 + 16 * k:.0f}" font-size="11.5" fill="{line}">{esc(p)}</text>')

    if canvas["tail"]:
        n = len(canvas["tail"])
        tw = (W - 2 * M - gap * (n - 1)) / n
        ty = bottom + 16
        for i, t in enumerate(canvas["tail"]):
            tx = M + i * (tw + gap)
            prompt = (t["print"] or wrap(t["hint"], int(tw / 6.4)))[:1]
            out.append(f'<rect x="{tx:.0f}" y="{ty:.0f}" width="{tw:.0f}" height="{tail_h}" rx="8" fill="#F1EFE8" stroke="#888780" stroke-width="1"/>'
                       f'<text x="{tx + 14:.0f}" y="{ty + 24:.0f}" font-size="15" font-weight="700" fill="#444441">{esc(t["name"])}</text>'
                       + "".join(f'<text x="{tx + 14:.0f}" y="{ty + 42:.0f}" font-size="11.5" fill="#5F5E5A">{esc(p)}</text>' for p in prompt))

    ly = H - 38
    hw = round(len(human) * 6.3) + 60
    out.append(f'<rect x="{M}" y="{ly}" width="14" height="14" rx="3" fill="{COL["human"][0]}" stroke="{COL["human"][1]}"/>'
               f'<text x="{M + 20}" y="{ly + 11}" font-size="11.5" fill="#2C2C2A">{esc(human)}</text>'
               f'<rect x="{M + hw}" y="{ly}" width="14" height="14" rx="3" fill="{COL["agent"][0]}" stroke="{COL["agent"][1]}"/>'
               f'<text x="{M + hw + 20}" y="{ly + 11}" font-size="11.5" fill="#2C2C2A">{esc(agent)}</text>')
    if footer:
        out.append(f'<text x="{W - M}" y="{ly + 11}" font-size="10.5" text-anchor="end" fill="#5F5E5A">{esc(footer)}</text>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def find_browser():
    candidates = [os.environ.get("CHROME"), "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    candidates += sorted(str(p) for p in pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))
    for c in candidates:
        if c and (shutil.which(c) or pathlib.Path(c).exists()):
            return shutil.which(c) or c
    return None


def to_pdf(svg_path, pdf_path):
    browser = find_browser()
    if not browser:
        sys.exit("No Chrome or Chromium found for --pdf (set CHROME=/path/to/chrome). The SVG was written.")
    page = ('<!doctype html><meta charset="utf-8"><style>@page{size:297mm 210mm;margin:0}'
            'html,body{margin:0}img{width:297mm;height:210mm;display:block}</style>'
            f'<img src="{svg_path.resolve().as_uri()}">')
    with tempfile.TemporaryDirectory() as tmp:
        wrapper = pathlib.Path(tmp) / "canvas.html"
        wrapper.write_text(page, encoding="utf-8")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--user-data-dir={tmp}/profile", f"--print-to-pdf={pdf_path.resolve()}", wrapper.as_uri()],
                       check=True, capture_output=True, timeout=120)


# ---------------------------------------------------------------- main

def load(source):
    text = source.read_text(encoding="utf-8")
    canvas = parse_canvas(text)
    if not canvas["columns"]:
        sys.exit(f"No blocks found in {source}: expected '## Section' and '### N. Block 👤|🤖' headings.")
    return text, canvas


def build(source, out, decisions_path, watch, lang):
    _, canvas = load(source)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(canvas, parse_decisions(decisions_path), source, watch, lang), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("canvas", type=pathlib.Path)
    p.add_argument("--out", type=pathlib.Path, help="default: build/canvas.html, or build/canvas.svg with --print")
    p.add_argument("--decisions", type=pathlib.Path,
                   help="decision log (default: DECISIONS.md next to the canvas, if it exists)")
    p.add_argument("--watch", action="store_true", help="re-render whenever the canvas or the log changes")
    p.add_argument("--lang", default="en", choices=sorted(LABELS), help="language of the labels the script adds")
    p.add_argument("--print", dest="printable", action="store_true", help="write the blank canvas as A4 SVG")
    p.add_argument("--pdf", type=pathlib.Path, help="with --print: also print the SVG to this PDF")
    p.add_argument("--subtitle", default="", help="with --print: line under the title")
    p.add_argument("--footer", default="", help="with --print: name, version, license, URL at the bottom right")
    a = p.parse_args()

    if a.printable:
        text, canvas = load(a.canvas)
        out = a.out or pathlib.Path("build/canvas.svg")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(svg(canvas, text, a.subtitle, a.footer, a.lang), encoding="utf-8")
        print(f"Wrote {out}", flush=True)
        if a.pdf:
            to_pdf(out, a.pdf)
            print(f"Wrote {a.pdf}", flush=True)
        return

    out = a.out or pathlib.Path("build/canvas.html")
    decisions = a.decisions or a.canvas.with_name("DECISIONS.md")
    build(a.canvas, out, decisions, a.watch, a.lang)
    print(f"Wrote {out}", flush=True)
    if not a.watch:
        return
    print("Watching for changes (Ctrl+C to stop).", flush=True)
    mtimes = lambda: tuple(f.stat().st_mtime if f.exists() else 0 for f in (a.canvas, decisions))
    last = mtimes()
    try:
        while True:
            time.sleep(1)
            if (now := mtimes()) != last:
                last = now
                build(a.canvas, out, decisions, a.watch, a.lang)
                print(f"Updated {out}", flush=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
