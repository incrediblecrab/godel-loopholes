# Quorum cascade: no verified path; the cost comparison is corrected

`silence-inventory.md` rows 4, 5 and 6 identify internal chamber powers that can affect membership, quorum, and proceedings. Their legal limits require separate examination. `search/quorum_cascade.py` generated an arithmetic relaxation whose congressional threshold falls from 179 to 4; it did not establish a lawfully reachable endpoint.

**The cascade remains unverified as a constitutional path. The earlier claim that it is strictly dominated on coalition cost is withdrawn.** The [consistent-attendance audit](attendance-consistency.md) identifies a mismatch in the comparison, while preserving the true scalar inequality. An invalid refutation is not a verified solution.

This file is written to `method/what-counts-as-a-finding.md`, which requires a closed path be recorded in the same detail as an open one.

## The text and the recension

Article I, Section 5 and Article V, from `corpus/united-states-1947/09-17-1787-constitution-parchment-nara-transcription.txt`. Nothing here turns on punctuation, so the recension disagreements catalogued in `corpus/README.md` do not bear on it. Vantage December 5, 1947.

## The path, as numbered steps

**Step 0. Exclude, at the organisation of a new Congress, by simple majority.** The proposed authority is Article I, Section 5, clause 1: each House "shall be the Judge of the Elections, Returns and Qualifications of its own Members." Whether this authorizes the contemplated exclusions is contested below.

**Step 1 and after. Expel sitting members, at two thirds of those present.** Authorized by Article I, Section 5, clause 2: "with the Concurrence of two thirds, expel a Member."

**The effect being sought.** Each removal lowers the number of members chosen and sworn, which lowers the quorum, which lowers two thirds of the quorum, which is the Article V proposing threshold under *National Prohibition Cases*, 253 U.S. 350 (1920). Run to exhaustion the script drives the House to 2 members and the Senate to 2, and the congressional price of an amendment from 179 individuals to 4.

## The legal status of each step

**The premise under all of it — that the quorum base is members chosen and sworn rather than the statutory size of the chamber — is SETTLED, and settled in the cascade's favour.** This was the open question the whole exercise waited on, and it resolved the way the cascade needed. Hinds' *Precedents* volume 4, sections 2889 and 2890 (House, Speaker Cannon, April 16, 1906) and section 2891 (Senate) both hold that vacancies and unsworn members-elect come out of the denominator. Verified from a photographic scan of the printing and written up in `quorum-base.md`.

**Step 0 is CONTESTED, and the strongest published argument on the other side is five years before the vantage.** Both chambers had in fact excluded members-elect by simple majority on grounds found nowhere in Article I, Section 2 — Roberts in the House in 1900 for polygamy, Smith in the Senate in 1928 and Vare in 1929 for campaign expenditure. But on March 27, 1942 the Senate, confronted with a committee report recommending that William Langer of North Dakota "be excluded by a majority vote" for moral unfitness while conceding he met every constitutional qualification, **rejected the part of the resolution asserting that a simple majority sufficed**, held that the case was therefore an expulsion requiring two thirds, and then declined to remove him 30 to 52. The Senate Historical Office's account records that the minority's argument — "new qualifications for a Senate seat could not be added to those set by the Constitution" — "won out."

Sourcing note, and it matters: the Langer account above is the Senate Historical Office's, from *United States Senate Election, Expulsion and Censure Cases: 1793-1990* (GPO, 1995), pages 368 to 370, read through senate.gov. It is a secondary source and it has **not** been checked against the Congressional Record for March 27, 1942. The same is true of the vote counts for Roberts, Smith and Vare. *Powell v. McCormack*, 395 U.S. 486 (1969), which would settle the question, is twenty-two years past the vantage and may not be used.

**Steps 1 and after have an express two-thirds requirement.** The existence of the expulsion power is not in doubt. Its initial voting threshold is the same as a direct proposal under the two-thirds-of-present convention used here, not automatically a higher price.

**A step the script does not model at all: the seats refill, and the chamber cannot stop it.** Article I, Section 2, clause 4 puts House vacancies in the hands of state executives by writ of election, and the Seventeenth Amendment does the same for the Senate including temporary appointment where the legislature has authorized it. In 1947 a Senate seat could be refilled by gubernatorial appointment in a matter of days — Milton Young of North Dakota was appointed nine days after John Moses died — in what appears to be forty-five of the forty-eight states. House seats took longer, six to twenty-two weeks in 80th Congress practice. In neither case does the emptying chamber have any say in the refilling; it can only refuse to seat the replacement, which costs another vote, against a governor who can simply appoint again. The House did exactly this to Victor Berger twice, in November 1919 and January 1920, and the seat stayed empty — so the manoeuvre is possible, but it is a standing expense, not a one-time one.

Sourcing note again: the count of forty-five of forty-eight states is **reconstructed backwards from modern data** and is not primary-source verified. It is reported here because it is the honest state of the evidence, not because it is load-bearing — nothing below depends on it.

## The arithmetic theorem survives; its former cost interpretation does not

Let `n` be a chamber's chosen-and-sworn membership and `q = floor(n/2) + 1` its minimum quorum. With exactly that quorum present, the two-thirds threshold is `ceil(2q/3)`. The following statement is true:

    for all n >= 4:   ceil(2 * (floor(n/2) + 1) / 3)  <  floor(n/2) + 1

`search/cascade_domination.py` verifies it with Z3, checks chamber sizes through 200,000, and finds a counterexample when the `n >= 4` guard is removed. Its exceptions are exactly 1, 2, and 3.

The former comparison treated the first expression as the direct-proposal coalition, with nonsupporters helping constitute a quorum, and the second as the cascade coalition, whose supporters must supply the quorum alone. Those are different attendance assumptions. Applying the same convention to both gives:

| Attendance | Initial majority exclusion | Direct proposal |
|---|---:|---:|
| Full membership | **267** | **354** |
| Favorable minimum quorum | **135** | **179** |
| Supporters alone supply quorum | **267** | **267** |

Thus a self-quorate bloc sufficient for an initial majority exclusion is also large enough for a direct proposal under that convention: there is no initial numerical saving. But the claim of an **88-member extra cost** does not follow. Under favorable quorum or full attendance, the initial majority threshold is lower. These comparisons assume the same willing bloc is assessed for the two actions; they do not establish political willingness or lawful exclusion grounds.

The correction concerns initial voting only. Subsequent removals, attendance, the continued existence of vacancies, and ratification are still unverified. The historical and legal questions cannot be dismissed by the old arithmetic argument.

## The disqualifiers, applied

**Name the edit that closes it.** No complete lawful path has been established to which a closing edit can yet be applied.

**Does it require only bad faith?** A proposed path must identify lawful grounds and authority for its exclusions, rather than assume a power to remove qualified opponents. The statutory text, contested precedents, and actual process must be checked separately.

**Does it reach amendment?** No. Ratification in 36 of the fixed 48 states remains necessary, by legislatures or conventions as Congress directs. This cascade calculation supplies neither mode's support.

## The falsifier

The scalar theorem is checked by `cascade_domination.py`. The cost interpretation is separately tested by `attendance_audit.py`, including an actual artifact-mutation control that rejects substitution of the favorable-attendance proposal price for the self-quorate price.

A completed cascade would need an explicit sequence satisfying the same attendance assumptions at every stage, lawful membership changes, and a defensible treatment of seat refilling. It would still not supply state ratification. The separate [Article I, Section 4 investigation](article-i-4-route.md) considers election legislation rather than shrinking membership.

## The methodological lesson

Comparing two printed numbers is not enough. Their units, attendance assumptions, decision stages, and quantified claims must also match. Here the numerical inequality was correct and the claimed interpretation was not.

**An unverified candidate is not a finding, and an invalid refutation does not turn it into one.**
