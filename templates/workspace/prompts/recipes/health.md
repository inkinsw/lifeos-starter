# Recipe: a health engine (a wearable)

Give this file to the agent: "Build the health engine from prompts/recipes/health.md." It builds the
engine in this folder, for your device.

## What you get

Ask "how recovered am I?" or "why has my sleep been bad?" and get an answer from your own data: recovery,
sleep, resting heart rate, HRV, strain. The engine states the facts; the advice is written separately, so
you can always tell which is which.

## What you need

One of these, depending on your device:

- **WHOOP:** a developer app (OAuth) on WHOOP's developer platform. The API gives daily summaries
  (recovery, sleep, strain, workouts), not the second-by-second graphs the app shows.
- **Oura, Garmin, Fitbit:** each has its own API or export. Same pattern.
- **Apple Health:** an export file from the Health app, re-exported when you want fresh data.

## The rules (why it works)

1. **Facts vs advice.** The engine computes facts deterministically (no AI in the math): last night's
   sleep, a 7-day trend, a simple push / hold / rest state from fixed thresholds. Advice ("go easy today")
   is written by the agent on request, clearly labelled, and never mixed into the numbers.
2. **Secrets stay out of git.** API client IDs and secrets go in `.env`; tokens go in `data/`. Both are
   gitignored.
3. **One writer.** Only one machine syncs from the device. If you use two computers, pick one.
4. **Freshness is visible.** Every brief prints when the data was last synced.
5. **Medical records are private.** Lab results, doctor's notes, and imaging go in `private/health/`. The
   wiki gets a one-line pointer.
6. **Watch the units.** HRV is the classic trap: some apps show raw RMSSD in milliseconds, others a scaled
   score, so the same night can read 38 in one app and 72 in another. Say which one a number is.

## Build steps (for the agent)

1. Ask which device, and walk the user through getting API access (or an export).
2. Write a sync script that pulls daily summaries into `data/health.db` (SQLite, standard library) or a
   JSON file in `data/`, with a `synced_at` stamp.
3. Write `scripts/health_brief.py`: data age, last night, the 7-day trend, the push / hold / rest state and
   which threshold set it, and a `RECEIPT:` line.
4. Add a line to `AGENTS.md` → Present-State Answers: health numbers come from `health_brief.py` run at
   the moment of answering.
5. Create `wiki/domains/health.md` (thresholds and why, the device, gotchas) and link it from
   `wiki/domains/index.md`.

## Check before trusting it

Pick three recent days and compare the brief against the device's own app. Same numbers, same dates
(time zones shift late nights onto the wrong day; check one that crosses midnight).
