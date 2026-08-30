"""Why the Article I Section 5 quorum cascade cannot lower the Article V price.

STATUS: NULL RESULT, machine-checked. This is the disposition of the cascade
    recorded as an open question in silence-inventory.md and computed in
    quorum_cascade.py. The write-up is quorum-cascade-null.md.

    The cascade's load-bearing premise turned out to be TRUE. The quorum base
    really is members chosen and sworn, so a vacancy really does lower the
    denominator of Article V's fraction. See quorum-base.md, which verifies it
    from the page images of Hinds' Precedents sections 2889 and 2891.

    The cascade fails anyway, and it fails on arithmetic rather than on law.
    Running it costs more members than the thing it was supposed to make cheap.

THE ARGUMENT

    Let n be the number of members a chamber has as it stands.

    A quorum is a majority of them, Art. I Sec. 5 cl. 1:

        quorum(n) = floor(n/2) + 1

    An Article V proposal needs two thirds of those present, and a coalition
    that wants the smallest possible number wants exactly a quorum present and
    nobody else, National Prohibition Cases, 253 U.S. 350 (1920):

        articleV(n) = ceil(2 * quorum(n) / 3)

    PREMISE P. Any manoeuvre that changes who is a member is business of the
    chamber, so it needs a quorum present, and the bloc driving it must be able
    to supply that quorum from its own ranks, because the members it is about
    to remove will not stay to help. So the bloc costs at least quorum(n).

    THEOREM. For every n >= 4, articleV(n) < quorum(n).

    So under P, the entry price of the cascade is strictly greater than the
    price of simply proposing the amendment. Any coalition large enough to
    start shrinking the chamber was already large enough to propose without
    shrinking anything. The manoeuvre is strictly dominated at step zero, and
    no later step can rescue it, because the coalition has already been paid.

WHAT THIS DOES AND DOES NOT RULE OUT

    It rules out the cascade in quorum_cascade.py, and every variant that has
    to begin by carrying a vote in the undiminished chamber.

    It does not rule out a chamber that is ALREADY small for reasons nobody
    engineered: mass resignation, a refusal to be sworn, an epidemic, a war.
    articleV falls with n whatever causes n to fall. That is a real property of
    the 1920 reading and it is recorded in threshold-arithmetic.md. What the
    theorem denies is that a coalition can profitably manufacture that state,
    because manufacturing it is dearer than the state is worth.

    It says nothing whatever about ratification. Article V still needs three
    fourths of the state legislatures, which no congressional manoeuvre reaches.
    That was already the cascade's disqualification and it still is.
"""

import json
import math
from pathlib import Path

HOUSE_1947 = 435
SENATE_1947 = 96

EXHAUSTIVE_LIMIT = 200_000


def quorum(n: int) -> int:
    """A Majority of each. Art. I Sec. 5 cl. 1."""
    return n // 2 + 1


def article_v(n: int) -> int:
    """Two thirds of a quorum, the 1920 reading, with only a quorum present."""
    return math.ceil(2 * quorum(n) / 3)


def exhaustive(limit: int = EXHAUSTIVE_LIMIT):
    """Every chamber size up to limit. Returns the sizes where the theorem fails."""
    return [n for n in range(1, limit + 1) if not article_v(n) < quorum(n)]


def z3_proof():
    """Prove the theorem for ALL n >= 4, not merely up to a limit.

    Negate the theorem and ask Z3 for a counterexample. unsat is the proof.
    """
    from z3 import Int, Solver, unsat

    n, q, t = Int("n"), Int("q"), Int("t")
    s = Solver()
    s.add(n >= 4)
    # q == n // 2 + 1, written without division so the encoding is checkable.
    s.add(2 * q - 2 <= n, n <= 2 * q - 1)
    # t == ceil(2q / 3): the least integer with 3t >= 2q.
    s.add(3 * t >= 2 * q, 3 * t <= 2 * q + 2)
    # The negation of what we want to prove.
    s.add(t >= q)
    return s.check() == unsat


def z3_negative_control():
    """The same query with the n >= 4 guard dropped MUST find a counterexample.

    n = 1, 2 and 3 really are exceptions, so a solver that reports unsat here is
    broken or the encoding is vacuous. This control is the reason to believe the
    unsat above means anything.
    """
    from z3 import Int, Solver, sat

    n, q, t = Int("n"), Int("q"), Int("t")
    s = Solver()
    s.add(n >= 1)
    s.add(2 * q - 2 <= n, n <= 2 * q - 1)
    s.add(3 * t >= 2 * q, 3 * t <= 2 * q + 2)
    s.add(t >= q)
    if s.check() != sat:
        return None
    return s.model()[n].as_long()


def main():
    failures = exhaustive()
    proved = z3_proof()
    control = z3_negative_control()

    # The 1947 vantage, from quorum_cascade.py's own recorded output.
    entry_price = quorum(HOUSE_1947) + quorum(SENATE_1947)
    propose_price = article_v(HOUSE_1947) + article_v(SENATE_1947)

    print("=== THEOREM: two thirds of a quorum is cheaper than a quorum ===")
    print(f"  exhaustive check, n = 1..{EXHAUSTIVE_LIMIT}")
    print(f"    sizes where the theorem fails : {failures}")
    print(f"    all of them below n = 4       : {all(n < 4 for n in failures)}")
    print(f"  Z3, for all n >= 4              : {'PROVED' if proved else 'NOT PROVED'}")
    print(f"  Z3 negative control, n >= 1     : counterexample n={control}")

    print("\n=== THE CASCADE AT THE 1947 VANTAGE ===")
    print(f"  cheapest bloc that can carry an Article V proposal outright : {propose_price}")
    print(f"    House {article_v(HOUSE_1947)} + Senate {article_v(SENATE_1947)}")
    print(f"  cheapest bloc that can even BEGIN the cascade               : {entry_price}")
    print(f"    House {quorum(HOUSE_1947)} + Senate {quorum(SENATE_1947)}")
    print(f"  the cascade costs an extra                                  : "
          f"{entry_price - propose_price} members")

    print("\n=== VERDICT ===")
    print("  THE CASCADE IS STRICTLY DOMINATED AT STEP ZERO.")
    print("  Any coalition able to start it could already have proposed the")
    print("  amendment without it. The manoeuvre is not a loophole; it is a")
    print("  more expensive way to buy something already on the shelf.")
    print("  Article V still requires three fourths of the state legislatures,")
    print("  which this manoeuvre never approaches. That disqualification stands.")

    ok = proved and control is not None and all(n < 4 for n in failures)
    out = {
        "vantage": "United States, December 5, 1947",
        "status": "NULL RESULT -- the cascade is strictly dominated",
        "theorem": "for all n >= 4, ceil(2 * (n//2 + 1) / 3) < n//2 + 1",
        "premise": ("any manoeuvre that changes the membership is business of the "
                    "chamber, so it needs a quorum, and the bloc must supply that "
                    "quorum itself because the members it removes will not"),
        "exhaustive_limit": EXHAUSTIVE_LIMIT,
        "exhaustive_failures": failures,
        "z3_proved_for_all_n_ge_4": proved,
        "z3_negative_control_counterexample": control,
        "vantage_numbers": {
            "propose_outright": propose_price,
            "begin_cascade": entry_price,
            "extra_cost": entry_price - propose_price,
        },
        "all_checks_passed": ok,
    }
    p = Path(__file__).with_name("cascade_domination.json")
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"\n  wrote {p.name}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
