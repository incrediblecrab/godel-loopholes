#!/usr/bin/env python3
"""Measure WCAG contrast for every foreground/background pair in the palette.

Eyeballing contrast is the design equivalent of reading a number off a solver
and writing an English sentence beside it that says something else. This reads
the pairs out of site/src/styles/tokens.css and computes them, so a palette
change that breaks legibility fails the harness instead of shipping.

  python3 tools/contrast.py            # table
  python3 tools/contrast.py --check    # exit 1 if any required pair fails
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKENS = REPO / "site" / "src" / "styles" / "tokens.css"

# WCAG 2.1 minimums. Body text is normal-size, so 4.5. Large text and non-text
# indicators are 3.0. Nothing here is allowed to rely on the large-text
# exemption for something a reader has to read at reading size.
AA_NORMAL = 4.5
AA_LARGE = 3.0

# (foreground token, background token, minimum, what it is used for)
REQUIRED = [
    ("ink", "paper", AA_NORMAL, "body prose"),
    ("ink", "paper-sunk", AA_NORMAL, "prose on a recessed panel"),
    ("ink", "paper-raised", AA_NORMAL, "prose on the lifted surface"),
    ("ink-muted", "paper", AA_NORMAL, "margin apparatus and captions"),
    ("ink-muted", "paper-sunk", AA_NORMAL, "apparatus on a recessed panel"),
    ("ink-faint", "paper", AA_LARGE, "the quietest tier, never body text"),
    ("verified", "paper", AA_NORMAL, "verified status text"),
    ("disproved", "paper", AA_NORMAL, "disproved status text"),
    ("inconclusive", "paper", AA_NORMAL, "inconclusive status text"),
    ("verified", "verified-tint", AA_NORMAL, "verified text on its own tint"),
    ("disproved", "disproved-tint", AA_NORMAL, "disproved text on its own tint"),
    ("inconclusive", "inconclusive-tint", AA_NORMAL, "inconclusive text on its tint"),
    # --rule and --rule-strong are deliberately absent. They are decorative
    # hairlines and table borders, and WCAG 1.4.11 does not require 3:1 of a
    # border that conveys no information on its own. --graphic is the token for
    # anything a reader has to see to understand the content, and that one is
    # required to meet 3:1 in both schemes.
    ("graphic", "paper", AA_LARGE, "axes, bars and meaningful outlines"),
    ("graphic-strong", "paper", AA_LARGE, "emphasised graphic elements"),
    ("graphic", "paper-sunk", AA_LARGE, "graphics on a recessed panel"),
]


def parse_blocks(css: str) -> tuple[dict[str, str], dict[str, str]]:
    """Return (light, dark) token maps.

    The dark block is the one inside the prefers-color-scheme media query; the
    light block is everything before it.
    """
    idx = css.find("prefers-color-scheme: dark")
    light_src = css if idx == -1 else css[:idx]
    dark_src = "" if idx == -1 else css[idx:]

    def grab(src: str) -> dict[str, str]:
        return {
            m.group(1): m.group(2).lower()
            for m in re.finditer(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})\b", src)
        }

    light = grab(light_src)
    dark = dict(light)
    dark.update(grab(dark_src))
    return light, dark


def luminance(hex_colour: str) -> float:
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = channel(r), channel(g), channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def evaluate() -> tuple[list[tuple], list[str]]:
    if not TOKENS.exists():
        return [], [f"{TOKENS.relative_to(REPO)} does not exist"]

    css = TOKENS.read_text(encoding="utf-8")
    light, dark = parse_blocks(css)

    rows: list[tuple] = []
    failures: list[str] = []

    for scheme, tokens in (("light", light), ("dark", dark)):
        for fg, bg, minimum, use in REQUIRED:
            if fg not in tokens or bg not in tokens:
                failures.append(f"{scheme}: token --{fg} or --{bg} is missing")
                continue
            r = ratio(tokens[fg], tokens[bg])
            passed = r >= minimum
            rows.append((scheme, fg, bg, tokens[fg], tokens[bg], r, minimum, passed, use))
            if not passed:
                failures.append(
                    f"{scheme}: --{fg} on --{bg} is {r:.2f}:1, below the "
                    f"{minimum}:1 required for {use}"
                )

    # A stray non-hex character in a colour value produces a token that simply
    # does not parse, and a missing token is a silent failure rather than a
    # loud one. Catch any custom property whose value looks like a colour but
    # is not a well-formed six-digit hex.
    for m in re.finditer(r"--([a-z0-9-]+):\s*(#[^;\s]*)", css):
        value = m.group(2)
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            failures.append(f"--{m.group(1)} has a malformed colour value {value!r}")

    return rows, failures


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="terse; exit 1 on failure")
    args = ap.parse_args()

    rows, failures = evaluate()

    if args.check:
        for f in failures:
            print(f"FAIL {f}")
        print(f"{len(rows) - len(failures)}/{len(rows)} contrast pairs meet WCAG AA")
        return 1 if failures else 0

    print(f"{TOKENS.relative_to(REPO)}\n")
    header = f"{'scheme':<6} {'foreground':<14} {'background':<18} {'ratio':>7}  {'min':>4}  result"
    print(header)
    print("-" * len(header))
    for scheme, fg, bg, fgv, bgv, r, minimum, passed, use in rows:
        mark = "pass" if passed else "FAIL"
        print(f"{scheme:<6} {fg:<14} {bg:<18} {r:>6.2f}:1  {minimum:>4}  {mark}  {use}")
    print()
    if failures:
        print(f"{len(failures)} failure(s):")
        for f in failures:
            print(f"  {f}")
    else:
        print("Every required pair meets WCAG AA at its intended size.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
