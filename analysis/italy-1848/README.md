# Italy, 1848

This is the control case, and it is the only one of the three where the method is supposed to fail. Germany and Austria can both be recovered by careful reading. Italy cannot, and a version of this project that reported a finding here would have proved that its procedures generate results from any input, which is the specific failure the whole apparatus is built to avoid.

The value of the folder is therefore the shape of the failure. A method that fails in a predicted, diagnosable way is usable. A method that simply returns nothing is not, because in the field there is no answer key to tell the two apart.

## Vantage

The snapshot is the Kingdom of Sardinia at the Statuto's promulgation in 1848, and it holds three files in `corpus/italy-1848/`: the Statuto Albertino in the Italian transcription, the 1894 Lindsay and Rowe English translation, and the February 8 proclamation of the bases that preceded it.

The Statuto is the right text to analyse for a collapse eighty years later because it was never amended. `academia/interwar-collapse.md` establishes that its eighty-four articles remained formally in force through the entire fascist period, which is confirmed here: the corpus file contains eighty-four articles and the last is Art. 84.

No Italian statute of the fascist period is in the corpus, for reasons recorded in `corpus/README.md`. Everything below about the Acerbo Law and Law 2263 of 1925 rests on `academia/interwar-collapse.md` and is marked where it occurs.

## The result

Every enumeration in `method/enumerations.md` was run against the Statuto. The outputs are recorded in `null-result-formal-route.md`. Five of the six return nothing usable, one returns the entire answer, and the pattern of which is which turns out to be a diagnostic that can be run before any analysis begins.

The decisive one is threshold arithmetic, and it is decisive because its output is empty. There is no amendment threshold in the Statuto because there is no amendment procedure. A search of the corpus file for any language of revision, reform, modification or amendment returns zero occurrences across all eighty-four articles.

That empty return is not a failure of the search. It is the finding. A constitution with no amendment procedure is not thereby harder to change; it is changeable by ordinary legislation, which is what `academia/interwar-collapse.md` records La Spina naming as flexibility as against rigidity. The absence that a rigidity-seeking method reads as nothing to report is the reason nothing needed to be reported.

## The strongest entrenchment language in the corpus did nothing

The Statuto's preamble declares it a Statuto and Fundamental Law, *perpetua ed irrevocabile*, perpetual and irrevocable, of the Monarchy.

No text in this corpus makes a stronger claim about its own permanence, and no text in this corpus was set aside more completely while remaining formally in force. The words were in the document the entire time. They did nothing, because nothing in the eighty-four articles said what procedure could or could not alter them, and a declaration of irrevocability with no procedure attached is a description of an intention rather than a rule anyone can apply.

This is worth carrying into every later analysis. Entrenchment is not a matter of emphatic language. It is a matter of whether some identifiable actor is empowered to refuse to give effect to a change, and by what test. The Statuto names no such actor and states no such test, and its preamble is the most forceful thing in the corpus.

## Minimum coalition

`academia/interwar-collapse.md` records the Acerbo Law of November 18, 1923 awarding two thirds of the seats to any list taking more than a quarter of the vote, and Law 2263 of December 24, 1925 making the head of government answerable to the King alone and removing Parliament's power to dismiss him. Both are ordinary statutes.

So the minimum coalition is a bare majority of a chamber, used once to pass an electoral law, after which something above a quarter of the votes cast delivers two thirds of the seats. The units differ from the German case and the comparison has to be made carefully, but the direction is not in doubt: Germany's path required the assent of forty-four percent of a chamber at its arithmetic minimum, and Italy's required a plurality of voters and a chamber majority willing to legislate its own succession.

The general point is the uncomfortable one. Across the three cases, the constitution with no entrenchment at all had the lowest threshold, and its lack of entrenchment is precisely why a formal analysis of it finds nothing to criticise.

## Null results

The Statuto was examined for internal contradiction between the royal prerogative articles and the parliamentary articles, on the theory that a document granting both extensive Crown powers and parliamentary government must conflict somewhere. Tensions exist and none of them is on the path. `academia/interwar-collapse.md` records Lyttelton establishing that the regime preserved constitutional continuity deliberately, in order to retain the monarchy, the bureaucracy and conservative elites, which means the Crown's powers functioned as an asset to be kept rather than an instrument to be abused. Looking for the contradiction was the right instinct applied to the wrong document, and it cost real time.

Parse enumeration was not run past a first pass. With no entrenched provision anywhere in the text, no reading of any clause can be more or less protective than any other, since the clause can be replaced by ordinary statute whichever way it parses. This is the clearest case in the project so far of an enumeration that is cheap to run, guaranteed to produce output, and guaranteed that none of the output means anything. It is exactly the volume problem, and the only thing that stopped it was asking first what a result would be a result about.
