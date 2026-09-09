"""Saturate the declared interpretation grid and cross-check bounded reachability."""

import argparse
from collections import Counter
import hashlib
from itertools import product
import json
from pathlib import Path
import platform
import sys

import z3

from article_v_model import (
    Amendment,
    Policy,
    Screening,
    Suffrage,
    Target,
    explore,
    reaches,
    replay,
    support_profile,
)
from article_v_smt import solve


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "article_v_results.json"
SMT_BOUND = 4


def evaluate(policy, support, alphabet=tuple(Amendment)):
    graph = explore(policy, support, alphabet)
    nonvacuity = solve(policy, support, None, max_steps=0, alphabet=alphabet)
    results = {}
    for target in Target:
        path = graph.shortest_path(target)
        if path is not None and not reaches(replay(policy, support, path), target):
            raise AssertionError("Explicit-state witness failed replay")
        smt = solve(policy, support, target, max_steps=SMT_BOUND, alphabet=alphabet)
        expected = "SAT" if path is not None and len(path) <= SMT_BOUND else "UNSAT"
        if smt.status != "UNKNOWN" and smt.status != expected:
            raise AssertionError(f"BFS/SMT disagreement for {policy!r}: {target.value}")
        results[target.value] = {
            "finite_graph": "REACHABLE" if path is not None else "UNREACHABLE",
            "shortest_operations": len(path) if path is not None else None,
            "ratifications": sum(step.phase == "ratify" for step in path) if path else None,
            "witness": [step.label() for step in path] if path is not None else None,
            "smt_within_bound": smt.status,
            "smt_reason": smt.reason,
            "implementations_agree_within_bound": smt.status == expected,
        }
    return {
        "policy": policy.to_dict(),
        "support": {
            "ratifying_states": sorted(support.ratifiers),
            "consenting_states": sorted(support.consenters),
            "ratification_mode": support.mode,
        },
        "graph": {
            "saturated": True,
            "protocol_states": len(graph.parents),
            "constitutional_states": len({state.constitution for state in graph.parents}),
            "legal_edges": graph.legal_edges,
            "rejected_edges": graph.rejected_edges,
            "initial_smt_nonvacuity": nonvacuity.status,
        },
        "targets": results,
    }


def run_grid():
    configurations = []
    for suffrage, entrenched, floor, screening, count in product(
        Suffrage, (False, True), (False, True), Screening, (35, 36, 48),
    ):
        policy = Policy(suffrage, entrenched, floor, screening)
        configurations.append(evaluate(policy, support_profile(count)))
    no_repeal = tuple(amendment for amendment in Amendment if amendment not in (
        Amendment.REPEAL_PROVISO, Amendment.REPEAL_AND_CONCENTRATE,
    ))
    ablations = {
        "no_repeal_in_action_alphabet": evaluate(Policy(), support_profile(36), no_repeal),
        "threshold_rule_held_fixed": evaluate(
            Policy(allow_threshold_change=False), support_profile(36),
        ),
    }
    answers = [answer for row in configurations for answer in row["targets"].values()]
    counts = Counter(answer["finite_graph"] for answer in answers)
    unresolved = [
        (group, index, target)
        for group, rows in (("grid", configurations), ("ablations", list(ablations.values())))
        for index, row in enumerate(rows)
        for target, answer in row["targets"].items()
        if not answer["implementations_agree_within_bound"]
    ]
    for row in configurations + list(ablations.values()):
        if row["graph"]["initial_smt_nonvacuity"] != "SAT":
            raise RuntimeError("Initial consistency check did not return SAT")
    source_names = (
        "article_v_model.py", "article_v_smt.py", "article_v_search.py", "test_article_v.py",
    )
    return {
        "schema_version": 1,
        "vantage": "December 5, 1947",
        "scope": {
            "states": 48,
            "house_seats": 435,
            "senate_seats": 96,
            "action_alphabet": [amendment.value for amendment in Amendment],
            "protocol": ["propose", "ratify", "withdraw"],
            "smt_max_operations": SMT_BOUND,
            "support_counts": [35, 36, 48],
            "support_identity_rule": "Both sets are the prefix 0..count-1; deprivation names state 47",
            "initial_ratifiers_required": 36,
            "ordinary_rule_self_amendment": "allowed in grid; separately ablated",
            "scope_warning": (
                "Exhaustive only for this finite action alphabet, fixed supports and interpretation grid; "
                "not all constitutional acts, coalitions, legal interpretations or historical paths."
            ),
        },
        "environment": {"python": platform.python_version(), "z3": z3.get_version_string()},
        "source_sha256": {
            name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in source_names
        },
        "summary": {
            "grid_configurations": len(configurations),
            "grid_target_queries": len(answers),
            "grid_reachable": counts["REACHABLE"],
            "grid_unreachable": counts["UNREACHABLE"],
            "grid_smt_agreements": sum(
                answer["implementations_agree_within_bound"] for answer in answers
            ),
            "additional_ablation_queries": sum(len(row["targets"]) for row in ablations.values()),
            "unresolved_cross_checks": unresolved,
            "constitutional_loophole_established": False,
            "historical_attribution_established": False,
        },
        "configurations": configurations,
        "ablations": ablations,
    }


def comparable(document):
    return {key: value for key, value in document.items() if key != "environment"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="Write deterministic result artifact")
    group.add_argument("--check", action="store_true", help="Compare with the committed artifact")
    args = parser.parse_args()
    document = run_grid()
    print(json.dumps(document["summary"], indent=2))
    if args.write:
        RESULTS.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Wrote {RESULTS}")
    if document["summary"]["unresolved_cross_checks"]:
        print("INCONCLUSIVE: at least one solver cross-check is unresolved", file=sys.stderr)
        return 2
    if args.check:
        if not RESULTS.is_file():
            print(f"Missing artifact: {RESULTS}; run with --write first", file=sys.stderr)
            return 1
        recorded = json.loads(RESULTS.read_text(encoding="utf-8"))
        if comparable(recorded) != comparable(document):
            print("Result artifact differs from current source/results", file=sys.stderr)
            return 1
        print("Result artifact matches; environment-version metadata is not compared.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
