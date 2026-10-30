# Stage 1: Choose the workspace folder

Read-only until the user confirms.

## Ask (once, skipping anything already known)

1. Should the LifeOS live in a new folder, or in a folder that already exists?
2. Which path? Suggest a new folder named `LifeOS` in the user's home directory.

## Inspect the candidate

Show: the resolved path; whether it exists; whether it is already a git repository; its immediate files
and folders only (no recursive scan); whether `AGENTS.md`, `CLAUDE.md`, or `wiki/` already exist; any
file the starter would collide with.

**Warn if the folder sits inside another project that has its own `AGENTS.md` or `CLAUDE.md` above it.**
Some harnesses load every instruction file in the folders above the one they open, so a LifeOS inside
another repository would inherit that repository's rules. Suggest a folder outside it.

## Confirm

One question: the exact path, permission to create it if missing, and permission to add the starter's
files. Return the confirmed path to the setup manager.
