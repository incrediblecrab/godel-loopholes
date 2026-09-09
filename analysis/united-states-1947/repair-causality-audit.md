# Causality and rival-rule audit of the repaired Isabelle model

**Run:** September 8, 2026, Isabelle2025-2. **Scope:** logical entailment, missing causal constraints, and the rival-rule experiment—not legal validity or Gödel's historical reasoning.

## Findings

1. The repaired model really derives its dictatorship theorem after adding the five step-one facts. Their deletion really changes entailment. **This establishes an axiom-group dependency, not that repeal is necessary for dictatorship to occur.**
2. Stronger countermodels expose two distinct omissions: the entrenchment clause can switch off without the scheduled repeal event; and dictatorship, including the presidential concentration specified by `amd2`, can occur with the clause always on and **no amendments ratified at all**.
3. In the rival theorem's imported context, `in_force_omsp t2` **alone** entails `False`. Neither the rival rule nor an additional `comsp` hypothesis is needed for that contradiction.
4. The rival proof's abstract reasoning remains sound: a sufficient rule and a necessary constraint conflict when their forbidden trigger is present. That does **not** establish that the particular sufficient rule `pvr`, its syntax, or its legal interpretation is uniquely forced.

The two new theories add **no axioms**. The core audit imports only `GodelNetAddCore`; the second theory deliberately isolates the `Full`/`RivalRule` context. After an independent rerun reproduced all reported outcomes, `step-one-repair.md` and the misleading comments in the older theories were corrected. Their axioms, theorem statements, and proofs remain unchanged.

## 1. What the ablation does—and does not—establish

Let:

- `C` be the 39-axiom `GodelNetAddCore`;
- `S1` be the conjunction of the five additional step-one facts;
- `F2` mean `in_force_omsp t2`;
- `D3` mean `Dictatorship t3`.

`GodelNetAddNoStep1` [imports only Core and adds no axioms](isabelle/GodelNetAddNoStep1.thy). Deleting `S1` is not asserting that its events did not happen, still less supplying a persistence rule. In classical logic, unasserted facts need not be false.

### Kernel results in Core alone

The new [core-only audit](isabelle/GodelNetAddCausalityAudit.thy#L1) proves:

| Lemma | Result |
|---|---|
| `audit_amd2_proposed_iff_clause_off` | `is_prop amd2 t2 ↔ ¬F2` |
| `audit_amd2_ratified_iff_proposed` | `is_rat amd2 t3 ↔ is_prop amd2 t2` |
| `audit_clause_on_blocks_amd2` | `F2 → (¬is_prop amd2 t2 ∧ ¬is_rat amd2 t3)` |
| `audit_amd2_content_implies_dictatorship` | `amd2 t → Dictatorship t` |
| `audit_clause_off_entails_dictatorship` | `¬F2 → D3` |
| `audit_no_dictatorship_requires_clause_on` | `¬D3 → F2` |

These results use the existing step-two stipulations and rules. The ratification equivalence also uses the explicitly fixed, unique successor of `t2`. They are **not** unconditional legal claims or general proposal-validity equivalences for every amendment.

### Stronger Nitpick witnesses

Every probe below used `user_axioms, card time = 4, show_consts, timeout = 300`. All four returned exactly **`Nitpick found a counterexample`**, not a timeout, UNKNOWN, potential, or quasi-genuine result. These are bounded model-finder diagnostics, not kernel-certified model constructions.

| Probe, in addition to Core | Conjecture refuted | What its countermodel establishes |
|---|---|---|
| [`audit_no_repeal_event_does_not_supply_frame`](isabelle/GodelNetAddCausalityAudit.thy#L109): no repeal attempted at `t1`, no repeal ratified at `t2` | `F2` | `F2` is false anyway. By the kernel implication above, `D3` follows. |
| [`audit_clause_on_no_ratification_does_not_exclude_dictatorship`](isabelle/GodelNetAddCausalityAudit.thy#L121): clause on at every time; no ratification of any proposition at any time; no repeal attempt at `t1` | `¬D3` | Dictatorship is compatible with all those restrictions. The displayed dictator witness is **Congress**. |
| [`audit_clause_on_no_ratification_does_not_exclude_amd2_content`](isabelle/GodelNetAddCausalityAudit.thy#L128): the same restrictions | `¬amd2 t3` | The result is not merely an alternative-dictator artifact: **P has all three powers at `t3`**, although `amd2` is neither validly proposed at `t2` nor ratified at `t3`. |
| [`audit_clause_on_no_ratification_does_not_force_dictatorship`](isabelle/GodelNetAddCausalityAudit.thy#L135): the same restrictions | `D3` | Non-dictatorship is also compatible with those restrictions. |

The final raw log records the first result's clause assignment as `(t1=True, t2=False, t3=False, te=True)`. The next three have the clause true at all four times. The presidential witness assigns `is_leg P t3`, `is_exe P t3`, and `is_jud P t3` all `True`.

Together with the kernel implication, this gives the following exact classification of the two Boolean outcomes within the tested encoding:

| `F2` | `D3` | Evidence |
|---|---|---|
| False | True | Nitpick witness, even excluding the scheduled repeal event |
| True | True | Nitpick witness, even excluding every ratification |
| True | False | Nitpick witness under the same exclusions |
| False | False | Excluded by the kernel theorem `¬F2 → D3` |

Thus `F2` is **not fixed by Core**, but it is not wholly unconstrained in relation to other predicates. In particular, the report's observation that an operative clause blocks `amd2` is correct. Inferring that it therefore blocks `D3` is not.

### Why this is not a lawful-reachability result

The source has a successor relation on four times, but no event-complete state-transition/reachability definition:

- [`in_force_omsp_t1`](isabelle/GodelNetAddCore.thy#L247) fixes the initial clause status; it does not say the status persists absent a repeal.
- [`amd1a`](isabelle/GodelNetAddCore.thy#L210) is the proposition that the clause is off, not an event history.
- [`rv`](isabelle/GodelNetAddCore.thy#L177) says ratification implies content. It does not say content can become true only through ratification.
- The government propagation axioms [reach `t2` only](isabelle/GodelNetAddCore.thy#L223). They do not preserve offices into `t3` when no amendment changes them.

Consequently, the countermodels are admissible **assignments to the encoding**, not demonstrated lawful constitutional executions. Some assignments are plainly unsuitable as realistic histories: the non-dictatorship witness, for example, has no executive at `t3`. That does not invalidate its logical counterexample, but it further limits its constitutional interpretation.

The justified entailment statement is:

> `C + S1` entails `D3`; `C` alone entails neither `D3` nor its negation, as diagnosed by countermodels. Removing the five facts therefore removes an entailment guarantee. It does not make `D3` impossible, establish the necessity of every individual fact, or prove that every lawful route to `D3` must contain a repeal.

The new witnesses go beyond lack of a proof: they refute unrestricted claims that dictatorship in a Core model requires the scheduled repeal or even requires some ratification.

## 2. The rival theorem's ambient context

[`GodelNetAddRivalRule`](isabelle/GodelNetAddRivalRule.thy) imports `GodelNetAddFull`. The latter already proves [`in_force_omsp_false_t2`](isabelle/GodelNetAddFull.thy#L82). The rival theorem then assumes `in_force_omsp t2`.

The isolated [Full-context audit](isabelle/GodelNetAddCausalityAuditFull.thy#L10) kernel-proves:

```text
in_force_omsp t2 ⟹ False
in_force_omsp t2 ⟹ ψ
```

The proofs use only that local hypothesis and the inherited `in_force_omsp_false_t2`. They do **not** require `pvr_strong`, the extra `comsp_holds` hypothesis, or the other rival-theorem hypotheses.

This does not make Full inconsistent: the contradiction is in **Full plus the contrary clause-on hypothesis**. The imported Full diagnostics again found a model for `True` and a counterexample to `False`; the imported rival shape probe also found a model.

There is a useful positive control. [`audit_full_unguarded_rule_consistency`](isabelle/GodelNetAddCausalityAuditFull.thy#L25) assumes the entire globally quantified unguarded rule:

```text
∀φ t. attempted φ t ∧ is_amd φ t ∧
      (∀g. is_leg g t → sup_prop g φ t) → is_prop φ t
```

It does **not** assume `F2`. Nitpick returned **`Nitpick found a counterexample`** to `False`, with all Full axioms included and `F2=False`. Thus even adding this stronger rule to Full is satisfiable in the bounded diagnostic. It is the forbidden-case combination that conflicts, not the mere presence of the stronger rule in every model.

That result does not authorize the unguarded rule for forbidden attempts. It shows why the original theorem's impossible ambient scenario cannot serve as a discriminating comparison of legal encodings.

## 3. The sound abstract argument, and its limit

The original rival proof's displayed steps are locally sound: they derive proposal from the sufficient rule and its trigger, derive non-proposal from the necessary condition and its trigger, and contradict them. The ambient-context problem **does not refute this propositional reasoning**.

The core-only audit [reproves it over fresh Boolean variables](isabelle/GodelNetAddCausalityAudit.thy#L149), without appealing to the Full theorem. Write:

- `A`, `M`, `S`: attempted, amendment status, legislative support;
- `F`, `H`, `V`: clause in force, suffrage maintained, valid proposal.

The kernel proves:

```text
(A ∧ M ∧ S → V), (F ∧ ¬H → ¬V), A, M, S, F, ¬H ⟹ False

(F ∧ ¬H → ¬V) ↔ (V → ¬F ∨ H)

(C → V), (F ∧ ¬H → ¬V) ⟹ (C → ¬F ∨ H)
```

The last line is the strongest justified general constraint here: **a sufficient antecedent must imply the necessary guard in the intended context**. It need not literally contain that disjunction, and necessity does not determine sufficiency.

For an actual Core-specific check, [`audit_core_unguarded_rule_forces_clause_off`](isabelle/GodelNetAddCausalityAudit.thy#L90) proves that the unguarded rule entails `¬F2`, using Core's existing attempted-amendment, support, and non-maintenance facts. Since Core admits clause-on assignments, this is a meaningful restriction without importing Full.

Two further Boolean probes, both with `user_axioms, card time = 4, timeout = 300`, returned ordinary counterexamples:

| Probe | Result |
|---|---|
| Necessary constraint entails the repaired sufficient rule | Refuted: `A=M=S=F=H=True`, `V=False` satisfies the constraint but rejects the otherwise eligible proposal. |
| Unguarded sufficient rule and necessary constraint alone entail `False` | Refuted: they can coexist when the forbidden trigger is absent. |

These Booleans are fresh variables, **not aliases for the Core constants**. The probes retain the Core axioms to check ambient satisfiability; they do not purport to replace `pvr` inside Core. In addition, [`audit_abstract_stricter_rule_witness`](isabelle/GodelNetAddCausalityAudit.thy#L168) is a kernel proof of an existential Boolean witness: an eligible proposal can be rejected while satisfying the necessary constraint and a sufficient rule that also requires an extra condition `E`.

Compatible alternatives therefore include stricter sufficient conditions. The argument establishes neither that all guarded attempts must succeed nor that this proposal-stage interpretation is the uniquely correct legal one.

## 4. Corrections applied to `step-one-repair.md`

The [earlier note](https://github.com/incrediblecrab/godel-loopholes/blob/0b66df5/analysis/united-states-1947/step-one-repair.md) has been corrected as follows:

| Existing assertion | Strongest warranted replacement |
|---|---|
| Step one is “necessary” | The five-fact package is load-bearing for entailment in this encoding. Its absence does not prohibit dictatorship, and causal necessity over lawful executions has not been established. |
| The objection “fails mechanically” | One unguarded sufficient rule conflicts with the assumed necessary condition when a forbidden attempt occurs. This does not dispose of encoding-choice objections. The published test also assumes a case already excluded by its Full import. |
| “The disjunction is forced by Article V's proviso” | Given the encoded `comsp`, valid proposals must imply `¬in_force_omsp ∨ maint_suf`. The particular sufficient rule is a further modeling choice; the legal adequacy of `comsp` is not proved by this entailment. |
| The check is “forced rather than chosen,” classified as kernel-certified | Kernel-certified: the conditional logical compatibility requirement. Not established: uniqueness of the complete proposal rule, its constitutional interpretation, or repeal's causal necessity. |
| Moving the check to ratification leaves step one necessary | This needs its own isolated encoding and reachability/necessity tests. It does not follow from the rival theorem examined here. |

The source also has [only three government actors and four times](isabelle/GodelNetAddCore.thy#L38). [`maint_suf` and `sup_rat`](isabelle/GodelNetAddCore.thy#L132) are uninterpreted amendment/time predicates. There is no individual-state domain, per-state deprivation predicate, or separate state-consent exception. An external interpretation could try to place additional meaning inside those predicates, but no such correspondence is formalized here. This audit does not settle the relevant legal scholarship.

## 5. Reproduction and actual outcomes

All commands ran from the repository root. **Every imported local theory was supplied with its own `-f`; both final invocations used `process_theories -O -U`.**

The original raw records, `core-complete.log` and `full-verified.log`, are retained outside the checkout in the research session's `files/repair-causality-audit/` directory. Independent reruns in `files/parent-causality/` reproduced the same 16 new kernel lemmas and seven new ordinary counterexamples. These machine-local logs are not checked-in proof certificates; the source theories and commands below permit fresh reproduction.

A session-local runtime prefix was used because this Isabelle installation's settings overwrite ordinary incoming `ISABELLE_TMP_PREFIX` values. The commands override it inside `isabelle env`, after settings initialization, and also set Java's runtime directory. A fresh temporary directory avoids depending on the original machine's session path.

Setup and the final commands, including the display-only filters:

```bash
set -euo pipefail
ARTIFACTS=$(mktemp -d "${TMPDIR:-/tmp}/godel-causality.XXXXXX")
mkdir -p "$ARTIFACTS/runtime"

isabelle env bash -c \
  'export ISABELLE_TMP_PREFIX="$1/runtime/isabelle" TMPDIR="$1/runtime"; export ISABELLE_JAVA_SYSTEM_OPTIONS="$ISABELLE_JAVA_SYSTEM_OPTIONS -Djava.io.tmpdir=$1/runtime"; shift; exec isabelle "$@"' \
  audit "$ARTIFACTS" process_theories -O -U -o threads=1 \
  -f analysis/united-states-1947/isabelle/GodelNetAddCore.thy \
  -f analysis/united-states-1947/isabelle/GodelNetAddCausalityAudit.thy \
  GodelNetAddCausalityAudit 2>&1 |
  tee "$ARTIFACTS/core-complete.log" |
  awk '/audit_|Nitpick|\*\*\*|Running|Finished|Total|found a|ran out|timed out|Failed/ { print; fflush(); }'

isabelle env bash -c \
  'export ISABELLE_TMP_PREFIX="$1/runtime/isabelle" TMPDIR="$1/runtime"; export ISABELLE_JAVA_SYSTEM_OPTIONS="$ISABELLE_JAVA_SYSTEM_OPTIONS -Djava.io.tmpdir=$1/runtime"; shift; exec isabelle "$@"' \
  audit "$ARTIFACTS" process_theories -O -U -o threads=1 \
  -f analysis/united-states-1947/isabelle/GodelNetAddCore.thy \
  -f analysis/united-states-1947/isabelle/GodelNetAddFull.thy \
  -f analysis/united-states-1947/isabelle/GodelNetAddRivalRule.thy \
  -f analysis/united-states-1947/isabelle/GodelNetAddCausalityAuditFull.thy \
  GodelNetAddCausalityAuditFull 2>&1 |
  tee "$ARTIFACTS/full-verified.log" |
  awk '/audit_|rival_pvr_inconsistency|in_force_omsp_false_t2|Nitpick|\*\*\*|Running|Finished|Total|found a|ran out|timed out|Failed/ { print; fflush(); }'
```

| Final run | Process result | New kernel lemmas | Nitpick output |
|---|---|---:|---|
| Core audit | Exit 0; `Finished Draft (0:00:07 elapsed time)` | 14 | Six ordinary counterexamples |
| Full-context audit | Exit 0; `Finished Draft (0:00:08 elapsed time, 0:00:03 cpu time, factor 0.41)` | 2 | One new ordinary counterexample; inherited probes produced two models and one ordinary counterexample |

All ten final Nitpick invocations had explicit `timeout = 300`. **Final timeout/UNKNOWN results: none.** A successful theory build alone would not establish a probe result: the probes end in `oops`, and the stated outcomes are read from their actual logs.

Earlier attempts remain visible rather than being counted as successes: `core-first.log` records a parse error caused by the reserved fact name `prop`, subsequently renamed; `core-final.log` records two **quasi genuine** Boolean counterexamples when imported user axioms were disabled. The corrected probes retain those axioms and produced ordinary counterexamples. `core-verified.log` is the successful intermediate run before adding the separate presidential-content probe.

SHA-256 of the verified new sources:

```text
f4d6d537b0e7bb95f9f8f9d9da09e8e67ed60302d1a3f9d1cda0aa5aa1bcce39  GodelNetAddCausalityAudit.thy
ccd819f8c5bd65a098e8743f4a9fc482b69e8d086eed25381f8ce19ce20f38df  GodelNetAddCausalityAuditFull.thy
```

No `sorry`, added constitutional axioms, or additional dependencies were used. These experiments identify limits of the existing encoding; they do not identify Gödel's historical thought or establish a lawful constitutional loophole.
