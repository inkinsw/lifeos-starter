# Recall test: does a fresh session still know me?

Memory that only works inside the session that wrote it isn't memory. This test asks a brand-new session
fixed questions about me and about how this folder works, answered from the files alone.

Run it **once at setup**, and again **whenever `AGENTS.md`, `wiki/index.md`, or `wiki/storage-policy.md`
changes**.

## The two files

- `prompts/recall-questions.md` (in this folder, tracked): the questions only.
- **The answer key, outside this folder:** `~/.lifeos-recall/<this-folder's-name>-key.md`. It lives in
  the home directory on purpose: if the key sat anywhere inside this folder, the test session could find
  the answers by searching instead of by following the routing.

## Writing the questions

8 to 10 questions, numbered:

- **5 or 6 durable facts**, one each from `identity.md`, `values.md`, `goals.md`, and, where they hold
  anything yet, `life.md` and a domain page (e.g. "What am I working toward in the next three months?").
- **2 routing questions:** "Where does a purchase I mention in passing get written?" and "Which files do
  you read at the start of a session?"
- **1 rule** from Working With Me.
- **1 probe for a fact that is NOT in the record** (something plausible, like a favorite food that was
  never mentioned). The right answer is "not in the record". A session that guesses fails this one.

The key holds, for each question, the expected answer and the page that holds it. When a new durable fact
matters to you, add a question for it.

## Running it

Start a **fresh** session in this folder: a new chat, no history. If the harness can run a one-off,
read-only session from the command line, the agent may run it itself. Otherwise open a new session and
paste:

```text
Treat this as a fresh session. Use only the files in this folder: read nothing outside it and edit
nothing. Follow the session-start routine in AGENTS.md, then answer every question in
prompts/recall-questions.md. Name the file each answer came from. If the record does not hold an answer,
say "not in the record" instead of guessing.
```

## Grading

Back in a normal session, say "grade the recall test" and paste the answers. The agent reads the key from
the home directory, marks each answer right, partial, or wrong, and adds one line to `wiki/log.md`:

```text
- 2026-11-02 - **Recall test: 9/10.** Missed Q4 (the weekly long-run day): the fact was only in a daily note.
```

A miss is one of two things. **Routing broke:** the page holds the fact but the session didn't find it,
so fix the index or the contract. **The fact never got promoted:** it lives only in an old daily note, so
move it to the right page. **Fix the record, never the question.**
