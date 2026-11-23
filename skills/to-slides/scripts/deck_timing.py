#!/usr/bin/env python3
"""Build a session's timetable from the minutes on its slides, and check it.

For decks stored as files: a claude.ai Slides deck (project/deck.json with the
slide order, project/slides/<id>.html per slide).

The deck is where people edit minutes, so the slides are the timing source
while a deck is being worked on: the first slide of each block says
"… · N minutes" in its kicker (the first element whose class contains
"kicker"); the slides after it, up to the next such slide, belong to that
block. Hidden slides are skipped.

Usage, with a local copy of the deck (the folder that holds project/deck.json):
    deck_timing.py <deck folder> --start 16:00 --length 105 [--write-timing] [--timing-slide timing]

Prints the timetable, the total, and every line of the hidden timing slide
whose minutes or start time disagree. Minutes not given to any block are shown
as a buffer at the end (the timing slide lists it as a row starting "Buffer").
Exit code 1 if the blocks exceed the session or the timing slide disagrees.
With --write-timing the timeline on the hidden timing slide is rewritten from
the kickers (its notes are kept). The timing slide's timeline is a
<div class="timeline"> of rows <p class="time">, <p class="slot">,
<p class="mins">, <p class="actual">.
"""
import argparse
import html
import json
import pathlib
import re
import sys

KICKER = re.compile(r'<p class="[^"]*\bkicker\b[^"]*"[^>]*>(.*?)</p>', re.S)
TITLE = re.compile(r'<h2 class="title"[^>]*>(.*?)</h2>', re.S)
MINUTES = re.compile(r"(\d+)\s*minutes?\b")
TAG = re.compile(r"<[^>]+>")


def text(fragment):
    return html.unescape(TAG.sub("", fragment)).strip()


def clock(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("deck")
    parser.add_argument("--start", default="16:00")
    parser.add_argument("--length", type=int, default=105)
    parser.add_argument("--write-timing", action="store_true")
    parser.add_argument("--timing-slide", default="timing", help="id of the hidden timing slide")
    args = parser.parse_args()

    root = pathlib.Path(args.deck)
    order = json.loads((root / "project/deck.json").read_text())["order"]
    hour, minute = map(int, args.start.split(":"))
    now = hour * 60 + minute

    blocks = []
    for slide_id in order:
        path = root / f"project/slides/{slide_id}.html"
        if not path.exists():
            continue
        source = path.read_text()
        section = source.split(">", 1)[0]
        if re.search(r"\shidden[\s>]", section + ">"):
            continue
        kicker = KICKER.search(source)
        found = MINUTES.search(text(kicker.group(1))) if kicker else None
        title = text(TITLE.search(source).group(1)) if TITLE.search(source) else slide_id
        if found:
            label = text(kicker.group(1)).split("·")[0].strip()
            blocks.append({"start": now, "minutes": int(found.group(1)), "slides": [(slide_id, title)], "label": f"{label}: {title}"})
            now += int(found.group(1))
        elif blocks:
            blocks[-1]["slides"].append((slide_id, title))

    total = sum(b["minutes"] for b in blocks)
    buffer = args.length - total
    if buffer > 0:
        blocks.append({"start": now, "minutes": buffer, "slides": [("buffer", "Buffer")], "label": "Buffer"})
        now += buffer
    for b in blocks:
        first_id, first_title = b["slides"][0]
        others = ", ".join(s for s, _ in b["slides"][1:])
        print(f"{clock(b['start'])}  {b['minutes']:>3} min  {first_title} [{first_id}]" + (f"  + {others}" if others else ""))
    print(f"{clock(now)}  end   blocks {total} min, buffer {max(buffer, 0)} min, session {args.length}")

    failed = total > args.length
    if failed:
        print(f"FAILED: blocks add up to {total} min, session is {args.length}")

    timing = root / f"project/slides/{args.timing_slide}.html"
    if args.write_timing and timing.exists():
        rows = "\n".join(
            f'<p class="time">{clock(b["start"])}</p>\n<p class="slot">{html.escape(b["label"], quote=False)}</p>\n'
            f'<p class="mins">{b["minutes"]} min</p>\n<p class="actual">actual: ____</p>'
            for b in blocks
        )
        rows += f'\n<p class="time">{clock(now)}</p>\n<p class="slot">End</p>\n<p class="mins"></p>\n<p class="actual"></p>'
        source = timing.read_text()
        source = re.sub(r'(<div class="timeline"[^>]*>).*?(</div>)', lambda m: m.group(1) + "\n" + rows + "\n" + m.group(2), source, count=1, flags=re.S)
        timing.write_text(source)
        print(f"wrote the timeline of {timing}")

    timing = root / f"project/slides/{args.timing_slide}.html"
    if timing.exists():
        rows = re.findall(
            r'<p class="time">(.*?)</p>\s*<p class="slot">(.*?)</p>\s*<p class="mins">(.*?)</p>',
            timing.read_text(),
            re.S,
        )
        slide = [(text(t), text(s), text(m)) for t, s, m in rows if text(m)]
        expected = [(clock(b["start"]), f"{b['minutes']} min") for b in blocks]
        if [(t, m) for t, _, m in slide] != expected:
            failed = True
            print("FAILED: the hidden timing slide disagrees with the kickers:")
            for i in range(max(len(slide), len(expected))):
                have = f"{slide[i][0]} {slide[i][2]} ({slide[i][1]})" if i < len(slide) else "—"
                want = f"{expected[i][0]} {expected[i][1]}" if i < len(expected) else "—"
                mark = "  " if i < len(slide) and i < len(expected) and (slide[i][0], slide[i][2]) == expected[i] else "≠ "
                print(f"  {mark}slide: {have:<60} kickers: {want}")

    print("deck timing: " + ("FAILED" if failed else "ok"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
