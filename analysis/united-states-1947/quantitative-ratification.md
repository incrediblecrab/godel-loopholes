# State ratification thresholds weighted by census residents

## Result and scope

Using **1940 census resident counts for the 48 states in 1947**, the smallest
population total in a group of exactly 36 states is **54,982,723 / 131,006,184 =
41.9696%**. The corresponding minimum for exactly 32 states is **42,959,945 /
131,006,184 = 32.7923%**.

These are extrema of **residents in selected states**, not estimates of voter
support, numbers of legislators or convention delegates, political feasibility,
or a finding of a constitutional loophole. They answer the explicitly uncomputed
1940-census question in [threshold-arithmetic.md](threshold-arithmetic.md).
They do **not** answer the separate individual-participant question in
[ratification-price.md](ratification-price.md).

Article V's state-count thresholds are 36 for ratification, in whichever mode
Congress chooses, and 32 legislatures for convention applications. An application
threshold does not specify how a proposing convention would vote. The population
data are census counts from **1940**, not estimates of population on December 5,
1947.

## Primary source and denominator audit

The source is the U.S. Census Bureau's **“Change in Resident Population of the 50
States, the District of Columbia, and Puerto Rico: 1910 to 2020”**, released
April 26, 2021, on its
[Historical Population Change Data page](https://www.census.gov/data/tables/time-series/dec/popchange-data-text.html).
This is an official retrospective historical compilation, not a document
published in 1940 or a source of post-1947 constitutional doctrine.

Both downloadable versions were actually obtained and compared on
**September 9, 2026 (UTC)**:

| File | Location of the data | Bytes | SHA256 |
|---|---|---:|---|
| [Official XLSX](https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.xlsx) | Sheet `Population Change`; areas `S6:S56`; **1940 residents `T6:T56`**; **1910 residents `Z6:Z56`** | 24,339 | `053ac373f7f76b12bfa0d1f9f9ccb5a238f37c04b8b14bc3cc90208bea18732f` |
| [Official PDF](https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.pdf) | Page **3 of 3**, columns headed `1940 Census / Resident Population` and `1910 Census / Resident Population` | 157,673 | `3920c1a1a38c7fcb758182c392b335d57bde8c57f544c8adb281cc213ac390b1` |

The units are **persons**, not thousands, percentages, apportionment populations,
electors, or citizens. The adjacent `Percent Change` columns are not inputs.
The extracted [CSV](search/state-populations.csv) has 48 unique, explicitly
validated state names and two positive integer population columns. Its SHA256 is
`289c226281ca89c4daa4bb68db03cd3fd1937b2eacb22f75f598d6590f6190df`.
The raw XLSX and PDF remain in the session's `files/` area, outside the repository.

The national-total footnote on **PDF page 1**, also in **XLSX cell `A63`**, says
the table's United States row includes the resident population of **50 states
and DC**. That is a retrospective geographic series: Alaska and Hawaii were
not states in 1940 or 1947. The printed national totals are `T57` and `Z57`.
Puerto Rico appears separately at row 62 and is not in those national totals.

| Population geography | 1940 residents | 1910 residents |
|---|---:|---:|
| Source's retrospective 50 states + DC | 132,165,129 | 92,228,531 |
| Subtract Alaska | 72,524 | 64,356 |
| Subtract Hawaii | 423,330 | 191,909 |
| **48-state geography + DC** | **131,669,275** | **91,972,266** |
| Subtract DC | 663,091 | 331,069 |
| **48-state denominator used here** | **131,006,184** | **91,641,197** |

Thus the 1940 check is the independently printed aggregate identity
`132165129 - 72524 - 423330 - 663091 = 131006184`, not merely summing the
same CSV twice. The analogous 1910 identity also passes. Every geographic
row and both national totals matched between XLSX and PDF; the executable audit
checks all **96 state-year values** against each format, the national totals,
and the excluded reference rows. All territories, including Puerto Rico, are
excluded from the optimization and denominator.

## Exact 1940 bounds

All four fractions below use **131,006,184** as denominator.

| Exactly this many selected states | Extremum | Resident numerator | Share of residents in the 48 states |
|---|---|---:|---:|
| 36 — ratification threshold | Minimum | **54,982,723** | **41.9696%** |
| 36 — ratification threshold | Maximum | **125,577,321** | **95.8560%** |
| 32 — convention-application threshold | Minimum | **42,959,945** | **32.7923%** |
| 32 — convention-application threshold | Maximum | **121,803,769** | **92.9756%** |

“Exactly” is important. With strictly positive population weights, the minimum
over **at least** 36 states is also attained at exactly 36, but the maximum over
at least 36 is **all 48 states, or 100%**, not 95.8560%. The same distinction
applies to 32.

### State witnesses

The **minimum 32-state** witness, in ascending 1940 resident-population order, is:

> Nevada, Wyoming, Delaware, Vermont, New Hampshire, Arizona, Idaho, New Mexico,
> Utah, Montana, North Dakota, South Dakota, Rhode Island, Maine, Oregon,
> Colorado, Nebraska, Connecticut, Washington, Kansas, Maryland, Florida,
> South Carolina, West Virginia, Arkansas, Mississippi, Oklahoma, Louisiana,
> Iowa, Virginia, Minnesota, Alabama.

The **minimum 36-state** witness adds **Kentucky, Tennessee, Georgia, and
Wisconsin**, in that order. The largest included state is Wisconsin
(3,137,587), below the smallest excluded state, Indiana (3,427,796).

The **maximum 36-state** witness comprises every state except the first **12**
in the displayed list, Nevada through South Dakota. The **maximum 32-state**
witness additionally excludes Rhode Island, Maine, Oregon, and Colorado.
All four boundary gaps are strict, so these four optimal state sets are unique.

[state_population_results.json](search/state_population_results.json) records
every selected state explicitly, both the sorted witness and the independent Z3
witness, for every extremum in both census years.

## Method, exact boundaries, and solver controls

For each state \(i\), let \(p_i\) be its integer resident population and let
\(x_i\) be an integer with \(0 \leq x_i \leq 1\). The computation is

\[
\min\ \text{or}\ \max\ \sum_{i=1}^{48}p_i x_i
\quad\text{subject to}\quad \sum_{i=1}^{48}x_i=k,
\qquad k\in\{36,32\}.
\]

Two algorithms were genuinely run:

1. **Sorting.** Select the \(k\) smallest or largest populations. The exchange
   argument proves optimality: swapping an included larger population for an
   excluded smaller one cannot increase a minimum. Reverse the argument for a
   maximum. Alphabetical tie-breaking makes the sorted witness deterministic.
2. **Independent Z3 integer optimization.** Give Z3 only the populations, binary
   integer domains, exact cardinality, and linear objective. No sorted witness,
   population ordering, or proposed optimum is supplied to the optimizer.
   Require identical exact lower and upper objective bounds and a model attaining
   that integer. Separate SMT checks then require **SAT at exactly that total**
   and **UNSAT for any strictly better total**.

The final run used **Python 3.13.3 and Z3 5.1.0**, with a 60,000 ms timeout per
check, `Optimize(elim_01=False)` configured through `.set`, and
`Tactic("smt").solver()` for the boundary checks. This retains the 0–1 variables
in arithmetic rather than compiling the optimization into weighted SAT.
The initial default configuration returned **UNKNOWN** on the 1940
36-state maximum at its timeout; it produced no published bound. The final
arithmetic configuration completed all eight optimizations. UNKNOWN, including
an UNKNOWN boundary check or unclosed objective bounds, is never called an
optimum; report generation stops instead.

All **eight** sorted totals and Z3 optima agree. All exact-total checks were
**SAT** and all strictly-better checks **UNSAT**. Since residents are integers,
the latter checks exclude totals at least one person better; they do not
accidentally exclude equality.

The state thresholds also include equality: `4*36 = 3*48`, while 35 fails;
`3*32 = 2*48`, while 31 fails. Population shares are stored as exact integer
numerators and denominators. Displayed percentages are rounded **half up to four
decimal places**, using integer division and remainders, not floating point.
Comparisons with 45% or 50% use cross-multiplication. A displayed `50.0000%`
would not by itself establish an exact 50% boundary; a regression test covers
that case.

The **26 passing unittests** also cover the expected state set, duplicate and
missing rows, territories/DC, invalid values, independently printed totals,
balanced transcription errors that preserve the sum, source fingerprints,
exhaustive toy subsets with ties, infeasible cardinalities, zero/all/empty
selections, complement identities, UNKNOWN handling, and fresh computation
against the checked-in numerical results.

## Separate 1910 comparison, not a verified replication of counsel's inputs

The same authoritative table supplies 1910 counts, so no secondary population
series was spliced in. Keeping the **later 48-state geography** fixed gives:

| Exactly this many selected states | Extremum | Resident numerator / 91,641,197 | Percentage |
|---|---|---:|---:|
| 36 | Minimum | 40,865,581 / 91,641,197 | 44.5930% |
| 36 | Maximum | 87,698,188 / 91,641,197 | 95.6973% |
| 32 | Minimum | 31,810,758 / 91,641,197 | 34.7123% |
| 32 | Maximum | 84,946,545 / 91,641,197 | 92.6947% |

**Arizona and New Mexico were territories in 1910 and became states in 1912.**
Their 1910 resident counts, 204,354 and 327,301, are included because the
universe is the 48 states existing by 1920 and 1947. This is **not** a claim that
there were 48 ratifying states in 1910; an actual 1910 constitutional threshold
would need the then-existing 46-state universe instead.

The 1910 minimum is strictly below 45% using this denominator, consistent with
the possibility behind counsel's reported 1920 assertion. But **neither the
precise census input year nor counsel's intended nationwide denominator has been
verified**. Agreement with “less than forty-five per cent” does not establish
that the original calculation has been replicated. The narrower, independently
measured 1940 statement is also strictly below 45%.

## Two amendments: repeated actions, not 72 distinct states

If two distinct amendments each receive exactly 36 state ratifications in a
fixed 48-state universe, that is **72 state-amendment ratification actions**.
The same 36 states can be reused. The union can contain 36–48 states and the
intersection 24–36 states. Reusing a coalition does not double its residents.
This bookkeeping assumes neither amendment's legal validity, state willingness,
nor that ratification is equivalent to any separate state consent requirement.
It does not convert the population weights into a minimum coalition of people.

## Reproduce

From the repository root, using the existing environment and **without new
dependencies**:

```sh
.venv/bin/python -B -m unittest discover \
  -s analysis/united-states-1947/search -p 'test_state_population.py' -v
.venv/bin/python -B analysis/united-states-1947/search/state_population.py
```

The second command computes offline from the fingerprinted CSV and prints JSON.
It explicitly marks optional binary-source audits `NOT_RUN`; it does not
pretend that reading the CSV fetched or rechecked the remote files.

For full source-verified regeneration, download both pinned source formats to a
fresh temporary directory outside the checkout. `pdftotext`, already present for
this run, is needed only for the optional PDF comparison; XLSX extraction uses
Python's standard library.

```sh
set -euo pipefail
source_dir=$(mktemp -d "${TMPDIR:-/tmp}/godel-census.XXXXXX")
curl --fail --location --silent --show-error --max-time 90 \
  'https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.xlsx' \
  -o "$source_dir/census-population-change-data-table.xlsx"
curl --fail --location --silent --show-error --max-time 90 \
  'https://www2.census.gov/programs-surveys/decennial/2020/data/apportionment/population-change-data-table.pdf' \
  -o "$source_dir/census-population-change-data-table.pdf"

# Reconstruct the checked-in CSV from the pinned workbook, without hand transcription.
.venv/bin/python -B analysis/united-states-1947/search/state_population.py \
  --source-xlsx "$source_dir/census-population-change-data-table.xlsx" \
  --extract-csv analysis/united-states-1947/search/state-populations.csv

.venv/bin/python -B analysis/united-states-1947/search/state_population.py \
  --source-xlsx "$source_dir/census-population-change-data-table.xlsx" \
  --source-pdf "$source_dir/census-population-change-data-table.pdf" \
  --output analysis/united-states-1947/search/state_population_results.json

.venv/bin/python -B -m unittest discover \
  -s analysis/united-states-1947/search -p 'test_state_population.py' -v
```

The source-audited command, not the offline command, generated the checked-in
JSON. Both binaries' byte lengths and SHA256 values, table headings, source
totals, exclusions, and state-year values must pass before regeneration proceeds.
If Census changes a file, the audit fails closed rather than silently adopting
different data.

These checks establish a reproducible result **conditional on the Census series
and specified 48-state universe**. They do not certify the census enumeration's
accuracy, solve state-level voting rules, refine every aspect of `sup_rat`, or
show that an Article V route would be valid or achievable.
