#!/usr/bin/env python3
"""Export one unit's quiz from the course's quiz CSV to an import format.

CSV columns: session, type, question, option_a, option_b, option_c[, option_d], correct, explanation

Closing CSV (optional, --closing): questions every quiz ends with, such as feedback on the week.
Columns: question, options (separated by " | "; empty = open text). No correct answer.

  export_quiz.py quizzes/video-checks.csv --session 2 --format formbricks --out build/
  export_quiz.py quizzes/video-checks.csv --session 2 --format forms --out build/ \\
      --name "Session 2 · Data import and visualization" --description "Video check" \\
      --closing quizzes/closing-questions.csv

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
MARKS = "ABCDEFGHIJ"


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


def load_closing(path):
    # Questions without a correct answer: a choice question, or open text when it has no options.
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    questions = []
    for r in rows:
        options = [o.strip() for o in r.get("options", "").split("|") if o.strip()]
        if len(options) > len(MARKS):
            sys.exit(f"More than {len(MARKS)} options: {r['question']}")
        questions.append({"question": r["question"].strip(), "options": options,
                          "correct": "", "explanation": "", "type": "closing"})
    return questions


def formbricks(questions, name, description, workspace_id):
    def question(i, q):
        if not q["options"]:
            return {"id": f"q{i}", "type": "openText", "inputType": "text",
                    "headline": {"default": q["question"]}, "required": False}
        return {"id": f"q{i}", "type": "multipleChoiceSingle",
                "headline": {"default": q["question"]}, "required": True, "shuffleOption": "none",
                "choices": [{"id": f"q{i}{j}", "label": {"default": o}}
                            for j, o in enumerate(q["options"])]}

    survey = {
        "workspaceId": workspace_id or "<WORKSPACE_ID>",
        "name": name,
        "type": "link",
        "status": "draft",
        "questions": [question(i, q) for i, q in enumerate(questions, 1)],
        "endings": [{
            "id": "end",
            "type": "endScreen",
            "headline": {"default": "Thank you!"},
            "subheader": {"default": "We go through the answers together in the session."},
        }],
    }
    if description:
        survey["welcomeCard"] = {"enabled": True, "headline": {"default": name},
                                 "html": {"default": description}}
    return survey


def forms_markdown(questions, name, description):
    # Quick Import takes the first line as the title and the next paragraph as the description,
    # then numbered questions followed by lettered options, one per line; a question without
    # options becomes a text question.
    # Pandoc needs two spaces after a capital-letter marker ("A.  ") to read it as a list item.
    lines = [f"# {name}", ""]
    if description:
        lines += [description, ""]
    for i, q in enumerate(questions, 1):
        lines += [f"{i}. {q['question']}", ""]
        if q["options"]:
            lines += [f"    {MARKS[j]}.  {o}" for j, o in enumerate(q["options"])]
            lines.append("")
    return "\n".join(lines)


def answer_key(questions, name):
    lines = [f"# Answer key: {name}", "", "Instructor only. Tick these in Microsoft Forms after Quick Import.", ""]
    for i, q in enumerate(questions, 1):
        if not q["correct"]:
            kind = "choice" if q["options"] else "text"
            lines += [f"{i}. No correct answer ({kind} question, closing).", ""]
            continue
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
    p.add_argument("--description", help="text under the title")
    p.add_argument("--closing", help="CSV of questions every quiz ends with (question, options)")
    p.add_argument("--workspace-id", help="Formbricks workspace (environment) id")
    a = p.parse_args()

    questions = load(a.csv, a.session)
    if a.closing:
        questions += load_closing(a.closing)
    name = a.name or f"Video check, session {a.session}"
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stem = f"video-check-session-{a.session}"

    if a.format == "formbricks":
        target = out / f"{stem}.formbricks.json"
        target.write_text(json.dumps(formbricks(questions, name, a.description, a.workspace_id),
                                     indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Written: {target} ({count(questions)}, status draft)")
        print("Create it with your own key (never commit the key):")
        print(f"  curl -X POST https://app.formbricks.com/api/v1/management/surveys \\\n"
              f"    -H \"x-api-key: $FORMBRICKS_API_KEY\" -H 'Content-Type: application/json' \\\n"
              f"    --data @{target}")
        return

    md = forms_markdown(questions, name, a.description)
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
    if any(not q["correct"] for q in questions):
        print("Closing questions have no correct answer; set 'Required' in Forms where you want it.")


if __name__ == "__main__":
    main()
