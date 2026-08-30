#!/usr/bin/env node
/**
 * Seal the Content-Security-Policy over the exact scripts that shipped.
 *
 * Astro inlines module scripts when they are small, and all three of this
 * site's islands are small -- about 2.4 KB between them. An inline script is
 * blocked by `script-src 'self'`, so there were three ways out:
 *
 *   1. Add 'unsafe-inline'. That is the one directive actually doing work here,
 *      and turning it off to make a toggle work is the wrong trade.
 *   2. Force the scripts external. Then `'self'` permits *any* same-origin
 *      script, which is weaker than what follows.
 *   3. Hash them. `script-src 'sha256-...'` permits exactly those bytes and
 *      nothing else -- not a different inline script, not an external one.
 *
 * Three is strictly the strongest and is the standard technique for a static
 * host that cannot set response headers. This walks the built HTML, hashes
 * every inline script, and writes the hashes into that page's policy.
 *
 *   node scripts/seal-csp.mjs           # seal
 *   node scripts/seal-csp.mjs --check   # verify a sealed build, exit 1 if not
 *
 * The --check mode exists because a security control nobody verifies is a
 * comment, not a control.
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join, relative, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(siteRoot, 'dist');
const check = process.argv.includes('--check');

const SCRIPT = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
const CSP_META = /(<meta http-equiv="Content-Security-Policy" content=")([^"]*)(")/i;

function html(dir) {
  const out = [];
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return out;
  }
  for (const e of entries) {
    const full = join(dir, e);
    if (statSync(full).isDirectory()) out.push(...html(full));
    else if (e.endsWith('.html')) out.push(full);
  }
  return out;
}

const pages = html(dist);
if (pages.length === 0) {
  console.error('seal-csp  no HTML in dist/. Run the build first.');
  process.exit(1);
}

let sealed = 0;
let scripts = 0;
const problems = [];

for (const page of pages) {
  const rel = relative(dist, page);
  let source = readFileSync(page, 'utf8');

  const hashes = [];
  SCRIPT.lastIndex = 0;
  let m;
  while ((m = SCRIPT.exec(source)) !== null) {
    const body = m[1];
    // An empty inline script needs no hash and would produce a useless one.
    if (body.trim() === '') continue;
    const digest = createHash('sha256').update(body, 'utf8').digest('base64');
    hashes.push(`'sha256-${digest}'`);
    scripts += 1;
  }

  const meta = CSP_META.exec(source);
  if (!meta) {
    problems.push(`${rel}: no Content-Security-Policy meta tag`);
    continue;
  }

  const policy = meta[2];

  if (check) {
    for (const h of hashes) {
      if (!policy.includes(h)) {
        problems.push(`${rel}: an inline script is not covered by the policy (${h})`);
      }
    }
    // A policy that still permits arbitrary inline script defeats the exercise.
    if (/script-src[^;]*'unsafe-inline'/.test(policy)) {
      problems.push(`${rel}: script-src contains 'unsafe-inline'`);
    }
    // A hash source suppresses 'unsafe-inline' but NOT 'self'. Leaving 'self'
    // beside the hashes means any same-origin script URL still executes, so
    // the policy would be exactly as strong as 'self' and no stronger --
    // which is not what this script or the layout comment claim.
    if (/script-src[^;]*'self'/.test(policy)) {
      problems.push(
        `${rel}: script-src still contains 'self', so the hashes buy nothing`,
      );
    }
    if (hashes.length === 0 && !/script-src\s+'none'/.test(policy)) {
      problems.push(
        `${rel}: has no inline script but does not say script-src 'none'`,
      );
    }
    if (/script-src[^;]*'unsafe-eval'/.test(policy)) {
      problems.push(`${rel}: script-src contains 'unsafe-eval'`);
    }
    sealed += 1;
    continue;
  }

  // Replace script-src outright rather than appending to it. 'self' must go:
  // a hash source suppresses 'unsafe-inline' but not 'self', so appending
  // leaves a policy exactly as strong as 'self' while reading like a pinned
  // one. The build emits no external <script src> at all, so nothing is lost.
  const next = policy.replace(/(script-src)([^;]*)/, (_all, key, rest) => {
    const keep = rest
      .trim()
      .split(/\s+/)
      .filter((t) => t && t !== "'self'" && !t.startsWith("'sha256-"));
    const sources = hashes.length > 0 ? [...keep, ...hashes] : [...keep, "'none'"];
    return `${key} ${sources.join(' ')}`.replace(/\s+/g, ' ');
  });

  if (next !== policy) {
    source = source.replace(CSP_META, `$1${next}$3`);
    writeFileSync(page, source, 'utf8');
    sealed += 1;
  }
}

const verb = check ? 'verified' : 'sealed';
if (problems.length > 0) {
  console.error(`seal-csp  ${problems.length} problem(s):`);
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}

console.log(
  `seal-csp  ${verb} ${sealed} page(s), ${scripts} inline script(s) pinned by hash, ` +
    `${pages.length} page(s) scanned`,
);
