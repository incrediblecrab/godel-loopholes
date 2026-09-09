"""Compare initial congressional voting costs under identical attendance assumptions."""

import argparse
import hashlib
import json
from pathlib import Path

import z3

from state_admission import Attendance, majority_required, proposal_required


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "attendance_audit_results.json"
CHAMBERS = {"House": 435, "Senate": 96}


def _validate(members: int, attendance: Attendance) -> None:
    if type(members) is not int or members < 1:
        raise ValueError("Members must be a positive integer")
    if not isinstance(attendance, Attendance):
        raise ValueError("An explicit Attendance convention is required")


def brute_minimum(members: int, attendance: Attendance, *, two_thirds: bool) -> int:
    _validate(members, attendance)
    eligible = []
    for present in range(1, members + 1):
        if 2 * present <= members:
            continue
        if attendance == Attendance.FULL and present != members:
            continue
        if attendance == Attendance.FAVORABLE and 2 * (present - 1) > members:
            continue
        for yes in range(present + 1):
            if attendance == Attendance.SELF_QUORATE and yes != present:
                continue
            passes = 3 * yes >= 2 * present if two_thirds else 2 * yes > present
            if passes:
                eligible.append(yes)
    if not eligible:
        raise AssertionError("A unanimously supporting chamber should be feasible")
    return min(eligible)


def _vote_constraints(members, present, yes, attendance, two_thirds):
    conditions = [present <= members, 2 * present > members, yes >= 0, yes <= present]
    if attendance == Attendance.FULL:
        conditions.append(present == members)
    elif attendance == Attendance.FAVORABLE:
        conditions.append(2 * (present - 1) <= members)
    elif attendance == Attendance.SELF_QUORATE:
        conditions.append(yes == present)
    else:
        raise ValueError(f"Unknown attendance convention: {attendance!r}")
    conditions.append(3 * yes >= 2 * present if two_thirds else 2 * yes > present)
    return conditions


def smt_minimum(members: int, attendance: Attendance, *, two_thirds: bool) -> dict:
    _validate(members, attendance)
    present, yes = z3.Ints("attendance_present attendance_yes")
    constraints = _vote_constraints(members, present, yes, attendance, two_thirds)
    optimizer = z3.Optimize()
    optimizer.set(timeout=30_000)
    optimizer.add(*constraints)
    optimizer.minimize(yes)
    verdict = optimizer.check()
    if verdict == z3.unknown:
        return {"status": "UNKNOWN", "reason": optimizer.reason_unknown()}
    if verdict != z3.sat:
        raise RuntimeError(f"Unanimous-vote feasibility control failed: {verdict}")
    model = optimizer.model()
    minimum = model.eval(yes).as_long()
    observed_present = model.eval(present).as_long()
    checker = z3.Solver()
    checker.set(timeout=30_000)
    checker.add(*constraints, yes < minimum)
    verdict = checker.check()
    if verdict == z3.unknown:
        return {"status": "UNKNOWN", "reason": checker.reason_unknown()}
    if verdict != z3.unsat:
        raise AssertionError("A smaller voting coalition exists")
    return {
        "status": "OPTIMAL", "yes": minimum, "present": observed_present,
        "smaller_coalition": "UNSAT",
    }


def general_controls() -> dict:
    n, present, yes = z3.Ints("attendance_n attendance_p attendance_y")
    q = n / 2 + 1
    claims = {
        "full_majority_not_costlier_than_two_thirds": (
            [n >= 1], n / 2 + 1 <= (2 * n + 2) / 3,
        ),
        "majority_strictly_cheaper_with_at_least_seven_voters": (
            [n >= 7], n / 2 + 1 < (2 * n + 2) / 3,
        ),
        "favorable_majority_not_costlier_than_two_thirds": (
            [n >= 1], q / 2 + 1 <= (2 * q + 2) / 3,
        ),
        "legacy_scalar_inequality": ([n >= 4], (2 * q + 2) / 3 < q),
    }
    for name, two_thirds in (("majority", False), ("two_thirds", True)):
        claims[f"self_quorate_{name}_cannot_use_fewer_than_quorum"] = (
            [n >= 1, *_vote_constraints(
                n, present, yes, Attendance.SELF_QUORATE, two_thirds,
            )],
            yes >= q,
        )
        claims[f"self_quorate_{name}_quorum_witness_always_works"] = (
            [n >= 1],
            z3.And(*_vote_constraints(n, q, q, Attendance.SELF_QUORATE, two_thirds)),
        )
    results = {}
    for name, (domain, claim) in claims.items():
        solver = z3.Solver()
        solver.set(timeout=30_000)
        solver.add(*domain, z3.Not(claim))
        verdict = solver.check()
        if verdict != z3.unsat:
            raise RuntimeError(f"{name}: expected UNSAT, got {verdict}")
        results[name] = "UNSAT"
    solver = z3.Solver()
    solver.set(timeout=30_000)
    solver.add(n == 1, (2 * q + 2) / 3 >= q)
    verdict = solver.check()
    if verdict != z3.sat:
        raise RuntimeError(f"Unguarded-inequality negative control: {verdict}")
    results["legacy_inequality_without_n_ge_4_at_n_1"] = "SAT"
    solver = z3.Solver()
    solver.set(timeout=30_000)
    solver.add(n == 6, n / 2 + 1 >= (2 * n + 2) / 3)
    verdict = solver.check()
    if verdict != z3.sat:
        raise RuntimeError(f"Incorrect n >= 5 strict-majority claim control: {verdict}")
    results["strict_majority_advantage_does_not_hold_at_six_voters"] = "SAT"
    return results


def run() -> dict:
    rows = {}
    for attendance in Attendance:
        chambers = {}
        for chamber, members in CHAMBERS.items():
            majority = majority_required(members, attendance)
            proposal = proposal_required(members, attendance)
            solved_majority = smt_minimum(members, attendance, two_thirds=False)
            solved_proposal = smt_minimum(members, attendance, two_thirds=True)
            if any(row["status"] != "OPTIMAL" for row in (solved_majority, solved_proposal)):
                raise RuntimeError(f"Inconclusive attendance optimization: {attendance}/{chamber}")
            if (majority, proposal) != (solved_majority["yes"], solved_proposal["yes"]):
                raise AssertionError("Closed forms and direct voting constraints disagree")
            chambers[chamber] = {
                "members": members,
                "majority_exclusion": majority,
                "two_thirds_expulsion": proposal,
                "article_v_proposal": proposal,
                "smt_majority": solved_majority,
                "smt_two_thirds": solved_proposal,
            }
        totals = {
            key: sum(chamber[key] for chamber in chambers.values())
            for key in ("majority_exclusion", "two_thirds_expulsion", "article_v_proposal")
        }
        rows[attendance.value] = {"chambers": chambers, "totals": totals}
    return {
        "schema_version": 1,
        "scope": {
            "vantage": "December 5, 1947",
            "chamber_membership": "Assume all 435 House and 96 Senate seats chosen and sworn",
            "measurement": "Initial yes-vote/supporter counts, not complete constitutional paths",
            "attendance": "Same convention on each side of each comparison",
            "ballots": "Every present member votes yes or no; no abstentions or VP tie-break",
            "majority_exclusion_authority": "CONTESTED; not established by these inequalities",
            "later_cascade_steps_and_seat_refilling": "NOT MODELED",
            "state_ratification": "36 of 48 remains a separate gate",
        },
        "source_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in ("attendance_audit.py", "test_attendance_audit.py", "state_admission.py")
        },
        "rows": rows,
        "legacy_mixed_comparison": {
            "cascade_entry_self_quorate": rows[Attendance.SELF_QUORATE.value]["totals"]["majority_exclusion"],
            "direct_proposal_favorable": rows[Attendance.FAVORABLE.value]["totals"]["article_v_proposal"],
            "same_attendance_assumption": False,
            "strict_cost_domination_established": False,
        },
        "general_counterexample_searches": general_controls(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--write", action="store_true")
    actions.add_argument("--check", action="store_true")
    args = parser.parse_args()
    results = run()
    print(json.dumps({key: row["totals"] for key, row in results["rows"].items()}, indent=2))
    if args.write:
        RESULTS.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.check:
        if not RESULTS.is_file() or json.loads(RESULTS.read_text(encoding="utf-8")) != results:
            raise SystemExit("Missing or stale attendance-audit artifact")
        print("Attendance audit artifact matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
