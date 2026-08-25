# Enumerations

Brute force is the project's stated method, and this file says what can actually be enumerated over a constitutional text, what each enumeration costs, and where each one terminates. The last part matters most. An enumeration that terminates in a document rather than in a disqualification has produced volume, and volume is the failure this project was built to avoid.

Every procedure below ends by handing its output to the disqualifiers in `what-counts-as-a-finding.md`. None of them ends by writing anything down.

## The power inventory

Walk the document clause by clause. Wherever a clause confers a power on anyone, record six things: who holds it, what condition opens it, what it reaches, who can stop it, what bounds it in time, and what happens to the stopper if the person holding the power is hostile to them.

The sixth column is the one that does the work, and it exists because of the third failure mode in `attack-surfaces.md`. Both interwar enabling instruments carried a parliamentary revocation check, and a table with five columns records both as checked. A table with six records that the check fires only if a legislature is sitting, and that whether it sits is not under the legislature's own control.

Cost: linear in the document, and a few hundred rows for a constitution of this size. This is the cheapest of the enumerations and should be done first, because every later procedure reads from it.

Terminates in: rows where the sixth column is empty or self-referential.

## Threshold arithmetic

Extract every numeric threshold in the document and convert each to a count of human beings at the stated vantage. This is the enumeration that produces the minimum coalition number that `what-counts-as-a-finding.md` demands of every candidate, and it is pure arithmetic, so it is the least arguable thing this project does.

It is also strictly vantage-dependent, which is the reason snapshots are keyed to years. In 1947 there were forty-eight states, so two thirds of the state legislatures is thirty-two and three fourths is thirty-six. In 2026 the same two fractions are thirty-four and thirty-eight. The clause did not change; the arithmetic did. An analysis that reports the modern numbers under a 1947 vantage has made exactly the error the folder names exist to catch.

The more interesting output is not the numbers but the cases where the document does not say what the fraction is a fraction of. Article V requires that two thirds of both Houses deem an amendment necessary and does not state whether that is two thirds of the membership or two thirds of those voting. Weimar Article 76 states its base explicitly, requiring that two thirds of the statutory membership be present and that at least two thirds of those present assent. The same fraction, and only one of the two documents says what it divides. A silence of that kind is worth more than the number.

Cost: trivial. Terminates in: the minimum coalition figure, and a list of fractions with unstated bases.

## The reference graph

Every internal cross-reference is an edge. Build the directed graph and look for cycles, and in particular for any provision that can reach itself.

This is the formal route in its most tractable form, and it is not hypothetical. Article 3 of the Enabling Act disapplied Articles 68 to 77 of the Weimar constitution to laws made by the government, and Article 76, the amendment procedure under which the Enabling Act itself had just been passed, sits inside that range. The rule was used to disable the rule. That is a cycle, and it is visible in the reference graph of two documents read together, which is an argument for building the graph across a whole snapshot rather than across the constitution alone.

Cost: linear to build, and cycle detection is cheap. Terminates in: self-reaching provisions and the paths that reach them.

## Undefined operative terms

List every term that carries legal weight in an operative clause and is not defined anywhere in the document. Then ask, for each, who decides what it means, and whether that decider is inside the set of actors the clause is meant to constrain.

The second question is the point. An undefined term is harmless when a body outside the dispute settles it and dangerous when the party exercising the power also defines its scope, which is the self-judged trigger from `attack-surfaces.md` arriving by another route.

Cost: linear, but the judgment about what counts as operative is real and should be recorded rather than assumed. Terminates in: terms whose definer is also the actor being constrained.

## Parse enumeration

For every operative clause containing a structural ambiguity — a comma that could bound one clause or another, a coordination with more than two members, a modifier that could attach at more than one level — enumerate the readings and state what each would permit.

This is the only enumeration here that explodes. A clause with several independent ambiguities has a number of parses exponential in that count, and almost all of them are absurd. The discipline is that a parse is not a candidate until someone competent has argued for it or a recension supports it, and the corpus already supplies both kinds of evidence: the Seventh Amendment exists in three punctuations across authoritative printings, and the paired commas at 1 Stat. 98 make a different grammatical claim about what the re-examination clause restricts than the parchment does.

Run this only on clauses the power inventory has already marked as consequential. Running it across a whole document first is the fastest way to generate a great deal of unfalsifiable material.

Cost: exponential if unbounded, which is why it is bounded. Terminates in: parses supported by a recension or by published argument, and nothing else.

## The silence inventory

List the fields the document does not reserve to itself, where ordinary legislation governs and no constitutional provision constrains what that legislation may say.

This is the only procedure here that can see the third class in `attack-surfaces.md`, and it is the one most easily skipped, because its input is an absence. Italy is the reminder: everything that dismantled the Italian state was an ordinary statute, and the constitution's silence about electoral law is the entire reason the 1923 electoral law could hand two thirds of the Chamber to a quarter of the vote without amending anything.

An honest silence inventory requires knowing what the statute book contained, which means the snapshot must hold statutes in force and not constitutional text alone.

Cost: bounded by the document but requires external knowledge to interpret. Terminates in: fields where a bare legislative majority can alter the conditions of its own re-election or tenure.

## What brute force does not license

None of these procedures produces a finding. They produce a shortlist, and the shortlist is worthless until each entry has been through the disqualifiers: whether a step breaks a rule, whether an edit to the text would close it, how large the minimum coalition is, whether the literature already named it, and what would falsify it.

The reason to say this here is that enumeration is the part of the work that feels most like progress and is the easiest to automate. A table of four hundred rows looks like a result. It is an input, and treating it as a result is how a project like this fills up with material that no one can check.
