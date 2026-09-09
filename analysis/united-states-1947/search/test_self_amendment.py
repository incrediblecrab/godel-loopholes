from contextlib import redirect_stderr
import io
from itertools import product
import json
from math import comb
import unittest
from unittest.mock import patch

import z3

import self_amendment as replication
from self_amendment import (
    Domain, FAILURE_KEYS, RESULTS, SOURCE_FILES, alternatives, analyze_profile,
    complaining_groups, compositions, describe_profile, enumerate_profiles,
    evolutionary_constitution, find_negative_control, h_from_peaks,
    is_single_peaked, make_domain, paper_figure_control, preference_types,
    require_status, revolution_control, smt_checks, solver_query, support_table,
    validate_counts, verify_sources,
)


def profile_counts(domain, groups):
    counts = [0] * len(domain.rankings)
    for ranks, count in groups:
        counts[domain.rankings.index(ranks)] += count
    return tuple(counts)


def brute_preference_types(size):
    accepted = set()
    for ranks in product(range(size), repeat=size):
        if ranks.count(0) != 1 or set(ranks) != set(range(max(ranks) + 1)):
            continue
        peak = ranks.index(0)
        valid = True
        for x in range(size):
            for y in range(size):
                if (y < x <= peak or peak <= x < y) and not ranks[x] < ranks[y]:
                    valid = False
        if valid:
            accepted.add(ranks)
    return accepted


def assert_serialized_complaints(case, profile, votes):
    groups = {}
    ranks = {}
    peaks = {}
    for group in profile["groups"]:
        case.assertIn("id", group)
        group_id = group["id"]
        case.assertNotIn(group_id, groups)
        case.assertGreater(group["count"], 0)
        groups[group_id] = group
        tiers = group["ranking_best_to_worst"]
        case.assertEqual(len(tiers[0]), 1)
        peaks[group_id] = tiers[0][0]
        ranks[group_id] = {
            rule: rank for rank, tier in enumerate(tiers) for rule in tier
        }
    case.assertEqual(sum(group["count"] for group in groups.values()), profile["n"])
    for vote in votes:
        old, proposal = vote["old"], vote["proposal"]
        winner = vote["winner"]
        other = old if winner == proposal else proposal
        support = sum(
            group["count"] for group_id, group in groups.items()
            if ranks[group_id][proposal] < ranks[group_id][old]
        )
        expected = {
            group_id for group_id in groups
            if (proposal if support > peaks[group_id] else old) != winner
            and ranks[group_id][winner] >= ranks[group_id][other]
        }
        reported = vote["complaining_groups"]
        case.assertEqual(len(reported), len(set(reported)))
        case.assertTrue(set(reported) <= groups.keys())
        case.assertEqual(set(reported), expected)
        case.assertEqual(vote["yes_votes"], support)
        case.assertEqual(
            vote["complaining_voters"], sum(groups[group_id]["count"] for group_id in reported),
        )


class DomainTests(unittest.TestCase):
    def test_canonical_grid_and_odd_majority_alias(self):
        self.assertEqual(alternatives(5), (2, 3, 4))
        self.assertEqual(alternatives(6), (3, 4, 5))
        for n in range(2, 9):
            rules = alternatives(n)
            self.assertEqual(len(rules), (n + 1) // 2)
            self.assertNotIn(n, rules)
            for yes in range(n + 1):
                self.assertEqual(yes > rules[0], 2 * yes > n)
                self.assertEqual(yes > rules[-1], yes == n)

    def test_all_rank_types_match_independent_weak_order_enumeration(self):
        for size, expected in enumerate((1, 2, 5, 12), start=1):
            generated = preference_types(size)
            self.assertEqual(set(generated), brute_preference_types(size))
            self.assertEqual(len(generated), expected)
            self.assertTrue(all(is_single_peaked(ranks) for ranks in generated))
            strict = preference_types(size, allow_ties=False)
            self.assertEqual(len(strict), 2 ** (size - 1))
            self.assertEqual(set(strict), {
                ranks for ranks in generated if len(set(ranks)) == size
            })

    def test_cross_peak_comparisons_are_not_invented_from_distances(self):
        domain = make_domain(6)
        left = profile_counts(domain, [((1, 0, 2), 6)])
        right = profile_counts(domain, [((2, 0, 1), 6)])
        tied = profile_counts(domain, [((1, 0, 1), 6)])
        self.assertEqual(support_table(domain, left)[2][0], 0)
        self.assertEqual(support_table(domain, right)[2][0], 6)
        self.assertEqual(support_table(domain, tied)[2][0], 0)
        self.assertEqual(support_table(domain, tied)[0][2], 0)
        for counts in (left, right, tied):
            self.assertEqual(analyze_profile(domain, counts)["h"], 4)
            self.assertEqual(evolutionary_constitution(domain, counts)["winner"], 4)
        support = support_table(domain, tied)
        self.assertFalse(complaining_groups(domain, tied, support, 3, 5, 3))
        self.assertTrue(complaining_groups(domain, tied, support, 3, 5, 5))

    def test_fixed_electorate_and_invalid_profile_controls(self):
        domain = make_domain(4)
        for counts in ((1,), (1, 2), (1, 4), (-1, 5), (True, 3), (1.0, 3)):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                validate_counts(domain, counts)
        for n in (0, 1, -1, True, 4.0):
            with self.subTest(n=n), self.assertRaises(ValueError):
                alternatives(n)
        for rankings in (((0, 0),), ((0, 2),), ((0, 1), (0, 1)), ((0, -1),), ((0,),)):
            with self.subTest(rankings=rankings), self.assertRaises(ValueError):
                Domain(4, rankings)

    def test_profile_compositions_are_exhaustive_without_duplicates(self):
        for n in range(5):
            for width in range(1, 5):
                profiles = list(compositions(n, width))
                self.assertEqual(len(profiles), comb(n + width - 1, n))
                self.assertEqual(len(set(profiles)), len(profiles))
                self.assertTrue(all(sum(counts) == n for counts in profiles))
        for n, width in ((-1, 2), (2, 0), (True, 2), (2, 1.0)):
            with self.assertRaises(ValueError):
                list(compositions(n, width))

    def test_only_admissible_thresholds_and_outcomes_are_accepted(self):
        domain = make_domain(4)
        counts = (2, 2)
        support = support_table(domain, counts)
        for old, proposal, winner in ((2, 4, 2), (1, 2, 2), (2, 3, 4), (True, 3, 3)):
            with self.assertRaises(ValueError):
                complaining_groups(domain, counts, support, old, proposal, winner)
        for peaks in ([2, 3, 3], [2, 3, 3, 4], [True, 3, 3, 3]):
            with self.assertRaises(ValueError):
                h_from_peaks(4, peaks)

    def test_serialized_profile_preserves_nonzero_group_ids(self):
        domain = make_domain(6)
        counts = profile_counts(domain, [((0, 1, 2), 5), ((2, 1, 0), 1)])
        groups = describe_profile(domain, counts)["groups"]
        for group in groups:
            self.assertIn("id", group)
        self.assertEqual([group["id"] for group in groups], [
            i for i, count in enumerate(counts) if count
        ])
        self.assertEqual([group["id"] for group in groups], [0, 4])
        self.assertEqual([group["count"] for group in groups], [5, 1])


class ProtocolTests(unittest.TestCase):
    def test_equal_yes_count_rejects_and_weak_inequality_is_a_real_mutation(self):
        domain = make_domain(4)
        counts = (2, 2)
        correct = evolutionary_constitution(domain, counts)
        mutated = evolutionary_constitution(domain, counts, mutation="weak_approval")
        self.assertEqual(correct["winner"], 2)
        vote = correct["trace"][1]
        self.assertEqual((vote["yes_votes"], vote["threshold"]), (2, 2))
        self.assertFalse(vote["accepted"])
        self.assertEqual(mutated["winner"], 3)
        self.assertEqual(mutated["trace"][1]["complaining_voters"], 2)

    def test_old_threshold_not_proposed_threshold_and_h_is_weak(self):
        domain = make_domain(4)
        counts = (1, 3)
        self.assertEqual(evolutionary_constitution(domain, counts)["winner"], 3)
        self.assertEqual(evolutionary_constitution(
            domain, counts, mutation="proposed_threshold",
        )["winner"], 2)
        self.assertEqual(h_from_peaks(4, [2, 3, 3, 3]), 3)
        self.assertEqual(h_from_peaks(4, [2, 3, 3, 3], strict_mutation=True), 2)

    def test_current_threshold_updates_after_each_success(self):
        domain = make_domain(6)
        counts = profile_counts(domain, [((0, 1, 2), 2), ((2, 1, 0), 4)])
        run = evolutionary_constitution(domain, counts)
        self.assertEqual([vote["threshold"] for vote in run["trace"]], [3, 3, 4])
        self.assertEqual([vote["winner"] for vote in run["trace"]], [3, 4, 4])
        self.assertEqual(run["trace"][-1]["yes_votes"], 4)
        self.assertEqual(evolutionary_constitution(
            domain, counts, mutation="reverse_agenda",
        )["winner"], 5)

    def test_published_initialization_agenda_and_noop(self):
        domain = make_domain(6)
        counts = profile_counts(domain, [((0, 1, 2), 6)])
        run = evolutionary_constitution(domain, counts)
        self.assertEqual([vote["proposal"] for vote in run["trace"]], [3, 4, 5])
        self.assertEqual(run["trace"][0]["old"], 3)
        self.assertEqual(run["trace"][0]["yes_votes"], 0)
        self.assertFalse(run["trace"][0]["complaining_groups"])
        self.assertEqual(run["winner"], 3)
        self.assertEqual(len(run["trace"]), len(domain.rules))

    def test_unanimity_is_n_minus_one_not_an_impossible_threshold_of_n(self):
        domain = make_domain(6)
        unanimous = profile_counts(domain, [((0, 1, 2), 6)])
        one_veto = profile_counts(domain, [((0, 1, 2), 5), ((2, 1, 0), 1)])
        self.assertNotIn(5, analyze_profile(domain, unanimous)["self_stable"])
        self.assertIn(5, analyze_profile(domain, one_veto)["self_stable"])
        self.assertEqual(support_table(domain, unanimous)[0][2], 6)
        self.assertEqual(support_table(domain, one_veto)[0][2], 5)

    def test_even_electorate_uses_upper_median_for_the_larger_claimed_interval(self):
        analysis = analyze_profile(make_domain(4), (2, 2))
        self.assertEqual(analysis["h"], 2)
        self.assertEqual(analysis["upper_median"], 3)
        self.assertEqual(analysis["self_stable"], [2, 3])
        self.assertEqual(analysis["other_stable"], [2, 3])

    def test_paper_figure_is_reproduced_without_inventing_complete_preferences(self):
        result = paper_figure_control()
        self.assertEqual(result["n"], 11)
        self.assertEqual(result["h_numerator"], 7)
        self.assertEqual(result["median_numerator"], 8)
        self.assertEqual(len(result["bliss_point_numerators"]), 11)

    def test_anonymity_and_compressed_counts_preserve_all_votes(self):
        domain = make_domain(6)
        counts = profile_counts(domain, [((0, 1, 2), 2), ((1, 0, 1), 1), ((2, 1, 0), 3)])
        ballots = [ranks for ranks, count in zip(domain.rankings, counts) for _ in range(count)]
        support = support_table(domain, counts)
        for p in range(len(domain.rules)):
            for r in range(len(domain.rules)):
                literal = sum(ranks[p] < ranks[r] for ranks in reversed(ballots))
                self.assertEqual(support[p][r], literal)
        self.assertTrue(describe_profile(domain, counts)["single_peaked"])
        self.assertFalse(describe_profile(domain, counts)["strict_preferences"])


class SolverAndFalsificationTests(unittest.TestCase):
    def test_sat_unsat_and_exact_model_values(self):
        x = z3.Int("test_count")
        self.assertEqual(solver_query([x == 7], witness_variables=(x,)), {
            "status": "SAT", "witness_values": [7],
        })
        self.assertEqual(solver_query([x == 7, x < 7]), {"status": "UNSAT"})

    def test_unknown_is_explicit_and_never_reads_a_model(self):
        with patch("self_amendment.z3.Tactic") as factory:
            solver = factory.return_value.solver.return_value
            solver.check.return_value = z3.unknown
            solver.reason_unknown.return_value = "test timeout"
            result = solver_query([z3.BoolVal(True)], witness_variables=(z3.Int("x"),))
            solver.model.assert_not_called()
        self.assertEqual(result, {"status": "UNKNOWN", "reason": "test timeout"})
        with self.assertRaisesRegex(RuntimeError, "UNKNOWN"):
            require_status(result, "UNSAT", "counterexample search")

    def test_nonempty_domain_does_not_turn_a_later_unknown_into_success(self):
        with patch("self_amendment.solver_query", side_effect=(
            {"status": "SAT"}, {"status": "UNKNOWN", "reason": "proof timeout"},
        )):
            with self.assertRaisesRegex(RuntimeError, "UNKNOWN"):
                smt_checks(4)
        with patch("self_amendment.solver_query", return_value={"status": "SAT"}):
            with self.assertRaisesRegex(RuntimeError, "expected UNSAT"):
                smt_checks(4)

    def test_four_mutations_have_concrete_independently_checked_witnesses(self):
        for name in ("weak_approval", "proposed_threshold", "reverse_agenda", "drop_single_peakedness"):
            with self.subTest(name=name):
                result = find_negative_control(name)
                self.assertTrue(result["analysis"]["failures"])
                self.assertEqual(result["pinned_counterexample_z3"]["status"], "SAT")
                self.assertLessEqual(result["profile"]["n"], 6)
                self.assertEqual(
                    result["profile"]["single_peaked"], name != "drop_single_peakedness",
                )
                assert_serialized_complaints(
                    self, result["profile"], result["analysis"]["protocol"]["trace"],
                )

    def test_literal_never_complaint_free_sentence_has_a_valid_counterexample(self):
        example = revolution_control(complain=False)
        self.assertTrue(example["profile"]["single_peaked"])
        self.assertTrue(example["profile"]["strict_preferences"])
        self.assertEqual((example["profile"]["n"], example["old"], example["proposal"]), (6, 5, 3))
        self.assertEqual(example["yes_votes"], 5)
        self.assertFalse(example["old_rule_approves"])
        self.assertTrue(example["proposed_rule_approves"])
        self.assertEqual(example["complaining_voters"], 0)
        self.assertEqual(example["z3"]["status"], "SAT")

    def test_revolutions_are_not_guaranteed_complaint_free_either(self):
        example = revolution_control(complain=True)
        self.assertFalse(example["old_rule_approves"])
        self.assertTrue(example["proposed_rule_approves"])
        self.assertEqual(example["complaining_voters"], 1)
        self.assertEqual(example["z3"]["status"], "SAT")


class ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.small_runs = [enumerate_profiles(n) for n in range(2, 7)]
        cls.small_smt = [smt_checks(n) for n in range(2, 7)]
        cls.saved = json.loads(RESULTS.read_text(encoding="utf-8"))

    def test_all_small_profiles_and_rules_satisfy_published_claims(self):
        self.assertEqual(sum(row["anonymous_profiles"] for row in self.small_runs), 346)
        self.assertEqual(sum(row["strict_anonymous_profiles"] for row in self.small_runs), 150)
        for row in self.small_runs:
            self.assertEqual(row["counterexample_profiles"], {name: 0 for name in FAILURE_KEYS})
            self.assertIsNone(row["first_counterexample"])
            self.assertEqual(sum(row["endpoint_histogram"].values()), row["anonymous_profiles"])
            self.assertEqual(row["theorem_1_candidate_checks"], row["algorithm_1_vote_steps"])

    def test_independent_symbolic_checks_cover_the_same_small_domain(self):
        for row in self.small_smt:
            self.assertEqual(row["nonempty_domain"]["status"], "SAT")
            self.assertEqual(row["theorem_1_counterexample"]["status"], "UNSAT")
            self.assertEqual(row["algorithm_1_counterexample"]["status"], "UNSAT")

    def test_saved_small_results_match_fresh_computation(self):
        self.assertEqual(self.saved["enumeration"]["by_n"][:5], self.small_runs)
        self.assertEqual(self.saved["smt"]["by_n"][:5], self.small_smt)
        totals = self.saved["enumeration"]["totals"]
        self.assertEqual(totals["anonymous_profiles"], 107_752)
        self.assertEqual(totals["strict_anonymous_profiles"], 10_017)
        self.assertEqual(totals["represented_labeled_profiles"], 465_832_279)
        self.assertEqual(totals["represented_strict_labeled_profiles"], 18_879_513)
        self.assertEqual(totals["algorithm_1_vote_steps"], 430_651)

    def test_saved_complaint_references_resolve_to_the_correct_groups(self):
        for control in self.saved["negative_controls"]:
            with self.subTest(control=control["name"]):
                assert_serialized_complaints(
                    self, control["profile"], control["analysis"]["protocol"]["trace"],
                )
        for name in ("complaint_free_revolution", "revolution_with_complaint"):
            control = self.saved["source_statement_control"][name]
            with self.subTest(control=name):
                assert_serialized_complaints(
                    self, control["profile"], [{**control, "winner": control["proposal"]}],
                )

    def test_missing_profile_is_detected_as_incomplete_enumeration(self):
        real_compositions = compositions
        def incomplete(total, width):
            rows = iter(real_compositions(total, width))
            next(rows)
            yield from rows
        with patch("self_amendment.compositions", side_effect=incomplete):
            with self.assertRaisesRegex(RuntimeError, "coverage"):
                enumerate_profiles(2)

    def test_source_fingerprints_fail_closed(self):
        self.assertEqual(len(SOURCE_FILES), 7)
        self.assertEqual(len({row["url"] for row in SOURCE_FILES.values()}), 7)
        for source in SOURCE_FILES.values():
            self.assertEqual(len(source["sha256"]), 64)
            self.assertGreater(source["bytes"], 0)
        with patch("self_amendment.Path.read_bytes", return_value=b"changed source"):
            with self.assertRaisesRegex(ValueError, "fingerprint mismatch"):
                verify_sources(HERE_FOR_TESTS)

    def test_unknown_never_overwrites_a_verified_artifact(self):
        with (
            patch("self_amendment.run", side_effect=RuntimeError("UNKNOWN: test timeout")),
            patch("self_amendment.RESULTS") as output,
            patch("sys.argv", ["self_amendment.py", "--write"]),
            redirect_stderr(io.StringIO()),
        ):
            with self.assertRaises(SystemExit) as error:
                replication.main()
            self.assertEqual(error.exception.code, 2)
            output.write_text.assert_not_called()

    def test_check_rejects_stale_artifact_without_writing(self):
        with (
            patch("self_amendment.run", return_value={"fresh": True}),
            patch("self_amendment.RESULTS") as output,
            patch("sys.argv", ["self_amendment.py", "--check"]),
            redirect_stderr(io.StringIO()),
        ):
            output.is_file.return_value = True
            output.read_text.return_value = "{}\n"
            with self.assertRaises(SystemExit) as error:
                replication.main()
            self.assertEqual(error.exception.code, 2)
            output.write_text.assert_not_called()


HERE_FOR_TESTS = RESULTS.parent


if __name__ == "__main__":
    unittest.main()
