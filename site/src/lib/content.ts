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
