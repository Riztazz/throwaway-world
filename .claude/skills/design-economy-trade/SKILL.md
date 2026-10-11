---
name: design-economy-trade
description: Use when the user wants lore currency, trade, labor, infrastructure, ownership, supply dependencies, or how material exchange shapes societies; excludes numeric game pricing.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Economy & Trade

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. An economy page is a core-rule type and therefore protected: this skill adds craft, not permission to edit one.

## Use when / not when
Use when: currency, trade, labour, ownership, supply or infrastructure needs explaining, or a route or resource change needs its consequences traced.
Not when: balanced shop prices, rewards or currency sinks (not this library), or a story seed (`design-story-hooks`).

## Before you write
1. Search `INDEX.md` for the goods, the routes, the places and the currency. Open the economy page, the geography and history pages, and the faction pages that control the routes.
2. Changing the existing economy page, a fact line on it, or a rate it fixes, is a protected change: stop and ask once, naming the page, the exact change and the pages that depend on it (`rules/INVENTION.md`). In explore mode a new page of a different type may describe a local trade without editing the economy page.
3. Read the decisions about payment or control. If a decision was replaced, follow the newer one.
4. Check any magic-assisted production against the physical-rules page; it is protected and its invariants win.
5. Ask in facts and costs: who makes it, who uses it, who carries it, what spoils or is lost on the way, who can refuse payment, what happens if the route closes.

## Procedure
1. Define **Currency** and other exchange: credit, debt, payment in kind, trust and enforcement, only in forms the setting supports. Say why it is accepted and who can issue or refuse it.
2. Map **Trade relationships** between named places: goods, producers, users, middlemen, and why the carriage pays.
3. Derive **Barrier costs** in time, risk, spoilage, scarcity and bargaining power. No tuned prices.
4. Describe **Control** of routes, land, extraction, workshops, licences and labour. Separate law from practical control and include informal networks.
5. Show the **Historical mark** through a relevant disruption or inherited institution. Propose a missing causal fact; do not manufacture canon.
6. Cover everyday provisioning where it matters (food, water, storage, repair, waste, news, medicine). Test a closure or a depletion and say who feels it first.
7. Keep lore consequences apart from player-market tuning. No guaranteed scarcity only because a story needs it.

## Output
Use the economy page's section names:

```markdown
# <Economy or local trade>
## Currency
## Trade relationships
## Barrier costs
## Control
## Historical mark
```

Add a short supply-dependency sketch (producer -> carrier -> user) and one disruption example when useful.

## Worked example
Request in explore mode: "How does lamp oil reach the cliff town of Verrow?" The index shows Verrow, a trade road, and an economy page that fixes the road toll in coin. Write a new local-trade page: oil is pressed at the lowland farms, carried by mule trains the toll office taxes in coin (as the economy page states, so it is cited, not changed), stored in the chapel cellars. Barrier costs: spoilage in summer and the mule-driver's winter premium. Control: the chapel decides who may buy before the feast days (a proposal). Disruption: if the road closes, the chapel's stock lasts one season and the tallow-makers gain. The economy page is untouched and no prices are given.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Tuned shop prices and reward amounts | Describe costs in time, risk and bargaining power |
| Editing the economy page to add a local trade | Link to it; write a new page or ask for authorization |
| Following the replaced payment rule | Check decision status and follow the newer one |
| Magic that makes goods for free | Check the invariants; cost has to come from somewhere |
| Control stated only as law | Add who actually controls it in practice |

## Acceptance
- A reader can trace a necessity from production to use and name the bottleneck and the labour.
- A specific consequence follows if a route or institution fails.
- No protected page was changed without quoted authorization; proposed facts are labelled.
