"""Check a map SVG against the STUDIO handoff rules (docs/WORLD-HANDOFF.md, "Draw each map as an SVG").

New code, not a port: the old design-cartographer script only checked label overlap.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .issues import Issue
from .types import SLUG_RE

SVG_NS = "http://www.w3.org/2000/svg"
MAX_ELEMENTS = 200_000
BANNED_ELEMENTS = {
    "pattern": "pattern fills are left out by the importer",
    "lineargradient": "gradients fill with the first colour only",
    "radialgradient": "gradients fill with the first colour only",
    "filter": "filters are drawn without the effect",
    "mask": "masks are drawn without the effect",
    "marker": "markers (arrowheads) are left out",
    "textpath": "text along a path is drawn straight",
    "image": "<image> is left out",
    "foreignobject": "<foreignObject> is left out",
    "script": "<script> is left out",
}
SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "text", "use"}
NON_VISUAL = {"defs", "title", "desc", "metadata", "style", "namedview", "sodipodi:namedview"}
_URL_ATTRS = ("fill", "stroke", "filter", "mask", "marker-start", "marker-mid", "marker-end", "clip-path")


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _attr(el: ET.Element, name: str) -> str | None:
    for key, value in el.attrib.items():
        if key.rsplit("}", 1)[-1] == name:
            return value
    return None


def _count(el: ET.Element, by_id: dict[str, ET.Element], seen: frozenset[int] = frozenset()) -> int:
    total = 1
    for child in el:
        total += _count(child, by_id, seen)
    if _local(el.tag) == "use":
        ref = (_attr(el, "href") or "").lstrip("#")
        target = by_id.get(ref)
        if target is not None and id(target) not in seen:
            total += _count(target, by_id, seen | {id(el), id(target)})
    return total


CHAR_WIDTH_RATIO = 0.6  # estimated glyph width as a fraction of the font size
DEFAULT_FONT_SIZE = 14.0


def _number(text: str | None) -> float | None:
    match = re.match(r"\s*(-?\d+(?:\.\d+)?)", text or "")
    return float(match.group(1)) if match else None


def _font_size(el: ET.Element, parents: dict[ET.Element, ET.Element]) -> float:
    node: ET.Element | None = el
    while node is not None:
        size = _number(node.get("font-size"))
        if size is None:
            style = re.search(r"font-size\s*:\s*(-?\d+(?:\.\d+)?)", node.get("style", ""))
            size = float(style.group(1)) if style else None
        if size is not None:
            return size
        node = parents.get(node)
    return DEFAULT_FONT_SIZE


def _transformed(el: ET.Element, parents: dict[ET.Element, ET.Element]) -> bool:
    node: ET.Element | None = el
    while node is not None:
        if node.get("transform"):
            return True
        node = parents.get(node)
    return False


def _label_issues(root: ET.Element, parents: dict[ET.Element, ET.Element], where: str) -> list[Issue]:
    """Heuristic text-box overlap and off-canvas check. Widths are estimated from the character count, so a result is a
    hint to look at the render, not proof either way. Text under a transform is skipped."""
    box = re.split(r"[ ,]+", (root.get("viewBox") or "").strip())
    view = [float(v) for v in box] if len(box) == 4 and all(_number(v) is not None for v in box) else None
    labels: list[tuple[float, float, float, float, str]] = []
    skipped = 0
    for el in root.iter():
        if _local(el.tag) != "text":
            continue
        words = "".join(el.itertext()).strip()
        x, y = _number(el.get("x")), _number(el.get("y"))
        if not words or x is None or y is None:
            continue
        if _transformed(el, parents):
            skipped += 1
            continue
        size = _font_size(el, parents)
        width = len(words) * size * CHAR_WIDTH_RATIO
        anchor = el.get("text-anchor", "start")
        left = x - width / 2 if anchor == "middle" else x - width if anchor == "end" else x
        labels.append((left, y - size, width, size, words))
    issues: list[Issue] = []
    if view is not None:
        vx, vy, vw, vh = view
        for left, top, width, height, words in labels:
            if left < vx or top < vy or left + width > vx + vw or top + height > vy + vh:
                issues.append(Issue("warning", "S-LABEL-OFFCANVAS", where, f'label "{words}" may fall outside the viewBox (estimated box)'))
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            if a[0] < b[0] + b[2] and a[0] + a[2] > b[0] and a[1] < b[1] + b[3] and a[1] + a[3] > b[1]:
                issues.append(Issue("warning", "S-LABEL-OVERLAP", where, f'labels "{a[4]}" and "{b[4]}" may overlap (estimated boxes)'))
    return issues


def check_svg(path: Path | str, places: dict[str, str] | None = None) -> list[Issue]:
    """`places` is the manifest map row's {data-id: page file}; None skips the manifest cross-checks."""
    path = Path(path)
    where = path.name
    issues: list[Issue] = []
    try:
        root = ET.fromstring(path.read_bytes())
    except (ET.ParseError, OSError) as error:
        return [Issue("error", "S-PARSE", where, f"not well-formed SVG: {error}")]
    if _local(root.tag) != "svg":
        return [Issue("error", "S-ROOT", where, "root element must be <svg>")]
    if not root.get("viewBox"):
        issues.append(Issue("warning", "S-VIEWBOX", where, "no viewBox; the painted background cannot line up"))

    by_id = {el.get("id"): el for el in root.iter() if el.get("id")}
    parents = {child: parent for parent in root.iter() for child in parent}

    for el in root.iter():
        name = _local(el.tag)
        if name in BANNED_ELEMENTS:
            issues.append(Issue("error", "S-FEATURE", where, f"<{name}>: {BANNED_ELEMENTS[name]}"))
        for attr in _URL_ATTRS:
            value = el.get(attr) or ""
            if value.startswith("url("):
                issues.append(Issue("error", "S-FEATURE", where, f'{attr}="{value[:30]}" references a paint server or effect the importer does not read'))
        href = _attr(el, "href")
        if href and not href.startswith("#"):
            issues.append(Issue("error", "S-FEATURE", where, f"link to another file ({href[:40]}) is left out"))

    for child in root:
        name = _local(child.tag)
        if name in SHAPES:
            issues.append(Issue("error", "S-TOPLEVEL", where, f"<{name}> sits outside a top-level <g>; every shape must be inside a layer group"))
    layer_groups = [c for c in root if _local(c.tag) == "g"]
    if not layer_groups:
        issues.append(Issue("error", "S-LAYERS", where, "no top-level <g>: the importer cannot cut the map into layers"))

    seen_ids: dict[str, ET.Element] = {}
    place_elems: dict[str, ET.Element] = {}
    for el in root.iter():
        data_id = el.get("data-id")
        if data_id is None:
            continue
        if not SLUG_RE.match(data_id):
            issues.append(Issue("error", "S-PLACE-KEY", where, f'data-id "{data_id}" is not a slug'))
        if data_id in seen_ids:
            issues.append(Issue("error", "S-PLACE-DUP", where, f'data-id "{data_id}" is used more than once'))
        seen_ids[data_id] = el
        place_elems[data_id] = el
        if not el.get("aria-label"):
            issues.append(Issue("error", "S-PLACE-LABEL", where, f'place "{data_id}" has no aria-label'))
        if el.get("id"):
            issues.append(Issue("error", "S-PLACE-ID", where, f'place "{data_id}" must not carry an id (it would be read as a layer)'))
        parent = parents.get(el)
        if parent is None or _local(parent.tag) != "g":
            issues.append(Issue("error", "S-PLACE-PARENT", where, f'place "{data_id}" must be a direct child of a layer group'))

    if places is not None:
        for key in places:
            if key not in place_elems:
                issues.append(Issue("error", "S-PLACE-MISSING", where, f'manifest place "{key}" has no element with that data-id'))
        for key, element in place_elems.items():
            if key not in places:
                issues.append(Issue("warning", "S-PLACE-UNLINKED", where, f'place "{key}" is not linked to a page in the manifest'))
            ancestor = parents.get(element)
            while ancestor is not None:
                outer = ancestor.get("data-id")
                if outer is not None and places.get(outer) and places.get(key) and places[outer] != places[key]:
                    issues.append(Issue("error", "S-PLACE-NEST", where, f'"{key}" sits inside place "{outer}" but links to a different page'))
                ancestor = parents.get(ancestor)

    issues.extend(_label_issues(root, parents, where))

    total = _count(root, by_id)
    if total > MAX_ELEMENTS:
        issues.append(Issue("error", "S-SIZE", where, f"{total} elements with every <use> expanded; the importer refuses more than {MAX_ELEMENTS}"))
    return issues


def scale_note_present(cartography_text: str) -> bool:
    """The cartography page should state the map scale (for example '1 unit is 0.65 miles')."""
    match = re.search(r"^##\s+Scale\s*\n(.*?)(?=^##\s|\Z)", cartography_text, re.M | re.S)
    return bool(match and match.group(1).strip())
