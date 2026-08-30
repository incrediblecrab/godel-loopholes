#!/usr/bin/env python3
"""Check that every file this repository points at actually exists.

This tool exists because of a specific change. Deduplicating the prose moved
several incidents out of the files that narrated them twice and left a pointer
behind: `method/attack-surfaces.md` now says the German path is in
`analysis/germany-1933/path-enabling-act.md` rather than retelling it. That is
the right shape for a single source of truth, but it converts a cross-reference
from a courtesy into load-bearing structure. A pointer to a file that has been
renamed is worse than the duplication it replaced, because the duplicate was at
least still readable.

Resolution is deliberately permissive, because the repository legitimately
writes references three different ways and none of them is wrong:

  1. repository-root-relative -- `analysis/germany-1933/path-enabling-act.md`
  2. relative to the referring file -- `silence-inventory.md` from a sibling
  3. bare basename -- `cascade_domination.py`, which lives in a search/
     subdirectory that the surrounding sentence has already named

A reference resolves if any of the three finds a tracked file. Only a reference
that finds nothing at all is reported, so this catches renames, typos and
deletions without forcing a house style on how a sentence names a file.

Usage:
    tools/links.py --check              scan tracked markdown, exit 1 on a dangle
    tools/links.py --check --extra F    also scan F, which need not be tracked
    tools/links.py --json               machine-readable report
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# Extensions worth checking. A reference to a `.txt` inside corpus/ is usually
# quoting a source rather than pointing at a repository file, so the list is
# restricted to the kinds of file this project actually cross-references.
EXTENSIONS = ("md", "py", "sh", "json", "thy", "pl", "mjs", "astro", "ts", "css", "yml")

REFERENCE = re.compile(r"`([^`\s]+\.(?:" + "|".join(EXTENSIONS) + r"))`")

# corpus/ holds primary sources transcribed from scans. Their internal wording
# is not ours to police, and a statute that happens to contain a backticked
# filename is not making a claim about this repository's layout.
SKIP_PREFIXES = ("corpus/",)

# A checker that scans nothing passes trivially. This floor is far below the
# real count and exists only to make silent scope collapse a failure rather
# than a green tick.
MINIMUM_REFERENCES = 50


def repo_root() -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    while here != "/":
        if os.path.isdir(os.path.join(here, ".git")):
            return here
        here = os.path.dirname(here)
    raise SystemExit("links.py: not inside a git repository")


def tracked_files(root: str) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return out.stdout.split()


def scan(root: str, extra: list[str] | None = None) -> dict:
    tracked = tracked_files(root)

    by_basename: dict[str, list[str]] = defaultdict(list)
    for path in tracked:
        by_basename[os.path.basename(path)].append(path)

    targets = [
        f
        for f in tracked
        if f.endswith(".md") and not f.startswith(SKIP_PREFIXES)
    ]
    for path in extra or []:
        absolute = os.path.abspath(path)
        relative = os.path.relpath(absolute, root)
        # A scratch file outside the repository reads better as its own path
        # than as a stack of parent directories.
        targets.append(relative if not relative.startswith("..") else absolute)

    total = 0
    dangling = []
    for rel in targets:
        absolute = os.path.join(root, rel)
        if not os.path.isfile(absolute):
            continue
        directory = os.path.dirname(rel)
        with open(absolute, encoding="utf-8") as handle:
            text = handle.read()
        for match in REFERENCE.finditer(text):
            reference = match.group(1)
            total += 1
            # A URL or an absolute path is not a claim about this repository.
            if reference.startswith(("http", "/")):
                continue
            if os.path.exists(os.path.join(root, reference)):
                continue
            if os.path.exists(os.path.join(root, directory, reference)):
                continue
            if by_basename.get(os.path.basename(reference)):
                continue
            dangling.append({"file": rel, "reference": reference})

    return {
        "files_scanned": len(targets),
        "references_scanned": total,
        "dangling": dangling,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 on any dangling reference")
    parser.add_argument("--json", action="store_true", help="emit the full report as JSON")
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        help="also scan this file, which need not be tracked (used by the negative control)",
    )
    args = parser.parse_args()

    root = repo_root()
    report = scan(root, args.extra)

    if args.json:
        print(json.dumps(report, indent=2))

    dangling = report["dangling"]
    total = report["references_scanned"]

    if total < MINIMUM_REFERENCES:
        if not args.json:
            print(
                f"only {total} references scanned, below the floor of {MINIMUM_REFERENCES}; "
                "the scan has silently collapsed and its result means nothing"
            )
        return 1 if args.check else 0

    if dangling:
        if not args.json:
            for item in dangling:
                print(f"  {item['file']} points at {item['reference']}, which does not exist")
            print(
                f"{len(dangling)} of {total} references in {report['files_scanned']} files "
                "point at nothing"
            )
        return 1 if args.check else 0

    if not args.json:
        print(
            f"{total} file references in {report['files_scanned']} tracked files all resolve"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
