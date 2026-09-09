# Navier–Stokes, AI, and a transferable standard of evidence

**Result of this review, September 8, 2026:** the supplied 166-page paper is
byte-identical to OpenAI's public PDF and explicitly claims the forced
Navier–Stokes breakdown alternatives **C and D**. An official repository
provides accompanying Lean sources and a separate challenge
interface. This review read the complete paper text, including Sections 4–9
and Appendices A–C, but **did not independently validate all estimates, build
the Lean project, run Comparator, or verify a Clay prize decision**.

No named theorem or conjecture was independently attributed to **GPT-6 Astra
specifically** from the primary artifacts successfully examined. That is a
bounded source-verification gap, not evidence that no such result exists.
The mathematical artifacts and their model attribution are different claims.

## What the supplied paper claims

[OPENAI, *Finite Time Blowup for Navier–Stokes*][paper], Theorem 1.1, printed
page 1, states an existence result for **every fixed positive viscosity**.
There is a smooth force, compactly supported in space and time, and a solution
starting with **zero velocity** that is smooth before time one, has bounded
kinetic energy, and develops unbounded velocity as time approaches one.
Velocity and pressure have fixed compact spatial support before that time.

Defining the force as the momentum residual of a chosen velocity is easy;
making that force smooth through a singularity of the velocity is the hard
part. This is not merely a simulation that becomes numerically unstable.
The paper constructs fields and supplies estimates intended to establish an
exact existence theorem.

Lemma 10.5, printed pages 121–123, compares the constructed solution with any
smooth bounded-energy competitor having the same force and initial datum.
Theorem 1.1 uses that comparison to exclude a global smooth bounded-energy
competitor. Corollary 10.6, pages 125–126, rescales and periodizes the compact
construction, including the pressure.

[Fefferman's official Clay statement][clay], page 2, explicitly invites a
proof of one of four alternatives. C and D permit forcing satisfying their
smoothness and decay conditions. The appended erratum explicitly requires
periodic pressure. **Forcing alone is not a reason to dismiss C/D as outside
the stated problem.** The paper does not resolve the separate unforced
alternatives A and B.

A claimed proof, a locally rechecked proof, expert acceptance, and a prize
award are separate evidentiary stages. No award or nonaward is inferred here
from a failed search or an inaccessible announcement.

## How the construction is organized

The following is a reading of the published argument, not a new proof or a
claim that every estimate has been independently checked.

| Stage | Published mechanism | Where |
|---|---|---|
| Construct the background | Join a regular core to an exact exterior heat flow; match five radial integrals and enforce the stress-cone conditions | Theorem 4.6; Appendices A–C |
| Correct the background | Solve successive coefficient equations, then sum with shrinking cutoffs on potentials so incompressibility survives | Propositions 5.3, 5.5; Lemma 5.4 |
| Supply momentum flux | Separate pulse supports, solve their amplitude equations, and match the leading stress through positive covariance weights | Lemma 6.1; Propositions 7.2, 7.5 |
| Correct the full residual | Recompute the actual updated fields; correct nonzero harmonics, averaged stress, auxiliary means, and three compatibility defects while preserving two moments | Section 8.7; Proposition 9.6 |
| Complete the existence argument | Sum the infinite correction sequence, localize, extend the force smoothly, and exclude a competing global solution | Proposition 9.9; Section 10 |

The iteration is **not** a finite search that stops when a residual looks
small. Proposition 9.6 improves the residual exponent by one tenth per cycle.
Lemma 9.7 supplies a common domain for all finite stages, and Lemma 9.8 keeps
physical derivative losses independent of the stage. Lemma 5.4 then constructs
a locally finite cutoff sum and controls its residual by comparison with a
fixed finite stage. In particular, the separately retained flat remainders
are not simply summed without a convergence argument.

## What the formal artifacts establish here

The official [OpenAI repository][repo] was inspected at commit
`8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`.

The [reference file][reference] says it was adapted from Google DeepMind's
Formal Conjectures file at commit
`8bf45ed70d48b2b2a501de9c00b26bfa38c573ee`. It defines smooth initial data,
force regularity and decay, the equations, and the whole-space and periodic
solution conditions. Its C/D theorem slots contain intentional `sorry`
placeholders: these specify challenges, **not submitted proofs**.

The separate [solution interface][solution] imports proof adapters and exposes
the same two theorem names. It does not import the challenge module, and
includes `#print axioms` commands. The [manifest][manifest] enables Nanoda and
permits only `propext`, `Quot.sound`, and `Classical.choice`; it does not permit
`sorryAx`. The [Comparator instructions][comparator] specify the additional
tools and upstream commands.

These are concrete, inspectable arrangements for checking statement
correspondence and proof dependencies. They are more informative than merely
being told that a proof assistant was used. However, the reference is an
**adaptation**, not an untouched independently authored specification, and
inspection of a manifest is not execution of its checks. No claim is made
here that this checkout passed a local build or Comparator run.

The repository also advertises a separate unforced Euler result. Its paper
and proof were not independently reviewed in this investigation.

## What was verified about Astra

The paper has the corporate author **OPENAI** and does not describe the
generating model, agent architecture, or compute budget. Its existence cannot
by itself establish which particular model produced it.

The [Navier–Stokes announcement][announcement] was reachable as a titled
page, but its body was not obtained by direct retrieval. The [Astra launch
page][astra] yielded a partial body concerning cyber evaluations rather than
the mathematical results sought here; a separate direct fetch returned HTTP
403. Targeted searches for the reported earlier Astra mathematics results
did not recover a primary paper or proof repository with an exact producing-
system attribution that could be confirmed in this review.

Consequently, benchmark percentages, counts of purported open-problem
solutions, agent counts, runtime figures, and assertions about an internal
model's relationship to public Astra are not repeated as findings. None is
needed for the constitutional experiments below.

## What transfers to the constitutional investigation

**Fix the problem contract before searching.** The relevant mathematical
alternatives specify domains, regularity, forcing, and quantifiers. The
constitutional counterpart must specify its 1947 text, actors, transitions,
consent identities, and terminal predicate. Power concentration, removal of
executive elections, and unequal Senate suffrage are different targets.

**Preserve invariants by construction.** Taking curls of potentials preserves
incompressibility even when cutoffs are introduced. In the constitutional
model, a proposal does not change the constitution, unchanged fields persist,
and ratification is judged under the current rule rather than the rule the
amendment wishes to create. These are concrete transition invariants in
[the framed search](bounded-article-v-search.md).

**Recompute after every change.** Section 8.7 requires the full updated
velocity, including correction terms, in the next residual. The state-
admission experiment likewise recomputes both the supporting-state count and
the total-state denominator. The attendance audit compares vote costs under
one attendance convention, rather than mixing two favorable numbers.

**Keep dependency claims precise.** A proof that uses a component is not a
proof that no other construction can work without it. The
[causality audit](repair-causality-audit.md) distinguishes an entailment
dependency from causal necessity and tests contradictory hypotheses and
missing persistence constraints explicitly.

**Match the conclusion to its quantifiers.** A bounded SMT UNSAT result is
not unbounded constitutional impossibility. A complete finite-state
exploration closes only its declared graph. An existential lawful path does
not need to be the unique path, but a path under a disputed formal
interpretation is not yet an established legal witness.

**Separate checking layers.** A trusted kernel checks deductions from encoded
assumptions; a separately encoded comparison helps catch specification
mistakes. Neither decides an unresolved legal interpretation. Formal tools
can usefully explore several declared interpretations without pretending
to settle which one was legally correct in 1947.

## Reading and provenance record

All **8,656 lines** of the extracted paper text were read, covering the
complete 166-page document, all appendices, and references. Printed pages
1 and 15 were also rendered and read as images to inspect the principal
theorem and correction diagram. This coverage is a reading record, not a
certification of the analytic argument.

The supplied and official PDFs have SHA-256:

```text
0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f
```

The reference, solution interface, and manifest links below are pinned to the
inspected repository commit. Downloaded PDFs and page renders are research
artifacts outside the repository, not newly redistributed paper copies.

[paper]: https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf
[clay]: https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf
[repo]: https://github.com/openai/NavierStokesAndEuler/tree/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538
[reference]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/NavierStokes.lean
[solution]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/NavierStokes/ComparatorSolution.lean
[manifest]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/NavierStokes.json
[comparator]: https://github.com/openai/NavierStokesAndEuler/blob/8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538/ComparatorChallenges/README.md
[announcement]: https://openai.com/index/navier-stokes-solution/
[astra]: https://openai.com/index/gpt-6-astra/
