# Wiki Schema: the shape of a page

**This page owns the shape of the wiki: page roles, filenames, links.** How memory is read and written
lives in [[storage-policy]].

The wiki holds **compiled understanding**: who I am, what I value, life facts, how each life area works,
decisions and why. It is not raw data. Raw sources go in [[raw/README|raw/]] or `private/`.

## Page roles

| Page | Role |
|---|---|
| `index.md` | The router. Every page must be reachable from it by links (directly or through a sub-index). It does not list every page. |
| `storage-policy.md` | How memory is read and written. |
| `SCHEMA.md` | This page. |
| `log.md` | One line per milestone, **newest on top**. |
| `identity.md`, `values.md`, `life.md`, `goals.md` | The self pages. Compact, user-confirmed, `UNKNOWN` instead of a guess. |
| `reminders.md` | Nudges and open questions, as data. |
| `session-catalog.md` | One line per session note, newest on top. |
| `inbox.md` | Material not yet verified. |
| `decisions/NNN-short-title.md` | One decision each. Listed in `decisions/index.md`. |
| `domains/<area>.md` | One life area each. Listed in `domains/index.md`. |
| `daily/YYYY-MM-DD.md` | Append-anytime life capture. Read by date, not by link, so it is exempt from reachability. |
| `sessions/YYYY-MM-DD.md` | What a working session changed and why. |
| `raw/` | Source material kept unchanged, for provenance. |

## Conventions

- **Links:** `[[page]]` or `[[folder/page]]`, written from the wiki root (`[[domains/running]]`). An
  alias goes after a pipe: `[[decisions/index|decisions]]`. Link a folder's `index` page, never the bare
  folder. (Any markdown viewer works; Obsidian renders these links as a clickable graph.)
- **Dates are absolute:** `2026-11-02`, never "last Tuesday". Convert relative dates when writing.
- **Cite the source** behind a durable claim: a daily note, a session note, a file in `raw/` or
  `private/`, or "confirmed by me on 2026-11-02".
- **Mark uncertainty, contradictions, and stale claims** where they sit, with a date. Don't delete history
  to make a page tidy.
- **Consolidate, don't append forever.** When a page passes a few hundred lines, split or tighten it.

## Formats

A log line:

```text
- 2026-11-02 - **What changed, as a headline.** One sentence of why. See [[sessions/2026-11-02]].
```

A decision record (`decisions/NNN-short-title.md`):

```text
# NNN: Short title
Date: YYYY-MM-DD · Status: decided | superseded by NNN

## Decision
## Why
## Options considered (and why not)
## What would change it
```

A domain page (`domains/<area>.md`):

```text
# <Area>
## What I want from this area
## Where the data lives (sources of truth)
## Rules I follow here
## Engine (if built): what runs, what it reads, how fresh it is
## Open questions
```
