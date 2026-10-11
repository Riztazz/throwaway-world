# Narrative agents

The provider-independent source for **28 roles backed by 34 skills**. It holds prompts and work contracts, not a running service.

- [ORCHESTRATION.md](ORCHESTRATION.md): how to route a request, gather your input, delegate and resume.
- [task-packet.md](task-packet.md): copyable task, result, checkpoint and canon-change templates.
- [PROJECT-SKILLS.md](PROJECT-SKILLS.md): how a world adds skills, context and references to the base roles; the loader and the reference chain.
- [registry.json](registry.json): stable role IDs, routing descriptions, modes and skill ownership.
- [reference-categories.json](reference-categories.json): which roles read which reference categories, and the nine roles that need references.
- [contract.md](contract.md): shared behavior embedded in every native definition.
- [roles/](roles/): responsibility, triggers, inputs, deliverable, boundaries and handoffs per role.
- [rules/](../rules/): the invention, decision and page rules every role follows.
- [Skills guide](../docs/NARRATIVE-SKILLS.md): the full skill mapping.

Edit the shared files here, then regenerate and check:

```
py -3 tools/sync.py --write
py -3 tools/check.py
```

Codex adapters are generated at `.codex/agents/narrative-*.toml`, but a live probe (2026-10-10, `docs/PROVIDERS.md`) found that Codex's sub-agent tool cannot start a role by name, so in Codex the coordinator passes the role brief and skill text (the `context.py prepare` packet) instead; Claude Code uses `.claude/agents/narrative-*.md`. Do not edit generated files. The check detects missing skill ownership, adapter drift and collisions with hand-written files; `--write` regenerates adapters and never silently deletes stale ones.

Root `AGENTS.md` and `CLAUDE.md` are entry instructions for working on this library. A world project gets its own generated copies from the bootstrapper.
