# Gödel's step one forces a repeal event that no published result needs

This is the most substantial result in this folder, and it is a result about an instrument rather than about the Constitution. It is machine-checked and reproducible with one command. It does not advance the search for a candidate path by a single step, and it is not offered as one.

`formal-model-replication.md` records that Zahoransky and Benzmüller's model reproduces. `ratification-price.md` records what one ratification axiom carries. This file records what the amendment at the centre of Gödel's manoeuvre does and does not carry.

The short version. Gödel's route has two steps: first amend Article V to remove the clause protecting equal Senate suffrage, then use the unentrenched procedure to install a dictator. The model represents step one properly — the amendment `amd1a` is an object, it is proposed, supported, and genuinely ratified. Delete the four axioms that do all of that and **every theorem and lemma published in the original still proves, in a theory that is still consistent.** What is lost is the ratification event itself: `⌊is_rat amd1a⌋t2` is entailed by the full theory and becomes *independent* in the reduced one. So step one is not free — it costs exactly one proposition, and that proposition is the repeal. It is simply that no published result depends on it.

The reason is that `amd1a` is extensionally equal to the negation of the entrenchment clause, and that negation is separately forced by the stipulation that the dictatorship amendment was proposed. The repeal's *postcondition* is available without the repeal. The event is represented and entailed; its normative effect is not what does the work.

This is a narrower claim than earlier drafts of this file made. One said the model *cannot represent* repeal at all; another said deleting step one costs *nothing*. Both were false, adversarial review said so, and the machine agrees with the reviewer both times. The corrections are recorded below rather than quietly absorbed.

## Five machine-checked facts

**One. `Dictatorship_t3` is provable from six of the model's fifty-one axioms, and those six are consistent.**

| axiom | what it says |
|---|---|
| `t1_s_t2` | `t2` succeeds `t1` |
| `t2_s_t3` | `t3` succeeds `t2` |
| `Xpsr_t1` | at the next instant, a proposed amendment with ratification support becomes ratified |
| `Xrv_t2` | at the next instant, a ratified amendment is in force |
| `amd2_prop_t2` | the amendment vesting all three powers in the President is proposed at `t2` |
| `amd2_sup_rat_t2` | that amendment has ratification support at `t2` |

Sufficiency is a kernel-certified Isabelle theorem. Consistency is a Nitpick model of the six, which matters because an inconsistent theory proves everything and would make the first fact worthless.

Two qualifications, because both are the obvious objections and both are fair.

The proof also uses the model's definitions and abbreviations — `amd2_def`, `Dictatorship_def`, the temporal and quantifier operators. Definitions are conservative over the *old* vocabulary, but they are not inert: they carry the interpretation of the new symbols they introduce. `amd2` is *defined* as `is_leg P ❙∧ is_exe P ❙∧ is_jud P`, the concentration of all three powers in one person. So the honest statement is: six of the fifty-one non-definitional assumptions suffice, relative to the model's original definitional apparatus, which is shared unchanged.

Consequently the claim is *not* that the six mention no constitutional content. Unfold `amd2` and the separation of powers is right there. Nor is it that they contain no Article V machinery: `Xpsr_t1` and `Xrv_t2` propagate the generic rules that a proposed-and-supported amendment becomes ratified and that a ratified amendment takes effect, and those *are* the amendment procedure. An earlier version of this file said "none of the six is an Article V axiom", which classified by symbol name rather than by content and was not defensible.

The accurate breakdown is this. Two of the six are generic amendment-procedure rules (`Xpsr_t1`, `Xrv_t2`). Two are bare temporal-successor facts (`t1_s_t2`, `t2_s_t3`). Two stipulate that the dictatorship amendment is proposed and has ratification support (`amd2_prop_t2`, `amd2_sup_rat_t2`). **None is an equal-suffrage axiom, an entrenchment axiom, a Senate axiom, or a step-one axiom.** The concentration of powers enters as the *content of a stipulated proposal*, never as something the model derives a right to propose.

**Two. Four of those six are necessary to every sufficient support; six is not proved minimum.**

Dropping any one of the six from the six yields a countermodel, so the set is irredundant — no member is idle. That is weaker than minimality, and an earlier version of this file wrongly claimed the stronger thing. Irredundance leaves open that some different, smaller set drawn from the other forty-five proves the theorem.

There is a real lower bound available, and it was run. If the *full fifty-one-axiom theory* minus axiom `a` does not entail `Dictatorship_t3`, then no subset omitting `a` entails it either, since subsets are weaker. Four axioms pass that test: `Xpsr_t1`, `Xrv_t2`, `amd2_prop_t2`, `amd2_sup_rat_t2`. Every possible proof of the dictatorship theorem in this model must cite the generic ratification rule, the generic in-force rule, and the two stipulations that the dictatorship amendment is proposed and supported.

For `t1_s_t2` and `t2_s_t3` Nitpick returned no counterexample, which is a failure to find and not a proof of redundancy. **The established lower bound is four, not six.** `python3 axiom_sweep.py tight` prints both halves and labels which is which.

**Three. The four axioms representing Gödel's step one can be deleted, and nothing is lost.**

Delete `amd1a_prop_t1`, `amd1b_prop_t1`, `amd1a_sup_rat_t1`, and `amd1b_sup_rat_t1` — the axioms proposing and supporting the amendment that strips Article V's entrenchment clause — and Isabelle still proves `noDictatorship_t1`, `noDictatorship_t2`, and `Dictatorship_t3`. Nitpick then finds a model of the reduced theory, so the survival is not the vacuous survival of an inconsistent theory.

Two earlier versions of this file got the cost wrong in opposite directions. The first said no proof script changed, which was false. The second said five lemmas were "lost necessarily", which was also false and is the version this paragraph replaces. The truth is between them and closer to the first. Three of the five — `amd1b_val`, `amd1b_val_t1`, `amd1b_val_t2` — cite no `amd1` axiom whatever and survive completely untouched, because `amd1b` is an instance of excluded middle. The remaining two, `amd1a_val_t2` and `amd1b_val_t2_2`, have proof scripts that name deleted axioms, so those scripts break; but both propositions are re-provable without them, and the experiment re-proves them rather than dropping them. `amd1b_val_t2_2` is a duplicate of `amd1b_val_t2` and needs no axioms. `amd1a_val_t2` follows from `amd2_prop_t2` and `amd2_not_maint_suf_t2`, which is fact five (iii) and the whole explanation.

So the accurate statement is: **every published theorem and every intermediate lemma survives deletion of Gödel's step one, in a consistent theory. Two proof scripts are casualties; among those five propositions, none is.** The script prints which two.

What *is* lost is stated in fact five and should be read with this one: the ratification event `⌊is_rat amd1a⌋t2` is entailed by the full theory and is not entailed by the reduced one. An earlier version of this file said deleting step one costs "nothing" and that "no proposition is lost". That was false, and the experiment that refutes it is one I had already run. The cost is exactly one proposition, and it is the repeal.

**Four. Keeping the entrenchment clause at `t2` really does derive `False`, exactly as the authors say.**

The thesis anticipates the obvious objection — why not propagate `omsp` to `t2`? — and answers that "we would run into inconsistencies, were we to keep condition omsp for `t2` and also introduce an amendment `amd2` with `¬(maint_suf amd2)`." Adding `⌊❙X omsp⌋t1` to the full model lets Isabelle derive `False` in three lines. Their defence of the omission is correct on its own terms.

**Five. The model does represent the repeal, the repeal does occur, and deleting step one makes it independent.**

Three theorems, all proved in the unmodified fifty-one-axiom model, plus one countermodel.

The first is an equality between the amendment and the negation of the clause:

```
theorem amd1a_IS_not_omsp: "amd1a = (❙¬omsp)"
```

`amd1a` is defined as `❙∃φ. ❙¬(maint_suf φ) ❙∧ (is_prop φ)`; `omsp` abbreviates `❙∀φ. ❙¬(maint_suf φ) ❙⟶ ❙¬(is_prop φ)`. These are **extensionally** equal in Isabelle/HOL — not the same term, and not definitionally equal. An earlier version of this file called it a term identity, which was wrong; `by (rule refl)` fails on this goal, and the proof needs unfolding, classical reasoning, and function extensionality. What matters is that it needs **none of the model's non-definitional axioms**. So the amendment repealing the entrenchment clause is, in this encoding, the same proposition as *the clause has been broken* — as a matter of the logic, not of the stipulations.

The second says the repeal event actually happens:

```
theorem amd1a_ratified_at_t2: "⌊is_rat amd1a⌋t2"
```

`is_rat` is a predicate distinct from truth, so this is a real event and not a restatement. Gödel's step one is not merely gestured at in this model; it is carried out.

The third says the event was unnecessary for the post-state:

```
theorem amd1a_content_without_repeal: "⌊amd1a⌋t2"
```

proved from `amd2_prop_t2` and `amd2_not_maint_suf_t2` alone, citing no `amd1` axiom.

Then the countermodel. With the four `amd1` axioms deleted, Nitpick finds a model of the reduced theory in which `⌊is_rat amd1a⌋t2` is false. Combined with the rest, that fixes the status of the event precisely. Write `T` for the full theory, `T⁻` for the reduced one, `R` for `⌊is_rat amd1a⌋t2`. We have `T ⊨ R`, `T` consistent, `T⁻ ⊆ T`, and a model of `T⁻ ∧ ¬R`. Since `T⁻ ⊆ T`, every model of `T` is a model of `T⁻`, and every one of those satisfies `R` — so `T⁻ ⊭ ¬R`. And the Nitpick model gives `T⁻ ⊭ R`. **`R` is independent in the reduced theory.** The event does not become false; it becomes undetermined, which is exactly what one expects when the axioms that forced it are withdrawn.

That is the honest accounting of the cost. It is not nothing. It is one proposition, and no published result uses it.

`python3 axiom_sweep.py repeal` runs all four.

## Why every fact has one cause

`omsp` is an abbreviation for a material universal over propositions:

```
omsp ≡ ❙∀φ. (❙¬(maint_suf φ)) ❙⟶ (❙¬(is_prop φ))
```

Read it plainly: *nothing that fails to maintain equal suffrage is proposed*. That is a statement about the world's contents. A norm being legally in force is not the same kind of thing as everybody happening to comply with it, and this formula is the second. The model has no separate `in_force` predicate, and `is_prop` is itself ambiguous between an amendment having been *put forward* and an amendment having been *validly* put forward.

Everything follows from that, and the chain is short.

Because the clause's content is "no forbidden proposal exists", its negation is made true by any forbidden proposal. The model stipulates one: `amd2_prop_t2` together with `amd2_not_maint_suf_t2`. So `⌊❙¬omsp⌋t2` is derivable from those two axioms alone — the theorem is named `omsp_false_at_t2` for that reason. Nothing has to be repealed for the clause to come out false; asserting the violation suffices.

Fact five is then immediate. `amd1a` *is* `❙¬omsp`, so the very same two axioms that make the clause false also establish the content of the repealing amendment. Ratifying `amd1a` is a distinct event, it does occur, and it is redundant: it delivers a proposition the theory already has.

Fact three follows from fact five. The `amd1` axioms are the model's representation of the repealing amendment as something proposed and supported, and they are bypassed entirely, because their payload arrives by another route.

Fact four falls out too: if asserting the forbidden proposal is by itself enough to falsify the clause, then asserting both the clause and the proposal is a flat contradiction. The authors did not hit a deep obstacle. They hit the fact that in their encoding, "the clause holds" and "the forbidden amendment was proposed" cannot both be written down.

The authors are explicit that this was their design, in both venues: "In a way the amendment to Art. V is implemented by simply not using `⌊X omsp⌋t1` as axiom, rather than by working with one of the above suggested amendments amd1a and amd1b."

**Nothing here was concealed.** The disclosure appears in the thesis and again in the peer-reviewed paper. They also call `amd1b` "a tautology" — correctly; it is `∀φ. is_prop φ → (maint_suf φ ∨ ¬maint_suf φ)`, an instance of excluded middle that proves with no axioms at all — and they write that "the suggested amendments do not constitute ideal amendments for the desired outcome." Any account of this result implying otherwise is wrong.

What the experiments add is the size of the concession. "In a way" and "not ideal" are hedges of unknown magnitude. The measurement is that the magnitude is zero: every published theorem and every intermediate lemma survives complete deletion of those axioms, in a theory that is still consistent.

## The limits of the criticism, stated against myself

Three claims made in earlier drafts of this file were disproved, two of them by experiments written specifically to try to break them.

**"The formalism cannot represent a constraint that blocks an amendment."** False. The refuting experiment is `blocking`. Propagate `omsp` to `t2`, drop `amd1a`, and — the operative change — decline to stipulate `amd2_prop_t2`. The result is satisfiable, Nitpick finds a model, and Isabelle proves

```
theorem amd2_is_blocked_at_t2: "⌊❙¬(is_prop amd2)⌋t2"
```

The clause holds and the dictatorship amendment is provably not proposed. Blocking is expressible in the authors' own logic with no added machinery.

**"The six axioms are minimal."** False as stated; they are irredundant, which is weaker. Fact two now reports the established lower bound of four and says which two axioms are undetermined.

**"The model cannot tell repeal from violation."** This was the previous title of this file, and it overshoots. Fact five is the refutation: `is_rat amd1a` is a predicate distinct from `amd1a`, the model can and does say that the repealing amendment was ratified, and the two are not confused. What survives is narrower. The clause's *failure* is not brought about by the repeal in any proof, because the clause's content is a description of the world rather than a statement of a norm's standing, so a violation falsifies it just as a repeal would. The model can name the repeal; it just never needs it.

The residue is a defect in the encoding, not in the logic, and that distinction has to be kept. Higher-order logic can perfectly well carry a separate `in_force` predicate and a distinction between an attempted and a valid proposal; this model has neither. The correct criticism is specific and repairable rather than sweeping.

A one-axiom repair gets partway and no further. Replacing the omission with `⌊(❙X(is_rat amd1a)) ❙∨ (❙X omsp)⌋t1` — the clause persists unless the anti-entrenchment amendment is ratified — leaves the theory consistent and `Dictatorship_t3` provable. But with `amd2_prop_t2` still an axiom the second disjunct is impossible, so the model *derives* that `amd1a` was ratified whether or not anything says so. A faithful formalization would have to stop asserting `amd2_prop_t2` and derive it from satisfied preconditions. That is the outstanding work and the shape the next experiment should take.

## What the formalization therefore establishes

Read narrowly, `Dictatorship_t3` says: in a model with a generic amendment rule and no entrenchment constraint in force, if an amendment vesting all powers in one person is proposed and has ratification support, then that person holds all powers. That is valid, correctly proved, and close to a restatement of the amendment procedure.

The paper concludes that "we have explored an argument on how to introduce a dictatorship in the USA without violating the rules laid out in the US Constitution." The gap is in the phrase *without violating*. Establishing that requires the entrenchment clause to have been lawfully removed *before* the forbidden amendment is proposed. The model does contain such a removal, and it happens; but no theorem depends on it, because the clause is encoded as a claim about what has been proposed rather than about what a rule requires, and the forbidden proposal falsifies it directly. So the formalization proves that a dictatorship follows once the clause is out of the way. It does not prove that the way it got out of the way was lawful.

This is a limitation of the formalization. It is not evidence that Gödel was wrong, and this file makes no claim either way about the underlying legal question.

## Reproducing it

```
cd analysis/united-states-1947/search
python3 axiom_sweep.py all      # minimal, noamd1, omsp, lapsed, blocking, repeal
python3 axiom_sweep.py tight    # irredundance and the four-axiom lower bound, slower
python3 axiom_sweep.py sweep    # all 51 single ablations, slowest and weakest
```

Every theory the script runs is generated from `isabelle/GodelCore.thy` and `isabelle/GodelConstitution.thy`. Nothing is transcribed twice. `verify.sh` §4f runs the six fast experiments.

`sweep` is the weakest and is kept only for completeness: it reports which axioms produce a countermodel when singly withdrawn, and "Nitpick found no counterexample" is a failure to find rather than a proof of redundancy. The `minimal` and `tight` experiments settle the same question constructively and should be preferred.

## Standing of the evidence

`minimal`, `noamd1`, `omsp`, `lapsed`, `blocking`, and the first three parts of `repeal` rest on Isabelle proofs, kernel-certified and retained. The consistency probes, the irredundance and lower-bound results in `tight`, `sweep`, the satisfiability half of `blocking`, and part (iv) of `repeal` are Nitpick results terminated with `oops` — model-finder diagnostics, strong and re-runnable, but not proofs.

Every ablation in this file is now paired with a consistency probe, and that guard exists because it caught a real failure. The first version of the `noamd1` generator rebuilt all the axioms into a single block placed before the `amd2` definition. `amd2` was then a free variable, Isabelle generalized it, *every* proposition became proposed and supported at `t2`, and the theory collapsed into inconsistency — while still printing all three theorems as proved. The result looked like a triumph in the log and was worth nothing. It was found by adversarial review, not by the harness, and the harness was changed so that the same class of defect cannot pass silently again. The repaired experiment reproduces the finding honestly.

Two further objections deserve answering rather than deflecting.

*Every proof uses a subset of the axioms; is "six of fifty-one" merely that?* Partly, and the framing has been narrowed accordingly. In a monotonic logic a positive conclusion will not generally need the negative constraints, so the bare count proves less than it appears to. The load is carried instead by the *lower bound* — four axioms that every sufficient support must contain, none of them constitutional — and by fact three, which is not a subset observation at all but a survival result about three named theorems under deletion.

*Does the six-axiom support show the other axioms do no legal work?* No, and this file no longer says so. The other axioms restrict which models count and carry the claim that the path violates no rule. Showing the theorem provable without them is not showing them idle. It is showing that the theorem, as stated, does not depend on the rules the paper's title says are not violated.

The scope of every claim here is *this transcription*. The authors publish no `.thy` file, so the model was transcribed by hand from the thesis PDF. `verify.sh` §5b checks that the split into `GodelCore` and `GodelConstitution` preserved all labelled formulas verbatim against the pre-split file in git, which guards the refactor but not the original transcription, and it compares labelled propositions rather than definition bodies. The definitions the six-axiom proof leans on are hand-checked against §§4.2–4.3 of the thesis, not machine-diffed, and that is a real gap in the assurance. The specific fact this result turns on was verified directly against the PDF: `omsp` occurs in exactly one axiom, `omsp_t1`, and the thesis contains no `X omsp` axiom anywhere.

## Falsifiers

An `X omsp` axiom, or any equivalent propagation of the entrenchment clause past `t1`, found in the thesis and missing from this transcription. The result would be an artifact of the transcription and would be withdrawn entirely.

A transcription error in `amd2_def`, `Dictatorship_def`, `psr`, `rv`, or `tnext`. These are load-bearing for the six-axiom proof and are the part of the transcription the automated checks do not cover.

A published theorem of the model that fails when the four `amd1` axioms are deleted. The three replication targets survive; if a fourth result of the thesis does not, fact three must be narrowed to those three.

A five-axiom support for `Dictatorship_t3`. This would not overturn anything, since six is only claimed to be irredundant, but it would sharpen the picture and would retire the six-axiom framing.

A reading of the model on which `amd1a` and `amd1b` do carry the transition. One partial reading is already known and is not sufficient: if `omsp` *were* propagated to `t2`, `amd1a` would be inconsistent with it, so `amd1a` does encode the incompatibility the manoeuvre is about. But nothing in the model exercises that incompatibility, because `omsp` is never propagated and no published theorem uses it. A reading that also survives `amd1b` being a tautology, and the null result in `isabelle/RatificationDependency.thy` showing `amd1a` holds at `t2` with no ratification axiom whatever, would defeat this file.

A demonstration that `blocking` assumes its conclusion — that withholding `amd2_prop_t2` is not the same as declining to assume it. The answer is that `amd2_prop_t2` is an axiom in the original and its withdrawal is the entire point, but a reader who thinks the blocked state is reached too cheaply should say so.

An `in_force` predicate, or any other separation of a norm's standing from its observance, found in the thesis and missing here. That would defeat the central claim outright.

## Relation to the rest of the folder

`ratification-price.md` shows `amd2_sup_rat_t2` is non-redundant. That result is subsumed here and strengthened twice over: the axiom is not merely non-redundant, it is one of six that suffice, and it is one of the four that every sufficient support must contain.

`academia/article-v-entrenchment.md` records the pre-1947 literature on whether Article V's entrenchment clause can be amended away at all. It bears on this file only indirectly, but it is the reason the question is worth formalizing correctly.

`threshold-arithmetic.md` derives the thirty-six-of-forty-eight requirement the model does not contain. `search/quorum_cascade.py` measures the congressional proposing stage. Neither bears on this result, which is about the model rather than about 1947.
