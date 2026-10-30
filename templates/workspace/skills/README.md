# Skills

Reusable procedures the agent can follow. Each skill is a folder with a `SKILL.md`: a description of when
to use it, then the steps. Harnesses that support skills load them from their own skills folder; setup
copies these there. A harness without skill support can still follow one: say "read
skills/grill-me/SKILL.md and do that".

| Skill | Use it when |
|---|---|
| `grill-me` | You want to think a plan through: it interviews you one question at a time and saves every answer to `brainstorms/`. |
| `roast` | You want a brutal second opinion before committing to an idea: five critics, one GO / RESHAPE / KILL verdict, saved to `roasts/`. |
| `session-handoff` | You're about to clear the chat and want the next session to pick up exactly where this one stopped. |

These three came from the LifeOS this starter was built from. `grill-me` is adapted from Matt Pocock's
skills (github.com/mattpocock/skills, MIT); `roast` and `session-handoff` are adapted from community
skills of the same names (MIT-licensed collections). Add your own as you find yourself repeating a
procedure: that is "convert discipline into mechanism" applied to how you work.
