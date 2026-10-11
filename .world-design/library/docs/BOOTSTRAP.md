# Starting a world

```
py -3 tools/new_world.py            # opens the page in your browser
py -3 tools/new_world.py --no-browser --port 8765   # prints the link instead
```

The page runs only on this computer: it listens on `127.0.0.1` on a random port, needs a one-time token that is in the link, and can only create or update a world folder. Stop it with the Quit button or Ctrl+C. Python 3.12 or newer is the only requirement.

## New world

1. **World folder**: an empty folder, or one that does not exist yet (a `.git` folder inside is fine). The page refuses the library itself, anything containing it, relative paths and a drive root. Browse opens a folder dialog; typing the path always works.
2. **Name and id**: the name goes into the entry files; the id (lowercase letters, digits, dashes) identifies the project.
3. **What you already know**: premise and ideas, what is already decided (each line becomes an accepted decision in your words), what to leave to the agent (it proposes boldly instead of asking), the game or medium and scale, the language of the bible and of in-game text, tone, what must never appear, whether stories will be written. Rough is fine; the agent pushes back and asks about gaps.
4. **Live-game roles** (ticked by default): live events, persistent state, player societies, roadmap, and onboarding and legacy. Untick for a world that is not an online game; the five roles, their skills and agent files are then left out of the snapshot, the adapters and the manifest. The choice is stored in `.world-design/world.json` (`packs`); to add the pack later edit that list, run the update, and add the new roles to `.agents/narrative/project.json` yourself (the update never edits your manifest).
5. **References** (optional): creator and medium are required for each one you add; the work may be empty (the creator as a whole). Mark each **hard** (it must visibly shape the work; needs at least one aspect ticked; at most 3) or **soft** (may be set aside, with a one-line reason), and tick what it is wanted for (characters, dialogue, tone, ...). Edition, spoiler ceiling, a source pointer, what you want, what to avoid and your notes are optional. Nothing is opened, attached or copied: references travel into the prompt as pointers and your words.
6. **Create world**: writes the folder and shows two prompts with Copy buttons: the bootstrap prompt (saved as `BOOTSTRAP-PROMPT.md`) and the pitch prompt for later (saved as `PITCH-PROMPT.md`). The whole path is in [JUMPSTART.md](JUMPSTART.md).

## What it creates

| In the world | What it is | Edited by |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md` | `AGENTS.md` is the coordinator's guide (what is where, workflows, modes, orchestration, tools to propose) with a generated "This world" block that `canon_index.py entry` refreshes from the files; `CLAUDE.md` imports it and adds only what exists in Claude Code | the library (re-run to update; your notes outside the block are kept as long as you do not edit library text) |
| `START-HERE.md` | the one-page human guide | the library |
| `.claude/skills/start-session/`, `.agents/skills/start-session/` | the skill that makes the agent propose a task mode at the start of every conversation | the library |
| `.claude/agents/`, `.codex/agents/`, `.claude/settings.json` | the role definitions (22 core, plus the live-game roles for an online game and the game systems role for any game), the SessionStart hook (open questions plus a generated "where we left off") the lint feedback after each write (`tools/lint_feedback.py`: after an Edit or Write in `world/`, `decisions/`, `ledger/`, `drafts/stories/`, `authoring/references/` or `design/pitches/`, shows the agent the lint findings in that file and in the pages it links to or from, capped at 8, never blocking) and the `/world-mode` command (`tools/mode_hook.py`: the user types `/world-mode explore|extend|edit|lock`, a hook records it per session, and the write guard then enforces it: lock writes nothing, explore changes no existing page, extend only adds; only the user can set it; `/world-mode off` removes it) and the write guard (`tools/write_guard.py`: blocks an Edit or Write of a protected page without a T3 record that has the user's authorization words; Claude Code only) | generated; do not edit |
| `.world-design/library/` | pinned copy of the skills, roles, rules and tools | the library; do not edit |
| `.world-design/world.json`, `owned.json` | project record and the hash of every library file copied | the tool |
| `manifest.json`, `world/` | the pages STUDIO imports; starts empty | you and the agents |
| `decisions/`, `ledger/` | decisions, open questions, change records, the invention log, the baseline | you and the agents |
| `design/`, `drafts/`, `work/` | everything that is not an importable page: quests, stories, packets | you and the agents |
| `voice.md`, `authoring/references/` | the style anchor and the reference cards and exemplars | the bootstrap agent, approved by you |
| `.claude/rules/world-*.md` | the library's rules re-loaded next to the work: Claude Code loads each when a matching file is read or edited (pages, stories and series, the ledger, decisions, reference cards), also after compaction; generated from `rules/`, Claude only | the library |
| `.agents/narrative/project.json` | binds extra skills and context to roles; every installed role listed (22 core, plus 5 with the live-game pack, plus 1 with the game pack), empty to start | you |
| `.agents/narrative/policy.json` | optional: your own limits, word lists and finding levels (`docs/POLICY.md`); not created, never overwritten | you |
| `INDEX.md` | generated page index | `canon_index.py` |
| `BOOTSTRAP-PROMPT.md`, `PITCH-PROMPT.md` | the two prompts for your agent | written once |
| `design/pitches/` | the pitch rounds, kept after the choice | the agents; you choose |

Only the library-owned rows are touched by an update.

## The bootstrap prompt

Paste it into your agent with the world folder open. It tells the agent to: (1) read the entry file, the rules and the intake and give every reference a light pass (what the creator is good at, what is tied to their medium, fit); (2) **stop and send you one message and wait**: its questions in one batch, a proposed **split** (for each role, a primary reference and a blend option, with conflicts and the references it would keep as background), so you can accept, reassign, ask for a blend, or add or drop sources; (3) only then go deep on the references the approved split uses, decomposing each creator into **atoms** (one technique with its mechanism steps, a test and a confidence label) in `authoring/references/ANALYSIS.md`; (4) write the atoms as technique cards with an original sample pair each, for the eight required roles and for shared categories; (5) draft `voice.md` and propose two or three original exemplar passages for the prose roles; (6) verify with the lint and the loader. Your answers are recorded as accepted decisions with your exact words. It does not write world pages. Technique cards describe transferable techniques in their own words; they quote at most a few words and never summarize plot. Anything the agent could not read is marked unread. `PITCH-PROMPT.md` then runs the pitch rounds (core, cast, first place) into `design/pitches/`.

The instruction text of the three prompts (bootstrap, add references, pitch) lives in `templates/prompts/*.md` with `{{placeholders}}`; `tools/bootstrap/prompt.py` only fills in your words and the product-specific parts. To change what the agent is told, edit the template, then run `python -m tests.golden_prompts` from `tools/` and read the diff of `tools/tests/golden/prompts/`: those files are what the agent receives, and a test fails when they and the code disagree.

## Without the browser

```
py -3 tools/new_world.py print-template > zalesie.json     # edit it
py -3 tools/new_world.py create --from zalesie.json [--print]
```

The file has the form's fields (path, name, optional project id, the intake boxes, products, references with binding and aspects, a quick list of sources). It goes through the same `create_world`, so the world is identical to the form's and every refusal is the same message. Packs follow the products unless the file gives `packs`. For Codex users, scripts and tests.

## Adding references later

Authors and works you think of after the bootstrap: the **Add references** tab (or `py -3 tools/new_world.py add-references --world DIR --from refs.json --bulk "Creator | Work | Medium"`). The rows are validated like the form (a hard one needs an aspect; at most 3 hard in the whole world, counting the old ones; a reference already in the world is refused), appended to `.world-design/world.json`, and `ADD-REFERENCES-PROMPT.md` is written. That prompt makes the agent triage only the new references against the **approved** reference map and propose changes to the split; it never changes an approved row on its own, and sets the map back to `status: proposed` if you accept a change. `py -3 tools/new_world.py regenerate-prompts --world DIR` rewrites `BOOTSTRAP-PROMPT.md` and `PITCH-PROMPT.md` from the stored intake after you edit `world.json`.

## Update an existing world

Use the Update tab (or choose the same folder again). The tool compares each library-owned file with the version it recorded when it copied it:

- untouched files are replaced; files new in the library are added; files removed from the library are deleted if you never edited them;
- a file you edited and the library did not change is kept silently;
- a file you edited that the library also changed, a file removed from the library that you edited, and a file you deleted that the library still ships are **asked about**: keep yours (the new version is saved beside it as `<file>.new`) or use the library's;
- a world with no record is treated as unknown: every difference is a question.

Your pages, decisions, ledger, voice, references, manifest, drafts and designs are never read as library files and never changed. There is no git handling: commit before updating if you want a restore point.

## Writing records

```
py -3 .world-design/library/tools/record.py decision --type question --status open --title "Who holds the lease?" --affects gate.md --blocking
py -3 .world-design/library/tools/record.py accept D-0004 --authority "the user's exact words"
py -3 .world-design/library/tools/record.py supersede D-0004 --by D-0009
py -3 .world-design/library/tools/record.py change --mode edit --tier T2 --pages gate.md --dependents keep.md --summary "..."
```

The next free id, the frontmatter the lint expects, the inbox line for an open question and a refreshed `decisions/INDEX.md`. `accepted` and T3 need the user's exact words; the tool refuses an empty quote but cannot check that the words are theirs.

## Starting a story, a series or a system spec

```
py -3 .world-design/library/tools/new_item.py story ember-quay [--form short|novella|novel] [--series dusk --book 1]
py -3 .world-design/library/tools/new_item.py series dusk
py -3 .world-design/library/tools/new_item.py system water-draw      # game worlds only
```

Copies the world's own template, fills the frontmatter (id, title, form, created, series and book), refuses to overwrite, and prints the next steps. A novel gets `chapters.md` and `continuity.md` too.

## Bootstrap status

```
py -3 .world-design/library/tools/bootstrap_status.py [--strict]
```

Read-only. Lists the intake, decisions, the reference map status (`status:` in `authoring/references/ANALYSIS.md`), atom cards by binding, required roles without a role card, the `voice.md` status (`Status:` at the top), exemplars proposed versus approved, and pitch rounds written, then says READY or NOT READY for the pitch round and names what to approve. You approve by editing the status to `approved`. `--strict` exits 1 when not ready.

## Review page

```
py -3 tools/new_world.py --review WORLD_FOLDER
```

Opens the bootstrapper's page on the **Review** tab for that world (or open the tab and choose the folder). It shows what the agent has written and refreshes itself every two seconds while the agent works: the status lines from `bootstrap_status`, what is still to do, the reference map, `voice.md`, each exemplar, open questions from `decisions/INBOX.md`, pitch rounds, and the technique cards. A click does one of these and nothing else:

- **Send the agent** (the box at the top) always shows the one message to send next, with a Copy button: the bootstrap prompt line when nothing is written yet, "revise what I rejected" after a rejection, the pitch prompt line (in a fresh session) when everything is approved, "continue with the next round" after you picked a pitch. While you still have something to judge it says what, and shows no message.
- **Approve** or **Reject** sets the `status:` line of `authoring/references/ANALYSIS.md`, `voice.md` or one exemplar, or the `- Status:` line of one technique card (optional: cards for hard references come first and never block the pitch round; each shows its sample pair, without the technique and with it). A rejection keeps the reason in a `Review note:` line (`review_note:` inside frontmatter); `bootstrap_status` lists it, and the agent revises the file and sets it back to `proposed`. Undo returns an approved item to `proposed`.
- **Answer** or **Accept** records an open or proposed decision as `accepted` with your words (or "accepted as proposed, by a click on the review page") in `authority`, and appends your answer to the decision.
- **Record my choice** on a pitch round accepts the round's pending decision, or writes a new accepted one, naming the pitch and the options not chosen.

The page reads one world folder (it must have `.world-design/world.json`) and writes only those lines and decisions; it never touches `world/`, `manifest.json` or any other file. It needs the world's files on this computer: if the agent works elsewhere (for example in the cloud), you move the files yourself (git pull before you look, git push after you click); the page does no syncing. It uses the library's copy of the code, so a world made before this page existed shows rejections to the agent only after `new_world.py update` brings the world's `bootstrap_status.py` up to date.

## Command lines

Every tool script in `tools/` (and in a world's `.world-design/library/tools/`) is an ordinary command line: `--help` lists what it takes, a misspelt or abbreviated flag stops it with exit 2 and the usage line (nothing is written), and the world tools find the world from the current folder or any folder below it, or from `--world PATH` (given before or after the command). `canon_lint.py`, `finish_check.py` and `bootstrap_status.py` also take the folder as a positional argument. The five hook scripts read JSON on stdin and take no arguments.

## Checking a world

Besides the import and change rules, the lint warns about the bootstrap output: `L-CARD-FIELD`, `L-CARD-ID`, `L-CARD-BINDING` and `L-CARD-SAMPLE` for atom cards that miss a field or have a bad id, binding or over-long sample; `L-REF-MAP` when cards exist without `ANALYSIS.md`; `L-REF-HARD` when a hard reference has no atom; `L-PITCH-SHAPE` when a pitch round lacks pitches A to D, a recommendation or its hard-reference lines. `L-SYSTEM-NUMBERS` flags a line of a `design/systems/` spec that states a value next to a balance word (damage, cost, cooldown, drop rate, percent ...); a value the user gave goes on a `user-given:` line, and a value from a world page is allowed when the line links the page. For novels and series: `L-STORY-CHAPTER` (a chapter file without a ledger row, or a row for a missing file), `L-STORY-CONTINUITY` (a drafted chapter that set no fact in `continuity.md`, or a cited chapter that does not exist) and `L-STORY-SERIES-BOOK` (a series that lists a missing book, or a book that names the series but is not listed). `L-VOICE-STATUS`, `L-VOICE-SECTION` and `L-VOICE-EXAMPLE` check a written `voice.md` (a `Status:` line, the four sections with concrete rules, each with a worked example); `L-EXEMPLAR-HEADER` and `L-EXEMPLAR-IMITATION` check the exemplars (`status:`, `role:`, `purpose:` lines, and no source creator or work named in them). They are warnings, never import errors.

```
py -3 .world-design/library/tools/canon_lint.py        # import format and change rules
py -3 .world-design/library/tools/canon_index.py index # refresh INDEX.md
py -3 .world-design/library/tools/canon_index.py search TERM # keyword search: pages, facts, decisions, log (before inventing)
py -3 .world-design/library/tools/context.py prepare --project . --role historian
```

The lint implements the checks in [WORLD-HANDOFF.md](WORLD-HANDOFF.md) plus the mechanical rules from [rules/INVENTION.md](../rules/INVENTION.md). See [PROVIDERS.md](PROVIDERS.md) for what is and is not verified about Claude Code and Codex discovery.

## Bulk text (barks, trivia, NPC lines)

```
py -3 .world-design/library/tools/batch_draft.py plan   --role fiction-writer --requests work/barks.json
py -3 .world-design/library/tools/batch_draft.py submit --role fiction-writer --requests work/barks.json --name barks-1 --yes
py -3 .world-design/library/tools/batch_draft.py collect --name barks-1
```

For hundreds of short texts after the voice, the reference cards and the key pages are approved. It uses the Message Batches API (half the standard price, most batches done within an hour) with **your own `ANTHROPIC_API_KEY`**, which is billed; `plan` shows the size and sends nothing, and `submit` refuses without `--yes`. The requests file is a JSON list of `{"id", "prompt", "pages"}` (or a text file, one request per line). The role brief, `voice.md` and the role's reference card go in as the system prompt. Results land in `drafts/batch/<name>/` as files marked `status: proposed`, with an `INDEX.md`; nothing is written to `world/`. A batch cannot ask questions, so it is not for creative decisions. The live API path has not been run in this repository (the tests use a fake transport): try a batch of two first.
