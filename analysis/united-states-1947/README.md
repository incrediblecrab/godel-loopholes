# United States, 1947

This folder is the reconstruction of what Gödel could have found, from the documents as they stood when he found it. It is the only analysis in this project where the answer is not known, which is why the three collapse folders were worked first: they exist to establish that the procedures recover a real path when one is there, and fail visibly when one is not.

## Vantage

The snapshot is the United States as of December 5, 1947, the date of the hearing, and it holds five files in `corpus/united-states-1947/`.

The vantage rule bites hardest here. Nothing forward of December 5, 1947 may enter an argument in this folder. The Twenty-second Amendment had been proposed in March 1947 but was not ratified until 1951 and is therefore not part of the document under analysis. There were forty-eight states, ninety-six senators, and four hundred thirty-five representatives, and every threshold in this folder is computed on those numbers rather than on modern ones.

Case law decided before the vantage date is admissible, and two decisions matter enough to name here. *National Prohibition Cases*, 253 U.S. 350 (1920), fixed the base of Article V's two-thirds requirement. *Schneiderman v. United States*, 320 U.S. 118 (1943), described Article V as carrying no substantive limitation beyond the Senate proviso, in a naturalization case decided under the same attachment standard Gödel was examined under four years later. Both are recorded in `academia/naturalization-1947.md`.

## What is here

`threshold-arithmetic.md` runs the threshold-arithmetic enumeration over Article V. It establishes that the article does not state the base of its fraction, that the Supreme Court settled the base as a quorum rather than the full membership in 1920, and that the congressional stage of Article V was therefore satisfiable in 1947 by 146 of 435 representatives and 33 of 96 senators.

It also records that the minimum-coalition argument this project treats as one of its own procedures was made to the Supreme Court by counsel in 1920, and lost. That is a direct hit on the novelty requirement in `method/what-counts-as-a-finding.md`, and it arrived before any candidate had been raised, which is the best possible time for it to arrive.

`silence-inventory.md` runs the silence inventory. It lists twelve fields the constitution leaves to ordinary legislation or to nobody at all, and finds that six of them form a self-referential cluster: Article V's threshold is two thirds of a quorum, the quorum is a majority of the House's membership, and the House determines its own membership under Article I, Section 5. It returns no candidate, and it records that Justice Rutledge grouped three of the same clauses in *Colegrove v. Green* in June 1946.

## What is not here yet

No candidate path. Four enumerations have not been run: the power inventory over the Article I and Article II grants, the reference graph, the undefined-terms pass, and the parse enumeration over the clauses the power inventory marks as consequential.

The silence inventory was expected to be the most productive and was the enumeration the Italian control case was worked to make unavoidable. It was productive in the sense that it found the cluster, and unproductive in the sense that the cluster reaches only Congress and the federal courts and leaves state ratification entirely untouched. That is the same conclusion `threshold-arithmetic.md` reached from the opposite direction, which is mild evidence that the conclusion is right.

Its results are provisional in one respect that matters. The inventory names the statutes filling each silence, and none of them has been verified against Statutes at Large, because the retrieval problem recorded in `corpus/README.md` is unsolved. The standing rules of the House and Senate as of 1947 are also absent from this corpus, and that is the row the Austrian case suggests is most likely to repay work.

No claim is made here about what Gödel actually found. `academia/naturalization-1947.md` records that no source establishes it, that the notebooks covering the period are in Gabelsberger shorthand and untranscribed for the relevant pages, and that the naturalization file at the National Archives appears never to have been requested. This folder reconstructs what was available to be found. That is a different question from what he found, and conflating the two is how the existing literature on this subject fills up.
