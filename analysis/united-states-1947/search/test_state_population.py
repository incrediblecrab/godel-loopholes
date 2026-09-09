import csv
from hashlib import sha256
import io
from itertools import combinations
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import z3

from state_population import (
    CSV_FIELDS, CSV_SHA256, EXPECTED_STATES, EXPECTED_TOTALS, HERE,
    build_results, compare_share, format_percentage, load_populations,
    population_csv, read_population_csv, sorted_bound, validate_populations,
    verify_source, z3_bound,
)


class PopulationDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_populations()
        cls.raw = (HERE / "state-populations.csv").read_text(encoding="utf-8")

    def altered_csv(self, change):
        rows = list(csv.DictReader(io.StringIO(self.raw)))
        change(rows)
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        stream.seek(0)
        return stream

    def test_exact_48_state_universe(self):
        for populations in self.data.values():
            self.assertEqual(len(populations), 48)
            self.assertEqual(set(populations), EXPECTED_STATES)
            self.assertTrue({"Arizona", "New Mexico"} <= populations.keys())
            self.assertFalse(
                {"Alaska", "Hawaii", "District of Columbia", "Puerto Rico"} & populations.keys()
            )
            self.assertTrue(all(type(value) is int and value > 0 for value in populations.values()))

    def test_primary_published_totals_not_just_csv_sums(self):
        self.assertEqual(sum(self.data[1940].values()), 131_006_184)
        self.assertEqual(sum(self.data[1910].values()), 91_641_197)
        self.assertEqual(sum(self.data[1940].values()) + 663_091, 131_669_275)
        self.assertEqual(sum(self.data[1910].values()) + 331_069, 91_972_266)
        self.assertEqual(sum(self.data[1940].values()) + 663_091 + 72_524 + 423_330, 132_165_129)
        self.assertEqual(sum(self.data[1910].values()) + 331_069 + 64_356 + 191_909, 92_228_531)

    def test_canonical_csv_fingerprint_and_round_trip(self):
        self.assertEqual(sha256(self.raw.encode()).hexdigest(), CSV_SHA256)
        self.assertEqual(population_csv(self.data), self.raw)
        self.assertEqual(read_population_csv(io.StringIO(self.raw)), self.data)

    def test_duplicate_or_missing_state_is_rejected(self):
        for change in (lambda rows: rows.append(rows[0].copy()), lambda rows: rows.pop()):
            with self.subTest(change=change), self.assertRaises(ValueError):
                read_population_csv(self.altered_csv(change))

    def test_territory_or_dc_cannot_replace_a_state(self):
        for area in ("Alaska", "Hawaii", "District of Columbia", "Puerto Rico", "Guam"):
            with self.subTest(area=area), self.assertRaises(ValueError):
                read_population_csv(self.altered_csv(lambda rows: rows[0].update(state=area)))

    def test_missing_negative_zero_or_fractional_population_is_rejected(self):
        for value in ("", "-1", "0", "1.5", "nan"):
            for year in (1940, 1910):
                with self.subTest(value=value, year=year), self.assertRaises(ValueError):
                    read_population_csv(self.altered_csv(
                        lambda rows: rows[0].update({f"population_{year}": value})
                    ))

    def test_total_change_is_rejected(self):
        with self.assertRaises(ValueError):
            read_population_csv(self.altered_csv(
                lambda rows: rows[0].update(population_1940="2832962")
            ))

    def test_missing_and_extra_columns_are_rejected(self):
        for raw in (
            self.raw.replace(",population_1910", "", 1),
            self.raw.replace("state,population_1940", "state,extra,population_1940", 1),
            self.raw.replace("Alabama,2832961,2138093", "Alabama,2832961"),
            self.raw.replace("Alabama,2832961,2138093", "Alabama,2832961,2138093,99"),
        ):
            with self.subTest(raw=raw[:70]), self.assertRaises(ValueError):
                read_population_csv(io.StringIO(raw))

    def test_balanced_tampering_does_not_evade_source_audit(self):
        changed = {year: populations.copy() for year, populations in self.data.items()}
        changed[1940]["Alabama"] += 1
        changed[1940]["Arizona"] -= 1
        validate_populations(changed)
        with patch("state_population.read_source_xlsx", return_value=self.data):
            with self.assertRaisesRegex(ValueError, "does not match"):
                verify_source(Path("unused-source.xlsx"), "xlsx", changed)
        changed_raw = population_csv(changed).encode()
        with patch("state_population.Path.read_bytes", return_value=changed_raw):
            with self.assertRaisesRegex(ValueError, "SHA256"):
                load_populations()

    def test_source_binary_change_fails_closed(self):
        with patch("state_population.Path.read_bytes", return_value=b"not the Census file"):
            with self.assertRaisesRegex(ValueError, "pinned Census source"):
                verify_source(Path("unused-source.xlsx"), "xlsx", self.data)


class PopulationOptimizationTests(unittest.TestCase):
    def test_known_toy_minimum_and_maximum(self):
        populations = {"A": 7, "B": 2, "C": 5, "D": 3}
        for solver in (sorted_bound, z3_bound):
            self.assertEqual(solver(populations, 2)["population_total"], 5)
            self.assertEqual(solver(populations, 2, maximize=True)["population_total"], 12)

    def test_exhaustive_toy_control_including_ties(self):
        populations = {"D": 2, "B": 2, "A": 9, "C": 6}
        for cardinality in range(5):
            totals = [
                sum(populations[state] for state in states)
                for states in combinations(populations, cardinality)
            ]
            for maximize in (False, True):
                expected = max(totals) if maximize else min(totals)
                for solver in (sorted_bound, z3_bound):
                    with self.subTest(k=cardinality, maximize=maximize, solver=solver.__name__):
                        result = solver(populations, cardinality, maximize=maximize)
                        self.assertEqual(result["status"], "OPTIMAL")
                        self.assertEqual(result["population_total"], expected)
                        self.assertEqual(len(result["selected_states"]), cardinality)
        self.assertEqual(sorted_bound(populations, 1)["selected_states"], ["B"])
        self.assertFalse(sorted_bound(populations, 1)["unique_optimum"])
        self.assertTrue(sorted_bound(populations, 2)["unique_optimum"])

    def test_zero_all_and_empty_state_universes(self):
        for populations in ({}, {"A": 0, "B": 0}, {"A": 1, "B": 100}):
            for cardinality in (0, len(populations)):
                for maximize in (False, True):
                    for solver in (sorted_bound, z3_bound):
                        result = solver(populations, cardinality, maximize=maximize)
                        expected = sum(populations.values()) if cardinality else 0
                        self.assertEqual(result["status"], "OPTIMAL")
                        self.assertEqual(result["population_total"], expected)

    def test_infeasible_cardinality_is_unsat(self):
        for cardinality in (-1, 3):
            for solver in (sorted_bound, z3_bound):
                self.assertEqual(solver({"A": 2, "B": 7}, cardinality)["status"], "UNSAT")

    def test_invalid_inputs_are_not_coerced(self):
        for solver in (sorted_bound, z3_bound):
            for populations, cardinality in (
                ({"A": -1}, 1), ({"A": 1.5}, 1), ({"A": True}, 1),
                ({"A": 1}, True), ({"A": 1}, 1.0), ({"": 1}, 1),
            ):
                with self.subTest(populations=populations, k=cardinality), self.assertRaises(ValueError):
                    solver(populations, cardinality)
        for timeout in (0, -1, True):
            with self.assertRaises(ValueError):
                z3_bound({"A": 1}, 1, timeout_ms=timeout)

    def test_optimization_unknown_is_never_reported_as_a_bound(self):
        with patch("state_population.z3.Optimize") as factory:
            factory.return_value.check.return_value = z3.unknown
            factory.return_value.reason_unknown.return_value = "test timeout"
            result = z3_bound({"A": 1}, 1)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["reason"], "test timeout")
        self.assertNotIn("population_total", result)

    def test_sat_with_unclosed_objective_bounds_is_unknown(self):
        with patch("state_population.z3.Optimize") as factory:
            factory.return_value.check.return_value = z3.sat
            factory.return_value.lower.return_value = z3.IntVal(1)
            factory.return_value.upper.return_value = z3.IntVal(2)
            result = z3_bound({"A": 1}, 1)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertNotIn("population_total", result)

    def test_unknown_in_a_boundary_check_is_not_an_optimum(self):
        for checks, expected_stage in (
            ([z3.unknown], "exact_boundary"),
            ([z3.sat, z3.unknown], "strictly_better"),
        ):
            with patch("state_population.z3.Tactic") as factory:
                factory.return_value.solver.return_value.check.side_effect = checks
                factory.return_value.solver.return_value.reason_unknown.return_value = "boundary timeout"
                result = z3_bound({"A": 1, "B": 2}, 1)
            self.assertEqual(result["status"], "UNKNOWN")
            self.assertEqual(result["stage"], expected_stage)
            self.assertNotIn("population_total", result)

    def test_exact_optimum_is_allowed_and_one_resident_better_is_not(self):
        for maximize in (False, True):
            result = z3_bound({"A": 3, "B": 7, "C": 10}, 2, maximize=maximize)
            self.assertEqual(result["population_total"], 17 if maximize else 10)
            self.assertEqual(result["objective_lower_bound"], result["objective_upper_bound"])
            self.assertEqual(result["exact_boundary"], "SAT")
            self.assertEqual(result["strictly_better"], "UNSAT")

    def test_population_percentages_use_exact_comparisons_not_rounded_display(self):
        self.assertEqual(compare_share(1, 2, 50, 100), "equal")
        self.assertEqual(compare_share(499_999, 1_000_000, 1, 2), "below")
        self.assertEqual(compare_share(500_001, 1_000_000, 1, 2), "above")
        self.assertEqual(format_percentage(49_999_999, 100_000_000), "50.0000")
        self.assertEqual(compare_share(49_999_999, 100_000_000, 1, 2), "below")
        self.assertEqual(format_percentage(1, 32, places=2), "3.13")
        self.assertEqual(format_percentage(0, 10), "0.0000")
        self.assertEqual(format_percentage(10, 10), "100.0000")
        for numerator, denominator in ((0, 0), (-1, 10), (1.0, 2), (True, 2)):
            with self.subTest(numerator=numerator, denominator=denominator):
                with self.assertRaises(ValueError):
                    format_percentage(numerator, denominator)
                with self.assertRaises(ValueError):
                    compare_share(numerator, denominator, 1, 2)
        with self.assertRaises(ValueError):
            compare_share(1, 2, float("nan"), 100)


class CensusResultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_populations()
        cls.results = build_results(cls.data)

    def test_all_eight_measured_optima_and_independent_algorithms(self):
        expected = {
            1940: {36: (54_982_723, 125_577_321), 32: (42_959_945, 121_803_769)},
            1910: {36: (40_865_581, 87_698_188), 32: (31_810_758, 84_946_545)},
        }
        for year, cardinalities in expected.items():
            for cardinality, totals in cardinalities.items():
                for direction, total in zip(("minimum", "maximum"), totals):
                    with self.subTest(year=year, k=cardinality, direction=direction):
                        result = self.results["census_years"][str(year)]["bounds"][str(cardinality)][direction]
                        self.assertEqual(result["fraction"], {
                            "numerator": total, "denominator": EXPECTED_TOTALS[year],
                        })
                        self.assertEqual(result["z3"]["population_total"], total)
                        self.assertEqual(len(set(result["sorted_witness"])), cardinality)
                        self.assertEqual(
                            sum(self.data[year][state] for state in result["sorted_witness"]), total,
                        )
                        self.assertTrue(result["algorithms_agree"])
                        self.assertTrue(result["witness_sets_agree"])
                        self.assertTrue(result["unique_optimum"])
                        self.assertEqual(result["z3"]["exact_boundary"], "SAT")
                        self.assertEqual(result["z3"]["strictly_better"], "UNSAT")

    def test_complement_identity_and_membership_boundary(self):
        for year, populations in self.data.items():
            for cardinality in (36, 32):
                maximum = sorted_bound(populations, cardinality, maximize=True)["population_total"]
                excluded_minimum = sorted_bound(populations, 48 - cardinality)["population_total"]
                self.assertEqual(maximum, EXPECTED_TOTALS[year] - excluded_minimum)
        controls = self.results["threshold_controls"]
        self.assertEqual(controls["ratification"]["required_states"], 36)
        self.assertEqual(controls["convention_applications"]["required_states"], 32)
        for result in controls.values():
            self.assertTrue(result["exact_equality_passes"])
            self.assertTrue(result["one_fewer_fails"])

    def test_repeated_state_actions_are_not_distinct_states(self):
        result = self.results["two_amendments"]
        self.assertEqual(result["state_amendment_actions"], 2 * 36)
        self.assertEqual(result["minimum_distinct_states"], 36)
        self.assertEqual(result["maximum_distinct_states"], 48)
        self.assertEqual(result["minimum_intersection_states"], 2 * 36 - 48)

    def test_unverified_binary_sources_are_not_reported_verified(self):
        for result in self.results["validation"]["source_files"].values():
            self.assertEqual(result["status"], "NOT_RUN")

    def test_results_generation_stops_on_unknown(self):
        with patch("state_population.z3_bound", return_value={"status": "UNKNOWN", "reason": "test"}):
            with self.assertRaisesRegex(RuntimeError, "UNKNOWN"):
                build_results(self.data)

    def test_checked_in_numeric_results_match_a_fresh_run(self):
        saved = json.loads((HERE / "state_population_results.json").read_text(encoding="utf-8"))
        self.assertEqual(saved["census_years"], self.results["census_years"])
        self.assertEqual(saved["threshold_controls"], self.results["threshold_controls"])
        self.assertEqual(saved["two_amendments"], self.results["two_amendments"])
        self.assertEqual(saved["validation"]["csv_sha256"], CSV_SHA256)


if __name__ == "__main__":
    unittest.main()
