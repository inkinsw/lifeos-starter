"""wrap.py: end a working session. Check the write-back, then commit by path (and push).

What to write and which facts to promote is the agent's judgment (AGENTS.md -> Memory Write-back), done
BEFORE running this. This script is the mechanism that keeps the habit from decaying: it scaffolds today's
session note if missing, checks the steps were actually done, then does the git plumbing the same way
every time.

  python scripts/wrap.py                          # check, commit, push (if a remote exists)
  python scripts/wrap.py --paths wiki/life.md     # also commit other files this session changed
  python scripts/wrap.py --dry-run                # check only
  python scripts/wrap.py --no-push                # commit, don't push

Blocking checks (fix them, or --force):
  - wiki/sessions/<today>.md exists and has a real line in it (not just the scaffold)
  - wiki/session-catalog.md links today's session note
  - CLAUDE.md still imports AGENTS.md (one contract, not two)
  - nothing under private/ is tracked by git

Warnings (never block):
  - wiki/log.md: today's line missing (fine unless the change matters across the wiki), dates out of
    newest-on-top order, or today's entry too long
  - unfilled {{FILL: ...}} placeholders left in AGENTS.md or the self pages
  - wiki lint errors (broken links, unreachable pages)

Staging is BY PATH: today's session note, the log, the catalog, today's and yesterday's daily notes, and
anything named with --paths. Everything else is left unstaged and listed, because another session may be
working in the same folder. --all stages everything, for a tree that holds only this session's work.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lint_wiki  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCAFFOLD = """# Session: {today}

## What changed
- <fill me in>

## Decisions
- <fill me in>

## Next
- <fill me in>
"""
PLACEHOLDER = "{{FILL"
SELF_PAGES = ("AGENTS.md", "wiki/identity.md", "wiki/values.md", "wiki/goals.md")
LOG_ENTRY_MAX = 400
_DATE_LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2})\b")
_BULLET = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*)$")


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


def is_substantive(text: str) -> bool:
    """A real note has at least one filled bullet: four or more words, no placeholder."""
    for line in text.splitlines():
        m = _BULLET.match(line)
        if m and "<fill me in>" not in m.group(1) and len(m.group(1).split()) >= 4:
            return True
    return False


def log_dates(text: str) -> list[str]:
    return [m.group(1) for line in text.splitlines() if (m := _DATE_LINE.match(line))]


def entry_lengths(text: str, day: str) -> list[int]:
    """Length of each log entry dated `day`, counting its indented continuation lines."""
    out: list[int] = []
    current: int | None = None
    for ln in text.splitlines():
        if ln.startswith("- "):
            if current is not None:
                out.append(current)
            current = len(ln) if ln.startswith(f"- {day}") else None
        elif current is not None and ln.startswith("  "):
            current += len(ln.strip()) + 1
        elif current is not None:
            out.append(current)
            current = None
    if current is not None:
        out.append(current)
    return out


def validate(root: Path, today: str, scaffolded: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warns: list[str] = []
    wiki = root / "wiki"

    session = wiki / "sessions" / f"{today}.md"
    if scaffolded:
        errors.append(f"scaffolded wiki/sessions/{today}.md: fill it in, then run wrap again.")
    elif not session.exists():
        errors.append(f"no session note: wiki/sessions/{today}.md (write it first).")
    elif not is_substantive(session.read_text(encoding="utf-8")):
        errors.append(f"wiki/sessions/{today}.md is still an empty stub: add what changed.")

    catalog = wiki / "session-catalog.md"
    if catalog.exists() and f"sessions/{today}" not in catalog.read_text(encoding="utf-8"):
        errors.append(f"wiki/session-catalog.md doesn't link sessions/{today} (add it, newest on top).")

    claude = root / "CLAUDE.md"
    if claude.exists() and "@AGENTS.md" not in claude.read_text(encoding="utf-8"):
        errors.append("CLAUDE.md no longer imports AGENTS.md: keep it as the one-line @AGENTS.md import "
                      "and put rules in AGENTS.md.")

    tracked_private = [p for p in git(root, "ls-files", "private").stdout.split()
                       if p != "private/README.md"]
    if tracked_private:
        errors.append(f"private/ files are tracked by git ({', '.join(tracked_private[:3])}): run "
                      "`git rm --cached <file>`; private/ must never reach a remote.")

    log = wiki / "log.md"
    if log.exists():
        text = log.read_text(encoding="utf-8")
        dates = log_dates(text)
        if today not in dates:
            warns.append(f"wiki/log.md has no line dated {today}: fine unless this session made a change "
                         "that matters across the wiki (then add one, newest on top).")
        elif dates[0] != today:
            warns.append(f"wiki/log.md's top line is {dates[0]}, not today: newest goes on top.")
        if dates != sorted(dates, reverse=True):
            warns.append("wiki/log.md dates aren't in newest-on-top order.")
        longest = max(entry_lengths(text, today), default=0)
        if longest > LOG_ENTRY_MAX:
            warns.append(f"wiki/log.md: today's entry is {longest} characters (max {LOG_ENTRY_MAX}). "
                         "Keep one line; move detail into the session note.")

    unfilled = [p for p in SELF_PAGES if (root / p).exists()
                and PLACEHOLDER in (root / p).read_text(encoding="utf-8")]
    if unfilled:
        warns.append(f"unfilled {{{{FILL}}}} placeholders in: {', '.join(unfilled)}.")

    try:
        msg = lint_wiki.lint_warning(root)
    except Exception as exc:  # noqa: BLE001  a broken lint must never break a wrap
        msg = f"wiki lint could not run ({exc.__class__.__name__}: {exc})"
    if msg:
        warns.append(msg)
    return errors, warns


def default_stage_paths(root: Path, today: str) -> list[str]:
    """What a wrap commits without --paths: the write-back it checked plus the daily lane."""
    yesterday = (date.fromisoformat(today) - timedelta(days=1)).isoformat()
    wiki = root / "wiki"
    cands = [wiki / "sessions" / f"{today}.md", wiki / "log.md", wiki / "session-catalog.md",
             wiki / "daily" / f"{today}.md", wiki / "daily" / f"{yesterday}.md"]
    return [c.relative_to(root).as_posix() for c in cands if c.exists()]


def unstaged_paths(root: Path) -> list[str]:
    changed = git(root, "diff", "--name-only").stdout.split()
    untracked = git(root, "ls-files", "--others", "--exclude-standard").stdout.split()
    return sorted(set(changed) | set(untracked))


def main(argv: list[str] | None = None, root: Path = ROOT, today: str | None = None) -> int:
    ap = argparse.ArgumentParser(description="Wrap the session: check the write-back, commit, push.")
    ap.add_argument("--message", default=None, help="commit message (default: 'Session wrap <today>')")
    ap.add_argument("--paths", nargs="+", default=[], metavar="PATH",
                    help="also commit these files (everything else this session changed)")
    ap.add_argument("--all", action="store_true", help="stage the whole tree (only when it is all yours)")
    ap.add_argument("--no-push", action="store_true", help="commit but don't push")
    ap.add_argument("--dry-run", action="store_true", help="check only; no scaffold, commit, or push")
    ap.add_argument("--force", action="store_true", help="commit even if blocking checks fail")
    args = ap.parse_args(argv)
    today = today or date.today().isoformat()

    session = root / "wiki" / "sessions" / f"{today}.md"
    scaffolded = False
    if not session.exists() and not args.dry_run:
        session.parent.mkdir(parents=True, exist_ok=True)
        session.write_text(SCAFFOLD.format(today=today), encoding="utf-8", newline="\n")
        scaffolded = True
        print(f"scaffolded wiki/sessions/{today}.md")

    errors, warns = validate(root, today, scaffolded)
    for w in warns:
        print(f"  ! {w}")
    for e in errors:
        print(f"  x {e}")

    if git(root, "rev-parse", "--git-dir").returncode != 0:
        print("not a git repository yet: run `git init -b main` first. Nothing committed.")
        return 1

    stage = default_stage_paths(root, today) + list(args.paths)
    if args.dry_run:
        print(f"  would commit: {'everything (--all)' if args.all else ', '.join(stage) or '(nothing)'}")
        print(f"\ndry run: {len(errors)} blocking, {len(warns)} warning(s). Nothing committed.")
        return 1 if errors else 0
    if errors and not args.force:
        print(f"\nwrap blocked: {len(errors)} check(s) failed. Fix them (or --force). Nothing committed.")
        return 1

    if args.all:
        git(root, "add", "-A")
    elif stage:
        r = git(root, "add", "-A", "--", *stage)
        if r.returncode:
            print(f"wrap blocked: could not stage {stage}:\n{r.stderr.strip()}")
            return 1
    left = [] if args.all else unstaged_paths(root)
    if left:
        print(f"  ! left unstaged ({len(left)}): {', '.join(left[:8])}{' ...' if len(left) > 8 else ''}. "
              "Name your own files with --paths.")

    if git(root, "diff", "--cached", "--quiet").returncode == 0:
        print("nothing to commit.")
    else:
        msg = args.message or f"Session wrap {today}"
        r = git(root, "commit", "-m", msg)
        if r.returncode:
            print(f"commit failed:\n{r.stderr.strip() or r.stdout.strip()}")
            return 1
        print(f"committed: {msg}")

    if args.no_push:
        print("--no-push: skipped push.")
        return 0
    if not git(root, "remote").stdout.strip():
        print("no git remote: committed locally only (add a private remote to back it up).")
        return 0
    if not left:
        r = git(root, "pull", "--rebase")
        if r.returncode:
            print("pull --rebase failed, so nothing was pushed. The commit is saved locally.\n"
                  f"{(r.stderr or r.stdout).strip()}")
            return 1
    r = git(root, "push")
    if r.returncode:
        print(f"push failed (the commit is saved locally):\n{r.stderr.strip()}")
        return 1
    print("pushed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
