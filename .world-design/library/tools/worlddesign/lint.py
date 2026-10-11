"""Canon lint: the handoff validator (layer 1) and the mechanical library rules (layer 2).

Layer 2 only checks what a script can know: records vs. baseline hashes, modes, decision
status and authority, stale index. Whether a sentence is a consequential invention is NOT
linted; that is for the custodian and the evals (rules/INVENTION.md, section "What checks").
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, replace
from pathlib import Path

from .issues import Issue
from .miniyaml import split_frontmatter
from .ledger import (
    CHANGE_MODES,
    CHANGE_STATUSES,
    CHANGE_TIERS,
    DECISION_STATUSES,
    DECISION_TYPES,
    Record,
    is_authorization,
    record_pages,
    as_list,
    classify_changes,
    compute_stale,
    load_baseline,
    load_changes,
    load_decisions,
)
from .policy import OVERRIDE_REL, Policy, PolicyError, load_policy
from .refcheck import check_references
from .stories import NEW_TAG, NOVEL_FILES, SERIES_REL, STORY_FORMS, invention_rows, load_stories
from .storycheck import check_novels
from .svgcheck import check_svg, scale_note_present
from .textio import read_text
from .types import PAGE_FILE_RE
from .world import World, build_index, load_world

_CODE_SPAN = re.compile(r"`[^`]*`")
_HTML = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?>|<!--")
_IMAGE = re.compile(r"!\[")
_WIKI = re.compile(r"\[\[")
_TASK = re.compile(r"^\s*[-*+]\s+\[[ xX]\]\s")
_REFLINK = re.compile(r"\[[^\]]+\]\[[^\]]*\]")
_FOOTNOTE = re.compile(r"\[\^[^\]]+\]")
_AUTOLINK = re.compile(r"<(?:https?://|mailto:)[^>]*>")
_TITLE = re.compile(r"\]\([^)]*\s+\"[^\"]*\"\s*\)")
_EXTERNAL_OK = re.compile(r"^(https?://|mailto:|/|#)")
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def check_handoff(world: World) -> list[Issue]:
    issues: list[Issue] = []
    add = issues.append
    for problem in world.problems:
        add(Issue("error", "H-STRUCT", "manifest.json", problem))
    if (world.root / "manifest.json").read_bytes().startswith(b"\xef\xbb\xbf"):
        add(Issue("error", "H-BOM", "manifest.json", "manifest has a byte-order mark; save UTF-8 without BOM"))

    # --- files in world/ vs the manifest -------------------------------------------------
    wd = world.world_dir
    on_disk: set[str] = set()
    if wd.is_dir():
        for entry in sorted(wd.iterdir()):
            if entry.is_dir():
                add(Issue("error", "H-SUBFOLDER", f"world/{entry.name}", "world/ must be flat: pages and assets sit at its top level"))
            else:
                on_disk.add(entry.name)
    else:
        add(Issue("error", "H-NO-WORLD", "world/", "world/ folder is missing"))
    assets = world.manifest.get("assets") or []
    maps = world.manifest.get("maps") or []
    asset_files = {a.get("file") for a in assets if isinstance(a, dict)}
    listed = set(world.pages) | {f for f in asset_files if f}
    for name in sorted(on_disk - listed):
        add(Issue("error", "H-UNLISTED", f"world/{name}", "file is in world/ but not in manifest.json (move it out of world/ or add its row)"))
    for name in sorted(f for f in listed - on_disk if f in asset_files):
        add(Issue("error", "H-MISSING", f"world/{name}", "manifest names this asset but the file is not in world/"))

    # --- page names ----------------------------------------------------------------------
    lowered: dict[str, str] = {}
    for file in world.pages:
        if not PAGE_FILE_RE.match(file):
            add(Issue("error", "H-SLUG", f"world/{file}", "page file name must be a slug ending in .md (lowercase, digits, single dashes, starts with a letter)"))
        key = file.lower()
        if key in lowered and lowered[key] != file:
            add(Issue("error", "H-NAME-CLASH", f"world/{file}", f"name clashes with {lowered[key]} once lowercased"))
        lowered[key] = file

    # --- per-page checks -----------------------------------------------------------------
    types = world.types
    for file, page in world.pages.items():
        where = f"world/{file}"
        if not page.raw and not (wd / file).is_file():
            continue
        try:
            page.raw.decode("utf-8")
        except UnicodeDecodeError:
            add(Issue("error", "H-ENCODING", where, "page is not valid UTF-8"))
            continue
        if page.raw.startswith(b"\xef\xbb\xbf"):
            add(Issue("error", "H-BOM", where, "page has a byte-order mark; save UTF-8 without BOM"))
        if b"\r" in page.raw:
            add(Issue("error", "H-LINE-ENDINGS", where, "page has CR/CRLF line endings; use LF"))
        if not page.raw.endswith(b"\n") or page.raw.endswith(b"\n\n"):
            add(Issue("error", "H-TRAILING-NEWLINE", where, "page must end with exactly one newline"))
        first = page.text.split("\n", 1)[0]
        if first.strip() == "---":
            add(Issue("error", "H-FRONTMATTER", where, "pages must not start with YAML frontmatter; type and status live in manifest.json"))
        elif not first.startswith("# ") or not first[2:].strip():
            add(Issue("error", "H-NAME", where, "page must start with `# Name`"))

        if page.type_key not in types.types:
            add(Issue("error", "H-TYPE", where, f"unknown typeKey `{page.type_key}`"))
            ptype = None
        else:
            ptype = types.types[page.type_key]
        if page.status not in types.status_values:
            add(Issue("error", "H-STATUS", where, f"status must be one of {', '.join(types.status_values)}"))
        if not page.summary.strip():
            add(Issue("warning", "H-SUMMARY", where, "no summary: add one or two plain sentences to the manifest fields"))
        if ptype is not None:
            for key, value in page.fields.items():
                if key in ("status", "summary"):
                    continue
                if key not in ptype.fields:
                    add(Issue("warning", "H-FIELD", where, f"field `{key}` is not defined for type {ptype.key}"))
                elif key in ptype.refs and value and value not in world.pages:
                    add(Issue("error", "H-FIELD-REF", where, f"field `{key}` names {value}, which is not a page in the manifest"))
            heads = [h[1] for h in page.headings if h[0] == 2]
            missing = [s for s in ptype.sections if s not in heads]
            if missing:
                add(Issue("warning", "H-SECTIONS", where, f"missing sections for {ptype.key}: {', '.join(missing)}"))
            else:
                order = [h for h in heads if h in ptype.sections]
                if order != [s for s in ptype.sections if s in order]:
                    add(Issue("warning", "H-SECTION-ORDER", where, f"sections are not in the order {', '.join(ptype.sections)}"))

        # forbidden markup and link targets
        for number, line in page.prose_lines:
            plain = _CODE_SPAN.sub("", line)
            loc = f"{where}:{number}"
            if _HTML.search(plain):
                add(Issue("error", "H-HTML", loc, "HTML is not allowed"))
            if _IMAGE.search(plain):
                add(Issue("error", "H-IMAGE", loc, "inline images are not allowed; mention the picture by file name"))
            if _WIKI.search(plain):
                add(Issue("error", "H-WIKILINK", loc, "wikilinks are not allowed; use [label](page.md)"))
            if _TASK.match(plain):
                add(Issue("error", "H-TASKLIST", loc, "task lists are not allowed"))
            if _FOOTNOTE.search(plain):
                add(Issue("error", "H-FOOTNOTE", loc, "footnotes are not allowed"))
            if _AUTOLINK.search(plain):
                add(Issue("error", "H-AUTOLINK", loc, "autolinks are not allowed; use [label](https://...)"))
            if _TITLE.search(plain):
                add(Issue("error", "H-LINK-TITLE", loc, "link titles are not allowed"))
            if _REFLINK.search(plain) and not _WIKI.search(plain) and not _FOOTNOTE.search(plain):
                add(Issue("error", "H-REFLINK", loc, "reference-style links are not allowed"))
        own_slugs = {h[2] for h in page.headings}
        for link in page.links:
            loc = f"{where}:{link.line}"
            target = link.target
            if _EXTERNAL_OK.match(target):
                if target.startswith("#") and target[1:] and target[1:] not in own_slugs:
                    add(Issue("error", "H-ANCHOR", loc, f"anchor {target} is not a heading in this page"))
                continue
            if _SCHEME.match(target):
                add(Issue("error", "H-LINK-SCHEME", loc, f"link scheme not allowed: {target}"))
                continue
            path, _, anchor = target.partition("#")
            if "]" in link.label or "|" in link.label:
                add(Issue("error", "H-LINK-LABEL", loc, "link labels must not contain ] or |"))
            if not PAGE_FILE_RE.match(path):
                add(Issue("error", "H-LINK-TARGET", loc, f"`{target}` must be the exact file name of a page (no folder, no ./, no capitals; pictures and maps cannot be linked)"))
            elif path not in world.pages:
                add(Issue("error", "H-LINK-DEAD", loc, f"`{path}` is not a page in the manifest"))
            elif anchor and anchor not in {h[2] for h in world.pages[path].headings}:
                add(Issue("error", "H-ANCHOR", loc, f"`#{anchor}` is not a heading in {path}"))

    # --- maps ----------------------------------------------------------------------------
    for row in maps:
        if not isinstance(row, dict) or not isinstance(row.get("svg"), str):
            add(Issue("error", "H-MAP", "manifest.json", f"map row needs an `svg`: {row!r}"))
            continue
        svg = row["svg"]
        if svg not in asset_files:
            add(Issue("error", "H-MAP-ASSET", "manifest.json", f"map svg {svg} is not listed in assets"))
        bg = row.get("background")
        if bg and bg not in asset_files:
            add(Issue("error", "H-MAP-ASSET", "manifest.json", f"map background {bg} is not listed in assets"))
        places = row.get("places") or {}
        for key, target in places.items():
            if target not in world.pages:
                add(Issue("error", "H-MAP-PLACE", "manifest.json", f'map place "{key}" links to {target}, which is not in pages'))
        if (wd / svg).is_file():
            issues.extend(check_svg(wd / svg, {k: v for k, v in places.items() if isinstance(v, str)}))
    for file, page in world.pages.items():
        if page.type_key == "cartography" and not scale_note_present(page.text):
            add(Issue("warning", "H-SCALE", f"world/{file}", "cartography page should state the map scale under `## Scale`"))
    return issues


def _decision_issues(world: World, decisions: list[Record], changes: dict[str, str]) -> list[Issue]:
    issues: list[Issue] = []
    ids: dict[str, Record] = {}
    for rec in decisions:
        if rec.error:
            issues.append(Issue("error", "L-DECISION-FORMAT", rec.path, rec.error))
            continue
        meta = rec.meta
        did = str(meta.get("id", ""))
        if not re.match(r"^D-\d{4}$", did):
            issues.append(Issue("error", "L-DECISION-ID", rec.path, f"id must look like D-0001, got `{did}`"))
        elif did in ids:
            issues.append(Issue("error", "L-DECISION-DUP", rec.path, f"{did} is also used by {ids[did].path}"))
        ids[did] = rec
        if meta.get("type") not in DECISION_TYPES:
            issues.append(Issue("error", "L-DECISION-TYPE", rec.path, f"type must be one of {', '.join(DECISION_TYPES)}"))
        status = meta.get("status")
        if status not in DECISION_STATUSES:
            issues.append(Issue("error", "L-DECISION-STATUS", rec.path, f"status must be one of {', '.join(DECISION_STATUSES)}"))
        if status == "accepted" and not str(meta.get("authority", "")).strip():
            issues.append(Issue("error", "L-DECISION-AUTHORITY", rec.path, "an accepted decision needs the user's exact words in `authority`"))
        if status == "superseded" and not as_list(meta.get("superseded_by")):
            issues.append(Issue("error", "L-DECISION-SUPERSEDED", rec.path, "a superseded decision must name `superseded_by`"))
    for rec in decisions:
        if rec.error:
            continue
        for ref in as_list(rec.meta.get("supersedes")) + as_list(rec.meta.get("superseded_by")):
            if ref not in ids:
                issues.append(Issue("error", "L-DECISION-REF", rec.path, f"refers to unknown decision {ref}"))
        for page in as_list(rec.meta.get("affects")):
            if page not in world.pages:
                issues.append(Issue("warning", "L-DECISION-AFFECTS", rec.path, f"affects {page}, which is not a page"))
        if rec.meta.get("blocking") is True and rec.meta.get("status") in ("open", "proposed"):
            hit = [p for p in as_list(rec.meta.get("affects")) if changes.get(p, "unchanged") != "unchanged"]
            if hit:
                issues.append(Issue("error", "L-BLOCKING", rec.path, f"open blocking decision affects changed pages: {', '.join(hit)}"))
    return issues


def check_library(world: World) -> list[Issue]:
    issues: list[Issue] = []
    add = issues.append
    try:
        baseline = load_baseline(world.root)
    except ValueError as error:
        add(Issue("error", "L-BASELINE", "ledger/page-hashes.json", str(error)))
        baseline = None
    changes = classify_changes(world, baseline)
    records = load_changes(world.root)
    decisions = load_decisions(world.root)

    for rec in records:
        if rec.error:
            add(Issue("error", "L-CHANGE-FORMAT", rec.path, rec.error))
            continue
        meta = rec.meta
        if meta.get("mode") not in CHANGE_MODES:
            add(Issue("error", "L-CHANGE-MODE", rec.path, f"mode must be one of {', '.join(CHANGE_MODES)}"))
        if meta.get("tier") not in CHANGE_TIERS:
            add(Issue("error", "L-CHANGE-TIER", rec.path, f"tier must be one of {', '.join(CHANGE_TIERS)}"))
        if meta.get("status") not in CHANGE_STATUSES:
            add(Issue("error", "L-CHANGE-STATUS", rec.path, f"status must be one of {', '.join(CHANGE_STATUSES)}"))
        if meta.get("tier") == "T3" and not str(meta.get("authority", "")).strip():
            add(Issue("error", "L-CHANGE-AUTHORITY", rec.path, "a T3 record needs the user's exact authorizing words in `authority`"))

    good = [r for r in records if not r.error]

    by_page: dict[str, list[Record]] = {}
    for r in good:
        for page_file in record_pages(r):
            by_page.setdefault(page_file, []).append(r)

    def covering(file: str) -> list[Record]:
        return by_page.get(file, [])

    old = baseline["pages"] if baseline else {}
    logged_names: set[str] | None = None
    for file, kind in changes.items():
        if kind == "unchanged":
            continue
        page = world.pages.get(file)
        was_protected = bool(old.get(file, {}).get("protected"))
        now_protected = bool(page and world.is_protected(page))
        recs = covering(file)
        where = f"world/{file}"
        if kind == "deleted":
            add(Issue("error", "L-DELETED", where, "page was deleted; never delete a page others may link to, set it `superseded` instead"))
        elif kind == "changed":
            if was_protected or now_protected:
                t3 = [r for r in recs if is_authorization(r, baseline)]
                if not t3:
                    add(Issue("error", "L-PROTECTED-CHANGE", where, "protected page changed with no T3 change record naming the user's authorization"))
            elif not recs:
                add(Issue("error", "L-UNRECORDED-EDIT", where, "existing page changed with no change record in ledger/changes/"))
            for r in recs:
                if r.meta.get("mode") in ("explore", "lock"):
                    add(Issue("error", "L-MODE", r.path, f"mode `{r.meta.get('mode')}` may not change the existing page {file}"))
        elif kind == "new":
            if not recs:
                if logged_names is None:  # read and split once, however many pages are new
                    log = world.root / "ledger" / "log.md"
                    logged_names = set(re.findall(r"[\w-]+", read_text(log))) if log.is_file() else set()
                if file[:-3] not in logged_names:  # a whole name, so `page-1` is not logged by a line about `page-10`
                    add(Issue("warning", "L-UNLOGGED-NEW", where, "new page has no log line or change record (T1b needs a log line, T2 a change record)"))
    # status flipped to accepted must carry a recorded acceptance
    for file, page in world.pages.items():
        if page.status != "accepted":
            continue
        if old.get(file, {}).get("status") == "accepted":
            continue
        ok = [r for r in covering(file) if r.meta.get("status") == "accepted" and str(r.meta.get("authority", "")).strip()]
        if not ok:
            add(Issue("error", "L-ACCEPTED", f"world/{file}", "status accepted without a change record (status accepted) naming the user's words; only the user accepts"))

    issues.extend(_decision_issues(world, decisions, changes))

    index_path = world.root / "INDEX.md"
    if index_path.is_file():
        if read_text(index_path) != build_index(world):
            add(Issue("error", "L-INDEX-STALE", "INDEX.md", "index is out of date; run `py -3 tools/canon_index.py index`"))
    elif world.pages:
        add(Issue("warning", "L-INDEX-MISSING", "INDEX.md", "no INDEX.md; run `py -3 tools/canon_index.py index`"))

    stale = world.root / "ledger" / "stale.md"
    _, open_count = compute_stale(world, baseline, read_text(stale) if stale.is_file() else "")
    if open_count:
        add(Issue("warning", "L-STALE", "ledger/stale.md", f"{open_count} dependent page(s) still to check after protected pages changed"))
    return issues


def check_stories(world: World) -> list[Issue]:
    """Mechanical story rules from rules/STORIES.md: tags need rows; a final story has no open items."""
    issues: list[Issue] = []
    for story in load_stories(world.root):
        folder, rel, status = story.path, story.rel, story.status
        if not story.has_story_md:
            issues.append(Issue("error", "L-STORY-META", rel, "story folder needs a story.md"))
        elif story.error:
            issues.append(Issue("error", "L-STORY-META", f"{rel}/story.md", story.error))
        else:
            if status not in ("draft", "final"):
                issues.append(Issue("error", "L-STORY-META", f"{rel}/story.md", "status must be draft or final"))
            if story.meta.get("form") not in STORY_FORMS:
                issues.append(Issue("error", "L-STORY-META", f"{rel}/story.md", f"form must be one of {', '.join(STORY_FORMS)}"))
            if story.meta.get("form") == "novel":
                for needed in NOVEL_FILES:
                    if not (folder / needed).is_file():
                        issues.append(Issue("error", "L-STORY-NOVEL", rel, f"a novel needs {needed} (copy it from drafts/stories/_template-novel/)"))
            if story.series and not (world.root / SERIES_REL / story.series / "series.md").is_file():
                issues.append(Issue("error", "L-STORY-SERIES", f"{rel}/story.md", f"series `{story.series}` has no drafts/series/{story.series}/series.md"))
        rows, problems = invention_rows(folder / "inventions.md")
        for problem in problems:
            issues.append(Issue("error", "L-STORY-ROW", f"{rel}/inventions.md", problem))
        for key, (row_status, resolution) in rows.items():
            if row_status != "open" and not resolution:
                issues.append(Issue("error", "L-STORY-RESOLUTION", f"{rel}/inventions.md", f"`{key[0]}` is {row_status} but names no resolution"))
            if row_status == "open" and status == "final":
                issues.append(Issue("error", "L-STORY-FINAL-OPEN", f"{rel}/inventions.md", f"story is final but `{key[0]}` is still open"))
        for path in sorted(folder.rglob("*.md")):
            if path.name == "inventions.md":
                continue
            text = read_text(path)
            where = f"{rel}/{path.relative_to(folder).as_posix()}"
            good = NEW_TAG.findall(text)
            if text.count("{{new:") != len(good):
                issues.append(Issue("error", "L-STORY-TAG-FORMAT", where, 'malformed tag; write {{new: type, "name"}}'))
            for kind, name in good:
                if (name.lower(), kind.lower()) not in rows:
                    issues.append(Issue("error", "L-STORY-TAG-ROW", where, f"tag for `{name}` ({kind}) has no row in inventions.md"))
            if good and status == "final":
                issues.append(Issue("error", "L-STORY-FINAL-TAGS", where, f"story is final but {len(good)} invention tag(s) remain"))
    return issues


# Fact lines that name one event: `<subject>-<event verb>` such as `toll-war-ended`. The same key on two pages with
# different values is a contradiction. Generic per-page keys (`founded`, `born`, `elevation`) are not checked: two
# guilds may each have their own founding year.
_START_VERBS = ("began", "started", "founded", "chartered", "opened", "formed", "born")
_END_VERBS = ("ended", "fell", "destroyed", "dissolved", "abolished", "closed", "died")
_OTHER_VERBS = ("raised", "walled", "signed", "crowned", "completed", "built", "conquered", "sealed", "declared", "won", "lost")
_EVENT_KEY = re.compile(r"^(?P<stem>[a-z0-9]+(?:-[a-z0-9]+)*)-(?P<verb>%s)$" % "|".join(_START_VERBS + _END_VERBS + _OTHER_VERBS))
_DATE = re.compile(r"^(?P<n>\d[\d,]*)\s*(?P<era>[A-Za-z]{1,4})\b")


def check_facts(world: World) -> list[Issue]:
    """Warnings for same-key conflicts and event dates out of order, from the `::key:: value` lines. Fast and deterministic."""
    issues: list[Issue] = []
    values: dict[str, list[tuple[str, str]]] = {}
    for file, page in world.pages.items():
        for key, value, _ in page.facts:
            if _EVENT_KEY.match(key):
                values.setdefault(key, []).append((file, value))
    for key, rows in sorted(values.items()):
        distinct = {re.sub(r"\s+", " ", v.strip().lower()) for _, v in rows}
        if len(distinct) > 1:
            shown = "; ".join(f"{f}: {v}" for f, v in rows)
            issues.append(Issue("warning", "L-FACT-CONFLICT", f"world/{rows[0][0]}",
                                f"`::{key}::` has different values ({shown}). Report both, do not pick one silently, and ask which stands."))
    by_stem: dict[str, dict[str, tuple[int, str]]] = {}
    for key, rows in values.items():
        match = _EVENT_KEY.match(key)
        date = _DATE.match(rows[0][1].strip())
        if match and date:
            by_stem.setdefault(match.group("stem"), {})[match.group("verb")] = (int(date.group("n").replace(",", "")), date.group("era").upper())
    for stem, verbs in sorted(by_stem.items()):
        for start in (v for v in _START_VERBS if v in verbs):
            for end in (v for v in _END_VERBS if v in verbs):
                (n1, era1), (n2, era2) = verbs[start], verbs[end]
                if era1 == era2 and n1 > n2:
                    issues.append(Issue("warning", "L-FACT-ORDER", f"world/{values[f'{stem}-{start}'][0][0]}",
                                        f"`{stem}` {start} in {n1} {era1} but {end} in {n2} {era2}: the end comes before the start."))
    return issues


@dataclass(frozen=True)
class Check:
    """One check function in the registry: what it reads (path prefixes), and whether it needs the parsed world."""
    name: str
    scope: tuple[str, ...]
    needs_world: bool
    run: Callable[[Path, "World | None", Policy], list[Issue]]

    def applies_to(self, paths: Iterable[str] | None) -> bool:
        return paths is None or any(path == prefix or path.startswith(prefix) for path in paths for prefix in self.scope)


CHECKS: tuple[Check, ...] = (
    Check("handoff", ("manifest.json", "world/"), True, lambda root, world, policy: check_handoff(world)),
    Check("library", ("manifest.json", "world/", "ledger/", "decisions/", "INDEX.md"), True, lambda root, world, policy: check_library(world)),
    Check("stories", ("manifest.json", "world/", "ledger/", "decisions/", "drafts/stories/", "drafts/series/"), True, lambda root, world, policy: check_stories(world)),
    Check("facts", ("manifest.json", "world/"), True, lambda root, world, policy: check_facts(world)),
    Check("references", ("authoring/references/", "design/", "voice.md", ".world-design/"), False, lambda root, world, policy: check_references(root, policy)),
    Check("novels", ("drafts/stories/", "drafts/series/"), False, lambda root, world, policy: check_novels(root, policy)),
)


def apply_policy(issues: list[Issue], policy: Policy) -> list[Issue]:
    """Drop the findings the world turned off and re-level the ones it changed (only warnings can be tuned; see policy.py)."""
    out: list[Issue] = []
    for issue in issues:
        level = policy.check_level(issue.code, issue.level)
        if level == "off":
            continue
        out.append(issue if level == issue.level else replace(issue, level=level))
    return out


def lint_world(root: Path | str, world: World | None = None, policy: Policy | None = None, paths: Iterable[str] | None = None) -> list[Issue]:
    """All findings for a world, with the world's policy applied.

    Pass an already loaded `world` (and `policy`) to avoid parsing everything twice. With `paths` (world-relative, posix) only the
    checks that read those paths run, and the world is loaded only if one of them needs it: the post-write hook uses this so a
    card or a systems spec is not checked against every page.
    """
    root = Path(root)
    extra: list[Issue] = []
    try:
        policy = policy or load_policy(root)
    except PolicyError as error:
        policy = load_policy(None)
        extra.append(Issue("error", "L-POLICY", OVERRIDE_REL, str(error)))
    selected = [c for c in CHECKS if c.applies_to(paths)]
    if world is None and any(c.needs_world for c in selected):
        world = load_world(root)
    issues: list[Issue] = []
    for check in selected:
        issues += check.run(root, world, policy)
    return apply_policy(issues, policy) + extra
