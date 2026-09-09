# Replicating a published self-amending voting protocol

**Result:** AAMAS 2021 **Algorithm 1** and **Theorem 1** reproduce on the
explicit finite domains below. This is a new implementation of the published
procedure, not a newly invented amendment rule or an unbounded proof.
A counterexample to an **unnumbered sentence** does not falsify those results.

The parent independently retrieved the proceedings and v2 with matching hashes,
read both texts and the pivotal page images, and ran a separate expanded-voter
enumerator that imports none of the implementation under review. It matched all
per-electorate counts and endpoint histograms, all reported totals, and both
six-voter controls. This is additional verification, not another set of
independent observations to add to the profile count.

## Source verification and version control

The verified authors are **Ben Abramowitz, Ehud Shapiro, and Nimrod Talmon**.
The official [AAMAS proceedings index](https://www.ifaamas.org/Proceedings/aamas2021/forms/authors.htm)
links **“How to Amend a Constitution? Model, Axioms, and Supermajority Rules”**,
an extended abstract on **pp. 1443–1445**.
All three proceedings pages and twelve-page **arXiv v2**, including proofs, were
read. Proofs are inline, without a separate appendix. Proceedings p. 1444 and
v2 p. 7 were also checked as rendered page images, not only extracted text.

**The unversioned arXiv link is not a safe specification.**
[2011.03111v1](https://arxiv.org/abs/2011.03111v1) verifies the proposed
identifier and original title, but the latest version observed was **v4**, retitled
**“In the Beginning there were n Agents: Founding and Amending a Constitution.”**
Its Theorem 1 is a different, “Condorcet Amendment” result.
The original v1 also parameterizes thresholds as **1/2 + delta**, whereas
the proceedings and v2 use **delta**. Importing those formulas or theorem
numbers interchangeably would change the experiment.

| Downloaded source | Version / pages | SHA256 |
|---|---|---|
| [Official proceedings PDF](https://www.ifaamas.org/Proceedings/aamas2021/pdfs/p1443.pdf) | AAMAS 2021; 3 pages; **primary target** | `4ee8691ce53916b95349ab3b5fc457a32f670c9e27f6a863bd96ae40aee4bb70` |
| [Matching full preprint](https://arxiv.org/pdf/2011.03111v2) | v2, March 5, 2021; 12 pages; **proof reference** | `a25450ce60f3a5dd336757d890b484041ad1a071081937d70adaec251a96ac59` |
| [Original preprint](https://arxiv.org/pdf/2011.03111v1) | v1, November 5, 2020; 18 pages; version comparison | `9e45fcf00fc95cb46bafec0e0eb2985943b55790f7aa4ab549c05b7370cdef1e` |
| [Retitled latest preprint](https://arxiv.org/pdf/2011.03111v4) | v4, November 9, 2021; 14 pages; version comparison | `91021a0a2f0387d7d4828dd6d4ca9500b62ed9117fb88e9642d9c78fcf516b16` |

Revision dates follow arXiv's history, not PDF recompilation timestamps. Only
v1/v4 metadata, definitions and statement outlines were inspected for comparison;
they are **not** additional replication targets.
Downloads and extracted text remain outside the repository in the session's
`files/` directory. The JSON records byte lengths and all seven source-file
fingerprints, including the three verification webpages, retrieved September 9,
2026 UTC. Fingerprints identify the inspected sources, not a machine proof
that the source was interpreted correctly.

## The implemented protocol and its assumptions

There are **n fixed, equally weighted voters**, with preferences fixed throughout. Alternatives are only supermajority decision rules:
`A = {k/n : floor(n/2) <= k < n}`. The code stores **integer numerators k**.
With `s` voters strictly preferring proposal `p` to current rule `r`,
the paper's `R_delta` selects the proposal exactly when `s > delta*n`;
otherwise it retains `r`. Thus an integer rule `k` requires **k + 1** votes.

This preserves four consequential boundaries:

- Vote-count **equality rejects**; there is no floating-point comparison.
- The highest admissible threshold is `(n-1)/n`, which permits unanimous change;
  the impossible-to-satisfy strict threshold `1` is not an alternative.
- For odd n, `floor(n/2)/n` is the canonical rule equivalent to the paper's
  `1/2` majority label. This is equivalence of vote rules, not of distances.
- The index `h` has a **different, weak** inequality:
  `h = max {k in A_numerators : count(bliss >= k) >= k}`.

**Algorithm 1, proceedings p. 1444**, initializes the majority rule, considers
every proposal in **strictly increasing order** (footnote 4), and updates by
`r <- R_r(r,p)`. Each successful vote changes the rule used for the next vote.
The implementation does not substitute the proposed threshold, freeze the
initial threshold, skip rejected proposals, or initialize at an arbitrary rule.
The first proposal can coincide with the current rule; this is a harmless
no-op with zero strict supporters.

Voters' unique bliss points lie in A. Preferences strictly improve toward the
peak on either side of the natural ordering. **Bliss points alone do not
determine comparisons across the peak.** The primary replication therefore
enumerates every **strict complete single-peaked ranking**, not a conveniently
chosen Euclidean completion. An explicitly identified robustness extension also
enumerates all complete weak-order completions with a unique peak, strict
decline on each side, and possible **cross-side indifference**. Indifference
contributes no strict support in either direction. Incomplete or intransitive
relations outside these complete-ranking domains are not checked.

Self-stability at `r` means no admissible proposal wins under **R_r**.
Other-stability means none wins under **R_p**, the proposed rule.
These are different predicates, not two jointly required approval gates.
Under Definition 2, a voter does not complain if they strictly prefer the
winner, **or** applying their own bliss-point rule would produce that winner.
Complaint-freeness is checked **after each vote**; it is not imposed as a filter
to make the experiment succeed. There is no additional unanimity or legal
state-consent requirement in this algorithm.

## Precisely which published claims are checked

**Proceedings Theorem 1, p. 1444:** for a fixed electorate and a
single-peaked profile, no admissible `r < h` is self-stable, and every
admissible `r` in `[h,m]` is both self-stable and other-stable, where `m`
is a median bliss point. These are universal claims over the relevant rules
and all opposing proposals, not merely claims about the selected endpoint.
The corresponding full-version arguments are **v2 Lemmas 4–6, pp. 4–5**.
For even n, the code tests the interval through the upper median; it includes
the intervals ending at either median bliss point.

The same proceedings page states that **Algorithm 1 elects h and is
complaint-free**. Its initialization is the minimum-rule special case of
**v2 Constitution 1**; the relevant complaint-freeness result is
**v2 Theorem 3, pp. 6–7**. V2's own **Theorem 1** instead concerns stabilization
from arbitrary initial rules. The present run does **not** silently substitute
that different protocol or claim.

The strongest computed statement is: for each **n = 2,...,8**, every enumerated
complete-ranking profile satisfies the selected theorem at **every** candidate
rule; Algorithm 1 reaches h, that endpoint has both stability properties, and
every voter satisfies the complaint criterion at **every** vote.
This is not a proof for arbitrary n. Strategyproofness, social-cost distortion,
the v4 axiomatization, and arbitrary initial constitutions are not replicated.

## Measured exhaustive and independent solver results

| n | Weak-completion ranking types | Anonymous profiles, including strict | Strict-profile subset |
|---:|---:|---:|---:|
| 2 | 1 | 1 | 1 |
| 3 | 2 | 4 | 4 |
| 4 | 2 | 5 | 5 |
| 5 | 5 | 126 | 56 |
| 6 | 5 | 210 | 84 |
| 7 | 12 | 31,824 | 3,432 |
| 8 | 12 | 75,582 | 6,435 |
| **Total** | | **107,752** | **10,017** |

Anonymity permits grouping identical voters without changing any vote or
complaint test. Integer count vectors sum to the fixed n; coverage is checked
against `C(n+t-1,n)`, with multinomial multiplicities summing to `t**n`.
The run thus represents **465,832,279 labeled profiles**, including
**18,879,513 strict profiles**. These are combinatorial coverage counts, not
empirical populations, samples, independent observations, or political support.

There were **430,651 candidate-rule checks** and **430,651 protocol vote steps**.
All five recorded failure categories have **zero counterexamples**.
**24,027 nontrivial votes** had support exactly equal to the current integer
threshold and correctly rejected the proposal.

The separate Z3 implementation uses integer multiplicities of ranking types,
the largest weak-h condition, and an unrolled transition relation. It does not
call the Python voting, h, or complaint functions, or assume the desired endpoint.
For each n it found a valid profile/trace (**7 SAT checks**), then found **no**
counterexample to Theorem 1 or to the algorithm's endpoint/path properties
(**14 UNSAT searches**). Four mutated/domain-relaxed witnesses and two
revolution examples were additionally verified **SAT**: **27 solver queries**
in the canonical run altogether.

The environment was **Python 3.13.3 / Z3 5.1.0**, using
`Tactic("smt").solver()` with a 60,000 ms per-query timeout. No actual query
returned UNKNOWN. Injected-UNKNOWN tests verify that it is reported explicitly,
never treated as SAT/UNSAT, and cannot overwrite the artifact. No optimization
routine or approximate optimum is used.

## Falsification and boundary controls

All witnesses, full rankings, vote traces and solver results are in
[self_amendment_results.json](search/self_amendment_results.json).
Every emitted `profile.groups` entry preserves its original preference-type
`id`. A `complaining_groups` list refers to those IDs, **not positions in the
compacted groups array**; zero-count types are not emitted. Complaint counts
can therefore be reconstructed from the identified groups' counts and rankings.

The search stops at the first counterexample for each control within n <= 6:

| Deliberate change | First n | Consequence; integer rule labels |
|---|---:|---|
| Replace `s > current_k` by `s >= current_k` | 3 | Elects 2 instead of h = 1; complaints occur |
| Use proposed threshold instead of current threshold | 3 | Remains at 1 instead of h = 2; not self-stable |
| Reverse the published agenda | 5 | Elects 4 instead of h = 3 |
| Drop single-peakedness, keeping complete strict rankings | 5 | Reaches h = 4, **but an intermediate vote causes a complaint** |

These are mutations of the canonical integer implementation or a removed
hypothesis, **not counterexamples to the theorem under its assumptions**.
Even-n tests separately check literal 50% equality and current/proposed gates.
An additional h-boundary control has n = 4 and bliss numerators `[2,3,3,3]`:
the published weak condition gives h = 3; changing it to strict gives 2.
V2's **Figure 1** calibration reproduces **h = 7/11, m = 8/11** from its eleven
bliss points, without inventing the figure's unspecified pairwise preferences.

### A genuine source-level counterexample, narrowly identified

Proceedings p. 1444 contains the unnumbered sentence saying non-evolutionary
revolutions are **“never complaint-free.”** Under its own Definition 2:

- Let n = 6, current `r = 5/6`, and proposal `p = 1/2`.
- Five voters rank `1/2 > 2/3 > 5/6`.
- One voter ranks `2/3 > 5/6 > 1/2`.

Both rankings are strict and single-peaked. Five support the proposal.
The current rule rejects: **5 is not greater than 5**. The proposed rule
accepts: **5 > 3**. This is therefore a revolution that is not an evolution.
The five supporters prefer its outcome. The dissenter's own `2/3` rule would
also accept it, since **5 > 4**. Consequently **nobody complains**, in precisely
the paper's formal sense. Z3 confirms the fixed witness SAT.

The current rule in this example is **not self-stable**: all six voters prefer
2/3 to 5/6, so an evolution to 2/3 is available. The counterexample tests the
unqualified printed sentence, not a claim restricted to self-stable starting
rules.

This falsifies the **literal sentence**, not Theorem 1 or Algorithm 1.
V2 p. 7 instead says revolutions are **“never guaranteed to be complaint-free”**,
a weaker statement consistent with the example. Replacing the dissenter's
ranking with `5/6 > 2/3 > 1/2` gives one complaint, also verified SAT.
No authorial intent, formal erratum, or invalidity of the entire paper is inferred.

## Reproduce and audit

From the repository root; no new packages are required:

```sh
.venv/bin/python -B analysis/united-states-1947/search/self_amendment.py --check
.venv/bin/python -B -m unittest discover \
  -s analysis/united-states-1947/search -p 'test_self_amendment.py' -v
```

Use `--write` only to regenerate after a deliberate change, then inspect the
resulting diff. Rewriting the reference artifact before checking it is not
evidence that the old artifact was correct.

**29 unittests pass.** They include independent enumeration of all small
rank types, coverage identities, fixed-n validation, tied preferences, dynamic
threshold updates, equality/unanimity boundaries, concrete falsifiers, solver
UNKNOWN handling, source fingerprints, stale artifacts and fresh small runs.
`--check` compares the complete deterministic JSON byte-for-byte, including
runtime-version metadata; it never rewrites it. Source checks are optional
offline inputs, not a claim that ordinary runs re-fetch or re-interpret PDFs.

The final code review found that omitted zero-count groups had left complaint
references without identifiers in the serialized witnesses. Preserving group
IDs fixes the output contract without changing votes or totals. Two regression
tests first failed on the old shape; the corrected checks resolve every
published complaint reference and recompute complaints from the serialized
rankings.

An additional actual CLI failure control copied the unmodified driver and JSON
into a temporary directory. The clean `--check` exited **0**. Changing the
stored profile total from 107,752 to 107,753 made it exit **2** with
`Missing or stale self-amendment result artifact`. This was a real file
mutation and process exit, not a mocked result or an import failure; it is
separate from the 29 unit tests.

For a cache containing the seven filenames in JSON `source.files`, substitute
its actual location for the example path:

```sh
source_dir='/absolute/path/to/source-cache'
.venv/bin/python -B analysis/united-states-1947/search/self_amendment.py \
  --verify-sources "$source_dir" --check
```

The audit verified **all seven fingerprints**. For a fresh cache, download the
URLs in JSON `source.files` using their object keys as filenames. Keep PDFs and
extracted text outside the checkout. Webpage updates can invalidate historical
HTML hashes; do not silently substitute later versions. Version selection and
underdetermined cross-peak comparisons were handled explicitly, not presented
as successful replications of v4 or a Euclidean model.

## What this does—and does not—say about 1947

Article V is **multistage and bicameral**, with separate ratification by states
and a separate equal-suffrage consent proviso. It is not automatically one
electorate of 48 equal individual voters choosing a single decision threshold.
State preferences over thresholds, single-peakedness and their persistence are
not supplied by the constitutional text or measured here. Complaint-freeness is
not unanimous support and is not Article V consent.

Even an isolated numerical mapping needs care: Article V's inclusive **36 of
48** ratification gate is **not** this paper's strict `R_(3/4)`, which would
require 37. The equivalent strict-count parameter for that isolated gate is
**35/48**. This arithmetic is not an n = 48 preference-profile simulation.

Algorithm 1's initial majority is stipulated, not a legal authorization to
replace an existing amendment rule with majority rule. The explicit legal
stages in [bounded-article-v-search.md](bounded-article-v-search.md) are outside
this protocol; the changing membership in
[state-admission-replication.md](state-admission-replication.md) violates its
fixed-electorate assumption. The replication establishes neither legal authority,
political support, nor Gödel's undocumented argument.
