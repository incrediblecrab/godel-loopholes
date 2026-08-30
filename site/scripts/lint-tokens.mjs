#!/usr/bin/env node
/**
 * Every custom property the site uses must be one the design system defines.
 *
 * This exists because `font-family: var(--font-mono)` is silently valid CSS
 * when `--font-mono` does not exist. The declaration is simply dropped and the
 * element inherits, so a typo in a token name produces a page that looks
 * almost right and is never flagged by a build, a type checker or a browser
 * console. Three of them shipped before this script was written.
 *
 * Definitions are read from src/styles/, which is where the design system
 * lives. Uses are read from every source file. A property that is defined and
 * never used is reported too, but only as a note: an unused token is dead
 * weight, not a defect.
 *
 * Run: node scripts/lint-tokens.mjs
 */
import { readFileSync, globSync } from 'node:fs';

import { fileURLToPath } from 'node:url';
import { dirname, join, relative } from 'node:path';

const SITE = dirname(dirname(fileURLToPath(import.meta.url)));
const SRC = join(SITE, 'src');

const files = globSync('**/*.{css,astro,ts,tsx}', { cwd: SRC }).sort();

/** Blank out comments so a token named only inside one is not counted. */
function strip(text) {
  return text.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
}

const defined = new Map(); // name -> where it was defined
const used = new Map(); // name -> [{file, line}]

for (const rel of files) {
  const abs = join(SRC, rel);
  const text = strip(readFileSync(abs, 'utf8'));
  const lines = text.split('\n');

  lines.forEach((line, i) => {
    // A definition is `--name:` in a declaration position. A use inside
    // var(--name, --other) is not a definition, hence the leading boundary.
    for (const m of line.matchAll(/(?:^|[;{]|\s)(--[A-Za-z0-9-]+)\s*:/g)) {
      // Only src/styles/ defines the design system. A component defining its
      // own token is legal CSS but is a second source of truth for a value,
      // so those are recorded separately and allowed.
      const where = rel.startsWith('styles/') ? 'system' : 'local';
      if (!defined.has(m[1]) || where === 'system') defined.set(m[1], where);
    }

    for (const m of line.matchAll(/var\(\s*(--[A-Za-z0-9-]+)/g)) {
      if (!used.has(m[1])) used.set(m[1], []);
      used.get(m[1]).push({ file: rel, line: i + 1, text: line.trim() });
    }
  });
}

const undef = [...used.keys()].filter((n) => !defined.has(n)).sort();

// A var() with a fallback -- var(--x, 1rem) -- still works when --x is
// missing, so it is reported but does not fail the build.
const withFallback = new Set();
for (const rel of files) {
  const text = strip(readFileSync(join(SRC, rel), 'utf8'));
  for (const m of text.matchAll(/var\(\s*(--[A-Za-z0-9-]+)\s*,/g)) withFallback.add(m[1]);
}

const fatal = undef.filter((n) => !withFallback.has(n));
const soft = undef.filter((n) => withFallback.has(n));

const unused = [...defined.entries()]
  .filter(([n, where]) => where === 'system' && !used.has(n))
  .map(([n]) => n)
  .sort();

console.log(
  `\nlint:tokens  ${files.length} files, ${defined.size} properties defined, ${used.size} used`,
);

if (soft.length) {
  console.log(`\n${soft.length} undefined but carrying a fallback (not fatal):`);
  for (const n of soft) console.log(`  ${n}`);
}

if (unused.length) {
  console.log(`\n${unused.length} defined and never used:`);
  console.log('  ' + unused.join(' '));
}

if (fatal.length) {
  console.log(`\n${fatal.length} UNDEFINED custom propert${fatal.length === 1 ? 'y' : 'ies'}:\n`);
  for (const n of fatal) {
    for (const u of used.get(n)) {
      console.log(`  ${u.file}:${u.line}`);
      console.log(`    ${u.text.slice(0, 96)}`);
    }
    const near = [...defined.keys()]
      .filter((d) => d.startsWith(n.slice(0, 7)) || n.startsWith(d.slice(0, 7)))
      .sort();
    console.log(`    -> ${n} is not defined${near.length ? `. Did you mean ${near.join(', ')}?` : ''}\n`);
  }
  console.log(
    'A var() naming a property that does not exist is silently dropped by the\n' +
      'browser, so the element inherits and the page looks almost right. Nothing\n' +
      'else in the toolchain catches this.\n',
  );
  process.exit(1);
}

console.log('\nEvery custom property used is one the design system defines.\n');
