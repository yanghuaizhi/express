#!/usr/bin/env python3
"""Load packaged communication guidance; never read session input or user files."""

import json
from pathlib import Path
import sys


def main() -> int:
    core = Path(__file__).resolve().parent.parent / "skills/express/references/core.md"
    try:
        content = core.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("Express: packaged core.md could not be read as UTF-8.", file=sys.stderr)
        return 1
    if not content.strip():
        print("Express: packaged core.md is empty.", file=sys.stderr)
        return 1
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": content,
        }
    }
    # Escapes keep the protocol valid even when a host's stdout encoding is ASCII.
    print(json.dumps(payload, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
