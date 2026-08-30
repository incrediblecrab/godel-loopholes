# Method

This folder holds how to look. It is written once and applied many times, so nothing in it names a jurisdiction except as an example or a test case.

The test for whether a file belongs here is whether it would change if you swapped countries. Procedures, criteria and templates would not, so they live here. Anything about what a particular text says lives in `analysis/`.

## The claim we are trying to make or break

Every candidate this project produces has the same shape. Following the rules of a document, at a stated vantage, an actor can reach a state that the people who ratified it would have called the destruction of the order it establishes, without any step breaking a rule.

The last clause is the whole difficulty. A coup is not a loophole. If a step requires breaking a rule, the candidate is describing lawlessness, which is real but is not what Gödel claimed to have found and is not what a text can be examined for.

## Method is validated before it is applied

No procedure in this folder gets pointed at an open question until it has rediscovered a solved one. The standing test set is the three interwar collapses, and they are useful precisely because they failed in three different ways.

Germany 1933 was carried out through the amendment procedure itself, which carried procedural limits and no substantive ones. It tests whether a method notices that an amendment rule can be adequate on its own terms and still authorize its own defeat.

Austria 1933 and 1934 ran through an instrument the constitution never mentions: a wartime economic enabling act from 1917 that had never been repealed. It tests whether a method looks outside the constitutional text at the statutes still standing beside it. A method reading only the constitution cannot see this one at all.

Italy 1925 and 1926 happened through ordinary legislation while the Statuto sat untouched, its eighty-four articles never amended. It tests whether a method can register that constitutional text is sometimes simply not where the action is. The legal mechanics of all three are set out once, in `attack-surfaces.md`; what matters here is only the role each one plays in validation.

A procedure that cannot recover all three is not ready. Reporting which of the three a procedure catches, and which it misses, is part of proposing it.

## Two routes

The semantic route reads for defects in the text as written: contradictions between clauses, terms left undefined, and marks that change a parse. This is not speculative. Collating Amendments I through X across six authoritative witnesses produced two live instances without anyone looking for them, and both are recorded in `corpus/README.md`.

The formal route treats the document as a system with rewrite rules and asks what is reachable. Article V is the obvious object: an amendment procedure that can amend the amendment procedure, carrying exactly two entrenchments, one of them expired. The relevant literature on self-amendment is already shelved in `academia/`.

The routes are not rivals and a candidate may use both. What neither is allowed to do is produce a conclusion that cannot be stated as a sequence of legal operations with citations.

## What this folder does not hold

No results. A procedure demonstrated on a text produces an analysis, and analyses live in `analysis/` under the name of the snapshot they examine, including the ones written to validate a procedure.

No tooling. Nothing here assumes a program exists to run it, and every procedure is written so a person could execute it by hand on one document. That constraint holds for this folder and is not an artifact of our not having tools: provers and solvers are installed, and `TOOLING.md` records them. Where they have been used, the result is an analysis and sits in `analysis/` under the snapshot it examines, which is the same rule that governs everything else produced by applying a procedure to a text. When a procedure here does acquire a mechanical implementation, the procedure and the implementation stay separate, so the first remains checkable by hand.
