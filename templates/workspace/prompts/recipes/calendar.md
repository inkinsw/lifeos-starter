# Recipe: a calendar engine

Give this file to the agent: "Build the calendar engine from prompts/recipes/calendar.md." It builds the
engine in this folder, for your calendar.

## What you get

"What's my week look like?" "Find me two free evenings for a run" answered from your real calendar, and
events added or moved when you ask.

## What you need

Either a calendar connector in your harness (many harnesses offer Google Calendar or Outlook connectors),
or API access you set up yourself (for Google: a Desktop OAuth client in a Google Cloud project, with its
ID and secret in `.env`).

## The rules (why it works)

1. **One writer.** Reading and writing are separate. The engine only reads; every change goes through one
   path (the connector, or one script such as `scripts/cal.py add / move / rm`) that the agent runs when
   you ask. Never two tools writing the same calendar.
2. **Never cache.** Fetch live every time. A calendar that was right this morning can be wrong by lunch.
3. **Time zones.** Calendar APIs return UTC or the event's own zone. Convert to your local zone before
   saying a time out loud. An event at 11 PM can land on the wrong day if you don't.
4. **Confirm before writing.** The agent says exactly what it will add or move, then does it.

## Build steps (for the agent)

1. Ask which calendar and which access path (connector or API).
2. With a connector: add a short section to `wiki/domains/calendar.md` saying which calendars count and
   how to read them. With the API: write `scripts/cal.py` (`ls`, `add`, `move`, `rm`), tokens in `data/`.
3. Add a line to `AGENTS.md` → Present-State Answers: schedule questions are answered from a live fetch.
4. Link `wiki/domains/calendar.md` from `wiki/domains/index.md`.

## Check before trusting it

List next week, then compare against the calendar app, including one event that crosses midnight.
