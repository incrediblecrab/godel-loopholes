# A formalization where the conjectured first step affects entailment

This file records the construction and results of a new Isabelle/HOL formalization that repairs three structural defects in the Zahoransky & Benzmüller (Z&B) model, the model whose replication and analysis are documented in `inert-manoeuvre.md` and `formal-model-replication.md`.

The finding in `inert-manoeuvre.md` is that the published model's step one is inert: deleting the axioms encoding Gödel's first step (repealing the Article V entrenchment clause) does not break any published theorem, because `amd2_prop_t2` — the dictatorship amendment being proposed — is asserted as an axiom rather than derived from the repeal.

This file asks: **can that defect be repaired?** Can a formalization be built in which `amd2_prop_t2` is derived from satisfied preconditions, and if so, does step one then become load-bearing?

The short answer. **Yes, as an entailment dependency, not a causal necessity.** In the repaired model (44 axioms), `Dictatorship_t3` is a machine-checked theorem. Deleting the five step-one axioms yields a 39-axiom theory where Nitpick finds countermodels to both `Dictatorship_t3` and `¬Dictatorship_t3` — the theorem is independent without that package. The full theory and the reduced theory are both consistent by Nitpick. The package is therefore load-bearing for entailment. The [subsequent causality audit](repair-causality-audit.md) also finds dictatorship with the clause always in force and **no amendments ratified at all**: this encoding does not define lawful execution histories or supply the persistence constraints needed to establish causal necessity. The two-step argument is a scholarly reconstruction, not a preserved account of Gödel's actual mechanism.

## Three defects repaired

The Z&B model conflates three things that ought to be distinct. The repair separates them.

**1. `in_force` separated from compliance.** Z&B represent the entrenchment clause (`omsp`) at a time point by the *presence or absence* of the axiom asserting it. This means the model cannot state "the clause is in force but is being violated" or "the clause has been repealed." The repair introduces an explicit predicate `in_force_omsp :: σ` that tracks whether the clause is legally operative, independent of whether actors are complying with it. The entrenchment constraint (`comsp`) is conditioned on `in_force_omsp`: when the clause is in force, no proposal that fails to maintain suffrage can be valid; when it is not in force, the constraint is lifted.

**2. Attempted proposals distinguished from valid ones.** Z&B treat `is_prop` as directly stipulated. The repair introduces `attempted :: σ → σ` (put forward for proposal) and derives `is_prop` via a proposal validity rule (`pvr`): an attempted amendment that is an amendment, has legislative support, and passes the entrenchment check (either the clause is not in force or the amendment maintains suffrage) is validly proposed. This is how `amd2_prop_t2` becomes derivable rather than asserted.

**3. `amd2_prop_t2` is derived, not asserted.** This is the crux. In Z&B, the dictatorship amendment being proposed at `t2` is an axiom. Here, the step-two stipulations assert only the *preconditions* for the dictatorship amendment: it is attempted, it is an amendment, Congress supports it, it does not maintain suffrage, and the states support ratification. Whether it is *validly proposed* depends on whether the entrenchment clause is in force at `t2`. Full derives the clause's absence from the step-one facts; Core does not require a repeal event to explain its absence.

### The derivation chain

1. `pvr` fires at `t1`: `amd1a` is validly proposed. It is attempted, it is an amendment, Congress supports it, and it maintains suffrage (repealing the entrenchment clause does not itself change Senate representation). So even with the entrenchment clause in force, `amd1a` passes. **Derived, not asserted.**
2. `psr` fires at `t1`: proposed and supported → ratified at `t2`.
3. `rv` fires at `t2`: ratified `amd1a` → `amd1a` holds → `¬in_force_omsp t2`.
4. `pvr` fires at `t2`: `amd2` is validly proposed. It is attempted, it is an amendment, Congress supports it, and the entrenchment clause is *not in force* (from step 3). The suffrage check is vacuously passed. **This is the derived `amd2_prop_t2`.**
5. `psr` fires at `t2`: proposed and supported → ratified at `t3`.
6. `rv` fires at `t3`: ratified `amd2` → `Dictatorship_t3`.

### Design choices

**Rules are global, not time-indexed.** Z&B assert each constitutional rule at `t1` and propagate it forward via `X`-axioms. In the repair, rules are asserted globally (`⌊rule⌋` rather than `⌊rule⌋t1`). This is an encoding assumption, not a proved equivalence between the two theories. The rules hold at every modeled time; the separate fact `in_force_omsp` can vary.

**`amd1a ≡ ¬ in_force_omsp`.** The content of the repeal amendment is simply that the entrenchment clause is not in force. When ratified and `rv` applies, this directly yields `¬in_force_omsp`. This is a cleaner representation than Z&B's `amd1a ≡ ∃φ. ¬(maint_suf φ) ∧ (is_prop φ)`, which defines the repeal as a violation of the constraint rather than a repeal of it.

**`maint_suf amd1a` is TRUE.** The repeal of the entrenchment clause does not itself change Senate representation. This is how `amd1a` passes the entrenchment check at `t1` while the clause is still in force. The dictatorship amendment, which concentrates all three powers in the President, does *not* maintain suffrage (`amd2_not_maint_suf_t2`), which is why it needs the clause repealed first.

## Machine-checked results

### Full model (GodelNetAddFull.thy, 44 axioms)

All seven are kernel-certified Isabelle theorems:

| theorem | statement | status |
|---|---|---|
| `amd1a_proposed_t1` | `⌊is_prop amd1a⌋t1` | **proved** (derived) |
| `amd1a_ratified_t2` | `⌊is_rat amd1a⌋t2` | **proved** |
| `amd1a_val_t2` | `⌊amd1a⌋t2` | **proved** |
| `in_force_omsp_false_t2` | `¬(in_force_omsp t2)` | **proved** |
| `amd2_proposed_t2` | `⌊is_prop amd2⌋t2` | **proved** (derived — the key fact) |
| `amd2_val_t3` | `⌊amd2⌋t3` | **proved** |
| `Dictatorship_t3` | `⌊Dictatorship⌋t3` | **proved** |

Consistency (diagnostic, Nitpick, `card time = 4`, timeout 300s):
- `True` with `satisfy`: **model found** — the axioms are satisfiable.
- `False`: **counterexample found** — the theory does not entail `False`.

### Reduced model (GodelNetAddNoStep1.thy, 39 axioms)

No step-one axioms. All three are Nitpick probes (diagnostic, not proof):

| probe | statement | result |
|---|---|---|
| `no_step1_consistent` | `False` | **counterexample found** — theory is consistent |
| `dictatorship_without_step1` | `⌊Dictatorship⌋t3` | **counterexample found** — NOT entailed |
| `no_dictatorship_without_step1` | `⌊¬ Dictatorship⌋t3` | **counterexample found** — NOT entailed |

The two countermodels diagnose **independence** without the step-one package. Core does not fix `in_force_omsp` at `t2`, although it constrains its relationship to other predicates. An operative clause blocks `amd2` from being proposed and ratified; an inoperative clause entails `Dictatorship_t3` given the other stipulations. Blocking that amendment does **not** block the dictatorship predicate itself: offices can change without ratification because their persistence into `t3` is not encoded.

### Core model (GodelNetAddCore.thy, 39 axioms)

All proved (kernel-certified):

| theorem | statement | status |
|---|---|---|
| `noDictatorship_t1` | `⌊¬ Dictatorship⌋t1` | **proved** |
| `noDictatorship_t2` | `⌊¬ Dictatorship⌋t2` | **proved** |
| government lemmas (10) | unique legislators, executives, judges at t1, t2 | **proved** |
| `pvr_elim` | elimination form of `pvr` | **proved** |

## The answer

**Step one now does work.** In the Z&B model, `Dictatorship_t3` survives deletion of step one because the fact it would derive (`amd2_prop_t2`) is asserted as an axiom. In the repaired model, `amd2_proposed_t2` is derived via the six-step chain above, and deleting the five step-one axioms makes the theorem independent.

This does not establish that the Z&B proofs are wrong. Their consistent formalization proves its stated theorems, but those theorems do not test whether the repeal matters to the reconstructed argument. The repair makes the repeal facts matter to entailment; it does not settle the lawfulness of repeal or show that every path to dictatorship needs one. Gödel's own mechanism has not been established by the historical sources.

## The encoding-choice objection remains

The obvious objection is that the repair was built to reach this conclusion. A proposal-validity rule is a design choice, and a rule chosen so that step one lies on the only path to a valid proposal would leave `Dictatorship_t3` independent without the five step-one axioms for reasons that say nothing about Gödel and everything about the encoding. That would be the same defect as the asserted axiom it replaces, pointed the other way.

The original response overstated what its rival-rule experiment established. Its displayed propositional reasoning is sound: a sufficient rule authorizing a proposal and a necessary condition forbidding that same proposal contradict each other when both triggers hold. But `GodelNetAddRivalRule.thy` imports Full, which already proves the clause is off at `t2`, and then assumes it is on. The [isolated audit](repair-causality-audit.md#2-the-rival-theorems-ambient-context) proves that this contrary assumption **alone** entails `False`, without the rival rule. The original experiment therefore does not discriminate between otherwise admissible encodings.

A Core-only proof over fresh Boolean variables establishes the narrower compatibility requirement: given the encoded necessary condition `comsp`, a sufficient antecedent must imply `¬in_force_omsp ∨ maint_suf`. This does not uniquely determine a sufficient rule. Stricter rules can satisfy that requirement without accepting every proposal that passes the guard. Neither the legal interpretation of `comsp` nor the completeness of `pvr` follows from this logical constraint.

Moving the check from proposal to ratification requires a separate model and tests; the rival theorem does not establish the result of that change. The [finite Article V search](bounded-article-v-search.md) supplies such a separate experiment with explicit frames, identified state consent, and both screening stages. It is a new conditional model, not a proof that the repaired Isabelle encoding faithfully represents constitutional law.

## Epistemic status

| claim | status |
|---|---|
| `Dictatorship_t3` is a theorem of the 44-axiom model | **machine-checked** (Isabelle kernel) |
| The 44-axiom model is consistent | **diagnostic** (Nitpick countermodel to `False`) |
| `Dictatorship_t3` is independent of the 39-axiom model | **diagnostic** (Nitpick countermodels to `⌊Dictatorship⌋t3` and `⌊¬Dictatorship⌋t3`) |
| The 39-axiom model is consistent | **diagnostic** (Nitpick countermodel to `False`) |
| Given `comsp`, a sufficient antecedent must imply its necessary guard | **machine-checked conditional logic** (Core-only causality audit) |
| The full sufficient rule or its legal interpretation is uniquely forced | **not established**; stricter compatible rules exist |
| Repeal is necessary for dictatorship in every Core model | **refuted diagnostically**; dictatorship without any ratifications has a countermodel |
| Repeal is causally necessary over lawful constitutional histories | **not tested by this encoding**; event-complete histories and persistence are missing |
| The derivation chain is faithful to Gödel's actual argument | **historically unverified**, not established by a formal proof |

The distinction matters. Nitpick is a bounded model finder. An ordinary genuine countermodel refutes entailment in the encoding, but failure to find one — whether from exhausted finite bounds, timeout, or another inconclusive outcome — is not a proof. The consistency claims rest on Nitpick diagnostics, not on Isabelle's kernel.

## Files

| file | role |
|---|---|
| `isabelle/GodelNetAddCore.thy` | Infrastructure, rules, government, step-two stipulations (39 axioms) |
| `isabelle/GodelNetAddFull.thy` | Step-one axioms + derivation chain + `Dictatorship_t3` (5 additional axioms) |
| `isabelle/GodelNetAddNoStep1.thy` | Ablation: no step one, Nitpick probes |
| `isabelle/GodelNetAddRivalRule.thy` | Original model-shape probe and conditional incompatibility proof; its ambient-context limitation is audited below |
| `isabelle/GodelNetAddCausalityAudit.thy` | Core-only entailment lemmas, missing-frame countermodels, and abstract compatibility controls |
| `isabelle/GodelNetAddCausalityAuditFull.thy` | Isolated audit of the rival theorem's Full context |

The baseline replication (`GodelCore.thy`, `GodelConstitution.thy`) is untouched.

## Axiom inventory

### Core (GodelNetAddCore.thy) — 39 axioms

| group | count | axioms |
|---|---|---|
| Time structure | 16 | `t1_s_t2`, `t2_s_t3`, `t3_s_te`, `te_s_te`, 12 negative successor facts |
| Uniqueness | 3 | `unique_is_leg`, `unique_is_exe`, `unique_is_jud` |
| Government at t1 | 3 | `Con_Leg_t1`, `P_Exe_t1`, `Cou_Jud_t1` |
| Government propagation | 3 | `XCon_Leg_t1`, `XP_Exe_t1`, `XCou_Jud_t1` |
| Constitutional rules (global) | 8 | `oap`, `osp`, `comsp`, `opr`, `rv`, `osr`, `psr`, `pvr` |
| Initial state | 1 | `in_force_omsp_t1` |
| Step-two stipulations | 5 | `amd2_attempted_t2`, `is_amd_amd2_t2`, `sup_prop_amd2_t2`, `amd2_not_maint_suf_t2`, `amd2_sup_rat_t2` |

### Full (GodelNetAddFull.thy) — adds 5 axioms (total 44)

| group | count | axioms |
|---|---|---|
| Step-one stipulations | 5 | `amd1a_attempted_t1`, `is_amd_amd1a_t1`, `sup_prop_amd1a_t1`, `maint_suf_amd1a_t1`, `amd1a_sup_rat_t1` |

### Reduced (GodelNetAddNoStep1.thy) — 39 axioms

No axioms added. Same as Core.
