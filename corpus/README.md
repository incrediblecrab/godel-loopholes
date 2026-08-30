# Corpus

This folder holds the primary documents and nothing said about them. Constitutions, the statutes that ran beside them, and the founding texts that get cited in argument. Every claim this project makes has to land on a specific mark in one of these files.

Every file here is a transcription. None is a document. The distinction matters because this project reads punctuation, and punctuation is the first thing a transcriber changes, quietly and usually while trying to help. A missing comma on the 1789 parchment is a finding. A missing comma introduced by a volunteer proofreader in 2007 is noise. Telling the two apart requires knowing who set each text and from what, so that is what the entries below record.

Material was retrieved on August 24 and August 25, 2026. Sources are ranked by transmission lineage rather than by the standing of the institution hosting them, which is not the obvious ordering and is defended under rejected sources.

## How the corpus is kept

**One file per source document.** If a page publishes twenty-seven amendments as one document, they are held as one file, and the corpus does not impose a structure the source does not have.

**Texts are kept as they came.** Defects are recorded in this file and never repaired in the text. The Austrian file has optical character recognition errors, the GPO file corrupts a word of the First Amendment, and both are still on disk exactly as retrieved, because a corpus that has been quietly improved cannot be used to settle an argument about wording.

**Nothing we write goes inside a corpus file.** No headers, no labels, no editorial notes, not even to flag a known error. The files carry only the transcribed text, and every word of provenance and judgment lives here.

**Fix by addition, not by edit.** Where a snapshot needs something it lacks, the missing text is added beside the existing file rather than the existing file being altered to suit.

**Translations cannot carry an argument about wording** and are named for their translator so that stays visible.

**Every link here was verified by fetching it** and checking that the returned page serves the work it claims to. Retrieval routes that took work to find are recorded so no one has to find them twice.

## Snapshots

A folder is a snapshot: every document in force at the end of that year, gathered so the folder can be read on its own. It is named for the year the analysis stands in, not the year any document in it was published.

The corpus currently holds six snapshots: `austria-1920`, `germany-1919`, `germany-1933`, `italy-1848`, `united-states-1947` and `united-states-2026`. That is 16 distinct texts across 22 files, six of which appear in two snapshots each.

Publication dates are the wrong key for two reasons. An earlier revision keyed folders to publication and produced a `united-states-1787/` holding texts published in 1776, 1787, 1789, 1794 and 2007, so no publication date described it, which is how a modern typeset edition sat in a founding-era folder without anyone noticing. And publication dates are ambiguous in a way vantage years are not. The Eleventh Amendment passed Congress on March 4, 1794, was ratified on February 7, 1795, and was declared ratified on January 8, 1798. One document, three defensible dates. The question a vantage year asks instead is what was in force on that date and what could lawfully be done with it, which is the question this project exists to ask, and the one Gödel asked of a Constitution with 21 amendments.

A snapshot has to be complete, which means documents repeat across folders. An earlier revision split the founding documents so each lived in exactly one folder, and produced four directories none of which was a snapshot of anything: one held the Constitution without the Bill of Rights, another held nothing but the Eleventh Amendment. Neither could answer what was in force in its own year. Duplication is what a self-contained folder costs, and for plain text it is a rounding error.

Four documents repeat verbatim across the two United States snapshots, and both German files repeat across the two German ones. Every repeated copy was compared against its sibling and is byte-identical: the Declaration, the Constitution parchment, the Bill of Rights parchment, the Senate rendering of Amendments I through X, the Weimar gazette transcription and its translation. The United States amendment files are the exception and are not siblings in that sense. Both are drawn from the same National Archives page, but the 1947 file stops at the Twenty-first and the 2026 file runs to the Twenty-seventh, so they differ by design.

Folders stay at year granularity even where a year is too coarse. Germany passed through at least three constitutional orders between January and March 1933, and those dates are recorded in prose here rather than in a directory name.

The European folders are keyed to promulgation because for those three constitutions promulgation and first vantage year agree: the Statuto Albertino governed from the day it was granted in 1848, the Weimar Constitution took effect on August 14, 1919, and the Austrian B-VG on November 10, 1920. Had any of the three sat unratified for eighteen months, as the United States Constitution did, its folder would have been wrong in the same way. The agreement is coincidence, not confirmation of the scheme, and `germany-1933` shows it plainly: nothing was promulgated in 1933 that gives the folder its name, and the year is a vantage like any other.

## United States

The National Archives sets its transcriptions from the engrossed parchments it holds, and says so on each page. One exception matters: the Declaration transcript follows the 1823 Stone engraving rather than the parchment, which makes it a copy of a copy and unsuitable for any argument that turns on a mark.

| file | set from | retrieved from |
| --- | --- | --- |
| `07-04-1776-declaration-of-independence-nara-transcription.txt` | the 1823 Stone engraving, not the parchment | https://www.archives.gov/founding-docs/declaration-transcript |
| `09-17-1787-constitution-parchment-nara-transcription.txt` | the parchment engrossed by Jacob Shallus, spelling and punctuation retained | https://www.archives.gov/founding-docs/constitution-transcript |
| `09-25-1789-bill-of-rights-parchment-nara-transcription.txt` | the enrolled Joint Resolution, all twelve proposed articles | https://www.archives.gov/founding-docs/bill-of-rights-transcript |
| `02-07-1795-amendments-11-21-nara-transcription.txt` | operative text of Amendments XI through XXI, no ratification apparatus | https://www.archives.gov/founding-docs/amendments-11-27 |
| `02-07-1795-amendments-11-27-nara-transcription.txt` | operative text of Amendments XI through XXVII, no ratification apparatus | https://www.archives.gov/founding-docs/amendments-11-27 |
| `09-25-1789-amendments-01-10-senate-transcription.txt` | operative text of Amendments I through X, in the Senate's rendering | https://www.senate.gov/about/origins-foundations/senate-and-constitution/constitution.htm |
| `09-17-1787-constitution-as-amended-hdoc110-50-typeset.txt` | House Document 110-50, 2007, through Amendment XXVII | https://www.govinfo.gov/content/pkg/CDOC-110hdoc50/pdf/CDOC-110hdoc50.pdf |

The two amendment files each hold every amendment from a single source page in a single file, because that page is one document. An earlier revision split them into 28 separate files, one per amendment, which invented a structure the source does not have. The rule the corpus follows is one file per source document.

Amendments I through X are held twice, deliberately, because they exist in two different kinds of document. The parchment file is the enrolled Joint Resolution of 1789: twelve articles proposed, none yet ratified, which is what the engrossed document actually says. The Senate file is the ten that became law, under the numbers they are cited by. Neither substitutes for the other. The parchment cannot be cited as "Amendment II" without renumbering it by hand, and the operative rendering cannot show that the ten were once twelve.

The Senate rendering was chosen over the alternatives on evidence rather than on standing. It reproduces the parchment text **byte for byte in nine of ten amendments**, diverging only by capitalizing `Suits` in the Seventh, where GPO agrees with the Senate against the parchment. Cornell and Avalon were rejected: both modernize orthography silently and Avalon drops two commas. GPO was rejected as a base text because it corrupts the First Amendment. All of this is set out under where the sources disagree.

`united-states-1947` is the order Gödel was reading: the Constitution, the Bill of Rights in both the proposed and the operative rendering, and Amendments XI through XXI. It stops at the Twenty-first, ratified December 5, 1933, because the Twenty-second was not ratified until February 27, 1951, more than three years after his hearing.

`united-states-2026` is the order in force now, a Constitution with 27 amendments, unchanged since the Twenty-seventh was ratified on May 7, 1992.

Ratification dates for the amendments in these two files, which previously survived only in the split filenames: XI, February 7, 1795. XII, June 15, 1804. XIII, December 6, 1865. XIV, July 9, 1868. XV, February 3, 1870. XVI, February 3, 1913. XVII, April 8, 1913. XVIII, January 16, 1919. XIX, August 18, 1920. XX, January 23, 1933. XXI, December 5, 1933. XXII, February 27, 1951. XXIII, March 29, 1961. XXIV, January 23, 1964. XXV, February 10, 1967. XXVI, July 1, 1971. XXVII, May 7, 1992.

The Declaration appears in both snapshots and is not constitutional text in either. It is kept as founding context because United States constitutional argument cites it constantly, not because it is operative law. The instrument that did govern before 1789, the Articles of Confederation of 1781, is absent from the corpus, so the pre-1789 order cannot be examined here at all.

The GPO file was produced by running `pdftotext -layout` over the source PDF and removing 170 printer lines, which were running heads, page numbers and rule characters. It is filed under 2026 because its text is the order still in force, though the document itself was printed in 2007.

Its 80 form-feed characters were kept rather than stripped, and the decision is deliberate. Each one marks a boundary between printed pages of House Document 110-50, so they do for this file what the gazette page markers do for the German transcription: they let any passage be carried back to the page it was set on. A file that has already had 170 lines removed needs that anchor more than a clean one would.

### How the three defects in `united-states-1947` were resolved

**A 1992 amendment sat inside a 1947 snapshot.** The Bill of Rights file carries twelve articles because twelve were proposed. `Article the third` through `Article the twelfth` became Amendments I through X, so the mapping is offset by two, and reading the file as a list of the ten will mis-number every citation drawn from it. `Article the first` has never been ratified. `Article the second` was still pending in 1947 and was ratified in 1992 as Amendment XXVII.

This was fixed by addition, not by editing. The parchment file is a faithful transcription of a real 1789 document and nothing in it is wrong; renumbering it would have meant altering a source text to make a folder tidier, which is the one thing this corpus does not do. Adding the Senate's operative I through X gives each snapshot a text that can be read as what was in force, and leaves the transmittal document intact beside it.

**Two orphan footnote markers.** The amendment files carried two `*` characters whose footnote text had been dropped during extraction, so they pointed at nothing. Both footnotes were recovered from the National Archives page they came from and restored in place: `*Superseded by section 3 of the 20th amendment.` after Amendment XII, and `*Changed by section 1 of the 26th amendment.` after Amendment XIV.

The 1947 file keeps only the first. The Twentieth Amendment was ratified in 1933 and had superseded that passage of the Twelfth long before Gödel read it, so the marker and its note are both true as of 1947. The Twenty-sixth was not ratified until 1971, so its marker was removed from the 1947 file entirely rather than restored: it annotated a change that had not yet happened. The 2026 file carries both. A footnote is evidence about a date as much as the text it annotates is.

**Amendment XVIII appeared without any note of its repeal.** This one dissolved on inspection rather than needing a fix. The Twenty-first Amendment repealed the Eighteenth on December 5, 1933, and the Twenty-first is in the same file, where its first section reads `The eighteenth article of amendment to the Constitution of the United States is hereby repealed.` The document states its own repeal. Adding an editorial label would have been redundant and would have put our words inside a source text to say something the source already says.


## Germany

| file | set from | retrieved from |
| --- | --- | --- |
| `08-11-1919-rgbl-1383-reichsverfassung-wikisource-transcription.txt` | RGBl. 1919 page 1383 scans, proofread by two editors, through Artikel 181 | https://de.wikisource.org/wiki/Verfassung_des_Deutschen_Reichs_%281919%29 |
| `08-11-1919-reichsverfassung-mcbain-rogers-1922-english.txt` | translated by Howard Lee McBain and Lindsay Rogers | https://en.wikisource.org/wiki/Weimar_constitution |
| `02-28-1933-rgbl-i-83-reichstagsbrandverordnung-wikisource-transcription.txt` | RGBl. 1933 I, Nr. 17, page 83, from a gazette scan on Commons | https://de.wikisource.org/wiki/Reichstagsbrandverordnung |
| `03-24-1933-rgbl-i-141-ermaechtigungsgesetz-wikisource-transcription.txt` | RGBl. 1933 I, Nr. 25, page 141, from a gazette scan on Commons | https://de.wikisource.org/wiki/Ermächtigungsgesetz |

`germany-1933` holds the two statutes together with both Weimar files, because the Weimar Constitution was never repealed and was still nominally in force at the end of 1933. That is the whole point of the snapshot: the constitution is present and intact, and the order it established is gone.

Both 1933 texts come from the same Wikisource project as the 1919 transcription and follow its edition guidelines, so they share a lineage the corpus has already accepted. Each carries `BEARBEITUNGSSTAND=fertig`, names its Commons gazette scan as its exemplar, and sits entirely on one gazette page, which is why each opens with a page marker and carries no others.

They were checked against the modernizing copy at `documentarchiv.de` and do not descend from it. That copy reads `verfassungsändernder` where the gazette form is `verfassungändernder` without the Fugen-s, prints `Reiches` for `Reichs`, and contains a plain typo, `beteligten`. Our file has the gazette forms and the correct spelling. This is the same kind of shared-error test as the `Bankwesen` check on the 1919 file, and it is recorded here rather than merely performed.

A third decree of the period, the Verordnung des Reichspräsidenten zum Schutze des Deutschen Volkes of February 4, 1933, RGBl. 1933 I page 35, is not in the corpus. No proofread transcription of it exists. The available copies state no exemplar, and one of them silently omits two of its five sections.

The German transcription keeps the gazette's page markers in the body, so any passage can be carried back to the scan it came from. It also keeps the gazette's spelling rather than modernizing it, which is checkable in the Preamble: the text reads `zu erneuen`, not the modern `erneuern`.

One caution on the translation. Wikisource names McBain and Rogers as the translators but states no edition and files the page under undated works. The 1922 in the filename comes from *The New Constitutions of Europe*, Doubleday, Page, which is where that translation was published; it is not a date the source page asserts. Anyone citing the year should confirm it against the volume.

## Austria

| file | set from | retrieved from |
| --- | --- | --- |
| `10-01-1920-stgbl-450-b-vg-oeaw-machine-transcription.txt` | StGBl. 450/1920, machine transcription, through Artikel 152 | https://bundesverfassung-oesterreich.github.io/bv-static/bv_doc_id__62.html |
| `07-24-1917-rgbl-307-kriegswirtschaftliches-ermaechtigungsgesetz-wikisource-transcription.txt` | RGBl. 1917 Nr. 307, pages 739 to 740, from gazette scans | https://de.wikisource.org/wiki/Kriegswirtschaftliches_Ermächtigungsgesetz |

The wartime enabling act of 1917 is in the 1920 snapshot because it was in force in 1920 and was never repealed until 1946. It is an ordinary economic statute, it is not mentioned anywhere in the constitution, and it is the instrument the 1933 and 1934 seizure ran through. A snapshot holding only the constitution would not show it, which is the reason snapshots hold statutes in force and not constitutional text alone.

Its transcription is the strongest Austrian file in the corpus by some distance: proofread status `fertig`, a named gazette scan as exemplar, and inline page markers at 739 and 740. It carries one known defect, kept as found. The signature block reads `Bauhaus m.p.` where the minister's name was Banhans. The error is in the source and is recorded rather than corrected.

This is the weakest file in the corpus and the only one its own publisher disclaims. The page carries a warning that the transcription was produced by machine to make the document broadly searchable, and that because it is purely provisional it should under no circumstances be used as a citation source: `Sie sollte – ob ihres rein provisorischen Charakters – keinesfalls als Zitationsquelle verwendet werden.` It is here anyway, because no clean transcription of the 1920 Stammfassung appears to exist online at all. The official Austrian legal information system stores only the amended modern text, split article by article across separate documents, so the founding version cannot be reassembled from it.

The optical character recognition has visible failures. Against 207 correct instances of `Artikel`, the file contains one `Artifel` at Article 3 and one `Artitel`, both the same substitution of f or t for k. Errors of that shape are easy to spot. Errors that turn one plausible German word into another are not, and nothing in the corpus can currently catch them, because the facsimile that would have served as the check was deleted along with the other page images.

## Italy

| file | set from | retrieved from |
| --- | --- | --- |
| `03-04-1848-statuto-albertino-wikisource-transcription.txt` | *Statuto fondamentale del Regno* page scans, proofread, 84 articles | https://it.wikisource.org/wiki/Italia,_Regno_-_Statuto_albertino |
| `03-04-1848-statuto-albertino-lindsay-rowe-1894-english.txt` | translated by Samuel McCune Lindsay and Leo Stanton Rowe, 1894 | https://en.wikisource.org/wiki/Statuto_Albertino |
| `02-08-1848-proclama-basi-wikisource-transcription.txt` | the proclamation of February 8, 1848, 14 articles | https://it.wikisource.org/wiki/Proclama_per_l%27adozione_delle_basi_del_nuovo_Statuto |

The February proclama is not an early draft of the Statuto and should not be quoted as one. It is the fourteen-article basis Carlo Alberto announced four weeks before the Statuto was granted, and the two texts differ in substance, not only in length.

## Where the sources disagree

Amendments I through X were collated across six independent witnesses on August 25, 2026: the National Archives parchment transcription, the Senate rendering and GPO House Document 110-50, all three now held in this corpus; Cornell's Legal Information Institute and Yale's Avalon Project, both fetched and both rejected as base texts on the evidence below; and the Statutes at Large, read from the Library of Congress page scans.

**On wording the six agree completely.** Across all ten amendments there is not one divergence in word choice. Every difference found is orthographic or punctuational, which is precisely the class of difference this project cannot afford to normalize away.

The witnesses fall into two families. The National Archives, the Senate and GPO preserve eighteenth-century orthography, with capitalized substantives, British spellings and hyphenated `re-examined`. Cornell and Avalon silently modernize all three. The Senate reproduces the parchment text verbatim for nine of ten amendments, diverging only by capitalizing `Suits` in the Seventh, which makes it an independent confirmation of the parchment rather than a separate recension, and it supplies the operative numbering the parchment lacks.

**GPO corrupts the First Amendment.** House Document 110-50 reads `of the right of the people peaceably to assemble` where the other five read `or the right`. The difference was confirmed against a fresh download of the PDF, reproduced under two extraction modes, and located in the body text rather than the index, so it is in GPO's text and not in the tooling. It is not trivial: `or` makes assembly a fourth coordinate object of `abridging`, while `of` subordinates it to `the press`. Where the two federal sources conflict, the parchment transcription is the better authority, because the 2007 document is a typeset edition several removes from any original.

**Avalon deletes two commas.** The Fifth Amendment loses the comma before `without just compensation` and the Seventh loses the comma after `tried by a jury`. Cornell, which modernizes as aggressively in every other respect, keeps both. Avalon is alone among the six. This is worth stating plainly: a Yale-hosted transcription of the Bill of Rights silently drops the comma that hinges the Seventh Amendment's re-examination clause, in a project whose premise is that such commas carry legal weight.

### The Second Amendment, corrected

An earlier version of this file claimed that the widely circulated two-comma Second Amendment appears in no source, on the strength of the National Archives and GPO both giving three commas. That claim overreached. It was true about this corpus and false as a statement about the record, because the corpus did not then contain the recension where the count differs.

The Statutes at Large was checked directly. It prints the Second Amendment **twice, and not identically**.

At 1 Stat. 21, in the volume's front matter, it reads `A well regulated militia being necessary to the security of a free State, the right of the people to keep and bear arms shall not be infringed.` At 1 Stat. 97, in the Joint Resolution itself, it reads the same but with `state` in lower case.

Both give **one comma**, not the parchment's three and not the two of the popular version. Both were read from the page images rather than from the optical character recognition layer, because commas are the first thing OCR loses and a comma count taken from OCR is not evidence.

The right conclusion is that at least three punctuations of the Second Amendment are in circulation across authoritative printings, and the corpus holds only one of them.

### One volume, two Seventh Amendments

The same check turned up something sharper. The Statutes at Large prints the Seventh Amendment twice and the two printings are punctuated differently.

At 1 Stat. 21: `and no fact tried by a jury shall be otherwise re-examined in any court of the United States than according to the rules of the common law.`

At 1 Stat. 98: `and no fact, tried by a jury, shall be otherwise re-examined in any court of the United States, than according to the rules of the common law.`

Zero internal commas in one printing, two in the other, inside one book, published by authority. The parchment gives a third reading again, with a single comma after `jury`. The paired commas at 1 Stat. 98 set `tried by a jury` off as parenthetical, which is a different grammatical claim about what the clause restricts than either of the others makes.

No argument in this project should rest on the punctuation of the Seventh Amendment without saying which printing it follows and why.

## Translation is not evidence

No translated file in this corpus can carry an argument about wording, and each is named for its translator to keep that fact in view. The Weimar Constitution makes the case in its opening sentence. The Preamble describes a people `einig in seinen Stämmen`, which McBain and Rogers render as "united in every respect" and the German Historical Institute renders as "united in all their racial elements." Those are different claims about what the German republic was, and the same sentence carries the `zu erneuen` spelling above, so one line of text is doing double duty as the corpus's spelling check and its clearest warning about translation. The translator is a variable, so the translator goes in the filename.

## Rejected sources

Official standing turned out to be a poor guide to textual quality, and each rejection below cost a fetch that the next person now does not have to repeat.

The German Justice Ministry serves the Weimar Constitution at `gesetze-im-internet.de` as six articles out of 181: 109, 136, 137, 138, 139 and 141, the fragments still operative through Article 140 of the Basic Law. The site is official, authentic, and the wrong document.

The Bavarian State Library's `1000dokumente.de` prints Article 7(14) as `Bauwesen` where the gazette reads `Bankwesen`. That single error is also the test that clears our German file, which has `Bankwesen sowie das Börsenwesen` and therefore did not descend from that copy.

The Quirinale hosts a Statuto Albertino PDF that states no exemplar. Highest possible authority, unknown lineage, unusable for a punctuation question.

Kelsen's 1922 edition on archive.org was fetched and discarded. Its Fraktur optical character recognition is unreadable, rendering the title as `3ur (£nt[tef)ung ber 93nnbc§t)er[Q[fung`, and returning nothing for `Artikel` across 1.2 megabytes.

Avalon and Cornell are rejected as base texts for Amendments I through X, on the evidence set out above. Both are useful as witnesses and both are cited here as such. Neither can serve as a text this project reasons over, because both modernize orthography silently and one of them drops commas.

Wikisource won for Germany and Italy on a specific and checkable ground: both texts were proofread against gazette scans by two independent editors, and both carry page markers in the body, so any passage can be verified against the image that produced it. Neither claim rests on the site's reputation.

Agreement between sources proves nothing by itself. Three sites that copied one another are one source counted three times, and the only reliable test is whether they share an error, which is why the `Bauwesen` and `zu erneuen` checks above are recorded rather than merely performed.

## Retrieval notes

Several holders of these texts block automated retrieval, and the working routes are recorded so they need not be rediscovered.

`loc.gov/law/help/statutes-at-large/` returns 403. The scans themselves are served without challenge from `https://tile.loc.gov/storage-services/service/ll/llsl/llsl-c1/llsl-c1.pdf`, which is volume 1, 31 MB. Page images must be rendered and read; the OCR layer in that file doubles every line and is not reliable for punctuation.

The `llsl` identifiers are keyed to Congress, not to volume, and the resemblance is a trap. `llsl-c1` is volume 1 because the First Congress produced it, but `llsl-c54` returns volume 29, covering December 1895 to March 1897, at 103 MB and HTTP 200. The volume was downloaded and its title page read before the mismatch was noticed, which is the whole lesson: the request succeeded, the file was a genuine Statutes at Large volume, and it was the wrong one.

That trap has a second floor, and `llsl-c76` is how it was found. The bare Congress number is not always the identifier, because a Congress that filled more than one volume is split by session: volume 54 is `llsl-c76s2-s3`, not `llsl-c76`, which is why the earlier attempt returned 404 and was recorded here as having no route. Volume 61, holding the Presidential Succession Act of 1947 at 61 Stat. 380, is `llsl-c80s1` on the same pattern. Guessing the suffix is not necessary and should not be attempted, because there is a route keyed to the volume itself: **`https://www.loc.gov/item/llsl-v<volume>/?fo=json` answers with the item record, and its `resources[].pdf` field names the scan directly.** Volume 61, volume 54 and volume 36 were each resolved this way and the returned titles were read to confirm the volume before anything was quoted from it. Do that confirmation every time; it is the only step that catches the trap.

The note above that the `loc.gov` collection search API returns 403 to scripted requests no longer holds and should not be relied on. Both `https://www.loc.gov/item/llsl-v61/?fo=json` and `https://www.loc.gov/collections/united-states-statutes-at-large/?q=<terms>&fo=json` answer 200 with JSON to a plain `curl`. What does still return 403 is `loc.gov/resource`, which is a different endpoint and is recorded separately below. The OCR layer in these volumes doubles every line, as it does in volume 1, and in volume 61 it renders the date of the Act as 1917 rather than 1947 — the usual reason for rendering the page and reading the image.

United States Reports are a different and reliable service. The pattern is `https://tile.loc.gov/storage-services/service/ll/usrep/usrep<volume>/usrep<volume><first page>/usrep<volume><first page>.pdf`, and it serves official page images. Three other routes to the same opinions failed: Justia returns a Cloudflare 403, CourtListener's cluster endpoint now requires authentication and its HTML pages return an empty HTTP 202, and Wikisource has no page for many older cases even where its own volume index links to them.

`ias.edu` returns 403 for its library landing pages regardless of user agent, but files under `ias.edu/sites/default/files/` download normally, so material there is reachable if the direct path is known. `albert.ias.edu` returns 403. `papers.ssrn.com` returns 403. `hal.science` returns 500 on unversioned document URLs and 200 when the version suffix is included.

`constitution.congress.gov` and `loc.gov/resource` return 403. `verfassungen.at` returns 403 without a browser user agent and rate-limits under rapid sequential requests. The Senate's `civics/constitution_item/constitution.htm` is a 120-byte meta-redirect stub; the real page is at `about/origins-foundations/senate-and-constitution/constitution.htm`. GPO's CONAN pages and `ourdocuments.gov` are JavaScript-rendered and cannot be plaintexted from a fetch.

ALEX, the Austrian National Library's gazette portal at `alex.onb.ac.at`, holds the scans for the German Reichsgesetzblatt and the Austrian Reichs-, Staats- and Bundesgesetzblatt. It cannot be fetched. Every ALEX address tested, across all three gazettes, returns HTTP 200 carrying a `Sicherheitsüberprüfung` challenge page rather than the scan. The status code is the trap: a check that records only the response code will log these as successful retrievals. They were opened and read before being recorded here.

Web search returned confidently wrong URLs on several occasions during this work, including URLs that resolved to entirely different articles than the citation claimed. Every link in this file was verified by fetching it and checking the returned title.

## Gaps

The statutory recension is missing, and adding the Senate rendering did not close this gap. The corpus now holds Amendments I through X twice, but both texts descend from the same lineage: the Senate rendering is byte-identical to the parchment in nine of ten amendments, which is what makes it a confirmation rather than an independent witness. The Statutes at Large is a genuinely different lineage, and the collation above shows it differs from the parchment at many points and from itself at some. Adding 1 Stat. 97 to 98 would give the corpus a second lineage rather than a third copy of one. It has not been added because doing so means transcribing from page images by hand, and a hand transcription made to settle punctuation questions is exactly the kind of artifact this file exists to be suspicious of. It should be done deliberately, proofread twice, and labelled as ours.

No English translation of the Austrian 1920 constitution is available. The one that exists appears in *British and Foreign State Papers*, volume 113, 1923, which is print only.

Austria's StGBl. 451/1920, the transitional law, is still not in the corpus, and the reason is now known and is worse than a simple absence. Article 150 of the B-VG defers the whole transition to it, and Article 151 makes the B-VG's own entry into force conditional on the exceptions it sets, so the constitution cannot be read without it. Two full transcriptions exist and neither is the 1920 text. The one at `verfassungen.at` states in its own header that it gives the law `in der Fassung des B.G.Bl. Nr. 368 vom Jahre 1925` as a `konsolidierte Fassung zum 28.9.2012`. The official RIS copy reports the same governing instrument, BGBl. 368/1925, in force from October 1, 1925. The 1925 republication has displaced the 1920 text in every digital source, and the gazette scan that would settle it is behind the ALEX challenge page. Filing either copy under `austria-1920` would repeat exactly the defect resolved in `united-states-1947`, a later text sitting inside an earlier snapshot, so neither was added.

On the substance the news is better than on the text. The amendment apparatus at `verfassungen.at` records no change to § 7 in 1925, only a 2008 declaration that it had ceased to apply, so § 7 (2) is very likely 1920 wording carried forward. That is a claim about substance and not about punctuation, and this project distinguishes the two.

No Italian statute of the fascist period is in the corpus, and no transcription of one exists at the standard the corpus requires. Italian Wikisource, which supplied the Statuto, has none of them: its 1923, 1925 and 1926 categories hold only boundary and railway decrees. Normattiva, the official database of the Italian state, does serve the original text but states no exemplar, claims no proofreading, carries no page markers, and renders its articles through JavaScript so that a fetch returns only the first one. Its lineage is unknown in exactly the way the Quirinale's Statuto was, and the corpus rejected that. Authoritative gazette scans of every relevant issue are on archive.org in the `gazzetta-ufficiale` collection, as image-only PDFs. So Italy can be settled, but only by transcribing from scans, which the corpus treats as work to be done deliberately, proofread twice, and labelled as ours.

Germany's collapse can now be read from the corpus and Austria's cannot yet. `germany-1933` holds the decree and the enabling act beside the constitution they ran through. Austria still needs the 1929 Novelle, which is the text Dollfuß actually operated under, and the May 1934 constitution, promulgated under the 1917 economic enabling act. Italy needs the Acerbo Law of 1923 and Law 2263 of 1925 before an `italy-1926` snapshot would say anything an `italy-1848` snapshot does not, since the Statuto declared itself `perpetua ed irrevocabile` and its 84 articles were never amended.

A whole category of document is missing, and the analysis of Austria is what surfaced it. The step that ended Austrian parliamentary government was a gap in the Nationalrat's rules of procedure, which had no provision for all three presidents resigning in succession, and the neutralization of the Constitutional Court two months later worked through a rule about how many of its members had to be present. Neither document is a constitution and neither is a statute, and the corpus holds only constitutions and statutes. A constitution's most important check is usually a body, a body's capacity to act is governed by its own procedural and composition rules, and those rules are therefore part of the constitutional machinery whatever their formal rank. Chamber standing orders and court composition rules should be acquired for every snapshot. This is the first gap in this file that was found by doing analysis rather than by cataloguing sources, which is an argument for doing more of it before acquiring more texts.

There are no patch snapshots. The constitutions written specifically to prevent recurrence, the Italian Constitution in force January 1, 1948 and the German Basic Law of May 23, 1949, are the natural counterparts to the collapse snapshots and neither is here. The Italian one is worth adding for a reason beyond symmetry: the Constituent Assembly approved it on December 22, 1947, seventeen days after Gödel's hearing.
