"""Behavioral controls for the finite model, not tests of constitutional truth."""

from dataclasses import replace
import unittest
from unittest.mock import patch

import z3

from article_v_model import (
    Amendment,
    InvalidTransition,
    Policy,
    Screening,
    Step,
    Suffrage,
    Support,
    Target,
    Votes,
    apply_step,
    explore,
    initial_state,
    reaches,
    replay,
    support_profile,
)
from article_v_smt import solve


REPEAL = Amendment.REPEAL_PROVISO
CONCENTRATE = Amendment.CONCENTRATE
END_ELECTIONS = Amendment.END_ELECTIONS


def enact(amendment):
    return [Step("propose", amendment), Step("ratify", amendment)]


class ArticleVTests(unittest.TestCase):
    def setUp(self):
        self.policy = Policy()
        self.support = support_profile(36)

    def test_1947_proposing_thresholds(self):
        self.assertEqual((self.support.house.present, self.support.house.yes), (218, 146))
        self.assertEqual((self.support.senate.present, self.support.senate.yes), (49, 33))
        for vote in (self.support.house, self.support.senate):
            self.assertTrue(vote.can_propose())
            self.assertFalse(replace(vote, yes=vote.yes - 1).can_propose())
            self.assertFalse(replace(vote, present=vote.seats // 2).can_propose())

    def test_invalid_inputs_are_errors(self):
        for values in ((0, 0, 0), (10, 11, 5), (10, 5, 6), (10, 5, -1)):
            with self.assertRaises(ValueError):
                Votes(*values)
        for count in (-1, 49):
            with self.assertRaises(ValueError):
                support_profile(count)
        with self.assertRaises(ValueError):
            replace(self.support, consenters=frozenset({48}))
        with self.assertRaises(ValueError):
            replace(self.support, mode="referendum")
        with self.assertRaises(ValueError):
            initial_state(0)
        with self.assertRaises(ValueError):
            solve(self.policy, self.support, None, max_steps=-1)

    def test_proposal_has_no_normative_effect(self):
        start = initial_state()
        pending = apply_step(start, Step("propose", REPEAL), self.policy, self.support)
        self.assertEqual(pending.constitution, start.constitution)
        self.assertTrue(pending.constitution.proviso)
        self.assertEqual(pending.pending, REPEAL)

    def test_ratification_without_proposal_is_rejected(self):
        with self.assertRaisesRegex(InvalidTransition, "no-matching-proposal"):
            replay(self.policy, self.support, [Step("ratify", CONCENTRATE)])

    def test_withdrawal_cannot_change_the_constitution(self):
        endpoint = replay(self.policy, self.support, [
            Step("propose", REPEAL), Step("withdraw", REPEAL),
        ])
        self.assertEqual(endpoint, initial_state())

    def test_repeal_has_only_its_declared_effect(self):
        endpoint = replay(self.policy, self.support, enact(REPEAL))
        self.assertEqual(endpoint.constitution, replace(initial_state().constitution, proviso=False))

    def test_functional_reading_requires_a_separate_repeal(self):
        with self.assertRaisesRegex(InvalidTransition, "deprived-state-without-consent"):
            replay(self.policy, self.support, enact(CONCENTRATE))
        endpoint = replay(self.policy, self.support, enact(REPEAL) + enact(CONCENTRATE))
        self.assertTrue(reaches(endpoint, Target.CONCENTRATED_POWERS))
        self.assertEqual(len(explore(self.policy, self.support).shortest_path(
            Target.CONCENTRATED_POWERS,
        )), 4)

    def test_35_states_cannot_ratify_or_bootstrap_a_lower_threshold(self):
        support = support_profile(35)
        for amendment in Amendment:
            with self.subTest(amendment=amendment):
                with self.assertRaisesRegex(InvalidTransition, "state-ratification-threshold"):
                    replay(self.policy, support, enact(amendment))
        exploration = explore(self.policy, support)
        self.assertEqual({state.constitution for state in exploration.parents}, {
            initial_state().constitution,
        })

    def test_new_threshold_cannot_authorize_its_own_enactment(self):
        with self.assertRaisesRegex(InvalidTransition, "state-ratification-threshold"):
            replay(
                Policy(suffrage=Suffrage.FORMAL), support_profile(35),
                enact(Amendment.LOWER_AND_CONCENTRATE),
            )
        endpoint = replay(self.policy, self.support, enact(Amendment.LOWER_THRESHOLD))
        self.assertEqual(endpoint.constitution.ratifiers_required, 1)

    def test_same_instrument_cannot_use_its_own_repeal(self):
        for screening in Screening:
            with self.subTest(screening=screening):
                with self.assertRaisesRegex(InvalidTransition, "deprived-state-without-consent"):
                    replay(
                        replace(self.policy, screening=screening), self.support,
                        enact(Amendment.REPEAL_AND_CONCENTRATE),
                    )

    def test_formal_reading_bypasses_repeal_for_this_target(self):
        policy = Policy(suffrage=Suffrage.FORMAL, self_entrenched=True)
        endpoint = replay(policy, self.support, enact(CONCENTRATE))
        self.assertTrue(endpoint.constitution.proviso)
        self.assertTrue(endpoint.constitution.equal_senate)
        self.assertTrue(reaches(endpoint, Target.CONCENTRATED_POWERS))

    def test_self_entrenchment_blocks_ordinary_repeal(self):
        policy = replace(self.policy, self_entrenched=True)
        with self.assertRaisesRegex(InvalidTransition, "proviso-repeal"):
            replay(policy, self.support, enact(REPEAL))
        self.assertIsNone(explore(policy, self.support).shortest_path(Target.CONCENTRATED_POWERS))

    def test_unanimous_consent_is_a_direct_positive_control(self):
        policy = replace(self.policy, self_entrenched=True)
        endpoint = replay(policy, support_profile(48), enact(CONCENTRATE))
        self.assertTrue(reaches(endpoint, Target.CONCENTRATED_POWERS))
        self.assertTrue(endpoint.constitution.proviso)

    def test_consent_identity_not_just_cardinality(self):
        policy = replace(self.policy, self_entrenched=True)
        without_affected = self.support
        with_affected = replace(
            self.support, consenters=frozenset(range(35)) | frozenset({47}),
        )
        self.assertEqual(len(without_affected.consenters), len(with_affected.consenters))
        with self.assertRaisesRegex(InvalidTransition, "deprived-state-without-consent"):
            replay(policy, without_affected, enact(Amendment.UNEQUAL_SENATE))
        self.assertTrue(reaches(
            replay(policy, with_affected, enact(Amendment.UNEQUAL_SENATE)),
            Target.UNEQUAL_SENATE,
        ))

    def test_consent_is_not_a_substitute_for_ratification(self):
        support = replace(support_profile(35), consenters=frozenset(range(48)))
        with self.assertRaisesRegex(InvalidTransition, "state-ratification-threshold"):
            replay(self.policy, support, enact(CONCENTRATE))

    def test_ratification_is_not_blanket_consent_from_nonratifiers(self):
        support = replace(self.support, ratifiers=frozenset(range(48)))
        with self.assertRaisesRegex(InvalidTransition, "deprived-state-without-consent"):
            replay(self.policy, support, enact(CONCENTRATE))

    def test_target_sensitivity_electoral_lock_is_not_all_powers(self):
        policy = replace(self.policy, self_entrenched=True)
        endpoint = replay(policy, self.support, enact(END_ELECTIONS))
        self.assertTrue(reaches(endpoint, Target.EXECUTIVE_ELECTORAL_LOCK))
        self.assertFalse(reaches(endpoint, Target.CONCENTRATED_POWERS))
        self.assertTrue(endpoint.constitution.proviso)

    def test_implicit_democracy_floor_changes_results(self):
        policy = replace(self.policy, democracy_floor=True)
        for amendment in (CONCENTRATE, END_ELECTIONS):
            with self.assertRaisesRegex(InvalidTransition, "implicit-democracy-floor"):
                replay(policy, support_profile(48), enact(amendment))
        self.assertFalse(replay(policy, self.support, enact(REPEAL)).constitution.proviso)

    def test_removing_step_one_blocks_closed_world_path(self):
        alphabet = tuple(amendment for amendment in Amendment if amendment not in (
            REPEAL, Amendment.REPEAL_AND_CONCENTRATE,
        ))
        exploration = explore(self.policy, self.support, alphabet)
        self.assertIsNone(exploration.shortest_path(Target.CONCENTRATED_POWERS))
        self.assertTrue(all(state.constitution.proviso for state in exploration.parents))
        self.assertEqual(solve(
            self.policy, self.support, Target.CONCENTRATED_POWERS, alphabet=alphabet,
        ).status, "UNSAT")

    def test_ratification_modes_are_abstract_not_different_thresholds(self):
        legislature = explore(self.policy, self.support)
        conventions = explore(self.policy, replace(self.support, mode="conventions"))
        self.assertEqual(legislature.parents, conventions.parents)

    def test_screening_stage_preserves_ratified_endpoints(self):
        proposal = explore(replace(self.policy, screening=Screening.PROPOSAL), self.support)
        ratification = explore(self.policy, self.support)
        self.assertEqual(
            {state.constitution for state in proposal.parents},
            {state.constitution for state in ratification.parents},
        )
        self.assertLess(len(proposal.parents), len(ratification.parents))

    def test_smt_sat_witnesses_are_replayed(self):
        for policy, count, target in (
            (Policy(), 36, Target.CONCENTRATED_POWERS),
            (Policy(suffrage=Suffrage.FORMAL), 36, Target.CONCENTRATED_POWERS),
            (Policy(self_entrenched=True), 36, Target.EXECUTIVE_ELECTORAL_LOCK),
            (Policy(self_entrenched=True), 48, Target.UNEQUAL_SENATE),
        ):
            with self.subTest(policy=policy, count=count, target=target):
                support = support_profile(count)
                result = solve(policy, support, target)
                self.assertEqual(result.status, "SAT")
                self.assertTrue(reaches(replay(policy, support, list(result.steps)), target))

    def test_smt_bounded_unsat_does_not_mean_unbounded_impossibility(self):
        self.assertEqual(solve(
            self.policy, self.support, Target.CONCENTRATED_POWERS, max_steps=2,
        ).status, "UNSAT")
        self.assertIsNotNone(explore(self.policy, self.support).shortest_path(
            Target.CONCENTRATED_POWERS,
        ))

    def test_smt_nonvacuity_and_empty_alphabet(self):
        self.assertEqual(solve(self.policy, self.support, None, alphabet=()).status, "SAT")
        self.assertEqual(solve(
            self.policy, self.support, Target.CONCENTRATED_POWERS, alphabet=(),
        ).status, "UNSAT")

    def test_smt_unknown_is_not_unsat(self):
        with patch("article_v_smt.z3.Solver") as factory:
            factory.return_value.check.return_value = z3.unknown
            factory.return_value.reason_unknown.return_value = "test timeout"
            result = solve(self.policy, self.support, Target.CONCENTRATED_POWERS)
        self.assertEqual(result.status, "UNKNOWN")
        self.assertEqual(result.reason, "test timeout")
        self.assertEqual(result.steps, ())

    def test_forbidden_congressional_proposal_cannot_be_ratified(self):
        support = replace(self.support, house=replace(self.support.house, yes=145))
        with self.assertRaisesRegex(InvalidTransition, "congressional-proposal-threshold"):
            replay(self.policy, support, enact(REPEAL))
        self.assertEqual(len(explore(self.policy, support).parents), 1)
        self.assertEqual(solve(
            self.policy, support, Target.CONCENTRATED_POWERS,
        ).status, "UNSAT")


if __name__ == "__main__":
    unittest.main()
