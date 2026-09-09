from dataclasses import replace
import unittest
from unittest.mock import patch

import z3

from state_admission import (
    Attendance, Scenario, admission_can_begin, enumerate_minimum, gates,
    general_controls, historical_denominator_control, minimum_all_supporting_additions, ratification_reached,
    smt_minimum, target_matrix,
)


class StateAdmissionTests(unittest.TestCase):
    def test_expanding_denominator_not_the_old_threshold(self):
        self.assertEqual(minimum_all_supporting_additions(48, 0), 144)
        self.assertFalse(ratification_reached(48, 0, 36, 36))
        self.assertFalse(ratification_reached(48, 0, 143, 143))
        self.assertTrue(ratification_reached(48, 0, 144, 144))

    def test_near_boundary_and_no_additions(self):
        self.assertEqual(minimum_all_supporting_additions(48, 35), 4)
        self.assertEqual(minimum_all_supporting_additions(48, 36), 0)
        self.assertEqual(minimum_all_supporting_additions(48, 48), 0)

    def test_invalid_counts_raise_errors(self):
        for inputs in ((0, 0, 0, 0), (48, 49, 0, 0), (48, 0, -1, 0), (48, 0, 2, 3)):
            with self.assertRaises(ValueError):
                ratification_reached(*inputs)
        with self.assertRaises(ValueError):
            Scenario(48, 435, 436, 49, 1)
        with self.assertRaises(ValueError):
            Scenario(48, 435, 218, 97, 1)

    def test_published_count_depends_on_unpublished_inputs(self):
        compatible = Scenario(50, 435, 258, 60, 14)
        initial_house = replace(compatible, house_support=257)
        self.assertEqual(enumerate_minimum(compatible)["new_states"], 96)
        self.assertEqual(enumerate_minimum(initial_house)["new_states"], 99)
        self.assertEqual(smt_minimum(compatible)["new_states"], 96)
        self.assertEqual(smt_minimum(initial_house)["new_states"], 99)

    def test_joint_minimum_keeps_the_house_gate(self):
        scenario = Scenario(48, 435, 218, 49, 1)
        self.assertEqual(minimum_all_supporting_additions(48, 1), 140)
        self.assertFalse(gates(scenario, 140)["house_proposal"])
        self.assertEqual(enumerate_minimum(scenario)["new_states"], 216)
        self.assertEqual(smt_minimum(scenario)["new_states"], 216)

    def test_favorable_attendance_is_a_separate_assumption(self):
        scenario = Scenario(48, 435, 110, 25, 1, Attendance.FAVORABLE)
        self.assertTrue(admission_can_begin(scenario))
        self.assertEqual(enumerate_minimum(scenario)["new_states"], 140)
        for changed in (
            replace(scenario, president_cooperates=False),
            replace(scenario, attendance=Attendance.SELF_QUORATE),
            replace(scenario, attendance=Attendance.FULL),
        ):
            self.assertFalse(admission_can_begin(changed))
            self.assertEqual(enumerate_minimum(changed)["status"], "BLOCKED")
            self.assertEqual(smt_minimum(changed)["status"], "BLOCKED")

    def test_new_votes_cannot_authorize_the_admission_act(self):
        scenario = Scenario(48, 435, 1, 1, 1)
        self.assertTrue(all(gates(scenario, 1000).values()))
        self.assertEqual(enumerate_minimum(scenario)["status"], "BLOCKED")

    def test_support_is_not_entailed_by_admission(self):
        self.assertTrue(ratification_reached(48, 1, 140, 140))
        self.assertFalse(ratification_reached(48, 1, 140, 0))
        self.assertFalse(ratification_reached(48, 1, 140, 139))

    def test_direct_amendment_needs_no_presidential_signature(self):
        scenario = Scenario(48, 435, 290, 64, 36, president_cooperates=False)
        self.assertEqual(enumerate_minimum(scenario)["new_states"], 0)
        self.assertEqual(smt_minimum(scenario)["new_states"], 0)

    def test_consent_objection_survives_state_admission(self):
        scenario = Scenario(48, 435, 110, 25, 1, Attendance.FAVORABLE)
        rows = target_matrix(scenario, 140)
        self.assertEqual(
            {(row["suffrage"], row["self_entrenched"]): row["reachable"] for row in rows},
            {("formal", False): True, ("formal", True): True,
             ("functional", False): True, ("functional", True): False},
        )

    def test_general_arithmetic_controls(self):
        result = general_controls()
        self.assertEqual(result["boundary_cases_checked"], 20_300)
        self.assertEqual(result["closed_form_equivalence_counterexample_search"], "UNSAT")
        self.assertEqual(
            result["below_threshold_old_states_succeed_without_any_new_support"], "UNSAT",
        )
        self.assertFalse(result["fixed_denominator_negative_control"]["correct_expanded_denominator_says_pass"])

    def test_unknown_is_not_a_minimum(self):
        with patch("state_admission.z3.Optimize") as factory:
            factory.return_value.check.return_value = z3.unknown
            factory.return_value.reason_unknown.return_value = "test timeout"
            result = smt_minimum(Scenario(48, 435, 218, 49, 1))
        self.assertEqual(result, {"status": "UNKNOWN", "reason": "test timeout"})

    def test_historical_certification_keeps_the_expanded_denominator(self):
        result = historical_denominator_control()
        self.assertEqual((result["initial_states"], result["states_at_certification"]), (46, 48))
        self.assertEqual((result["initial_threshold"], result["threshold_at_certification"]), (35, 36))
        self.assertEqual(result["principal_ratification_list_count"], 36)
        self.assertEqual(result["all_ratifications_acknowledged_on_page"], 38)
        self.assertTrue(result["one_fewer_than_threshold"]["frozen_original_denominator_would_accept"])
        self.assertFalse(result["one_fewer_than_threshold"]["current_denominator_accepts"])


if __name__ == "__main__":
    unittest.main()
