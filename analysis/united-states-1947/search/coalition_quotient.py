"""Classify all fixed coalition pairs in the existing finite Article V model, not in constitutional law."""

import argparse
from collections import Counter
from dataclasses import replace
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
import platform
import sys

import z3

from article_v_model import (
    Amendment, Policy, Screening, Suffrage, Support, Target,
    amendment_effect, initial_state, support_profile,
)
from article_v_search import RESULTS as BASE_RESULTS, comparable, evaluate


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "coalition_quotient_results.json"


class InconclusiveCertificate(RuntimeError):
    pass


def threshold(states):
    return initial_state(states).constitution.ratifiers_required


def signature(support: Support) -> tuple[int, int]:
    count = len(support.ratifiers)
    ratification = 0 if count == 0 else 1 if count < threshold(support.states) else 2
    consent = (2 if support.consenters == support.all_states else
               1 if support.states - 1 in support.consenters else 0)
    return ratification, consent


def canonical_support(support: Support) -> Support:
    ratification, consent = signature(support)
    count = (0, 1, threshold(support.states))[ratification]
    consenters = (frozenset(), frozenset({support.states - 1}), support.all_states)[consent]
    return replace(support, ratifiers=frozenset(range(count)), consenters=consenters)


def representatives(states):
    cutoff = threshold(states)
    ratifier_counts = (0, 1, cutoff) if cutoff > 1 else (0, cutoff)
    consents = (frozenset(), frozenset({states-1}), frozenset(range(states)))
    unique = {}
    for count, consenters in product(ratifier_counts, consents):
        support = replace(support_profile(count, states), consenters=consenters)
        unique[signature(support)] = support
    return [unique[key] for key in sorted(unique)]


def class_size(states, key):
    cutoff = threshold(states)
    ratifier_sizes = (1, sum(comb(states, r) for r in range(1, cutoff)),
                     sum(comb(states, r) for r in range(cutoff, states+1)))
    consent_sizes = (2**(states-1), 2**(states-1)-1, 1)
    return ratifier_sizes[key[0]] * consent_sizes[key[1]]


def classified_lengths(policy: Policy, support: Support):
    result = {target.value: None for target in Target}
    if not support.house.can_propose() or not support.senate.can_propose():
        return result
    if len(support.ratifiers) < threshold(support.states):
        return result
    unanimous = support.consenters == support.all_states
    if not policy.democracy_floor:
        result[Target.EXECUTIVE_ELECTORAL_LOCK.value] = 2
        if policy.suffrage == Suffrage.FORMAL or unanimous:
            result[Target.CONCENTRATED_POWERS.value] = 2
        elif not policy.self_entrenched:
            result[Target.CONCENTRATED_POWERS.value] = 4
    if support.states - 1 in support.consenters:
        result[Target.UNEQUAL_SENATE.value] = 2
    elif not policy.self_entrenched:
        result[Target.UNEQUAL_SENATE.value] = 4
    return result


def unsat_certificate(constraints):
    solver = z3.Solver()
    solver.set(timeout=30_000)
    solver.add(*constraints)
    verdict = solver.check()
    if verdict == z3.unsat:
        return {"status": "UNSAT"}
    if verdict == z3.sat:
        return {"status": "SAT", "counterexample": str(solver.model())}
    return {"status": "UNKNOWN", "reason": solver.reason_unknown()}


def quotient_certificates(states, plant=None):
    cutoff = threshold(states)
    values = {cutoff}
    for amendment in Amendment:
        value = amendment_effect(amendment, states).get("ratifiers_required")
        if value is not None:
            values.add(value)
    if values != {1, cutoff}:
        raise ValueError(f"Threshold domain changed: {sorted(values)}; rederive the quotient")

    left, right, required = z3.Ints("left_ratifiers right_ratifiers required")
    ratifier_equalities = [(left >= cutoff) == (right >= cutoff)]
    if plant != "threshold":
        ratifier_equalities.append((left >= 1) == (right >= 1))
    arithmetic = unsat_certificate([
        0 <= left, left <= states, 0 <= right, right <= states,
        z3.Or(*(required == value for value in values)), *ratifier_equalities,
        (left >= required) != (right >= required),
    ])

    first, second, deprived = z3.BitVecs("first_consent second_consent deprived", states)
    full, affected = (1 << states)-1, 1 << (states-1)
    consent_equalities = []
    if plant != "consent-all":
        consent_equalities.append((first == full) == (second == full))
    if plant != "consent-id":
        consent_equalities.append(((first & affected) != 0) == ((second & affected) != 0))
    consent = unsat_certificate([
        *consent_equalities, z3.Or(deprived == 0, deprived == affected, deprived == full),
        ((first & deprived) == deprived) != ((second & deprived) == deprived),
    ])
    return {
        "threshold_domain": sorted(values),
        "ratification_guard_preserved": arithmetic,
        "permitted_deprivation_tests_preserved": consent,
    }


def load_baseline():
    baseline = json.loads(BASE_RESULTS.read_text(encoding="utf-8"))
    for name, expected in baseline["source_sha256"].items():
        actual = hashlib.sha256((HERE/name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Baseline source changed: {name}; recheck the model before extending it")
    if baseline["scope"]["action_alphabet"] != [amendment.value for amendment in Amendment]:
        raise ValueError("Action alphabet differs from the checked baseline")
    return baseline


def policy_from_record(record):
    return Policy(**{**record, "suffrage": Suffrage(record["suffrage"]),
                     "screening": Screening(record["screening"])})


def run():
    baseline = load_baseline()
    states = baseline["scope"]["states"]
    certificates = quotient_certificates(states)
    unresolved_certificates = [
        name for name, result in certificates.items()
        if isinstance(result, dict) and result["status"] == "UNKNOWN"
    ]
    if unresolved_certificates:
        raise InconclusiveCertificate(f"Quotient certificate unresolved: {unresolved_certificates}")
    if any(isinstance(result, dict) and result["status"] == "SAT" for result in certificates.values()):
        raise AssertionError("A counterexample refutes the proposed coalition quotient")
    supports = representatives(states)
    sizes = {signature(support): class_size(states, signature(support)) for support in supports}
    if sum(sizes.values()) != 2**(2*states):
        raise AssertionError("Coalition classes do not cover all pairs of subsets")

    policies = {}
    for record in baseline["configurations"]:
        policy = policy_from_record(record["policy"])
        policies[json.dumps(policy.to_dict(), sort_keys=True)] = policy
    configurations, lookup = [], {}
    for policy_key, policy in sorted(policies.items()):
        for support in supports:
            row = evaluate(policy, support)
            key = signature(support)
            predicted = classified_lengths(policy, support)
            actual = {target: answer["shortest_operations"] for target, answer in row["targets"].items()}
            if predicted != actual:
                raise AssertionError(f"Classification disagrees with saturated BFS: {policy_key}, {key}")
            row["coalition_class"] = list(key)
            row["represented_subset_pairs"] = sizes[key]
            row["classification_shortest_operations"] = predicted
            configurations.append(row)
            lookup[policy_key, key] = row

    for old in baseline["configurations"]:
        policy_key = json.dumps(old["policy"], sort_keys=True)
        old_support = replace(
            support_profile(len(old["support"]["ratifying_states"]), states),
            ratifiers=frozenset(old["support"]["ratifying_states"]),
            consenters=frozenset(old["support"]["consenting_states"]),
            mode=old["support"]["ratification_mode"],
        )
        current = lookup[policy_key, signature(old_support)]
        if current["graph"] != old["graph"] or current["targets"] != old["targets"]:
            raise AssertionError("Original prefix-coalition result changed under the quotient")

    answers = [answer for row in configurations for answer in row["targets"].values()]
    counts = Counter(answer["finite_graph"] for answer in answers)
    unresolved = [
        [index, target] for index, row in enumerate(configurations)
        for target, answer in row["targets"].items()
        if not answer["implementations_agree_within_bound"]
    ]
    if any(row["graph"]["initial_smt_nonvacuity"] != "SAT" for row in configurations):
        raise RuntimeError("A representative failed initial nonvacuity")
    names = (*baseline["source_sha256"], "coalition_quotient.py", "test_coalition_quotient.py")
    return {
        "schema_version": 1,
        "vantage": baseline["vantage"],
        "scope": {
            "states": states,
            "action_alphabet": baseline["scope"]["action_alphabet"],
            "support": "Arbitrary independent ratifier and consenter subsets, fixed throughout each path.",
            "proposal_votes_and_mode": "The original grid's quorum-vote profile and legislature mode.",
            "deprivation_sets": ["empty", "designated state states-1", "all states"],
            "preserves": "Transition guards and action-labeled witnesses, not raw coalition cardinalities, overlap, costs, or probabilities.",
            "limit": "A classification of the existing finite interpretation model, not constitutional legality or variable coalitions.",
        },
        "quotient_certificates": certificates,
        "environment": {"python": platform.python_version(), "z3": z3.get_version_string()},
        "source_sha256": {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names},
        "baseline_sha256": hashlib.sha256(BASE_RESULTS.read_bytes()).hexdigest(),
        "summary": {
            "policies": len(policies), "coalition_classes_per_policy": len(supports),
            "configurations": len(configurations), "target_queries": len(answers),
            "reachable": counts["REACHABLE"], "unreachable": counts["UNREACHABLE"],
            "bfs_smt_agreements": sum(answer["implementations_agree_within_bound"] for answer in answers),
            "original_configurations_preserved": len(baseline["configurations"]),
            "subset_pairs_covered_per_policy": sum(sizes.values()),
            "unresolved_cross_checks": unresolved,
            "constitutional_loophole_established": False,
        },
        "configurations": configurations,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--plant", choices=("threshold", "consent-id", "consent-all"))
    args = parser.parse_args()
    if args.plant:
        report = quotient_certificates(load_baseline()["scope"]["states"], args.plant)
        print(json.dumps(report, indent=2))
        if any(isinstance(value, dict) and value["status"] == "SAT" for value in report.values()):
            print("FAIL: weakened coalition signature does not preserve a model guard")
            return 1
        print("FAIL: the planted defect did not yield the required counterexample", file=sys.stderr)
        return 2
    try:
        document = run()
    except InconclusiveCertificate as error:
        print(f"INCONCLUSIVE: {error}", file=sys.stderr)
        return 2
    print(json.dumps(document["summary"], indent=2))
    if document["summary"]["unresolved_cross_checks"]:
        print("INCONCLUSIVE: solver comparison unresolved", file=sys.stderr)
        return 2
    if args.write:
        RESULTS.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {RESULTS}")
    if args.check:
        recorded = json.loads(RESULTS.read_text(encoding="utf-8"))
        if comparable(document) != comparable(recorded):
            print("FAIL: coalition result artifact differs from current results", file=sys.stderr)
            return 1
        print("Coalition result artifact matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
