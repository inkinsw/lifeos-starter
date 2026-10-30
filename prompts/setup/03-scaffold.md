# Stage 3: Add the workspace files

Source: `templates/workspace/` in the staging clone. Target: the confirmed workspace folder.

## Merge rules

- Copy **missing** files and folders only, including the dotfiles (`.gitignore`, `.gitattributes`) and
  the empty `wiki/daily/` and `wiki/sessions/` folders (their `.gitkeep` files).
- **Never replace, truncate, or merge an existing file.** Record every collision.
- Never copy installer files (`SETUP.md`, `prompts/setup/`, `tests/`, the starter's own `README.md` and
  `LICENSE`, `.git/`). Copy only what is inside `templates/workspace/`.
- Never touch an existing project folder.
- An existing `AGENTS.md` or `CLAUDE.md` is preserved for the reviewed merge in Stage 6.
- An existing `.gitignore`: propose only the missing lines (`private/*`, `!private/README.md`, `.env`,
  `.env.*`, `data/`) and ask before adding them.

## Review

Return: files created, files skipped because they existed, collisions to resolve, and confirmation that no
installer file and no existing project file changed. Resolve collisions with the user before continuing.
