"""Exact resident-population bounds on subsets of the 48 states in 1947."""

import argparse
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import platform
import re
import subprocess
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

import z3


HERE = Path(__file__).resolve().parent
YEARS = (1940, 1910)
CSV_FIELDS = ("state", "population_1940", "population_1910")
CSV_SHA256 = "289c226281ca89c4daa4bb68db03cd3fd1937b2eacb22f75f598d6590f6190df"
EXPECTED_STATES = frozenset((
    "Alabama", "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
    "Delaware", "Florida", "Georgia", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
    "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
))
EXCLUDED = ("District of Columbia", "Alaska", "Hawaii")
REFERENCE_ROWS = {
    1940: {
        "United States": 132_165_129, "District of Columbia": 663_091,
        "Alaska": 72_524, "Hawaii": 423_330, "Puerto Rico": 1_869_255,
    },
    1910: {
        "United States": 92_228_531, "District of Columbia": 331_069,
        "Alaska": 64_356, "Hawaii": 191_909, "Puerto Rico": 1_118_012,
    },
}
EXPECTED_TOTALS = {
    year: rows["United States"] - sum(rows[area] for area in EXCLUDED)
    for year, rows in REFERENCE_ROWS.items()
}
SOURCE_BASE = (
    "https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/"
    "population-change-data-table"
)
SOURCE_TITLE = (
    "Change in Resident Population of the 50 States, the District of Columbia, "
    "and Puerto Rico: 1910 to 2020"
)
SOURCE = {
    "publisher": "U.S. Census Bureau, U.S. Department of Commerce",
    "table": SOURCE_TITLE,
    "release_date": "2021-04-26",
    "retrieved_utc_date": "2026-09-09",
    "units": "resident persons, not thousands; decennial census counts",
    "landing_page": (
        "https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html"
    ),
    "xlsx": {
        "url": SOURCE_BASE + ".xlsx",
        "sha256": "053ac373f7f76b12bfa0d1f9f9ccb5a238f37c04b8b14bc3cc90208bea18732f",
        "bytes": 24_339,
        "sheet": "Population Change",
        "area_cells": "S6:S56",
        "resident_population_cells": {"1940": "T6:T56", "1910": "Z6:Z56"},
        "national_total_cells": {"1940": "T57", "1910": "Z57"},
        "national_geography_note_cell": "A63",
    },
    "pdf": {
        "url": SOURCE_BASE + ".pdf",
        "sha256": "3920c1a1a38c7fcb758182c392b335d57bde8c57f544c8adb281cc213ac390b1",
        "bytes": 157_673,
        "data_page": 3,
        "national_geography_note_page": 1,
    },
    "national_total_definition": (
        "The source's United States row retrospectively includes the resident "
        "population of all 50 states and DC; Puerto Rico is a separate row."
    ),
}


def validate_populations(data):
    if set(data) != set(YEARS):
        raise ValueError("Both and only the 1940 and 1910 census columns are required")
    for year, populations in data.items():
        if set(populations) != EXPECTED_STATES:
            raise ValueError(f"{year}: expected exactly the 48 states in 1947")
        if any(type(value) is not int or value <= 0 for value in populations.values()):
            raise ValueError(f"{year}: resident populations must be positive integers")
        if sum(populations.values()) != EXPECTED_TOTALS[year]:
            raise ValueError(f"{year}: state sum disagrees with the primary national total")


def read_population_csv(stream):
    reader = csv.DictReader(stream)
    if tuple(reader.fieldnames or ()) != CSV_FIELDS:
        raise ValueError(f"Expected CSV columns {CSV_FIELDS}")
    data = {year: {} for year in YEARS}
    for row in reader:
        state = row["state"]
        if None in row or state in data[1940]:
            raise ValueError("Unexpected CSV fields or duplicate state")
        for year in YEARS:
            text = row[f"population_{year}"]
            if text is None or re.fullmatch(r"[0-9]+", text) is None:
                raise ValueError(f"{state}: missing or non-integer population for {year}")
            data[year][state] = int(text)
    validate_populations(data)
    return data


def load_populations(path=HERE / "state-populations.csv"):
    raw = Path(path).read_bytes()
    if sha256(raw).hexdigest() != CSV_SHA256:
        raise ValueError("CSV SHA256 differs from the source-verified extraction")
    return read_population_csv(io.StringIO(raw.decode("utf-8"), newline=""))


def population_csv(data):
    validate_populations(data)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(CSV_FIELDS)
    for state in sorted(EXPECTED_STATES):
        writer.writerow((state, *(data[year][state] for year in YEARS)))
    return stream.getvalue()


def _check_source_bytes(path, format_name):
    raw = Path(path).read_bytes()
    reference = SOURCE[format_name]
    if len(raw) != reference["bytes"] or sha256(raw).hexdigest() != reference["sha256"]:
        raise ValueError(f"{format_name.upper()} differs from the pinned Census source")
    return raw


def _validate_source_rows(rows):
    required = EXPECTED_STATES | set(REFERENCE_ROWS[1940])
    if set(rows) != required:
        raise ValueError("Source must contain the expected 51 geographic rows, US, and PR")
    data = {year: {state: rows[state][year] for state in EXPECTED_STATES} for year in YEARS}
    validate_populations(data)
    for year in YEARS:
        for area, expected in REFERENCE_ROWS[year].items():
            if rows[area][year] != expected:
                raise ValueError(f"{year}: primary reference row mismatch for {area}")
        geographic_total = sum(rows[area][year] for area in EXPECTED_STATES | set(EXCLUDED))
        if geographic_total != rows["United States"][year]:
            raise ValueError(f"{year}: 50 states plus DC do not match published US total")
    return data


def read_source_xlsx(path):
    raw = _check_source_bytes(path, "xlsx")
    namespace = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(io.BytesIO(raw)) as archive:
        workbook = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        sheets = workbook.findall("s:sheets/s:sheet", namespace)
        if len(sheets) != 1 or sheets[0].get("name") != "Population Change":
            raise ValueError("Unexpected Census workbook sheet")
        strings = [
            "".join(item.itertext())
            for item in ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
        ]
        cells = {}
        sheet = ElementTree.fromstring(archive.read("xl/worksheets/sheet1.xml"))
        for cell in sheet.findall(".//s:c", namespace):
            value = cell.find("s:v", namespace)
            if value is not None:
                cells[cell.get("r")] = (
                    strings[int(value.text)] if cell.get("t") == "s" else value.text
                )
    expected_headers = {
        "A3": SOURCE_TITLE, "S4": "Area", "T4": "1940 Census", "Z4": "1910 Census",
        "T5": "Resident Population 1940 Census",
        "Z5": "Resident Population 1910 Census",
    }
    if any(cells.get(cell) != text for cell, text in expected_headers.items()):
        raise ValueError("Census title, years, or resident-population headers changed")
    if "50 states and the District of Columbia" not in cells.get("A63", ""):
        raise ValueError("National geography note missing")
    rows = {}
    for index in (*range(6, 58), 62):
        area = cells[f"S{index}"]
        if area in rows:
            raise ValueError("Duplicate area in source workbook")
        rows[area] = {1940: int(cells[f"T{index}"]), 1910: int(cells[f"Z{index}"])}
    return _validate_source_rows(rows)


def read_source_pdf(path):
    _check_source_bytes(path, "pdf")
    text = subprocess.run(
        ["pdftotext", "-layout", "-f", "3", "-l", "3", str(path), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    required = EXPECTED_STATES | set(REFERENCE_ROWS[1940])
    rows = {}
    for line in text.splitlines():
        match = re.match(r"^([A-Za-z][A-Za-z ]*?)\s{2,}(\d[\d,]*\s+.*)$", line)
        if match and match[1] in required:
            fields = match[2].split()
            if len(fields) != 8 or match[1] in rows:
                raise ValueError("Unexpected historical PDF row structure")
            rows[match[1]] = {
                1940: int(fields[0].replace(",", "")),
                1910: int(fields[6].replace(",", "")),
            }
    return _validate_source_rows(rows)


def verify_source(path, format_name, data):
    readers = {"xlsx": read_source_xlsx, "pdf": read_source_pdf}
    if readers[format_name](path) != data:
        raise ValueError(f"CSV does not match the primary {format_name.upper()} values")
    return {
        "status": "VERIFIED",
        "sha256": SOURCE[format_name]["sha256"],
        "matched_state_year_values": 96,
        "published_national_totals_and_exclusions_match": True,
    }


def _validate_problem(populations, cardinality):
    if type(cardinality) is not int:
        raise ValueError("State cardinality must be an integer")
    if any(not isinstance(name, str) or not name for name in populations):
        raise ValueError("States require nonempty names")
    if any(type(value) is not int or value < 0 for value in populations.values()):
        raise ValueError("Objective weights must be nonnegative integer resident counts")


def sorted_bound(populations, cardinality, *, maximize=False):
    _validate_problem(populations, cardinality)
    if not 0 <= cardinality <= len(populations):
        return {"status": "UNSAT"}
    order = sorted(
        populations,
        key=lambda state: (-populations[state] if maximize else populations[state], state),
    )
    selected = order[:cardinality]
    return {
        "status": "OPTIMAL",
        "population_total": sum(populations[state] for state in selected),
        "selected_states": selected,
        "unique_optimum": (
            cardinality in (0, len(populations))
            or populations[order[cardinality - 1]] != populations[order[cardinality]]
        ),
    }


def z3_bound(populations, cardinality, *, maximize=False, timeout_ms=60_000):
    _validate_problem(populations, cardinality)
    if type(timeout_ms) is not int or timeout_ms <= 0:
        raise ValueError("Solver timeout must be a positive integer in milliseconds")
    # Binary integers keep the objective linear; Z3 receives no population ordering.
    selected = {state: z3.Int(f"selected_{i}") for i, state in enumerate(populations)}
    constraints = [condition for x in selected.values() for condition in (x >= 0, x <= 1)]
    count = z3.Sum(list(selected.values())) if selected else z3.IntVal(0)
    objective = z3.Sum([
        populations[state] * x for state, x in selected.items()
    ]) if selected else z3.IntVal(0)
    constraints.append(count == cardinality)
    optimizer = z3.Optimize()
    optimizer.set(timeout=timeout_ms, elim_01=False)
    optimizer.add(*constraints)
    handle = optimizer.maximize(objective) if maximize else optimizer.minimize(objective)
    status = optimizer.check()
    if status == z3.unknown:
        return {"status": "UNKNOWN", "stage": "optimization", "reason": optimizer.reason_unknown()}
    if status == z3.unsat:
        return {"status": "UNSAT"}
    lower, upper = optimizer.lower(handle), optimizer.upper(handle)
    if not z3.is_int_value(lower) or not z3.is_int_value(upper) or lower.as_long() != upper.as_long():
        return {"status": "UNKNOWN", "stage": "optimization", "reason": "Unclosed exact objective bounds"}
    optimum = lower.as_long()
    model = optimizer.model()
    witness = [state for state, x in selected.items() if model.eval(x).as_long() == 1]
    if (
        len(witness) != cardinality
        or sum(populations[state] for state in witness) != optimum
        or model.eval(objective).as_long() != optimum
    ):
        raise RuntimeError("Z3 model does not attain its claimed objective bound")
    checker = z3.Tactic("smt").solver()
    checker.set(timeout=timeout_ms)
    checker.add(*constraints)
    for stage, predicate, expected in (
        ("exact_boundary", objective == optimum, z3.sat),
        ("strictly_better", objective > optimum if maximize else objective < optimum, z3.unsat),
    ):
        checker.push()
        checker.add(predicate)
        checked = checker.check()
        if checked == z3.unknown:
            return {"status": "UNKNOWN", "stage": stage, "reason": checker.reason_unknown()}
        checker.pop()
        if checked != expected:
            raise RuntimeError(f"Z3 {stage} control returned {checked}, expected {expected}")
    return {
        "status": "OPTIMAL",
        "population_total": optimum,
        "selected_states": sorted(witness),
        "objective_lower_bound": optimum,
        "objective_upper_bound": optimum,
        "exact_boundary": "SAT",
        "strictly_better": "UNSAT",
    }


def format_percentage(numerator, denominator, places=4):
    if (
        any(type(value) is not int for value in (numerator, denominator, places))
        or numerator < 0 or denominator <= 0 or places < 0
    ):
        raise ValueError("Invalid percentage fraction or precision")
    scale = 10 ** places
    rounded, remainder = divmod(numerator * 100 * scale, denominator)
    rounded += 2 * remainder >= denominator
    return f"{rounded // scale}.{rounded % scale:0{places}d}" if places else str(rounded)


def compare_share(numerator, denominator, target_numerator, target_denominator):
    if (
        any(type(value) is not int for value in (
            numerator, denominator, target_numerator, target_denominator,
        ))
        or numerator < 0 or target_numerator < 0 or denominator <= 0 or target_denominator <= 0
    ):
        raise ValueError("Invalid nonnegative population fraction")
    difference = numerator * target_denominator - target_numerator * denominator
    return "below" if difference < 0 else "above" if difference > 0 else "equal"


def build_results(data, source_validation=None, timeout_ms=60_000):
    validate_populations(data)
    results = {
        "schema_version": 1,
        "scope": {
            "state_universe": "48 states admitted by 1947, fixed for both census years",
            "objective": "sum of residents in selected states, not support or voters",
            "excluded_from_denominator": [*EXCLUDED, "Puerto Rico", "other territories"],
            "1910_caveat": (
                "Arizona and New Mexico were territories in 1910, admitted in 1912; "
                "this uses their 1910 counts in the later 48-state universe, not a "
                "1910 constitutional threshold or verified inputs of 1920 counsel."
            ),
            "cardinality": "exactly k; all weights positive",
            "percentage_rounding": "nearest 0.0001 percentage point, half up, integer arithmetic",
        },
        "source": SOURCE,
        "validation": {
            "csv_sha256": CSV_SHA256,
            "expected_unique_states": 48,
            "published_total_checks": {},
            "source_files": source_validation or {
                kind: {"status": "NOT_RUN", "reason": f"Supply --source-{kind} for binary audit"}
                for kind in ("xlsx", "pdf")
            },
        },
        "runtime": {
            "python": platform.python_version(), "z3": z3.get_version_string(),
            "solver_timeout_ms_per_check": timeout_ms,
            "optimizer_elim_01": False,
            "boundary_solver": "Tactic('smt').solver()",
        },
        "threshold_controls": {},
        "census_years": {},
        "two_amendments": {
            "assumption": "exactly 36 ratifying states per amendment; fixed universe of 48",
            "state_amendment_actions": 72,
            "minimum_distinct_states": 36,
            "maximum_distinct_states": 48,
            "minimum_intersection_states": 24,
            "maximum_intersection_states": 36,
            "no_claim_of_legal_validity_or_political_support": True,
        },
    }
    for name, numerator, denominator in (("ratification", 3, 4), ("convention_applications", 2, 3)):
        required = (48 * numerator + denominator - 1) // denominator
        results["threshold_controls"][name] = {
            "required_states": required,
            "exact_equality_passes": denominator * required == numerator * 48,
            "one_fewer_fails": denominator * (required - 1) < numerator * 48,
        }
    for year, populations in data.items():
        denominator = sum(populations.values())
        references = REFERENCE_ROWS[year]
        results["validation"]["published_total_checks"][str(year)] = {
            "source_50_states_plus_dc": references["United States"],
            "subtract": {area: references[area] for area in EXCLUDED},
            "derived_48_states": EXPECTED_TOTALS[year],
            "observed_48_states": denominator,
            "48_states_plus_dc": denominator + references["District of Columbia"],
        }
        year_result = {"denominator_48_state_residents": denominator, "bounds": {}}
        for cardinality in (36, 32):
            bounds = {}
            for direction in ("minimum", "maximum"):
                maximize = direction == "maximum"
                ordered = sorted_bound(populations, cardinality, maximize=maximize)
                solved = z3_bound(populations, cardinality, maximize=maximize, timeout_ms=timeout_ms)
                if solved["status"] != "OPTIMAL":
                    raise RuntimeError(f"{year}/{cardinality}/{direction}: {solved}")
                if ordered["population_total"] != solved["population_total"]:
                    raise RuntimeError("Sorting and independent Z3 optimization disagree")
                total = ordered["population_total"]
                bounds[direction] = {
                    "fraction": {"numerator": total, "denominator": denominator},
                    "percentage": format_percentage(total, denominator),
                    "sorted_witness": ordered["selected_states"],
                    "unique_optimum": ordered["unique_optimum"],
                    "z3": solved,
                    "algorithms_agree": True,
                    "witness_sets_agree": set(ordered["selected_states"]) == set(solved["selected_states"]),
                    "share_vs_45_percent": compare_share(total, denominator, 45, 100),
                    "share_vs_50_percent": compare_share(total, denominator, 1, 2),
                }
            year_result["bounds"][str(cardinality)] = bounds
        results["census_years"][str(year)] = year_result
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-xlsx", type=Path, help="Audit the pinned official workbook")
    parser.add_argument("--source-pdf", type=Path, help="Audit the official PDF using pdftotext")
    parser.add_argument("--extract-csv", type=Path, help="Extract a CSV from --source-xlsx, then exit")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of standard output")
    parser.add_argument("--timeout-ms", type=int, default=60_000)
    args = parser.parse_args()
    try:
        if args.extract_csv:
            if not args.source_xlsx:
                parser.error("--extract-csv requires --source-xlsx")
            raw = population_csv(read_source_xlsx(args.source_xlsx)).encode("utf-8")
            if sha256(raw).hexdigest() != CSV_SHA256:
                raise ValueError("Source extraction differs from the pinned canonical CSV")
            args.extract_csv.write_bytes(raw)
            return
        data = load_populations()
        validation = {}
        for kind, path in (("xlsx", args.source_xlsx), ("pdf", args.source_pdf)):
            validation[kind] = verify_source(path, kind, data) if path else {
                "status": "NOT_RUN", "reason": f"Supply --source-{kind} for binary audit",
            }
        results = build_results(data, validation, args.timeout_ms)
        output = json.dumps(results, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output, end="")
    except (ValueError, OSError, BadZipFile, ElementTree.ParseError, subprocess.CalledProcessError, RuntimeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
