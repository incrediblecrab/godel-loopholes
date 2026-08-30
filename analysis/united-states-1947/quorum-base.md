# The quorum base, 1947

`silence-inventory.md` row 5 records that Article I, Section 5 says "a Majority of each shall constitute a Quorum to do Business" and does not say a majority of what. `search/quorum_cascade.py` turns that silence into numbers, and every number it produces rests on one premise: that the base is the members actually chosen and sworn, not the statutory size of the chamber. If the base is the statutory 435, the cascade collapses at step one and the whole thing is a null result.

This file settles that one premise. It settles nothing else.

## The answer

The base is the members chosen, sworn and living. A vacancy lowers the denominator, and so does a member-elect who has not been sworn.

Both chambers had said so in terms, decades before the vantage, and neither had changed its position by December 5, 1947.

## The House

Hinds' *Precedents of the House of Representatives*, volume 4, section 2889, at printed page 62. The section heading is the holding:

> **2889. After the House is once organized the quorum consists of a majority of those Members chosen, sworn, and living, whose membership has not been terminated by resignation or by the action of the House.**

Speaker Cannon delivered it on March 16, 1906, on a point of order raised by Marlin E. Olmsted of Pennsylvania during a vote on H.R. 15744. Olmsted's argument is on the same page and carries the arithmetic that matters here:

> Mr. Speaker, the statute fixing the number of Members provides for the election of 386, and I understand that 386 were chosen. Two of those Members, one from Pennsylvania, Mr. Castor, and one from Virginia, Mr. Swanson, are not now Members of Congress, The gentleman from Pennsylvania is dead and the gentleman from Virginia, who was sworn in, has resigned. They are clearly no longer Members of this House. Two persons who were chosen to be Members have never been sworn. They have never qualified. They have not become Members of this House. That, therefore, leaves the membership of this House at 382, of which number 192 constitute a quorum.

Four deductions from a statutory 386: one death, one resignation, two unsworn. The chair accepted the reasoning and the resulting quorum.

The footnote on the same page gives an earlier instance of the same rule producing a smaller number:

> On April 3, 1896 (first session Fifty-fourth Congress, Journal, p. 366), Mr. Speaker Reed ruled that 178 Members were a quorum, although, had there been no vacancies in representation, the quorum would have been 179.

## The Senate

Hinds' volume 4, section 2891, at printed page 64:

> **2891. After long discussion the Senate finally decided that a quorum consisted of a majority of Senators duly chosen and sworn.**

The Senate reached that position slowly and against real opposition, which is worth recording rather than smoothing over. On June 30 and July 9, 1862 the Senate considered declaring that a majority of the Senators "duly elected and entitled to seats" was a quorum — the statutory-size reading — and laid the proposition on the table by nineteen votes to eighteen. President pro tempore Solomon Foot of Vermont "expressed a decided opinion that a quorum consisted of a majority of the whole number to which the body would be entitled."

That view lost by one vote. The chosen-and-sworn reading then hardened: adopted by resolution on May 4, 1864 by yeas 26, nays 11, in the form "a quorum of the Senate consists of a majority of the Senators duly chosen"; revised on March 26, 1868 by a committee of Anthony, Pomeroy and Edmunds to insert the words "and sworn"; re-adopted in that form on January 17, 1877; and sustained on October 11, 1893 when an appeal from a decision of the chair resting on the rule was laid on the table, yeas 38, nays 5.

The section is candid that the Senate went further than the House and with less deliberation: "The rule of the Senate goes further than the decisions in the House, and does not seem to have been the subject of extended deliberation so far as the qualification feature is concerned."

## What was read, and how

Read from page images rendered at 200 dpi from the GovInfo PDF, not from the text layer.

- URL: `https://www.govinfo.gov/content/pkg/GPO-HPREC-HINDS-V4/pdf/GPO-HPREC-HINDS-V4-4.pdf`
- SHA-256: `945d83fcd1ddc95ea90c8b48c204b298d333b3a646a4d33eea272225e01d2193`
- Printed page 62 is PDF page 4; printed page 64 is PDF page 6.

**A caveat that matters, and that this project's own rule did not anticipate.** Reading the page image is normally enough, because the page image is a photograph of the printing. This document is not that. GovInfo's Hinds is a modern re-typesetting derived from optical character recognition, and the corruption is visible in the rendered page: page 62 prints "If the first moaning was to be taken" for *meaning*, "he does not thin that" for *think*, "as there axe two vacancies" for *are*, and "Air. Vallandigham concurred" for *Mr.* The errors are baked into the document, so rendering it at any resolution reproduces them faithfully.

The three passages quoted above are clean and unambiguous in the image, and the four corruptions listed are all in surrounding narrative rather than in a holding. But "read from the page image" is a weaker guarantee here than it is for the Library of Congress *Statutes at Large* scans, and it should not be recorded as though it were the same thing. Verifying against a scan of the 1907 printing remains open.

## Corrections to the research that produced this

A research agent was asked this question and returned a report that reached the right answer on the strength of the text layer. Two of its citations are wrong, and both were caught by reading the image:

- It dated Cannon's ruling **April 16, 1906** and placed it at Congressional Record page **5354**. The section is dated **March 16, 1906** and its footnote reads "First session Fifty-ninth Congress, Record, p. 3932."
- It reported the ruling as synthesising a chain ending in a decision it called definitive, without recording that the Senate's contrary reading lost by a single vote in 1862. A rule settled 19 to 18 is settled, but a write-up that omits the margin is describing a different degree of certainty than the record supports.

The vote counts it gave for 1864 (26 to 11), for 1893 (38 to 5), and the 1868 insertion of "and sworn" are confirmed.

## What this does and does not establish

Established: the denominator of "a Majority of each" tracks the membership as it actually stands. The premise under `search/quorum_cascade.py` step one holds.

It did not save the cascade. `quorum-cascade-null.md` closes that as a null result on arithmetic the premise has no bearing on: beginning the manoeuvre costs a quorum, and two thirds of a quorum is fewer people than a quorum. This file remains worth having — the holding is a real feature of the 1947 Congress, and it is the thing anyone re-examining the silence inventory will need — but it did not turn out to be load-bearing.

Not established, and the cascade is not a finding without them:

- That an emptied seat refills slower than it empties. That is a claim about 1940s state election law, not about the Constitution, and it is open.
- That exclusion of a member-elect and expulsion of a sitting member carry the asymmetry the cascade turns on. Article I, Section 5 states two different thresholds on its face; what is open is pre-1947 practice, and *Powell v. McCormack* is 1969 and out of bounds.
- That any of this survives contact with a chamber that does not wish to be reduced.

Until those are settled, `cascade.status` stays where it is.

## The falsifier

A pre-1947 ruling, in either chamber, computing a quorum against the statutory chamber size while seats stood vacant. Solomon Foot argued for exactly that in 1862 and lost by one vote; if he or anyone else ever prevailed on it, this file is wrong and the cascade collapses at step one.
