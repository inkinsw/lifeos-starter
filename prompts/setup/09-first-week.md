# Stage 9: First week, then clean up

## Tell the user how to live in it (short, in chat)

- **Talk to it about your life as it happens.** Purchases, decisions, questions: it writes each one to
  today's daily note.
- **Say "wrap"** at the end of a session that changed something. It writes a session note, promotes what
  will still matter next month, and commits.
- **Correct it out loud.** When it works with you the wrong way, it proposes a Working With Me rule, and
  every future session follows it.
- **Your values page grows from your life.** When something you do shows a principle (or contradicts
  one), it proposes an update; you decide.
- **When an area deserves real numbers,** build its engine from `prompts/recipes/`.
- **Tools you have:** "grill me on <plan>", "roast <idea>", "session handoff".

## Commit and clean up

1. Run `python scripts/wrap.py --all` to commit anything setup left uncommitted (the tree holds only
   setup's work at this point). "nothing to commit" is fine: it means every stage already committed.
2. Remove the staging clone. Confirm it is gone and that nothing in the workspace points at it.
3. Final message: the workspace path, the recall score, the life areas created, and one suggested first
   thing to say tomorrow.
