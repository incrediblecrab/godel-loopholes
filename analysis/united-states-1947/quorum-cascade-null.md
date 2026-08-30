# The quorum cascade is strictly dominated — a null result

`silence-inventory.md` rows 4, 5 and 6 are the only entries in that table a single chamber can alter with no concurrence from anyone: no other chamber, no President, and on the 1947 law no court. Chained, they appear to say that the denominator of Article V's fraction is set by the body the fraction is meant to constrain. `search/quorum_cascade.py` turned that into numbers and got the congressional stage down from 179 individuals to 4.

It has been carried to a verdict. **The cascade fails.** It fails on arithmetic, not on law, and the arithmetic was in the script's own committed output from the first day, unremarked.

This file is written to `method/what-counts-as-a-finding.md`, which requires a closed path be recorded in the same detail as an open one.

## The text and the recension

Article I, Section 5 and Article V, from `corpus/united-states-1947/09-17-1787-constitution-parchment-nara-transcription.txt`. Nothing here turns on punctuation, so the recension disagreements catalogued in `corpus/README.md` do not bear on it. Vantage December 5, 1947.

## The path, as numbered steps

**Step 0. Exclude, at the organisation of a new Congress, by simple majority.** Authorized by Article I, Section 5, clause 1: each House "shall be the Judge of the Elections, Returns and Qualifications of its own Members." A member-elect who is not seated is never sworn.

**Step 1 and after. Expel sitting members, at two thirds of those present.** Authorized by Article I, Section 5, clause 2: "with the Concurrence of two thirds, expel a Member."

**The effect being sought.** Each removal lowers the number of members chosen and sworn, which lowers the quorum, which lowers two thirds of the quorum, which is the Article V proposing threshold under *National Prohibition Cases*, 253 U.S. 350 (1920). Run to exhaustion the script drives the House to 2 members and the Senate to 2, and the congressional price of an amendment from 179 individuals to 4.

## The legal status of each step

**The premise under all of it — that the quorum base is members chosen and sworn rather than the statutory size of the chamber — is SETTLED, and settled in the cascade's favour.** This was the open question the whole exercise waited on, and it resolved the way the cascade needed. Hinds' *Precedents* volume 4, section 2889 (House, Speaker Cannon, March 16, 1906) and section 2891 (Senate) both hold that vacancies and unsworn members-elect come out of the denominator. Verified from page images and written up in `quorum-base.md`, with a caveat there about the quality of the available scan.

**Step 0 is CONTESTED, and the strongest published argument on the other side is five years before the vantage.** Both chambers had in fact excluded members-elect by simple majority on grounds found nowhere in Article I, Section 2 — Roberts in the House in 1900 for polygamy, Smith in the Senate in 1928 and Vare in 1929 for campaign expenditure. But on March 27, 1942 the Senate, confronted with a committee report recommending that William Langer of North Dakota "be excluded by a majority vote" for moral unfitness while conceding he met every constitutional qualification, **rejected the part of the resolution asserting that a simple majority sufficed**, held that the case was therefore an expulsion requiring two thirds, and then declined to remove him 30 to 52. The Senate Historical Office's account records that the minority's argument — "new qualifications for a Senate seat could not be added to those set by the Constitution" — "won out."

Sourcing note, and it matters: the Langer account above is the Senate Historical Office's, from *United States Senate Election, Expulsion and Censure Cases: 1793-1990* (GPO, 1995), pages 368 to 370, read through senate.gov. It is a secondary source and it has **not** been checked against the Congressional Record for March 27, 1942. The same is true of the vote counts for Roberts, Smith and Vare. *Powell v. McCormack*, 395 U.S. 486 (1969), which would settle the question, is twenty-two years past the vantage and may not be used.

**Steps 1 and after are SETTLED as to authority and fatal as to price.** Expulsion at two thirds is on the face of clause 2 and nobody disputes it. The difficulty is that it is expensive, and see below.

**A step the script does not model at all: the seats refill, and the chamber cannot stop it.** Article I, Section 2, clause 4 puts House vacancies in the hands of state executives by writ of election, and the Seventeenth Amendment does the same for the Senate including temporary appointment where the legislature has authorized it. In 1947 a Senate seat could be refilled by gubernatorial appointment in a matter of days — Milton Young of North Dakota was appointed nine days after John Moses died — in what appears to be forty-five of the forty-eight states. House seats took longer, six to twenty-two weeks in 80th Congress practice. In neither case does the emptying chamber have any say in the refilling; it can only refuse to seat the replacement, which costs another vote, against a governor who can simply appoint again. The House did exactly this to Victor Berger twice, in November 1919 and January 1920, and the seat stayed empty — so the manoeuvre is possible, but it is a standing expense, not a one-time one.

Sourcing note again: the count of forty-five of forty-eight states is **reconstructed backwards from modern data** and is not primary-source verified. It is reported here because it is the honest state of the evidence, not because it is load-bearing — nothing below depends on it.

## Why it closes: the minimum coalition is larger than the thing it buys

The disqualifier in `method/what-counts-as-a-finding.md` is that a candidate needing an enormous coalition is Article V working as designed. This one is worse than enormous. It is self-defeating, and provably so.

Let `n` be the members a chamber has as it stands. A quorum is a majority of them. The Article V proposing threshold, under the 1920 reading and with a coalition sensibly arranging for exactly a quorum to be present, is two thirds of that quorum.

Any manoeuvre that changes who is a member is business of the chamber. It needs a quorum present, and the bloc driving it has to supply that quorum out of its own ranks, because the members it is removing will not stay to help make one. **So the entry price of the cascade is a quorum.**

And two thirds of a quorum is less than a quorum.

    for all n >= 4:   ceil(2 * (floor(n/2) + 1) / 3)  <  floor(n/2) + 1

`search/cascade_domination.py` proves this with Z3 for all `n` at once, checks it exhaustively for every chamber size to 200,000, and carries a negative control: dropping the `n >= 4` guard, the solver must and does return a counterexample, because 1, 2 and 3 genuinely are exceptions. A proof whose check cannot fail is not a check.

At the 1947 vantage:

| | House | Senate | total |
|---|---|---|---|
| carry an Article V proposal outright | 146 | 33 | **179** |
| merely begin the cascade | 218 | 49 | **267** |

**The cascade costs 88 members more than not running it.** Anybody who can assemble 267 members willing to purge Congress already had, among them, the 179 needed to propose the amendment on the first morning without touching anyone's seat. Every later step is cheaper than the one before, which is what made the trace look like a discovery, but the coalition has already been paid by then. The manoeuvre is strictly dominated at step zero, and no downstream saving can refund it.

This holds regardless of how Langer comes out, regardless of how fast seats refill, and regardless of the quorum base — it is arithmetic about the 1920 reading and nothing else. Three parallel research threads ran for over two hours each to settle questions the verdict did not need.

## The disqualifiers, applied

**Name the edit that closes it.** There is none to name, because there is nothing open to close. That is normally the fatal filter; here it is moot.

**Does it require only bad faith?** Substantially, yes. A chamber that excludes forty-seven senators-elect to lower its own quorum is not exploiting a defect in the text; it is doing something the text plainly contemplates being done for cause, without cause. `method/what-counts-as-a-finding.md` calls that a fact about power rather than about the document.

**Does it reach amendment?** No, and this was recorded before any of the above. Article V requires ratification by three fourths of the state legislatures, 36 of 48 in 1947. Nothing in the cascade approaches that number. It was confined to the proposing stage from the beginning.

## The falsifier

The theorem is arithmetic and falsifiable only by finding the encoding wrong; `cascade_domination.py` is the place to attack it, and its negative control is the place to start.

The premise beneath the theorem is the one to attack instead: that a bloc must supply a quorum from its own ranks. A manoeuvre that changed the membership **without** a vote of the chamber would escape it entirely. Nothing in Article I, Section 5 supplies one — that is the whole content of "each House shall be the Judge" — but a route through Article I, Section 4, where Congress may "make or alter" state regulations for congressional elections, would not be answered by this file. That is a different candidate and it has not been examined.

## What this cost, and the lesson

The refutation required no research at all. `quorum_cascade.json` has printed `"peak_coalition_total": 267` next to `"settled_1920_total": 179` since the day it was committed, and 267 is visibly larger than 179. The file was labelled `NOT A FINDING` for the right reason — an unverified premise — and that label did its job of keeping the numbers out of the analysis. But it also became a place to stop looking. The premise was interesting, so the premise got the attention, and the two numbers that killed the thing sat unread in the output of the script that produced them.

The general form is worth keeping: **when a result is quarantined pending one open question, check whether it is already dead for a reason that needs no question answered.** Quarantine is not the same as refutation and should not be allowed to feel like it.
