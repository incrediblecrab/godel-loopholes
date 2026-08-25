# Gödel's loophole

The whole evidentiary base for this project is one document, dictated from memory twenty-four years after the fact by a man who says in his first line that he has not checked his notes. Everything else — every reconstruction, every formalization, including the ones this project will build — is inference stacked on that. It is worth being blunt about this at the start, because the story is retold constantly and the retellings are almost uniformly worse-sourced than they sound.

Morgenstern's memo does not say what Gödel found. It says he found something. No reconstruction has ever been verified against Gödel's own reasoning, because Gödel's own reasoning has never been located — not in his letters to his mother, not in his correspondence with colleagues, not in Morgenstern's account or diary. Anyone who tells you what Gödel's loophole *was* is telling you what someone later thought it might have been.

## The primary source

**Oskar Morgenstern, "History of the Naturalisation of Kurt Gödel,"** dictated September 13, 1971. Deposited at the Shelby White and Leon Levy Archives Center, Institute for Advanced Study, by Dorothy Morgenstern Thomas, received August 30, 2005.

Full transcript, free: https://mathshistory.st-andrews.ac.uk/Extras/Godel_naturalisation/ and the archival record with scanned PDF at https://albert.ias.edu/20.500.12111/2333 — the IAS catalogue sits behind a Cloudflare challenge and will not resolve without a browser, so the St Andrews transcript is the working copy.

The memo opens by disclaiming itself: dictated "on the basis of memory only without consultation of my notes and diaries," with concrete dates to "be filled in at another opportunity." It establishes the year as 1947 and the place as Trenton, and it does not give the day; December 5 comes from court records rather than from Morgenstern. It carries the two passages everything else hangs on — that Gödel had found "some inner contradictions" showing "in a perfectly legal manner it would be possible for somebody to become a dictator and set up a Fascist regime," and the exchange in the hearing room where Gödel says of Austria that "the constitution was such that it finally was changed into a dictatorship," the examiner says it could not happen here, and Gödel answers "Oh, yes, I can prove it." The examiner's reply — "Oh God, let's not go into this" — ends the examination.

Morgenstern's diaries are separately digitized, at the University of Graz, and are the obvious next place to look for anything more specific: http://gams.uni-graz.at/archive/objects/o:ome.b47-47/methods/sdef:TEI/get?mode=b47-47

**Jeffrey Kegler's source criticism.** https://jeffreykegler.github.io/personal/morgenstern.html and the rediscovery account at https://jeffreykegler.blogspot.com/2009/01/gdel-and-constitution-iv-redisovery.html

Not scholarship, and indispensable anyway. Kegler tracked how the Morgenstern document went missing — Dawson could not locate it while writing *Logical Dilemmas* — and what filled the vacuum. His central finding is that essentially every pre-2009 telling is hearsay, and that the version in Gödel's own *Collected Works* contains invented dialogue, double-translated from English into German and back, from a source that put the hearing in Washington rather than Trenton. For a project whose stated risk is amplifying plausible unsupported claims, this is the required reading. The practical rule that falls out of it: cite the Morgenstern memo and Dawson, and treat everything else as commentary.

## The reconstructions

**F.E. Guerra-Pujol, "Gödel's Loophole,"** 41 Capital University Law Review 637 (2013). Free mirror: https://i2i.org/wp-content/uploads/Guerra-Pujol-Godel.pdf

The central modern attempt and the source of the vocabulary everyone else uses. The reconstruction is two-step and turns on the fact that Article V does not exempt itself from its own operation: first amend Article V to strip its procedural hurdles and its substantive protection of equal state suffrage, then use the weakened procedure to install whatever you like. He also proposes a criterion separating self-referential contradictions, which he calls Gödelian, from ordinary ones. He calls it a conjecture, and the project should keep that word attached to it.

**Guerra-Pujol, "Gödel's Loophole: A Prequel,"** 30 Southwestern Journal of International Law 613 (2024). Free: https://www.swlaw.edu/sites/default/files/2025-01/13%20-%20Guerra.pdf

The bridge to the interwar material, and the paper most directly relevant to what this corpus already contains. It asks whether the loophole is historically plausible by comparing the American case against the Central European constitutions that were in fact amended into dictatorships, Austria foremost. Gödel's answer to the examiner was about Austria, not about theory, which makes this the paper that takes his actual stated reasoning most seriously.

**Guerra-Pujol, "Gödel's Loophole 2.0,"** SSRN working paper 4519241 (2023). SSRN blocks automated retrieval; the author's summary is at https://priorprobability.com/2023/07/26/godels-loophole-2-0/

Extends the self-amendment argument to other self-regulating systems, including constitutional-style constraints on language models. Mostly of interest here as evidence that the author regards the logic as general rather than American.

Two of his blog posts are more useful than their form suggests. "Works Citing Gödel's Loophole," https://priorprobability.com/2022/01/20/works-citing-godels-loophole/, is an author-maintained citation map across English, German, Italian and Polish, and is the fastest route into the secondary literature. "Replies to Mader and Roznai," https://priorprobability.com/2022/01/21/godels-loophole-replies-to-mader-and-roznai/, is his answer to the two constitutional scholars who engaged and, in his view, waved the problem through: his position is that unamendability is not real, because any entrenchment can be undone by the two-step move before the thing it protects is touched.

## The formalization that already exists

**Valeria Zahoransky & Christoph Benzmüller, "Modelling the US Constitution to establish constitutional dictatorship,"** MIREL 2019 at JURIX, CEUR vol. 2632 (2020). Free, CC BY 4.0: http://ceur-ws.org/Vol-2632/MIREL-19_paper_1.pdf The bachelor's thesis version, with the full Isabelle sources, is at https://www.mi.fu-berlin.de/inf/groups/ag-ki/Theses/Completed-theses/Bachelor-theses/2019/Zahoransky/BA-Zahoransky.pdf

Someone has already run this argument through a proof assistant. They encode the separation of powers in Articles I through III and the amendment procedure of Article V in classical higher-order logic, and check Guerra-Pujol's two-step sequence in Isabelle/HOL. They are scrupulous about whose argument it is: not Gödel's, and they say so immediately, along with the negative result about where Gödel's reasoning is not to be found.

Their own limits are stated plainly and should be quoted rather than paraphrased when this project describes its position relative to theirs. They call the work "a mere case example," and note that general reasoning about the Constitution would require representing "more of its contents, rather than just one small part." The remark worth building on is about method: the hard steps were deciding which parts of the text matter and how to represent them, and "a large part of the benefit" of those steps "is finding out what does not work for the text at hand" — which they did not publish, for space. The failed encodings are where the knowledge is, and they are missing from the record.

## What Gödel might have found

Four candidates are in circulation. None is verified, and the differences between them matter, because they imply different searches.

The first is Guerra-Pujol's: Article V can be used on itself, so entrenchment is a speed bump rather than a wall. The second is weaker and older, and appears in Suber and in the general literature: Article V imposes procedural conditions and almost no substantive ones, so anything at all can be adopted if the procedure is followed. The third is the runaway convention — that an Article V convention, once seated, might claim plenary constituent power and exceed its mandate. The fourth is procedural manipulation of quorum and vote-counting rules, so that each amendment makes the next one easier.

The second candidate deserves more attention than it gets, because it requires no cleverness at all. If Article V's only substantive limit is equal state suffrage in the Senate, then the document simply does not prohibit its own contents being replaced, and no contradiction is needed — just a majority and patience. Whether that counts as a *loophole* or merely as how amendment works is exactly the question Schmitt, Hart, and Roznai answer differently below.

## Self-amendment: the canon

**Peter Suber, "The Paradox of Self-Amendment: A Study of Logic, Law, Omnipotence, and Change"** (Peter Lang, 1990). Out of print, and free in full at https://legacy.earlham.edu/~peters/writing/psa/index.htm with a copy at Harvard DASH.

The central work, and the most useful single thing in this file after the Morgenstern memo. Suber's argument is that self-amendment is logically contradictory and nonetheless routine and lawful, and he makes the empirical case hard to dismiss: it has happened in 47 of the 50 states, and in every nation with a written constitution he examined. He shows the paradox shares a structure with the omnipotence paradox — the stone too heavy to lift — and concludes that law can contain a genuine contradiction and go on operating. That conclusion cuts against this project's instincts and should be read carefully rather than around. The condensed version, "The Paradox of Self-Amendment in American Constitutional Law," 7 Stanford Literature Review 53 (1990), is at https://legacy.earlham.edu/~peters/writing/psaessay.htm, and his encyclopedia entry "Self-Reference in Law" at https://legacy.earlham.edu/~peters/writing/slfreflw.htm is the quickest orientation to the whole debate.

**Alf Ross, "On Self-Reference and a Puzzle in Constitutional Law,"** 78 Mind 1 (1969). Paywalled through JSTOR and Oxford Academic.

The founding paper. Ross argues, using Article 88 of the Danish Constitution, that an amending clause cannot coherently be used to amend itself, and that the attempt reduces to formal self-contradiction. Suber's summary is that Ross either did not know or did not acknowledge that self-amendment happens constantly in practice. The first published reply is Norbert Hoerster, "On Alf Ross's Alleged Puzzle in Constitutional Law," 81 Mind 422 (1972), also paywalled, which denies the puzzle is a puzzle.

**Manish Oza, "Can We Legally Revise the Highest Legal Rule?,"** 31 Legal Theory 270 (2025). Open access: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B4A6B1267807410343A9395021586191/S135232522510075Xa.pdf/can-we-legally-revise-the-highest-legal-rule.pdf

The current state of the Ross debate, free, and recent. The right place to see where the argument stands before adding to it.

**Fabien Gélinas, "Modelling Fundamental Legal Change: The Paradox of Context and the Context of Paradox,"** 28 Canadian Journal of Law & Jurisprudence 77 (2015). Paywalled; abstract open.

The explicit bridge between the legal and the formal literatures — self-referential legal constructs resist first-order treatment, sit more naturally in modal and deontic frameworks, and connect to fixed-point arguments. Short, and the closest thing to a map between the two halves of this project.

## The positions that dissolve the problem

These are the serious objections, and the project is stronger for meeting them than for ignoring them.

**H.L.A. Hart, "The Concept of Law"** (Oxford, 1961; 2nd ed. 1994), chapter 5. Book. Hart's rules of change are secondary rules — rules about rules — and their validity rests on the rule of recognition, which is a social fact about what officials accept and practice rather than a theorem. On this account self-amendment is valid because it is accepted, and its logical shape is beside the point. **Joseph Raz, "The Authority of Law"** (Clarendon, 1979), book, sharpens this into the sources thesis: validity comes from pedigree, not from logic or morality.

If Hart and Raz are right, then finding a formal contradiction in a constitution proves nothing about what is lawful, and this project has to explain why a contradiction should worry anyone. That is a real burden and it should be carried explicitly rather than assumed away.

**Carl Schmitt, "Constitutional Theory"** (1928; Duke, 2008, trans. Seitzer). Book. The opposite objection, from the opposite direction. Schmitt's separation of constituent power from constituted powers implies that an amendment procedure is a constituted power and therefore cannot reach the constitutional order's identity — a constitution cannot lawfully authorize its own destruction, so what looks like a loophole is simply void. Schmitt is the principal theoretical opponent of the Gödelian position, and the fact that he is also the jurist who supplied intellectual cover for the Nazi seizure of power is not incidental to a project about lawful routes to dictatorship.

## Amendment beyond the text

**Akhil Reed Amar, "Philadelphia Revisited: Amending the Constitution Outside Article V,"** 55 University of Chicago Law Review (1988). Free: https://law.yale.edu/sites/default/files/documents/pdf/1988Philadelphia.pdf

Amar argues Article V is not exclusive, and that the People retain an unenumerated power to amend by direct majoritarian action — the Philadelphia Convention itself having acted outside the amendment rules of the Articles of Confederation. Two consequences for this project. It is a competing loophole, larger than the one Guerra-Pujol describes. And it undercuts the premise that analyzing Article V is sufficient, since on Amar's account the document is changeable by means its text does not mention.

**Yaniv Roznai, "Unconstitutional Constitutional Amendments"** (Oxford, 2017), book, with the article-length precursor "Towards a Theory of Unamendability," NYU Public Law Research Paper 15-12 (2015), on SSRN. Roznai's numbers are worth carrying: eternity clauses appeared in roughly 17 percent of constitutions between 1789 and 1944, and in more than half between 1989 and 2013. His distinction between primary and secondary constituent power is Schmitt's, put to democratic use.

**Richard Albert, "Constitutional Amendments: Making, Breaking, and Changing Constitutions"** (Oxford, 2019). Book. Introduces dismemberment for changes that break a constitution's core commitments while wearing the form of amendment — which is the category Gödel's scenario would fall into if it exists, and a useful name for the thing this project is looking for.

**Ben Abramowitz, Ehud Shapiro & Nimrod Talmon, "How to Amend a Constitution? Model, Axioms, and Supermajority Rules,"** AAMAS 2021. Free preprint: https://arxiv.org/abs/2011.03111

An axiomatic treatment of amendment protocols and supermajority thresholds, from the multiagent systems community rather than from law. It cites Guerra-Pujol, which makes it one of the few places the two literatures touch.

## Gaps

Neither Hart nor Raz ever published a direct reply to Ross. Their engagement is diffused through *The Concept of Law*, *Essays on Bentham*, and *The Authority of Law*, so the Ross debate has no single canonical rebuttal to point at and has to be assembled.

Ross and Hoerster are both paywalled at Mind, and they are the two papers that define the problem. This is the most consequential access gap in this file.

SSRN blocks automated retrieval entirely, which affects Guerra-Pujol's original paper and Roznai's working paper; both have mirrors, and the mirrors are what is cited above.

The largest gap is not bibliographic. Nobody has tested any of the four candidate reconstructions against what a 1947 reader would have been looking at — a Constitution with twenty-one amendments, no presidential term limit, and no formal emergency power. Every reconstruction in this file is written against the modern document.
