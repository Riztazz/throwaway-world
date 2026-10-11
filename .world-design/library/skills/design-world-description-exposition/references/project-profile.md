# Description profile (legacy convention)

Worlds made by the bootstrapper do not use this. They keep the style source in `voice.md`, role and category technique cards in `authoring/references/`, and approved exemplars next to them; the context loader resolves that chain for the describing role (`py -3 .world-design/library/tools/context.py prepare --project . --role fiction-writer`).

An older world that still has `authoring/description/profile.md` can keep it. Treat it as the first link of the chain: read its current revision, use it for the task, and say so in the notes. Do not create one in a new world, and do not copy its text between worlds.
