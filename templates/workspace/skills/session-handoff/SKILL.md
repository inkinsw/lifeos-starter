---
name: session-handoff
description: Use when the user says "session handoff", "wrap up session", "hand off", "handoff summary", or wants a structured end-of-session summary before clearing context. Writes a durable handoff file (surviving /clear) covering decisions, shipped changes, key files, running state, verification steps, deferrals, and open questions, plus a chat preview, so a fresh agent can continue seamlessly by reading the file.
---

# Session Handoff

Produce a repeatable end-of-session summary so the user can `/clear` and start a fresh agent without losing continuity. The next agent should be able to pick up by reading the handoff **file** alone.

This is a **context-handoff artifact**, not a status report. The audience is a future instance of you, not a stakeholder.

**Why this writes a file.** The whole point of a handoff is surviving context loss — but `/clear` wipes the context window, and a chat-only handoff lives *in* that window. So at the moment it's meant to be read, it would already be gone. The handoff must therefore be written to disk. The chat copy is a human-readable preview; the file is the thing that actually survives the clear and that the next agent reads.

## When to invoke

User says: "session handoff", "wrap up session", "hand off", "handoff summary", "let's wrap up", "summarize before I clear", or any near-equivalent. Also invoke proactively if the user says they're about to `/clear` without having run it yet.

## How to produce the summary

1. **Review the full conversation**, not just the last few turns. Handoffs miss things when they only summarize recent context.
2. **Pull state from these sources (in order):**
   - Plan files referenced this session (check `~/.claude/plans/` if a plan was mentioned; the config dir honors `$CLAUDE_CONFIG_DIR` if the user has set it).
   - TodoWrite state — any in-progress or pending tasks.
   - Background processes you started with `run_in_background` — shell IDs are load-bearing for the next agent.
   - Files created or modified this session — you know what you touched; start from recall, then cross-check (step 3).
   - Memory files written or updated (`~/.claude/projects/<project>/memory/`).
   - Unresolved questions — things you asked the user that never got a clear answer, or things the user asked that got deflected.
3. **Cross-check your file list against git — do NOT audit the filesystem.** Over a long session, auto-compaction can quietly drop the "which files did I touch" details, so pure recall is not fully trustworthy for the one thing the next agent most needs to be correct. If you're in a git repo, run a single `git diff --name-only` (and `git status --short` for untracked files) purely as a sanity check against what you remember, and fold in anything you missed. That is the only filesystem read allowed. No `git log`, no broad `Glob` sweeps, no directory crawls. If a change isn't from THIS session, it doesn't belong here — the git cross-check is to catch omissions, not to reconstruct history.
4. **Write the handoff to a file, then show a chat preview** (see "Persistence" below). Do not update memory from this skill.

## Output template — use exactly this structure, every time

```
# Session Handoff — <one-line title of what this session was about>

## Where it started
<2-3 sentences: what the user asked for, key framing or constraints that emerged>

## Decisions locked + what shipped
- <decision or change> — <why, and where it lives (absolute path if a file)>
- ...

## Key files for next session
- `<absolute path>` — <why the next agent should read this first>
- Plan file: `<path>` (if a plan drove the session)
- Memory files touched: `<paths>` (if any)

## Running state
- Background processes: <shell IDs + what they are + how to kill> — or "none"
- Dev servers / ports: <url + port> — or "none"
- Open worktrees / branches: <paths> — or "none"

## Verification — how to confirm things still work
- `<command>` — <expected outcome>
- ...

## Deferred + open questions
- Deferred: <item> — <why pushed to later>
- Open: <question needing the user's input> — <context>

## Pick up here
<1-2 sentences: the single most likely next action for a fresh agent>
```

## Persistence — the file is the mechanism, not an afterthought

1. Get today's date with `date +%F` if you don't already know it.
2. Write the handoff to `.claude/handoffs/{YYYY-MM-DD}-{slug}.md` in the current project (create the `.claude/handoffs/` folder if it doesn't exist). Project-local so it sits next to the work the next agent continues, and survives `/clear`.
3. Print the same content in chat as a preview so the user can eyeball it.
4. **Tell the user how the next agent picks it up**, in one line: the saved path, plus "after you `/clear`, tell the fresh agent to read `<path>`." The fresh agent has no context after the clear, so the handoff only works if it's pointed at the file — surface the path explicitly. (Optional: a one-line pointer in the project's `CLAUDE.md` telling agents to check `.claude/handoffs/` for the most recent file makes this automatic.)

## Hard rules

1. **Persist to a file, always.** Write the handoff to `.claude/handoffs/{date}-{slug}.md` and surface the path. The chat preview is a convenience, not the deliverable — the file is what survives `/clear` and what the next agent reads. Do not update memory from this skill.
2. **Never invent state.** If a section has nothing to report, write "none" — do not omit the section. Structure stability is the whole point.
3. **Absolute paths always** inside the handoff body. The next agent may have a different working directory.
4. **If a plan file drove the session, name it first** in "Key files" so the next agent reads it before anything else.
5. **No emojis, no hype, no "great job" summaries.** Terse and concrete — paths, commands, shell IDs, decisions. Match the tone of a seasoned engineer handing off at end-of-shift.
6. **Background process IDs are critical.** If you started any `run_in_background` shells, their IDs must appear in "Running state" with the kill command — the next agent cannot find them otherwise.
7. **Portable paths for config lookups.** Use `~/.claude/` (honoring `$CLAUDE_CONFIG_DIR`), never a hardcoded username. A path baked to one machine silently reads nothing on any other.

## Anti-patterns — do not do these

- Summarizing the last 3 turns and calling it a handoff.
- Listing files by relative path inside the handoff body.
- Skipping the "Running state" section because "nothing is running" — write "none" instead.
- Producing the handoff in chat only, without writing the file. After `/clear` the chat copy is gone; the file is the whole point.
- Reconstructing the session from `git log` or broad `Glob` sweeps. The git cross-check is one `git diff --name-only` to catch omissions, not a filesystem audit.
- Trusting recall alone for the file list on a long session — compaction may have dropped it; cross-check with git.
- Adding a "what went well / what went poorly" retrospective. This isn't a retro.
- Recommending next steps beyond the single "Pick up here" line. The next agent decides; you just hand off.
