# Germany, 1933

This is a validation case, not a discovery. The outcome is known, the mechanism is documented, and the reason to work it is to find out whether the procedures in `method/` recover the path without being told the answer. A method that cannot reconstruct a collapse that already happened, from texts that were public at the time, has no claim on a case where the answer is unknown.

## Vantage

The snapshot is Germany at the end of 1933, and it holds four files in `corpus/germany-1933/`: the Weimar constitution in the gazette transcription and in the 1922 McBain and Rogers English translation, the Reichstag fire decree of February 28, and the Enabling Act of March 24.

The constitution sits in the snapshot alongside the two statutes because it was never repealed. It remained nominally in force through everything that followed, and that is the fact the folder exists to make unavoidable. Nothing here required removing the constitution. The path ran through it.

Scoring is retrospective, which is a real hazard and is named here rather than in a footnote. A method built against cases whose answers are known will tend to fit those answers. The protection is not in this folder; it is that Italy is held out as a case where the method is predicted to fail, and a method that appears to succeed everywhere has been fitted rather than tested.

## Result

The path is reconstructed step by step in `path-enabling-act.md`. In summary: the procedures recover it, and the reference-graph enumeration finds the decisive step without any historical knowledge at all, because the step is visible as a cycle in the text of two documents read together.

Two things came out of the reconstruction that were not in the account this folder started from.

The first is arithmetic. Article 76 is universally described as a two-thirds amendment rule, and it required both a two-thirds quorum and two thirds of those present. Those compose. Two thirds of two thirds is four ninths, so the constitution could be amended by the assent of about forty-four percent of the statutory membership, which is less than half. The rule that is supposed to protect the document against a majority could be satisfied by a minority. This falls straight out of the threshold-arithmetic procedure and requires nothing but the clause and multiplication.

The second is that the Enabling Act carried substantive limits, and they held, and it did not matter. Article 2 exempted the institution of the Reichstag and the Reichsrat as such and preserved the rights of the Reichspräsident. Both were in fact respected. The institutions continued to exist and the presidency was untouched until Hindenburg died. The limits were obeyed and the state was reorganized anyway, which is the same result the Austrian enabling act produced under three limits that were also never repealed. Two independent instances of the same pattern is enough to treat it as a finding about limits rather than an accident of two cases.

## What the method would have missed

Everything that made the vote possible. The exclusion of the Communist deputies, the arrests, the pressure in the chamber, the fire decree's suspension of the rights that would have protected the opposition — none of that is recoverable from clause structure, and a text-only procedure that scored the Weimar constitution in 1932 would have produced a list of structural weaknesses with no way to say that any of them was about to be used.

That is the honest boundary of the formal route, and it is why `method/attack-surfaces.md` treats political likelihood as outside the taxonomy rather than as a factor to be estimated. The method can say a door is unlocked. It cannot say anyone is coming.

## Null results

The fire decree was checked for the failure mode where a power exceeds an enumerated list, and on the enumeration it is clean. Article 48(2) names seven articles whose rights may be suspended, and § 1 of the decree suspends those seven, correctly cited, with nothing added. Looking for the obvious violation here produces nothing, which is worth writing down, because the obvious violation is what a first pass looks for and its absence is what makes the actual defect easy to walk past. The actual defect is one word away and is recorded in the path file.

That null result does not extend to the whole decree. Article 48(2) contains two grants, a general power to take measures necessary to restore public security and order and a specific power to suspend the seven listed rights, and only the second is bounded by a list. Section 2 of the decree, which lets the Reich government assume the powers of the highest authority of a Land, is not covered by the enumeration and has to rest on the general limb. Whether it does is contestable, and it is left contested here rather than resolved, because the honest answer from the text alone is that the general limb has no stated boundary and therefore cannot be shown to have been exceeded. A power that cannot be exceeded is a finding in its own right, and it is the first failure mode in `method/attack-surfaces.md` rather than the fourth.

Article 48(3) was checked as a candidate for a missing check and is not one. The Reichstag could demand the decree's revocation, the provision is sound on its face, and it was never amended or repealed. It failed for a reason that is not visible in its own text, and that reason is the subject of the third step in the path file.

Article 48(3) was checked as a candidate for a missing check and is not one. The Reichstag could demand the decree's revocation, the provision is sound on its face, and it was never amended or repealed. It failed for a reason that is not visible in its own text, and that reason is the subject of the third step in the path file.
