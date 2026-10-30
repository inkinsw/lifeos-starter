"""Tests for the workspace template and its scripts. Standard library only.

  python -m unittest discover -s tests -v

Each test copies templates/workspace/ into a temporary folder, so it exercises exactly what setup copies.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "templates" / "workspace"
TODAY = "2026-11-02"


def load(script: str, root: Path):
    """Import a workspace script from a copied workspace, so ROOT points at the copy."""
    path = root / "scripts" / f"{script}.py"
    name = f"{script}_{id(root)}"
    sys.path.insert(0, str(root / "scripts"))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod  # dataclasses look their module up here
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(str(root / "scripts"))
        sys.modules.pop("lint_wiki", None)  # wrap.py imports it by name; the next copy needs its own
    return mod


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)


class Workspace(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "LifeOS"
        shutil.copytree(TEMPLATE, self.root)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def init_git(self) -> None:
        git(self.root, "init", "-q", "-b", "main")
        git(self.root, "config", "user.email", "test@example.com")
        git(self.root, "config", "user.name", "Test")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-q", "-m", "setup")


class TestNote(Workspace):
    def test_creates_note_with_header_then_appends(self):
        note = load("note", self.root)
        now = datetime(2026, 11, 2, 9, 5)
        path = note.append_daily("bought shoes, 120", root=self.root, now=now)
        note.append_daily("take the summer job?", kind="question", root=self.root, now=now)
        note.append_daily("yes, it pays for the trip", kind="answer", root=self.root, now=now)
        self.assertEqual(path, self.root / "wiki" / "daily" / "2026-11-02.md")
        text = path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Daily: 2026-11-02"))
        self.assertIn("- 09:05 - bought shoes, 120\n", text)
        self.assertIn("- 09:05 - Q: take the summer job?\n", text)
        self.assertIn("- 09:05 - A: yes, it pays for the trip\n", text)
        self.assertEqual(text.count("# Daily"), 1)

    def test_rejects_empty_note(self):
        note = load("note", self.root)
        with self.assertRaises(ValueError):
            note.append_daily("   ", root=self.root)

    def test_collapses_newlines_to_one_line(self):
        note = load("note", self.root)
        path = note.append_daily("line one\nline two", root=self.root, now=datetime(2026, 11, 2, 10, 0))
        self.assertIn("- 10:00 - line one line two\n", path.read_text(encoding="utf-8"))


class TestLint(Workspace):
    def errors(self):
        lint = load("lint_wiki", self.root)
        return lint.errors(lint.lint(self.root))

    def test_fresh_template_is_clean(self):
        self.assertEqual(self.errors(), [])

    def test_broken_link_is_an_error(self):
        self.write("wiki/life.md", (self.root / "wiki/life.md").read_text(encoding="utf-8")
                   + "\nSee [[nowhere]].\n")
        errs = self.errors()
        self.assertEqual([(e.kind, e.page) for e in errs], [("broken link", "life")])

    def test_unreachable_page_is_an_error(self):
        self.write("wiki/domains/running.md", "# Running\n")
        errs = self.errors()
        self.assertEqual([(e.kind, e.page) for e in errs], [("unreachable", "domains/running")])

    def test_linking_from_the_domain_index_makes_it_reachable(self):
        self.write("wiki/domains/running.md", "# Running\n")
        idx = self.root / "wiki/domains/index.md"
        idx.write_text(idx.read_text(encoding="utf-8") + "- [[domains/running]]: runs\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_folder_link_is_an_error(self):
        self.write("wiki/goals.md", "# Goals\nSee [[domains]].\n")
        self.assertIn("folder link", [e.kind for e in self.errors()])

    def test_links_in_code_are_ignored(self):
        self.write("wiki/goals.md", "# Goals\n`[[nowhere]]`\n```\n[[also-nowhere]]\n```\n")
        self.assertEqual(self.errors(), [])

    def test_daily_notes_are_exempt_from_reachability(self):
        self.write("wiki/daily/2026-11-02.md", "# Daily\n- 09:00 - note\n")
        self.assertEqual(self.errors(), [])

    def test_broken_link_in_history_never_fails(self):
        self.write("wiki/sessions/2026-11-02.md", "# Session\n- see [[gone]]\n")
        cat = self.root / "wiki/session-catalog.md"
        cat.write_text(cat.read_text(encoding="utf-8") + "- [[sessions/2026-11-02]] - x\n", encoding="utf-8")
        self.assertEqual(self.errors(), [])

    def test_markdown_link_to_missing_page_is_an_error(self):
        self.write("wiki/goals.md", "# Goals\nSee [life](missing.md).\n")
        self.assertIn("broken link", [e.kind for e in self.errors()])


class TestWrap(Workspace):
    def run_wrap(self, *argv: str) -> int:
        wrap = load("wrap", self.root)
        return wrap.main(list(argv) + ["--no-push"], root=self.root, today=TODAY)

    def fill_session(self) -> None:
        self.write(f"wiki/sessions/{TODAY}.md",
                   f"# Session: {TODAY}\n\n## What changed\n- set up the life areas page today\n")
        cat = self.root / "wiki/session-catalog.md"
        cat.write_text(cat.read_text(encoding="utf-8") + f"- [[sessions/{TODAY}]] - setup\n",
                       encoding="utf-8")

    def last_commit_files(self) -> list[str]:
        return git(self.root, "show", "--name-only", "--format=", "HEAD").stdout.split()

    def test_scaffolds_then_blocks_until_filled(self):
        self.init_git()
        self.assertEqual(self.run_wrap(), 1)
        self.assertTrue((self.root / f"wiki/sessions/{TODAY}.md").exists())
        self.assertEqual(git(self.root, "log", "--oneline").stdout.count("\n"), 1)

    def test_blocks_without_catalog_link(self):
        self.init_git()
        self.write(f"wiki/sessions/{TODAY}.md", "# S\n- a real line with enough words\n")
        self.assertEqual(self.run_wrap(), 1)

    def test_commits_by_path_and_leaves_other_work(self):
        self.init_git()
        self.fill_session()
        self.write(f"wiki/daily/{TODAY}.md", "# Daily\n- 09:00 - bought shoes\n")
        self.write("wiki/life.md", "# Life\nchanged\n")            # this session's, named with --paths
        self.write("wiki/goals.md", "# Goals\nanother session\n")  # not named: must stay unstaged
        self.assertEqual(self.run_wrap("--paths", "wiki/life.md"), 0)
        files = self.last_commit_files()
        self.assertIn(f"wiki/sessions/{TODAY}.md", files)
        self.assertIn("wiki/session-catalog.md", files)
        self.assertIn(f"wiki/daily/{TODAY}.md", files)
        self.assertIn("wiki/life.md", files)
        self.assertNotIn("wiki/goals.md", files)
        self.assertIn("wiki/goals.md", git(self.root, "status", "--short").stdout)

    def test_tracked_private_file_blocks(self):
        self.init_git()
        self.fill_session()
        self.write("private/labs.md", "secret")
        git(self.root, "add", "-f", "private/labs.md")
        git(self.root, "commit", "-q", "-m", "oops")
        self.assertEqual(self.run_wrap(), 1)

    def test_claude_md_without_import_blocks(self):
        self.init_git()
        self.fill_session()
        self.write("CLAUDE.md", "Rules live here now.\n")
        self.assertEqual(self.run_wrap(), 1)

    def test_private_folder_is_ignored_by_git(self):
        self.init_git()
        self.write("private/statement.csv", "1,2,3")
        self.write(".env", "KEY=1")
        status = git(self.root, "status", "--short", "--untracked-files=all").stdout
        self.assertNotIn("private/statement.csv", status)
        self.assertNotIn(".env", status)
        self.assertIn("private/README.md", git(self.root, "ls-files").stdout)

    def test_dry_run_commits_nothing(self):
        self.init_git()
        self.fill_session()
        self.assertEqual(self.run_wrap("--dry-run"), 0)
        self.assertEqual(git(self.root, "log", "--oneline").stdout.count("\n"), 1)


class TestTemplate(unittest.TestCase):
    """The template's promises about itself."""

    def test_claude_md_imports_agents_md(self):
        self.assertIn("@AGENTS.md", (TEMPLATE / "CLAUDE.md").read_text(encoding="utf-8"))

    def test_placeholders_only_where_setup_fills_them(self):
        allowed = {"AGENTS.md", "wiki/identity.md", "wiki/values.md", "wiki/goals.md"}
        found = {p.relative_to(TEMPLATE).as_posix() for p in TEMPLATE.rglob("*.md")
                 if "{{FILL" in p.read_text(encoding="utf-8")}
        self.assertEqual(found, allowed)

    def test_contract_and_wiki_are_harness_neutral(self):
        pages = [TEMPLATE / "AGENTS.md", *(TEMPLATE / "wiki").rglob("*.md"), *(TEMPLATE / "prompts").rglob("*.md")]
        for p in pages:
            text = p.read_text(encoding="utf-8")
            for name in ("Claude", "Codex", "ChatGPT", "Cursor"):
                self.assertNotIn(name, text, f"{p.relative_to(TEMPLATE)} names a product: {name}")

    def test_repo_map_names_files_that_exist(self):
        text = (TEMPLATE / "AGENTS.md").read_text(encoding="utf-8")
        for rel in ("scripts/note.py", "scripts/wrap.py", "scripts/lint_wiki.py", "prompts/recall-test.md",
                    "wiki/storage-policy.md", "wiki/index.md", "skills/README.md"):
            self.assertIn(rel.split("/")[-1], text)
            self.assertTrue((TEMPLATE / rel).exists(), rel)

    def test_every_routed_stage_exists(self):
        setup = (REPO / "SETUP.md").read_text(encoding="utf-8")
        stages = re.findall(r"`(prompts/setup/[\w-]+\.md)`", setup)
        self.assertEqual(len(stages), 9)
        for s in stages:
            self.assertTrue((REPO / s).exists(), s)

    def test_every_recipe_named_in_setup_exists(self):
        for name in ("running", "health", "money", "calendar"):
            self.assertTrue((TEMPLATE / "prompts" / "recipes" / f"{name}.md").exists(), name)

    def test_skills_ship(self):
        for name in ("grill-me", "roast", "session-handoff"):
            self.assertTrue((TEMPLATE / "skills" / name / "SKILL.md").exists(), name)


if __name__ == "__main__":
    unittest.main()
