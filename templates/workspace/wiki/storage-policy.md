# Storage Policy: the routing contract

**This page owns the behavior of memory: how it is READ (routing) and how it is WRITTEN (promotion).**
`AGENTS.md` summarizes it and points here. [[SCHEMA]] owns the complementary concern, the *shape* of a
page (roles, filenames, links). No overlap.

## Where memory lives

- **The wiki** (`wiki/`): who I am, what I value, life facts, decisions, the log. Always available; kept
  thin enough that the start-of-session read stays small.
- **Projects** (`projects/<name>/`): one folder per effort, loaded only when working in it.
- **`private/`**: sensitive originals (health records, statements, anything about other people).
  Gitignored, so it never reaches a git remote. The wiki keeps a one-line pointer to a private file so
  the agent knows it exists, never the content.
- **A harness's own memory** (some agents keep a private cache): pointers and the story behind a rule at
  most. **Never the rule itself**: rules live in `AGENTS.md` → Working With Me, because a cache reaches
  only the harness that wrote it. If the cache and the wiki disagree, the wiki wins.

## Reads: start of every session

The steps are in `AGENTS.md` → Memory Routing. The reasons behind them:

- **Read today's and yesterday's daily note only**, never "the most recent few regardless of age": a note
  from three weeks ago must not read as current.
- **"Start of session" is not a timestamp.** Sessions run past midnight and run in parallel, so the agent's
  loaded copy can be the stale one. Re-read the daily note when the date rolls, and before answering
  anything it may already have closed.
- **The index is a router.** Open only the pages the task needs. Loading everything makes every answer
  slower and blurrier.

## Writes: the promotion gradient

Facts start hot and move up as they prove durable.

| Tier | Where | What goes there | When |
|---|---|---|---|
| Hot | `daily/YYYY-MM-DD.md` | purchases, decisions, questions with their answers, quick notes | the moment they come up (`scripts/note.py`) |
| Hot | `sessions/YYYY-MM-DD.md` | what a working session changed and why | at wrap |
| Durable | `life.md`, `identity.md`, `values.md`, `goals.md`, `domains/*`, `decisions/*` | facts that will still be true next month | at wrap, promoted from the hot tier |
| Spine | `log.md` | one line per change that matters across the whole wiki | at wrap, only for those changes |

### Where a new fact goes

1. **A secret** (password, key, token, full account number): nowhere in the wiki. `.env` or a password
   manager.
2. **Sensitive** (health records, financial statements, details about another person): the original in
   `private/`, plus a bland one-line pointer in the relevant page.
3. **A purchase, decision, or question in passing**: today's `daily/` note. Always, even if it might be
   promoted later.
4. **A durable life fact** (a preference, a routine, a standing choice): [[life]].
5. **Who I am** (role, story, what I'm working on): [[identity]]. Propose the edit; I confirm it.
6. **A principle or tradeoff I live by**: [[values]]. Propose the edit; I confirm it.
7. **How a life area works** (sources, rules, gotchas): its page under `domains/`.
8. **A decision with real tradeoffs**: a record under `decisions/` (what, why, what was rejected).
9. **Something unverified**: [[inbox]] until it is checked.

### Values keep updating, carefully

My values page should grow from how I actually live, not stay frozen at setup. When a daily entry shows a
principle in action, or contradicts what `values.md` says, **propose** an update and say why. Never
rewrite values or identity silently.

### Self-descriptions are framing, not fact

Anything written to impress someone (an application, a bio, a cover letter) describes how I want to be
seen. Ask before promoting a line from one into identity or values.

### The log stays short

One line per milestone, newest on top, linking the session note for detail. If an entry runs past a
couple of lines, the detail belongs in the session note.

Related: [[index]] · [[SCHEMA]]
