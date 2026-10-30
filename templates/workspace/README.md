# My LifeOS

A personal life harness: a folder of plain-text memory that any AI agent reads before it answers, so it
knows who I am, what I value, how I want to be helped, and what has happened in my life.

## Daily use

Just talk to the agent in this folder. It reads `AGENTS.md` (the rules) and `wiki/index.md` (the memory)
at the start of every session.

- **Mention life as it happens.** "Bought new running shoes for 120." "Decided to drop the 8 AM class."
  "Should I take the summer job?" The agent captures each one to today's `wiki/daily/` note.
- **Ask about your life.** It answers from the record and says where the answer came from.
- **Say "wrap"** at the end of a session that changed something. The agent writes a session note,
  promotes what will still matter next month, and runs `scripts/wrap.py` to commit it.
- **Correct it.** When it works with you the wrong way, say so; it proposes a rule for the Working With
  Me section of `AGENTS.md`, and every future session follows it.

## Commands

```text
python scripts/note.py "something to remember"
python scripts/wrap.py
python scripts/lint_wiki.py
```

## Grow it

- **A life area deserves real numbers?** Follow a recipe in `prompts/recipes/` (running, health, money,
  calendar) to build an engine for it.
- **Changed the rules or the index?** Rerun `prompts/recall-test.md`.
- **Want a project remembered?** Add a folder under `projects/` and a row in `projects/index.md`.

## Privacy

`private/` and `.env` are gitignored. Keep this repository private if you push it anywhere.
