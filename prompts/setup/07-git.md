# Stage 7: Git

The workspace is versioned with git, so every change to the memory is recorded and reversible.

## If the folder is not a git repository yet

1. Show what would be tracked (`git add -n .` after init, or a file listing before) and confirm nothing
   from `private/` (except its README) and no `.env` is in the list.
2. Ask, then run `git init -b main`.
3. If git has no name or email configured, ask the user for them and set them for this repository only
   (`git config user.name "..."`, `git config user.email "..."`).
4. Ask, then make the first commit: `git add -A` and `git commit -m "LifeOS setup"`.

## If it already is one

Don't reinitialize it and don't touch its remote. Commit only the files setup added, after showing them.

## Optional backup

Offer once: "Want a private GitHub repository as a backup? Your memory then survives a lost laptop." If
yes and `gh` is installed and logged in: ask for the name, then
`gh repo create <name> --private --source . --push`. **Never** use the starter repository as this
workspace's remote. If no, `scripts/wrap.py` commits locally and says so.

Return the commit hash and the remote (or "none").
