# LifeOS Starter: Setup Manager

This is the only setup entrypoint. The agent the user already works in (any file-aware agent) is the
setup manager for the whole flow. Read one stage at a time.

## The user's prompt

```text
Set up my LifeOS from this repository:
https://github.com/inkinsw/lifeos-starter

Start with SETUP.md. Use the repository only as setup instructions and a template source; do not turn
its clone into my workspace.
```

## Goal

Turn one folder into a personal life harness: a plain-text memory the agent reads before it answers, a
contract (`AGENTS.md`) every harness follows, a daily capture lane, and pages about who the user is and
what they value, filled from a short interview.

## Global rules

- **Never replace, truncate, or silently merge an existing file.** Add missing files only. When a file the
  starter needs already exists, show the proposed change and ask.
- **Never move or edit an existing project folder.**
- **Never read secrets** (`.env`, keychains, token files) or broad source trees.
- **Ask before:** creating the workspace folder, running `git init`, committing, creating a remote, or
  pushing.
- **Ask only what the current stage cannot answer safely.** If the user already gave an answer (in the
  first message or earlier), use it instead of asking again.
- **Never infer personal facts.** Unknown stays `UNKNOWN`.
- **Sensitive answers** (health, money specifics, other people) go to `private/`, with a one-line pointer
  in the wiki, unless the user says otherwise.
- Write everything harness-neutral: *the agent*, *the harness*.
- Read only the next routed prompt.

## Stage 0: make the starter available

If this repository is not already on disk, clone it into a temporary staging directory the agent
creates (for example under the system temp folder):

```text
git clone --depth 1 https://github.com/inkinsw/lifeos-starter <staging-dir>
```

**If the clone fails with an authentication error,** the repository is private and this computer is not
logged in to GitHub yet. Ask the user to run `gh auth login` (GitHub's CLI; install it first if missing)
and finish the browser step, then retry with `gh repo clone inkinsw/lifeos-starter <staging-dir>`.

- Never clone over the user's folder. Never personalize the staging clone.
- Record the staging path; later stages read their prompts from it.
- If the repository was cloned directly into a folder meant to become the workspace, stop, move the clone
  to a staging path, and use the now-empty folder as the candidate workspace. If unsure what was there
  before, ask.

## Routed workflow

1. `prompts/setup/01-choose-folder.md`
2. `prompts/setup/02-prerequisites.md`
3. `prompts/setup/03-scaffold.md`
4. `prompts/setup/04-life-interview.md`
5. `prompts/setup/05-life-areas.md`
6. `prompts/setup/06-finalize-contract.md`
7. `prompts/setup/07-git.md`
8. `prompts/setup/08-recall-test.md`
9. `prompts/setup/09-first-week.md`

After Stage 1, use the confirmed workspace as the working directory for every remaining stage. Keep
reading the stage prompts from the staging clone.

## Done when

- one workspace folder is confirmed and holds the scaffold, with no existing file replaced without
  approval;
- `AGENTS.md` is personalized (no `{{FILL` placeholders left) and `CLAUDE.md` imports it;
- `wiki/identity.md`, `values.md`, `goals.md` hold confirmed answers or `UNKNOWN`;
- one domain page exists per chosen life area, linked from `wiki/domains/index.md`;
- the workspace is a git repository with a first commit (or the user declined git);
- the recall test ran once and its result is in `wiki/log.md`;
- the first-week handoff was given;
- the staging clone is removed.
