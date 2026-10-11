---
name: design-magic-system-fusion
description: Use when the user wants world-level magic or power rules, their limits and costs, or a coherent fusion of multiple power concepts; excludes combat balance.
metadata:
  type: workflow
  family: world-bible-skills
  stage: world
compatibility: []
---

# Design: Magic System Fusion

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. A magic-system page is a core-rule type and therefore protected: this skill adds craft, not permission to edit one.

## Use when / not when
Use when: world-level power rules, their cost and limits, or the way several traditions interact need defining or checking. A mundane world can say it has no magic.
Not when: class unlocks, ability damage or combat tuning (not this library), or political licensing of power (`design-faction-culture`).

## Before you write
1. Read the magic page first, with its `Core Invariants` and every `::fact::` line on it, then the decisions that created them (an accepted decision explains why a rule exists). If a decision was replaced, follow the newer one.
2. **A task that needs the rules to be different is a protected change.** Changing the existing page, a fact line or an invariant needs the user's authorization naming the page and the change. A request such as "add a trade in X" is a test of the existing rules, not permission to alter them: if X breaks an invariant, say which one and offer what fits (for instance a version that needs no storage, or a one-off exception the user decides).
3. Search `INDEX.md` for pages that rely on the rule, since a change reaches them.
4. Fill the six axes from what the world states before interviewing. Ask only about an unresolved axis that changes the work: what does it cost, who can do it, what stops unlimited use.

## Procedure
1. Fill **Source**, **Cost** (immediate and accumulated), **Limits** (ceiling and failure), **Access**, **Physics** (what it transforms and what it never does), **Societal Integration** (infrastructure, authority, labour, taboo).
2. For a fusion, compare each tradition across the axes and build a **Unified Cost Stack**: pools, triggers, recovery, compounding, and whether one tradition can pay or evade another's cost. A bypass must be bounded and accounted for.
3. State checkable **Core Invariants** with ids, domain and any chosen exceptions. Prefer a few load-bearing rules. Test unlimited production, healing, transport, information and combined-use loopholes.
4. Trace one limit or cost into daily consequence. Keep physical ability apart from licensing, taboo and people's wrong theories.
5. Record **Deliberately Unexplained** phenomena. Source-stated unknowns stay unknown.
6. For a change to an accepted rule, list direct and reverse dependents and a migration, and hand to `design-canon-continuity`.

## Output
Use the magic page's section names:

```markdown
# <System>
## Source
## Cost
## Limits
## Access
## Physics
## Societal Integration
## Unified Cost Stack     (when several traditions)
## Core Invariants
- INV-1 <rule> | domain | exceptions: none | cannot be demonstrated: <x>
## Deliberately Unexplained
```

Include two or three worked interaction cases and label proposals.

## Worked example
Request in explore mode: "Add a way to send a spell across the strait." The magic page fixes `::reach:: 0 paces` and `INV-2: no effect beyond the caller's footing`. Report that a crossing spell breaks INV-2. Offer what fits: a relay of callers on stepping-stones (each acts at its own footing, cost paid per stone), or a courier who carries a physical token the caller charged before leaving (only if INV-3 allows storage, which it does not). Recommend the relay; propose it as a new page that cites the invariants. The magic page is unchanged. Ask the user whether they want an exception to INV-2, and wait.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Treating "add X" as permission to loosen a rule | Read the invariants; report what X breaks; offer what fits |
| Editing the magic page or a fact line without asking | Ask once with the page, the change and the dependents |
| A bypass that quietly cancels a cost | Bound it and put it in the cost stack |
| Solving a deliberate unknown for tidiness | Keep it under Deliberately Unexplained |
| Stat tables and unlock gates | Lore only |

## Acceptance
- A reader can say who can use power, what stops unlimited use, what happens near a limit and how traditions interact.
- Every example fits the invariants, or an approved exception is recorded with the user's words.
- No protected page was changed without quoted authorization.
