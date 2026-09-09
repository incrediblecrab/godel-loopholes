"""Conditional arithmetic replication of the Harvard Law Review's Pack the Union.

New-state votes are inputs, not consequences of admission. The House-expansion
convention and attendance scenarios are explicit; no geographic partition or
binding promise of future ratification is inferred from these inequalities.
"""

import argparse
from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from pathlib import Path

import z3

from article_v_model import (
    Policy, Suffrage, Support, Target, Votes, explore, quorum_votes,
)


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "state_admission_results.json"


class Attendance(str, Enum):
    FULL = "full_membership"
    FAVORABLE = "favorable_minimum_quorum"
    SELF_QUORATE = "supporters_supply_quorum"


@dataclass(frozen=True)
class Scenario:
    states: int
    house_seats: int
    house_support: int
    senate_support: int
    old_ratifiers: int
    attendance: Attendance = Attendance.FULL
    president_cooperates: bool = True

    def __post_init__(self):
        if self.states < 1 or self.house_seats < 1:
            raise ValueError("Initial state and House counts must be positive")
        if not 0 <= self.house_support <= self.house_seats:
            raise ValueError("House support exceeds the chamber or is negative")
        if not 0 <= self.senate_support <= 2 * self.states:
            raise ValueError("Senate support exceeds the chamber or is negative")
        if not 0 <= self.old_ratifiers <= self.states:
            raise ValueError("Old ratifiers must identify a possible number of old states")


def ratification_reached(states: int, old_yes: int, added: int, new_yes: int) -> bool:
    if states < 1 or not 0 <= old_yes <= states or added < 0 or not 0 <= new_yes <= added:
        raise ValueError("Invalid state or ratification counts")
    return 4 * (old_yes + new_yes) >= 3 * (states + added)


def minimum_all_supporting_additions(states: int, old_yes: int) -> int:
    ratification_reached(states, old_yes, 0, 0)
    return max(0, 3 * states - 4 * old_yes)


def proposal_required(seats: int, attendance: Attendance) -> int:
    votes = quorum_votes(seats)
    if attendance == Attendance.FULL:
        return (2 * seats + 2) // 3
    if attendance == Attendance.FAVORABLE:
        return votes.yes
    if attendance == Attendance.SELF_QUORATE:
        return votes.present
    raise ValueError(f"Unknown attendance convention: {attendance!r}")


def admission_required(seats: int, scenario: Scenario) -> int:
    if not scenario.president_cooperates:
        return proposal_required(seats, scenario.attendance)
    if scenario.attendance == Attendance.FULL:
        return seats // 2 + 1
    if scenario.attendance == Attendance.FAVORABLE:
        return quorum_votes(seats).present // 2 + 1
    if scenario.attendance == Attendance.SELF_QUORATE:
        return quorum_votes(seats).present
    raise ValueError(f"Unknown attendance convention: {scenario.attendance!r}")


def admission_can_begin(scenario: Scenario) -> bool:
    return (
        scenario.house_support >= admission_required(scenario.house_seats, scenario)
        and scenario.senate_support >= admission_required(2 * scenario.states, scenario)
    )


def gates(scenario: Scenario, added: int) -> dict[str, bool]:
    if added < 0:
        raise ValueError("Added states cannot be negative")
    return {
        "house_proposal": scenario.house_support + added >= proposal_required(
            scenario.house_seats + added, scenario.attendance,
        ),
        "senate_proposal": scenario.senate_support + 2 * added >= proposal_required(
            2 * (scenario.states + added), scenario.attendance,
        ),
        "state_ratification": ratification_reached(
            scenario.states, scenario.old_ratifiers, added, added,
        ),
    }


def enumerate_minimum(scenario: Scenario) -> dict:
    if all(gates(scenario, 0).values()):
        return {"status": "FEASIBLE", "new_states": 0, "admission_needed": False}
    if not admission_can_begin(scenario):
        return {
            "status": "BLOCKED", "new_states": None,
            "reason": "The original Congress cannot authorize admission under the stated attendance/veto inputs",
        }
    # Even from zero support, these bounds suffice when every added delegation
    # and ratifying state is assumed supportive. They are not a political model.
    bound = max(3 * scenario.states, 2 * scenario.house_seats)
    for added in range(bound + 1):
        if all(gates(scenario, added).values()):
            return {
                "status": "FEASIBLE",
                "new_states": added,
                "admission_needed": added > 0,
                "expanded_states": scenario.states + added,
                "ratifying_states": scenario.old_ratifiers + added,
                "ratification_threshold": (3 * (scenario.states + added) + 3) // 4,
                "house_yes": scenario.house_support + added,
                "house_seats": scenario.house_seats + added,
                "senate_yes": scenario.senate_support + 2 * added,
                "senate_seats": 2 * (scenario.states + added),
                "one_fewer_gates": gates(scenario, added - 1) if added else None,
            }
    raise AssertionError("Constructive search bound failed")


def _symbolic_proposal(seats, attendance: Attendance):
    if attendance == Attendance.FULL:
        return (2 * seats + 2) / 3
    quorum = seats / 2 + 1
    if attendance == Attendance.FAVORABLE:
        return (2 * quorum + 2) / 3
    if attendance == Attendance.SELF_QUORATE:
        return quorum
    raise ValueError(f"Unknown attendance convention: {attendance!r}")


def smt_minimum(scenario: Scenario) -> dict:
    added = z3.Int("additional_states")
    house = scenario.house_seats + added
    senate = 2 * (scenario.states + added)
    constraints = [
        added >= 0,
        z3.Or(added == 0, z3.BoolVal(admission_can_begin(scenario))),
        scenario.house_support + added >= _symbolic_proposal(house, scenario.attendance),
        scenario.senate_support + 2 * added >= _symbolic_proposal(senate, scenario.attendance),
        4 * (scenario.old_ratifiers + added) >= 3 * (scenario.states + added),
    ]
    optimizer = z3.Optimize()
    optimizer.set(timeout=30_000)
    optimizer.add(*constraints)
    optimizer.minimize(added)
    verdict = optimizer.check()
    if verdict == z3.unknown:
        return {"status": "UNKNOWN", "reason": optimizer.reason_unknown()}
    if verdict == z3.unsat:
        return {"status": "BLOCKED", "new_states": None}
    if verdict != z3.sat:
        raise RuntimeError(f"Unexpected optimization result: {verdict}")
    minimum = optimizer.model().eval(added).as_long()
    exclusion = z3.Solver()
    exclusion.set(timeout=30_000)
    exclusion.add(*constraints, added < minimum)
    verdict = exclusion.check()
    if verdict == z3.unknown:
        return {"status": "UNKNOWN", "reason": exclusion.reason_unknown()}
    if verdict != z3.unsat:
        raise AssertionError("The optimization witness is not a minimum")
    return {"status": "FEASIBLE", "new_states": minimum, "smaller_solution": "UNSAT"}


def general_controls() -> dict:
    states, old, added = z3.Ints("states old added")
    domain = [states >= 1, old >= 0, old <= states, added >= 0]
    solver = z3.Solver()
    solver.set(timeout=30_000)
    solver.add(*domain, (
        (4 * (old + added) >= 3 * (states + added)) != (added >= 3 * states - 4 * old)
    ))
    equivalence = solver.check()
    solver = z3.Solver()
    solver.set(timeout=30_000)
    solver.add(*domain, 4 * old < 3 * states, 4 * old >= 3 * (states + added))
    uncommitted_votes = solver.check()
    for name, verdict in (
        ("closed-form equivalence", equivalence), ("no guaranteed new support", uncommitted_votes),
    ):
        if verdict != z3.unsat:
            raise RuntimeError(f"{name}: expected UNSAT, obtained {verdict}; no theorem reported")
    cases = 0
    for count in range(1, 201):
        for supporting in range(count + 1):
            minimum = minimum_all_supporting_additions(count, supporting)
            if not ratification_reached(count, supporting, minimum, minimum):
                raise AssertionError("Claimed minimum is infeasible")
            if minimum and ratification_reached(count, supporting, minimum - 1, minimum - 1):
                raise AssertionError("A smaller feasible count exists")
            cases += 1
    return {
        "closed_form_equivalence_counterexample_search": str(equivalence).upper(),
        "below_threshold_old_states_succeed_without_any_new_support": str(uncommitted_votes).upper(),
        "boundary_cases_checked": cases,
        "initial_states_exhaustively_checked": [1, 200],
        "fixed_denominator_negative_control": {
            "initial_states": 48, "old_ratifiers": 0, "added_states": 36,
            "incorrect_old_denominator_says_pass": 4 * 36 >= 3 * 48,
            "correct_expanded_denominator_says_pass": ratification_reached(48, 0, 36, 36),
        },
    }


def historical_denominator_control() -> dict:
    case = json.loads((HERE / "sixteenth-denominator-case.json").read_text(encoding="utf-8"))
    original = case["states_before_1912_admissions"]
    new_states = {entry["state"] for entry in case["admitted_while_amendment_pending"]}
    principal = set(case["principal_list"])
    additional = set(case["additional_ratifications_acknowledged"])
    if len(principal) != len(case["principal_list"]) or principal & additional:
        raise ValueError("Historical ratification lists contain duplicates")
    if len(principal) != case["declared_principal_list_count"]:
        raise ValueError("Historical principal-list count disagrees with the primary page")
    total = original + len(new_states)
    old_yes, new_yes = len(principal - new_states), len(principal & new_states)
    required = (3 * total + 3) // 4
    if not ratification_reached(original, old_yes, len(new_states), new_yes):
        raise AssertionError("Historical certification count is rejected")
    return {
        "case": case["case"],
        "evidence_kind": case["evidence_kind"],
        "initial_states": original,
        "states_at_certification": total,
        "initial_threshold": (3 * original + 3) // 4,
        "threshold_at_certification": required,
        "principal_ratification_list_count": len(principal),
        "all_ratifications_acknowledged_on_page": len(principal | additional),
        "principal_list_satisfies_current_threshold": True,
        "one_fewer_than_threshold": {
            "ratifications": required - 1,
            "frozen_original_denominator_would_accept": 4 * (required - 1) >= 3 * original,
            "current_denominator_accepts": 4 * (required - 1) >= 3 * total,
            "status": "SYNTHETIC negative control, not an assertion about a specific historical date",
        },
    }


def target_matrix(scenario: Scenario, added: int) -> list[dict]:
    if not all(gates(scenario, added).values()) or (added and not admission_can_begin(scenario)):
        raise ValueError("Cannot examine post-admission targets before the modeled gates pass")
    total = scenario.states + added
    ratifiers = frozenset(range(scenario.old_ratifiers)) | frozenset(range(scenario.states, total))
    house_yes = scenario.house_support + added
    senate_yes = scenario.senate_support + 2 * added

    def votes(seats, yes):
        present = seats if scenario.attendance == Attendance.FULL else max(seats // 2 + 1, yes)
        return Votes(seats, present, yes)

    support = Support(
        total, ratifiers, ratifiers,
        votes(scenario.house_seats + added, house_yes), votes(2 * total, senate_yes),
    )
    matrix = []
    for scope in Suffrage:
        for entrenched in (False, True):
            policy = Policy(suffrage=scope, self_entrenched=entrenched)
            path = explore(policy, support).shortest_path(Target.CONCENTRATED_POWERS)
            matrix.append({
                "suffrage": scope.value,
                "self_entrenched": entrenched,
                "democracy_floor": False,
                "reachable": path is not None,
                "post_admission_witness": [step.label() for step in path] if path else None,
            })
    return matrix


def run():
    scenarios = {
        "1947_bare_full_majorities_one_old_ratifier": Scenario(48, 435, 218, 49, 1),
        "1947_favorable_quorum_one_old_ratifier": Scenario(
            48, 435, 110, 25, 1, Attendance.FAVORABLE,
        ),
        "1947_same_small_bloc_without_president": Scenario(
            48, 435, 110, 25, 1, Attendance.FAVORABLE, False,
        ),
        "1947_same_small_bloc_must_supply_quorum": Scenario(
            48, 435, 110, 25, 1, Attendance.SELF_QUORATE,
        ),
        "paper_96_compatible_hypothetical_inputs": Scenario(50, 435, 258, 60, 14),
        "111th_initial_house_257_with_other_inputs_held_fixed": Scenario(50, 435, 257, 60, 14),
    }
    outcomes = {}
    for name, scenario in scenarios.items():
        enumeration = enumerate_minimum(scenario)
        symbolic = smt_minimum(scenario)
        if symbolic["status"] == "UNKNOWN":
            raise RuntimeError(f"{name}: solver UNKNOWN: {symbolic['reason']}")
        if (enumeration["status"], enumeration["new_states"]) != (
            symbolic["status"], symbolic["new_states"],
        ):
            raise AssertionError(f"Enumeration/SMT disagreement: {name}")
        outcomes[name] = {
            "inputs": {**asdict(scenario), "attendance": scenario.attendance.value},
            "enumeration": enumeration,
            "smt": symbolic,
        }
    paper_rows = []
    for added in (96, 127):
        paper_rows.append({
            "new_states": added,
            "total_states": 50 + added,
            "ratification_required": (3 * (50 + added) + 3) // 4,
            "old_ratifiers_still_required": max(0, (3 * (50 + added) + 3) // 4 - added),
            "old_house_yes_required_full_attendance": (2 * (435 + added) + 2) // 3 - added,
            "house_expansion_assumption": "One new seat per new state, old seats retained",
        })
    matrix_scenario = scenarios["1947_favorable_quorum_one_old_ratifier"]
    matrix_added = outcomes["1947_favorable_quorum_one_old_ratifier"]["enumeration"]["new_states"]
    return {
        "schema_version": 1,
        "paper": {
            "title": "Pack the Union",
            "citation": "133 Harvard Law Review 1049 (2020), Part II.A, page 1060 footnote 94",
            "publication_date": "January 10, 2020",
            "url": "https://harvardlawreview.org/print/vol-133/pack-the-union-a-proposal-to-admit-new-states-for-the-purpose-of-amending-the-constitution-to-ensure-equal-representation/",
            "pdf_sha256": "049574ce9eddc77c29facb9cc72c9fa66226700b7737b112dc8b94a37c979c90",
            "printed_claim": 96,
            "printed_claim_replication_status": "UNDERDETERMINED: no exact roster date, attendance, or state-support inputs published",
            "conditional_reconstructions": paper_rows,
        },
        "official_house_roster_comparison": {
            "url": "https://history.house.gov/Institution/Party-Divisions/Party-Divisions/",
            "html_sha256": "f8d496451af0cfc0544be4b80da2de950701ad72cddc455b8aaf674721e5c83d",
            "scope": "Initial election results only; not every date during the 111th Congress",
            "congress": 111,
            "house_seats": 435,
            "democrats": 257,
            "republicans": 178,
            "other_scenario_inputs": "Hypothetical and held fixed, not taken from this roster",
        },
        "scope": {
            "vantage": "December 5, 1947",
            "all_new_delegations_support": "ASSUMED, not derived from state admission",
            "all_new_states_ratify": "ASSUMED, not an admission condition validated as lawful",
            "one_extra_house_seat_per_new_state": "ASSUMED; old House seats retained",
            "state_creation_and_geographic_partition": "NOT VERIFIED",
            "vice_presidential_tie_breaking": "NOT MODELED",
            "numbers_are_counts_of": "Additional states, not people or political probabilities",
            "historical_attribution_to_godel": False,
        },
        "source_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
            for name in (
                "state_admission.py", "test_state_admission.py", "article_v_model.py",
                "sixteenth-denominator-case.json",
            )
        },
        "controls": general_controls(),
        "historical_denominator_control": historical_denominator_control(),
        "ratification_frontier_1947": [
            {"old_ratifiers": old, "minimum_all_supporting_new_states": minimum_all_supporting_additions(48, old)}
            for old in range(49)
        ],
        "joint_scenarios": outcomes,
        "post_admission_target_matrix": target_matrix(matrix_scenario, matrix_added),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    document = run()
    print(json.dumps({
        name: row["enumeration"] for name, row in document["joint_scenarios"].items()
    }, indent=2))
    print(json.dumps(document["controls"], indent=2))
    if args.write:
        RESULTS.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.check:
        if not RESULTS.is_file() or json.loads(RESULTS.read_text(encoding="utf-8")) != document:
            raise SystemExit("Missing or stale state-admission result artifact")
        print("State-admission result artifact matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
