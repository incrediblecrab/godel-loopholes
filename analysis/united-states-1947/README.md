# United States, 1947

This folder investigates what Gödel could have found in the United States constitutional order of 1947. No verified loophole or identification of his actual argument has been established. The comparative collapse folders supply historical control material, not certified examples of wholly lawful collapse; their evidentiary and legal limitations must be retained when using them.

Start with [the consolidated research report](research-report.md) for the
completed logical and quantitative results, corrections, reproduction commands,
and outstanding evidence gaps. The detailed reports below preserve the
individual experiments and their assumptions.

## Vantage

The snapshot is the United States as of December 5, 1947, the date of the hearing, and it holds five files in `corpus/united-states-1947/`.

Constitutional authority must come from norms effective by December 5, 1947. Later scholarship may analyze those norms, and later historical compilations may supply earlier data; neither can add a post-1947 power to the target system. The Twenty-second Amendment had been proposed in March 1947 but was not ratified until 1951 and is not part of the operative document. The baseline has forty-eight states and nominal chambers of ninety-six senators and four hundred thirty-five representatives. Calculations assume filled, chosen-and-sworn seats unless stated otherwise; state-admission experiments explicitly vary membership.

Case law decided before the vantage date is admissible, and two decisions matter enough to name here. *National Prohibition Cases*, 253 U.S. 350 (1920), fixed the base of Article V's two-thirds requirement. *Schneiderman v. United States*, 320 U.S. 118 (1943), described Article V as carrying no substantive limitation beyond the Senate proviso, in a naturalization case decided under the same attachment standard Gödel was examined under four years later. Both are recorded in `academia/naturalization-1947.md`.

## What is here

`literature-replication-map.md` connects the academic sources to the actual
experiments, distinguishes verified reading from metadata or secondary accounts,
and separates contemporary authorization from retrospective acceptance.

`ai-science-methods.md` reviews the complete supplied Navier–Stokes paper and
its official proof interfaces. It separates the published C/D claim from local
proof execution and prize status, and records the remaining Astra-attribution
gap. Its transferable practices guide the experiments below; it does not
claim that mathematical verification settles constitutional interpretation.

`threshold-arithmetic.md` runs the threshold-arithmetic enumeration over Article V. The 1920 holding uses members present, assuming a quorum. Under favorable minimum-quorum attendance and nominal full membership, 146 House and 33 Senate yes votes suffice; these are not attendance-independent thresholds.

It also records that the minimum-coalition argument this project treats as one of its own procedures was made to the Supreme Court by counsel in 1920, and lost. That is a direct hit on the novelty requirement in `method/what-counts-as-a-finding.md`, and it arrived before any candidate had been raised, which is the best possible time for it to arrive.

`silence-inventory.md` runs the silence inventory. It lists twelve fields the constitution leaves to ordinary legislation or to nobody at all, and identifies six in a connected group: the proposal threshold depends on attendance and quorum, quorum depends on membership, and each House judges its members' elections, returns, and qualifications under Article I, Section 5. The scope of those powers still requires legal interpretation. The inventory returns no candidate and records that Justice Rutledge grouped three of the same clauses in *Colegrove v. Green* in June 1946.

## The formal model

The three starting replication reports concern Zahoransky and Benzmüller's
Isabelle/HOL reconstruction, documented in the 2019 thesis and 2020 workshop
paper. Modern scholarship may be replicated, but any asserted correspondence
to the 1947 constitutional order must still respect the vantage rule.

`formal-model-replication.md` records the replication: the model reproduces, its axioms are consistent, and its three theorems carry information. It is the borrowed baseline, not a result of this project.

`inert-manoeuvre.md` records a central instrument finding. It is a result about the instrument, not about the Constitution, and it advances the search for a candidate path by zero steps. Its finding is that the model represents Gödel's step one properly — the amendment stripping Article V's entrenchment clause is an object, it is proposed, supported, and genuinely ratified — and that deleting all four axioms responsible costs no published result. Five things are machine-checked: `Dictatorship_t3` follows from six consistent axioms, none of them an equal-suffrage, entrenchment, Senate, or step-one axiom; four of those six are necessary to every possible proof; every published theorem *and* every intermediate lemma survives deleting step one, in a theory that is still consistent; the authors' own defence of their omission is sound; and the repealing amendment is extensionally equal to the negation of the entrenchment clause, so its content is already forced by the separate stipulation that the dictatorship amendment was proposed. The deletion is not free — it makes the ratification event `⌊is_rat amd1a⌋t2` independent, where the full theory entails it — but nothing published depends on that event. The limitation is disclosed by the authors in both venues, so what is new is the measurement and the diagnosis rather than the discovery.

`ratification-price.md` is the earlier and weaker version of the same finding, kept because it records four overstatements and how each was caught.

`search/axiom_sweep.py` generates the ablation theories from `isabelle/GodelCore.thy` and `isabelle/GodelConstitution.thy`, so the model is not transcribed twice for each experiment.

`step-one-repair.md` describes this project's separate repaired encoding.
`repair-causality-audit.md` corrects its interpretation: the first-step facts are
load-bearing for entailment, not proof of causal necessity. Sixteen new kernel
lemmas and seven new ordinary Nitpick counterexamples expose missing persistence
constraints and an already-contradictory hypothesis in the original rival-rule test.
These outcomes were independently rerun before publication.

`search/quorum_cascade.py` retains a separate arithmetic relaxation, not a
verified constitutional path. `attendance-consistency.md` corrects the old
267-versus-179 cost refutation in `quorum-cascade-null.md`: its two sides used
different attendance assumptions. The scalar inequality checked by
`search/cascade_domination.py` survives; the claimed strict cost domination does
not follow.

## Executable interpretation search

`bounded-article-v-search.md` extends the replication with a consent-aware finite
transition model, exhaustive graph search, an independently encoded bounded SMT
cross-check, and behavioral mutation controls. It makes the interpretation matrix
in `ratification-price.md` executable and distinguishes a satisfying endpoint
from a path reached by authorized changes. The exact scope and measured results
are in `search/article_v_results.json`. Its conditional model witnesses are not
new constitutional loopholes or evidence of what Gödel privately intended.

`state-admission-replication.md` tests a boundary the fixed-state model excludes:
Article IV can change the membership set counted by Article V. It reproduces
the conditional arithmetic of the Harvard Law Review's *Pack the Union* Note,
keeps the congressional gates in the calculation, and checks the changing
denominator against the Sixteenth Amendment's primary certification. The
paper's precise historical minimum remains underdetermined, and its
new-state voting assumptions are not converted into legal guarantees.

`quantitative-ratification.md` supplies source-verified 1940 Census bounds:
the smallest 36-state group contains 54,982,723 of 131,006,184 residents in the
48-state universe, or 41.9696%. Sorting and independent integer optimization
agree. These are residents of selected states, not voters, supporters, or the
number of ratifying legislators or delegates.

## What is not here yet

No verified candidate path. `power-inventory.md` has been run and identifies six
selected rows; its reported clause walk is not a complete persisted row-by-row
dataset. The reference graph, undefined-terms pass, and systematic parse
enumeration have not been completed as reproducible exhaustive searches.

The silence inventory was expected to be the most productive and was the enumeration the Italian control case was worked to make unavoidable. It was productive in the sense that it found the cluster, and unproductive in the sense that the cluster reaches only Congress and the federal courts and leaves state ratification entirely untouched. That is the same conclusion `threshold-arithmetic.md` reached from the opposite direction, which is mild evidence that the conclusion is right.

The later “statutes, read” section of `silence-inventory.md` records verification
of its identified statutory sources; the earlier blanket retrieval blockage is
outdated. This does not constitute a comprehensive search of all operative
statutes. The actual 1947 standing-rule texts remain incompletely verified, and
catalog leads are not a substitute for the operative rules.

No source reviewed here establishes Gödel's actual mechanism. The notebooks and
naturalization records discussed in `academia/naturalization-1947.md` are
archival leads, not proof that no relevant record exists or that nobody has
requested one. Reconstructing a possible vulnerability is a different question
from identifying what Gödel privately meant.
