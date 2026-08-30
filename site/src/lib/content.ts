/**
 * Build-time readers for the repository's own markdown.
 *
 * The site does not keep a second copy of the prose. `eli5.md` is the canonical
 * general-audience telling of this project and the site renders it; if the site
 * needs a new paragraph, the paragraph goes into `eli5.md`, not beside it. That
 * is the same rule `data/facts.json` enforces for values, applied to narrative:
 * one place, or it drifts.
 *
 * Everything here runs at build time under Node. None of it ships.
 */

import { readFileSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { Marked } from 'marked';

/**
 * Find the repository root by walking up from the working directory.
 *
 * Deliberately not `import.meta.url`. Astro bundles this module into
 * `dist/.prerender/chunks/`, so at build time the module's own path is several
 * directories away from where the source sits and every relative path computed
 * from it is wrong. That failure is silent in dev and loud only at build, which
 * is the worst combination.
 *
 * Two markers, not one: a directory that merely contains `verify.sh` could be
 * anything, but one that contains `verify.sh` and `data/facts.json` is this
 * repository.
 */
function findRepoRoot(): string {
  let dir = resolve(process.cwd());
  for (let i = 0; i < 8; i += 1) {
    if (existsSync(join(dir, 'verify.sh')) && existsSync(join(dir, 'data', 'facts.json'))) {
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error(
    `Could not find the repository root above ${process.cwd()}. ` +
      `Looked for a directory containing both verify.sh and data/facts.json.`,
  );
}

export const REPO_ROOT = findRepoRoot();

const REPO_BLOB = 'https://github.com/incrediblecrab/godel-loopholes/blob/main/';

export function repoFile(relPath: string): string {
  const full = join(REPO_ROOT, relPath);
  if (!existsSync(full)) {
    throw new Error(
      `The site asked for ${relPath}, which does not exist in the repository. ` +
        `A renamed research file should break the build, not silently empty a page.`,
    );
  }
  return readFileSync(full, 'utf8');
}

/**
 * A configured Marked instance.
 *
 * `gfm` for tables, which the silence inventory needs. Smart typography is off:
 * this project's entire premise is that a comma changes what a law means, and a
 * renderer that rewrites punctuation is the last thing it should use. Quotation
 * marks in the constitutional text are curled deliberately in the source or not
 * at all.
 */
const md = new Marked({
  gfm: true,
  breaks: false,
  // No `sanitize` option exists in current Marked and none is wanted: the input
  // is this repository's own tracked markdown, not user submissions. Nothing on
  // this site accepts input from anyone.
});

export interface Section {
  /** URL-safe id derived from the heading. */
  slug: string;
  /** The heading text, markdown stripped. */
  title: string;
  /** Rendered HTML of everything under the heading, excluding the heading. */
  html: string;
  /** The raw markdown, for callers that want to transform it themselves. */
  markdown: string;
}

export function slugify(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

/**
 * Split a markdown document on its level-2 headings.
 *
 * Returns the sections in document order. Content before the first `##` is
 * dropped, which for every file here is the level-1 title.
 */
export function sections(markdown: string): Section[] {
  const lines = markdown.split('\n');
  const out: Section[] = [];
  let current: { title: string; body: string[] } | null = null;
  let inFence = false;

  for (const line of lines) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    const h2 = !inFence && /^##\s+(.+?)\s*$/.exec(line);
    if (h2) {
      if (current) out.push(finish(current));
      current = { title: h2[1], body: [] };
    } else if (current) {
      current.body.push(line);
    }
  }
  if (current) out.push(finish(current));
  return out;

  function finish(c: { title: string; body: string[] }): Section {
    const raw = c.body.join('\n').trim();
    const title = c.title.replace(/[*_`]/g, '');
    return {
      slug: slugify(title),
      title,
      markdown: raw,
      html: render(raw),
    };
  }
}

/** Render a markdown fragment to HTML. */
export function render(markdown: string): string {
  return md.parse(markdown, { async: false }) as string;
}

/** Read a repository markdown file and split it into level-2 sections. */
export function readSections(relPath: string): Section[] {
  return sections(repoFile(relPath));
}

/** Pick sections by slug, in the order given, failing loudly on a typo. */
export function pick(all: Section[], ...slugs: string[]): Section[] {
  return slugs.map((slug) => {
    const found = all.find((s) => s.slug === slug);
    if (!found) {
      throw new Error(
        `No section "${slug}". Available: ${all.map((s) => s.slug).join(', ')}`,
      );
    }
    return found;
  });
}

/**
 * Parse the first GitHub-flavoured markdown table out of a document.
 *
 * The silence inventory is a twelve-row table in a research note, and the site
 * renders it as an interactive artifact. Parsing it rather than retyping it is
 * the difference between one source of truth and two.
 */
export interface Table {
  headers: string[];
  rows: string[][];
}

export function firstTable(markdown: string): Table {
  const lines = markdown.split('\n');
  const start = lines.findIndex(
    (l, i) =>
      /^\s*\|/.test(l) &&
      i + 1 < lines.length &&
      /^\s*\|[\s:|-]+\|?\s*$/.test(lines[i + 1]),
  );
  if (start === -1) throw new Error('No GFM table found in the given markdown.');

  const cells = (line: string): string[] =>
    line
      .trim()
      .replace(/^\||\|$/g, '')
      .split('|')
      .map((c) => c.trim());

  const headers = cells(lines[start]);
  const rows: string[][] = [];
  for (let i = start + 2; i < lines.length; i += 1) {
    if (!/^\s*\|/.test(lines[i])) break;
    rows.push(cells(lines[i]));
  }
  return { headers, rows };
}

/** Render inline markdown (bold, italics, code, links) without a paragraph wrapper. */
export function inline(markdown: string): string {
  return md.parseInline(markdown, { async: false }) as string;
}

export function blobUrl(relPath: string): string {
  return REPO_BLOB + relPath;
}

/**
 * Pull the ordered list that follows a heading, at any heading level.
 *
 * The eight disproved claims live in README.md as a numbered list. They are
 * the most persuasive object on this site and there must be exactly one copy
 * of them, so the site parses them out rather than restating them. If someone
 * disproves a ninth, the site grows a ninth with no edit here.
 */
export function orderedListUnder(relPath: string, heading: string): string[] {
  const text = repoFile(relPath);
  const lines = text.split('\n');
  const at = lines.findIndex(
    (l) => /^#{1,6}\s/.test(l) && l.replace(/^#{1,6}\s*/, '').trim() === heading,
  );
  if (at === -1) {
    const found = lines
      .filter((l) => /^#{1,6}\s/.test(l))
      .map((l) => l.replace(/^#{1,6}\s*/, '').trim());
    throw new Error(`No heading "${heading}" in ${relPath}. Have: ${found.join(' | ')}`);
  }

  const items: string[] = [];
  for (let i = at + 1; i < lines.length; i++) {
    const line = lines[i];
    if (/^#{1,6}\s/.test(line)) break;
    const m = /^\s*\d+\.\s+(.*)$/.exec(line);
    if (m) {
      items.push(m[1].trim());
    } else if (items.length && /^\s+\S/.test(line)) {
      items[items.length - 1] += ' ' + line.trim();
    }
  }
  if (!items.length) {
    throw new Error(`Heading "${heading}" in ${relPath} is not followed by a numbered list`);
  }
  return items;
}

/**
 * The negative controls, read out of verify.sh's own section headers.
 *
 * A harness that has never been seen to fail is not evidence that anything
 * passed, so some of its checks are built to fail if the thing they test is
 * broken in the opposite direction. Those sections label themselves, and this
 * reads the labels rather than trusting a count typed on a web page.
 */
export function negativeControls(): { id: string; title: string }[] {
  const text = repoFile('verify.sh');
  const out: { id: string; title: string }[] = [];
  const re = /^\s*hdr\s+"([0-9a-z]+)\.\s+NEGATIVE CONTROL[:\u2014-]*\s*(.*?)"\s*$/gim;
  let m: RegExpExecArray | null;
  while ((m = re.exec(text))) {
    out.push({ id: m[1], title: m[2].trim() });
  }
  if (!out.length) throw new Error('No negative-control headers found in verify.sh');
  return out;
}
