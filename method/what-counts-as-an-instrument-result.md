# What counts as an instrument result

This file exists because the sibling standard, `what-counts-as-a-finding.md`, covers candidate paths through constitutions and nothing else. Of its twelve substantive clauses, ten are inapplicable to a result about a formal model — they demand numbered steps with authorizing clauses, a minimum coalition, per-step legal status, and a judgment about destruction, none of which a measurement of what a proof assistant does and does not establish can supply. `audit-inert-manoeuvre.md` confirmed the gap clause by clause.

The gap matters now because instrument results are this project's only substantive content. The README says "No loophole has been found." Everything below that sentence — axiom-dependency measurements, consistency probes, ablation experiments — is instrument work, and until this file existed it was self-governing. The author picked the measurements, ran them, reported them, and no written standard in `method/` told anyone else what to check or what to reject. Honesty is visible in the self-corrections, but honesty is not a gate. Without a criterion fixed in advance, nobody can audit a result against anything except the author's own choices.

Every clause below codifies a practice this project already follows. The reason to write it down is that a practice kept in one person's head is not auditable, and auditability is the whole point. One caveat belongs in the text rather than in a footnote, because the file timestamps make it checkable: this standard was written after `step-one-repair.md` was already on disk, by a separate process that had no sight of it. So the clauses were not adjusted to fit that result — but neither did they gate it in advance, which is what the sibling standard managed and this one did not. `step-one-repair.md` is accordingly the first result this standard is applied to, not the last one it was derived from, and it is being audited against these clauses rather than presumed to satisfy them.

## What an instrument result is

An instrument result is a claim about what a formal tool — a proof assistant, a model finder, a solver, a script — establishes, refutes, or leaves open about a stated input. It is not a candidate path through a constitution and is not governed by the finding standard. It may bear on a candidate path, but the bearing is the author's assertion, not the tool's output, and the gap between them is the site of the most dangerous errors.

The category has a boundary and the boundary is the tool. If the claim could be stated and defended without running anything, it is analysis, not an instrument result, and it belongs under `analysis/` without this standard's overhead. If it can only be stated because something was run, it falls here.

## What every instrument result must state

**What it claims to establish, and where those claims stop.** An instrument result that does not say where its claims stop invites the reader to extend them. The failure this guards against is overclaiming, and the defence is a scope statement written as a boundary rather than a summary. "The formalization does not prove that the entrenchment clause was lawfully removed" is a boundary. "The model has some issues" is not.

**What was run, on what version, and what counted as agreement.** Reproducing a published result is itself a claim, and stating that claim requires three things: the command a third party would run, the version of every tool in the chain, and the criterion for agreement. A reproduction that reports "all theorems proved" has not stated its criterion — it has reported a log line.

Agreement means: every labelled proposition in the source was discharged by the same proof method or an explicitly noted substitute, on the stated tool version, and any deviation is named and explained. `formal-model-replication.md` records a deviation — renamed bold-face connectives to avoid HOL built-in collisions — and flags it as the most likely site of a silent divergence rather than burying it. That is the model.

Completeness runs in both directions. Every identifier in the source must appear in the reproduction, and every identifier in the reproduction must appear in the source. A result that checks in only one direction has not controlled for additions or deletions.

**What an ablation controls for.** Deleting an axiom and observing that a theorem still proves is evidence only if the reduced theory is still doing work — that is, the surviving axioms are not trivially satisfying the goal for a reason unrelated to the question. The control is a consistency check on the reduced theory and a check that the surviving axioms still carry content bearing on the target. A sufficiency proof is weaker than it appears if the sufficient set includes stipulations that, once unfolded, restate the conclusion; `inert-manoeuvre.md` addresses this directly, noting that the six axioms include `amd2_prop_t2` and that unfolding `amd2_def` puts the separation of powers right there.

**Every ablation carries a consistency probe.** This is the most important clause in this file and it is not hypothetical. The `noamd1` experiment in this repository was vacuous for a period. The generator rebuilt all axioms into one block placed before the `amd2` definition, leaving `amd2` as a free variable. Isabelle generalized it. Every proposition became proposed and supported at `t2`. The theory went inconsistent. All three theorems still printed as proved. The result looked correct in every log and was worth nothing.

Adversarial review caught it, not the harness.

An inconsistent theory proves every formula, including every formula you were hoping to see. That makes inconsistency the one failure mode an instrument result cannot survive — it does not weaken the result, it annihilates it. Every ablation must report a consistency probe on the reduced theory: at minimum, a model-finder search for a model of the surviving axioms, and an attempt to derive `False`. Both outcomes are reported. A probe that was run and found nothing is still reported, because a missing report and a silent omission look identical from the outside. The rule is that the probe's outcome is in the file, not that the outcome is favourable.

**Model-finder output is labelled as diagnostic, not proof.** A Nitpick countermodel is evidence about one model, not a theorem about all models. It is strong evidence — it is a concrete witness — and it is not the same kind of object as an Isabelle kernel proof. Every file reporting a model-finder result says which kind of evidence it is: kernel-certified proof or model-finder diagnostic. The "Standing of the evidence" section in `inert-manoeuvre.md` does this and is the template.

**A timeout is not a negative answer.** A model finder or solver that runs out of time has found nothing. Reporting "no countermodel found" as though it were "no countermodel exists" manufactures a result from the absence of one. This project made the error twice. First: the consistency lemmas in the harness were written without an explicit timeout, and under load the model finder gave up, and the harness read the absence of a countermodel as evidence of inconsistency. Second: a Kodkodi malformed-output error was classified the same way because the detector had been written from one observed failure mode and did not generalize.

Outcomes are three-valued: confirmed, refuted, and inconclusive. Inconclusive means the tool returned no answer and is not a pass. The distinction between "the search succeeded and found nothing" and "the search did not complete" is load-bearing and must be stated. `verify.sh` enforces this as PASS / FAIL / INCONCLUSIVE. The rule needed widening once, which is itself evidence that the two-valued error is a standing temptation rather than a one-time mistake.

**The correspondence between the formal statement and the claim attached to it.** This is the gap no tool checks. A verified result is only as good as the match between the formula and the English sentence labelling it, and that correspondence is the one link in the chain no prover inspects.

The harness produced the clearest illustration. Z3 printed a House quorum of 219 where the hand derivation gave 218. The solver was right and the label was wrong: the encoding minimized `yes` rather than `present`, so 219 was an arbitrary witness among the models achieving 146 yes-votes, and minimizing `present` gives 218. Nothing was unsound. The formula answered exactly what had been written, and the English sentence attached to the output claimed something the formula did not say.

An instrument result must state what the formal claim says and what the English-language claim says, separately, so that a reader can inspect the correspondence rather than assume it.

## Disqualifiers

**It cannot be re-run by a third party from a tracked source.** A result that depends on files not in the repository, tool versions not recorded, or steps not written down is not reproducible and cannot be audited. The command that re-runs it appears in the file. The input files are tracked or their checksums are recorded. The tool version is stated. A reader who clones the repository and runs the command either gets the same answer or has found a bug.

**Its test reads its expected value from the same source as the code under test.** A check that loads the axiom set it is checking and asserts that the axiom set is consistent has verified only that the check runs, not that the theory is consistent. The test must derive its expectation from a source independent of the artefact it tests. This is a failure of separation, not of honesty, and it is the easiest to commit accidentally.

**An ablation is presented without a consistency probe.** After the vacuous-experiment incident, this is a bright line. An ablation result reported without a consistency check on the reduced theory is not admitted, regardless of what the theorems say. The probe may have been run and found the theory consistent. The probe may have been run and found nothing. Either is fine. It may not have been omitted.

**A result is derived from an inconsistent theory.** This follows from the previous clause but is stated separately because it is the only disqualifier that is absolute. An inconsistent theory proves everything. Nothing derived from it is evidence of anything. If a consistency probe discovers inconsistency, the result is withdrawn, not qualified.

**Timeouts or tool failures are reported as negative answers.** A search that did not complete is not a search that found nothing. A result that treats an inconclusive outcome as a refutation is disqualified on that claim. The result may stand on its other claims if those are independently supported.

**A result whose scope has been silently narrowed after a disproof.** A claim that was made, disproved, and then quietly dropped is worse than a claim never made. It conceals that the inquiry reached a dead end, and it makes the surviving claims look like the only ones that were tried. The retraction must be visible in the file, not only in the git diff.

## Disproved claims stay visible

This is a standing obligation, not a clause to be satisfied once. An instrument result that quietly drops a retracted claim is not auditable. The record of what was tried and failed is evidence about the inquiry's coverage — it tells a reader which alternatives were explored and closed.

This project keeps a public list of claims it made and later broke, in the README, and treats that list as among the most persuasive things it has. The same practice applies at the file level. `inert-manoeuvre.md` records three claims from earlier drafts that were disproved and explains how each was caught. A file that has never been wrong about anything is either very short or not being honest about its history.

The mechanism is in the file, not in the git history. A reader should not have to diff commits to discover that a claim was retracted. The retraction, the reason, and the replacement appear in the text alongside the surviving claims, because that is where they do their work.

## Null instrument results

An experiment that was run and produced no finding is written up with its setup, the outcome, and why it closed. The same rule applies here as in the finding standard: the closed experiments are how a reader can tell that the open claims were not simply the first thing tried.
