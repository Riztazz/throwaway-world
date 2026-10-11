# Project skills, context and references

The library owns reusable base roles and skills. A world adds its own skills, context and references on top. The registry (`agents/registry.json`) never changes per world; the world's manifest only adds.

## What a role receives

For one task the loader builds a packet in this order:

1. the world's manifest, the library registry, the shared contract, the role brief and the role's base skills (library);
2. the project skills and context files the manifest binds to the role (world);
3. the role's **reference chain**: `authoring/references/roles/<role-id>.md`, then `authoring/references/categories/<category-id>.md` for every category that lists the role (`agents/reference-categories.json`), then `voice.md`.

A role with no file of its own inherits its categories and the voice. Eight roles should not be considered configured without at least one reference level plus `voice.md`: world-director, fiction-writer, narrative-editor, historian, culture-builder, character-designer, quest-narrative-designer, magic-fusion. The packet's `references` block reports which levels exist and which are missing; `--strict` turns a missing required configuration into an error.

## The manifest

`.agents/narrative/project.json` belongs to the world:

```json
{ "version": 1, "projectId": "dusk-harbour", "revision": "1",
  "roles": { "historian": { "requiredSkills": [".agents/narrative/skills/layered/SKILL.md"], "requiredContext": [] } } }
```

- Every role is listed. A role that needs only its base has empty arrays; an unlisted role needs configuration and the loader refuses it. The bootstrapper writes every role of the chosen packs (27, or 22 without the live-game pack) with empty arrays.
- `requiredSkills` are `SKILL.md` files under `.agents/narrative/skills/<name>/`. `requiredContext` are other `.md` files in the world. A file cannot be both.
- Paths are portable (no absolute paths, `..`, backslashes), at most 32 per list, at most 128 KiB per file, at most 64 files and 256 KiB per packet.
- Project skills supplement the base. They cannot grant permissions or change a role's ownership.

## Running the loader

```
py -3 .world-design/library/tools/context.py prepare --project . --role historian > work/historian-context.json
py -3 .world-design/library/tools/context.py verify  --project . --packet work/historian-context.json
```

Inside the library itself use `py -3 tools/context.py ...` with `--library .`. The loader is read-only and launches no model. Hashes are computed on LF-normalized text, so a CRLF checkout is not a change. `verify` rejects missing or altered inputs and a packet whose reference configuration changed; it proves the inputs are fresh, not that the prose follows them.

## Changing a project default

Edit the file, record the user's decision (`rules/DECISIONS.md`), and bump the manifest `revision` in the same change. A task-specific exception stays in that task's packet. Superseded choices stay in the decision log. Never edit generated files under `.claude/agents/` or `.codex/agents/`.

## Examples

`examples/layered-world/` (a real bootstrapped world) shows two project skills bound to roles, reference cards, a voice and a proposed decision. It is an example, not a default, and its Erikson-informed techniques are an original adaptation of high-level choices, not an imitation of any author.
