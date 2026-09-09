import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import z3

from attendance_audit import (
    HERE, Attendance, brute_minimum, general_controls, run, smt_minimum,
)
from state_admission import majority_required, proposal_required


class AttendanceAuditTests(unittest.TestCase):
    def test_1947_house_and_senate_thresholds(self):
        expected = {
            Attendance.FULL: ((218, 290), (49, 64)),
            Attendance.FAVORABLE: ((110, 146), (25, 33)),
            Attendance.SELF_QUORATE: ((218, 218), (49, 49)),
        }
        for attendance, pairs in expected.items():
            for members, pair in zip((435, 96), pairs):
                self.assertEqual(
                    (majority_required(members, attendance), proposal_required(members, attendance)),
                    pair,
                )
                for two_thirds, minimum in zip((False, True), pair):
                    solved = smt_minimum(members, attendance, two_thirds=two_thirds)
                    self.assertEqual(solved["status"], "OPTIMAL")
                    self.assertEqual(solved["yes"], minimum)
                    self.assertEqual(solved["smaller_coalition"], "UNSAT")

    def test_small_chambers_against_all_present_and_yes_assignments(self):
        for members in range(1, 25):
            for attendance in Attendance:
                for two_thirds in (False, True):
                    expected = brute_minimum(members, attendance, two_thirds=two_thirds)
                    computed = (
                        proposal_required(members, attendance) if two_thirds
                        else majority_required(members, attendance)
                    )
                    self.assertEqual(computed, expected, (members, attendance, two_thirds))

    def test_exact_boundary_and_one_fewer(self):
        for members in (96, 435, 10**40):
            for attendance in Attendance:
                for two_thirds in (False, True):
                    required = (
                        proposal_required(members, attendance) if two_thirds
                        else majority_required(members, attendance)
                    )
                    if attendance == Attendance.SELF_QUORATE:
                        self.assertGreater(2 * required, members)
                        self.assertLessEqual(2 * (required - 1), members)
                    else:
                        present = members if attendance == Attendance.FULL else members // 2 + 1
                        if two_thirds:
                            self.assertGreaterEqual(3 * required, 2 * present)
                            self.assertLess(3 * (required - 1), 2 * present)
                        else:
                            self.assertGreater(2 * required, present)
                            self.assertLessEqual(2 * (required - 1), present)

    def test_invalid_chamber_or_unspecified_attendance_is_rejected(self):
        for members in (0, -1, True, 1.5):
            for method in (brute_minimum, smt_minimum):
                with self.assertRaises(ValueError):
                    method(members, Attendance.FULL, two_thirds=False)
            with self.assertRaises(ValueError):
                majority_required(members, Attendance.FULL)
        with self.assertRaises(ValueError):
            smt_minimum(48, "unknown", two_thirds=True)

    def test_optimization_unknown_is_explicit(self):
        with patch("attendance_audit.z3.Optimize") as factory:
            factory.return_value.check.return_value = z3.unknown
            factory.return_value.reason_unknown.return_value = "test timeout"
            result = smt_minimum(435, Attendance.FULL, two_thirds=True)
        self.assertEqual(result, {"status": "UNKNOWN", "reason": "test timeout"})

    def test_minimality_unknown_is_explicit(self):
        with patch("attendance_audit.z3.Solver") as factory:
            factory.return_value.check.return_value = z3.unknown
            factory.return_value.reason_unknown.return_value = "boundary timeout"
            result = smt_minimum(435, Attendance.FULL, two_thirds=True)
        self.assertEqual(result, {"status": "UNKNOWN", "reason": "boundary timeout"})

    def test_result_generation_stops_on_unknown(self):
        with patch("attendance_audit.smt_minimum", return_value={"status": "UNKNOWN"}):
            with self.assertRaisesRegex(RuntimeError, "Inconclusive"):
                run()

    def test_general_controls_include_a_real_negative(self):
        controls = general_controls()
        self.assertEqual(controls.pop("legacy_inequality_without_n_ge_4_at_n_1"), "SAT")
        self.assertEqual(controls.pop("strict_majority_advantage_does_not_hold_at_six_voters"), "SAT")
        self.assertEqual(len(controls), 8)
        self.assertEqual(set(controls.values()), {"UNSAT"})

    def test_six_voters_are_an_exception_to_strict_majority_advantage(self):
        self.assertEqual(majority_required(6, Attendance.FULL), 4)
        self.assertEqual(proposal_required(6, Attendance.FULL), 4)
        self.assertEqual(majority_required(7, Attendance.FULL), 4)
        self.assertEqual(proposal_required(7, Attendance.FULL), 5)

    def test_artifact_gate_rejects_a_planted_mixed_attendance_result(self):
        with tempfile.TemporaryDirectory(prefix="godel-attendance-") as directory:
            scratch = Path(directory)
            for name in (
                "attendance_audit.py", "test_attendance_audit.py", "state_admission.py",
                "article_v_model.py", "attendance_audit_results.json",
            ):
                shutil.copyfile(HERE / name, scratch / name)
            command = [sys.executable, "-B", "-m", "attendance_audit", "--check"]
            control = subprocess.run(command, cwd=scratch, capture_output=True, text=True)
            self.assertEqual(control.returncode, 0, control.stdout + control.stderr)
            artifact = scratch / "attendance_audit_results.json"
            corrupted = json.loads(artifact.read_text(encoding="utf-8"))
            corrupted["rows"][Attendance.SELF_QUORATE.value]["totals"]["article_v_proposal"] = 179
            artifact.write_text(json.dumps(corrupted), encoding="utf-8")
            mutant = subprocess.run(command, cwd=scratch, capture_output=True, text=True)
            self.assertEqual(mutant.returncode, 1, mutant.stdout + mutant.stderr)
            self.assertIn("Missing or stale attendance-audit artifact", mutant.stderr)

    def test_persisted_results_do_not_mix_attendance(self):
        actual = run()
        saved = json.loads((HERE / "attendance_audit_results.json").read_text(encoding="utf-8"))
        self.assertEqual(actual, saved)
        expected = {
            Attendance.FULL: (267, 354),
            Attendance.FAVORABLE: (135, 179),
            Attendance.SELF_QUORATE: (267, 267),
        }
        for attendance, (majority, proposal) in expected.items():
            totals = actual["rows"][attendance.value]["totals"]
            self.assertEqual(totals["majority_exclusion"], majority)
            self.assertEqual(totals["article_v_proposal"], proposal)
            self.assertEqual(totals["two_thirds_expulsion"], proposal)
        legacy = actual["legacy_mixed_comparison"]
        self.assertEqual(legacy["cascade_entry_self_quorate"], 267)
        self.assertEqual(legacy["direct_proposal_favorable"], 179)
        self.assertFalse(legacy["same_attendance_assumption"])
        self.assertFalse(legacy["strict_cost_domination_established"])


if __name__ == "__main__":
    unittest.main()
