<!-- Verbatim copy of the STUDIO app's handoff contract (upstream path: world-building-skills/docs/guides/WORLD-HANDOFF.md), supplied by the user on 2026-10-09. The app owns this contract; do not edit here. Relative links in "External authoring library" point outside this repository. -->

# Writing a world STUDIO can import

STUDIO is a world-bible and map builder. This page is for an agent that writes a game world now, outside
STUDIO, and hands it over later. Follow it and STUDIO turns your folder into a project: every page an entry of
the right type, every link a typed link between entries, and your map cut into layers and shapes whose places open
their pages. Nothing has to be fixed by hand on the way in.

Every rule below comes from what STUDIO's importer accepts or refuses today. Where a rule looks arbitrary, the
reason is given next to it.

## Hand over one folder and one manifest

```
handoff/
  manifest.json          which type each page is, which files are pictures, which file is a map
  world/                 the world itself, and nothing else
    tone-premise.md
    magic-system.md
    the-combine.md
    haldren.md
    ...
    world-map.svg
```

- **Keep every page at the top of `world/`.** No subfolders for pages. A page's file name becomes its permanent
  key, and a key can't hold a `/`.
- **Put only pages, pictures and map files in `world/`.** STUDIO refuses the whole folder when it finds a file the
  manifest doesn't name. Working notes, drafts, scripts and alternates live outside `world/`.
- **Keep `manifest.json` beside `world/`, not inside it**, for the same reason.

## Name every page file as a slug

A slug is lowercase letters and digits, in words joined by single dashes, starting with a letter:
`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`, then `.md`.

| File name | Imports? | Why |
|---|---|---|
| `haldren.md` | yes | |
| `iron-pact.md` | yes | |
| `b1-geography.md` | yes | starts with a letter |
| `01-geography.md` | no | starts with a digit |
| `Iron Pact.md` | no | a space, and STUDIO lowercases the name before checking |
| `iron_pact.md` | no | an underscore |
| `iron--pact.md` | no | a double dash |

- **Two pages can't share a name**, even in different case. Two people called Aldric become `aldric-of-torn.md` and
  `aldric-the-younger.md`.
- **Don't rename a page once others link to it.** The file name is the key every link uses.

## Make one page per thing

- **Each character, location, faction, region, creature and belief gets its own page.** A page is what STUDIO pins
  on the map, links to, comments on and sends to an AI with its neighbours. A city buried in a chapter about
  geography can't be pinned, hovered or linked.
- **An overview page per category is fine.** `factions.md` can introduce the factions and link each one's page.
- **Keep the glossary for words.** A glossary entry that is a place, a person or a group should be a page of its
  own, and other pages link to that page instead of the glossary.
- **Split a page when it grows a second subject other pages would link to.** STUDIO sends a page to an AI together
  with the pages it links, so short pages with links make smaller, sharper prompts than long ones.

## Start each page with its name

The first heading of a page becomes the entry's name. A page with no heading is refused.

```markdown
# Haldren

Haldren is the capital of [the Combine](the-combine.md) and the seat of the
[Thermal Ministry](thermal-ministry.md).

## Region / terrain

...
```

- **Don't put YAML frontmatter at the top.** STUDIO keeps a page's type and fields in the manifest, not in the
  page. A `---` block at the top lands in the page as text, and its closing `---` turns the line above it into a
  heading, which can then become the page's name.
- **Use your type's sections as `##` headings** under the name. The sections per type are in the type table below.

## Link pages with plain markdown links

```markdown
The [Combine](the-combine.md) holds the north.
Its border is [held ground](glossary.md#held-ground).
```

STUDIO rewrites each link to another page into its own entity link, `[[the-combine|Combine]]`, and records that
the page cites the other one. The same links work in Obsidian and on GitHub, so the folder stays readable before
the import.

- **Write the target as the exact file name**, with no `./`, no folder and no capital letters.
- **Point at a heading with its anchor:** `## Held Ground` is `#held-ground`. An anchor is lowercase letters,
  digits and dashes.
- **Keep `]`, `|` and line breaks out of a link's label.** A label with one of them isn't converted, and its
  paragraph is kept as raw text.
- **Don't use Obsidian wikilinks** like `[[Iron Pact]]`. A name with a space or a capital isn't a slug, so STUDIO
  shows the brackets as plain text.
- **Link what a page builds on.** A faction links its region and the history entries that made it. A location links
  its region, the faction that holds it and the people found there. Each link becomes a citation STUDIO keeps
  between the two entries.
- **Don't link to a picture or a map file**, and don't use image syntax `![alt](map.png)`. STUDIO allows a link only
  to `http://`, `https://`, `mailto:`, `/` or `#`, and it refuses inline images. A paragraph holding either is kept
  as raw source text that the editor shows unformatted. Mention the picture by its file name. It gets embedded
  after the import.

## Write the body in plain markdown

STUDIO's markdown is CommonMark plus GitHub tables, written one way. What you write is kept byte for byte, but a
block STUDIO can't read becomes a raw block: kept, shown as source, and not editable as rich text.

| Use | Avoid, since it turns the block raw |
|---|---|
| `#` headings, paragraphs, `>` quotes | HTML of any kind, `<br>`, `<div>`, `<span>` |
| `-` bullets, `1.` numbered lists | task lists, `- [ ]` and `- [x]` |
| `**bold**`, `_italic_`, `` `code` `` | images, `![alt](src)` |
| fenced code blocks, `---` rules | autolinks, `<https://example.com>` |
| tables with outer pipes, `\| a \| b \|` | reference links `[a][b]`, footnotes `[^1]: text`, link titles `[a](b "t")` |
| links to `https://` sites | a quote or list line that drops its `>` or its indent |

Save every page as UTF-8 with no byte-order mark, LF line ends and one newline at the end. A page that isn't UTF-8 is
refused.

### Add STUDIO's own blocks where they help

Each block starts a line, after a blank line. Keys are slugs.

A field, a fact STUDIO can query across the world:

```markdown
::population:: 210,000
::founded:: 1031 CR
```

An infobox, the card at the top of a wiki article. Its `image` row takes a picture after the import:

```markdown
:::infobox
::name:: The Iron Pact
::leader:: [Varok](varok.md)
::founded:: Year 312 of the Third Age
:::
```

A stat block, for a creature or a fighter. STUDIO draws `name` as the title, `size`, `type` and `alignment` as
the subtitle, and `str`, `dex`, `con`, `int`, `wis` and `cha` as the ability row. Every other key is a row:

```markdown
:::statblock
::name:: Ash Warden
::size:: medium
::type:: humanoid
::level:: 12
::health:: 4200
::str:: 16
::dex:: 12
:::
```

Any other `:::name` box is kept raw.

## Pick a type for every page

Every page has one type. The type decides the page's sections and its fields in STUDIO. The order is the build
order: write a type after the ones it depends on.

| Order | Type key | Holds | Sections | Fields besides status and summary |
|---|---|---|---|---|
| 0 | `tone-premise` | the premise, one page | Premise, Player Fantasy / Reader Experience, Tone Guardrails, Design Pillars | |
| 1 | `magic-system` | one page | Source, Cost, Limits, Access, Physics, Societal Integration, Unified Cost Stack, Core Invariants, Deliberately Unexplained | |
| 2 | `geography` | one page per region | Water, Barriers, Resources, Culture, Biome theme, Magic-invariant check | `biome`, `faction`, `child-map` |
| 3 | `history` | the ledger, usually one page | Dating System, Historical Ledger, Deliberately Unexplained | |
| 4 | `faction` | one page per faction | Goals, Obstacles, Player Connections, Mechanic Ownership Map, Cites, Culture | `region`, `color` |
| 5 | `character` | one page per character | Allegiance, Personal history, Appearance, Voice / personality | `faction`, `role` |
| 6 | `location` | one page per location | Region / terrain, Control, History here, Present figures | `region`, `controlled-by` |
| 7 | `cosmology` | one page per belief system | Creation, Death and afterlife, Gods (or their absence), Sacred and taboo, Belief-vs-fact tags, Cites, Institutions | |
| 8 | `creature` | one page per creature | Habitat, Relationship to magic, What people do about it, Appearance | `habitat`, `level-range` |
| 9 | `naming` | one page per culture or region | Covers, Phonology, Place-name structure, Personal-name structure, Drift at barriers, Consulted by | `culture` |
| 10 | `economy` | usually one page | Currency, Trade relationships, Barrier costs, Control, Historical mark | |
| 11 | `cartography` | the map's gazetteer | Map Gazetteer, Legend, Scale | `map` |
| 12 | `trivia` | usually one page | World Events (ambient, current), Trivia & Flavor | |
| 13 | `environmental-trace` | one page per trace | Cites, The index, Placement | |
| 14 | `story-hook` | usually one page | Cites, Who cares, What changes on resolution | `location` |
| 15 | `roadmap` | usually one page | Draws from, What changes, What it seeds, Invariant check | `wave` |
| | `mob-group` | a group of creatures at one spot | Members, Behaviour, Notes | `mob-type`, `count` |
| | `scripted-event` | an event or scene at one spot | Setup, Beats, Outcome | |

- **Every page has a `status`:** `draft`, `reviewed`, `accepted` or `superseded`. Hand over `draft` unless a
  person has reviewed the page.
- **`summary` is one or two plain sentences** saying what the entry is.
- **Describe geography, locations and creatures independently of a camera.** Record physical facts and how people
  experience them. Put any later camera, rendering or presentation requirements in a separate production brief.

## Write the manifest

```json
{
  "pages": [
    { "file": "tone-premise.md", "typeKey": "tone-premise", "fields": { "status": "draft", "summary": "A world of held ground and spreading dark." } },
    { "file": "the-combine.md", "typeKey": "faction", "fields": { "status": "draft", "region": "the-north.md", "color": "#4a6b8a" } },
    { "file": "haldren.md", "typeKey": "location", "fields": { "status": "draft", "region": "the-north.md", "controlled-by": "the-combine.md" } }
  ],
  "assets": [
    { "file": "world-map.svg", "mediaType": "image/svg+xml" },
    { "file": "world-map-painted.webp", "mediaType": "image/webp" }
  ],
  "maps": [
    {
      "svg": "world-map.svg",
      "background": "world-map-painted.webp",
      "name": "The Held Ground",
      "slug": "held-ground",
      "places": { "haldren": "haldren.md", "the-combine": "the-combine.md" }
    }
  ]
}
```

- **`pages`:** one row per page, with its type key from the table above and the values of its fields. A field
  that names another entry, such as `region` or `faction`, takes that entry's file name.
- **`assets`:** one row per picture or map file, with its media type, such as `image/svg+xml`, `image/png`,
  `image/jpeg` or `image/webp`.
- **`maps`:** one row per map. `svg` is the map's file and `places` links each place key in it to the page that
  place opens. `background` is optional, a painted picture drawn under the shapes.
- **Every file in `world/` appears in the manifest once, and every file the manifest names is in `world/`.**

## Draw each map as an SVG

STUDIO cuts an SVG into layers of shapes: regions you can hover and fill, lines, labels and titles. A PNG or a JPEG
can only be a backdrop. STUDIO can't trace a painting into shapes, so hand over the SVG even when you also hand over
a painting.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 1800">
  <g id="layer-land">
    <path d="M166,364 C173,353 ... Z" fill="#d8ccb0" stroke="#6b5d48"/>
  </g>
  <g id="layer-rivers">
    <path d="M410,220 C430,260 ..." fill="none" stroke="#7b98a1" stroke-width="2"/>
  </g>
  <g id="layer-settlements">
    <g data-id="haldren" aria-label="Haldren">
      <circle cx="512" cy="430" r="6" fill="#2d2a26"/>
    </g>
    <text x="522" y="426" font-size="14">Haldren</text>
  </g>
  <g id="layer-titles">
    <text x="600" y="300" font-size="28" letter-spacing="6">THE COMBINE</text>
  </g>
</svg>
```

- **Put every shape inside a top-level `<g>`.** Each top-level group becomes one layer, the first one at the
  bottom. STUDIO names the layer from `inkscape:label`, or else from its `id`: `id="layer-rivers"` becomes
  "Rivers".
- **Nest named groups to make a layer group.** A `<g>` with an `id` or an `inkscape:label` inside a layer becomes
  a layer of its own under it, so "Roads" can hold "Capital road" and "Gate road". Neighbouring top-level groups
  with the same `data-layer` value are gathered into one layer group too.
- **Mark each place a page should open** with a direct child of a layer group that carries `data-id` and
  `aria-label`, and no `id`. `data-id` is a slug, unique in the map, and it's the key the manifest's `places`
  uses. `aria-label` is the place's name. Draw the place's shapes inside that child.
- **A `<text>` in the same layer group whose words match a place's `aria-label` becomes that place's label.**
- **Fill a shape to make a region.** A stroked shape with no fill becomes a line, or an unfilled region when it's
  closed. A `<text>` becomes a label. A level label of three letters or more with `letter-spacing` becomes a
  title, which stays readable at every zoom.
- **Use one SVG unit as one world unit**, and write the scale in the cartography page, such as "1 unit is 0.65
  miles".
- **Draw the painted background at the SVG's `viewBox` size**, so the two line up without adjusting.

The importer reads these SVG features poorly or not at all, so draw without them:

| Feature | What STUDIO does |
|---|---|
| pattern fills | leaves them out |
| gradients | fills with the first colour |
| filters, masks | draws without the effect |
| markers, such as arrowheads | leaves them out |
| text along a path | draws it straight |
| `<image>`, `<foreignObject>`, `<script>`, links to other files | leaves them out |
| more than 200,000 elements, with every `<use>` expanded | refuses the file |

## External authoring library

Reusable worldbuilding and narrative methods live in the separate [world-design-skills library](../../../world-design-skills/README.md). Its [category mapping](../../../world-design-skills/docs/world-bible-categories.md) connects methods to the app's stable type keys.

For import, retain the page bodies, manifest, type keys, links and map format specified above. STUDIO types provide starter templates; additional authoring skills do not create new app entity types.

## Check the folder before you hand it over

STUDIO stops at the first problem and names the file. Each of these is a refusal:

| STUDIO says | Fix |
|---|---|
| a file the manifest names as neither a page nor an asset | add its row, or move it out of `world/` |
| a file the manifest names that the folder doesn't hold | add the file, or remove its row |
| a type key no type has | use a key from the type table |
| a page name that isn't a slug, or two pages with one slug | rename the file |
| a page that isn't UTF-8 | save it as UTF-8 |
| a page with no heading | start it with `# Name` |
| a map place the manifest links to no page, or a page that isn't in `pages` | link the place to a page file listed in `pages` |
| a place key the SVG doesn't hold | match `places` to the SVG's `data-id` values |
| one shape under two places linked to different pages | give each shape one place |

Run these checks yourself before the handover:

1. Every file in `world/` is in the manifest, and every manifest file is in `world/`.
2. Every page file name matches `^[a-z][a-z0-9]*(-[a-z0-9]+)*\.md$`, and no two match after lowercasing.
3. Every page starts with `# Name` and has no frontmatter.
4. Every relative link points at a page file in `world/`, and every anchor is a heading's slug in that page.
5. No page holds HTML, an image, a wikilink or a task list.
6. Every SVG shape sits in a top-level `<g>`, every place has `data-id` and `aria-label`, and every key in `places`
   is one of those `data-id` values.
