# {{FILL: workspace title, e.g. "Alex's LifeOS"}}

> **The canonical agent contract. Any harness works this folder.** `CLAUDE.md` is a one-line pointer
> here. When a rule changes, edit this file, never a harness's private memory. Write everything here
> harness-neutral: say *the agent* / *the harness*, never a product name.

## What this is

This folder is my personal life harness: the place my AI reads before it answers, so it knows who I am,
what I value, how I want to be helped, and what has happened in my life. It holds:

- **Memory:** a plain-markdown `wiki/` (who I am, what I value, life facts, decisions, a log) plus
  `wiki/daily/`, where everyday life gets captured as it happens.
- **Life areas:** one page per area I care about, in `wiki/domains/`. An area can grow an *engine* later
  (a script plus data the agent reads, like running numbers from Strava) by following `prompts/recipes/`.
- **Projects:** one folder per effort under `projects/`.

**Use the memory before answering** anything about my plans, money, health, training, goals, or how I
work.

## Disciplines (non-negotiable)

- **Facts vs advice, kept separate.** A number from a source is a fact; what to do about it is advice.
  Say which is which.
- **Plain text.** Everything that matters is a markdown file in this folder, versioned with git.
- **Secrets never committed.** Passwords, API keys, tokens, account numbers: never in a tracked file.
  `.env` and `private/` are gitignored.
- **Convert discipline into mechanism.** When a rule here keeps slipping, don't just restate it. Turn it
  into a script, a check, or a template that enforces it, and log why. Anything left to willpower decays.

## Memory Routing (reads)

Full rules: `wiki/storage-policy.md`. At the START of every session:

1. If this folder has a git remote and the tree is clean, pull first (`git pull --ff-only`).
2. Read `wiki/index.md`, the past week of `wiki/log.md` (newest on top), and the newest note in
   `wiki/sessions/` (by filename).
3. Read **today's and yesterday's** `wiki/daily/` note if present. Not older ones: a stale note must
   never read as current. Re-read today's note when the date rolls mid-session, and before answering
   anything it may already have closed (another session may have written it).
4. **The index is a router, not the payload.** Open ONLY the pages the task needs. Don't load the whole
   wiki.
5. Working inside a project: also read `projects/<name>/` (its `README.md` and `wiki/`). Not other
   projects.
6. Tell me which pages you used.

## Memory Write-back (writes)

At the END of a session that meaningfully changed something (a plan, a decision, a page, the setup), when
I say "wrap":

1. Write 2 to 5 lines in today's session note, `wiki/sessions/YYYY-MM-DD.md`, and link it from
   `wiki/session-catalog.md` (newest on top).
2. **Promote** durable facts up the gradient in `wiki/storage-policy.md`: a fact that will still be true
   next month moves out of `daily/` into the page where it belongs. A change that matters across the whole
   wiki also gets one line in `wiki/log.md`.
3. Confirm today's purchases, decisions, and Q&A actually landed in `wiki/daily/`.
4. Run `python scripts/wrap.py --paths <every other file you changed>`. It checks the write-back, then
   commits by path (and pushes if there is a remote).

After changing this file, `wiki/index.md`, or `wiki/storage-policy.md`, rerun the recall test
(`prompts/recall-test.md`): a fresh session should still know me.

**"Lint the wiki":** run `python scripts/lint_wiki.py` first (broken links, pages unreachable from the
index), then read for contradictions, stale claims, and gaps, and FLAG them. Don't silently fix.

## Daily Capture

When I mention a **purchase, decision, or question about my life**, capture it to today's
`wiki/daily/YYYY-MM-DD.md` with `python scripts/note.py "..."`, the moment it comes up, not at wrap.
After answering a life question, write the pair (`note.py -q "the question"`, then `note.py -a "the
answer"`) so the answer is findable later instead of an orphan question. If Python is unavailable,
append the same line by hand.

## Present-State Answers (receipts)

Any answer about the **present** (a balance, whether something is done or bought, a status, a count, a
health or training number) comes from its source **re-read at the moment of answering**, not from what
is already loaded. Sessions cross midnight, and other sessions write the same files.

1. **Re-read, don't recall.**
2. **Answer first, then one short receipt line:** source + as-of, e.g. *(daily/2026-11-02 14:10:
   ordered, arrives Friday)*.
3. **The record describes the file, not the world.** An open reminder means "not closed in the record",
   never "not done". Say it that way and ask.
4. **No source, or a stale one:** give the last-known value with its date, labelled STALE. Never present
   a remembered number as current.

## Working With Me (standing rules)

The one home for how to work with me. Every harness reads this file; if a harness's own memory disagrees,
this section wins. When I correct how you work, propose a rule for this section.

{{FILL: rules from the setup interview, one bullet each, in the user's words where possible. The shape:
- **Choices:** lay out the realistic options with tradeoffs and mark the one you recommend.
- **Voice:** short and direct, no filler.
- **Teach:** explain concepts I may not know yet.}}

## Repo Map

- `wiki/` is the memory. `index.md` (router), `storage-policy.md` (how memory is read and written),
  `SCHEMA.md` (page roles), `log.md` (milestones, newest on top), `identity.md`, `values.md`, `life.md`,
  `goals.md`, `reminders.md`, `decisions/`, `domains/`, `daily/` (life capture), `sessions/` (session
  notes, listed in `session-catalog.md`), `raw/` (unchanged sources), `inbox.md` (not yet verified).
- `projects/` holds one folder per project; `projects/index.md` lists them.
- `private/` holds sensitive originals (health records, statements, anything about other people).
  Gitignored. The wiki keeps a one-line pointer, never the content.
- `scripts/`: `note.py` (daily capture), `wrap.py` (end-of-session check and commit), `lint_wiki.py`
  (links and reachability).
- `prompts/`: `recall-test.md` (does a fresh session still know me?), `recipes/` (build an engine for a
  life area).
- `skills/`: reusable procedures (`grill-me`, `roast`, `session-handoff`); see `skills/README.md`.
