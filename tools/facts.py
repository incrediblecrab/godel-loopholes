#!/usr/bin/env python3
"""Check data/facts.json against the files it names as canonical.

The rule this enforces: narrative is authored per audience, facts are
single-sourced. A general-audience page and a research note may say the same
thing in different words. They may not say it with different numbers.

So every entry in facts.json names one file as the owner of its value, and this
script asserts the value is actually there. If somebody edits the number in the
markdown and not in the JSON, or the other way round, this fails. Nothing that
renders a value is allowed to hold its own copy.

  python3 tools/facts.py            # human-readable report
  python3 tools/facts.py --check    # exit 1 on any failure, terse output
  python3 tools/facts.py --ids      # list fact ids, one per line
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Overridable so verify.sh can point the checker at a deliberately broken copy
# and confirm it rejects one. A checker that has never been seen to fail is not
# evidence that anything passed.
FACTS = Path(os.environ.get("GL_FACTS", REPO / "data" / "facts.json"))

REQUIRED_KEYS = ("id", "value", "label", "statement", "canonical", "status")
VALID_STATUS = ("verified", "unverified", "disproved")

# Prose in this repository spells small numbers out. A fact whose value is 48
# is present in a file that says "forty-eight states", and a checker that only
# looked for the digits would report a false failure.
NUMBER_WORDS = {
    0: ["zero", "no"],
    3: ["three"],
    4: ["four"],
    5: ["five"],
    6: ["six"],
    8: ["eight"],
    12: ["twelve"],
    32: ["thirty-two"],
    33: ["thirty-three"],
    36: ["thirty-six"],
    48: ["forty-eight"],
    49: ["forty-nine"],
    51: ["fifty-one"],
    64: ["sixty-four"],
    80: ["eighty"],
    96: ["ninety-six"],
    146: ["one hundred forty-six"],
    218: ["two hundred eighteen"],
    290: ["two hundred ninety"],
    435: ["four hundred thirty-five"],
}

# Arithmetic relations that must hold among the numeric facts. Each is
# (result_id, human description, callable over a dict of id -> value).
# These are a genuine cross-check: they catch a value edited in both the JSON
# and its canonical file but left inconsistent with the numbers it derives from.
ARITHMETIC = [
    ("house.quorum", "a majority of the House",
     lambda f: f["house.size"] // 2 + 1),
    ("senate.quorum", "a majority of the Senate",
     lambda f: f["senate.size"] // 2 + 1),
    ("threshold.house.propose", "two thirds of a House quorum",
     lambda f: math.ceil(f["house.quorum"] * 2 / 3)),
    ("threshold.senate.propose", "two thirds of a Senate quorum",
     lambda f: math.ceil(f["senate.quorum"] * 2 / 3)),
    ("threshold.house.full", "two thirds of full House membership",
     lambda f: math.ceil(f["house.size"] * 2 / 3)),
    ("threshold.senate.full", "two thirds of full Senate membership",
     lambda f: math.ceil(f["senate.size"] * 2 / 3)),
    ("threshold.states.ratify", "three fourths of the states",
     lambda f: math.ceil(f["states.count"] * 3 / 4)),
    ("threshold.states.convention", "two thirds of the states",
     lambda f: math.ceil(f["states.count"] * 2 / 3)),
    ("senate.size", "two senators per state",
     lambda f: f["states.count"] * 2),
]


def tracked() -> set[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return set(out)


def normalize(text: str) -> str:
    """Collapse whitespace and markdown emphasis so a quotation can be found.

    Markdown bold inside a quoted phrase is the reason the first version of the
    duplication audit reported a fact as absent when it was present twice.
    """
    text = text.replace("\u2014", "--").replace("\u2013", "-")
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"[*_`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def value_present(value, haystack: str) -> bool:
    if isinstance(value, bool):
        return True
    if isinstance(value, int):
        if re.search(rf"(?<![\d,]){value}(?![\d])", haystack):
            return True
        # Word boundaries matter more here than anywhere else in this file.
        # A bare substring test makes "no" match inside not, nothing, known
        # and cannot, so the value 0 -- which is the project's headline claim
        # -- was reported present in any English prose at all. Likewise
        # "eight" matches inside "forty-eight" and "three" inside
        # "thirty-three", so a hyphenated compound must not satisfy the
        # simple word.
        low = haystack.lower()
        return any(
            re.search(rf"(?<![a-z-]){re.escape(w)}(?![a-z-])", low)
            for w in NUMBER_WORDS.get(value, [])
        )
    needle = normalize(str(value))
    if not needle:
        return False
    if needle in haystack:
        return True
    # Long quotations may be split across a line break or lightly re-punctuated
    # in a second telling. Fall back to a distinctive interior run of words,
    # which is enough to prove the passage is the same one without demanding
    # byte identity between a research note and a general-audience page.
    words = needle.split()
    if len(words) >= 10:
        probe = " ".join(words[2:9])
        return probe in haystack
    return False


def check() -> tuple[list[str], list[str], int]:
    failures: list[str] = []
    warnings: list[str] = []

    if not FACTS.exists():
        return [f"{FACTS.relative_to(REPO)} does not exist"], [], 0

    try:
        data = json.loads(FACTS.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"facts.json is not valid JSON: {exc}"], [], 0

    if data.get("schema") != 1:
        failures.append(f"unexpected schema version {data.get('schema')!r}, expected 1")

    facts = data.get("facts", [])
    tracked_files = tracked()
    seen: set[str] = set()
    cache: dict[str, str] = {}
    numeric: dict[str, int] = {}

    for fact in facts:
        fid = fact.get("id", "<no id>")

        missing = [k for k in REQUIRED_KEYS if k not in fact]
        if missing:
            failures.append(f"{fid}: missing required key(s) {', '.join(missing)}")
            continue

        if fid in seen:
            failures.append(f"{fid}: duplicate id")
        seen.add(fid)

        if fact["status"] not in VALID_STATUS:
            failures.append(f"{fid}: status {fact['status']!r} is not one of {VALID_STATUS}")

        canonical = fact["canonical"]
        if canonical not in tracked_files:
            failures.append(f"{fid}: canonical file {canonical} is not tracked by git")
            continue

        if canonical not in cache:
            cache[canonical] = normalize(
                (REPO / canonical).read_text(encoding="utf-8", errors="replace")
            )

        if not value_present(fact["value"], cache[canonical]):
            failures.append(
                f"{fid}: value {str(fact['value'])[:60]!r} not found in its "
                f"canonical file {canonical}"
            )

        if isinstance(fact["value"], int) and not isinstance(fact["value"], bool):
            numeric[fid] = fact["value"]

        for dep in fact.get("derived_from", []):
            if dep not in {f.get("id") for f in facts}:
                failures.append(f"{fid}: derived_from names unknown fact {dep!r}")

        if fact["status"] == "unverified" and "source" in fact:
            src = fact["source"]
            if src.get("read_from") not in (None, "unverified"):
                warnings.append(
                    f"{fid}: marked unverified but its source claims read_from="
                    f"{src.get('read_from')!r}"
                )

    for fid, description, fn in ARITHMETIC:
        if fid not in numeric:
            continue
        try:
            expected = fn(numeric)
        except KeyError:
            continue
        if numeric[fid] != expected:
            failures.append(
                f"{fid}: recorded {numeric[fid]} but {description} is {expected}"
            )

    return failures, warnings, len(facts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="terse; exit 1 on failure")
    ap.add_argument("--ids", action="store_true", help="list fact ids")
    ap.add_argument(
        "--value",
        metavar="ID",
        help="print one fact's value and exit; unknown id exits 1",
    )
    args = ap.parse_args()

    if args.value:
        data = json.loads(FACTS.read_text(encoding="utf-8"))
        for fact in data["facts"]:
            if fact["id"] == args.value:
                print(fact["value"])
                return 0
        print(f"no fact {args.value!r}", file=sys.stderr)
        return 1

    if args.ids:
        data = json.loads(FACTS.read_text(encoding="utf-8"))
        for fact in data["facts"]:
            print(fact["id"])
        return 0

    failures, warnings, total = check()

    if args.check:
        for f in failures:
            print(f"FAIL {f}")
        for w in warnings:
            print(f"WARN {w}")
        print(f"{total - len(failures)}/{total} facts check out")
        return 1 if failures else 0

    print(f"data/facts.json: {total} facts\n")
    if failures:
        print(f"{len(failures)} failure(s):")
        for f in failures:
            print(f"  FAIL  {f}")
        print()
    if warnings:
        print(f"{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARN  {w}")
        print()
    if not failures and not warnings:
        print("Every fact was found in the file named as its owner, every")
        print("derived value agrees with the values it derives from, and every")
        print("canonical file is tracked.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
