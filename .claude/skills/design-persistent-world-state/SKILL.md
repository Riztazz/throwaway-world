---
name: design-persistent-world-state
description: Use when the user wants narrative state authority, shared consequences, personal knowledge, event transitions, concurrency, replay or continuity contracts for a persistent online world.
metadata:
  type: workflow
  family: world-bible-skills
  stage: narrative
compatibility: []
---

# Design: Persistent World State

> Binding rules live in `rules/` (modes, protected pages, decisions, page format). Ask the task mode first. This skill specifies state; it does not decide open questions, mutate databases or deploy content.

## Use when / not when
Use when: shared physical facts, personal progress and knowledge need clear scopes, a transition needs an authority and guards, or concurrency, replay and reset need a policy.
Not when: authoring rules for reactivity (`design-narrative-systems`), the event's experience (`design-live-events`), a canon revision (`design-canon-continuity`).

## Before you write
1. Read the pages for the entities the state concerns, the history ledger and `decisions/INBOX.md`.
2. **An open decision about who holds something is an open state, not a field to fill.** If the state's holder, owner or outcome is under an open decision, model it as `undecided` with the legal transitions out of it, and name the decision that blocks each one. Do not choose a holder to make the table complete, and do not write a holder into any page.
3. Read accepted decisions; a replaced one is not a source.
4. A state spec is not a page type. Save it as `design/state/<slug>.md`.
5. Ask in facts: who may cause the change, who sees it, what happens if two groups act at once, what a late joiner sees, whether it can reset.

## Procedure
1. Inventory the state: global, shard, region, group, personal, account history, knowledge, author-only plans, released canon. Use only scopes the project chose.
2. For each transition give the cause, precondition, authority, scope, resulting facts, guards and irreversible effects. Interface names are proposals unless a real interface supplies them.
3. State conflict intent: concurrent groups, duplicate signals, stale clients, order changes, partial progress. Say which outcome is authoritative and what others see. No player independently destroys the same shared thing.
4. Cover interrupted or repeated processing, reconnect and repeat participation. Idempotency and audit needs are contracts, not claims of implemented guarantees.
5. Keep replay and legacy presentation apart from present-time reversal. A recollection never repopulates a dead NPC in current canon.
6. Describe reset, recurrence and rollback only when chosen. A repeatable activity needs a diegetic reason or clear historical framing.
7. For canon revisions map the impact on completed quests, stored knowledge, NPC lines and evidence; do not rewrite player history.
8. Test on paper: two simultaneous outcomes, late joiner, returning veteran, failed event, stale quest, duplicate trigger, proposed retcon. Separate narrative decision from engineering feasibility.

## Output
```markdown
## State inventory
| state | scope | authority | possible values | blocked by (decision) |
## Transitions
| id | cause | precondition | authority | scope | result | guards | irreversible? | visible text / evidence |
## Conflict, repetition, reset
## Unresolved implementation needs
```

## Worked example
Request in explore mode: "Persistent state for who holds the Corbel ferry licence." The index shows the licence under open decision D-0007 (Harbourmaster or guild). State inventory: `licence_holder` = `undecided` (scope: shared world, authority: the content owner after D-0007 closes). Transitions: undecided -> harbourmaster or undecided -> guild, both blocked by D-0007; each result changes the toll office text and the quest giver's lines. Conflict: two groups pushing at once yields no change until the decision exists. No holder is written to any page.

## Common mistakes
| Mistake | Do this instead |
|---|---|
| Filling a holder field because the table looks incomplete | Model `undecided` and name the blocking decision |
| Per-player shared outcomes | One authoritative scoped result |
| Replay that revives the dead | Present it as history |
| Claiming idempotency is implemented | State it as a contract |
| Mixing knowledge and physical change | Separate domains |

## Acceptance
- A physical event has one authoritative scoped result; players may differ in knowledge and participation without incompatible world facts.
- Open decisions appear as undecided states with named blockers.
- Edge cases and unverified guarantees are explicit.
