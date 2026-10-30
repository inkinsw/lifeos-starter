# Stage 8: The recall test

Prove that a fresh session, with no memory of this setup conversation, can answer from the files alone.
The full method is in the workspace at `prompts/recall-test.md`. Follow it:

1. Write 8 to 10 questions to `prompts/recall-questions.md` (tracked): durable facts from the interview,
   two routing questions, one Working With Me rule, and one probe for a fact that is not in the record.
2. Write the answer key to `~/.lifeos-recall/<workspace-folder-name>-key.md`, **outside the workspace**,
   creating the folder if needed. Tell the user where it is.
3. Run the test in a fresh session. If this harness can run a one-off, non-interactive, read-only session
   from the command line, run it with the workspace as its working directory. Otherwise ask the user to
   open a new session in the workspace and paste the prompt from `prompts/recall-test.md`, then paste the
   answers back here.
4. Grade against the key. Add the result line to `wiki/log.md` (newest on top).
5. **Fix any miss before setup ends.** A routing miss means fixing the index or the contract; a missing
   fact means writing it to the right page. Rerun the questions that missed.

Return the score and any fixes made.
