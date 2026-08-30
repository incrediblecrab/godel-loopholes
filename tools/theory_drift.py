#!/usr/bin/env python3
"""Guard the one place this repository keeps two models on purpose.

`GodelCore.thy` is the transcription of Zahoransky & Benzmueller. `GodelNetAddCore.thy`
is the repaired model, and it is a separate theory rather than an import because
importing would drag in the very axioms the repair exists to replace. That decision
is right, and it has a cost: the modal-logic scaffolding is now written out twice and
can drift apart silently, which is exactly the failure section 5b of verify.sh was
built to prevent.

So the invariant is not "the model appears once". It is:

  every definition the two cores share is character-for-character identical,
  except for a short, named list of deliberate differences.

A difference that is not on that list is drift, and it fails. Adding to the list is a
deliberate act that shows up in a diff, which is the point.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

THY = Path(__file__).resolve().parent.parent / "analysis/united-states-1947/isabelle"
PUBLISHED = THY / "GodelCore.thy"
REPAIRED = THY / "GodelNetAddCore.thy"

# Definitions that are SUPPOSED to differ between the published model and the
# repaired one. Each needs a reason, because each is a hole in the guard.
INTENDED_DIFFERENCES = {
    "amd1a": "the repair: the first amendment repeals the entrenchment clause's force, "
             "not the clause, so amd1a is stated against in_force_omsp",
}

# Definitions that exist in only one of the two models, and why.
INTENDED_PUBLISHED_ONLY = {
    "omsp": "the published model's entrenchment clause, replaced by comsp",
    "amd1b": "the published model's alternative first amendment, not used by the repair",
}
INTENDED_REPAIRED_ONLY = {
    "comsp": "the entrenchment clause, separated from whether it is in force",
    "pvr": "proposal validity: the rule that makes a proposal derived rather than asserted",
}

HEAD = re.compile(r"^(definition|abbreviation|datatype|type_synonym)\s+(\S+)")


def definitions(path: Path) -> dict[str, list[str]]:
    """Map each top-level definition name to its verbatim lines."""
    out: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text().splitlines():
        head = HEAD.match(line)
        if head:
            current = head.group(2)
            out[current] = [line.rstrip()]
        elif current and line.strip() and line[:1] in " \t":
            out[current].append(line.rstrip())
        elif current and not line.strip():
            current = None
    return out


def main() -> int:
    for path in (PUBLISHED, REPAIRED):
        if not path.exists():
            print(f"DRIFT CHECK UNAVAILABLE: {path} is missing")
            return 2

    pub = definitions(PUBLISHED)
    rep = definitions(REPAIRED)

    shared = sorted(set(pub) & set(rep))
    identical = [k for k in shared if pub[k] == rep[k]]
    differing = sorted(k for k in shared if pub[k] != rep[k])

    failures: list[str] = []

    unexplained = [k for k in differing if k not in INTENDED_DIFFERENCES]
    if unexplained:
        failures.append(
            "shared definitions differ without being declared deliberate: "
            + ", ".join(unexplained)
        )

    stale = [k for k in INTENDED_DIFFERENCES if k not in differing]
    if stale:
        failures.append(
            "declared a deliberate difference that no longer differs: " + ", ".join(stale)
        )

    pub_only = sorted(set(pub) - set(rep))
    rep_only = sorted(set(rep) - set(pub))
    for names, allowed, side in (
        (pub_only, INTENDED_PUBLISHED_ONLY, "published"),
        (rep_only, INTENDED_REPAIRED_ONLY, "repaired"),
    ):
        rogue = [k for k in names if k not in allowed]
        if rogue:
            failures.append(
                f"undeclared definition present only in the {side} model: " + ", ".join(rogue)
            )

    print(f"shared definitions: {len(shared)}")
    print(f"character-identical: {len(identical)}")
    print(f"deliberately different: {len(differing)} ({', '.join(differing) or 'none'})")
    print(f"published-model only: {', '.join(pub_only) or 'none'}")
    print(f"repaired-model only: {', '.join(rep_only) or 'none'}")

    if failures:
        for f in failures:
            print(f"DRIFT: {f}")
        return 1

    print(
        f"RESULT: the two cores share {len(shared)} definitions, {len(identical)} of them "
        f"character-identical, and every difference is declared"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
