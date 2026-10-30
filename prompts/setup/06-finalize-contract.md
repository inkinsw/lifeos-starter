# Stage 6: Finalize the contract

## If AGENTS.md came from the template

Personalize it in place:

- The title: the user's name, e.g. `# Alex's LifeOS`.
- **Working With Me:** replace the `{{FILL: ...}}` block with the rules from the interview (answers 9 to
  12), one bullet each, bold label first, in the user's words.
- Leave every other section as written. Show the exact diff.

## If AGENTS.md existed before setup

1. Leave the original unchanged.
2. Write `AGENTS.proposed.md`: every original instruction, plus the starter's sections that are missing.
   Never silently drop or weaken an original instruction.
3. Show the full proposal and a diff; ask the user to confirm.
4. Only after confirmation: replace `AGENTS.md` with the proposal and delete `AGENTS.proposed.md`.

## CLAUDE.md

`AGENTS.md` is the one contract. `CLAUDE.md` exists only so harnesses that read `CLAUDE.md` load it, and
it does that with an import line: `@AGENTS.md`. A new `CLAUDE.md` comes from the template. An existing one
without that line: show the line and where it goes, and ask before adding it. Never copy rules into
`CLAUDE.md`.

## Skills

The workspace has `skills/` (grill-me, roast, session-handoff). If this harness loads skills from a folder
of its own inside the project (for harnesses that use a `.claude/` folder, that is `.claude/skills/`), copy
each skill folder there and say where. If it has no skill support, skip this: the user can still say
"read skills/grill-me/SKILL.md and do that".

## Fill the rest

- `wiki/log.md`: the first line, below the header:
  `- YYYY-MM-DD - **LifeOS set up.** Interview done, N life areas, recall test next. See [[sessions/YYYY-MM-DD]].`
- `wiki/sessions/YYYY-MM-DD.md`: a short note of what setup did (sections: What changed, Decisions,
  Next), and its line in `wiki/session-catalog.md`: `- [[sessions/YYYY-MM-DD]] - LifeOS setup`.
- Run `python scripts/lint_wiki.py`. Fix any error before continuing.

Return the final diff of `AGENTS.md` and the lint result.
