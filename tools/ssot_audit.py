#!/usr/bin/env python3
"""Find load-bearing facts that are told in more than one place.

A citation is not a retelling. This script cannot tell the difference, so it
does not try: it reports every file in which a value appears and leaves the
canonical/pointer judgment to a human. What it is for is making the judgment
possible at all, by turning "I think we said 146 somewhere else" into a list.

The corpus is excluded. Repetition inside corpus/ is the corpus doing its job:
a snapshot has to be self-contained, so documents repeat across folders by
design, and corpus/README.md already records which files are byte-identical.

Run from anywhere:  python3 tools/ssot_audit.py
Machine-readable:   python3 tools/ssot_audit.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Directories whose repetition is either by design or not ours.
#
# corpus/ is excluded but corpus/README.md is not, and the distinction cost a
# run to find. The transcriptions repeat across snapshots deliberately, so
# scanning them reports the corpus doing its job. The README is 222 lines of
# our own analysis -- the six-witness collation lives there and nowhere else --
# so excluding the whole directory hid a canonical source of truth from the
# tool built to find canonical sources of truth.
EXCLUDED_DIRS = ("corpus/", ".venv/", "site/", "node_modules/", "data/")
FORCE_INCLUDE = ("corpus/README.md",)

# Values this project treats as load-bearing: change one and a claim changes.
# Each entry is (id, regex, human description). The regex is matched against
# file text, so it must be specific enough not to fire on an unrelated number.
PROBES: list[tuple[str, str, str]] = [
    # -- Article V threshold arithmetic, 1947 vantage
    ("threshold.house", r"\b146\b", "146 representatives, two thirds of a House quorum"),
    ("threshold.senate", r"\b33 (?:of 96|senators)\b", "33 senators, two thirds of a Senate quorum"),
    ("threshold.house.full", r"\b290\b", "290 representatives, two thirds of full membership"),
    ("threshold.states.ratify", r"\b(?:36 of 48|thirty-six of forty-eight)\b", "36 of 48 states to ratify"),
    ("threshold.states.convention", r"\b(?:32 of 48|thirty-two)\b", "32 of 48 states to compel a convention"),
    ("house.size", r"\b435\b", "House fixed at 435 by the 1929 apportionment"),
    ("senate.size", r"\b96\b", "96 senators in 1947"),
    ("states.count", r"\b(?:48 states|forty-eight states|forty-eight)\b", "48 states at the 1947 vantage"),
    # -- the tooling incidents
    ("incident.219", r"\b219\b", "the 219/218 solver mislabelling incident"),
    ("incident.timeout", r"three (?:answers|outcomes) (?:instead of|rather than) two", "the timeout-reported-as-negative incident"),
    # -- the formal result
    ("model.axioms.total", r"\b51 axioms\b", "51 axioms in the Zahoransky & Benzmuller model"),
    ("model.axioms.support", r"\b6 of (?:the model's )?51\b|\bsix axioms\b", "6 of 51 axioms carry Dictatorship_t3"),
    ("model.axioms.necessary", r"\b4 of the 6\b|\bfour necessary\b", "4 of the 6 necessary to every proof"),
    # Number-agnostic on purpose. An earlier version of this probe hardcoded 80
    # and went stale the moment a check was added, which section 6c of the
    # harness then reported -- correctly -- as the audit under-reporting.
    ("verify.checks", r"\b\d+ checks, all passing\b|\b\d+ checks\b", "the advertised verify.sh check count"),
    # -- the recension findings
    # Markdown emphasis sits inside this phrase in eli5.md ("**of** the right"),
    # so the probe has to tolerate asterisks or it silently reports the fact as
    # absent. The first run of this tool did exactly that.
    ("recension.gpo", r"\**of\** the right of the people peaceably", "GPO prints 'of the right' for 'or the right'"),
    ("recension.avalon", r"Avalon (?:deletes|drops|silently drops) two commas", "Avalon drops two commas"),
    ("recension.witnesses", r"\bsix (?:independent )?witnesses\b|across six (?:official |independent )?sources", "six witnesses collated"),
    # -- the Maine comma case
    ("maine.comma", r"[Ff]or want of a comma", "O'Connor v. Oakhurst Dairy, the missing comma"),
    ("maine.settlement", r"\$5 million|five million", "the $5m settlement across 127 drivers"),
    # -- the Godel story
    ("godel.exam.date", r"December 5, 1947", "the citizenship hearing date"),
    ("godel.oath.date", r"April 2, 1948", "the date Godel swore the oath"),
    ("godel.memo.date", r"September 13, 1971", "the date Morgenstern dictated the memo"),
    ("godel.memo.quote", r"inner contradictions", "the Morgenstern memo quotation"),
    # -- the three collapses
    ("collapse.germany", r"Erm(?:ä|ae)chtigungsgesetz|Enabling Act", "the German Enabling Act, March 1933"),
    ("collapse.austria", r"Kriegswirtschaftliches", "the Austrian 1917 war economy act"),
    ("collapse.italy", r"Statuto Albertino", "the Italian Statuto, never amended"),
    # -- the authorities
    ("auth.prohibition", r"National Prohibition Cases|253 U\.? ?S\.? 350", "National Prohibition Cases, 253 U.S. 350 (1920)"),
    ("auth.missouri", r"Missouri Pacific|248 U\.? ?S\.? 276", "Missouri Pacific Ry. v. Kansas, 248 U.S. 276 (1919)"),
    ("auth.barry", r"Barry v\.? United States|279 U\.? ?S\.? 597", "Barry v. United States ex rel. Cunningham (1929)"),
    ("auth.colegrove", r"Colegrove|328 U\.? ?S\.? 549", "Colegrove v. Green, 328 U.S. 549 (1946)"),
    ("auth.schneiderman", r"Schneiderman|320 U\.? ?S\.? 118", "Schneiderman v. United States (1943)"),
    ("auth.mccardle", r"McCardle|74 U\.? ?S\.? 506", "Ex parte McCardle (1869)"),
]


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    keep = []
    for rel in out:
        if any(rel.startswith(d) for d in EXCLUDED_DIRS) and rel not in FORCE_INCLUDE:
            continue
        if not rel.endswith((".md", ".py", ".sh", ".thy", ".json")):
            continue
        keep.append(Path(rel))
    return sorted(keep)


def audit() -> dict:
    files = tracked_files()
    texts = {}
    for rel in files:
        try:
            texts[rel] = (REPO / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

    hits: dict[str, list[str]] = defaultdict(list)
    for probe_id, pattern, _desc in PROBES:
        rx = re.compile(pattern)
        for rel, text in texts.items():
            n = len(rx.findall(text))
            if n:
                hits[probe_id].append(f"{rel}:{n}")

    descriptions = {pid: desc for pid, _rx, desc in PROBES}
    return {
        "files_scanned": len(texts),
        "excluded_dirs": list(EXCLUDED_DIRS),
        "probes": [
            {
                "id": pid,
                "description": descriptions[pid],
                "file_count": len(hits.get(pid, [])),
                "files": hits.get(pid, []),
            }
            for pid, _rx, _d in PROBES
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit machine-readable output")
    ap.add_argument("--threshold", type=int, default=2,
                    help="report probes appearing in at least this many files (default 2)")
    args = ap.parse_args()

    result = audit()
    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"Scanned {result['files_scanned']} tracked files, "
          f"excluding {', '.join(result['excluded_dirs'])}\n")

    multi = [p for p in result["probes"] if p["file_count"] >= args.threshold]
    absent = [p for p in result["probes"] if p["file_count"] == 0]

    print(f"{len(multi)} facts appear in {args.threshold} or more files.\n")
    width = max((len(p["id"]) for p in multi), default=10)
    for p in sorted(multi, key=lambda p: -p["file_count"]):
        print(f"  {p['id']:<{width}}  {p['file_count']:>2} files  {p['description']}")
        for f in p["files"]:
            print(f"  {'':<{width}}     {f}")
        print()

    if absent:
        print("Probes matching nothing (either fixed, or the probe is stale):")
        for p in absent:
            print(f"  {p['id']}  {p['description']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
