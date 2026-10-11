status: approved

# Reference analysis and reference map: Test World

The user approves this file by changing the first line to `status: approved`. Until then the split below is a proposal. Two things in it were not answered by the user and are marked **proposed settlement**: the role split itself and the three conflicts.

Decisions behind it: D-0001 (original world, technique only), D-0003 (Grzędowicz is hard), D-0012 (Miéville is soft), D-0007 (spoiler ceiling: "everything I have read"; the volumes were not named, so the cards stay at premise level), D-0008 (English samples).

## 1. What was read, and how (read this first)

| Reference | Binding | What I actually had | Not read |
|---|---|---|---|
| *Pan Lodowego Ogrodu*, Jarosław Grzędowicz (4 volumes, Fabryka Słów) | hard | Search results only: publisher blurbs, reader and critic reviews, Wikipedia and SF Encyclopedia snippets. This is a **fetched summary**, not the text. Plus memory. | The text of every volume. No edition, no locator. No excerpt supplied. |
| *The City & The City*, China Miéville | soft | Memory only. A web fetch was attempted and failed, no search was made. | The text. |

Consequence: every atom below is `secondary` or `memory`, confidence **low**, and no card cites a chapter, page or timecode. Nothing is described as read. To raise confidence the user can supply: for the hard reference, one or two pages of Polish dialogue and one or two of description (this matters most for the dialogue and prose atoms); a deep-research report saved to `authoring/references/research/jaroslaw-grzedowicz.md` (secondary commentary); for the soft one, an excerpt or the edition.

## 2. Triage

| Reference | Verdict | Reason |
|---|---|---|
| Grzędowicz | keep, deep | Hard. Governs every role. |
| Miéville | keep, deep (light) | Soft, chosen by the user for rules, institutions and restraint. Used in 6 of 8 roles. |
| Others | none supplied | |

## 3. Reference map (proposed)

| Role | Primary (hard) | Blend (soft) | Atoms | How they combine; who wins | Not taken |
|---|---|---|---|---|---|
| world-director | Grzędowicz | + Miéville | grzedowicz.world.1, .world.2, .magic.1, .tone.1; mieville.rules.1, .institution.1, .tone.1 | Grzędowicz = how the world is met; Miéville = register and how rules and offices appear. Miéville wins on register. | spectacle; mission-of-destiny |
| historian | Grzędowicz | + Miéville | grzedowicz.history.1, .world.3; mieville.rules.1 | Miéville = order (habit first, reason later); Grzędowicz = layering. Miéville wins on order. | epic chronicle; one secret history |
| culture-builder | Grzędowicz | + Miéville | grzedowicz.world.2, .history.1; mieville.rules.1, .institution.1 | Grzędowicz = content of customs; Miéville = how they are shown. | real-religion models; one-to-one allegory |
| magic-fusion | Grzędowicz | + Miéville | grzedowicz.magic.1; mieville.institution.1 | Grzędowicz = how a power shows; Miéville = the office around it. | visible spectacle; plot-solving power |
| fiction-writer | Grzędowicz | + Miéville | grzedowicz.world.1, .world.3, .tone.1, .prose.1, .dialogue.1, .dialogue.2; mieville.rules.1, .rules.2, .tone.1 | Grzędowicz = scene shape and speech; Miéville = register; the intake's exclusions beat both. Miéville wins on register. | painterly density; all-knowing narrator |
| narrative-editor | Grzędowicz | + Miéville | grzedowicz.tone.1, .prose.1, .dialogue.1; mieville.tone.1 | The editor runs each card's Test; no rewriting toward an author. | editing toward imitation |
| character-designer | Grzędowicz | none | grzedowicz.history.1, .dialogue.1, .dialogue.2 | single reference | chosen-one characters |
| quest-narrative-designer | Grzędowicz | + Miéville | grzedowicz.world.1, .dialogue.1, .dialogue.2; mieville.rules.2 | Miéville = quest shape (case, ruling, consequence); Grzędowicz = lines. | long speeches; rewards; balance numbers |

Coverage check for the hard reference. Its wanted aspects and where they land:

| Aspect wanted (intake) | Atoms | Roles |
|---|---|---|
| Dialogue and voice | grzedowicz.dialogue.1, .dialogue.2 | character-designer, quest-narrative-designer, fiction-writer, narrative-editor |
| World, history and places | grzedowicz.world.1, .world.2, .world.3, .history.1 | world-director, historian, culture-builder, fiction-writer |
| Magic and powers | grzedowicz.magic.1 | magic-fusion, world-director |
| Tone and atmosphere | grzedowicz.tone.1 | world-director, fiction-writer, narrative-editor |
| Prose style | grzedowicz.prose.1 | fiction-writer, narrative-editor |

Roles with no card of their own (geographer-ecologist, location-designer, faction-designer, economy-designer and the rest) inherit the category cards and `voice.md`. No reference was invented for them.

## 4. Conflicts (proposed settlements; the user did not answer these)

| | Conflict | Settlement proposed | Cost |
|---|---|---|---|
| A | Intake wants factual, restrained prose and practical consequence over spectacle. Reviewers describe the hard reference as rich, painterly and in places psychedelic. | Take effects and methods, not register. Where they clash, the intake's tone and Miéville's flat register win. The painterly register is not taken. | The prose atoms stay thin (one comparison per paragraph, one mood detail per scene) until an excerpt raises confidence. |
| B | Intake: fantasy "in the background". In the hard reference, magic is foreground. | Take only the cost-and-consequence atom (grzedowicz.magic.1). Power shows as a list entry, a price or a refusal. | The magic role has one hard atom; the rest is for the pitch round. |
| C | The hard reference's hero is an outsider on a mission (an Earth operative sent to another planet, from the summaries). The intake excludes a chosen-one plot and the player is a local newcomer. | Take only the decoding-a-new-place effect (grzedowicz.world.1). Not the mission, not the outsider's special status. Each pitch states how it avoids the mission shape. | A local novice has less distance than an outsider, so the cost of each fact must be shown through work, not through strangeness. |

## 5. Reference: Pan Lodowego Ogrodu (Jarosław Grzędowicz): HARD

Evidence: secondary summaries and memory. Confidence: low. Spoiler ceiling: premise level. No plot after the premise is used anywhere.

- **Strengths (as reported):** a secondary planet built as a mirror of Earth's societies and religions, which lets the reader judge it; two narrative levels followed in parallel; technology colliding with older magic with consequences; characters praised as well written.
- **Limits and medium dependence:** a very long single novel (about 2,500 pages over four volumes, per the SF Encyclopedia), so its slow reveals do not fit a 3000 to 6000 word story or a one-line game bark without compression. No English translation, so the English-language reviews are thin. One critic reports an inconsistent mood and, in places, muddled style.
- **Fit for this world:** high for method (a decoder at the threshold, a bent familiar institution, power as cost); medium for scale; low to medium for register.
- **Take:** the decoding effect, the bent institution, the two-scale scene, custom outliving reason, magic as consequence, one material detail for mood, comparisons from the trade, the dodging answer, understatement.
- **Leave:** lush description, the mission-of-destiny arc, gods' war scale, any name, scene, gear or phrasing of the source.

### Atoms (9)

| Id | Aspect | Atom | Source type | Confidence |
|---|---|---|---|---|
| grzedowicz.world.1 | world | Decoder at the threshold: facts are paid for | secondary (premise) + memory | low |
| grzedowicz.world.2 | world | Familiar institution, one element bent | secondary (reading as a mirror of Earth) | low |
| grzedowicz.world.3 | world | Two scales in one scene | secondary ("two levels") | low |
| grzedowicz.history.1 | history | Practice outlives its reason | memory + premise fit | low |
| grzedowicz.magic.1 | magic | The marvel as a line item | secondary (technology meets magic) + the intake's "background" | low |
| grzedowicz.tone.1 | tone | One material detail carries the mood | secondary ("painterly"), restricted by the intake | low |
| grzedowicz.prose.1 | prose | Comparison from the trade | secondary ("painterly"), restricted by the intake | low |
| grzedowicz.dialogue.1 | dialogue | The dodge carries the information | memory; weakly evidenced | low |
| grzedowicz.dialogue.2 | dialogue | Understatement under pressure | memory + the intake's tone line | very low |

The cards (with sample pairs) are in `roles/` and `categories/`. The two dialogue atoms and the prose atom are the ones most likely to change once an excerpt is available.

## 6. Reference: The City & The City (China Miéville): SOFT

Evidence: memory only. Confidence: low. Spoiler ceiling: premise level.

- **Strengths (recalled):** a rule that governs what citizens may notice, obeyed through habit; procedural, case-by-case storytelling; an enforcing body met through its marks; a flat register for extraordinary conditions.
- **Limits and medium dependence:** its central conceit is a single spectacular premise held for a whole novel; in this world the conceit is not taken, only the manner of presenting rules.
- **Fit:** medium to high for rules, institutions and restraint; none for magic.
- **Take:** habit-before-explanation, case against rule, the office known by its marks, flat register.
- **Leave:** the central conceit, any enforcing body, name, term or noir voice of the source.

### Atoms (4)

| Id | Aspect | Atom | Source type | Confidence |
|---|---|---|---|---|
| mieville.rules.1 | rules | The rule is lived before it is explained | memory | low |
| mieville.rules.2 | rules | Case against rule | memory | low |
| mieville.institution.1 | institution | The office known by its marks | memory | low |
| mieville.tone.1 | tone | Flat register for large facts | memory | low |

## 7. Blends: the seam

| Blend | Layers | Wins on conflict |
|---|---|---|
| Structure + texture (world-director, historian, culture-builder) | Grzędowicz supplies how the world is discovered; Miéville supplies how rules and offices look when they are met | Miéville on register |
| Scene + register (fiction-writer, narrative-editor) | Grzędowicz supplies scene shape and speech; Miéville supplies the flat register | Miéville on register, the intake's exclusions on anything |
| Quest + line (quest-narrative-designer) | Miéville supplies the shape (case, ruling, consequence); Grzędowicz supplies the lines | Miéville on structure |

## 8. Soft-reference rule

Miéville is soft. Where a piece of work leaves one of his atoms out, it says so in one line.
