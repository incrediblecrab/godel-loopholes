# Replicating a changing-state-universe argument

**The fixed forty-eight-state model does not exhaust Article V's arithmetic.**
Article IV gives Congress a power that can change the set of states over which
Article V counts. A published Harvard Law Review Note explicitly proposes
using that interaction. Its arithmetic can be reproduced conditionally; its
headline minimum cannot be uniquely reconstructed from the inputs it publishes.
Neither result establishes an unambiguously lawful route to dictatorship.

This is a new surface for this repository's executable search, not a claim of
novelty in constitutional scholarship. The mechanism is already the subject
of the paper being replicated.

## The academic source, read rather than inferred from its title

The source is the unsigned Note,
[Pack the Union: A Proposal to Admit New States for the Purpose of Amending
the Constitution to Ensure Equal Representation](https://harvardlawreview.org/print/vol-133/pack-the-union-a-proposal-to-admit-new-states-for-the-purpose-of-amending-the-constitution-to-ensure-equal-representation/),
133 Harvard Law Review 1049-1070, published January 10, 2020. It is a law-review
Note, not an externally peer-reviewed mathematical proof or a formally
verified computational paper.

The full article and its footnotes were read. Printed page 1060, footnote 94,
was checked against the rendered PDF image. The primary PDF checksum and
the exact reconstruction inputs are in `search/state_admission_results.json`.
The PDF is not redistributed in the repository.

Part II.A proposes reducing the federal district and admitting its remaining
neighborhoods as new states. The text proposes 127 neighborhoods and footnote 94
says that a minimum of 96 new states would suffice using figures from the last
period of unified Democratic federal control. It does not supply a roster
date, the exact congressional inputs, an attendance convention, a state
ratification table, or executable calculations.

Part II.B then proposes substantive amendments, including transferring the
Senate's powers while retaining equal state suffrage. Part III.A.2 expressly
recognizes the formalistic nature of that workaround. Footnote 98 cites
Douglas Linder's 1981 discussion and acknowledges his qualification concerning
an intention to reduce small-state influence. The Note's defenses also appeal
to contested historical legitimacy and political desirability. They must not
be silently converted into the stronger claim that every step is indisputably
legal.

Its intended policy objective is equal representation, **not dictatorship**.
The transferable method is the interaction between membership rules and
amendment thresholds. Testing a different terminal objective is our extension,
not a result attributed to the Note.

## Exact arithmetic, with the denominator allowed to change

Let `N` be the initial number of states, `r` the original states supporting
ratification, and `k` the number of additional states. **Assume** that every new
state ratifies. Then:

```text
r + k >= ceil(3(N + k)/4)
iff 4(r + k) >= 3(N + k)
iff k >= 3N - 4r.

Minimum nonnegative k = max(0, 3N - 4r).
```

The new states count in both the numerator and the denominator. Keeping the
original denominator is the attractive but incorrect shortcut.

The implementation checks this equivalence with a general integer Z3 query
and checks feasibility plus the immediately smaller count across 20,300
`(N, r)` cases, for `N` from one through two hundred. These are arithmetic
boundary cases, not 20,300 historical observations.

At the 1947 vantage, the **ratification-only** frontier includes:

| Original ratifying states | Additional states, all assumed supportive |
|---|---|
| 0 | 144 |
| 1 | 140 |
| 35 | 4 |
| 36 | 0 |

Those numbers do not include the congressional proposing stage, legal
authorization of admission, state formation, or electoral outcomes.

## The House gate cannot be omitted

Under the stated convention that each additional state receives one new House
seat while existing seats remain, let `H` be the initial House size and `h`
its supporting members. With full attendance:

```text
3(h + k) >= 2(H + k)
iff k >= 2H - 3h.
```

New senators similarly increase both the Senate's supporting bloc and its
membership. The program checks House proposal, Senate proposal, and state
ratification **jointly**, and separately requires the original Congress to be
able to authorize admission. Future delegations cannot vote themselves into
existence.

Two deliberately hypothetical 1947 input sets illustrate why this matters.
They are not reconstructions of an actual political coalition.

| Inputs before admission | Joint minimum additional states | Binding gate |
|---|---|---|
| 218 House supporters, 49 Senate supporters, one original ratifier; full attendance; presidential cooperation | 216 | House proposal |
| 110 House supporters, 25 Senate supporters, one original ratifier; favorable minimum-quorum attendance; presidential cooperation | 140 | State ratification |

The second row is **blocked before admission** if the same small bloc must
supply its own quorum, or if the President refuses cooperation and an
override is required. The old Congress's legislative voting condition is
not a cost that can be paid by the new Congress.

"Favorable minimum quorum" assumes that enough non-supporters attend to make
a quorum, while enough others do not attend to keep the threshold low.
It is not a guarantee against opponents who choose a different attendance
strategy. Neither scenario resolves agenda control, cloture, other standing
rules, or the timing of seating new delegations. Vice-presidential
tie-breaking is not modeled.

## Does the published minimum of 96 replicate?

**Not as a uniquely identified historical calculation.** It is compatible
with one explicit reconstruction:

| Initial parameters, all hypothetical except the stated starting sizes | Joint minimum |
|---|---|
| 50 states; 435 House seats; 258 House supporters; 60 Senate supporters; 14 original ratifying states; full attendance | 96 |
| Same, but 257 House supporters | 99 |

The official House historian's
[party-division table](https://history.house.gov/Institution/Party-Divisions/Party-Divisions/)
lists 257 Democrats for the **initial election results** of the 111th Congress.
It expressly does not track every subsequent vacancy, special election or
party change. This does not refute a calculation using some other date; it
means that silently selecting 258 to force agreement would be inappropriate.
The other two support figures in the table above are conditional inputs,
not historical measurements supplied by that House source.

The proposed 127-state example is also conditional. Starting from fifty
states, it yields 177 states, a ratification threshold of 133, and a need for
six original ratifiers if every new state ratifies. With the one-extra-House-
seat convention and full attendance, it still needs 248 original House
supporters. "127 new states suffice" is not a statement independent of the
original supporting coalition.

The honest replication status is therefore: **the mechanism and its
parameterized arithmetic reproduce; the exact historical inputs behind the
published 96 are underdetermined.** This is not evidence that 96 is necessarily
wrong.

## A primary-source historical denominator control

The Sixteenth Amendment supplies a real, pre-1947 control for the changing
denominator. It was proposed in 1909. New Mexico became the forty-seventh
state on January 6, 1912, and Arizona the forty-eighth on February 14, 1912.
The Senate's official histories supply those admission dates
([New Mexico](https://www.senate.gov/states/NM/intro.htm),
[Arizona](https://www.senate.gov/states/AZ/intro.htm)).

The certification of February 25, 1913 was read from the complete rendered
page image of [37 Stat. 1785](https://www.govinfo.gov/content/pkg/STATUTE-37/pdf/STATUTE-37-Pg1785.pdf).
It enumerates a principal list of thirty-six states and states that these
constitute three-fourths of the whole number of states. It separately
acknowledges ratifications by New Jersey and New Mexico. Accordingly the page
acknowledges **38** ratifications in all; **36** is the principal list and the
constitutional threshold, not a claim that no other state had ratified.

`search/sixteenth-denominator-case.json` transcribes the names and provenance.
The program checks the distinct-name counts and recovers the change from
`ceil(3*46/4) = 35` to `ceil(3*48/4) = 36`.

A synthetic one-short control is then rejected by the current denominator
and wrongly accepted by a frozen original denominator. That control is
explicitly **not** asserted to describe the ratification count on a particular
historical day.

This is one historical arithmetic check. It is not a successful historical
backtest of engineered state creation, a predictor of constitutional collapse,
or validation of the Note's electoral assumptions.

## The legal bottleneck survives the arithmetic

[Article IV, Section 3](https://constitution.congress.gov/browse/article-4/section-3/clause-1/)
authorizes admissions and requires the consent of concerned state legislatures
when territory is taken from existing states. It does not itself specify
that a newly admitted state's voters, legislators or convention delegates
will support a later amendment.

The distinction is not merely practical. In *Coyle v. Smith*, 221 U.S. 559
(1911), the Court rejected a congressional restriction on Oklahoma's power to
move its capital. The operative discussion at pages 567-568 was read from
the [official reporter images](https://tile.loc.gov/storage-services/service/ll/usrep/usrep221/usrep221559/usrep221559.pdf).
It explains the equal sovereignty of admitted states and the continued
amendability of their constitutions after admission.

That decision did **not** adjudicate a condition requiring a particular
Article V ratification. It is relevant counter-authority to any easy inference
that Congress may create permanently subordinate, obedient ratification units.
It is not presented here as a holding on a case the Court never heard.

The program therefore keeps new-state support as an assumption. Removing it
produces a counterexample: admission can occur while every new state declines
the proposed amendment. For an original coalition below three-fourths,
admitting arbitrary non-supporting states never guarantees ratification.
This failure of a guarantee does not disprove an **existential** path with
cooperative new states; it exposes a political premise that arithmetic cannot
derive.

The equal-suffrage objection also remains. Composing the expanded support
sets with the finite interpretation model yields the same qualitative
two-by-two: formal-scope transfers need no repeal; functional scope needs
repeal; functional self-entrenchment blocks the transfer where original
affected states have not consented. Admitting more states does not manufacture
consent from a dissenting original state.

Finally, the Note's district-neighborhood boundaries and election evidence are
from 2010 and 2016. They are not a verified 1947 partition or 1947 political
evidence. The model applies the abstract arithmetic to the earlier snapshot,
not those later facts. The retrospective discussion of Article IV in today's
Constitution Annotated is a finding aid; it is not itself pre-1947 law.

## Reproduction and outcome

```sh
.venv/bin/python -m unittest discover -s analysis/united-states-1947/search -p 'test_state_admission.py' -v
.venv/bin/python analysis/united-states-1947/search/state_admission.py --check
```

Use `--write` to regenerate the canonical result artifact after a deliberate
change. Independent enumeration and integer optimization must agree; a second
SMT query excludes every smaller solution. Unknown solver outcomes are errors
to resolve, not claimed minima.

The research contribution is a boundary correction: a requirement for
three-fourths of the **current** states is not a timeless requirement to obtain
thirty-six of the **original 1947** states. The expanded model also shows why
that correction is not a completed loophole. It leaves the law of admission,
political support, all congressional gates, equal-suffrage interpretation,
and historical attribution to be established rather than wished away.
