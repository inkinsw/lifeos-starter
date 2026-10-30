# LifeOS Starter

Set up a personal **life harness**: a folder of plain-text memory that your AI agent reads before it
answers, so it knows who you are, what you value, how you want to be helped, and what has happened in
your life. It works with any agent that reads files (Claude Code, Codex, and others), and the memory is
yours: markdown files in a git repository on your own computer.

This repository is the installer, not your workspace. Your agent reads `SETUP.md`, copies a template into
a folder you choose, interviews you for about 15 minutes, and tests that a fresh session remembers you.

## Before you start

1. **An agent that can edit files on your computer.** A chat website can't do this; you need one of:
   - **Claude Code** (needs a paid Claude plan; the free plan doesn't include it). Install:
     - macOS: `curl -fsSL https://claude.ai/install.sh | bash`
     - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex`
   - **Codex** (OpenAI). Install:
     - macOS: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`
     - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"`
2. **git and Python 3.10+.** Setup checks for both and offers to install whatever is missing.

## Setup: one prompt

Open your agent in any folder and paste:

```text
Set up my LifeOS from this repository:
https://github.com/inkinsw/lifeos-starter

Start with SETUP.md. Use the repository only as setup instructions and a template source; do not turn
its clone into my workspace.
```

It asks before it creates anything, never overwrites a file you already have, and removes its temporary
copy of this repository when it's done.

## What setup does

1. Picks a folder (default: a new `LifeOS` folder in your home directory).
2. Checks for git and Python, and offers to install what's missing.
3. Copies the workspace template.
4. **Interviews you:** who you are, where you're headed, what you value, how you want it to work with you.
5. Creates a page for each life area you pick (health, money, a sport, school, anything).
6. Writes your answers into the contract (`AGENTS.md`) and the self pages.
7. Puts the folder under git (and offers a private GitHub backup).
8. **Runs a recall test:** a brand-new session answers questions about you from the files alone.
9. Tells you how to use it in your first week.

## What you get

```text
LifeOS/
  AGENTS.md        the rules every agent follows (CLAUDE.md just imports it)
  wiki/            your memory
    identity.md    who you are
    values.md      what you live by (grows as you do)
    life.md        durable facts: routines, preferences, standing choices
    goals.md       what you're working toward
    daily/         one note per day: purchases, decisions, questions, captured as they happen
    domains/       one page per life area
    decisions/     each real decision, with its why
    log.md         milestones, newest on top
  private/         sensitive files; git never sees them
  scripts/         note.py (capture), wrap.py (end-of-session check + commit), lint_wiki.py
  prompts/         the recall test, and recipes for building engines (running, health, money, calendar)
  skills/          grill-me, roast, session-handoff
```

## How it works, in four ideas

- **One contract, any agent.** `AGENTS.md` holds every rule. Agents that read `CLAUDE.md` get it through
  an import, so there is never a second copy to drift.
- **Capture now, promote later.** Anything you mention in passing lands in today's daily note at once.
  At the end of a session, facts that will still be true next month move up into the right page.
- **Answers carry receipts.** Anything about the present (a balance, a status, a training number) is
  re-read from its source at the moment you ask, and the answer says where it came from and how old it is.
- **Rules that slip become mechanisms.** When the agent keeps forgetting something, the fix is a script
  or a check, not a sterner sentence. `wrap.py` and the recall test are the first two.

## Credits

The installer flow (a staged setup run by your own agent, missing-files-only copying, approval gates, a
fresh-session check) is adapted from Duke Pan's
[ai-memory-workspace-starter](https://github.com/Fryingpannn/ai-memory-workspace-starter) (MIT). That
starter is built for a workspace of projects; this one adds the life layer (daily capture, identity and
values pages, life areas, receipts, the promotion gradient, a recurring recall test) from the LifeOS it
was built from. The memory pattern itself traces to Andrej Karpathy's
[LLM wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

Skills: `grill-me` is adapted from Matt Pocock's [skills](https://github.com/mattpocock/skills) (MIT).
`roast` and `session-handoff` are adapted from community skills of the same names; versions of both
appear in MIT-licensed collections such as
[Claude_Code_Boilerplate_Framework](https://github.com/Roentek/Claude_Code_Boilerplate_Framework) and
[claude-code-mods](https://github.com/nateherkai/claude-code-mods).

MIT licensed; see `LICENSE`.
