"""Usage: py -3 tools/context.py prepare|verify ...   (see --help)

Prepares the complete context packet for one narrative role in a world project, or verifies a
saved packet is still current. Read-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worlddesign.context import ContextError, run_project_context  # noqa: E402
from worlddesign.textio import use_utf8  # noqa: E402

if __name__ == "__main__":
    use_utf8()
    try:
        sys.stdout.buffer.write((run_project_context(sys.argv[1:], Path.cwd(), Path(__file__).resolve().parents[1]) + "\n").encode("utf-8"))
    except (ContextError, OSError, ValueError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
