# The formal model of the dictatorship argument

Someone has already run Guerra-Pujol's argument through a proof assistant. Zahoransky and Benzmüller encode the separation of powers in Articles I through III and the amendment procedure of Article V in classical higher-order logic, using Benzmüller's shallow semantic embedding, and walk the two-step sequence across three time points. The full sources are in the bachelor's thesis rather than the conference paper; both are cited in `academia/godel-loophole.md`.

This file records what happened when we re-derived that model here, and what it turns out to establish. The theory is in `isabelle/`, and `verify.sh` at the repository root re-runs everything below on demand.

The reason to do this before anything else on the formal route is stated in `method/README.md`: no procedure gets pointed at an open question until it has rediscovered a solved one. That rule is usually read as a constraint on our own procedures. It binds harder on borrowed ones, because a published result carries an implicit claim that the machinery works, and we cannot inspect the machinery from the citation. If the only existing formalization of this argument did not reproduce, our position relative to the literature would be guesswork.

## What reproduces

`isabelle/GodelConstitution.thy` is the model, transcribed by hand from the thesis. It compiles clean against Isabelle2025-2 and discharges thirty theorems, among them the three that carry the argument: `noDictatorship_t1`, no dictatorship under the Constitution as it stood; `noDictatorship_t2`, none after Article V is amended; and `Dictatorship_t3`, dictatorship reached with no step breaking a rule.

Compiling is not the same as reproducing, and the distance between them is the point. An inconsistent axiom set proves every formula, so a theory can discharge `Dictatorship_t3` while carrying no information at all. This is not a hypothetical worry about this particular theory: the thesis includes a smoke-test theory that is *deliberately* inconsistent and proves `False` on purpose, and our harness confirms it still does. Anyone reading `Dictatorship_t3` off a successful build without checking consistency has learned nothing.

So the result was tested three further ways. Nitpick was asked to satisfy the axiom set, and found a model. It was asked to refute `False`, and found a countermodel, so the axioms do not entail everything. Then it was asked for countermodels to the duals of all three targets — `Dictatorship⌋t1`, `Dictatorship⌋t2`, `¬Dictatorship⌋t3` — and found all three. Countermodels are semantic rather than tactical, so this is a stronger statement than observing that some proof attempt failed: it shows no proof can exist. The three theorems carry information, and the dictatorship result is not an artifact of a broken axiom set.

Transcription fidelity was checked in both directions against the thesis. All 110 identifiers in our theory appear in the source. Of 67 labelled formulas in the source, 65 appear in ours; the two that do not are `elections_2yearCycle`, an integer-valued time representation the thesis introduces only to reject as making Isabelle's tools "more or less unusable," and a false positive on the English word *proposition*. No axiom was omitted. One deviation is deliberate: the thesis overloads the bold-face connectives directly and we renamed them to avoid colliding with HOL built-ins. That changes notation only, but it is the most likely site of a silent divergence, so it is flagged rather than buried.

## What it actually establishes, which is less than it appears

The amendment of Article V is not performed anywhere in the model. It is implemented by *omitting* the axiom `⌊X omsp⌋t1`. The step from the pre-amendment state to the post-amendment state is therefore assumed rather than derived, and the authors concede this and call it unavoidable in their framework.

Read precisely, what the formalization proves is a conditional: *if* Article V can be amended in the way Guerra-Pujol describes, the rest follows by lawful steps. The antecedent is the contested part, and it sits outside the model. Worse for the argument's reach, the quantity that binds it is absent entirely — their model has no representation of ratification by the states, and `threshold-arithmetic.md` in this folder is about exactly that number. At 48 states, the requirement is 36. A model that omits the constraint cannot report that the constraint is what stops you.

They also report that neither of their two candidate formalizations of the amendment is adequate. One demands a witness into existence and the other collapses into a tautology, and they conclude that "there is no optimal solution for the presented framework." That is a negative result, and it is more interesting than the positive one. It is the closest thing in the literature to a measurement of how hard it is to state the self-amendment candidate formally at all, and it should be read alongside Lawsky's argument in `academia/formal-methods.md` that classical logic is the wrong setting for defeasible legal reasoning.

## Why this model cannot find what we are looking for

The limitation is structural rather than a matter of effort, and `method/attack-surfaces.md` predicts it. Their model contains constitutional text and nothing else.

Under the Class 1/2/3 partition, such a model cannot see Austria, which left the constitution through Article 150 into an unrepealed wartime statute from 1917, and it cannot see Italy, whose Statuto was never amended while the state was dismantled around it. Two of the three collapses in our standing test set are invisible to it in principle. That is not a criticism of the paper, which scopes itself to a case example and says so. It is the specification for what a successor has to do: the node set has to extend past the constitutional text to the statutes standing beside it and the chamber rules operating inside it.

It also converts a gap in our archive into a gap in the model. The missing 1947 House and Senate rules, noted in `silence-inventory.md`, are not merely an inconvenient hole in the record — under a model that only reads constitutional text, they are not even addressable.

## A caution the tooling produced

While confirming the thresholds in `threshold-arithmetic.md`, Z3 printed a House quorum of 219 where the hand derivation gives 218.

The solver was right and the label was wrong. The encoding minimized `yes` rather than `present`, so 219 was an arbitrary witness among the models achieving 146 yes votes; minimizing `present` gives 218. Nothing was unsound at any point. The formula answered exactly what had been written, and the English sentence attached to the output claimed something the formula did not say.

This is the failure mode that formal tools invite rather than prevent, and it belongs in the same file as a successful machine-checked replication. A verified result is only as good as the correspondence between the formula and the sentence, and that correspondence is the one link in the chain no prover checks.
