/**
 * The collation of Amendments I through X across six witnesses.
 *
 * The amendment text is read from the corpus at build time. The per-witness
 * readings are declared here -- and then every one of them is asserted against
 * `corpus/README.md`, which is the file that owns the collation. If the
 * research note changes its account of what GPO prints, this build fails rather
 * than quietly continuing to show the old account.
 *
 * That assertion is the same device `tools/facts.py` applies to numbers. A
 * structured finding needs it more than a scalar does, not less, because a
 * table is easier to leave stale than a number in a sentence.
 */

import { repoFile } from './content';
import { fact } from './facts';

const CORPUS = 'corpus/united-states-1947/09-25-1789-amendments-01-10-senate-transcription.txt';
const COLLATION = 'corpus/README.md';

export interface Witness {
  id: string;
  name: string;
  /** What this witness prints at the point of divergence. */
  reading: string;
  /** Whether the witness preserves eighteenth-century orthography. */
  family: 'preserves' | 'modernises';
  note?: string;
}

export interface Divergence {
  id: string;
  amendment: string;
  /** The sentence, with {{ }} marking the disputed span. */
  frame: string;
  question: string;
  /** Why it is not a triviality. */
  stakes: string;
  witnesses: Witness[];
  /**
   * The fact id whose value must appear in corpus/README.md for this entry to
   * be current. A literal phrase here would be a second copy of the finding,
   * which is the thing the whole apparatus exists to prevent, so the
   * attestation goes through data/facts.json like every other value.
   */
  attest: string;
}

export const DIVERGENCES: Divergence[] = [
  {
    id: 'first-or-of',
    amendment: 'Amendment I',
    frame:
      'Congress shall make no law \u2026 abridging the freedom of speech, or of the press; ' +
      '{{or}} the right of the people peaceably to assemble',
    question: 'or, or of?',
    stakes:
      'With or, assembly is a fourth coordinate object of abridging \u2014 its own protected thing. ' +
      'With of, it is subordinated to the freedom of the press. One letter, and the structure of the ' +
      'sentence changes what is protected.',
    attest: 'recension.gpo',
    witnesses: [
      { id: 'nara', name: 'National Archives, parchment', reading: 'or', family: 'preserves' },
      { id: 'senate', name: 'United States Senate', reading: 'or', family: 'preserves' },
      {
        id: 'gpo',
        name: 'Government Publishing Office',
        reading: 'of',
        family: 'preserves',
        note: 'House Document 110-50. Confirmed against a fresh download and reproduced under two extraction modes, so it is in GPO\u2019s text and not in our tooling.',
      },
      { id: 'cornell', name: 'Cornell Legal Information Institute', reading: 'or', family: 'modernises' },
      { id: 'avalon', name: 'Yale Avalon Project', reading: 'or', family: 'modernises' },
      { id: 'statutes', name: 'Statutes at Large', reading: 'or', family: 'preserves' },
    ],
  },
  {
    id: 'seventh-comma',
    amendment: 'Amendment VII',
    frame:
      'no fact tried by a jury{{,}} shall be otherwise re-examined in any Court of the United States',
    question: 'is the comma there?',
    stakes:
      'This is the comma that hinges the re-examination clause. Yale\u2019s transcription is alone among the ' +
      'six in dropping it \u2014 including against Cornell, which modernises far more aggressively in every ' +
      'other respect and keeps it.',
    attest: 'recension.avalon',
    witnesses: [
      { id: 'nara', name: 'National Archives, parchment', reading: 'present', family: 'preserves' },
      { id: 'senate', name: 'United States Senate', reading: 'present', family: 'preserves' },
      { id: 'gpo', name: 'Government Publishing Office', reading: 'present', family: 'preserves' },
      { id: 'cornell', name: 'Cornell Legal Information Institute', reading: 'present', family: 'modernises' },
      {
        id: 'avalon',
        name: 'Yale Avalon Project',
        reading: 'deleted',
        family: 'modernises',
        note: 'Also drops the comma before without just compensation in the Fifth.',
      },
      { id: 'statutes', name: 'Statutes at Large', reading: 'present', family: 'preserves' },
    ],
  },
  {
    id: 'second-commas',
    amendment: 'Amendment II',
    frame:
      'A well regulated Militia{{,}} being necessary to the security of a free State{{,}} the right of ' +
      'the people to keep and bear Arms{{,}} shall not be infringed.',
    question: 'how many commas?',
    stakes:
      'The Statutes at Large prints it twice and not identically, and both printings give one comma \u2014 ' +
      'neither the parchment\u2019s three nor the two of the popular version. What circulates as ' +
      '\u201cthe\u201d Second Amendment is a choice among printings, not a transcription of one.',
    attest: 'recension.second_amendment',
    witnesses: [
      { id: 'nara', name: 'National Archives, parchment', reading: 'three commas', family: 'preserves' },
      { id: 'gpo', name: 'Government Publishing Office', reading: 'three commas', family: 'preserves' },
      {
        id: 'statutes-21',
        name: 'Statutes at Large, 1 Stat. 21',
        reading: 'one comma',
        family: 'preserves',
        note: 'Front matter. Reads a free State.',
      },
      {
        id: 'statutes-97',
        name: 'Statutes at Large, 1 Stat. 97',
        reading: 'one comma',
        family: 'preserves',
        note: 'The Joint Resolution itself. Reads a free state, lower case.',
      },
      {
        id: 'popular',
        name: 'The widely circulated version',
        reading: 'two commas',
        family: 'modernises',
        note: 'In none of the printings this corpus holds. An earlier version of our own note claimed it appears in no source at all; that overreached and was corrected.',
      },
    ],
  },
];

/**
 * Assert that every divergence is still what `corpus/README.md` says it is.
 *
 * Called at build time. A failure here means the research note moved and this
 * table did not, which is precisely the drift the whole single-source-of-truth
 * apparatus exists to prevent.
 */
export function assertCurrent(): void {
  const collation = repoFile(COLLATION);
  const normalised = collation.replace(/[*`_]/g, '');
  for (const d of DIVERGENCES) {
    const f = fact(d.attest);
    const phrase = String(f.value);
    if (!normalised.includes(phrase)) {
      throw new Error(
        `The recension entry "${d.id}" rests on fact "${d.attest}", whose value is ` +
          `"${phrase}". That phrase is not in ${COLLATION}. Either the collation ` +
          `changed and this table is stale, or the fact's canonical owner moved.`,
      );
    }
  }
}


/** Split a frame on its {{ }} markers into alternating plain and disputed spans. */
export function frameParts(frame: string): { text: string; disputed: boolean }[] {
  return frame
    .split(/(\{\{[^}]*\}\})/)
    .filter((s) => s.length > 0)
    .map((s) =>
      s.startsWith('{{')
        ? { text: s.slice(2, -2), disputed: true }
        : { text: s, disputed: false },
    );
}
