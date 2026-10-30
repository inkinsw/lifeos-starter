# Recipe: a running engine (Strava)

Give this file to the agent: "Build the running engine from prompts/recipes/running.md." It builds the
engine in this folder, for your account. Nothing here is code to copy; it is what to build and the rules
that make it trustworthy.

## What you get

Ask "what should I run today?" or "am I on track this week?" and get an answer computed from your actual
runs, fetched a minute ago, with a receipt line saying where the numbers came from and how old they are.
Advice about training comes from live numbers, never from something written in a page last week.

## What you need

- A Strava account, and Strava's official **MCP connector** connected in your harness (look for Strava in
  your harness's connector or MCP settings). Strava's MCP needs a Strava subscription.
- Why the MCP and not Strava's regular API: Strava's 2026 API policy allows AI use of Strava data only
  through its MCP. Check the current policy when you build this; it may have changed.

## The rules (why it works)

1. **Live numbers, never prose.** No page in the wiki stores "my easy pace is 9:30" or "I ran 18 miles
   this week". Those go stale the day after they're written. The engine computes them at the moment of
   the question.
2. **Freshness first.** Every brief starts with how old its data is. Stale data is labelled STALE.
3. **The plan is config, the reasons are prose.** Targets and rules live in `config/training/plan.yaml`
   (weekly distance target, long-run day, easy-effort heart-rate cap, how fast mileage may rise). Why you
   chose them goes in `wiki/domains/running.md`.
4. **Grade the evidence behind each rule.** "Raise weekly mileage at most about 10%" is a common rule
   with weak evidence; say so in the plan (`basis: folklore | moderate | strong`), so advice can say how
   much to trust it.
5. **Units are a rule.** Miles or kilometers, min/mi or min/km: pick one in Working With Me and convert
   everything (Strava returns meters and seconds).

## Build steps (for the agent)

1. Ask the user their goal (a race and date, a weekly habit, or general fitness), current weekly
   distance, which days they can run, and their units.
2. Write `config/training/plan.yaml` from those answers. Every target gets a `basis`.
3. Write `scripts/run_brief.py` (standard library only). It reads a snapshot the agent fetches through
   the MCP into `data/tmp/strava_runs.json` (gitignored; include a `fetched_at` timestamp from the system
   clock) and prints: data age, this week vs target, the last few runs, easy pace from recent easy runs
   (and which runs it used), any rule that blocks raising volume, and a final `RECEIPT:` line.
4. Add a **Training Advice** section to `AGENTS.md`: any question about what to run, how far, how fast,
   or whether to build the week is answered by fetching from the MCP, running `run_brief.py`, answering
   first, then giving the receipt. If the MCP is down, give the last-known value with its date, labelled
   STALE.
5. Create `wiki/domains/running.md` (format in `wiki/SCHEMA.md`) and link it from `wiki/domains/index.md`.

## Check before trusting it

Compare the brief's weekly total against Strava's own app for the same week. They should match to within
rounding. If they don't, fix the engine before taking advice from it.
