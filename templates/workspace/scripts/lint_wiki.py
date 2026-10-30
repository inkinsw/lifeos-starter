"""lint_wiki.py: the mechanical half of "lint the wiki" (links, reachability, size).

The judgment half (contradictions, stale claims, gaps) stays a read by the agent. This half is cheap and
certain, so it should never depend on someone remembering: wrap.py runs it and warns.

  python scripts/lint_wiki.py          # report; exit 1 if a curated page has an error
  python scripts/lint_wiki.py --all    # also list findings in history (sessions/, daily/, log.md)

Checks:
  broken link   a [[target]] or a markdown link to a local .md file that resolves to nothing
  folder link   a [[target]] that names a folder: link the folder's index page instead
  unreachable   a page no chain of links reaches from wiki/index.md (daily/ is exempt: read by date)
  size          a curated page past SIZE_WARN lines (advice, never an error)

History (sessions/, daily/, log.md) is append-only: its findings never fail the run, because the record
is not rewritten to satisfy a linter. Everything else under wiki/, plus AGENTS.md as a link source, is
curated and must be clean. Links inside `code` and fenced blocks are ignored.

A [[target]] resolves as a path from the wiki root, a path relative to the linking page, or a unique page
name anywhere in the wiki.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIZE_WARN = 400
HISTORY_DIRS = ("sessions", "daily")
HISTORY_FILES = ("log",)
EXEMPT_FROM_REACH = ("daily",)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_FENCE = re.compile(r"^\s*(```|~~~)")
_CODE = re.compile(r"`[^`\n]*`")
_WIKILINK = re.compile(r"\[\[([^\]]{1,200}?)\]\]")
_MDLINK = re.compile(r"\]\(([^)\s]+?\.md)(?:#[^)]*)?\)")


@dataclass(frozen=True)
class Finding:
    kind: str     # "broken link" | "folder link" | "unreachable" | "size"
    page: str     # wiki-relative page id, or "AGENTS.md"
    detail: str
    history: bool  # True: append-only history, reported but never failing


def page_id(path: Path, wiki: Path) -> str:
    return path.relative_to(wiki).with_suffix("").as_posix()


def is_history(pid: str) -> bool:
    return pid.split("/")[0] in HISTORY_DIRS or pid in HISTORY_FILES


def strip_code(text: str) -> str:
    """Blank fenced blocks and inline code spans, keeping the line count."""
    out, fenced = [], False
    for line in text.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else _CODE.sub("", line))
    return "\n".join(out)


def wikilinks(text: str) -> list[str]:
    """Targets of [[target#heading|alias]] links (heading and alias dropped)."""
    out = []
    for raw in _WIKILINK.findall(strip_code(text)):
        target = re.split(r"\\?\|", " ".join(raw.split()), maxsplit=1)[0]
        target = target.partition("#")[0].strip().removesuffix(".md").strip()
        if target:
            out.append(target)
    return out


def mdlinks(text: str) -> list[str]:
    """Local .md targets of [text](path.md) links; web links are skipped."""
    return [t for t in _MDLINK.findall(strip_code(text)) if "://" not in t]


class Wiki:
    def __init__(self, wiki: Path) -> None:
        self.root = wiki
        self.pages: dict[str, Path] = {page_id(p, wiki): p for p in sorted(wiki.rglob("*.md"))
                                       if ".obsidian" not in p.parts}
        self.by_name: dict[str, list[str]] = {}
        for pid in self.pages:
            self.by_name.setdefault(pid.rsplit("/", 1)[-1].lower(), []).append(pid)
        self.lowered = {pid.lower(): pid for pid in self.pages}

    def text(self, pid: str) -> str:
        return self.pages[pid].read_text(encoding="utf-8")

    def resolve(self, target: str, source_dir: str) -> str | None:
        """A page id, "dir:<path>" for a folder, or None."""
        for cand in (target, f"{source_dir}/{target}" if source_dir else target):
            norm = Path(cand).as_posix()
            while norm.startswith("./"):
                norm = norm[2:]
            if norm.lower() in self.lowered:
                return self.lowered[norm.lower()]
            if norm and (self.root / norm).is_dir():
                return f"dir:{norm}"
        named = self.by_name.get(target.rsplit("/", 1)[-1].lower(), [])
        if "/" not in target and len(named) == 1:
            return named[0]
        return None

    def resolve_md(self, target: str, source: Path) -> str | None:
        """A markdown link resolves relative to the file that holds it."""
        dest = (source.parent / target).resolve()
        try:
            return page_id(dest, self.root.resolve())
        except ValueError:
            return "" if dest.exists() else None  # outside the wiki: fine if the file exists


def lint(root: Path = ROOT) -> list[Finding]:
    wiki_dir = root / "wiki"
    w = Wiki(wiki_dir)
    findings: list[Finding] = []
    edges: dict[str, set[str]] = {pid: set() for pid in w.pages}

    sources = [(pid, w.pages[pid]) for pid in w.pages]
    contract = root / "AGENTS.md"
    if contract.is_file():
        sources.append(("AGENTS.md", contract))

    for pid, path in sources:
        text = path.read_text(encoding="utf-8")
        hist = is_history(pid) if pid != "AGENTS.md" else False
        src_dir = pid.rsplit("/", 1)[0] if "/" in pid else ""
        for target in wikilinks(text):
            hit = w.resolve(target, src_dir)
            if hit is None:
                findings.append(Finding("broken link", pid, f"[[{target}]] resolves to nothing", hist))
            elif hit.startswith("dir:"):
                findings.append(Finding("folder link", pid, f"[[{target}]] names a folder: link its "
                                        "index page instead", hist))
            elif pid in edges:
                edges[pid].add(hit)
        for target in mdlinks(text):
            hit = w.resolve_md(target, path)
            if hit is None:
                findings.append(Finding("broken link", pid, f"({target}) resolves to nothing", hist))
            elif hit and hit in w.pages and pid in edges:
                edges[pid].add(hit)
            elif hit and hit not in w.pages:
                findings.append(Finding("broken link", pid, f"({target}) resolves to nothing", hist))

    if "index" in w.pages:
        seen, queue = {"index"}, deque(["index"])
        while queue:
            for nxt in edges.get(queue.popleft(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        for pid in w.pages:
            if pid not in seen and pid.split("/")[0] not in EXEMPT_FROM_REACH:
                findings.append(Finding("unreachable", pid, "no chain of links reaches it from index",
                                        is_history(pid)))

    for pid in w.pages:
        lines = w.text(pid).count("\n") + 1
        if lines > SIZE_WARN and not is_history(pid):
            findings.append(Finding("size", pid, f"{lines} lines (over {SIZE_WARN}): tighten or split?",
                                    False))
    return findings


def errors(findings: list[Finding]) -> list[Finding]:
    """What fails the run: curated broken links, folder links, unreachable pages. Size is advice."""
    return [f for f in findings if not f.history and f.kind != "size"]


def lint_warning(root: Path = ROOT) -> str | None:
    """One wrap-time warning line, or None when curated pages are clean."""
    errs = errors(lint(root))
    if not errs:
        return None
    first = errs[0]
    return (f"wiki lint: {len(errs)} error(s) in curated pages, e.g. {first.page}: {first.detail}. "
            "Run `python scripts/lint_wiki.py`.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lint the wiki: links, reachability, size.")
    ap.add_argument("--all", action="store_true", help="also list findings in append-only history")
    args = ap.parse_args(argv)

    findings = lint()
    errs = errors(findings)
    sizes = [f for f in findings if f.kind == "size"]
    history = [f for f in findings if f.history]

    print("WIKI LINT (mechanical: links, reachability, size)")
    for f in errs:
        print(f"  x {f.kind:<12} {f.page}: {f.detail}")
    for f in sizes:
        print(f"  ~ {f.kind:<12} {f.page}: {f.detail}")
    if args.all:
        for f in history:
            print(f"  . history      {f.page}: {f.kind}: {f.detail}")
    print(f"\n  {len(errs)} error(s) in curated pages, {len(sizes)} size note(s), "
          f"{len(history)} in append-only history{'' if args.all else ' (--all to list)'}")
    print('  The judgment half (contradictions, stale claims) is still a read: "lint the wiki".')
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
