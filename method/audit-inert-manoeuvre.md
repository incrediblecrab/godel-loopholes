# Audit of inert-manoeuvre.md against the finding standard

Filed: August 30, 2026

`method/what-counts-as-a-finding.md` is the project's quality gate. It was written before any candidates existed, deliberately, so it could not be adjusted afterward to admit one we like. This audit checks whether `analysis/united-states-1947/inert-manoeuvre.md` satisfies, fails, or falls outside each clause of that standard.

The short answer: the standard does not cover this class of result. It was written for candidate paths through a constitution — sequences of legal operations, carried out by named actors, arriving at destruction. `inert-manoeuvre.md` is a result about an instrument: a measurement of what a published Isabelle/HOL formalization does and does not establish, obtained by axiom ablation. Nearly every clause of the standard is inapplicable to it, not because the result is deficient but because the standard was built for a different kind of object.

The file itself says this plainly in its opening lines: it is "a result about an instrument rather than about the Constitution" and "does not advance the search for a candidate path by a single step, and it is not offered as one." There is no overclaiming on this point. But the fact that the result correctly disclaims candidacy does not resolve the gap in `method/`. The standard is the only quality gate the project has, and this result passes through it unchecked — not because it cheats, but because the gate does not have a lane for it.

## Clause-by-clause audit

### Requirements: what every candidate must state

**1. "The text and the recension. Which document, which vantage, and which printing."**

Inapplicable. `inert-manoeuvre.md` does not examine a constitutional text. It examines a formalization: Zahoransky and Benzmüller's Isabelle/HOL theory, transcribed from the bachelor's thesis. The "document" is a `.thy` file and the "vantage" is the model's axiom set. The file does identify its source precisely — the thesis, the conference paper, and the specific Isabelle transcription — but none of that is a text-and-recension in the standard's sense. The standard demands a printing of a constitution; this result is about a proof assistant theory.

**2. "The path, as numbered steps. Each step is a legal operation with a citation to the clause that authorizes it."**

Inapplicable. There is no path. The result presents five machine-checked facts about logical dependencies among axioms. These facts are numbered and rigorous, but they are facts about what a formal theory entails, not steps an actor takes through a legal text. The authorizing "clauses" are Isabelle axioms, not constitutional provisions.

**3. "The legal status of each step, marked as settled, contested, or novel."**

Inapplicable. There are no legal steps to classify. The result does note where its own claims were corrected — three earlier drafts made false claims that were disproved — but that is intellectual honesty about the formal work, not the settled/contested/novel classification the standard demands of legal operations.

**4. "The minimum coalition. How many actors, holding which offices, are required."**

Inapplicable. No coalition is stated or statable. The result is about which axioms are necessary and sufficient for a theorem, not about which officeholders must act. The standard says "this single number does more to place a candidate than any amount of prose around it." The result has no such number because it is not a candidate.

**5. "The falsifier. What would have to be true for this to be wrong."**

Satisfied, with a caveat. `inert-manoeuvre.md` has a detailed falsifiers section listing five specific things that would defeat its claims: a missing `X omsp` axiom in the thesis, a transcription error in load-bearing definitions, a published theorem that fails under `amd1` deletion, a five-axiom support, and a reading of `amd1a`/`amd1b` on which they carry the transition. Each is concrete and checkable.

The caveat: these falsify claims about a formalization, not claims about a constitutional path. The standard's falsifier clause contemplates "a case, a clause, a historical instance where the path was available and did not work." The file's falsifiers are of the form "a fact about the Isabelle theory that would defeat this measurement." They are honest and rigorous falsifiers for the claim actually made, but they are not the kind the standard describes.

### Disqualifiers

**D1. "Any step breaks a rule. Then it is not this project's claim."**

Inapplicable. There are no steps to break rules. Interestingly, the result's central finding is *about* this question — it shows that the formalization does not prove that no rule was broken, because the entrenchment clause's removal is achieved by omission rather than by a derived legal operation. But that is a finding about the model, not a step the result itself takes.

**D2. "You cannot name the edit that closes it. If no change to the text would shut the path, the defect is not in the text."**

Inapplicable. There is no path to close. The result does identify what would repair the formalization — an `in_force` predicate, a separation of norm-standing from observance, or propagating the entrenchment clause and deriving `amd2_prop_t2` from preconditions — but these are edits to a formal model, not to a constitution.

**D3. "It requires only bad faith and not the text."**

Inapplicable. The result is about logical structure, not about actors.

**D4. "The minimum coalition is enormous."**

Inapplicable. No coalition is stated.

**D5. "It is unfalsifiable."**

Does not trigger. The result is clearly falsifiable; the falsifiers section is one of the strongest parts of the file. This disqualifier would apply only if it triggered, and it does not.

**D6. "It is already in the literature and uncited."**

Does not trigger. The underlying model is thoroughly cited. The novelty — the ablation measurements — appears genuinely new. The file explicitly credits the authors for disclosing the design choice ("Nothing here was concealed") and notes that both the thesis and the peer-reviewed paper discuss the relevant tradeoff. What is new is the measurement of the cost, and the file says so.

### Other clauses

**"A chain is as strong as its weakest step."**

Inapplicable. There is no chain of legal steps. The result does have a chain of formal claims, each building on the previous, and the file is careful about which links are kernel-certified proofs and which are Nitpick model-finder results. But the standard's clause is about compounding contested legal operations, which is not what is happening here.

**"Whose judgment decides that it is destruction."**

Inapplicable. The result makes no destruction judgment. It does not claim that anything the formalization proves constitutes destruction of the constitutional order. It claims that the formalization does not prove what its framing says it proves — that the entrenchment clause was *lawfully* removed — and that is a judgment about the adequacy of a formal model, not about what counts as destruction.

**"Null results are recorded in the same detail."**

Partially applicable, and worth discussing. `inert-manoeuvre.md` functions as something like a null result: it finds that a published formalization does not use Gödel's step one and therefore does not establish that step one is lawful. It is "a path that was explored and closed" in the sense that the formal route through Zahoransky-Benzmüller was explored and found to be less than it appeared. But the standard envisions this clause as applying to candidate paths through a constitution that were tried and failed. The file does record its findings in full detail, which is what the clause asks for, but the object being recorded is not the object the clause was built to cover.

## Verdict

### The gap is confirmed

The standard in `method/what-counts-as-a-finding.md` has no category for results about instruments. It was built for one kind of object — a candidate path through a constitution — and it covers that object thoroughly. Ten of its twelve substantive clauses (five requirements, five of six disqualifiers, and two interpretive rules) are inapplicable to `inert-manoeuvre.md`, not because the result is deficient but because the clauses address properties (steps, coalitions, legal status, editable text) that a result about a formalization does not have.

The gap has a specific shape:

1. **Results about instruments are ungraded.** The project uses formal tools — Isabelle/HOL, Nitpick, Z3, Python scripts — and produces results about those tools' outputs. These results are the only substantive content in the repository so far (the README says "No loophole has been found"). They have no quality standard. The finding standard governs candidates; the method README governs procedures; nothing governs the intermediate results that formal instruments produce.

2. **The standard demands a path, a coalition, and a destruction judgment.** An instrument result supplies none of these. It supplies axiom dependencies, consistency proofs, and measurements of what a formal theory does and does not entail. These are rigorous, machine-checked, and falsifiable, but they are a different kind of object entirely.

3. **The null-result clause is the closest fit and is not close enough.** It asks for a path that was explored and closed, with steps and the reason it closed. `inert-manoeuvre.md` is closer to a meta-result: it finds that someone else's formalization of a path does not establish what its framing implies. That is a valuable finding, but it is not a closed path.

### Does `inert-manoeuvre.md` overclaim?

No. The file is unusually disciplined about this. It opens by disclaiming candidacy. It records three claims from earlier drafts that were disproved and explains how. It marks the standing of each piece of evidence (kernel-certified proof vs. Nitpick diagnostic). It names its own transcription gap. The "Claims made here and later disproved" section in `README.md` lists eight corrections, several originating from this file, and keeps them visible on purpose.

One place warrants scrutiny but does not constitute overclaiming: the "What the formalization therefore establishes" section makes a judgment about the *legal argument* — that the gap is in the phrase "without violating" — which goes beyond what the formal measurements alone support. But the file immediately adds "This is a limitation of the formalization. It is not evidence that Gödel was wrong." That qualifier is adequate.

The title — "Gödel's step one forces a repeal event that no published result needs" — is accurate within the model. It could be misread as a claim about the constitutional argument itself, but the opening paragraph forecloses that reading. Titles are inherently compressed; this one does not overclaim relative to the body.

### Is the result grading its own homework?

In one narrow sense, yes: the file sets up the axiom-ablation experiments, runs them, and reports the results, and no external standard governs what counts as a valid ablation or a valid consistency probe. The harness (`verify.sh`) re-runs the experiments, and the falsifiers section specifies what would defeat the claims, but the choice of what to measure and what to report is unchecked by any methodological standard in `method/`.

This is not a criticism of the file's honesty — the self-corrections demonstrate that the author does not spare himself. It is a structural observation: the method folder has a gate for candidates and no gate for instrument results, so instrument results are self-governing by default.

### What a new standard would need to cover

This is the next agent's job, but the audit suggests the shape:

- **What the instrument result claims to establish**, stated precisely.
- **What the instrument is** — formalization, solver output, replication — and its relation to the constitutional text it models.
- **Reproducibility** — the command that re-runs it, and what "passing" looks like.
- **The correspondence claim** — the link between the formal statement and the legal or textual claim, which (as `formal-model-replication.md` notes) is "the one link in the chain no prover checks."
- **Falsifiers** specific to instrument results: transcription errors, vacuous experiments, consistency failures.
- **Disqualifiers** specific to instrument results: vacuous proofs in inconsistent theories, results that measure only their own stipulations.

`inert-manoeuvre.md` already satisfies most of these informally. A standard would make the requirements explicit and checkable by someone other than the author.
