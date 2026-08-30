# The price of the ratification assumption

`formal-model-replication.md` records that Zahoransky and Benzmüller's model reproduces, that its axioms are consistent, and that its three theorems carry information. It also records the first thing the model assumes rather than derives: the *effect* of amending Article V is implemented by omitting an axiom. The ratification event itself is represented and entailed, as `inert-manoeuvre.md` fact five shows; what is not represented is any causal link from that event to the effect.

This file records what a second assumption turns out to carry. It is the only result in this folder that is ours rather than borrowed, and it is narrower than it first looked. An earlier draft overstated it in four places; the corrections are kept visible below rather than quietly removed, because those overstatements are the kind this project exists to catch.

## The claim, stated as narrowly as the evidence supports

`Dictatorship_t3` rests on `amd2_val_t3`, which rests on `amd2_sup_rat_t2`. That axiom reads `⌊sup_rat amd2⌋t2`, and since `amd2` is defined as `is_leg P ∧ is_exe P ∧ is_jud P`, it asserts that the amendment vesting all three powers in the President has the support required for ratification.

Withdrawing that one axiom, and nothing else, leaves a theory in which **no proof of `Dictatorship_t3` exists**. Nitpick returns a countermodel: an interpretation satisfying every remaining axiom in which dictatorship at `t3` is false.

That is the result, and it is worth stating carefully, because a weaker version of it is already visible in the source. Anyone reading the proof can see that it cites `amd2_sup_rat_t2`, and the thesis prints the same dependency. What a countermodel adds is that no *other* route exists either. The distinction between "the authors' proof used this premise" and "no proof succeeds without this premise" is the whole of the contribution here.

## What `sup_rat` is, and what it is not

`sup_rat` is uninterpreted. The thesis says so directly in §4.1: "What this support looks like shall not be specified further."

The same section is more specific than that, and this is the part that matters. It enumerates the components of Article V it will model and the components it will not, and among the discarded ones are "2.1. three fourths of State Legislatures" and "2.2. three fourths of State Conventions." The stated reason is that these "are part of the federal system which is not essential to the argument."

The omission is therefore deliberate, declared, and reasoned. It was not overlooked, and this file does not claim it was. Nor does the experiment show the authors were wrong to omit it, and an earlier draft claimed close to that. What §4.1 declares inessential is the *decomposition* — legislatures versus conventions, three fourths, the count of states — not the *condition* that ratification support obtains. Withdrawing the condition therefore says nothing about whether the decomposition was needed. A model of a car can require `has_fuel` without modelling refineries; deleting `has_fuel` breaks the model and tells you nothing whatever about refinery chemistry. Testing the abstraction itself would require refining it — replacing `sup_rat` with an explicit state-by-state ratification structure and asking whether the theorem survives — which is a different experiment and is not performed here.

What the ablation does establish is narrower and still worth having. The abstract premise is non-redundant: the theorem is conditional on it, by every route and not merely by the authors' chosen one. And because the premise is never decomposed, the model cannot be asked any question about coalition size, mode of ratification, or feasibility. Those questions are outside its expressive reach; they are not answered in the negative by it.

Three further precisions, each of which an earlier draft got wrong.

`sup_rat` does not mean "thirty-six state legislatures voted yes." Article V permits ratification "by the Legislatures of three fourths of the several States, or by Conventions in three fourths thereof, as the one or the other Mode of Ratification may be proposed by the Congress." The mode is Congress's to choose, so any claim about legislatures specifically is over-read. The correct statement is thirty-six of forty-eight states, by whichever mode Congress directs.

The model does not lack a representation of ratification. It has a coarse one — `is_rat`, `sup_rat`, and the three axioms `opr`, `osr`, `psr` that govern them. What it lacks is any decomposition of ratification into states, modes, votes, or thresholds.

The freedom is real but an earlier draft argued for it the wrong way, and the wrong argument is worth recording because it is persuasive. That draft said: `sup_rat` appears only in the antecedents of `osr` and `psr`, so no axiom can conclude it, so it can only ever be stipulated. Both halves are false. `osr` and `psr` are *definitions*, asserted at particular times by six separate axioms — `osr_t1`, `psr_t1`, `Xosr_t1`, `Xpsr_t1`, `Xosr_t2`, `Xpsr_t2` — with the rest derived. And "antecedent position" carries no weight in classical logic: `osr` is `¬(sup_rat φ) → ¬(X(is_rat φ))`, whose contrapositive is `X(is_rat φ) → sup_rat φ`. Given ratification, support follows. `RatificationDependency.thy` now carries the refutation as a proved lemma, `sup_rat_IS_derivable_from_ratification`, stated with the hypothesis discharged explicitly so that it cannot contaminate the ablation. The defensible statement is the semantic one and nothing more: `amd2_sup_rat_t2` is independent of the remaining theory. It is a fair modelling choice, since a constitutional model cannot be expected to predict how legislatures vote, but it means the headline theorem is conditional on an input the model never examines.

## The experiment, and which parts of it are informative

`isabelle/GodelCore.thy` holds everything not depending on a ratification axiom. `isabelle/GodelConstitution.thy` adds the three `sup_rat` axioms and the four results that follow. The union is the thesis model formula for formula: `verify.sh` §5b recovers the pre-split file from git, strips comments, normalises whitespace, and compares every labelled formula body — all eighty-one are identical. `isabelle/RatificationDependency.thy` loads `GodelCore`, restores `amd1a_sup_rat_t1` and `amd1b_sup_rat_t1`, and withholds `amd2_sup_rat_t2` alone.

| question | answer | informative? |
|---|---|---|
| is the reduced theory satisfiable? | model found | no — forced |
| does it entail `False`? | countermodel | no — forced |
| does it entail `⌊Dictatorship⌋t3`? | **countermodel** | **yes** |
| does it entail `⌊¬Dictatorship⌋t3`? | countermodel | no — forced |
| does it entail `⌊sup_rat amd2⌋t2`? | countermodel | no — forced |
| does it entail `⌊¬(sup_rat amd2)⌋t2`? | countermodel | no — forced |

The "forced" column is the correction that most changes the character of this file. Write `T` for the reduced theory and `A` for the withdrawn axiom. `formal-model-replication.md` already establishes that `T ∪ {A}` is satisfiable and entails dictatorship. Since `T ⊆ T ∪ {A}`, every model of `T ∪ {A}` is a model of `T`. That alone forces **five of the six rows** before anything is run. Satisfiability, non-triviality and the `¬Dictatorship` row are witnessed directly by any model of `T ∪ {A}`. The last row is too: such a model satisfies `A`, so `T ⊭ ¬A`. And the fifth is forced by the third — if `T ⊨ A` then `T ⊨ Dictatorship`, contradicting the countermodel, so `T ⊭ A`; indeed the countermodel found for `Dictatorship` must already falsify `A`. An earlier draft of this file described those last two rows as "locating the freedom." They locate nothing. They are consequences of results already in hand.

Only the `Dictatorship` row is new information. The other five are instrument checks — if Nitpick contradicted them the tooling would be wrong — and reporting six countermodels as six results would have been inflation by a factor of six.

One check that appeared to work does not, and it is kept in the theory because it looks convincing. Proving `amd1a` valid at `t2` seems to confirm that Article V is still amended in the reduced arm. It proves — but it proves with no ratification axiom whatsoever, because `amd1a` is the existential "some proposed amendment fails to maintain Senate suffrage" and `GodelCore` already asserts both `amd2_prop_t2` and `amd2_not_maint_suf_t2`, so `amd2` witnesses it directly. The theory now carries that proof under the name `amd1a_valid_t2_without_any_ratification_axiom`, citing no `sup_rat` axiom, so the trap is visible rather than hidden. What actually puts the model into its post-amendment state is the omission of `X omsp` at `t1`, hard-coded in `GodelCore`, which is the authors' own acknowledged concession.

These are Nitpick results, terminated with `oops`. They are model-finder diagnostics, not kernel-certified theorems retained by Isabelle. That is the right level of confidence to attach: strong evidence, machine-produced, re-runnable, and not a proof.

## The thesis's own objection: the argument fails, the conclusion may not

Section 3 of the thesis raises two practical objections and then proceeds anyway: "Having made these remarks, we do choose to work with the argument presented above."

The first is that it is "highly unlikely that any state legislature would ratify an amendment depriving Art. V of its entrenchment clause." That is a claim about politics rather than about the text, and this project has no quarrel with it.

The second is an argument. The thesis says that "if we assume that a majority of Congress and state legislatures do support the anti-entrenchment amendment, then the amendment is actually unnecessary," because Article V bars removing a state's equal suffrage only "when said state does not give its consent" — so states willing to ratify the first amendment would simply consent to the second, and the two-step manoeuvre does no work.

**The argument as stated is invalid, and this holds unconditionally.** Its premise is "a majority of ... state legislatures." Its conclusion requires "all states support," and the very next sentence silently supplies it: "Assuming that all states support the anti-entrenchment amendment..." Those are different assumptions, and Article V's proviso is exactly why the difference matters: consent is required from each state *deprived*, so a deprivation reaching all forty-eight requires forty-eight consents, while ratification requires thirty-six. A slide from *a majority of* to *all* is a defect in the argument regardless of whether its conclusion is true.

**Whether the conclusion is nevertheless true depends on two contested readings of Article V, and an earlier draft of this file resolved both in whichever direction suited it.** The two questions are independent:

- **Scope.** Does "deprived of its equal Suffrage in the Senate" reach only *inequality* of representation, or also the Senate's *emasculation* — an amendment that leaves two senators per state but vests their power elsewhere? Call these the formal and functional readings.
- **Self-entrenchment.** Can the proviso itself be repealed by an ordinary Article V amendment, clearing the way for a second one? Call these repealable and entrenched.

| | proviso repealable | proviso entrenched |
|---|---|---|
| **functional scope** | `amd2` deprives all forty-eight, so the direct route needs forty-eight consents; the two-step needs thirty-six twice. **The two-step does real work, and the thesis's conclusion is false.** | `amd1` cannot be enacted. The Gödel route dies at step one. Conclusion true, but the whole construction fails with it. |
| **formal scope** | `amd2` never triggers the proviso — every state keeps two equally powerless senators — so no consent is needed from anyone and `amd1` is superfluous. Conclusion true, thesis's reasoning still wrong. | As above. Self-entrenchment is irrelevant when the proviso is never engaged. Conclusion true, reasoning still wrong. |

So the thesis's conclusion survives in three cells of four, and its stated reasoning survives in none of them. The correction this file can defend is therefore two-part, and the second part is conditional: the argument given is invalid everywhere; the two-step manoeuvre does real work **if and only if** the proviso is read functionally *and* is not self-entrenched.

That combination is not idle — it is the reading Gödel's loophole requires, since a formal-scope reading makes the entire two-step construction unnecessary and a self-entrenched proviso makes it impossible. But it is one quadrant, it was contested before 1947, and this file does not resolve it.

**What the pre-1947 authorities say is now recorded and checked.** `../../academia/article-v-entrenchment.md` holds the search, with every quotation read from the scanned text of the source rather than from a summary. The result is unfavourable to the quadrant the loophole needs, in a specific and structural way.

On scope, both readings have serious published defenders. Machen in 1910 states the functional reading directly, holding that a state could not be deprived of equal suffrage "merely by abolishing the Senate, or reducing it to a body merely advisory," and Marbury reaches indirect nullification in 1919. Orfield in 1942 takes the formal reading and calls the functional one "legal casuistry," arguing that "if the Senate were abolished, the equality of suffrage would not be disturbed, as each state would have no senators at all."

On self-entrenchment the field leaned against repealability. Orfield states the two-step in 1942 — the limitation "might be disregarded directly, or if not directly, indirectly by first repealing the clause and then depriving a state of its equal representation" — and declines to adopt it, reporting that "there are not many who assert that the ordinary amending body could abolish the equal suffrage clause."

**The structural point is that the two positions the loophole needs were held by opposite camps.** The authorities supplying the functional scope are the same ones treating the proviso as perpetual and beyond the ordinary amending power; Machen's argument depends on the clause "being perpetual" and "still in full force." The authority most willing to let the ordinary amending body operate takes the formal scope, on which the two-step is superfluous because the proviso is never engaged. This search found no pre-1947 authority asserting both halves. That is a result about a search over six law-review sources and one case, not a proof of absence, and the qualification matters because the combination could sit in a source not reached.

No court had decided either question before December 5, 1947. Rottschaefer's 1939 treatise, quoted in Orfield, records that no case had been found "in which the power to amend has been employed to directly or indirectly modify a constitutional provision expressly excepted from that power." The only judicial utterance touching the clause, in *Dodge v. Woolsey*, is dictum and Orfield treats it as error.

## What happened to the caveats afterwards

The two remarks appear in §3 of the thesis and are not carried forward.

They are absent from the thesis's own conclusion, which reads "Having successfully verified the validity of the argument." That is defensible on its own terms — *validity* is used in its ordinary logical sense, and a valid argument may rest on improbable premises — so this is weak evidence taken alone.

They do not appear in the conference paper at all. The words *unlikely*, *improbable*, *unnecessary*, and *consent* occur zero times in it. §2.1 restates the argument without qualification, and the conclusion reads "we have explored an argument on how to introduce a dictatorship in the USA without violating the rules laid out in the US Constitution."

That is worth recording and worth not overstating. The paper is thirteen pages, not four; an earlier draft of this file said four and was simply wrong. The ratification premise remains fully visible in the paper's own model, `sup rat amd2` included, so nothing was concealed, and the paper describes itself as "a mere case example" dealing with "one small part" of the Constitution. The accurate and much duller claim is that the conference paper does not repeat the thesis's practical objections. Claims of concealment, or of meaningful publication drift, are not supported by the sources and are withdrawn.

`verify.sh` section 5c pins each quotation above to the two PDFs, whose checksums section 5 verifies.

## The net addition

Two things, neither of which is a loophole.

A semantic independence result: in this transcription `amd2_sup_rat_t2` is non-redundant, and no proof of `Dictatorship_t3` survives its withdrawal by any route. That is strictly more than the dependency list a reader can already see in the published proof, and it is all that the ablation shows. It does not show the authors were wrong to leave ratification undecomposed; it shows that the theorem is conditional on the undecomposed premise, and that questions about coalition size and feasibility lie outside the model's reach rather than being answered by it.

**This result has since been subsumed and sharpened.** `inert-manoeuvre.md` proves `Dictatorship_t3` from an irredundant set of six axioms, of which `amd2_sup_rat_t2` is one — and shows further that `amd2_sup_rat_t2` is one of four axioms necessary to *every* sufficient support, so no proof of the theorem in this model can avoid it. Non-redundancy is the weakest of the three statements. That file also carries the more consequential finding: none of the six is an equal-suffrage, entrenchment, Senate, or step-one axiom, because the amendment repealing the entrenchment clause is extensionally equal to the negation of that clause, so its content arrives free with the stipulation that the forbidden amendment was proposed. Read it first. This one survives as the record of how the result was reached, and of eight overstatements corrected along the way.

A correction to the literature, in two parts of unequal strength. The thesis's second objection slides from "a majority of state legislatures" to "all states support," and that is a defect in the argument no matter how the underlying law is read. The stronger claim — that the two-step manoeuvre converts unanimity into three fourths and so does real work — holds in one quadrant of the two-by-two above and is stated conditionally.

Neither advances the search for a loophole. Both make the standing of the existing formal result more accurate, which is what `method/README.md` requires before any procedure is pointed at an open question.

## The minimum coalition

Thirty-six of forty-eight states, by whichever mode Congress directs, plus the congressional proposing stage. The congressional stage is separately shown to be soft: `search/quorum_cascade.py` drives it from 179 individuals to 4 and reports its own disqualification, since nothing in that cascade touches the thirty-six. The count of individual legislators or convention delegates behind those thirty-six states has not been computed and is the next measurement. It is mode-dependent, since Congress selects between legislatures and conventions.

## Falsifiers

A derivation of `⌊Dictatorship⌋t3` from `GodelCore` plus the two Article V axioms alone. This would show the withheld axiom was redundant after all, and would defeat the only informative row in the table.

A demonstration that `GodelCore.thy` plus `GodelConstitution.thy` is not the thesis model. `verify.sh` §5b now recovers the pre-split file from git and compares every labelled formula body character for character after comment-stripping and whitespace normalisation; all eighty-one match. That guards the split. It does not guard the original transcription against the printed thesis, which remains hand-checked.

A derivation, from the thesis model as it stands, of any proposition about how many states, legislators, or delegates the manoeuvre requires. This file asserts that such questions lie outside the model's expressive reach; the model contains no numeral and no state, but one such derivation would refute the assertion.

A pre-1947 authority establishing either that the proviso reaches only inequality of representation, or that it is self-entrenched against ordinary repeal. Either would move the case out of the upper-left quadrant and reduce the correction above to its unconditional half — the quantifier slide — alone.

A demonstration that the quantifier slide is not a slide: that "a majority of Congress and state legislatures" in the thesis's premise was meant to denote the ratifying supermajority, and that the following sentence's "all states" is a translational artifact rather than a step in the argument. This would defeat the one part of the correction currently stated unconditionally.

Either practical objection appearing in the conference paper, in any wording. Section 5c tests four keywords, which is a keyword test rather than a semantic one and would not catch a paraphrase.
