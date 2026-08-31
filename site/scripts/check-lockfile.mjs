#!/usr/bin/env node
/**
 * Fail if package-lock.json is not installable on a platform other than this one.
 *
 * The same failure has now reached CI three times: `npm ci` on ubuntu-latest
 * dies with EUSAGE and `Missing: @emnapi/core@... from lock file`, while
 * everything installs perfectly on the macOS machine that wrote the lockfile.
 *
 * The mechanism. Optional dependencies are platform-filtered, and an
 * incremental `npm install` on macOS records only what macOS resolves. The
 * Linux-only WASM fallbacks reached through @img/sharp-wasm32 -- @emnapi/core
 * and @emnapi/runtime -- get pruned back out. `npm install --package-lock-only`
 * does the same thing; it is the pruning mechanism, not a repair for it.
 *
 * Why the previous guard did not catch it. It ran
 *
 *     npm ci --dry-run --os=linux --cpu=x64
 *
 * which passes on macOS against a lockfile that real `npm ci` on Linux rejects.
 * Those flags change which optional packages npm would install; they do not
 * make npm re-check that the entries are present. A guard that cannot fail is
 * not a guard, and this one reported success for three consecutive breakages.
 *
 * What this checks instead is a structural property of the file, so it gives
 * the same answer on every platform: every dependency named by every package
 * in the lockfile must resolve, by node_modules lookup rules, to a package
 * entry that actually exists in the lockfile at a satisfying version. That is
 * the invariant `npm ci` enforces. Checking it directly needs no network, no
 * install, and no Linux.
 *
 *   node scripts/check-lockfile.mjs [path-to-lockfile]
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { join, dirname } from 'node:path';
import semver from 'semver';

const here = dirname(fileURLToPath(import.meta.url));
const lockPath = process.argv[2] ?? join(here, '..', 'package-lock.json');
const lock = JSON.parse(readFileSync(lockPath, 'utf8'));
const pkgs = lock.packages;

if (!pkgs) {
  console.error(`check-lockfile: ${lockPath} has no "packages" map (lockfileVersion < 2?)`);
  process.exit(1);
}

/**
 * Resolve `name` as required from the package at lockfile key `fromPath`,
 * following node_modules lookup: try the requiring package's own
 * node_modules, then each ancestor's, then the root.
 */
function resolve(fromPath, name) {
  const segments = fromPath === '' ? [] : fromPath.split('/node_modules/');
  for (let i = segments.length; i >= 0; i -= 1) {
    const prefix = segments.slice(0, i).join('/node_modules/');
    const candidate = prefix === '' ? `node_modules/${name}` : `${prefix}/node_modules/${name}`;
    if (Object.hasOwn(pkgs, candidate)) return pkgs[candidate];
  }
  return null;
}

const problems = [];

for (const [path, meta] of Object.entries(pkgs)) {
  // A link entry points at a workspace elsewhere in the file; the target is
  // checked on its own iteration.
  if (meta.link) continue;

  for (const field of ['dependencies', 'optionalDependencies', 'peerDependencies']) {
    for (const [name, range] of Object.entries(meta[field] ?? {})) {
      // Peer dependencies may legitimately be absent when optional.
      if (field === 'peerDependencies' && meta.peerDependenciesMeta?.[name]?.optional) continue;

      const found = resolve(path, name);
      if (!found) {
        problems.push(`${path || '<root>'} needs ${name}@${range} — no entry in the lockfile resolves it`);
        continue;
      }
      // Non-registry ranges (file:, link:, git, npm: aliases, "*") are not
      // semver comparisons; existence is all this check can assert for them.
      if (found.version && semver.validRange(range) && !semver.satisfies(found.version, range, { includePrerelease: true })) {
        problems.push(`${path || '<root>'} needs ${name}@${range} but resolves ${found.version}`);
      }
    }
  }
}

if (problems.length) {
  console.error(`\n  LOCKFILE INCOMPLETE — ${problems.length} unresolved dependency reference(s).\n`);
  for (const p of problems.slice(0, 20)) console.error(`    ${p}`);
  if (problems.length > 20) console.error(`    ... and ${problems.length - 20} more`);
  console.error(`
  This is the failure that breaks 'npm ci' on Linux while installing fine here.
  Regenerate the lockfile from scratch — not with --package-lock-only, which
  prunes the platform-specific entries back out:

      cd site && rm -rf node_modules package-lock.json && npm install
`);
  process.exit(1);
}

console.log(`lockfile  ${Object.keys(pkgs).length} packages, every dependency reference resolves`);
