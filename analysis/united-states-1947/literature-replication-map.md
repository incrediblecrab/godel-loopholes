# Literature and replication map: United States 1947

**Updated September 9, 2026. Constitutional vantage: December 5, 1947.**

This is a selected source-to-experiment map, not a comprehensive literature
survey. Reading a paper, reproducing its formal calculation, and establishing
its legal interpretation are different achievements. The reading levels below
refer to what was actually examined, not what a title or secondary summary
suggests.

The [Morgenstern memorandum][morgenstern], dated September 13, 1971, records
Gödel's reported belief and expressly relies on recollection without consulting
notes or diaries. It does not give the missing argument. None of the sources
examined here establishes Gödel's actual mechanism. That bounded statement
does not establish the worldwide absence of a surviving record.

## 1. Zahoransky and Benzmüller: the reproduced formal instrument

**Source.** Valeria Zahoransky and Christoph Benzmüller, [*Modelling the US
Constitution to establish constitutional dictatorship*][zb], MIREL 2019,
published in CEUR Workshop Proceedings 2632 in 2020. The
[2019 bachelor's thesis][thesis] contains the longer treatment and source code.

**Publication status is verified, not inferred.** The
[proceedings preface][mirel-preface], page 2, states that submissions were
peer-reviewed by at least two Program Committee members. The page image was
read. The [volume index][mirel] lists this work among the accepted papers and
records publication on July 6, 2020. It is a peer-reviewed **workshop paper**;
that does not make its constitutional interpretation judicial authority.

**Read and reproduced.** The paper's narrative, including its limitation on
printed page 7, was read. The existing source transcription and replication
records are in [formal-model-replication.md](formal-model-replication.md).
The current run repeated `minimal` and `noamd1`: the original three target
theorems and five intermediate lemmas survive removal of the step-one axioms,
with consistency diagnostics. [inert-manoeuvre.md](inert-manoeuvre.md) gives
the precise instrument result and generator commands.

**Method.** Select legally relevant concepts, represent them in HOL, encode
them in Isabelle, and reason from the encoded assumptions. The authors
explicitly acknowledge that their desired repeal is represented partly by
omitting a subsequent `omsp` axiom rather than deriving a complete change of
the constitutional rule. The new ablation measurement is not discovery of an
undisclosed omission.

The paper has three substantive time stages **plus** the technical endpoint
`te`; it does not have a three-element time domain. Its abstract
`maint_suf` predicate is not an explicit domain of states with separate
deprivation and consent relations.

**Keep the models separate.** This project's `GodelNetAddCore/Full` repair is
not the published encoding. Its five added facts are load-bearing for
entailment, while its missing frames and contradictory clause-on hypothesis
in the Full-importing rival test are documented in
[repair-causality-audit.md](repair-causality-audit.md). The affected rival
test is not a meaningful comparison of alternative legal rules; this does
not make every theorem in the file vacuous or Full itself inconsistent.
Neither audit proves that classical HOL cannot encode self-amendment.

Use the actual reproduction commands in those reports, including the required
imported theories. A generic invocation with one arbitrary `X.thy` is not a
verified recipe for the whole dependency graph.

## 2. Pack the Union: the reproduced changing-membership calculation

**Source and reading.** The unsigned [*Pack the Union* Note][pack], 133
Harvard Law Review 1049-1070 (2020), was read in full, including footnotes.
Printed page 1060, footnote 94, was also inspected as an image. This is a
law-review Note; law-review publication is not, by itself, evidence of
external academic peer review.

**Method actually transferred.** New states change both sides of the Article V
fraction. If `N` is the original state count, `r` the original ratifiers, and
all `k` new states ratify, the ratification-only minimum is
`max(0, 3N - 4r)`. The implementation adds both congressional gates and
requires the original Congress to authorize admission.

[state-admission-replication.md](state-admission-replication.md) supplies exact
enumeration, independent optimization, boundary controls, and the primary
Sixteenth Amendment denominator check. The mechanism reproduces conditionally;
the Note's precise historical inputs behind **96** additional states remain
underdetermined.

The Note's objective is representation reform, not dictatorship. New-state
political support, geographic subdivision, congressional procedure, and
state-consent questions remain assumptions or separate legal inquiries.
The [Census bounds](quantitative-ratification.md) are a further computation
with primary population data, not an experiment attributed to this Note.

## 3. Abramowitz, Shapiro, and Talmon: replication pending

**Source.** Ben Abramowitz, Ehud Shapiro, and Nimrod Talmon, *How to Amend a
Constitution? Model, Axioms, and Supermajority Rules*, AAMAS 2021;
[preprint 2011.03111][aamas].

A separate worker is implementing a precisely specified protocol and numbered
result. Its deliverable has not yet completed parent verification and is not
counted as a successful replication here.

The required correspondence check includes electorate, preferences, threshold
inequalities, ties, old-rule authorization, and proposed-rule approval.
A single-electorate theorem must not silently become a theorem about bicameral,
multistage Article V.

## 4. Guerra-Pujol: conjecture, worked examples, and historical scope

### The 2013 conjecture

**Source.** F. E. Guerra-Pujol, [*Gödel's Loophole*][guerra2013], 41 Capital
University Law Review 637 (2013). This is a law-review article. Parent
verification covered the five-step argument on printed pages 654-665 and the
admission discussion on pages 670-672, rather than treating a search summary
as the paper.

The five-step argument classifies amendment provisions, treats Article V as
not protecting its own amendment procedure, and argues for downward amendment.
The worked example on page 662 replaces state ratification with a simple
Senate majority after a simple House majority proposes the amendment.
This is broader than the particular repeal-then-concentration sequence chosen
by the later Z&B model.

The taxonomy and its application to Article V are interpretive premises, not
facts established merely by the law of excluded middle. Step 5's universal
anti-entrenchment claim likewise does not relieve an implementation of checking
the first operation against the currently operative restriction.

The [framed search](bounded-article-v-search.md) tests several interpretations
and specified amendment effects. It does not implement every procedure in the
2013 paper: in particular, abolishing state ratification in favor of Senate
ratification is not the same operation as changing a state-count threshold.

The admission mechanism is also already discussed in Part IV.D, where the
author cites Mark Dominus's 2007 proposal and distinguishes admission,
congressional proposal, and ratification votes. The author's practical and
historical claims there were not all replicated. In particular, the present
Sixteenth Amendment control does not establish the article's separate analogy
to the Fourteenth Amendment.

### The 2024 Prequel

**Source.** Guerra-Pujol, [*Gödel's Loophole: A Prequel*][prequel], 30
Southwestern Journal of International Law 613 (2024), a law-review article.
The introductory case selection, footnote 17, and the opening Yugoslav
discussion were checked directly.

Its three principal cases are **Yugoslavia, Austria, and Romania**, stated on
page 614. Germany is not one of that trio. Footnote 17 lists several exclusion
criteria and examples, but does **not** explicitly name Germany; it should not
be cited as an express German exclusion.

The repository's separate historical review examined **Germany, Austria, and
Italy**, not the same set. Only Austria overlaps. Those reviews therefore
cannot be reported as a completed backtest of all three Prequel cases.
Germany's Enabling Act used constitutional-amendment procedure, with contested
and coercive adoption conditions.

The Prequel also discusses a prior extra-constitutional act receiving later
constitutional validation, notably on page 619. That is an important target
distinction: later validation does not by itself meet this repository's
requirement that every operation be lawful when performed. Neither the
historical narrative nor retrospective acceptance supplies a new Article V
authorization without a separate argument.

## 5. Suber: distinguish models of legality before claiming a paradox

**Sources and reading.** Peter Suber, *The Paradox of Self-Amendment*
(Peter Lang, 1990), has an [author-hosted online edition][suber-book].
The complete condensed essay, [*The Paradox of Self-Amendment in American
Constitutional Law*][suber-essay], Stanford Literature Review 7(1-2), 53-78
(1990), was read, including all notes. The book's online contents were
inspected; the entire book and its empirical appendix were not independently
audited.

**Argument.** The essay distinguishes an **inference model**, in which a new
rule is deduced from the authorizing old rule and enactment facts, from a
**procedural model** and Suber's **direct acceptance model**. Direct acceptance
can authorize rules through social practice rather than solely through a
hierarchy of prior rules.

Suber argues that legal self-amendment can be valid despite a logical
objection. He does **not** establish that every constitutional alteration is
contradictory, that every contradiction is harmless, or that a logical
dissolution is impossible. He expressly leaves the latter possibility open;
notes 2 and 7 discuss temporally indexed deontic logic while distinguishing
it from satisfaction of the inference model's particular requirements.

The essay's first solution tolerates a contradiction in genuine self-amendment;
its second locates the successor rule's authority elsewhere, avoiding strict
self-amendment. These must not be collapsed into one universal theorem.

**Empirical claim, not our replication.** Suber reports self-amendment in
47 of 50 states and in every written-constitution country he investigated,
while explicitly saying that the international inquiry was not systematic.
Those are the author's claims. The underlying constitutional episodes have
not been independently recounted or restricted to a 1947 universe here.

**What is already located.** The book's contents explicitly include
[self-disentrenchment, Section 9.C][suber-disentrenchment],
[the see-saw method, Section 13][suber-seesaw], and
[Nomic, a rule-changing game, Appendix 3][nomic]. They are concrete further
reading or replication targets, not unknown topics inferred from the title.
No Nomic or see-saw execution is claimed in the present results.

**Boundary for this project.** Direct acceptance can, in Suber's account,
validate a change after procedural violations. That is a different model from
the current search's pre-state authorization invariant. Treating acceptance
as a new transition would require an explicit, evidenced rule and a declared
change of research target, not a silent success-shaped exception.

## 6. The Ross debate: verified records, unread primary arguments

The following bibliographic records were independently checked against
publisher-deposited Crossref metadata. Full texts were not obtained in this
review; Suber's or Oza's characterizations remain secondary evidence.

| Work | Verified citation and link |
|---|---|
| Alf Ross, *On Self-Reference and a Puzzle in Constitutional Law* | Mind 78(309), 1-24 (1969), [DOI](https://doi.org/10.1093/mind/LXXVIII.309.1) |
| J. Raz, *Professor A. Ross and Some Legal Puzzles* | Mind 81(323), 415-421 (1972), [DOI](https://doi.org/10.1093/mind/LXXXI.323.415) |
| Norbert Hoerster, *On Alf Ross's Alleged Puzzle in Constitutional Law* | Mind 81(323), 422-426 (1972), [DOI](https://doi.org/10.1093/mind/LXXXI.323.422) |

The Raz record directly corrects the earlier bibliography's claim that he
published no direct reply. His substantive position is not inferred from the
title. Suber's note 4 also identifies Hart's *Self-Referring Laws* (1964);
that text was not independently read here.

These papers should not be replaced by an invented proof recipe or by
attributing the same view to Hart and Ross without qualification.

## 7. Legal interpretation and comparative design: limits of current reading

**Orfield and the pre-1947 dispute.** Lester B. Orfield, *The Amending of the
Federal Constitution* (1942), is available as an
[original-edition scan][orfield]. The existing
[entrenchment note](../../academia/article-v-entrenchment.md) records passages
on pages 84-99 and 157-158, alongside Machen, Marbury, and Dodd. This map uses
that prior research record; it does not claim a fresh full-book or page-image
audit. Their disagreement supplies rival interpretations, not a judicial
resolution of the two-step. Orfield's description of a prevailing view is
scholarly assessment, not a holding.

The related [Blewett Lee article][lee], 16 Virginia Law Review 364 (1930),
remains unread here. Its title and Orfield's citation do not determine which
interpretation Lee defended. No quotation's punctuation should be corrected
from an OCR layer instead of the page image.

**Landau.** David Landau, [*Abusive Constitutionalism*][landau], 47 U.C. Davis
Law Review 189 (2013). Opening pages 189-193 and the contents were checked;
this is not a full-paper replication. They expressly discuss constitutional
amendment and replacement, not exclusively ordinary legislation. Page 192
already discusses a Japanese proposal to lower an amendment threshold; it is
reported as a proposal, not a completed reform. Page 193 introduces selective
rigidity. No numerical risk scale or statistical correlation was reproduced,
and an Article V proposing convention is not assumed equivalent to an
unconstrained replacement assembly.

**Oza.** Manish Oza, [*Can We Legally Revise the Highest Legal Rule?*][oza],
Legal Theory 31(3), 270-291 (2025), DOI
`10.1017/S135232522510075X`. The title page, abstract, and opening discussion
on pages 270-272 were checked; the complete article was not read. The abstract
argues that internal legal reasons can support revision of a system's highest
rule. That does not supply an implemented voting protocol, a test of
opportunistic motives, or a demonstrated rule of American law in 1947.

**Roznai.** The [linked resource][roznai] is Yaniv Roznai's *Unconstitutional
Constitutional Amendments: A Study of the Nature and Limits of Constitutional
Amendment Powers*, a London School of Economics PhD thesis, February 2014.
The title page was directly checked; the body was not read for this review.
It is not the 2017 published book. No additional implicit 1947 amendment
restriction is derived from an unread thesis. Article V's express Senate
proviso must not disappear from an international comparison.

## What follows from this map

The directly reproduced instruments are the original Isabelle experiment and
the parameterized state-admission calculation; the AAMAS protocol remains
under verification. The framed search, Census bounds, repaired-model audit,
and attendance correction are separate extensions or diagnostics.

The unresolved tasks are specific: obtain and read the primary Ross/Raz/
Hoerster and Lee texts; finish the assigned protocol replication; and acquire
the operative 1947 parliamentary evidence needed for stronger procedural
claims. Additional source reading may change legal assumptions. Re-running a
conditional graph cannot settle them.

### Source fingerprints

The downloaded originals remain outside the checkout. These SHA-256 values
identify the files used for the primary checks, not the extent of reading.

| Source | SHA-256 |
|---|---|
| Z&B paper | `bff63e5d9818f64a7399326667f1a2acad38ee5ffd7f6102420e2badf200a79a` |
| MIREL preface | `3aba6f9a0ee47dad471df8571c33da878b60ab2b4e39399650901df9d2e9f8ee` |
| Guerra-Pujol 2013 | `5ba75d06e27a4ead36de084a8d88ae99bd1c77bde2b29b3d89de4ea15cad54f3` |
| Guerra-Pujol 2024 | `d7b28d299031058d3c47b9ac946e43bf91c5c0e64bfbe86bd93403825361ca3d` |
| Suber essay HTML | `ebff54fa1e4412f2038afb97bc3db382c16e98c3d9278b17651d77e792397df9` |
| Landau | `eadfdfa91dbf98701450859bceb40979283e196ab21ef0288099834c59d83aee` |
| Oza | `ba6e8efd5dd56c701a9f66cba2765c01d72e76b7e8c3de514c94c880652dbebc` |
| Roznai thesis | `1fe48ad8ca32c1dc62b68979617b8abe5ee7c4e1dccda1817565865b6776b222` |

[morgenstern]: https://mathshistory.st-andrews.ac.uk/Extras/Godel_naturalisation/
[zb]: https://ceur-ws.org/Vol-2632/MIREL-19_paper_1.pdf
[thesis]: https://www.mi.fu-berlin.de/inf/groups/ag-ki/Theses/Completed-theses/Bachelor-theses/2019/Zahoransky/BA-Zahoransky.pdf
[mirel]: https://ceur-ws.org/Vol-2632/
[mirel-preface]: https://ceur-ws.org/Vol-2632/mirel_2019_preface.pdf
[pack]: https://harvardlawreview.org/print/vol-133/pack-the-union-a-proposal-to-admit-new-states-for-the-purpose-of-amending-the-constitution-to-ensure-equal-representation/
[aamas]: https://arxiv.org/abs/2011.03111
[guerra2013]: https://i2i.org/wp-content/uploads/Guerra-Pujol-Godel.pdf
[prequel]: https://www.swlaw.edu/sites/default/files/2025-01/13%20-%20Guerra.pdf
[suber-book]: https://legacy.earlham.edu/~peters/writing/psa/index.htm
[suber-essay]: https://legacy.earlham.edu/~peters/writing/psaessay.htm
[suber-disentrenchment]: https://legacy.earlham.edu/~peters/writing/psa/sec09.htm#C
[suber-seesaw]: https://legacy.earlham.edu/~peters/writing/psa/sec13.htm
[nomic]: https://legacy.earlham.edu/~peters/writing/nomic.htm
[orfield]: https://archive.org/details/in.ernet.dli.2015.505449
[lee]: https://www.jstor.org/stable/1065399
[landau]: https://lawreview.law.ucdavis.edu/sites/g/files/dgvnsk15026/files/media/documents/47-1_Landau.pdf
[oza]: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B4A6B1267807410343A9395021586191/S135232522510075Xa.pdf/can-we-legally-revise-the-highest-legal-rule.pdf
[roznai]: https://constitutionalist.com.ua/wp-content/uploads/2022/01/Roznai_Unconstitutional-constitutional-amendments.pdf
