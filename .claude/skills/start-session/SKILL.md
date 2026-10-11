---
name: start-session
description: Use at the start of every conversation in this world, and whenever the work changes kind (brainstorming to editing, writing to reviewing), before any narrative, page, story, decision or review task. Reads the world's facts and open questions, tells the user where things stand, proposes a task mode with a reason, and says how to make it binding.
---

# Start of a session

Do this before the first piece of world work, once per conversation, and again when the kind of work changes.

## 1. Look (silently, in this order)

- The "This world" block in `AGENTS.md`, then `decisions/INBOX.md`, then `ledger/last-session.md` if it exists.
- If the facts say the bootstrap is not ready, run `bootstrap_status.py` and offer to continue it (`BOOTSTRAP-PROMPT.md`) before anything else.

## 2. Say where things stand (two or three lines)

What the world is, how many questions wait for the user, what is waiting for their approval. Lead with that. Do not repeat their request back.

## 3. Propose the mode

Pick from what they asked for, say why in one line, and offer the others:

| They want | Propose | Because |
|---|---|---|
| ideas, pitches, "what if", options to compare, a new direction | `explore` | nothing existing changes; proposals go to `design/` and `drafts/` |
| a new page, story or region; filling a thin page | `extend` | additions only; every original line survives |
| fixing, rewriting or revising what exists | `edit` | existing pages change, each with a change record; protected pages need their yes |
| an audit, a review, a question, a status report, "just tell me" | `lock` | read-only; nothing is written |
| not clear | `explore` | the safest mode that still produces work |

Ask it as a multiple-choice question with your recommendation first (use your client's structured question tool if it has one, otherwise a short numbered list). Their answer in chat is valid.

If they already named a mode, confirm it in one line and do not ask again. If the status line or the SessionStart context shows a `/world-mode` is already set, use it.

## 4. Tell them how to make it binding

In Claude Code the user can type `/world-mode <mode>` (and `/world-mode off`): a guard then blocks the writes that mode forbids and the status line shows it. **You cannot set it and must not look for a way around it.** In Codex there is no guard: say that you will follow the mode by instruction. Mention this once, briefly, at the start; do not nag.

## 5. Propose what fits (only what fits, one line each)

- A read-only second opinion: `canon_index.py review-packet`.
- Bulk text after the voice and key pages are approved: `batch_draft.py`.
- Reference research on a hard reference: a deep-research pass with the user's own research tool, the report saved to `authoring/references/research/<creator-slug>.md`.
- Before handing work back: `finish_check.py`.
- First session after the bootstrap is approved and no `project` decision about orchestration exists: ask the orchestration questions listed in `AGENTS.md` ("Orchestration"), record each answer as a decision, then go on.

## 6. When the work changes kind

If a request would cross the mode (for example changing an existing page while in `explore`), stop, say which mode it needs, and ask. Do not do the part you can and quietly skip the rest.
