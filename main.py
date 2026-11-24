#!/usr/bin/env python3
"""The One-Line Exit — a one-line resignation letter.

Writes a single-line resignation letter to entry.txt.
Python 3 standard library only; no network access.
"""

import os
import sys
import tempfile

# The entry is built from two literals (written in separate edits).
ENTRY_PART1 = "I hereby resign \u2014 I spent two years guarding this building at night, "
ENTRY_PART2 = "and the only thing anyone ever stole was my weekends."

ENTRY = ENTRY_PART1 + ENTRY_PART2


def validate(entry: str) -> None:
    """Gate: 1-140 UTF-8 characters, exactly one line, not whitespace only."""
    if not entry or entry.strip() == "":
        raise ValueError("entry must not be empty or whitespace only")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if not 1 <= len(entry) <= 140:
        raise ValueError(f"entry must be 1-140 characters, got {len(entry)}")


def resolve_output_dir() -> str:
    """Output dir fallback chain: MAKEFUN_OUTPUT_DIR -> /output -> output/ in repo -> temp dir."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "output"))
    candidates.append(tempfile.gettempdir())
    for path in candidates:
        try:
            os.makedirs(path, exist_ok=True)
            probe = os.path.join(path, ".write_probe")
            with open(probe, "wb") as f:
                f.write(b"")
            os.remove(probe)
            return path
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> int:
    validate(ENTRY)
    out_dir = resolve_output_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    # Write bytes, no trailing newline.
    with open(out_path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    print(f"Wrote {out_path} ({len(ENTRY)} chars, {len(ENTRY.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
