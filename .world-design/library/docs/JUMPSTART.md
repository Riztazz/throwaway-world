# Jumpstart: from an empty folder to a chosen core

Short version, one page: [START-HERE.md](START-HERE.md).

This is the whole path for a new world, in order. You do not need to be a writer. Your job is to **judge**: the agents bring the ideas, you accept, merge or reject them. Everything below is built so that sparse input still gives good proposals, and so that nothing becomes canon until you say so.

```
1. Fill one form          (5 to 10 minutes)      tools/new_world.py
2. Paste prompt 1         (agent works, you answer one batch of questions)   BOOTSTRAP-PROMPT.md
3. Approve the reference map and voice.md        (you read two files)
4. Paste prompt 2 in a fresh session             PITCH-PROMPT.md
5. Choose from pitches: core, then cast, then first place
6. Design the chosen core, one small scope at a time
```

## 1. The form

```
py -3 tools/new_world.py
```

One page, several boxes, no wizard. Fill what you have; leave the rest empty. The boxes that matter most:

| Box | What to put | Why it exists |
|---|---|---|
| **This world is for** | Tick what you will make in it: online game, single-player game, short stories, novel or series. Several are fine (a game and its own fiction); worlds never share anything with each other. | The prompts, required roles, exemplar types and pitch rounds adapt to it. Online game brings the live-world roles; any game brings the game systems role. |
| **Premise and ideas** | One paragraph. "A persistent online RPG in a small Polish village, fantasy mixed in." | The seed. Rough is fine. |
| **Already decided** | One line per thing you are sure of. | Each line becomes a recorded decision in your own words and cannot be changed without you. |
| **Leave to the agent** | One line per thing you want to be surprised by: "the central conflict", "who the factions are". | This is your permission to be bold. The agent proposes instead of asking you to invent. |
| **Scale of the first part** | "One village and its surroundings first." | Keeps the first pitches small enough to judge. |
| **Language** | "Bible in English, in-game text in Polish." | Names, tone and every later page depend on it. Decide it now. |
| **Tone, audience and rating** | A few words; "adults, PEGI 16, no sexual content". | The rating sets the level of violence, sex and language in everything. |
| **Must never appear** | Three items, even if you only have three. | The cheapest way to stop generic output is a hard "never", not more ideas. |

Ticks reveal at most one or two fields (who the player plays, the length of the fiction, what to start with). The craft questions (point of view, tense, progression shape, how a series is structured) come from the agent as multiple-choice questions with a recommendation, which is where a non-writer does best.

**What the library writes for a game.** Lore, quests, NPCs, magic and also **mechanics as prose specs** (loops, resources and flows, rules with edge cases, the shape of progression) under `design/systems/`, by the game systems role. It never states balance numbers; it names the tuning parameters and what each trades off, and you or your engine team set the values. Those files are not imported by STUDIO.

**What the library writes for fiction.** Short stories, novellas and novels under `drafts/stories/`, with a chapter ledger and a continuity ledger per act for novels, and `drafts/series/` for a series (what readers know at the end of each book, standing facts, state carried between books).


### References: hard and soft

Add as many as you like. Each one has:

- **A quick list for many sources.** Under the references there is a box for one source per line (`Creator | Work | Medium`, or just a name). They are soft with no aspects, which means "agent decides". Use it for the fifteen.
- **Creator, work, medium.** The work can stay empty: then the reference is the creator as a whole (an author, a studio). The agent picks up to two representative works, says which it could actually read, and marks the rest `not read`.
- **How binding.**
  - **Hard**: "I want this." Its named aspects must visibly shape the reference cards, `voice.md`, the exemplars and every pitch. The agent records it as a decision in your words and may not drop it silently. At most three hard references: if everything is a must, nothing is.
  - **Soft**: inspiration. The agent uses it where it fits and may set it aside, but must say so in one line with the reason. Ignored is allowed; ignored silently is not.
- **Wanted for.** Tick the aspects: characters, dialogue, world and history, cultures and factions, magic, creatures, tone, humor and irony, plot and structure, prose style, quests and game systems. **A hard reference needs at least one aspect**; a hard "I want Sapkowski" with no aspect cannot be honored or checked.
- Optional: edition, spoiler ceiling, a pointer (a URL or a path, never opened for you), what you want from it, what to avoid, your notes.

Both kinds bind **technique and effect only**. A hard reference never licenses names, scenes, plot order or signature phrasing. "100%" means the technique must show up and cannot be overridden by the agent, not that the text is copied.

#### Example: a small Polish village, fantasy mixed in

| Field | Entry |
|---|---|
| Premise | A persistent online RPG set in a small Polish village, with fantasy mixed into everyday rural life. |
| Already decided | The first region is the village and what an hour's walk reaches. |
| Leave to the agent | The central conflict. The main factions. What the fantasy is, and where it comes from. |
| Language | Bible in English, in-game text in Polish. |
| Never | No chosen-one plot. No hard instances. No modern weapons. |
| Reference 1 | Jarosław Grzędowicz, Book, work empty. **Hard**. Wanted for: characters. |
| Reference 2 | Andrzej Sapkowski, Book, work empty. **Soft**. Wanted for: dialogue, humor and irony. Soft keeps the agent free to set him aside where his irony fights the tone you want, and it must say so each time. |

## 2. Prompt 1: the bootstrap

The form shows two prompts. Paste the first into Claude Code or Codex with the world folder open (it is also saved as `BOOTSTRAP-PROMPT.md`). The agent:

1. **Triages every reference.** A light pass over all of them (what the creator does best, what is tied to their medium, how it fits). Give it fifteen sources if you have them: you do not rank or assign, the agent does.
2. **Stops and proposes the split**, in one message, and waits. The message holds its questions in one batch (pillars, first-region scale, language, anything a role would need), where your input contradicts itself or promises too much, and the **split**: for each role a **primary** reference and a **blend option** (a second or third reference contributing named strengths, how they combine, which wins on a conflict), the references it would keep as background or drop from deep work, and the conflicts with two ways to settle each. Every hard reference must govern at least one role. You answer in your own words: "yes, Erikson for the world-builder, but blend in X", "swap these two", "drop that one". Each answer is recorded as a decision in your words.
3. **Decomposes the approved references into atoms**, in `authoring/references/ANALYSIS.md`: one transferable technique each, the steps by which the writing produces the effect, a test an editor can run on a draft, and a confidence label. Only the references the approved split uses get this depth. It does not write "be X" and does not adopt a persona; the atoms are what gets applied.
4. **Writes the atoms as cards** per role and category, hard references first, and drafts `voice.md` plus two or three original exemplar passages. Each card has a **sample pair**: the same moment in your world written plainly and then with the technique, original and in your chosen language, so the agent (and you) can see the effect. A role loads only the atoms the map gave it, not a whole author.
5. **Verifies** with the lint and the role loader, and reports.

It writes no world pages. The one place it waits is step 2; the map, `voice.md`, the exemplars and the sample pairs are marked `proposed` and you approve them by changing the status. Read the split first: it is the one place where a wrong guess would steer everything after it. At any time, `py -3 .world-design/library/tools/bootstrap_status.py` lists what the bootstrap wrote and what still waits for your approval (the map, `voice.md`, the exemplars), and says whether the pitch round may start; the pitch prompt runs it first and stops if the base is not approved.

**Why atoms and samples rather than "write like X".** A persona prompt invites pastiche of whatever the model remembers of an author. Atoms with a test are applied deliberately and an editor role can audit a draft against them. Samples are written fresh for your world, never excerpts. How well an atom is known depends on what the agent actually read: excerpts or titles you supply raise its confidence, and anything it only knows from secondary sources or memory is labelled so.

**What to expect from the pushback.** Two real examples of what the analysis should raise, as hypotheses the agent must verify and label, not as facts: Sapkowski is usually read as ironic and deconstructive, working through dialogue; Grzędowicz as earnest and immersive, working through a protagonist's interiority. If both are hard on "tone", they pull apart, and the agent should propose a split (one governs dialogue, the other characters) and ask you. Likewise an MMORPG is shared and persistent, so techniques that depend on a single protagonist's interior view may not carry over without redesign.

**Research honesty.** A web fetch gives the agent a model-made summary of a page, not the page, and for novels, manga and anime the sources are mostly wikis, reviews and essays. So every card says what kind of source it rests on (the work, an excerpt you supplied, or secondary commentary), how it was read, and never cites a chapter or page that came only from commentary. For a **hard** reference the agent offers you a deep-research pass (in Claude Code, `/deep-research What is <creator> known to do well in <aspect>, with examples?`); its report is saved under `authoring/references/research/` and cited as secondary commentary. A short excerpt you paste in beats any of it.

**Cost.** The research is the expensive part. Use the standard model tier for the bootstrap and keep the reference count to what you will actually use.

## 3. Prompt 2: the pitch round

Start a **fresh session** with the world folder open and paste the second prompt (`PITCH-PROMPT.md`). It carries none of your text; it makes the agent read the intake, your decisions, the approved map and `voice.md` from the files, so a fresh session loses nothing and the context stays small.

Rounds, one at a time:

1. **Core**: the central pressure of the world and the one or two core systems the experience stands on.
2. **Cast**: six to eight character seeds across the pressures the core created.
3. **First place**: the region the first pages describe, with its scale and edges.

Each round is a file in `design/pitches/` with **three materially different pitches** and a **fourth, riskier wild card**. Every pitch has the same shape, so you can compare them: name and hook, what a person does and risks, why it differs, one line per **hard** reference on how it shows (or that it cannot), one line per **soft** reference on whether it was used, how it fits your decisions and exclusions, what you give up, what it unlocks. The file ends with the agent's recommendation and what it would not choose.

You answer by:

- picking one;
- merging ("A, but with B's cost"): the agent states the seams before recording it;
- rejecting all and asking for another round;
- or saying what you dislike about each: that is as useful as a pick.

The choice is recorded as an accepted decision in your words. Rejected options are recorded as rejected, so they are not pitched again.

## 4. After a pick: design in small scopes

1. The agent asks the **task mode** (explore, extend, edit, lock; `rules/INVENTION.md`). Explore for ideas, extend for adding, edit for changing, lock for read-only questions.
2. Order: the `tone-premise` page, then the rule pages the core needs, then the cast, then the first place. One bounded scope at a time, each with a short proposal before any page.
3. Core-rule pages and accepted pages are **protected**. The agent drafts and shows them; it changes one only after you authorize it, and the write guard blocks it otherwise.
4. After each write the lint runs and the agent sees its own errors. For a bigger change you can ask for a **reviewer pass**: a read-only agent checks the change against the fact lines and accepted decisions and answers a fixed checklist. It is off by default; the agent asks per task.
5. At a checkpoint you approve, run `canon_index.py snapshot`. It also spends the T3 authorizations written so far: a later change to a protected page needs a new question and a new record. The next session starts from a generated "where we left off" summary (`ledger/last-session.md`), so nothing unintegrated is redone or contradicted.

## What a world folder gives you out of the box

- A **worldbuilding output style** is the default in Claude Code inside the world (`.claude/output-styles/world-coordinator.md`): the main chat acts as a collaborator who brings concrete options, pushes back and protects canon, not as a software assistant. Do not switch a world to the built-in "Proactive" style: it assumes instead of asking, which fights the rules here.
- **Reasoning effort per role** is set in the generated agent files (strong roles and magic rules high, the rest inherit the session). Change it per world in `.agents/narrative/models.json` (`effort`).
- **`/world-mode explore|extend|edit|lock`** (Claude Code) sets the task mode for the session and the write guard enforces it: lock writes nothing, explore changes no existing page, extend only adds, edit changes pages with a record. Only you can set it; the agent cannot. `/world-mode off` removes it (a new session also starts with none). Answering the mode question in plain words still works but is not enforced.
- A **status line** shows the world's name, the current `/world-mode` mode and the number of open decisions (turn it off by overriding `statusLine` in `.claude/settings.local.json`).
- A **write guard** blocks edits to protected pages without your authorization, **lint feedback** shows the agent its own errors right after a write, a **reviewer pass** (ask per task) checks a bigger change against fact lines and decisions, and a generated **where we left off** summary starts every session.
- **Bulk text** (hundreds of barks or NPC lines) can go through `batch_draft.py` at half price once the voice and cards are approved; see [BOOTSTRAP.md](BOOTSTRAP.md). It needs your own API key and returns proposals only.
- If your Claude Code has `/voice`, dictating the premise and the "Leave to the agent" box is often richer than typing.

## Rules of thumb

- **Constraints beat ideas.** If the first pitches feel generic, add a "never" and a hard aspect; do not write more premise.
- **Do not give the agent your own invention to polish.** Give it a gap and let it pitch three.
- **Do not skip the map.** Everything downstream reads it.
- **Let the agent disagree with you.** If it never pushes back on your input, the prompt is not doing its job; say "challenge this".
- **A new session is fine.** The files carry the state, not the chat.

## Updating a world later

When the library changes, use the Update tab of `tools/new_world.py` (details: [BOOTSTRAP.md](BOOTSTRAP.md)). Your pages, decisions, voice, references and pitches are never touched.
