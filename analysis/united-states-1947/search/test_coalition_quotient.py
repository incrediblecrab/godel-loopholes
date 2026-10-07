"""Controls for coalition equivalence and the finite model's closed-form classification."""

from dataclasses import replace
from contextlib import redirect_stderr
from io import StringIO
from itertools import product
import unittest
from unittest.mock import patch

from article_v_model import (
    Amendment, Constitution, Policy, Screening, State, Step, Suffrage, Target, Votes,
    apply_step, explore, rejection, support_profile,
)
from coalition_quotient import (
    InconclusiveCertificate, canonical_support, class_size, classified_lengths, main,
    quotient_certificates, representatives, run, signature, threshold,
)


class CoalitionQuotientTests(unittest.TestCase):
    def test_classes_partition_small_coalition_spaces(self):
        for states in range(1, 6):
            counts = {}
            subsets = [frozenset(i for i in range(states) if mask >> i & 1)
                       for mask in range(1 << states)]
            for ratifiers, consenters in product(subsets, repeat=2):
                support = replace(support_profile(len(ratifiers), states),
                                  ratifiers=ratifiers, consenters=consenters)
                key = signature(support)
                counts[key] = counts.get(key, 0) + 1
                self.assertEqual(signature(canonical_support(support)), key)
            self.assertEqual(set(counts), {signature(support) for support in representatives(states)})
            self.assertEqual(sum(counts.values()), 2**(2*states))
            for key, count in counts.items():
                self.assertEqual(count, class_size(states, key))

    def test_canonicalization_preserves_other_support_fields(self):
        support = replace(support_profile(48), house=Votes(435, 217, 145), mode="conventions",
                          consenters=frozenset({0, 47}))
        canonical = canonical_support(support)
        self.assertEqual(canonical.house, support.house)
        self.assertEqual(canonical.senate, support.senate)
        self.assertEqual(canonical.mode, support.mode)
        self.assertEqual(canonical.states, support.states)
        self.assertFalse(canonical.house.can_propose())

    def test_zero_and_positive_low_support_must_remain_distinct(self):
        zero, one = support_profile(0), support_profile(1)
        self.assertNotEqual(signature(zero), signature(one))
        state = State(replace(Constitution(), ratifiers_required=1), Amendment.END_ELECTIONS)
        step = Step("ratify", Amendment.END_ELECTIONS)
        self.assertIsNotNone(rejection(state, step, Policy(), zero))
        self.assertIsNone(rejection(state, step, Policy(), one))

    def test_consent_identity_and_unanimity_are_separate_observations(self):
        support = support_profile(36)
        no_affected = replace(support, consenters=frozenset({0}))
        affected = replace(support, consenters=frozenset({47}))
        unanimous = replace(support, consenters=support.all_states)
        self.assertEqual(len(no_affected.consenters), len(affected.consenters))
        self.assertEqual(len({signature(item) for item in (no_affected, affected, unanimous)}), 3)
        expected = classified_lengths(Policy(self_entrenched=True), affected)
        self.assertIsNone(expected[Target.CONCENTRATED_POWERS.value])
        self.assertEqual(expected[Target.UNEQUAL_SENATE.value], 2)

    def test_universal_guard_certificates_and_plants(self):
        clean = quotient_certificates(48)
        self.assertEqual(clean["ratification_guard_preserved"]["status"], "UNSAT")
        self.assertEqual(clean["permitted_deprivation_tests_preserved"]["status"], "UNSAT")
        for plant, name in (
            ("threshold", "ratification_guard_preserved"),
            ("consent-id", "permitted_deprivation_tests_preserved"),
            ("consent-all", "permitted_deprivation_tests_preserved"),
        ):
            self.assertEqual(quotient_certificates(48, plant)[name]["status"], "SAT")

    def test_new_threshold_value_invalidates_the_claimed_domain(self):
        with patch("coalition_quotient.amendment_effect", return_value={"ratifiers_required": 2}):
            with self.assertRaisesRegex(ValueError, "Threshold domain changed"):
                quotient_certificates(48)

    def test_unknown_certificate_is_inconclusive_not_a_refutation(self):
        with patch("coalition_quotient.unsat_certificate", return_value={"status": "UNKNOWN", "reason": "timeout"}):
            with self.assertRaises(InconclusiveCertificate):
                run()
        with patch("coalition_quotient.run", side_effect=InconclusiveCertificate("timeout")):
            with patch("sys.argv", ["coalition_quotient.py", "--check"]), redirect_stderr(StringIO()) as output:
                self.assertEqual(main(), 2)
            self.assertIn("INCONCLUSIVE", output.getvalue())

    def test_classification_matches_every_representative_and_policy(self):
        for suffrage, entrenched, floor, screening, change in product(
            Suffrage, (False, True), (False, True), Screening, (False, True),
        ):
            policy = Policy(suffrage, entrenched, floor, screening, change)
            for support in representatives(48):
                expected = classified_lengths(policy, support)
                graph = explore(policy, support)
                for target in Target:
                    path = graph.shortest_path(target)
                    self.assertEqual(None if path is None else len(path), expected[target.value])

    def test_arbitrary_identities_have_the_same_transition_guards(self):
        policy = Policy(self_entrenched=True)
        support = replace(support_profile(37), ratifiers=frozenset(range(11, 48)),
                          consenters=frozenset({3, 17, 47}))
        canonical = canonical_support(support)
        for values in product((False, True), repeat=5):
            for required in (1, threshold(48)):
                constitution = Constitution(*values, required)
                for amendment in Amendment:
                    for state, step in (
                        (State(constitution), Step("propose", amendment)),
                        (State(constitution, amendment), Step("ratify", amendment)),
                        (State(constitution, amendment), Step("withdraw", amendment)),
                    ):
                        left = rejection(state, step, policy, support)
                        right = rejection(state, step, policy, canonical)
                        self.assertEqual(left, right)
                        if left is None:
                            self.assertEqual(apply_step(state, step, policy, support),
                                             apply_step(state, step, policy, canonical))


if __name__ == "__main__":
    unittest.main()
