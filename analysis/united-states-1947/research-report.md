# Research report: the search for Gödel's constitutional loophole

**Research date: September 8, 2026. Constitutional vantage: December 5, 1947.**

**No verified constitutional loophole, complete lawful-collapse path, or
identification of Gödel's actual argument has been established.** The work does
establish reproducible conditional results, corrects important overclaims in
the existing analysis, and identifies which unresolved premises actually change
the answer. Logical and quantitative methods were both implemented.

This report consolidates the completed work. A separate replication of an
AAMAS self-amendment protocol and a corrected literature map are still in
progress; neither is included in the completed-result counts below.

The repository's [finding standard](../../method/what-counts-as-a-finding.md)
requires authorized operations, an explicit legal status for each step, a
coalition, and a concrete falsifier. A route that merely uses the ordinary
amending coalition does not meet its loophole criterion. This matters when
interpreting the one- and two-amendment witnesses below.

## What was established

| Investigation | Completed result | What it does not establish |
|---|---|---|
| Published Isabelle reconstruction | The original `minimal` and `noamd1` experiments reproduce in consistent theories. The three target theorems and five intermediate lemmas survive deletion of the original step-one axioms. | That an actual constitution can be changed without an authorized first step. |
| Separate repaired-model audit | 16 new kernel lemmas and seven new ordinary Nitpick counterexamples distinguish entailment dependency from causal necessity and expose a contradictory rival-test hypothesis. | That the repaired model describes event-complete lawful histories. |
| Framed Article V search | 48 configurations, 144 target queries: 54 reachable and 90 unreachable in their declared finite graphs. All 144 agree with a separate bounded SMT encoding. | A probability of legal validity, an exhaustive search of constitutional law, or historical attribution. |
| State-admission arithmetic | The changing-denominator formula and joint congressional gates reproduce conditionally. The Note's precise historical minimum of 96 remains underdetermined. | That new states can be manufactured on the assumed terms or will support the later amendment. |
| Census-weighted state thresholds | The smallest 36-state group contains 54,982,723 of 131,006,184 residents in the 1940, 48-state universe: 41.9696%. | A minimum number or percentage of voters, supporters, legislators, or delegates. |
| Attendance audit | Under consistent assumptions, initial majority/proposal totals are 267/354, 135/179, or 267/267. The old 267-versus-179 strict cost refutation mixed assumptions. | That exclusion is lawful, that later attendance is controllable, or that a complete cascade succeeds. |
| Historical control | The Sixteenth Amendment's primary certification corroborates a changing state denominator and a 36-state threshold. It acknowledges 38 ratifications overall. | A successful backtest of engineered state creation or wholly lawful constitutional collapse. |

The computational results are not seven independent confirmations of one
conclusion. They answer different questions, sometimes share specification
data, and include corrections and negative results.

## 1. What transferred from the Navier-Stokes work

The supplied 166-page paper was read in full, including its technical sections
and appendices. It matches the official OpenAI PDF. The paper claims the
**forced breakdown alternatives C and D** in the Clay problem statement;
forcing alone is not grounds for dismissing those alternatives. This review
did not independently check every estimate, build the Lean project, execute
Comparator, or verify a prize decision.

The official proof interfaces were inspected at a pinned commit. Their
separation of reference statements, proof adapters, and permitted axioms is a
useful verification design, not evidence that those checks were run here.
No specific producing-model attribution to GPT-6 Astra was independently
confirmed from the accessible primary material. That retrieval gap does not
establish that Astra has produced no mathematical results.

The useful methodological transfer was concrete:

1. Fix the contract and quantifiers before searching.
2. Preserve invariants by construction, rather than hoping a solver supplies
   them.
3. Recompute consequences from the updated state.
4. Keep assumptions consistent across a comparison.
5. Separate a deduction from its assumptions, a model's legal correspondence,
   and an empirical or historical claim.

The PDE argument uses an infinite construction and a limiting argument.
The constitutional search is a finite transition system. It is not a
replication of the PDE proof technique in a different vocabulary.

Details and primary links: [Scientific methods review](ai-science-methods.md).

## 2. Logical results: a proof is not yet a lawful path

The published reconstruction genuinely represents and ratifies a first
amendment, yet its published targets remain provable when the step-one axioms
are removed. Reproducing that fact diagnoses the instrument; it does not show
that actual repeal is legally unnecessary.

The separate repaired model makes a five-fact step-one package load-bearing
for entailment. The new audit shows why that still falls short of causal
necessity. It permits the proviso to disappear without the scheduled repeal,
and permits presidential concentration of all three powers even with the
proviso always on and no amendments ratified. It also permits non-dictatorship
under those latter restrictions. Missing persistence constraints leave both
outcomes open.

The rival-rule experiment has a further problem: its imported theory already
entails that the proviso is off at the relevant time. Adding the contrary
clause-on hypothesis alone creates a contradiction, before the rival rule is
used. The abstract necessary-versus-sufficient-condition argument remains
sound; its particular ambient test does not uniquely justify a legal encoding.

The new transition model addresses those omissions directly. Proposals and
withdrawals preserve the constitution. A ratification must match a pending
proposal, meet the current rule, and change only its declared fields. Consent
and ratification are distinct sets of identified states.

At 36 supporting ratifiers and consenters, with no modeled implicit democracy
floor, the concentration-of-powers target has this sensitivity:

| Reading of Senate suffrage | Proviso ordinarily repealable | Repeal requires every state's consent |
|---|---|---|
| Formal equality of state votes | One ratification; repeal unnecessary | One ratification; untouched proviso does not block the target |
| Functional protection of the Senate's legislative role | Two ratifications; repeal then concentration | Unreachable in the declared graph with this support set |

Consent from every affected state supplies a separate positive control. An
implicit democracy floor changes the result again. Removal of executive
elections is a different target from concentration of all three powers.

Breadth-first search saturates each finite graph. The independent SMT check
only searches up to four operations; it does not supply the graph's
all-path-length conclusion. Neither implementation decides which interpretation
was legally correct in 1947. Both use the same declared amendment-effect
catalogue, which contains hypothetical effects rather than legally verified
amendment drafts.

Details: [Original instrument finding](inert-manoeuvre.md),
[causality audit](repair-causality-audit.md), and
[framed search](bounded-article-v-search.md).

## 3. Quantitative results: keep the units and denominators straight

### State membership can change

The Harvard Law Review Note *Pack the Union* explicitly studies the interaction
between admission and amendment. With `N` original states, `r` original
ratifiers, and `k` additional states, **all assumed to ratify**:

```text
4(r + k) >= 3(N + k)
minimum k = max(0, 3N - 4r).
```

For the 48-state baseline, 35 original ratifiers need four new supportive
states, not one. One original ratifier needs 140. These are ratification-only
bounds: the congressional proposing stage and the original authorization of
admission cannot be omitted.

Under the stated one-new-House-seat convention, joint hypothetical 1947
scenarios require 216 additional states with full attendance and initial
House/Senate support of 218/49, or 140 with favorable minimum-quorum attendance
and support of 110/25. Both examples assume one original ratifier and a
cooperative President. The latter bloc cannot bootstrap admission if it must
supply its own quorum or overcome presidential opposition.

The Note's printed 96 can be matched by one explicit parameter choice; a
one-member change in assumed House support changes the joint minimum to 99.
Its exact historical roster date, attendance, and supporting-state inputs were
not recovered. Matching a chosen example is not exact historical replication.

Most importantly, adding supportive states does not manufacture consent from
a dissenting original state whose Senate suffrage is protected. Nor does
Congress's admission power by itself establish control of a new state's later
ratification. Failure to guarantee that support is not a refutation of an
existential path with cooperative states; it identifies an additional premise.

Details: [State-admission replication](state-admission-replication.md).

### State populations are not ratification votes

The Census calculation uses all 96 state-year cells for 1940 and 1910, checked
against both official source formats. Alaska, Hawaii, DC, and territories are
excluded from the 48-state optimization and its denominator.

For 1940, the minimum populations of exactly 36 and exactly 32 states are:

| State-count threshold | Residents of the selected states | Share of 48-state residents |
|---|---:|---:|
| 36 ratifying states | 54,982,723 | 41.9696% |
| 32 convention-application states | 42,959,945 | 32.7923% |

Sorting and separately formulated integer optimization agree; exact-total
queries are SAT and strictly-better queries UNSAT. These are resident totals,
not support measurements or December 1947 population estimates. A convention-
application threshold does not specify how the convention itself votes.

Two amendments can reuse the same 36 states. Seventy-two state-amendment
ratification actions do not mean 72 distinct states or twice as many people.

Details: [Census bounds](quantitative-ratification.md).

### Attendance must be held consistent

For nominal filled chambers of 435 and 96, assuming every present member votes
and excluding vice-presidential tie-breaking:

| Attendance convention | Initial majority vote, House + Senate | Article V proposal, House + Senate |
|---|---:|---:|
| Full membership present | 218 + 49 = 267 | 290 + 64 = 354 |
| Favorable minimum quorum | 110 + 25 = 135 | 146 + 33 = 179 |
| Supporters supply the quorum | 218 + 49 = 267 | 218 + 49 = 267 |

The older scalar inequality remains true, but comparing its 267 entry cost
with 179 for direct proposal mixed the last and middle rows. The resulting
strict coalition-cost refutation was withdrawn. That correction does not
validate the cascade: authority to exclude members, later attendance, seat
refilling, and state ratification remain separate issues.

Details: [Attendance audit](attendance-consistency.md).

## 4. What a hybrid search can and cannot decide

The useful hybrid is an authorized transition model with integer coalition
constraints, not a population percentage attached to an unframed endpoint.
The experiments show three boundaries that a larger implementation must retain:

1. **Current-law authorization:** a proposed lower threshold cannot authorize
   itself; future members cannot authorize their own initial admission.
2. **Changing membership:** after admission, recompute both numerator and
   denominator, congressional representation, and the affected-state set.
3. **Distinct legal guards:** a ratification supermajority is not consent from
   a particular affected state, and neither resolves the amendment's
   substantive validity.

The fixed-state search and changing-membership arithmetic have been composed
for declared scenarios, not expanded into an exhaustive event model of all
admission, state-formation, seating, election, and amendment procedures.
Their conditional witnesses are candidate mechanisms already represented in
scholarship, not newly established constitutional vulnerabilities.

More search inside the same interpretation cannot settle the disagreement
between formal and functional suffrage, or whether the proviso protects itself.
Those are inputs to the current experiments. A useful next extension must
either obtain evidence that discriminates between them or encode a genuinely
new authorized operation with a falsifiable correspondence claim.

## 5. Historical testing and attribution

The Sixteenth Amendment provides a limited positive historical control:
membership changed from 46 to 48 states, so the quota changed from 35 to 36.
The February 25, 1913 certification names a principal 36-state list and
acknowledges two additional ratifications, for 38 in total. The one-short
negative example is synthetic, not a reconstructed historical daily vote count.

The repository's comparative collapses do not supply a clean, fully verified
positive backtest of wholly lawful collapse.
[Germany's](../germany-1933/path-enabling-act.md) constitutional-
amendment procedure cannot be erased from the account, but coercion and
contested adoption prevent treating it as an uncomplicated legal witness.
The [Austrian account](../austria-1920/path-kweg-bridge.md) has an incompletely
verified transitional-law bridge and unlawful prevention of reconvening.
The scoped [Italian corpus](../italy-1848/null-result-formal-route.md) lacks
relevant operative statutes. These cases help test representations; they do not
justify a measured success rate for the proposed search.

[Morgenstern's account](../../academia/naturalization-1947.md) records Gödel's
reported belief. It does not supply the missing argument or independently prove
that a defect existed. An executable modern reconstruction could establish a
conditional possibility without identifying what Gödel privately meant.

The exact 1947 congressional standing-rule texts remain incompletely verified.
Catalog records are leads, not operative rule pages. This blocks stronger
claims about assured passage, procedural obstruction, or an Austrian-style
reconvening mechanism in the target system.

## 6. Reproduction and evidence boundaries

The completed Python modules have 76 targeted unit tests. The Article V checks
also plant four actual behavioral defects in disposable copies. The attendance
checker has a separate planted-artifact control: the clean copy exits zero,
and replacing the self-quorate proposal total with 179 exits one. An import
failure is not counted as successful defect detection.

From the repository root:

```sh
(
  cd analysis/united-states-1947/search &&
  ../../../.venv/bin/python -B -m unittest \
    test_article_v test_state_admission test_state_population test_attendance_audit &&
  ../../../.venv/bin/python -B article_v_search.py --check &&
  ../../../.venv/bin/python -B state_admission.py --check &&
  ../../../.venv/bin/python -B attendance_audit.py --check &&
  ../../../.venv/bin/python -B -m article_v_mutations
)
```

The Census report supplies separate commands to re-download the pinned primary
files and audit the extraction. Its offline calculation explicitly labels
unperformed binary-source audits `NOT_RUN`. The Isabelle audit supplies its
actual independent process commands and distinguishes kernel lemmas from
model-finder diagnostics. A successful theory build alone does not certify a
Nitpick probe's result.

SAT means a witness to the stated constraints, not legality. UNSAT excludes
the stated search domain, not every constitutional path. UNKNOWN is not
converted into impossibility or an optimum. Source hashes and deterministic
artifacts permit reruns, but do not make source interpretation infallible.

The complete legacy repository verifier and the OpenAI Lean project were not
run locally in this program. The completed checks do not cover the whole statute book,
every historical rule, or every conceivable route to constitutional collapse.

## Bottom line

The best-supported progress is a more trustworthy research instrument: explicit
transitions, identified consenters, changing-denominator arithmetic, verified
population inputs, nonvacuity checks, and comparisons under matched assumptions.
It also withdraws claims that the evidence did not support.

The unresolved problem is no longer merely how to search faster. It is how to
establish the legal premises and historical correspondence needed to turn a
conditional witness into a defensible finding. No number of additional agents
or repeated runs of the same finite graph can substitute for those premises.
