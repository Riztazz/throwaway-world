---
name: design-history-timeline
description: Use when the user wants a dated history, chronology, contested historical accounts, or causal backstory explaining the present world.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: History & Timeline

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A history page is a protected type, so this skill adds craft, not permission to edit it.

## Use when / not when
Use when: building or checking a dated ledger, explaining the present through causes, or recording competing accounts of one event.
Not when: planning future arcs (`design-live-narrative-roadmap`), hiding or revealing facts to the audience (`design-knowledge-revelations`), or delivering the past through ruins (`design-environmental-storytelling`).

## Before you write
1. Search `INDEX.md` for the event, the actors and any date you are about to use. Open the ledger page and the pages that link to it, then `decisions/INBOX.md` for open questions about dates or causes.
2. The ledger is a `history` page, and `history` is a protected type. In explore mode write a new page or draft. In edit mode, adding or changing a dated entry on the existing ledger needs the user's authorization first (`rules/INVENTION.md`, T3). A request like "add X to the timeline" is not that authorization: stop and ask once, naming the entry, the year you propose or the missing year, and the pages that depend on the ledger.
3. If a year or cause is not in the world, it is unknown. Offer two or three options with what each would break, and let the user pick. Never write a guessed year into the ledger "as a placeholder".
4. Ask in facts and consequences, not pictures: what does the present still carry from this event, who gains from remembering it differently, and what must stay unexplained.

## Procedure
1. State the **Dating System**: epoch, era changes, calendar conversion, year length if relevant, and which dates are approximate or unknown. Do not manufacture precise dates from relative evidence.
2. Work backward from present consequences and forward from supplied events. For each entry record date or range, actors, cause, immediate change and what survives today.
3. Separate author truth, contemporary reports and later interpretation. Attribute competing accounts to their owners and evidence; a chronicle is not objective fact.
4. Check ages, travel times, succession, lifetimes, institutional continuity and the physical rules. Leave deliberately unknown causes unknown.
5. Connect each event to a living trace: infrastructure, borders, law, language, ruins, memory. A quiet event can matter more than a war.
6. If a contradiction needs an upstream revision, record the options and the dependent pages. Do not rewrite accepted lore silently, and do not refuse revision because it was authored earlier.

## Output
Use the history page's section names so the page imports without reshaping:

```markdown
# <Ledger name>

## Dating System
<epoch, conversion, known approximations>

::current-year:: <year>

## Historical Ledger
**<date>.** <What happened, who, what it changed.> [Link](page.md) to the actor or place.

::<event-key>:: <date>

## Deliberately Unexplained
<What the world chooses not to answer, and who disagrees.>
```

Each consequential event gets one `::key::` fact line so other pages can cite it. Competing accounts go in prose with their owners named.

## Worked example
Request in edit mode: "Add the year the Marrow Bridge fell." The index shows `marrow-bridge.md` calls it "lost before the ferries", and the ledger has the ferry guild at 60 AM and the first road at 12 AM. No page gives a year, and the ledger is protected.

Do not edit. Ask: "The ledger is a protected page and gives no year for the bridge. It would be one entry between 12 AM and 60 AM, and `ferry-guild.md` and `marrow-bridge.md` link to it. Which year do you choose, and do you authorize adding the entry?" Options to offer: before 40 AM (the road ran on the bridge for a generation), or 55 AM (the guild formed within five years of the collapse). After the user's answer, write the entry, a change record quoting their words, and leave the cause unexplained unless they supply it.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Treating "add it to the timeline" as authorization to edit the protected ledger | Ask once for the specific entry and wait; quote the answer in the change record |
| Picking a "placeholder" year because the task asked for one | Offer options and the consequence of each; the user picks |
| Resolving a deliberately unknown cause by inference | Keep it under Deliberately Unexplained |
| An encyclopedia of ancient names with no present consequence | Cut entries that explain nothing alive today |
| Taking one chronicle as fact | Attribute it; give the competing account its owner |

## Acceptance
- Dates and causal order reconcile, and each entry names a surviving consequence.
- Every year in the output comes from the world or from a choice the user made in this task.
- A protected ledger is changed only with quoted authorization and a change record listing dependents.
- Competing beliefs coexist without becoming contradictory author facts.
