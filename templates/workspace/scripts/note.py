"""note.py: frictionless daily capture (wiki/daily/YYYY-MM-DD.md).

Appends a timestamped line to today's daily note, creating the note on first write. Append-anytime: not
gated on a session wrap. The agent runs this the moment you mention a purchase, decision, or question
(AGENTS.md -> Daily Capture), and writes the answer as a paired line after answering a life question.

  python scripts/note.py "bought running shoes, 120"
  python scripts/note.py -q "should I switch to the 8 AM class?"
  python scripts/note.py -a "yes: it frees Thursday evenings for practice"

Where a fact goes (daily note vs. a curated page): wiki/storage-policy.md.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def daily_path(root: Path, day: date) -> Path:
    return root / "wiki" / "daily" / f"{day.isoformat()}.md"


def header(day: date) -> str:
    return (
        f"# Daily: {day.isoformat()}\n\n"
        "Append-anytime life log: purchases, decisions, questions (with answers), quick notes.\n"
        "Where facts go next: wiki/storage-policy.md.\n\n"
    )


def append_daily(
    text: str,
    *,
    kind: str = "note",
    root: Path = ROOT,
    now: datetime | None = None,
) -> Path:
    """Append one timestamped bullet to today's daily note; create the note (with header) if absent.

    kind: "note" (plain), "question" (prefix "Q: "), or "answer" (prefix "A: ").
    """
    text = " ".join(text.split())
    if not text:
        raise ValueError("nothing to capture: the note is empty")
    moment = now or datetime.now()
    path = daily_path(root, moment.date())
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(header(moment.date()), encoding="utf-8")
    prefix = {"note": "", "question": "Q: ", "answer": "A: "}[kind]
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"- {moment:%H:%M} - {prefix}{text}\n")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Append a line to today's wiki/daily note.")
    ap.add_argument("text", help="what to capture")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("-q", "--question", action="store_true", help="a question (prefix 'Q:')")
    group.add_argument("-a", "--answer", action="store_true", help="the answer to the last question ('A:')")
    args = ap.parse_args(argv)
    kind = "question" if args.question else "answer" if args.answer else "note"
    try:
        path = append_daily(args.text, kind=kind)
    except ValueError as e:
        print(f"note: {e}")
        return 1
    print(f"note: appended to {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
