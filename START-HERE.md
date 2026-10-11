# Start here

One page. Do one step at a time. You judge, the agent invents.

## Make a world (once)

1. **Run** `py -3 tools/new_world.py` in the library folder. A page opens in your browser (it runs only on your PC).
2. **Fill it** (rough is fine): name, your ideas, what it is for (game, stories, both). Add references if you have any:
   - **hard** = must show (max 3). **soft** = inspiration.
   - Pasting 15 titles? Use the list box. The agent picks who fits what.
3. **Pick an empty folder**, press Create. The page then shows your first prompt with a **Copy prompt** button (the same text is saved in the folder as `BOOTSTRAP-PROMPT.md`). Open the folder in Claude Code or Codex.
4. **Paste:** `Read BOOTSTRAP-PROMPT.md in this folder and follow it.`
5. **Answer its one message.** It proposes which reference serves which part. Say yes, no or "mix". Your own words are fine.
6. **Approve three things** (or tell the agent "run bootstrap_status" to see what is left):
   - `authoring/references/ANALYSIS.md`: set `status: approved`
   - `voice.md`: set `Status: approved`
   - one file in `authoring/references/exemplars/`: `status: approved`
7. **New session. Paste:** `Read PITCH-PROMPT.md in this folder and follow it.` Pick A, B, C, D or "A but with B's cost". Three rounds: core, cast, first place.

## What you get in the folder

```
AGENTS.md  CLAUDE.md   what the agent reads first
START-HERE.md          this page
BOOTSTRAP-PROMPT.md    step 4        PITCH-PROMPT.md   step 7
world/ manifest.json   the pages (what STUDIO imports)
decisions/ ledger/     what was decided and changed
voice.md  authoring/   style and reference cards
design/ drafts/ work/  pitches, stories, scratch
.world-design/library/ the rules (rules/), skills, tools, docs
.claude/ .codex/ .agents/  generated agents and hooks
```

The rules the agent follows are in `.world-design/library/rules/` (a dot-folder: turn on hidden items in Explorer). Do not edit it; the library updates it.

## Every work session

1. Open the folder. Tell the agent what you want.
2. It asks the **mode**. Pick one:

| Say | Means | Use for |
|---|---|---|
| `explore` | ideas only, nothing existing changes | pitching, "what if" |
| `extend` | add only, never cut | filling gaps |
| `edit` | change things, on the record | fixing, rewriting |
| `lock` | read only | audits, "just tell me" |

3. **Make it binding** (Claude Code): type `/world-mode edit` (or another). `/world-mode off` clears it.
4. Answer its questions. They are multiple choice. Skip nothing it marks blocking.
5. Before you stop: say **"run finish_check"**. It lists what still needs you.
6. At a good moment, say **"checkpoint"**. Only you approve this.

## Three rules that save you

- Only **you** accept things. The agent proposes.
- A **protected** page (accepted, or core rules like magic) is never changed without your clear yes.
- A reference gives **technique**, never names or phrasing.

## Stuck?

| Problem | Say |
|---|---|
| Agent invented something | "Search the index first. Is this already canon?" |
| Agent skipped a hard reference | "Show where hard reference X appears." |
| Too much at once | "One question at a time." |
| Lost track | "Run bootstrap_status and finish_check, then tell me the next step." |
| Newer library | In the library folder: `py -3 tools/new_world.py` (Update tab) |
| Add more references later | Same page, Add references tab |

Longer guide: `docs/JUMPSTART.md` (in the library). What the agent reads: `AGENTS.md` in your world.
