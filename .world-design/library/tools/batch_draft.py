"""Bulk draft text through the Message Batches API (half the standard price): barks, trivia, NPC lines, flavour text.

For text that is wanted in bulk after the voice, the reference cards and the key pages are approved. It is not for
creative decisions: a batch cannot ask a question, and everything it returns is a **proposal** in `drafts/batch/<name>/`
marked `status: proposed`. Nothing is ever written to `world/`.

    py -3 tools/batch_draft.py plan   --role ROLE --requests FILE [--name NAME] [--model MODEL] [--max-tokens N]
    py -3 tools/batch_draft.py submit --role ROLE --requests FILE --name NAME --yes
    py -3 tools/batch_draft.py collect --name NAME

REQUESTS is a JSON list of {"id": "bark-01", "prompt": "...", "pages": ["harbor.md", ...]} (pages are world pages whose text
is shown to the model), or a text file with one request per non-empty line. It needs your own ANTHROPIC_API_KEY and bills
that API account; `plan` shows the size first and `submit` refuses without --yes. Python 3.12+, standard library only.
Run from the world folder. The live API path is unverified in this repository (the tests use a fake transport).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.cli import add_subcommand, CliError, make_parser, parse, require_world  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

API = "https://api.anthropic.com"
VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-5-5"
DEFAULT_MAX_TOKENS = 600
MAX_REQUESTS = 5000
_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_ROLE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
_NAME = re.compile(r"^[a-z0-9][a-z0-9-]{0,47}$")

RULES = (
    "You write bulk draft text for a world project. Everything you write is a proposal for the user to review; none of it is canon. "
    "Follow the voice and the role card below. Use only the facts in the pages shown with each request, and invent nothing that "
    "contradicts them. Mark every new proper noun or world-level thing like {{new: type, \"name\"}}. Never state balance numbers "
    "(damage, costs, drop rates). Output only the requested text, with no preamble."
)


class BatchError(Exception):
    pass


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n") if path.is_file() else ""


def library_root(root: Path) -> Path:
    own = root / ".world-design" / "library"
    return own if own.is_dir() else Path(__file__).resolve().parents[1]


def load_requests(root: Path, spec: str) -> list[dict]:
    path = (root / spec) if not Path(spec).is_absolute() else Path(spec)
    if not path.is_file():
        raise BatchError(f"requests file not found: {spec}")
    text = _read(path)
    if path.suffix.lower() == ".json":
        try:
            rows = json.loads(text)
        except ValueError as error:
            raise BatchError(f"{spec} is not valid JSON: {error}") from None
        if not isinstance(rows, list):
            raise BatchError("the requests file must be a JSON list")
    else:
        rows = [{"id": f"r{n:03d}", "prompt": line.strip()} for n, line in enumerate((l for l in text.split("\n") if l.strip()), start=1)]
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or not str(row.get("prompt", "")).strip():
            raise BatchError("every request needs a non-empty prompt")
        rid = str(row.get("id", ""))
        if not _ID.match(rid) or rid in seen:
            raise BatchError(f"request id {rid!r} must be 1-64 letters, digits, - or _, and unique")
        seen.add(rid)
        pages = row.get("pages", [])
        if not isinstance(pages, list) or any(not isinstance(p, str) or "/" in p or "\\" in p or not p.endswith(".md") for p in pages):
            raise BatchError(f"request {rid}: pages must be a list of page file names such as harbor.md")
        for page in pages:
            if not (root / "world" / page).is_file():
                raise BatchError(f"request {rid}: world/{page} does not exist")
    if not rows:
        raise BatchError("no requests")
    if len(rows) > MAX_REQUESTS:
        raise BatchError(f"at most {MAX_REQUESTS} requests per batch ({len(rows)} given)")
    return rows


def build_system(root: Path, role: str) -> str:
    if not _ROLE.match(role):
        raise BatchError(f"role {role!r} must be a role id such as lore-writer (letters, digits and dashes)")
    lib = library_root(root)
    brief = _read(lib / "agents" / "roles" / f"{role}.md")
    if not brief:
        raise BatchError(f"unknown role {role!r}: no agents/roles/{role}.md in the library")
    parts = [RULES, "## Role brief\n" + brief.strip()]
    voice = _read(root / "voice.md")
    if voice:
        parts.append("## Voice\n" + voice.strip())
    card = _read(root / "authoring" / "references" / "roles" / f"{role}.md")
    if card:
        parts.append("## Role reference card\n" + card.strip())
    return "\n\n".join(parts)


def build_user(root: Path, row: dict) -> str:
    chunks = [f"## world/{p}\n{_read(root / 'world' / p).strip()}" for p in row.get("pages", [])]
    chunks.append("## Request\n" + str(row["prompt"]).strip())
    return "\n\n".join(chunks)


def build_batch(root: Path, role: str, rows: list[dict], model: str, max_tokens: int) -> dict:
    system = build_system(root, role)
    return {"requests": [{"custom_id": r["id"], "params": {"model": model, "max_tokens": max_tokens, "system": system,
                                                          "messages": [{"role": "user", "content": build_user(root, r)}]}} for r in rows]}


def size_report(batch: dict) -> str:
    n = len(batch["requests"])
    chars = sum(len(r["params"]["system"]) + len(r["params"]["messages"][0]["content"]) for r in batch["requests"])
    out = sum(r["params"]["max_tokens"] for r in batch["requests"])
    return (f"{n} request(s), model {batch['requests'][0]['params']['model']}\n"
            f"input about {chars // 4:,} tokens in total (characters / 4, an estimate), output up to {out:,} tokens\n"
            "Batch prices are half of the standard prices; check the current rates for your model. This bills the account of "
            "your ANTHROPIC_API_KEY. Most batches finish within an hour; results stay available for 24 hours after.")


def transport(method: str, url: str, key: str, body: dict | None = None) -> tuple[int, bytes]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "x-api-key": key, "anthropic-version": VERSION, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def api_key() -> str:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        raise BatchError("set ANTHROPIC_API_KEY to your own API key (this bills that account)")
    return key


def _json(status: int, body: bytes, what: str) -> dict:
    if status >= 300:
        raise BatchError(f"{what} failed (HTTP {status}): {body.decode('utf-8', 'replace')[:300]}")
    return json.loads(body.decode("utf-8"))


def state_file(root: Path, name: str) -> Path:
    return root / "work" / "batch" / name / "batch.json"


def submit(root: Path, name: str, role: str, batch: dict, force: bool = False) -> dict:
    path = state_file(root, name)
    if path.exists() and not force:
        raise BatchError(f"batch {name!r} was already submitted ({path.relative_to(root).as_posix()}); collect it, or pick another name")
    made = _json(*transport("POST", f"{API}/v1/messages/batches", api_key(), batch), "submit")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"id": made["id"], "role": role, "model": batch["requests"][0]["params"]["model"],
                                "requests": [r["custom_id"] for r in batch["requests"]]}, indent=2) + "\n", encoding="utf-8")
    return made


def collect(root: Path, name: str) -> tuple[str, int, int]:
    """Download finished results into drafts/batch/<name>/. Returns (status, written, failed)."""
    path = state_file(root, name)
    if not path.is_file():
        raise BatchError(f"no submitted batch named {name!r} (looked for {path.relative_to(root).as_posix()})")
    info = json.loads(path.read_text(encoding="utf-8"))
    key = api_key()
    status = _json(*transport("GET", f"{API}/v1/messages/batches/{info['id']}", key), "status")
    if status.get("processing_status") != "ended":
        return str(status.get("processing_status")), 0, 0
    url = status.get("results_url")
    if not url:
        raise BatchError("the batch ended but has no results_url yet; try again shortly")
    code, raw = transport("GET", url, key)
    if code >= 300:
        raise BatchError(f"results download failed (HTTP {code})")
    out = root / "drafts" / "batch" / name
    out.mkdir(parents=True, exist_ok=True)
    written, failed, rows = 0, 0, []
    for line in raw.decode("utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        cid, result = str(item.get("custom_id", "")), item.get("result") or {}
        if not _ID.match(cid):
            continue
        if result.get("type") == "succeeded":
            text = "".join(b.get("text", "") for b in (result.get("message") or {}).get("content", []) if b.get("type") == "text").strip()
            target = out / f"{cid}.md"
            if target.exists():  # a second collect must not overwrite a proposal the user already edited
                rows.append(f"| {cid} | proposed | {cid}.md |")
                continue
            target.write_text(f"---\nstatus: proposed\nsource: batch\nbatch: {name}\nrole: {info['role']}\nrequest: {cid}\n---\n\n{text}\n", encoding="utf-8")
            written += 1
            rows.append(f"| {cid} | proposed | {cid}.md |")
        else:
            failed += 1
            rows.append(f"| {cid} | {result.get('type', 'unknown')} | |")
    index = ["# Batch " + name, "", "Proposals only: nothing here is canon and nothing is in `world/`. Review, then move what you keep through the normal change rules.", "",
             "| Request | Result | File |", "|---|---|---|"] + sorted(rows)
    (out / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    return "ended", written, failed


def build_parser():
    parser = make_parser("batch_draft.py", __doc__)
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
    for name, text in (("plan", "show the size of the batch; sends nothing"), ("submit", "send the batch (needs --name and --yes)")):
        p = add_subcommand(sub, name, help=text)
        p.add_argument("--role", required=True, help="a role id such as fiction-writer")
        p.add_argument("--requests", required=True, help="a JSON list of {id, prompt, pages} or a text file with one request per line")
        p.add_argument("--model", default=DEFAULT_MODEL)
        p.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
        p.add_argument("--name", default="", help="lowercase letters, digits and dashes" + (" (required)" if name == "submit" else ""))
        if name == "submit":
            p.add_argument("--yes", action="store_true", help="confirm that this bills your API account")
            p.add_argument("--force", action="store_true", help="submit again under a name that was already submitted")
    p = add_subcommand(sub, "collect", help="download finished results into drafts/batch/NAME/ as proposals")
    p.add_argument("--name", required=True)
    return parser


def main(argv: list[str]) -> int:
    use_utf8()
    args = parse(build_parser(), argv)
    if isinstance(args, int):
        return args
    try:
        root = require_world(args.world)
        if args.name and not _NAME.match(args.name):
            raise BatchError("--name: lowercase letters, digits and dashes")
        if args.command in ("plan", "submit"):
            batch = build_batch(root, args.role, load_requests(root, args.requests), args.model, args.max_tokens)
            print(size_report(batch))
            if args.command == "plan":
                print("Nothing was sent. Add `submit --name NAME --yes` to send it.")
                return 0
            if not args.name:
                raise BatchError("--name is required to submit")
            if not args.yes:
                raise BatchError("refusing to spend without --yes")
            made = submit(root, args.name, args.role, batch, args.force)
            print(f"submitted batch {made['id']}; collect it later with: collect --name {args.name}")
        else:
            status, written, failed = collect(root, args.name)
            if status != "ended":
                print(f"still {status}; try again later")
                return 3
            print(f"wrote {written} proposal(s) to drafts/batch/{args.name}/ ({failed} failed or expired); see INDEX.md there")
    except (BatchError, CliError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
