# Compare coalition costs under the same attendance assumptions

**Result:** the earlier 267-versus-179 argument does not establish strict
coalition-cost domination of the quorum cascade. It compares self-supplied
quorum for exclusion with favorable attendance for direct amendment proposal.
The underlying scalar inequality remains true. Correcting its interpretation
does **not** establish a lawful cascade or a constitutional loophole.

## The consistent comparison

Assume all 435 House seats and 96 Senate seats are chosen and sworn. These are
the nominal 1947 chamber sizes, not a reconstruction of attendance at any actual
vote. Every present member votes yes or no; abstentions and vice-presidential
tie-breaking are outside the calculation.

| Attendance convention, applied to both actions | Majority exclusion: House + Senate | Direct Article V proposal: House + Senate | Expulsion under the same two-thirds rule |
|---|---:|---:|---:|
| Full membership present | 218 + 49 = **267** | 290 + 64 = **354** | **354** |
| Favorable minimum quorum present | 110 + 25 = **135** | 146 + 33 = **179** | **179** |
| Supporters alone supply quorum | 218 + 49 = **267** | 218 + 49 = **267** | **267** |

These are **initial voting thresholds**, conditional on the stated attendance
and voting rules. The majority-exclusion column does not establish authority to
exclude constitutionally qualified members. That authority is contested in the
pre-1947 record discussed in [quorum-cascade-null.md](quorum-cascade-null.md).

Under self-supplied quorum, the same number of supporters can propose directly
or begin a majority exclusion: there is no initial numerical saving. Under the
two other conventions, an initial majority vote costs fewer yes votes than a
two-thirds vote. Neither observation validates subsequent removals, supplies
attendance throughout a sequence, or secures ratification.

## The model and its independent check

For chamber membership \(n\), attendance \(p\), and yes votes \(y\):

```text
quorum:       2p > n
vote domain:  0 <= y <= p <= n
majority:     2y > p
two thirds:   3y >= 2p
```

Full attendance fixes `p = n`. Favorable minimum-quorum attendance also requires
`2(p - 1) <= n`. Self-supplied quorum requires `y = p`: no opponent is needed
to keep the chamber quorate.

[attendance_audit.py](search/attendance_audit.py) reuses the closed-form voting
helpers from the state-admission replication. Its independent Z3 model receives
the attendance and ballot constraints above, not the helper's answer. All
**12** optimizations (three conventions, two chambers, two vote rules) attain
the closed-form minimum; a separate solver query excludes every smaller
coalition. Any UNKNOWN stops artifact generation.

Eight general counterexample searches return **UNSAT**, including the
self-quorate lower bound and feasibility of an all-supporter quorum for either
vote rule. Two deliberately overbroad assertions have **SAT** counterexamples:
the old strict scalar inequality fails at chamber size one, and a bare majority
is not strictly cheaper than two thirds when six members vote. The latter
corrects the old `q >= 5` statement in `election_leverage.py`; `q >= 7` suffices.

The **11 attendance tests** include exhaustive ballot/attendance enumeration
for chamber sizes 1 through 24, exact and one-short boundaries, very large
integer inputs, UNKNOWN handling, and fresh artifact comparison. A real
failure control copies the executable and artifact to an isolated temporary
directory: the unmodified `--check` exits **0**; replacing the self-quorate
proposal total of 267 with the favorable-attendance total of 179 makes it exit
**1**. An import failure would fail the unmodified control, not count as a
detected research defect.

## What remains true about the earlier calculation

For \(q=\lfloor n/2\rfloor+1\):

\[
n \geq 4 \quad\Longrightarrow\quad \lceil 2q/3\rceil < q.
\]

[cascade_domination.py](search/cascade_domination.py) still verifies that
statement with Z3 and checks every chamber size from 1 through 200,000. Its
only exceptions are 1, 2, and 3. The error was interpreting the two sides as
coalition prices under the same attendance assumptions, not an error in this
inequality.

The script preserves its old numerical fields for traceability and labels
their attendance mismatch explicitly. Its `extra_cost = 88` is a legacy
mixed-assumption difference, **not** a measured extra cost under one scenario.
The corrected matrix is in
[attendance_audit_results.json](search/attendance_audit_results.json).

## Legal and historical limits

The 1920 holding in *National Prohibition Cases*, 253 U.S. 350, uses two thirds
of the members **present**, assuming a quorum; it does not require attendance
to equal the minimum quorum. The primary quotation and its source are in
[threshold-arithmetic.md](threshold-arithmetic.md). The smaller 146/33 result
is therefore conditional, not the threshold at every possible 1947 vote.

Quorum membership, authority to exclude, voting rules, attendance, continued
vacancies, agenda control, and eventual state ratification are different
questions. This experiment isolates only the initial voting calculation.
The actual 1947 standing-rule texts remain incompletely verified. No claim is
made that opponents would provide a quorum or that a chamber could prevent
states from refilling seats.

Nothing here changes the fixed-universe requirement of ratification in **36 of
48 states**, by legislatures or conventions as Congress directs. The separate
[state-admission experiment](state-admission-replication.md) examines changing
that universe; it is not part of this cascade calculation.

## Reproduce

From the repository root:

```sh
.venv/bin/python -B -m unittest discover \
  -s analysis/united-states-1947/search -p 'test_attendance_audit.py' -v
.venv/bin/python -B analysis/united-states-1947/search/attendance_audit.py --check
.venv/bin/python -B analysis/united-states-1947/search/cascade_domination.py
```

Use `--write` on `attendance_audit.py` only to deliberately regenerate the
artifact. `verify.sh` sections 2e and 2f now distinguish the scalar theorem from
the corrected attendance comparison; no deployment workflow was changed.
