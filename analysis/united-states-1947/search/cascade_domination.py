"""Verify the scalar inequality previously overinterpreted as cascade domination.

For n >= 4, ceil(2 * (floor(n/2) + 1) / 3) < floor(n/2) + 1.
This arithmetic remains true. Its former coalition interpretation compared
favorable attendance for direct proposal with self-supplied quorum for exclusion.
Those are different assumptions, not a strict cost-domination theorem.

The legacy 179/267 numbers and their difference are retained as arithmetic
records, not consistent-attendance prices. attendance_audit.py supplies the
correct comparison. Neither script validates a complete constitutional path or
changes the separate state-ratification requirement.
"""

import json
from pathlib import Path

HOUSE_1947 = 435
SENATE_1947 = 96

EXHAUSTIVE_LIMIT = 200_000


def quorum(n: int) -> int:
    """A Majority of each. Art. I Sec. 5 cl. 1."""
    return n // 2 + 1


def article_v(n: int) -> int:
    """Two thirds of a quorum, the 1920 reading, with only a quorum present."""
    return (2 * quorum(n) + 2) // 3


def exhaustive(limit: int = EXHAUSTIVE_LIMIT):
    """Every chamber size up to limit. Returns the sizes where the theorem fails."""
    return [n for n in range(1, limit + 1) if not article_v(n) < quorum(n)]


def z3_proof():
    """Prove the theorem for ALL n >= 4, not merely up to a limit.

    Negate the theorem and ask Z3 for a counterexample. unsat is the proof.
    """
    from z3 import Int, Solver

    n, q, t = Int("n"), Int("q"), Int("t")
    s = Solver()
    s.add(n >= 4)
    # q == n // 2 + 1, written without division so the encoding is checkable.
    s.add(2 * q - 2 <= n, n <= 2 * q - 1)
    # t == ceil(2q / 3): the least integer with 3t >= 2q.
    s.add(3 * t >= 2 * q, 3 * t <= 2 * q + 2)
    # The negation of what we want to prove.
    s.add(t >= q)
    s.set(timeout=30_000)
    return s.check()


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
    s.set(timeout=30_000)
    verdict = s.check()
    return str(verdict).upper(), s.model()[n].as_long() if verdict == sat else None


def main():
    failures = exhaustive()
    proof_status = str(z3_proof()).upper()
    proved = proof_status == "UNSAT"
    control_status, control = z3_negative_control()

    # The 1947 vantage, from quorum_cascade.py's own recorded output.
    entry_price = quorum(HOUSE_1947) + quorum(SENATE_1947)
    propose_price = article_v(HOUSE_1947) + article_v(SENATE_1947)

    print("=== THEOREM: two thirds of a quorum is smaller than a quorum ===")
    print(f"  exhaustive check, n = 1..{EXHAUSTIVE_LIMIT}")
    print(f"    sizes where the theorem fails : {failures}")
    print(f"    all of them below n = 4       : {all(n < 4 for n in failures)}")
    print(f"  Z3, for all n >= 4              : {'PROVED' if proved else 'NOT PROVED'}")
    print(f"  Z3 counterexample-search status : {proof_status}")
    print(f"  Z3 negative control, n >= 1     : counterexample n={control}")
    print(f"  Z3 negative-control status      : {control_status}")

    print("\n=== THE CASCADE AT THE 1947 VANTAGE ===")
    print(f"  favorable-quorum direct proposal : {propose_price}")
    print(f"    House {article_v(HOUSE_1947)} + Senate {article_v(SENATE_1947)}")
    print(f"  self-quorate cascade entry       : {entry_price}")
    print(f"    House {quorum(HOUSE_1947)} + Senate {quorum(SENATE_1947)}")
    print(f"  mixed-assumption difference      : {entry_price - propose_price}")

    print("\n=== VERDICT ===")
    print("  THE SCALAR THEOREM DOES NOT ESTABLISH STRICT COALITION-COST DOMINATION.")
    print("  The displayed prices use different attendance assumptions.")
    print("  Use attendance_audit.py for consistent-attendance comparisons.")
    print("  Article V still requires three fourths of the state legislatures,")
    print("  which this manoeuvre never approaches. That disqualification stands.")

    ok = proved and control_status == "SAT" and control in (1, 2, 3) and failures == [1, 2, 3]
    out = {
        "vantage": "United States, December 5, 1947",
        "status": "SCALAR ARITHMETIC VERIFIED -- not a cost-domination proof" if ok else "INCOMPLETE",
        "theorem": "for all n >= 4, ceil(2 * (n//2 + 1) / 3) < n//2 + 1",
        "premise": ("the former cost interpretation assumed self-supplied quorum for "
                    "cascade entry but favorable attendance for direct proposal; "
                    "that asymmetric comparison does not establish strict domination"),
        "exhaustive_limit": EXHAUSTIVE_LIMIT,
        "exhaustive_failures": failures,
        "z3_proved_for_all_n_ge_4": proved,
        "z3_counterexample_search_status": proof_status,
        "z3_negative_control_counterexample": control,
        "z3_negative_control_status": control_status,
        "consistent_attendance_comparison": False,
        "legacy_vantage_labels": "extra_cost is a mixed-assumption difference, not a proved extra coalition cost",
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
