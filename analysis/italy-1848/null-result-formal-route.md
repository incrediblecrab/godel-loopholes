# Null result: the formal route against a flexible constitution

Every enumeration in `method/enumerations.md` was run against `corpus/italy-1848/03-04-1848-statuto-albertino-wikisource-transcription.txt`. This file records what each returned. The purpose is not to document diligence. It is that the pattern of returns is itself a signal, and once named it can be checked in a few minutes before any analysis is undertaken.

## Power inventory

Returns a full table. The Statuto confers substantial powers: Art. 3 vests legislative power collectively in the King and two chambers, Art. 5 gives the King alone the executive power, supreme command of land and sea forces, the power to declare war and to make treaties, and Art. 6 gives him appointment to all offices of state and the making of decrees and regulations necessary for the execution of the laws.

Art. 6 also carries a limit, and it is a well-drafted one. The King makes such decrees *senza sospenderne l'osservanza o dispensarne*, without suspending the observance of the laws or dispensing from them. That is an explicit prohibition on the two historical abuses of the executive decree power, written in 1848. It appears to have held, and it did not matter, because the route to dictatorship ran through legislation rather than through decree, and a limit on decree power constrains nothing when the legislature is producing what the executive wants.

Another limit in the same document was not honoured at all, and it is the more instructive of the two. Art. 71 provides that no one may be removed from their natural judges and that extraordinary tribunals or commissions may therefore not be created. `academia/interwar-collapse.md` records the *leggi fascistissime* of 1925 and 1926 creating the Special Tribunal. That is as direct a contradiction of an unambiguous constitutional prohibition as this corpus contains.

Nothing followed from it, and the reason is the point of this whole folder. In a flexible constitution a later ordinary statute that contradicts a constitutional article is not a breach requiring justification. It is an implied amendment, valid on the ordinary principle that the later law prevails, because the document contains nothing that ranks itself above ordinary legislation and no organ empowered to say otherwise. Art. 70 makes this concrete from the other direction: the judicial organization may be derogated from *in forza di una legge*, by force of a law, which is the constitution itself pointing at ordinary legislation as the instrument for changing the courts.

So the pattern across the three cases needs stating carefully rather than tidily. In Germany and Austria the limits were obeyed and the state was reorganised around them. In Italy a limit was contradicted outright and the contradiction was lawful. What the three share is not that limits held, but that whether a limit held turned out to be uncorrelated with whether it protected anything. Any candidate anywhere in this project whose closing edit is a limit has to answer all three.

The sixth column, who can stop the power holder and what happens if the holder is hostile to them, returns the King and the chambers pointing at each other with no third party anywhere. There is no constitutional court, no judicial review, and no organ empowered to refuse effect to a statute. A search of the file for any language of interpretive authority returns nothing.

Verdict: produces output, and none of it is on the path.

## Threshold arithmetic

Returns empty, and this is the diagnostic.

There is no amendment procedure in the Statuto, so there is no amendment threshold, so there is no minimum coalition to compute for the act of changing the constitution. A search of all eighty-four articles for any language of revision, reform, modification or amendment returns zero occurrences.

An empty return here has exactly one cause and it is not a defect in the search. It means the document does not distinguish constitutional change from ordinary legislation, which means the threshold for constitutional change is the threshold for ordinary legislation, which is a bare majority. The enumeration that produces the most decisive number in every other case produces no number here because the number is the one every statute already meets.

Verdict: empty, and the emptiness is the entire finding.

## Reference graph

Returns a sparse graph with no cycles.

The German case turned on Art. 3 of the Enabling Act disapplying a range of constitutional articles that included the amendment article, which is a provision reaching itself. Nothing analogous is possible here. A self-reaching provision requires a provision that governs how provisions are changed, and there is none.

Verdict: structurally incapable of producing the finding it exists to produce.

## Undefined operative terms

Returns output of no consequence.

Terms are left undefined, as in any document of the period, and the second question the procedure asks, who defines them in practice and whether that definer is inside the set of actors being constrained, has the same answer for all of them. Parliament defines them, by statute, revisably, and no organ can refuse its definition. The undefined-term analysis collapses into the flexibility finding.

Verdict: subsumed.

## Parse enumeration

Not run past a first pass, deliberately.

With no entrenched provision anywhere in the document, no parse of any clause is more protective than any other, because the clause can be replaced by ordinary statute on either reading. The enumeration would have produced a substantial list of ambiguities at low cost, every one of them meaningless, and would have looked like work.

Verdict: refused on the grounds that a result here could not be a result about anything.

## Silence inventory

Returns everything, which is the same as returning the answer.

The Statuto does not reserve electoral law to itself, does not constrain the composition or election of the Chamber, does not entrench press freedom against ordinary legislation, does not protect political association, and does not fix the conditions under which the head of government holds office. `academia/interwar-collapse.md` records that these are precisely the fields the Acerbo Law of 1923, Law 2263 of 1925 and the *leggi fascistissime* of 1925 and 1926 legislated in, all by ordinary act, with the Statuto formally in force throughout.

Verdict: the only enumeration that fires, and it fires on absences rather than on text.

## What this yields for method

Five procedures returned nothing usable and one returned the whole answer, and the split is not random. Every enumeration that operates on the presence of constitutional text failed, and the single one that operates on the absence of it succeeded. That is a description of a flexible constitution, and it means the formal apparatus can be short-circuited by a test that costs almost nothing.

Before running any analysis, search the document for its amendment procedure. If there is none, or if the procedure is the ordinary legislative procedure, the document is flexible and the entire formal route is a category error against it. Go directly to the silence inventory, and understand that the answer will not be in the constitution at all but in the statute book, which means the corpus for that jurisdiction has to hold statutes before anything can be said.

The reason this belongs in an analysis folder rather than in `method/` is that it was not known in advance. It was produced by running six procedures against a real document and watching five of them fail in the same direction. Whether it graduates into `method/` should depend on it surviving a second flexible constitution, not on how convincing it sounds after one.

## What this case does not show

It does not show that flexible constitutions are more dangerous than rigid ones. Three cases, one of each relevant kind, cannot support that, and the honest statement is narrower: the method this project is building sees rigid constitutions and is blind to flexible ones, so its coverage is uneven in a way that has nothing to do with where the risk is. A survey of many constitutions that reports findings only against the rigid ones would be reporting a property of the instrument.

It also does not show that the Statuto was well made. It shows that the question the method asks was not answerable about it.
