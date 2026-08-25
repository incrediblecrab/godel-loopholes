# United States, 1947

This folder is the reconstruction of what Gödel could have found, from the documents as they stood when he found it. It is the only analysis in this project where the answer is not known, which is why the three collapse folders were worked first: they exist to establish that the procedures recover a real path when one is there, and fail visibly when one is not.

## Vantage

The snapshot is the United States as of December 5, 1947, the date of the hearing, and it holds five files in `corpus/united-states-1947/`.

The vantage rule bites hardest here. Nothing forward of December 5, 1947 may enter an argument in this folder. The Twenty-second Amendment had been proposed in March 1947 but was not ratified until 1951 and is therefore not part of the document under analysis. There were forty-eight states, ninety-six senators, and four hundred thirty-five representatives, and every threshold in this folder is computed on those numbers rather than on modern ones.

Case law decided before the vantage date is admissible, and two decisions matter enough to name here. *National Prohibition Cases*, 253 U.S. 350 (1920), fixed the base of Article V's two-thirds requirement. *Schneiderman v. United States*, 320 U.S. 118 (1943), described Article V as carrying no substantive limitation beyond the Senate proviso, in a naturalization case decided under the same attachment standard Gödel was examined under four years later. Both are recorded in `academia/naturalization-1947.md`.

## What is here

`threshold-arithmetic.md` runs the threshold-arithmetic enumeration over Article V. It establishes that the article does not state the base of its fraction, that the Supreme Court settled the base as a quorum rather than the full membership in 1920, and that the congressional stage of Article V was therefore satisfiable in 1947 by 146 of 435 representatives and 33 of 96 senators.

It also records that the minimum-coalition argument this project treats as one of its own procedures was made to the Supreme Court by counsel in 1920, and lost. That is a direct hit on the novelty requirement in `method/what-counts-as-a-finding.md`, and it arrived before any candidate had been raised, which is the best possible time for it to arrive.

## What is not here yet

No candidate path. The remaining enumerations have not been run: the power inventory over the Article I and Article II grants, the reference graph, the undefined-terms pass, the parse enumeration over the clauses the power inventory marks as consequential, and the silence inventory.

The silence inventory is likely to be the most productive and is the one the Italian control case was worked to make unavoidable. Much of what would matter here is not in the constitution at all. The size of the House is statutory, the size and appellate jurisdiction of the Supreme Court are statutory, the rules of proceedings of each chamber are made by each chamber under Article I, Section 5, and the machinery of elections is largely left to the states. `corpus/README.md` records that this project holds constitutions and statutes but not chamber rules, and the Austrian case showed what that omission costs.

No claim is made here about what Gödel actually found. `academia/naturalization-1947.md` records that no source establishes it, that the notebooks covering the period are in Gabelsberger shorthand and untranscribed for the relevant pages, and that the naturalization file at the National Archives appears never to have been requested. This folder reconstructs what was available to be found. That is a different question from what he found, and conflating the two is how the existing literature on this subject fills up.
