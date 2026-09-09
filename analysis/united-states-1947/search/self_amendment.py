"""Bounded replication of AAMAS 2021 Algorithm 1 and Theorem 1 (pp. 1443–1445)."""

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import cached_property, lru_cache
from hashlib import sha256
from itertools import permutations
import json
from math import comb, factorial, prod
from pathlib import Path
import platform

import z3


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "self_amendment_results.json"
MIN_N, MAX_N = 2, 8
TIMEOUT_MS = 60_000
SOURCE_FILES = {
    "aamas2021-p1443.pdf": {
        "url": "https://www.ifaamas.org/Proceedings/aamas2021/pdfs/p1443.pdf",
        "sha256": "4ee8691ce53916b95349ab3b5fc457a32f670c9e27f6a863bd96ae40aee4bb70",
        "bytes": 1_013_526, "pages": 3,
        "role": "Primary target; all pages 1443–1445 read; Algorithm 1 and Theorem 1 on 1444",
    },
    "arxiv-2011.03111v2.pdf": {
        "url": "https://arxiv.org/pdf/2011.03111v2",
        "sha256": "a25450ce60f3a5dd336757d890b484041ad1a071081937d70adaec251a96ac59",
        "bytes": 423_975, "pages": 12, "revision_date": "2021-03-05",
        "role": "Matching full paper; all 12 pages read; proofs inline, no separate appendix",
    },
    "arxiv-2011.03111v1.pdf": {
        "url": "https://arxiv.org/pdf/2011.03111v1",
        "sha256": "9e45fcf00fc95cb46bafec0e0eb2985943b55790f7aa4ab549c05b7370cdef1e",
        "bytes": 489_276, "pages": 18, "revision_date": "2020-11-05",
        "role": "Version comparison only; uses offset threshold 1/2 + delta",
    },
    "arxiv-2011.03111v4.pdf": {
        "url": "https://arxiv.org/pdf/2011.03111v4",
        "sha256": "91021a0a2f0387d7d4828dd6d4ca9500b62ed9117fb88e9642d9c78fcf516b16",
        "bytes": 227_997, "pages": 14, "revision_date": "2021-11-09",
        "role": "Version comparison only; retitled In the Beginning there were n Agents",
    },
    "aamas2021-authors.htm": {
        "url": "https://www.ifaamas.org/Proceedings/aamas2021/forms/authors.htm",
        "sha256": "1beaa3784732912da741ff5ff91116ad300544d1ffefb98c9c30f91c22d0ee01",
        "bytes": 191_198, "role": "Official index linking the extended abstract at p1443.pdf",
    },
    "arxiv-2011.03111-abs.html": {
        "url": "https://arxiv.org/abs/2011.03111",
        "sha256": "e92c1547b96be21a39bb2cbb6d42853c489ab87a4e8df4895a577395f492364c",
        "bytes": 43_299, "role": "Observed version history and latest-version title",
    },
    "arxiv-2011.03111v1-abs.html": {
        "url": "https://arxiv.org/abs/2011.03111v1",
        "sha256": "27026240b4d9dffedbfd844dd3ff5334bebda7d50156920e879d202a3e38e499",
        "bytes": 42_322, "role": "Verified original title, three authors, and identifier",
    },
}
FAILURE_KEYS = (
    "theorem_1", "algorithm_1_elects_h", "endpoint_self_stability",
    "endpoint_other_stability", "algorithm_1_complaint_freeness",
)


def alternatives(n):
    if type(n) is not int or n < 2:
        raise ValueError("This implementation requires an integer electorate size n >= 2")
    return tuple(range(n // 2, n))


def is_single_peaked(ranks):
    if not ranks or ranks.count(0) != 1:
        return False
    peak = ranks.index(0)
    return (
        all(ranks[i] > ranks[i + 1] for i in range(peak))
        and all(ranks[i] < ranks[i + 1] for i in range(peak, len(ranks) - 1))
    )


def _merge_sides(left, right, allow_ties):
    if not left and not right:
        yield ()
    if left:
        for rest in _merge_sides(left[1:], right, allow_ties):
            yield ((left[0],),) + rest
    if right:
        for rest in _merge_sides(left, right[1:], allow_ties):
            yield ((right[0],),) + rest
    if allow_ties and left and right:
        for rest in _merge_sides(left[1:], right[1:], allow_ties):
            yield ((left[0], right[0]),) + rest


@lru_cache(maxsize=None)
def preference_types(size, allow_ties=True):
    """All complete rankings with a unique peak and strict decline on either side."""
    if type(size) is not int or size < 1:
        raise ValueError("At least one alternative is required")
    result = set()
    for peak in range(size):
        left = tuple(range(peak - 1, -1, -1))
        right = tuple(range(peak + 1, size))
        for rest in _merge_sides(left, right, allow_ties):
            ranks = [0] * size
            for rank, block in enumerate(((peak,),) + rest):
                for index in block:
                    ranks[index] = rank
            result.add(tuple(ranks))
    return tuple(sorted(result))


@dataclass(frozen=True)
class Domain:
    n: int
    rankings: tuple

    def __post_init__(self):
        size = len(alternatives(self.n))
        if not self.rankings or len(set(self.rankings)) != len(self.rankings):
            raise ValueError("Preference types must be nonempty and unique")
        for ranks in self.rankings:
            if (
                len(ranks) != size or any(type(rank) is not int or rank < 0 for rank in ranks)
                or set(ranks) != set(range(max(ranks) + 1)) or ranks.count(0) != 1
            ):
                raise ValueError("Use canonical complete rankings with one unique bliss point")

    @cached_property
    def rules(self):
        return alternatives(self.n)

    @cached_property
    def peaks(self):
        return tuple(self.rules[ranks.index(0)] for ranks in self.rankings)

    @cached_property
    def supporter_types(self):
        return tuple(tuple(
            tuple(i for i, ranks in enumerate(self.rankings) if ranks[p] < ranks[r])
            for r in range(len(self.rules))
        ) for p in range(len(self.rules)))


def make_domain(n, *, allow_ties=True, single_peaked=True):
    size = len(alternatives(n))
    rankings = (
        preference_types(size, allow_ties) if single_peaked
        else tuple(permutations(range(size)))
    )
    return Domain(n, rankings)


def compositions(total, width):
    if type(total) is not int or total < 0 or type(width) is not int or width < 1:
        raise ValueError("Invalid profile-composition dimensions")
    if width == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, width - 1):
                yield (first,) + rest


def validate_counts(domain, counts):
    if (
        len(counts) != len(domain.rankings)
        or any(type(count) is not int or count < 0 for count in counts)
        or sum(counts) != domain.n
    ):
        raise ValueError("Preference multiplicities must be nonnegative integers summing to fixed n")


def support_table(domain, counts):
    validate_counts(domain, counts)
    return tuple(tuple(
        sum(counts[index] for index in indices) for indices in row
    ) for row in domain.supporter_types)


def h_from_peaks(n, peaks, *, strict_mutation=False):
    rules = alternatives(n)
    if len(peaks) != n or any(type(peak) is not int or peak not in rules for peak in peaks):
        raise ValueError("Exactly n admissible bliss points are required")
    return max(rule for rule in rules if (
        sum(peak >= rule for peak in peaks) > rule if strict_mutation
        else sum(peak >= rule for peak in peaks) >= rule
    ))


def complaining_groups(domain, counts, support, old, proposal, winner):
    rules = domain.rules
    if (
        any(type(value) is not int for value in (old, proposal, winner))
        or old not in rules or proposal not in rules or winner not in (old, proposal)
    ):
        raise ValueError("Amendment outcomes must be one of two admissible alternatives")
    r, p, w = rules.index(old), rules.index(proposal), rules.index(winner)
    other = r if winner == proposal else p
    yes = support[p][r]
    return tuple(i for i, ranks in enumerate(domain.rankings) if counts[i] and (
        (proposal if yes > domain.peaks[i] else old) != winner
        and not ranks[w] < ranks[other]
    ))


def _protocol(domain, counts, support, mutation=None):
    if mutation not in (None, "weak_approval", "proposed_threshold", "reverse_agenda"):
        raise ValueError("Unknown negative-control mutation")
    state = domain.rules[0]
    agenda = tuple(reversed(domain.rules)) if mutation == "reverse_agenda" else domain.rules
    trace = []
    for proposal in agenda:
        old = state
        yes = support[domain.rules.index(proposal)][domain.rules.index(old)]
        threshold = proposal if mutation == "proposed_threshold" else old
        accepted = yes >= threshold if mutation == "weak_approval" else yes > threshold
        state = proposal if accepted else old
        complainers = complaining_groups(domain, counts, support, old, proposal, state)
        trace.append({
            "old": old, "proposal": proposal, "threshold": threshold,
            "yes_votes": yes, "accepted": accepted, "winner": state,
            "complaining_groups": list(complainers),
            "complaining_voters": sum(counts[i] for i in complainers),
        })
    return {"winner": state, "trace": trace}


def evolutionary_constitution(domain, counts, *, mutation=None):
    return _protocol(domain, counts, support_table(domain, counts), mutation)


def analyze_profile(domain, counts, *, mutation=None):
    support = support_table(domain, counts)
    peaks = sorted(peak for peak, count in zip(domain.peaks, counts) for _ in range(count))
    h = h_from_peaks(domain.n, peaks)
    median = peaks[domain.n // 2]
    self_stable = [
        rule for r, rule in enumerate(domain.rules)
        if all(support[p][r] <= rule for p in range(len(domain.rules)))
    ]
    other_stable = [
        rule for r, rule in enumerate(domain.rules)
        if all(support[p][r] <= proposal for p, proposal in enumerate(domain.rules))
    ]
    violating_rules = [
        rule for rule in domain.rules if (
            (rule < h and rule in self_stable)
            or (h <= rule <= median and (rule not in self_stable or rule not in other_stable))
        )
    ]
    run = _protocol(domain, counts, support, mutation)
    flags = (
        bool(violating_rules), run["winner"] != h,
        run["winner"] not in self_stable, run["winner"] not in other_stable,
        any(vote["complaining_voters"] for vote in run["trace"]),
    )
    return {
        "h": h, "upper_median": median, "self_stable": self_stable,
        "other_stable": other_stable, "theorem_1_violating_rules": violating_rules,
        "protocol": run, "failures": [name for name, failed in zip(FAILURE_KEYS, flags) if failed],
    }


def describe_profile(domain, counts):
    validate_counts(domain, counts)
    groups = []
    for group_id, (ranks, count) in enumerate(zip(domain.rankings, counts)):
        if count:
            groups.append({
                "id": group_id,
                "count": count,
                "ranking_best_to_worst": [
                    [rule for rule, rank in zip(domain.rules, ranks) if rank == level]
                    for level in range(max(ranks) + 1)
                ],
            })
    return {
        "n": domain.n, "threshold_denominator": domain.n,
        "admissible_threshold_numerators": list(domain.rules), "groups": groups,
        "single_peaked": all(
            is_single_peaked(ranks) for ranks, count in zip(domain.rankings, counts) if count
        ),
        "strict_preferences": all(
            len(set(ranks)) == len(ranks)
            for ranks, count in zip(domain.rankings, counts) if count
        ),
    }


def enumerate_profiles(n):
    domain = make_domain(n)
    size = len(domain.rules)
    strict_types = tuple(len(set(ranks)) == size for ranks in domain.rankings)
    factorials = tuple(factorial(i) for i in range(n + 1))
    result = {
        "n": n, "alternatives": list(domain.rules), "preference_types_with_cross_side_ties": len(domain.rankings),
        "strict_preference_types": sum(strict_types),
        "anonymous_profiles": 0, "strict_anonymous_profiles": 0,
        "represented_labeled_profiles": 0, "represented_strict_labeled_profiles": 0,
        "theorem_1_candidate_checks": 0, "algorithm_1_vote_steps": 0,
        "nontrivial_votes_rejected_at_exact_threshold": 0,
        "counterexample_profiles": {name: 0 for name in FAILURE_KEYS},
        "endpoint_histogram": {str(rule): 0 for rule in domain.rules},
        "first_counterexample": None,
    }
    for counts in compositions(n, len(domain.rankings)):
        analysis = analyze_profile(domain, counts)
        labeled = factorials[n] // prod(factorials[count] for count in counts)
        strict = all(not count or strict_types[i] for i, count in enumerate(counts))
        result["anonymous_profiles"] += 1
        result["strict_anonymous_profiles"] += strict
        result["represented_labeled_profiles"] += labeled
        result["represented_strict_labeled_profiles"] += labeled if strict else 0
        result["theorem_1_candidate_checks"] += size
        result["algorithm_1_vote_steps"] += len(analysis["protocol"]["trace"])
        result["endpoint_histogram"][str(analysis["protocol"]["winner"])] += 1
        result["nontrivial_votes_rejected_at_exact_threshold"] += sum(
            vote["proposal"] != vote["old"] and vote["yes_votes"] == vote["threshold"]
            and not vote["accepted"] for vote in analysis["protocol"]["trace"]
        )
        for failure in analysis["failures"]:
            result["counterexample_profiles"][failure] += 1
        if analysis["failures"] and result["first_counterexample"] is None:
            result["first_counterexample"] = {
                "profile": describe_profile(domain, counts), "analysis": analysis,
            }
    if (
        result["anonymous_profiles"] != comb(n + len(domain.rankings) - 1, n)
        or result["strict_anonymous_profiles"] != comb(n + sum(strict_types) - 1, n)
        or result["represented_labeled_profiles"] != len(domain.rankings) ** n
        or result["represented_strict_labeled_profiles"] != sum(strict_types) ** n
    ):
        raise RuntimeError("Exhaustive domain coverage checks failed")
    return result


def _zsum(values):
    return z3.Sum(values) if values else z3.IntVal(0)


def symbolic_problem(domain, mutation=None):
    """Encode the formulas independently of the Python vote, h, and CF functions."""
    if mutation not in (None, "weak_approval", "proposed_threshold", "reverse_agenda"):
        raise ValueError("Unknown symbolic mutation")
    rules = domain.rules
    counts = tuple(z3.Int(f"count_{i}") for i in range(len(domain.rankings)))
    base = [count >= 0 for count in counts] + [_zsum(list(counts)) == domain.n]
    peaks = [rules[ranks.index(0)] for ranks in domain.rankings]
    support = [[
        _zsum([counts[i] for i, ranks in enumerate(domain.rankings) if ranks[p] < ranks[r]])
        for r in range(len(rules))
    ] for p in range(len(rules))]
    tails = {
        rule: _zsum([count for count, peak in zip(counts, peaks) if peak >= rule])
        for rule in rules
    }
    h = z3.Int("h")
    base.append(z3.Or([
        z3.And(h == rule, tails[rule] >= rule, *[
            tails[higher] < higher for higher in rules if higher > rule
        ]) for rule in rules
    ]))
    stable = [
        z3.And([support[p][r] <= rule for p in range(len(rules))])
        for r, rule in enumerate(rules)
    ]
    other = [
        z3.And([support[p][r] <= proposal for p, proposal in enumerate(rules)])
        for r in range(len(rules))
    ]
    theorem_bad = []
    for r, rule in enumerate(rules):
        below_rule = _zsum([count for count, peak in zip(counts, peaks) if peak < rule])
        theorem_bad.extend((
            z3.And(rule < h, stable[r]),
            z3.And(h <= rule, below_rule <= domain.n // 2, z3.Not(z3.And(stable[r], other[r]))),
        ))
    agenda = tuple(reversed(rules)) if mutation == "reverse_agenda" else rules
    states = tuple(z3.Int(f"state_{i}") for i in range(len(agenda) + 1))
    transitions = [states[0] == rules[0]]
    complaints = []
    for step, proposal in enumerate(agenda):
        p = rules.index(proposal)
        branches = []
        for r, old in enumerate(rules):
            yes = support[p][r]
            threshold = proposal if mutation == "proposed_threshold" else old
            succeeds = yes >= threshold if mutation == "weak_approval" else yes > threshold
            branches.append(z3.And(
                states[step] == old,
                states[step + 1] == z3.If(succeeds, proposal, old),
            ))
            if old == proposal:
                continue
            for winner, loser, w, losing_index in ((old, proposal, r, p), (proposal, old, p, r)):
                for i, ranks in enumerate(domain.rankings):
                    if not ranks[w] < ranks[losing_index]:
                        personal = z3.If(yes > peaks[i], proposal, old)
                        complaints.append(z3.And(
                            counts[i] > 0, states[step] == old,
                            states[step + 1] == winner, personal != winner,
                        ))
        transitions.append(z3.Or(branches))
    endpoint_bad = [
        z3.And(states[-1] == rule, z3.Not(z3.And(stable[r], other[r])))
        for r, rule in enumerate(rules)
    ]
    return {
        "counts": counts, "base": base, "transitions": transitions,
        "theorem_bad": z3.Or(theorem_bad),
        "algorithm_bad": z3.Or(states[-1] != h, *endpoint_bad, *complaints),
        "support": support, "h": h, "states": states,
    }


def solver_query(constraints, *, witness_variables=()):
    solver = z3.Tactic("smt").solver()
    solver.set(timeout=TIMEOUT_MS)
    solver.add(*constraints)
    status = solver.check()
    if status == z3.unsat:
        return {"status": "UNSAT"}
    if status == z3.unknown:
        return {"status": "UNKNOWN", "reason": solver.reason_unknown()}
    if status == z3.sat:
        result = {"status": "SAT"}
        if witness_variables:
            model = solver.model()
            result["witness_values"] = [
                model.eval(variable, model_completion=True).as_long()
                for variable in witness_variables
            ]
        return result
    raise RuntimeError(f"Unexpected Z3 status: {status}")


def require_status(result, expected, label):
    if result["status"] != expected:
        raise RuntimeError(f"{label}: expected {expected}, obtained {result}")
    return result


def smt_checks(n):
    domain = make_domain(n)
    problem = symbolic_problem(domain)
    return {
        "n": n, "preference_types": len(domain.rankings),
        "nonempty_domain": require_status(solver_query(
            problem["base"] + problem["transitions"],
        ), "SAT", f"n={n} profile and protocol trace"),
        "theorem_1_counterexample": require_status(solver_query(
            problem["base"] + [problem["theorem_bad"]], witness_variables=problem["counts"],
        ), "UNSAT", f"n={n} Theorem 1"),
        "algorithm_1_counterexample": require_status(solver_query(
            problem["base"] + problem["transitions"] + [problem["algorithm_bad"]],
            witness_variables=problem["counts"],
        ), "UNSAT", f"n={n} Algorithm 1"),
    }


def find_negative_control(name, max_n=6):
    if name not in ("weak_approval", "proposed_threshold", "reverse_agenda", "drop_single_peakedness"):
        raise ValueError("Unknown negative control")
    examined = 0
    for n in range(MIN_N, max_n + 1):
        unrestricted = name == "drop_single_peakedness"
        domain = make_domain(n, single_peaked=not unrestricted)
        mutation = None if unrestricted else name
        for counts in compositions(n, len(domain.rankings)):
            examined += 1
            analysis = analyze_profile(domain, counts, mutation=mutation)
            if not analysis["failures"]:
                continue
            problem = symbolic_problem(domain, mutation)
            fixed = [count == value for count, value in zip(problem["counts"], counts)]
            checked = require_status(solver_query(
                problem["base"] + problem["transitions"] + fixed
                + [z3.Or(problem["theorem_bad"], problem["algorithm_bad"])],
            ), "SAT", name)
            return {
                "name": name, "profiles_examined_until_first_counterexample": examined,
                "profile": describe_profile(domain, counts), "analysis": analysis,
                "pinned_counterexample_z3": checked,
            }
    raise RuntimeError(f"No counterexample found for negative control {name} through n={max_n}")


def revolution_control(*, complain):
    domain = make_domain(6)
    counts = [0] * len(domain.rankings)
    counts[domain.rankings.index((0, 1, 2))] = 5
    minority = (2, 1, 0) if complain else (2, 0, 1)
    counts[domain.rankings.index(minority)] = 1
    counts = tuple(counts)
    support = support_table(domain, counts)
    old, proposal = 5, 3
    yes = support[0][2]
    complainers = complaining_groups(domain, counts, support, old, proposal, proposal)
    problem = symbolic_problem(domain)
    symbolic_yes = problem["support"][0][2]
    cf_terms = []
    for i, ranks in enumerate(domain.rankings):
        if not ranks[0] < ranks[2]:
            cf_terms.append(z3.Or(problem["counts"][i] == 0, symbolic_yes > domain.peaks[i]))
    cf = z3.And(cf_terms)
    checked = require_status(solver_query(
        problem["base"] + [
            count == value for count, value in zip(problem["counts"], counts)
        ] + [symbolic_yes > proposal, symbolic_yes <= old, z3.Not(cf) if complain else cf],
    ), "SAT", "revolution complaint control")
    if not (yes > proposal and yes <= old) or bool(complainers) != complain:
        raise RuntimeError("Revolution complaint control disagrees with its expected definition")
    return {
        "profile": describe_profile(domain, counts), "old": old, "proposal": proposal,
        "yes_votes": yes, "old_rule_approves": yes > old, "proposed_rule_approves": yes > proposal,
        "complaining_groups": list(complainers),
        "complaining_voters": sum(counts[i] for i in complainers), "z3": checked,
    }


def paper_figure_control():
    peaks = [6, 6, 6, 6, 8, 8, 9, 9, 9, 10, 10]
    return {
        "source": "arXiv v2 Figure 1 and section 4, pp. 3–4",
        "n": 11, "bliss_point_numerators": peaks,
        "h_numerator": h_from_peaks(11, peaks), "median_numerator": sorted(peaks)[5],
        "scope": "Only h and median; the figure does not specify all cross-peak comparisons",
    }


def run():
    enumerated = [enumerate_profiles(n) for n in range(MIN_N, MAX_N + 1)]
    for row in enumerated:
        if any(row["counterexample_profiles"].values()):
            raise RuntimeError(f"Published target has a bounded counterexample: {row['first_counterexample']}")
    totals = {
        key: sum(row[key] for row in enumerated) for key in (
            "anonymous_profiles", "strict_anonymous_profiles", "represented_labeled_profiles",
            "represented_strict_labeled_profiles", "theorem_1_candidate_checks",
            "algorithm_1_vote_steps", "nontrivial_votes_rejected_at_exact_threshold",
        )
    }
    return {
        "schema_version": 1,
        "source": {
            "authors": ["Ben Abramowitz", "Ehud Shapiro", "Nimrod Talmon"],
            "title": "How to Amend a Constitution? Model, Axioms, and Supermajority Rules",
            "venue": "AAMAS 2021, extended abstract, pp. 1443–1445",
            "retrieved_utc_date": "2026-09-09", "files": SOURCE_FILES,
            "audit_note": "Hashes pin inspected sources; --verify-sources checks cache bytes, not mathematical interpretation",
            "full_version_mapping": "AAMAS Theorem 1: v2 Lemmas 4–6 (pp. 4–5); CF: v2 Theorem 3 (pp. 6–7)",
            "version_warning": "v1 uses 1/2 + delta; v4 is retitled and its numbered theorems are different",
        },
        "scope": {
            "fixed_electorate": True, "fixed_preferences_during_protocol": True,
            "bounds_n_inclusive": [MIN_N, MAX_N],
            "alternatives": "k/n with floor(n/2) <= k < n; integers k are canonical rule labels",
            "majority_alias": "For odd n, floor(n/2)/n and the paper's 1/2 label induce the same strict majority rule",
            "votes": "A proposal wins exactly when its strictly preferring voters exceed the OLD integer threshold k",
            "equality": "Equal vote count retains the status quo; h instead uses a weak >= count condition",
            "protocol": "Algorithm 1: initialize majority, visit every alternative in increasing order, update by R^r",
            "preferences": "All strict complete single-peaked rankings; also all complete weak extensions with a unique peak and only cross-side indifference",
            "not_assumed": "No Euclidean distance, changing membership, separate legal consent, or unconditional acceptance by every voter",
            "median": "Upper median for even n; its interval contains the intervals for either median bliss point",
            "coverage": "Anonymous count vectors; anonymity plus multinomial counts accounts for every labeled profile",
            "complaint_references": "complaining_groups lists ids in the accompanying profile.groups, not compact array positions",
        },
        "enumeration": {"by_n": enumerated, "totals": totals},
        "smt": {
            "solver": "Tactic('smt').solver()", "timeout_ms_per_query": TIMEOUT_MS,
            "encoding": "Integer counts for all ranking types; largest weak h condition, unrolled votes and complaint formulas",
            "by_n": [smt_checks(n) for n in range(MIN_N, MAX_N + 1)],
        },
        "negative_controls": [
            find_negative_control(name) for name in (
                "weak_approval", "proposed_threshold", "reverse_agenda", "drop_single_peakedness",
            )
        ],
        "source_statement_control": {
            "claim": "AAMAS p. 1444 says non-evolutionary revolutions are never complaint-free",
            "result": "COUNTEREXAMPLE_TO_THIS_UNNUMBERED_SENTENCE_NOT_TO_THEOREM_1",
            "complaint_free_revolution": revolution_control(complain=False),
            "revolution_with_complaint": revolution_control(complain=True),
            "version_difference": "v2 p. 7 says never guaranteed to be complaint-free; these examples agree with that weaker statement",
        },
        "h_boundary_control": {
            "n": 4, "bliss_point_numerators": [2, 3, 3, 3],
            "published_weak_h": h_from_peaks(4, [2, 3, 3, 3]),
            "incorrect_strict_h": h_from_peaks(4, [2, 3, 3, 3], strict_mutation=True),
        },
        "paper_figure_control": paper_figure_control(),
        "runtime": {"python": platform.python_version(), "z3": z3.get_version_string()},
        "not_established": [
            "A proof for unbounded electorates",
            "The v2 strategyproofness or social-cost theorems, or the v4 axiomatic results",
            "A legal or political implementation of Article V, or Godel's historical argument",
        ],
    }


def verify_sources(directory):
    for name, expected in SOURCE_FILES.items():
        raw = (Path(directory) / name).read_bytes()
        if len(raw) != expected["bytes"] or sha256(raw).hexdigest() != expected["sha256"]:
            raise ValueError(f"Source fingerprint mismatch: {name}")
    return len(SOURCE_FILES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--verify-sources", type=Path, metavar="SESSION_FILES")
    args = parser.parse_args()
    try:
        if args.verify_sources:
            print(f"Verified {verify_sources(args.verify_sources)} source-file fingerprints.")
        document = run()
        encoded = json.dumps(document, indent=2, sort_keys=True) + "\n"
        if args.write:
            RESULTS.write_text(encoded, encoding="utf-8")
        if args.check:
            if not RESULTS.is_file() or RESULTS.read_text(encoding="utf-8") != encoded:
                raise ValueError("Missing or stale self-amendment result artifact")
            print("Self-amendment artifact matches byte-for-byte.")
        print(json.dumps({
            "enumeration_totals": document["enumeration"]["totals"],
            "smt_query_status_counts": dict(Counter(
                row[key]["status"] for row in document["smt"]["by_n"]
                for key in ("nonempty_domain", "theorem_1_counterexample", "algorithm_1_counterexample")
            )),
            "negative_control_witnesses": len(document["negative_controls"]),
            "source_statement_control": document["source_statement_control"]["result"],
        }, indent=2, sort_keys=True))
    except (OSError, ValueError, RuntimeError, z3.Z3Exception) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
