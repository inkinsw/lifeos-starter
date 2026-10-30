# Stage 5: Life areas

Each life area the user cares about gets a page under `wiki/domains/`. The areas come from the user, not
from a fixed list.

## Ask

"Which parts of your life do you want this to keep track of? Pick 2 to 5 to start; you can add more any
time." If they want ideas, offer: health and fitness, a sport (running, lifting, a team), money, school
or work, learning a skill, creative projects, faith, relationships, calendar and time.

## For each area

1. Create `wiki/domains/<area>.md` (lowercase, hyphens) in the domain-page format from
   `wiki/SCHEMA.md`. Fill "What I want from this area" from what the user said; the rest starts
   `UNKNOWN`.
2. Add it to `wiki/domains/index.md`: `- [[domains/<area>]]: one line on what it covers`.
3. If a recipe in `prompts/recipes/` matches (running, health, money, calendar), mention it in one line:
   "When you want real numbers here, say: build the running engine from prompts/recipes/running.md."
   **Offer it, don't build it now.** Setup stays short; engines come after the user has lived with the
   memory for a while.

Return the pages created.
