#!/usr/bin/env python3
"""Export one unit's quiz from the course's quiz CSV to an import format.

CSV columns: session, type, question, option_a, option_b, option_c[, option_d], correct, explanation

  export_quiz.py quizzes/video-checks.csv --session 2 --format formbricks --out build/
  export_quiz.py quizzes/video-checks.csv --session 2 --format forms --out build/

formbricks: <name>.formbricks.json, a survey body for POST /api/v1/management/surveys.
forms:      <name>.forms.docx (or .md without pandoc) for Microsoft Forms Quick Import,
            plus <name>.answer-key.md for ticking the correct answers after import.
Answers and explanations never go into the participant-facing files.
"""
import argparse
import csv
import json
import pathlib
import shutil
import subprocess
import sys

LETTERS = "abcd"


def load(path, session):
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["session"].strip() == str(session)]
    if not rows:
        sys.exit(f"No questions for session {session} in {path}")
    questions = []
    for r in rows:
        options = [r[f"option_{l}"].strip() for l in LETTERS if r.get(f"option_{l}", "").strip()]
        correct = r["correct"].strip().upper()
        if correct not in "ABCD"[: len(options)]:
            sys.exit(f"Correct answer {correct!r} has no option: {r['question']}")
        questions.append({"question": r["question"].strip(), "options": options,
                          "correct": correct, "explanation": r["explanation"].strip(),
                          "type": r.get("type", "").strip()})
    return questions


def formbricks(questions, name, workspace_id):
    return {
        "workspaceId": workspace_id or "<WORKSPACE_ID>",
        "name": name,
        "type": "link",
        "status": "draft",
        "questions": [
            {
                "id": f"q{i}",
                "type": "multipleChoiceSingle",
                "headline": {"default": q["question"]},
                "required": True,
                "shuffleOption": "none",
                "choices": [{"id": f"q{i}{LETTERS[j]}", "label": {"default": o}}
                            for j, o in enumerate(q["options"])],
            }
            for i, q in enumerate(questions, 1)
        ],
        "endings": [{
            "id": "end",
            "type": "endScreen",
            "headline": {"default": "Thank you!"},
            "subheader": {"default": "We go through the answers together in the session."},
        }],
    }


def forms_markdown(questions, name):
    # Quick Import recognises numbered questions followed by lettered options, one per line.
    # Pandoc needs two spaces after a capital-letter marker ("A.  ") to read it as a list item.
    lines = [f"# {name}", ""]
    for i, q in enumerate(questions, 1):
        lines += [f"{i}. {q['question']}", ""]
        lines += [f"    {'ABCD'[j]}.  {o}" for j, o in enumerate(q["options"])]
        lines.append("")
    return "\n".join(lines)


def answer_key(questions, name):
    lines = [f"# Answer key: {name}", "", "Instructor only. Tick these in Microsoft Forms after Quick Import.", ""]
    for i, q in enumerate(questions, 1):
        lines += [f"{i}. **{q['correct']}**: {q['options']['ABCD'.index(q['correct'])]}",
                  f"   {q['explanation']}", ""]
    return "\n".join(lines)


def count(questions):
    return f"{len(questions)} question" + ("" if len(questions) == 1 else "s")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--session", required=True)
    p.add_argument("--format", choices=["formbricks", "forms"], required=True)
    p.add_argument("--out", default=".")
    p.add_argument("--name", help="quiz title (default: 'Video check, session <n>')")
    p.add_argument("--workspace-id", help="Formbricks workspace (environment) id")
    a = p.parse_args()

    questions = load(a.csv, a.session)
    name = a.name or f"Video check, session {a.session}"
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = f"video-check-session-{a.session}"

    if a.format == "formbricks":
        target = out / f"{stem}.formbricks.json"
        target.write_text(json.dumps(formbricks(questions, name, a.workspace_id), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Written: {target} ({count(questions)}, status draft)")
        print("Create it with your own key (never commit the key):")
        print(f"  curl -X POST https://app.formbricks.com/api/v1/management/surveys \\\n"
              f"    -H \"x-api-key: $FORMBRICKS_API_KEY\" -H 'Content-Type: application/json' \\\n"
              f"    --data @{target}")
        return

    md = forms_markdown(questions, name)
    if shutil.which("pandoc"):
        target = out / f"{stem}.forms.docx"
        subprocess.run(["pandoc", "-f", "markdown", "-o", str(target)], input=md, text=True, check=True)
    else:
        target = out / f"{stem}.forms.md"
        target.write_text(md, encoding="utf-8")
        print("pandoc not found: wrote Markdown; save it as .docx before Quick Import.")
    key = out / f"{stem}.answer-key.md"
    key.write_text(answer_key(questions, name), encoding="utf-8")
    print(f"Written: {target} ({count(questions)}) and {key}")
    print("Microsoft Forms: New quiz > Quick import > upload the .docx, then tick answers from the key.")


if __name__ == "__main__":
    main()
