# Gödel loopholes

**Research status: paused after a bounded research program. No verified constitutional loophole or identification of Gödel's actual argument.** Start with the [consolidated research report](analysis/united-states-1947/research-report.md) for the findings, assumptions, and reproduction commands.

Kurt Gödel proved that any consistent, effectively axiomatized formal system strong enough to do arithmetic contains true statements it cannot prove. In 1947 he studied the Constitution for his citizenship exam and, according to Morgenstern's later account, thought it permitted a path to dictatorship without anyone breaking a rule.

He took the exam on December 5, 1947, in Trenton, New Jersey. Einstein and Oskar Morgenstern came as his witnesses. His concern came up during the exam, but the examiner did not pursue it. Gödel swore the oath on April 2, 1948.

No source reviewed here establishes Gödel's argument. The principal eyewitness account used here is a [memo](https://mathshistory.st-andrews.ac.uk/Extras/Godel_naturalisation/) Morgenstern dictated on September 13, 1971, twenty-four years later, opening with the admission that he was working from memory and had not checked his diaries.

> He rather excitedly told me that in looking at the Constitution, to his distress he had found some inner contradictions and that he could show how in a perfectly legal manner it would be possible for somebody to become a dictator and set up a Fascist regime, never intended by those who drew up the Constitution.

Morgenstern does not say which part of the Constitution Gödel meant, and a few lines later he adds that he doubted Gödel was right. The phrase that defines this project's target is "in a perfectly legal manner." The reported claim concerns an attack that follows the rules, and a rule-following attack is the kind you cannot patch by enforcing the rules harder.

Austria comes up in the memo too. The examiner asked what sort of government Gödel had lived under, and Gödel answered that it was a republic whose constitution "was such that it finally was changed into a dictatorship." Then he said the same thing could happen here, and offered to prove it.

## Hypothesis

We test whether the constitutional order in force in 1947 permits a sequence of lawful actions that destroys democratic government. This remains a hypothesis, not a finding. Reading the constitutional text is a starting point; statutes, cases, and operative procedures also matter. Identifying what Gödel actually had in mind is a separate historical question.

The longer-term aim is a repeatable method for comparing constitutional systems, with each proposed path laid out so others can check it or knock it down. A candidate must meet the [finding standard](method/what-counts-as-a-finding.md): authorized steps, an explicit coalition, and a concrete falsifier. Merely exercising ordinary amendment power is not automatically a loophole.

For an introduction to the question without the jargon, see [eli5.md](eli5.md). The current results and limitations are below.

## Where this stands

The work produced reproducible conditional models, exact arithmetic, primary-data measurements, and corrections to earlier claims. It did not establish a complete lawful-collapse path, and it did not prove that every possible path is impossible.

We used **qualitative legal and historical research**, **quantitative analysis** of voting thresholds, changing membership, and population, and **formal logic** through Isabelle proofs, finite transition searches, and independent solver checks. These methods complement each other: mathematics computes consequences of a legal interpretation; it does not choose the legally correct interpretation.

The [literature and replication map](analysis/united-states-1947/literature-replication-map.md) distinguishes published arguments, reproduced results, primary-source checks, and material not yet read.

### Main insights

| Insight | What the work established |
|---|---|
| A theorem is not yet a lawful sequence. | The [repaired-model audit](analysis/united-states-1947/repair-causality-audit.md) found missing persistence constraints and a rival-rule test whose added hypothesis already contradicted its context. An axiom package being needed for an entailment does not make its events causally necessary. |
| Legal interpretation changes the model's answer. | The [framed Article V search](analysis/united-states-1947/bounded-article-v-search.md) gives different results under formal versus functional Senate suffrage, different repeal rules, and an implicit democracy floor. Reachability is conditional on those inputs, not a probability of constitutional collapse. |
| States, residents, supporters, and consent are different quantities. | [State admission](analysis/united-states-1947/state-admission-replication.md) changes the ratification denominator as well as the available ratifiers; future states cannot authorize their own creation. [Census bounds](analysis/united-states-1947/quantitative-ratification.md) measure residents of selected states, not the people who would support an amendment. Ratification is not automatically consent to losing equal Senate suffrage. |
| Coalition comparisons must use the same assumptions. | The [attendance audit](analysis/united-states-1947/attendance-consistency.md) withdrew a strict cost refutation that mixed attendance conventions. The scalar inequality was true; its coalition interpretation was not. Withdrawing that refutation does not establish a successful cascade. |
| Replication needs explicit version and domain boundaries. | The [AAMAS self-amendment replication](analysis/united-states-1947/self-amendment-replication.md) implemented the selected protocol and checked the theorem's predictions over declared finite preference domains. A six-voter counterexample refutes an unnumbered sentence, not the numbered theorem or Article V. |
| Historical controls are narrower than a successful backtest. | The [historical denominator control](analysis/united-states-1947/state-admission-replication.md) corroborates a changing state count. Neither that control nor the comparative collapse cases establish a wholly lawful route from the 1947 United States Constitution to dictatorship. |

The [AI-science and Navier-Stokes review](analysis/united-states-1947/ai-science-methods.md) informed the verification discipline, not a constitutional solution. It was not a replication of the PDE proof technique; full proof execution and Astra-specific producing-model attribution were not independently verified here.

### Original formal-model replication

The earlier result remains useful: Zahoransky and Benzmüller's published Isabelle/HOL reconstruction reproduces, and its ablations show exactly which assumptions support the selected conclusions:

- `Dictatorship_t3` follows from **6 of the model's 51 axioms**, and those six are consistent. Two are generic amendment-procedure rules, two are bare temporal-successor facts, and two stipulate that the dictatorship amendment is proposed and supported. None is an equal-suffrage, entrenchment, Senate, or step-one axiom.
- **4 of the 6** are necessary to every proof from this model's axiom pool, established by countermodels to the full theory minus each one. Six is irredundant but not proved minimum; the honest bound within that pool is 4 ≤ minimum ≤ 6.
- The four axioms encoding **the reconstruction's step one** — proposing and supporting the amendment that strips Article V's entrenchment clause — can be deleted and **every theorem and lemma published in the original still proves**, in a theory Nitpick confirms is still consistent. Two proof scripts break; none of those five propositions does.
- What the deletion demonstrably costs is entailment of `⌊is_rat amd1a⌋t2`, the ratification of the repeal itself, which the full theory entails and the reduced theory leaves **independent**. So step one is not free — it is just that no published result uses it.
- The reason: `amd1a` is extensionally equal to the negation of the entrenchment clause, provably without any of the model's non-definitional axioms. Its content is therefore already forced by the separate stipulation that the dictatorship amendment was proposed. The repeal event is represented and entailed; its normative effect is not what does the work.

The authors disclose the underlying design choice in both the thesis and the peer-reviewed paper. The contribution here is measuring which entailments depend on it and diagnosing why. It is not discovery of an undisclosed omission or proof that actual repeal is legally unnecessary. The full write-up is [inert-manoeuvre.md](analysis/united-states-1947/inert-manoeuvre.md); it concerns the original model, not the separate repaired model audited above.

### Reproduction and source ownership

Current scoped reproduction commands and numerical artifacts are linked from the [research report](analysis/united-states-1947/research-report.md). The earlier README recorded the legacy `./verify.sh` checkpoint as **103 checks, all passing**. That is a historical record, not a fresh validation of the expanded repository: the latest research pass did not rerun the full legacy harness, and it does not cover all the newer modules. The harness still reads its expected checkpoint count from this README.

[data/facts.json](data/facts.json) records ownership for its listed facts, not every result added by the newer research. `tools/facts.py` checks registered values against their owners and listed arithmetic relations; `tools/ssot_audit.py` reports repetitions of the values it probes. Newer experiments also have their own source-pinned data and result checks. These are consistency checks, not certification of legal interpretation or an exhaustive audit of every sentence. Prose may differ by audience; the underlying quantities and assumptions must not.

### When to reopen

The project is parked, not settled. Reopen it for **new archival or operative 1947 procedural evidence**, a **genuinely distinct legal mechanism**, or a **source-backed interpretation with a falsifiable test**. A new candidate should specify its starting coalition, current-rule authorization at every step, changes to membership and thresholds, and an independently checked witness or counterexample.

The [unfinished searches](analysis/united-states-1947/README.md#what-is-not-here-yet) include the reference graph, undefined-terms pass, and systematic parse enumeration. Their incompleteness prevents a claim of exhaustive coverage; it is not a reason to repeat an indefinite search over unchanged assumptions.

### Claims made here and later disproved

Eight earlier examples, kept visible on purpose. Later corrections are linked above and documented in their individual reports; this is not a count of every correction in the project.

1. That `sup_rat` could be attacked by contraposition — refuted by a countermodel.
2. That the formalism *cannot represent a constraint blocking an amendment* — refuted by building the blocked state (`axiom_sweep.py blocking`).
3. That the six axioms are *minimal* — they are irredundant, which is weaker.
4. That the model *cannot tell repeal from violation* — refuted by proving `amd1a = ❙¬omsp` and the event `⌊is_rat amd1a⌋t2`.
5. That deleting the reconstruction's step one *loses five lemmas* — it loses two proof scripts and none of those five propositions.
6. That deleting the reconstruction's step one therefore costs **nothing** — false, and refuted by an experiment I had already run. It costs `⌊is_rat amd1a⌋t2`, which becomes independent.
7. That `amd1a = ❙¬omsp` is a *term identity* — it is extensional equality; `by (rule refl)` fails on that goal.
8. That *none of the six axioms is an Article V axiom* — two of them are the generic amendment procedure. That was classification by symbol name.

One shipped experiment was also **vacuous** for a period: the ablation emitted axioms before the definition they mentioned, Isabelle generalized the free variable, and the reduced theory silently became inconsistent while still printing every theorem as proved. Adversarial review caught it, not the harness. Every ablation now carries a mandatory consistency probe.

Corrections at the level of a citation or a quotation are recorded in the file that owns the claim rather than repeated here. An example is [quorum-base.md](analysis/united-states-1947/quorum-base.md), which got the same ruling wrong twice in opposite directions before a photographic scan of the printing settled it.
