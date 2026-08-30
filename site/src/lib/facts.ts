/**
 * The only path from data/facts.json to the DOM.
 *
 * Nothing in this site is allowed to type a load-bearing number. Every value a
 * reader sees comes through here, from the same file `verify.sh` section 6
 * polices against the canonical markdown. If the JSON and the research notes
 * ever disagree, the harness fails and this site does not ship -- which is the
 * whole reason the indirection exists.
 *
 * The read is synchronous and happens at build time. Astro emits static HTML,
 * so facts.json never reaches the browser as a file and there is no fetch, no
 * loading state, and no way for a client to see a value the build did not
 * verify.
 */

import raw from '../../../data/facts.json';

export type Status = 'verified' | 'unverified' | 'disproved';

export interface FactSource {
  title?: string;
  cite?: string;
  url?: string;
  quotation?: string;
  note?: string;
  /** 'page image' | 'transcription' | 'scan'. Page image is the strong one. */
  read_from?: string;
  page?: string;
}

export interface Fact {
  id: string;
  value: string | number;
  /** Short noun phrase for a table cell or a label. Never a sentence. */
  label: string;
  /** One sentence a reader could quote without further context. */
  statement: string;
  /** The repository file that owns this value. Exactly one. */
  canonical: string;
  status: Status;
  source?: FactSource;
  /** Fact ids this one is computed from. Arithmetic is checked in tools/facts.py. */
  derived_from?: string[];
  /** How the value was confirmed independently -- Z3, Isabelle, hand derivation. */
  checked_by?: string;
  /** What this project believed before, when the belief changed. */
  history?: string;
  /** A deeper write-up, when the canonical file is the plain-language telling. */
  analysis?: string;
  /** For the collapse cases: which layer of law did the work. */
  layer?: string;
  /** True where the value is not keyed to the 1947 vantage. */
  vantage_exempt?: boolean;
  vantage_note?: string;
  kind?: string;
}

export interface FactsFile {
  schema: number;
  purpose: string;
  /** Every number here describes the law as it stood on this date. */
  vantage: string;
  vantage_note: string;
  status_values: Record<Status, string>;
  facts: Fact[];
}

const file = raw as unknown as FactsFile;

if (file.schema !== 1) {
  throw new Error(
    `data/facts.json is schema ${file.schema}; this site reads schema 1. ` +
      `Update src/lib/facts.ts rather than loosening the check.`,
  );
}

const index = new Map<string, Fact>();
for (const f of file.facts) {
  if (index.has(f.id)) {
    throw new Error(`data/facts.json has two facts with id "${f.id}"`);
  }
  index.set(f.id, f);
}

export const vantage = file.vantage;
export const vantageNote = file.vantage_note;
export const statusMeaning = file.status_values;
export const allFacts: readonly Fact[] = file.facts;

/**
 * Look a fact up, or fail the build.
 *
 * Throwing rather than returning undefined is deliberate. A typo in a fact id
 * should stop the build, not render an empty span that nobody notices until a
 * reader asks why the page says the House needed nothing.
 */
export function fact(id: string): Fact {
  const f = index.get(id);
  if (!f) {
    const near = [...index.keys()]
      .filter((k) => k.split('.')[0] === id.split('.')[0])
      .slice(0, 6);
    throw new Error(
      `No fact with id "${id}" in data/facts.json.` +
        (near.length ? ` Did you mean one of: ${near.join(', ')}?` : ''),
    );
  }
  return f;
}

/** The bare value, for interpolation into prose. */
export function value(id: string): string | number {
  return fact(id).value;
}

/** The value as a string, for attributes and text nodes. */
export function text(id: string): string {
  return String(fact(id).value);
}

/** The value as a number, or fail. For arithmetic in the interactive artifacts. */
export function num(id: string): number {
  const v = fact(id).value;
  if (typeof v !== 'number') {
    throw new Error(`Fact "${id}" is ${JSON.stringify(v)}, not a number.`);
  }
  return v;
}

/** Every fact whose id starts with the given dotted prefix. */
export function family(prefix: string): Fact[] {
  const p = prefix.endsWith('.') ? prefix : `${prefix}.`;
  return file.facts.filter((f) => f.id === prefix || f.id.startsWith(p));
}

export function byStatus(status: Status): Fact[] {
  return file.facts.filter((f) => f.status === status);
}

/**
 * True when the fact rests on a primary source read from a page image.
 *
 * The project's standing rule is that OCR is not evidence, because commas are
 * the first thing it loses and this project's entire premise is that commas
 * matter. The site surfaces the distinction rather than flattening every
 * citation into the same confident grey.
 */
export function readFromPageImage(f: Fact): boolean {
  return f.source?.read_from === 'page image';
}

/** A GitHub link to the repository file that owns the value. */
const REPO_BLOB = 'https://github.com/incrediblecrab/godel-loopholes/blob/main/';

export function canonicalUrl(f: Fact): string {
  return REPO_BLOB + f.canonical;
}

export function analysisUrl(f: Fact): string | undefined {
  return f.analysis ? REPO_BLOB + f.analysis : undefined;
}

/**
 * Facts that carry an explicit epistemic warning a reader must not miss.
 *
 * Used by the shell to decide whether a claim renders with a status marker. A
 * verified fact does not need one -- everything on this site is verified unless
 * it says otherwise, and marking the ordinary case teaches a reader to ignore
 * the marker.
 */
export function needsStatusMarker(f: Fact): boolean {
  return f.status !== 'verified';
}
