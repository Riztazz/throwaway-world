# Decision log rules

Decisions are how a world remembers what was chosen, by whom, and what it replaced. They are plain files, readable by any provider, loaded at session start through `decisions/INBOX.md`.

## Where

- One file per decision: `decisions/D-0001-short-slug.md` (template: `templates/world/decisions/_template.md`).
- `decisions/INBOX.md`: the open questions waiting for the user. Keep it short; it is injected into every session.
- `decisions/INDEX.md`: generated list of all decisions with status and the pages each affects.

## What counts as a decision

| `type` | Example |
|---|---|
| `creative` | "Magic costs memory, not blood." |
| `project` | "No hard instances in this game." |
| `question` | An open item the user has not answered yet. |

## Status and authority

| `status` | Meaning | Who sets it |
|---|---|---|
| `open` | Question waiting for the user. | Any agent. |
| `proposed` | An agent's suggestion. Not a decision yet. | Any agent. |
| `accepted` | The user chose it. | **Only the user.** An agent records it from the user's own words and copies the exact quote into `authority`. |
| `superseded` | Replaced by a later decision (`superseded_by`). | The agent recording the new decision, from the user's instruction. |
| `rejected` | The user declined it. | The agent recording it, from the user's words. |

A decision with `authority` empty cannot be `accepted`.

## When to pick decisions up and put them down

1. **Before work:** read `decisions/INBOX.md`, then the decisions whose `affects` lists the pages you will touch (the index tool lists them).
2. **If the user states a rule or choice in chat:** record it as `accepted` in the same turn, with the verbatim quote. If it replaces an earlier one, set the old one `superseded` and link both ways.
3. **If you make a creative or structural proposal the user has not confirmed:** record it as `proposed`, never as `accepted`.
4. **If you are blocked by a missing answer:** create an `open` decision with `blocking: true`, list `affects`, add one line to `INBOX.md`, and continue only with work that does not depend on it.
5. **After the user answers:** convert the open item to `accepted`, remove it from the inbox, and note which pages need revisiting.
6. **Never delete a decision.** Supersede it.
