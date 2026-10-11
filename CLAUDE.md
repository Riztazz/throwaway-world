@AGENTS.md

## Claude Code in this world

What exists here only for Claude Code (Codex has none of it, so `AGENTS.md` does not rely on it):

- **Hooks** (`.claude/settings.json`): a SessionStart hook injects the open questions and the generated "where we left off" summary; a write guard blocks edits to protected pages without a T3 record and enforces the session's `/world-mode`; a lint-feedback hook shows the findings for the file you just wrote, in the same turn. Fix errors it reports now. If a hook blocks a write, do not look for a way around it: tell the user.
- **`/world-mode explore|extend|edit|lock|off`** is the user's command. You cannot run it and the guard refuses any write to `.world-design/state/`. When you recommend a mode, tell the user they can type it. The status line shows the mode and the open questions.
- **Output style** `world-coordinator` is the default here: bring options, push back, short answers.
- **Path-scoped rules** (`.claude/rules/world-*.md`) load when you read or write the matching folders; they repeat the rules for that kind of file.
- **Roles** are subagents in `.claude/agents/` (generated; do not edit), started by name with their skills preloaded. Each runs at its own model tier and effort (`.agents/narrative/models.json`).
- **Skills** are in `.claude/skills/` and load on demand (`start-session` fires at the start of a conversation and proposes the mode); the multiple-choice question tool is yours to use for choices.
