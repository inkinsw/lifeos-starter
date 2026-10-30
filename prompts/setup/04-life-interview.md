# Stage 4: The life interview

This is the heart of setup. The answers become `wiki/identity.md`, `wiki/values.md`, `wiki/goals.md`,
and the Working With Me rules in `AGENTS.md`. Keep it a conversation, not a form: about 15 minutes.

## How to run it

- Say up front: every question is skippable, nothing is shared anywhere, and anything sensitive can go to
  `private/` (gitignored) instead of the wiki.
- **Ask one round at a time** (the questions below, one message per round). Wait for the answers.
- **Use their words.** Quote a phrase that matters exactly; don't polish it into something they didn't
  say.
- **Follow up once** when an answer is vague and the vagueness matters ("what would that look like by
  March?"). Then move on.
- **Never infer.** A skipped question becomes `UNKNOWN`.
- **If the user already answered** some of this in their first message, use it and ask only what's left.

## Round 1: who you are

1. What should I call you?
2. What does a normal week look like right now: school, work, what you're building, what takes your time?
3. In one sentence: what do you want this LifeOS to help you with?

## Round 2: where you're headed

4. What are you working toward this year?
5. What would a win in the next three months look like, concretely enough that we'd both know it
   happened?

## Round 3: what you value

6. Is there a motto or a principle you actually live by? In your words.
7. When you face a hard choice, what do you optimize for? Is there anything you won't bend on?
8. Optional: is there a habit or pattern you're working on changing, where a system could help more than
   willpower? (Offer `private/` for this one.)

## Round 4: how you want me to work with you

9. How should I talk to you: short or detailed, blunt or gentle, teach you things or just answer?
10. When a question has several reasonable answers, do you want every option laid out, or just my pick?
11. What should I always ask you before doing?
12. Anything AI answers do that annoys you, that I should never do?

## Write it down

Before writing, show a short summary of what goes where and ask "anything wrong or missing?" Then:

- `wiki/identity.md`: answers 1 and 2, answer 3 as what they're building toward, and answer 8 (or a
  pointer to a file in `private/` if they chose that).
- `wiki/values.md`: answers 6 and 7, and a first line under "How this page changed".
- `wiki/goals.md`: answers 4 and 5.
- The Working With Me rules (written into `AGENTS.md` in Stage 6): answers 9 to 12, one bullet each, in
  their words.
- Replace every `{{FILL: ...}}` in those pages, including `last updated` with today's date
  (`YYYY-MM-DD`). A section with no answer gets `UNKNOWN`.
- Write the first decision record, `wiki/decisions/001-start-a-lifeos.md` (format in `wiki/SCHEMA.md`):
  decided today to keep a LifeOS, why (answer 3), and what would change it. List it in
  `wiki/decisions/index.md` as `- [[decisions/001-start-a-lifeos]]: one line`.

Return the paths written.
