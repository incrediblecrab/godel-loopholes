# Article V threshold arithmetic, 1947

This is the threshold-arithmetic enumeration from `method/enumerations.md` run against Article V at the 1947 vantage. It is the cheapest procedure in the method and the only one whose output is not arguable, and it produces the minimum coalition figure that `method/what-counts-as-a-finding.md` requires of every candidate.

## The two clauses

Article V, from `corpus/united-states-1947/09-17-1787-constitution-parchment-nara-transcription.txt`:

> The Congress, whenever two thirds of both Houses shall deem it necessary, shall propose Amendments to this Constitution, or, on the Application of the Legislatures of two thirds of the several States, shall call a Convention for proposing Amendments, which, in either Case, shall be valid to all Intents and Purposes, as Part of this Constitution, when ratified by the Legislatures of three fourths of the several States, or by Conventions in three fourths thereof …

Article I, Section 5, from the same file:

> Each House shall be the Judge of the Elections, Returns and Qualifications of its own Members, and a Majority of each shall constitute a Quorum to do Business …

## The base is not stated, and that is the finding

Article V says two thirds of both Houses. It does not say two thirds of what. Two thirds of the membership and two thirds of those voting are different numbers, and the text does not choose between them.

That silence is not universal among constitutions of comparable ambition. The Weimar constitution's Article 76 states its base explicitly, requiring that two thirds of the statutory membership be present and that at least two thirds of those present assent. The same fraction appears in both documents and only one of them says what it divides.

An unstated base is the second output of the threshold-arithmetic procedure, and it is worth more than the numbers, because a number computed on the wrong base is simply wrong while a silence has to be filled by someone.

## Who filled it, and when

It was filled twenty-seven years before Gödel's hearing, and against the reading that would have made Article V harder to use.

*National Prohibition Cases*, 253 U.S. 350 (1920), decided June 7, 1920. Read from the official Library of Congress page images at https://tile.loc.gov/storage-services/service/ll/usrep/usrep253/usrep253350/usrep253350.pdf The case has no conventional opinion; the Court announced numbered conclusions, and the second reads:

> 2. The two-thirds vote in each house which is required in proposing an amendment is a vote of two-thirds of the members present—assuming the presence of a quorum—and not a vote of two-thirds of the entire membership, present and absent. *Missouri Pacific Ry. Co. v. Kansas*, 248 U. S. 276.

Read from the page image rather than from the optical character recognition layer, which rendered both em dashes as hyphens.

This is admissible at the 1947 vantage, and so is *Schneiderman v. United States*, 320 U.S. 118 (1943), recorded in `academia/naturalization-1947.md`. Both predate December 5, 1947. Nothing in this file reaches forward of the snapshot.

## The arithmetic

Combining the holding with the quorum clause: the base is a quorum, a quorum is a majority of the chamber, and the requirement is two thirds of that.

At the 1947 vantage there were forty-eight states, ninety-six senators, and four hundred thirty-five representatives, the House having been fixed at that number by the apportionment legislation of 1929.

| | Members | Quorum | Two thirds of quorum | Share of chamber |
|---|---|---|---|---|
| House | 435 | 218 | 146 | 33.6% |
| Senate | 96 | 49 | 33 | 34.4% |

Had the base been the entire membership, the figures would have been 290 and 64.

So at the congressional stage of Article V, an amendment could be proposed in 1947 by one hundred forty-six of four hundred thirty-five representatives and thirty-three of ninety-six senators. Slightly over a third of each chamber, and fewer than half the members that the phrase "two thirds of both Houses" is ordinarily taken to mean.

For completeness at the same vantage: three fourths of the states for ratification is thirty-six of forty-eight, and two thirds of the state legislatures to compel a convention is thirty-two.

## What this does and does not show

It does not show that the United States Constitution was easier to amend than the Weimar constitution. That comparison has to be made carefully and it comes out the other way.

Weimar Article 76 was single-stage. Four ninths of the Reichstag's statutory membership, about forty-four percent, together with the Reichsrat, amended the constitution outright. Article V's congressional stage is lower, at about a third of each chamber, but it only proposes. Ratification by thirty-six of the forty-eight state legislatures then had to follow, and there is no analogue to that in Article 76. Taken end to end the American procedure is markedly more rigid, and the honest statement of this finding is narrow.

The narrow statement is this. The congressional gate of Article V is roughly a third of each chamber rather than two thirds of it, that number is lower than the phrase suggests and lower than the corresponding single-stage German figure, and it was fixed by the Supreme Court in 1920 in the direction of the smaller number. Whatever protection Article V affords is carried almost entirely by the ratification stage, not by the supermajority in Congress.

That last sentence is the load-bearing one for later work, because it says where to look. A path that neutralises or bypasses state ratification faces a far weaker congressional threshold than the text implies.

## A minority of the population, argued at the bar in 1920

Counsel in *National Prohibition Cases* had already run this enumeration, and further than we have. Arguing against the Eighteenth Amendment, they told the Court:

> The census discloses, that there are three-fourths of the States of the Union whose total population amounts to less than forty-five per cent. of the people of the United States, and two-thirds of a quorum of both houses of Congress may, therefore, likewise represent only a minority of the population.

This is argument of counsel as reported, not a holding, and it rests on census figures contemporaneous with 1920 rather than 1947. This project has not recomputed it for the 1940 census and does not assert the 1947 figure.

It is recorded here for two reasons. It establishes that the minimum-coalition calculation this project treats as one of its own procedures was performed and presented to the Supreme Court in 1920, which is directly relevant to whether any later version of it is novel. And the argument lost.

## Where the base actually came from

Conclusion 2 rests on *Missouri Pacific Ry. Co. v. Kansas*, 248 U.S. 276 (1919), decided January 7, 1919. Read from the LOC page images at https://tile.loc.gov/storage-services/service/ll/usrep/usrep248/usrep248276/usrep248276.pdf

That case was not about Article V. It construed Article I, Section 7, Clause 2, the two-thirds required to pass a bill over a presidential veto, and held that it means two thirds of a quorum, a quorum being a majority under Article I, Section 5, and not two thirds of all the members. Its reported syllabus states that this conclusion follows from the context, from the proceedings in the Convention, and from the early and consistent practice of Congress, "especially under the similar provision made for submitting constitutional amendments."

The order of authority is worth stating plainly, because it is not what a citation chain usually looks like. The veto-clause holding was justified in part by pointing at how Congress had long behaved under Article V. Article V's own base was then settled in 1920 by citing the veto-clause holding.

This is not circular reasoning in the strict sense. *Missouri Pacific* relied on congressional practice as a fact about the world, not on a prior judicial construction of Article V, and there was no such construction to rely on. But it does mean something that matters for this project: the base of Article V's fraction was never litigated and decided on its own terms. It was ratified, once, by reference to what Congress had already been doing, and the doing came first.

A rule that a constitution does not state, which is then filled in by the practice of the body the rule constrains, is a distinct structural pattern from the ones in `method/attack-surfaces.md`. It belongs to the undefined-terms enumeration rather than the threshold one, and the question that procedure asks is whether the definer of an operative term is inside the set of actors the term is meant to constrain. Here it is.

## Falsifier

The claim is that Article V does not state the base of its fraction, that the Supreme Court fixed the base as a quorum in 1920, and that the resulting 1947 congressional threshold is 146 representatives and 33 senators.

It would be wrong if a quorum for the purpose of a constitutional amendment vote were something other than the Article I, Section 5 majority, which is the first thing an opponent should attack; *Missouri Pacific* expressly equates the two, so this now requires displacing a 1919 holding as well as a 1920 one. It would be wrong if the House was not 435 members in 1947, which is checkable and which this project has taken from the apportionment legislation rather than from a count.

The reading of *Missouri Pacific* offered above is the remaining soft point. It is taken from the reported syllabus and from the argument pages rather than from a close reading of the full opinion, and a careful reader of the whole case might find the reliance on amendment practice to be narrower than the syllabus makes it sound.

## Null result

Article V was searched for a stated base and there is none, which is recorded as the finding rather than as a failed search. It was also searched for any provision fixing a quorum specific to amendment votes, and there is none, which is why the general Article I quorum governs and why the two clauses have to be read together to get a number at all.
