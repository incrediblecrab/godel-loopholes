# Analysis

This folder holds what we found by looking. `method/` holds how to look, `corpus/` holds the texts, `academia/` holds what has already been said about them. Analysis is the only one of the four that produces claims of our own, so it is the only one that can be wrong in an interesting way.

## One folder per snapshot, named identically

Every folder here takes the name of a corpus snapshot, exactly: `corpus/united-states-1947` is analyzed in `analysis/united-states-1947`. No suffixes, no reordering, no abbreviations.

The point is that the pairing stays mechanical. A corpus folder with no sibling here has not been examined, and that is visible at a glance rather than by reading anything. Coverage is a property of the directory listing.

A snapshot is a vantage: a jurisdiction at a year, holding what was in force then. Analysis inherits that vantage and may not reach outside it. An argument about the 1947 United States that depends on the Twenty-fifth Amendment is not a hard argument, it is an anachronism, and the folder name is what catches it.

## What belongs here rather than in method

The test is whether the file would change if you swapped countries. If it would, it belongs here. If it would not, it belongs in `method/`.

Procedures, templates and criteria are written once and applied many times, so they live in `method/`. Everything about what a particular text says, and what follows from it, lives here.

## Modularity

Folders here do not reference each other and do not depend on being read in order. Each one stands alone, states its own vantage, and cites `corpus/` and `academia/` directly. Adding a jurisdiction means adding a folder and nothing else: there is no index to update, no ordering to maintain, and no file that has to know how many analyses exist.

This is deliberate. The long-term shape of this project is many jurisdictions at many vantages, and any structure with a central registry becomes the bottleneck and then the stale file. There is no such file here.

The cost is duplication. Two folders examining similar amendment procedures will repeat themselves. That is accepted, because a folder that cannot be read on its own is worse than one that repeats a paragraph.

## Null results are written down

Most attempts will fail, and the failures are the more useful half of the record. A line of attack that was tried and did not work is recorded with enough detail that no one walks it again, including ours.

A folder containing only successes is not a research record. It is a highlight reel, and it invites the failure mode this project was built to avoid: generating many confident claims quickly, none of which anyone can check.

## Every candidate carries its own disqualification

No claim is recorded here without the text and recension it depends on, the step in it that a competent opponent would attack first, and what would have to be true for it to be wrong.

A candidate that cannot be stated in a form that could be refuted is not a finding yet, and it stays out until it can be.
