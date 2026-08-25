# Corpus sources

Every file in this corpus is a transcription. None is a document. The distinction matters because this project reads punctuation, and punctuation is the first thing a transcriber changes, quietly and usually while trying to help. A missing comma on the 1789 parchment is a finding. A missing comma introduced by a volunteer proofreader in 2007 is noise. Telling the two apart requires knowing who set each text and from what, so that is what the entries below record.

Everything here was retrieved on August 24, 2026. Sources are ranked by transmission lineage rather than by the standing of the institution hosting them, which is not the obvious ordering and is defended under rejected sources.

## Snapshots

A folder is a snapshot: every document in force at the end of that year, gathered so the folder can be read on its own. It is named for the year the analysis stands in, not the year any document in it was published.

Publication dates are the wrong key for two reasons. The former `united-states-1787/` held texts published in 1776, 1787, 1789, 1794 and 2007, so no publication date described it, which is how a modern typeset edition sat in a founding-era folder without anyone noticing. And publication dates are ambiguous in a way vantage years are not. The Eleventh Amendment passed Congress on March 4, 1794, was ratified on February 7, 1795, and was declared ratified on January 8, 1798. One document, three defensible dates. The question a vantage year asks instead is what was in force on that date and what could lawfully be done with it, which is the question this project exists to ask, and the one Gödel asked of a Constitution with 21 amendments.

A snapshot has to be complete, which means documents repeat across folders. An earlier revision split the founding documents so each lived in exactly one folder, and produced four directories none of which was a snapshot of anything: one held the Constitution without the Bill of Rights, another held nothing but the Eleventh Amendment. Neither could answer what was in force in its own year. A folder covering 1795 has to contain the Constitution again and the Bill of Rights again. Duplication is what a self-contained folder costs, and for plain text it is a rounding error: the corpus holds 11 distinct documents across 15 files, and every repeated copy is byte-identical to its siblings.

Folders stay at year granularity even where a year is too coarse. Germany passed through at least three constitutional orders between January and March 1933, and those dates are recorded in prose here rather than in a directory name.

The European folders needed no renaming, which is coincidence rather than confirmation. Each of those constitutions took effect within months of its promulgation, so publication year and first vantage year agree: the Statuto Albertino governed from the day it was granted in 1848, the Weimar Constitution took effect on August 14, 1919, and the Austrian B-VG on November 10, 1920. Had any of the three sat unratified for eighteen months, as the United States Constitution did, its folder would have been wrong in the same way.

## United States

The National Archives sets its transcriptions from the engrossed parchments it holds, and says so on each page. One exception matters: the Declaration transcript follows the 1823 Stone engraving rather than the parchment, which makes it a copy of a copy and unsuitable for any argument that turns on a mark.

| file | set from | retrieved from |
| --- | --- | --- |
| `07-04-1776-declaration-of-independence-nara-transcription.txt` | the 1823 Stone engraving, not the parchment | https://www.archives.gov/founding-docs/declaration-transcript |
| `09-17-1787-constitution-parchment-nara-transcription.txt` | the parchment engrossed by Jacob Shallus, spelling and punctuation retained | https://www.archives.gov/founding-docs/constitution-transcript |
| `09-25-1789-bill-of-rights-parchment-nara-transcription.txt` | the enrolled Joint Resolution, all twelve proposed articles | https://www.archives.gov/founding-docs/bill-of-rights-transcript |
| `03-04-1794-amendment-11-nara-transcription.txt` | operative text only, no ratification apparatus | https://www.archives.gov/founding-docs/amendments-11-27 |
| `09-17-1787-constitution-as-amended-hdoc110-50-typeset.txt` | House Document 110-50, 2007, through Article XXVII | https://www.govinfo.gov/content/pkg/CDOC-110hdoc50/pdf/CDOC-110hdoc50.pdf |

Those five documents are distributed across three snapshots.

`united-states-1791` is the founding order once the Bill of Rights was ratified on December 15, 1791. It holds the Constitution, in force since March 4, 1789, and the Bill of Rights. There is no 1787 snapshot, because in 1787 the Constitution was a signed proposal that governed nothing.

`united-states-1795` is the same order plus the Eleventh Amendment, ratified February 7, 1795. It repeats all three of the 1791 documents, which is the model working rather than waste.

`united-states-2026` is the order in force now, a Constitution with 27 amendments, unchanged since the Twenty-seventh was ratified in 1992. It carries that whole order in one typeset file rather than a Constitution plus separate amendment texts, so it is convenient to read and not comparable line for line with the parchment transcriptions.

The Declaration appears in all three snapshots and is not constitutional text in any of them. It is kept as founding context because United States constitutional argument cites it constantly, not because it is operative law. The instrument that did govern before 1789, the Articles of Confederation of 1781, is absent from the corpus, so the pre-1789 order cannot be examined here at all.

The Bill of Rights file carries twelve articles because twelve were proposed. Articles the third through the twelfth became Amendments I through X; Article the second was ratified in 1992 as Amendment XXVII, and Article the first has never been ratified. Reading the file as a list of the ten will mis-number every citation drawn from it, and it is also why the 1791 snapshot is not strictly correct: by December 1791 ten articles were law and two were not, while the file shows all twelve as proposed.

The GPO file was produced by running `pdftotext -layout` over the source PDF and removing 170 printer lines, which were running heads, page numbers and rule characters. It is filed under 2026 because its text is the order still in force, though the document itself was printed in 2007.

The GPO file was produced by running `pdftotext -layout` over the source PDF and removing 170 printer lines, which were running heads, page numbers and rule characters. It is filed under 2026 because its text is the order still in force, though the document itself was printed in 2007.

## Germany

| file | set from | retrieved from |
| --- | --- | --- |
| `08-11-1919-rgbl-1383-reichsverfassung-wikisource-transcription.txt` | RGBl. 1919 page 1383 scans, proofread by two editors, through Artikel 181 | https://de.wikisource.org/wiki/Verfassung_des_Deutschen_Reichs_%281919%29 |
| `08-11-1919-reichsverfassung-mcbain-rogers-1922-english.txt` | translated by Howard Lee McBain and Lindsay Rogers | https://en.wikisource.org/wiki/Weimar_constitution |

The German transcription keeps the gazette's page markers in the body, so any passage can be carried back to the scan it came from. It also keeps the gazette's spelling rather than modernizing it, which is checkable in the Preamble: the text reads `zu erneuen`, not the modern `erneuern`.

One caution on the translation. Wikisource names McBain and Rogers as the translators but states no edition and files the page under undated works. The 1922 in the filename comes from *The New Constitutions of Europe*, Doubleday, Page, which is where that translation was published; it is not a date the source page asserts. Anyone citing the year should confirm it against the volume.

## Austria

| file | set from | retrieved from |
| --- | --- | --- |
| `10-01-1920-stgbl-450-b-vg-oeaw-machine-transcription.txt` | StGBl. 450/1920, machine transcription, through Artikel 152 | https://bundesverfassung-oesterreich.github.io/bv-static/bv_doc_id__62.html |

This is the weakest file in the corpus and the only one its own publisher disclaims. The page carries a warning that the transcription was produced by machine to make the document broadly searchable, and that because it is purely provisional it should under no circumstances be used as a citation source: `Sie sollte – ob ihres rein provisorischen Charakters – keinesfalls als Zitationsquelle verwendet werden.` It is here anyway, because no clean transcription of the 1920 Stammfassung appears to exist online at all. The official Austrian legal information system stores only the amended modern text, split article by article across separate documents, so the founding version cannot be reassembled from it.

The optical character recognition has visible failures. Against 207 correct instances of `Artikel`, the file contains one `Artifel` at Article 3 and one `Artitel`, both the same substitution of f or t for k. Errors of that shape are easy to spot. Errors that turn one plausible German word into another are not, and nothing in the corpus can currently catch them, because the facsimile that would have served as the check was deleted along with the other page images.

## Italy

| file | set from | retrieved from |
| --- | --- | --- |
| `03-04-1848-statuto-albertino-wikisource-transcription.txt` | *Statuto fondamentale del Regno* page scans, proofread, 84 articles | https://it.wikisource.org/wiki/Italia,_Regno_-_Statuto_albertino |
| `03-04-1848-statuto-albertino-lindsay-rowe-1894-english.txt` | translated by Samuel McCune Lindsay and Leo Stanton Rowe, 1894 | https://en.wikisource.org/wiki/Statuto_Albertino |
| `02-08-1848-proclama-basi-wikisource-transcription.txt` | the proclamation of February 8, 1848, 14 articles | https://it.wikisource.org/wiki/Proclama_per_l%27adozione_delle_basi_del_nuovo_Statuto |

The February proclama is not an early draft of the Statuto and should not be quoted as one. It is the fourteen-article basis Carlo Alberto announced four weeks before the Statuto was granted, and the two texts differ in substance, not only in length.

## Where federal sources disagree

Two United States government transcriptions print the First Amendment differently. The National Archives has `or the right of the people peaceably to assemble`. House Document 110-50 has `of the right`. The difference was confirmed against a fresh download of the PDF and reproduced under two extraction modes, so it is in GPO's text rather than in the tooling. Where the two conflict, the parchment transcription is the better authority for textual work, because the 2007 document is a typeset edition several removes from any original.

The Second Amendment goes the other way and is worth recording because the popular claim is wrong. Every text in this corpus gives three commas, National Archives and GPO alike: `A well regulated Militia, being necessary to the security of a free State, the right of the people to keep and bear Arms, shall not be infringed.` The widely circulated two-comma version is not in either.

## Translation is not evidence

No translated file in this corpus can carry an argument about wording, and each is named for its translator to keep that fact in view. The Weimar Constitution makes the case in its opening sentence. The Preamble describes a people `einig in seinen Stämmen`, which McBain and Rogers render as "united in every respect" and the German Historical Institute renders as "united in all their racial elements." Those are different claims about what the German republic was, and the same sentence carries the `zu erneuen` spelling above, so one line of text is doing double duty as the corpus's spelling check and its clearest warning about translation. The translator is a variable, so the translator goes in the filename.

## Rejected sources

Official standing turned out to be a poor guide to textual quality, and each rejection below cost a fetch that the next person now does not have to repeat.

The German Justice Ministry serves the Weimar Constitution at `gesetze-im-internet.de` as six articles out of 181: 109, 136, 137, 138, 139 and 141, the fragments still operative through Article 140 of the Basic Law. The site is official, authentic, and the wrong document.

The Bavarian State Library's `1000dokumente.de` prints Article 7(14) as `Bauwesen` where the gazette reads `Bankwesen`. That single error is also the test that clears our German file, which has `Bankwesen sowie das Börsenwesen` and therefore did not descend from that copy.

The Quirinale hosts a Statuto Albertino PDF that states no exemplar. Highest possible authority, unknown lineage, unusable for a punctuation question.

Kelsen's 1922 edition on archive.org was fetched and discarded. Its Fraktur optical character recognition is unreadable, rendering the title as `3ur (£nt[tef)ung ber 93nnbc§t)er[Q[fung`, and returning nothing for `Artikel` across 1.2 megabytes.

Wikisource won for Germany and Italy on a specific and checkable ground: both texts were proofread against gazette scans by two independent editors, and both carry page markers in the body, so any passage can be verified against the image that produced it. Neither claim rests on the site's reputation.

Agreement between sources proves nothing by itself. Three sites that copied one another are one source counted three times, and the only reliable test is whether they share an error, which is why the `Bauwesen` and `zu erneuen` checks above are recorded rather than merely performed.

## Gaps

The vantage this project was built to examine is missing. There is no `united-states-1947`, because the corpus has no text of the Constitution as Gödel read it: Articles I through VII with 21 amendments, the Twenty-second not arriving until 1951. The 1795 snapshot stops ten amendments short of him and the 2026 snapshot runs six past. Neither is the document he was looking at, so no claim about what he found can be checked against either.

Building that snapshot needs two things and one decision. The amendments through the Twenty-first can be taken from the National Archives page covering 11 through 27 and stopped at the right place. Amendments I through X are the harder part, because the corpus holds them only as the twelve articles Congress proposed, not as the ten that were ratified, and the two sources that carry them as operative text disagree: the National Archives and House Document 110-50 differ on the First Amendment, as recorded above. Choosing between them, or renumbering the proposed articles by hand, is an editorial act on exactly the punctuation this project claims to analyze. It should be decided deliberately rather than settled by whichever page was easier to fetch.

No English translation of the Austrian 1920 constitution is available. The one that exists appears in *British and Foreign State Papers*, volume 113, 1923, which is print only.

Austria's StGBl. 451/1920, the transitional law that Article 150 depends on, is not in the corpus. Article 150 cannot be read without it.

The corpus holds founding texts only. It cannot yet show how any of these systems fell, because constitutional text is the wrong place to look for that: the Statuto Albertino declared itself `perpetua ed irrevocabile` and its 84 articles were never amended, so an 1848 snapshot and a 1925 snapshot would be identical files while Mussolini dismantled the state through ordinary legislation. Closing this gap means adding statutes in force to each snapshot, starting with the Acerbo Law of 1923 and Law 2263 of 1925 for Italy, the Reichstag Fire Decree and the Enabling Act for Germany, and the 1929 Novelle for Austria, which is the text Dollfuss actually operated under and which makes `austria-1920` the wrong file for Austria's own collapse.
