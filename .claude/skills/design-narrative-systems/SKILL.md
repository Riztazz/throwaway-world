---
name: design-narrative-systems
description: Use when the user wants reusable dialogue, reputation, relationship, consequence, or narrative-reactivity rules and contracts for an online RPG; excludes combat and numeric economy tuning.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Narrative Systems & Reactivity

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill writes a contract authors can share; it does not make the world rules.

## Use when / not when
Use when: a rule for how narrative reacts (reputation, relationship, consequence, a repeating condition) must be specified so authors and implementers apply it the same way.
Not when: shared state authority (`design-persistent-world-state`), one quest's script (`design-quest-narrative`), combat or numeric tuning (not this library).

## Before you write
1. Read the rules the system rests on. If the proposed system moves, stores, carries or multiplies something the physical-rules page forbids, that is a conflict with a protected page: say which invariant it breaks and offer what fits. Do not specify around it.
2. Search `INDEX.md` for existing rules, factions and places the system touches; read open decisions about them.
3. A contract is not a page type. Save it as `design/systems/<slug>.md`.
4. Ask in facts: what can the player see, what changes for others, what happens when the condition lapses, who has authority over the result.

## Procedure
1. Describe the player-facing behaviour with concrete before and after cases. Keep reusable rules apart from one quest's script.
2. List inputs and events, conditions, outputs and side effects. Variable names are proposals unless a real interface supplies them.
3. Classify scope: personal, group, account, local community or shared world. Remembered choices and knowledge differ from physical change.
4. Set precedence for overlapping rules, defaults for missing data, expiry and reversal, repetition and idempotency intent. Dialogue variation is not mutation.
5. Check agency and legibility: which commitments the player understands, how consequences show, and how the rule avoids making each player the unique saviour.
6. Specify fallbacks for interrupted or out-of-order interaction, changed canon, reconnect and concurrent actors. Authority for shared transitions goes to `design-persistent-world-state`.
7. Write testable cases: condition met, condition absent, conflicting rules, repeated event, stale text, branch unreachable after a shared change.
8. Compare against a real interface if one exists. Otherwise mark the interface unverified; prose is not evidence the engine supports it.

## Output
```markdown
# <System> contract
Purpose:
Scope:
Inputs and events:
Conditions:
Outputs and side effects:
Precedence and defaults:
Lifecycle (expiry, reversal, repeat):
Fallbacks:
Cases: | given | when | expected |
Conflicts with world rules: <invariant ids, or none>
Open engineering questions:
```

## Worked example
Request in explore mode: "A system where lamp-oil rations earned in the south are carried north to feed the beacon stations." The physical-rules page says oil burns only where it was pressed (INV-4: no stored light). Report that carrying the ration to a distant station breaks INV-4 if the system treats the oil as keeping its charge. Offer: oil rations are ordinary oil and the station only keeps the *account* of what was delivered (a ledger system, scope: community), with a case table for a late delivery and a lapsed ledger. Do not specify the charge-carrying version unless the user authorizes changing INV-4.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Specifying around a world rule that forbids the system | Name the invariant, offer a version that fits, ask |
| Variable names presented as the real interface | Mark them proposals until a contract supplies them |
| Every player is the unique saviour | Scope the result; show shared consequences |
| Dialogue variation and state mutation mixed | Separate flavour from change |
| No cases | Write given / when / expected for the edge cases |

## Acceptance
- Different authors can apply the rule the same way; scope and precedence are explicit.
- Examples expose ambiguous or unsupported behaviour.
- No world rule is broken; any conflict is named with its invariant id.
