# Formal and computational methods

This is the part of the project most likely to waste a year. The literature here divides cleanly into work that is mature and useful now, work that is real but has never been tried at constitutional scale, and work that sounds transformative and is not yet anything. The sections below are ordered by that distinction rather than by ambition.

The headline finding has to be stated carefully, because the obvious version of it is wrong. **No one has formalized a complete constitution in a machine-checkable logic.** Most attempts handle individual statutory provisions, almost always tax or benefits rules, which are algorithms wearing legal clothing; constitutional provisions allocate authority rather than compute an amount, and nothing shows the tooling crosses that gap at scale.

But the specific argument this project exists to test has already been formalized, in Isabelle/HOL, with published code. Zahoransky and Benzmüller did it in 2019, and their work is treated in full below. This project is therefore not starting from nothing on its central question, and any claim that it is would be false. What remains unbuilt is everything around that one argument.

## What is usable now

**The Multilingual Corpus of World's Constitutions.** Mo El-Haj & Saad Ezzini, OSACT 6 at LREC-COLING 2024, pages 57 to 66. https://aclanthology.org/2024.osact-1.7/ and https://github.com/ArabicNLP-UK/MCWC

The best starting corpus, and the license is the reason: the CSV core is CC0, which is public domain with no attribution requirement. It carries 223 constitutions from 191 countries, sentence-aligned across English, Arabic and Spanish, with roughly 52,000 English-Arabic and 49,000 English-Spanish aligned pairs, and it includes historical texts rather than only those in force. Sentence alignment is the feature that matters, because it makes translation divergence measurable rather than anecdotal — which is the problem this project already hit with the Weimar text.

**The Comparative Constitutions Project.** Zachary Elkins, Tom Ginsburg & James Melton. https://comparativeconstitutionsproject.org and https://comparativeconstitutionsproject.org/download-data/

Two datasets matter. The Chronology of Constitutional Events, version 6.0, tracks constitutional change worldwide since 1789. Characteristics of National Constitutions, version 5.0, encodes several hundred structured features per constitution — executive structure, amendment procedure, rights provisions — across more than 200 countries, in CSV and Stata. The texts themselves are largely under copyright and only currently active constitutions are open through Constitute; the coded features are the asset. Constitute itself is a browsing interface with no documented bulk export, so it is for reading, not for pipelines.

**Elkins, Ginsburg & Melton, "The Endurance of National Constitutions"** (Cambridge, 2009). Book; replication data free through the CCP download page.

The nearest existing thing to what this project proposes: hazard models over every national constitution since 1789, asking which design features predict death. Median constitutional lifespan comes out around nineteen years. The variables coded as flexibility and specificity are, under another name, an attempt to measure how much surface a constitution offers, which makes this the natural baseline to beat or to build on.

**Donald Lutz, "Toward a Theory of Constitutional Amendment,"** 88 American Political Science Review 355 (1994). Paywalled through JSTOR.

The rigidity index: assign a probability to each procedural hurdle an amendment must clear, multiply them, and get a single number for how hard a constitution is to change. It is computable directly from text and from CCP features, and it is the obvious first-pass screen for vulnerability to lawful self-modification. Read it alongside Astrid Lorenz, "How to Measure Constitutional Rigidity," 17 Journal of Theoretical Politics 339 (2005), paywalled, which compares four rival operationalizations and finds they disagree — so the choice of index is itself a finding rather than a detail.

**David Law & Mila Versteeg, "The Declining Influence of the United States Constitution,"** 87 New York University Law Review (2012). Free: https://nyulawreview.org/issues/volume-87-number-3/the-declining-influence-of-the-united-states-constitution/

A working method for measuring constitutional similarity at scale. The same feature-coding that answers how closely other constitutions track the American one will answer how many constitutions share a given structural vulnerability, which is the query this project eventually wants to run. Their "Sham Constitutions," 101 California Law Review 863 (2013), is the companion worth having, because it scores the gap between textual promise and actual practice and therefore bounds how much any text-only analysis can claim.

## Formalizing law, and how far it actually goes

**Valeria Zahoransky & Christoph Benzmüller, "Modelling the US Constitution to establish constitutional dictatorship,"** MIREL 2019 at JURIX, CEUR Workshop Proceedings vol. 2632 (2020). Free, CC BY 4.0: http://ceur-ws.org/Vol-2632/MIREL-19_paper_1.pdf The longer version is Zahoransky's Freie Universität Berlin bachelor's thesis, which carries the full Isabelle code: https://www.mi.fu-berlin.de/inf/groups/ag-ki/Theses/Completed-theses/Bachelor-theses/2019/Zahoransky/BA-Zahoransky.pdf

Read this before doing anything else on the formal side. They encode the relevant provisions — the separation of powers in Articles I through III, and Article V — in classical higher-order logic and run the two-step dictatorship argument through Isabelle/HOL. They are careful about what they are doing: it is Guerra-Pujol's reconstruction, not Gödel's argument, and they say so in the second paragraph, noting that Gödel's own reasoning appears in neither his letters to his mother, nor his letters to colleagues, nor Morgenstern's account.

Their conclusion is the honest part and the useful part. They call it "a mere case example," state that general reasoning over the Constitution "is necessary to analyse and represent more of its contents, rather than just one small part," and then say something that should shape this project's method: the real work was in deciding which parts of the text are relevant and how to represent them, and "a large part of the benefit" of those steps "is finding out what does not work for the text at hand" — which they did not publish, for space. The modeling failures are where the knowledge is, and they are missing from the record. If this project does nothing else on the formal route, publishing its own dead ends would be a contribution.

Their theory has been re-derived here, and the record is `analysis/united-states-1947/formal-model-replication.md`. It compiles and proves what they say it proves, and the axiom set is consistent, which is the check that makes the rest mean anything. The substantive findings — that the Article V step is assumed rather than modeled, and that they report no adequate formalization of the amendment itself — are discussed in `academia/godel-loophole.md`.

**Sarah Lawsky, "A Logic for Statutes,"** 21 Florida Tax Review (2017). Free: https://journals.upress.ufl.edu/ftr/article/view/507

The theoretical foundation for everything below. Lawsky argues statutory reasoning is defeasible rather than deductive — conclusions get overridden by later provisions — and that default logic is the right formalism. The consequence for this project is a warning: formalize constitutional text in classical logic and it will report contradictions that are artifacts of the encoding rather than defects in the document. We have already made the analogous mistake once at the level of regex.

**Denis Merigoux, Nicolas Chataing & Jonathan Protzenko, "Catala: A Programming Language for the Law,"** ICFP 2021. Free: https://arxiv.org/abs/2103.03198 and https://github.com/CatalaLang/catala, Apache 2.0.

The most mature tool for turning legislative text into executable code, with default logic built in so that "X, unless Y" is native rather than encoded. It has handled French family benefits and parts of the US tax code. The caveat is structural rather than incidental: Catala targets provisions that compute something, and a clause like "Congress shall have Power To..." computes nothing. Worth watching; not worth adopting on the assumption it will stretch.

**LegalLean — Verified Legal Reasoning in Lean 4.** https://legal-lean.aguilar-pelaez.co.uk/, MIT licensed.

The most directly relevant tool, built on the same prover AlphaProof used. It provides a defeasibility solver and a typed intermediate representation for legal language covering modality, negation, exceptions, temporal conditions, thresholds, definitions and cross-references, and it reports 87 verified theorems across tax, immigration and telecoms case studies. Two features are worth stealing regardless of whether we use the tool: it marks explicitly where machine verification ends and human judgment begins, and it tests whether controlled paraphrases of the same rule produce stable formal output — a direct guard against the system reporting a finding that is really an artifact of how someone worded the input. It is very new and has been exercised on three statutory provisions, not on constitutional text.

**Yadamsuren, Platt & Diaz, "LLM-Assisted Formalization Enables Deterministic Detection of Statutory Inconsistency in IRC §121,"** Artificial Intelligence and Law, accepted 2026. Free: https://arxiv.org/abs/2511.11954 and https://github.com/borchuluun/section121-inconsistency-detection

The closest published work to what this project wants to do, and it carries the single most useful number in this file — with a caveat that has to travel alongside it. A language model alone detected known statutory inconsistencies about a third of the time. The same model used only to translate the statute into Prolog, with a symbolic engine doing the actual checking, reached full accuracy on their benchmark. That gap is the argument against asking a model to find loopholes directly, and the argument for using it as a translator in front of something that cannot be persuaded.

The caveat is that we cannot check the number. Their repository contains only the three Prolog appendices — no benchmark set, no harness, no accuracy data — so the comparison that makes the paper quotable is not reproducible from the published artifacts. The Prolog itself replicates completely on a local install, which is recorded in `TOOLING.md`. Treat the one-third figure as a claim we are relying on rather than one we have verified, and do not let it carry weight it cannot bear.

**Paul McNamara, "Deontic Logic,"** Stanford Encyclopedia of Philosophy. Free: https://plato.stanford.edu/entries/logic-deontic/

Background, and a warning list. Two paradoxes bear directly on constitutional text. Ross's paradox shows that an obligation to do X entails, in standard deontic logic, an obligation to do X-or-anything-else, which will generate spurious findings. Chisholm's paradox concerns contrary-to-duty obligations — what ought to happen when a prior duty is violated — and cannot be consistently formalized in the standard system. Constitutional text is saturated with contrary-to-duty structure, since a large fraction of any constitution specifies what follows when an officer fails to act. Naive formalization will therefore produce contradictions, and separating those artifacts from genuine defects is not a preliminary to the project's work. It is the work.

For the conflict-of-rules question specifically, the Prakken and Sartor argumentation frameworks are the standing apparatus, and ASPIC+ is the de facto standard. They model competing rules with explicit priority orderings and can determine whether a rule set is coherent under a given ordering. No application to a full constitution exists.

## What the Erdős results actually show

This project's stated inspiration is the recent run of AI results on Erdős problems, so the evidence deserves primary-source treatment rather than a summary of press coverage. Terence Tao maintains a wiki cataloguing these contributions, and it is unusually disciplined: every entry is graded, failures are recorded in the same table as successes, and eleven explicit disclaimers head the page, including that it is not a benchmark and that selection bias should be assumed. It was frozen on June 30, 2026.

Counting the tables directly gives 538 logged attempts across 405 distinct problems. The breakdown matters more than the total. In the strongest category — AI working standalone, without human involvement or a comparable result in the literature — there are 61 attempts on 57 problems, yielding 19 full solutions, 23 partial results, 9 unverified claims, and **11 recorded as outright incorrect**. Roughly one in five standalone attempts in the flagship category produced a wrong answer that a human had to catch.

The largest and cleanest category is something else entirely. Formalization — translating an already-known proof into machine-checkable Lean — accounts for 185 attempts and 173 full successes, with no recorded errors. That is not a like-for-like comparison, since formalizing a known result is easier than finding an unknown one. But the shape is the lesson: the reliable capability on display is *rendering mathematics into a form a verifier can check*, and the unreliable one is *producing new mathematics unsupervised*. Seventy of the results across all categories carry a Lean verification.

Read across to this project, that says the transferable move is not asking a model to find the loophole. It is using models to turn constitutional text into a representation something else can check, then doing the checking mechanically. The Yadamsuren result points the same way from the legal side, and Tao's own assessment of AI in mathematics — that it handles the routine and misses the clever step, and that proof assistants matter because they remove the need to trust a collaborator — is the third witness.

The supporting citations: DeepMind's AlphaProof work is published as "Olympiad-level formal mathematical reasoning with reinforcement learning," Nature 651, 607 (2025), doi 10.1038/s41586-025-09833-y, paywalled, with a free summary at https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/. OpenAI reported a model disproving the Erdős unit distance conjecture at https://openai.com/index/model-disproves-discrete-geometry-conjecture/, though that page renders only its title without a browser and the claim was not verifiable from the page itself. The problem database is at https://www.erdosproblems.com and the wiki is a git clone target rather than a browsable page — `git clone https://github.com/teorth/erdosproblems.wiki.git` works; the same URL in a browser does not.

## Punctuation and ambiguity

**O'Connor v. Oakhurst Dairy**, 851 F.3d 69 (1st Cir. 2017). Official slip opinion, free: http://media.ca1.uscourts.gov/pdf.opinions/16-1901P-01A.pdf

The Oxford comma case, and the direct precedent for this project's textual route. The opinion opens "For want of a comma, we have this case." A Maine overtime exemption covering "packing for shipment or distribution of" food products was held ambiguous for want of a serial comma, and the ambiguity was resolved against the employer. The detail worth carrying is that the court used Maine's own drafting manual, which discourages the serial comma, as evidence about what the legislature meant — a reminder that the relevant question is never whether a mark is present but what its presence or absence licenses given the drafting conventions in force.

**Adam Crews, "The So-Called Series-Qualifier Canon,"** 116 Northwestern University Law Review Online 198 (2021). Free: https://northwesternlawreview.org/articles/the-so-called-series-qualifier-canon/

Directly relevant to the Second Amendment work already underway. Crews argues the series-qualifier canon as applied in *Facebook v. Duguid* is an unjustified expansion of a narrower principle, and draws on formal linguistics to show it does not track ordinary English processing. The canon and the last-antecedent rule can point opposite directions on the same sentence, which is the situation a three-comma militia clause creates. Anyone building a parser for constitutional text needs this before writing the grammar.

**Thomas Lee & Stephen Mouritsen, "The Corpus and the Critics,"** 88 University of Chicago Law Review (2021). Free: https://chicagounbound.uchicago.edu/uclrev/vol88/iss2/1/

Corpus linguistics as evidence about ordinary meaning, defended against its critics. The use here is quantitative rather than interpretive: an exploit usually requires reading a term in a way that is permissible but unusual, and corpus methods can measure how unusual. That converts a rhetorical claim about strained reading into a number.

**Clement Guitton et al., "Identifying open-texture in regulations using LLMs,"** Artificial Intelligence and Law (2025), doi 10.1007/s10506-025-09450-0. Paywalled.

Detects deliberately vague language in GDPR text, reporting F1 around 0.84 for the stronger model. The finding that should temper enthusiasm is buried in their method: human annotators agreed with each other poorly about what counted as open-texture. Any automated vagueness score inherits that disagreement, and vagueness in a constitution is often a design choice rather than a defect.

## Gaps

Nobody has argued in general terms whether theorem-proving methods transfer to law. The nearest neighbors — Zahoransky and Benzmüller, LegalLean, Lawsky, the Prolog hybrid — each perform some version of the transfer without ever framing it as a question with an answer. Zahoransky and Benzmüller come closest and explicitly scope themselves to a case example. The obstacles a general argument would have to answer are that law has no Lean-scale corpus of formalized statements to train against, that legal validity is not binary in the way a proof obligation is, and that constitutional provisions are normative rather than descriptive, which is a category difference and not merely a difficulty.

Computational ambiguity detection has been applied to contracts and regulations, not constitutions, and no existing system distinguishes deliberate flexibility from exploitable ambiguity. That distinction is the whole question, and it currently requires a human.
