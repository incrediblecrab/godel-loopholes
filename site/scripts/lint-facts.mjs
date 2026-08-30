#!/usr/bin/env node
/**
 * Fail the build if a component types a load-bearing value instead of looking
 * it up.
 *
 * The governing rule of this repository is that narrative is authored per
 * audience but facts are single-sourced. A site is the most likely place for
 * that rule to break, because typing `146` is faster than importing an
 * accessor and the result looks identical the day it is written. It stops
 * looking identical the day the number changes in one place and not the other,
 * and by then the site has been lying in public for a while.
 *
 * So this reads data/facts.json and greps the site source for the literal
 * values. Any hit outside src/lib/facts.ts is a build failure.
 *
 * HONESTY ABOUT COVERAGE. This cannot police every fact. Small integers -- 0
 * loopholes, 3 theorems, 5 lemmas, 6 sufficient axioms -- appear in ordinary
 * code as array lengths, CSS values and loop bounds, and flagging every `3`
 * would produce so much noise that people would learn to suppress it, which is
 * worse than not checking. The script therefore reports exactly which facts it
 * can and cannot enforce, and the number it prints is the number it means.
 */

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, relative, extname } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = join(here, '..');
const repoRoot = join(siteRoot, '..');
const srcRoot = join(siteRoot, 'src');

const facts = JSON.parse(readFileSync(join(repoRoot, 'data', 'facts.json'), 'utf8'));

/** The accessor is allowed to know about facts.json. Nothing else is. */
const EXEMPT = new Set(['src/lib/facts.ts']);

const EXTENSIONS = new Set(['.astro', '.ts', '.tsx', '.js', '.mjs', '.jsx']);

/**
 * A numeric value is enforceable when a bare occurrence of it in source is
 * overwhelmingly more likely to be the fact than a coincidence. Three digits,
 * or two digits above 10, clears that bar. Single digits do not.
 */
function enforceableNumber(n) {
  return Number.isInteger(n) && n >= 12;
}

/**
 * A string value is enforceable when it is long enough to be distinctive and
 * short enough to be plausibly retyped. Very long quotations are handled by a
 * separate rule: any run of eight or more words from a fact's quotation.
 */
function enforceableString(s) {
  const trimmed = s.trim();
  return trimmed.length >= 8 && trimmed.split(/\s+/).length <= 12;
}

const enforced = [];
const unenforced = [];

for (const f of facts.facts) {
  if (typeof f.value === 'number') {
    if (enforceableNumber(f.value)) {
      enforced.push({
        id: f.id,
        needle: String(f.value),
        // Word boundaries alone would match 435 inside 1435. Require the digits
        // not be adjacent to other digits or to a decimal point.
        // Word boundaries alone would match 435 inside 1435. Require the digits
        // not be adjacent to other digits or to a decimal point, and not be
        // followed by a CSS unit -- `32ch` is a measure, not the thirty-two
        // states needed for a convention, and flagging it teaches people to
        // ignore this script. The unit must be immediately adjacent: a real
        // CSS length never has a space before its unit, and allowing one
        // exempted "435 in the House of Representatives" -- exactly the
        // hardcoded value this script exists to catch.
        re: new RegExp(
          `(?<![\\d.])${f.value}(?![\\d.])(?!(?:ch|r?em|px|%|vw|vh|vmin|vmax|fr|deg|m?s|pt|cm|mm|in|q|ex|cap|lh|rlh|dvh|svh|lvh)\\b)`,
          'g',
        ),
        kind: 'number',
      });
    } else {
      unenforced.push({
        id: f.id,
        value: f.value,
        why: 'single-digit integers occur too often in ordinary code to flag safely',
      });
    }
  } else if (typeof f.value === 'string') {
    if (enforceableString(f.value)) {
      enforced.push({
        id: f.id,
        needle: f.value,
        re: new RegExp(escapeRe(f.value), 'g'),
        kind: 'string',
      });
    } else {
      unenforced.push({
        id: f.id,
        value: String(f.value).slice(0, 60),
        why:
          String(f.value).trim().length < 8
            ? 'too short to be distinctive'
            : 'a long passage; enforced by the phrase rule instead',
      });
      // Long quotations still get policed, but on several overlapping windows
      // rather than one fixed slice. A single window is trivially missed by a
      // paraphrase that starts a word earlier, which a negative control on this
      // very script demonstrated.
      const words = f.value.trim().split(/\s+/);
      if (words.length > 12) {
        const WINDOW = 6;
        // Stride 1. A stride of 3 leaves gaps a paraphrase falls straight
        // through -- the negative control on this script planted a phrase that
        // began one word off a window boundary and was missed. The cost of
        // every window is a few hundred extra regexes over a handful of files,
        // which is nothing next to a quotation drifting in public.
        for (let i = 0; i + WINDOW <= words.length; i += 1) {
          const phrase = words.slice(i, i + WINDOW).join(' ');
          enforced.push({
            id: f.id,
            needle: phrase,
            re: new RegExp(escapeRe(phrase), 'g'),
            kind: 'phrase',
          });
        }
      }
    }
  }
}

function escapeRe(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Blank out regions that cannot reach a reader, preserving offsets so line
 * numbers stay honest.
 *
 * A `<style>` block is full of dimensions -- 48rem, 32ch, 12px -- that collide
 * with real facts and are not claims about anything. Block comments are prose
 * about the code. Both get replaced with spaces of the same length rather than
 * removed, so a violation's reported line number still points at the right
 * line.
 */
function blankNonRendering(source) {
  const blank = (m) => m.replace(/[^\n]/g, ' ');
  return source
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, blank)
    .replace(/\/\*[\s\S]*?\*\//g, blank)
    .replace(/<!--[\s\S]*?-->/g, blank);
}

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir)) {
    if (entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) out.push(...walk(full));
    else if (EXTENSIONS.has(extname(entry))) out.push(full);
  }
  return out;
}

let files = [];
try {
  files = walk(srcRoot);
} catch {
  console.error(`lint:facts  cannot read ${relative(siteRoot, srcRoot)}`);
  process.exit(1);
}

const violations = [];
const seen = new Set();

for (const file of files) {
  const rel = relative(siteRoot, file).split('\\').join('/');
  if (EXEMPT.has(rel)) continue;
  const source = blankNonRendering(readFileSync(file, 'utf8'));
  const lines = source.split('\n');

  for (const rule of enforced) {
    rule.re.lastIndex = 0;
    let m;
    while ((m = rule.re.exec(source)) !== null) {
      const upto = source.slice(0, m.index);
      const lineNo = upto.split('\n').length;
      const line = lines[lineNo - 1] ?? '';

      // A line that mentions the fact id is doing the right thing; the value
      // appearing next to it is a comment explaining what the id resolves to.
      if (line.includes(rule.id)) continue;
      // Comments are prose about the code, not rendered output.
      if (/^\s*(\/\/|\*|\/\*|<!--|#)/.test(line)) continue;

      // Overlapping quotation windows would otherwise report the same line
      // once per window.
      const key = `${rel}:${lineNo}:${rule.id}`;
      if (seen.has(key)) continue;
      seen.add(key);

      violations.push({ file: rel, line: lineNo, id: rule.id, kind: rule.kind, text: line.trim() });
    }
  }
}

const scanned = files.length;
// Count distinct facts, not rules: a long quotation contributes many
// overlapping windows and would otherwise inflate the coverage number.
const enforcedIds = new Set(enforced.map((r) => r.id));
const header = `lint:facts  ${scanned} file${scanned === 1 ? '' : 's'}, ${enforcedIds.size} of ${facts.facts.length} facts enforceable`;

if (violations.length === 0) {
  console.log(`${header}  --  clean`);
  if (process.argv.includes('--verbose')) {
    console.log(`\nNot enforceable (${unenforced.length}):`);
    for (const u of unenforced.filter((u) => !enforcedIds.has(u.id))) console.log(`  ${u.id.padEnd(28)} ${u.why}`);
  }
  process.exit(0);
}

console.error(`${header}\n`);
console.error(`${violations.length} hardcoded value${violations.length === 1 ? '' : 's'}:\n`);
for (const v of violations) {
  console.error(`  ${v.file}:${v.line}`);
  console.error(`    ${v.text}`);
  console.error(`    -> use the fact id "${v.id}" via src/lib/facts.ts, not the literal\n`);
}
console.error(
  'Every load-bearing value on this site resolves to data/facts.json, which\n' +
    'verify.sh section 6 checks against the canonical research file. A literal\n' +
    'here is a second source of truth and will drift.',
);
process.exit(1);
