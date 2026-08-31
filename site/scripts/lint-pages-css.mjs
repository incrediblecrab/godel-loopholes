/**
 * Guards src/styles/pages.css.
 *
 * MDX pages cannot use Astro's scoped <style>, so page CSS is isolated by
 * namespace instead. Namespacing is a convention, and a convention that nothing
 * checks is a convention that decays. This is the check.
 *
 * The failure it exists to catch is invisible and already happened once.
 * Astro's scoping stamps a data attribute on the elements of one template, so a
 * bare `section` in a page's <style> can never reach a <section> inside an
 * island. Rewritten as `.page-text section` it reaches every section on the
 * page, islands included, and RecensionDiff silently grew 32px.
 *
 * Three rules:
 *
 *   1. Every selector is anchored to a .page-<section> namespace. An unanchored
 *      rule in a globally imported sheet is a site-wide style with no warning.
 *
 *   2. An element selector must be reachable only within page-owned markup:
 *      either via a child combinator from the namespace, or beneath a class
 *      that no island uses. Both confine it to a subtree the page controls.
 *
 *   3. A page must not style a class that appears inside an island it actually
 *      renders. Checked per page rather than globally, because `.controls` on
 *      the method page is only a problem if the method page shows an island
 *      that uses `.controls`.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const CSS = 'src/styles/pages.css';
const ISLANDS = 'src/islands';
const COMPONENTS = 'src/components';
const PAGES = 'src/pages';

const ELEMENTS = new Set([
  'a', 'abbr', 'article', 'aside', 'blockquote', 'button', 'caption', 'code',
  'dd', 'details', 'div', 'dl', 'dt', 'em', 'figcaption', 'figure', 'footer',
  'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hr', 'img', 'input',
  'label', 'li', 'main', 'nav', 'ol', 'p', 'pre', 'section', 'select', 'small',
  'span', 'strong', 'summary', 'sup', 'table', 'tbody', 'td', 'th', 'thead',
  'tr', 'ul',
]);

const classesIn = (template) => {
  const out = new Set();
  for (const c of template.matchAll(/class(?:List)?=["'{]([^"'}]+)/g)) {
    for (const name of c[1].split(/\s+/)) {
      if (/^[a-zA-Z][\w-]*$/.test(name)) out.add(name);
    }
  }
  return out;
};

/**
 * component name -> classes it uses.
 *
 * Covers src/islands and src/components alike: page CSS must not reach into
 * either. Prose.astro is deliberately exempt because it renders the page's own
 * markdown, so `.page-text .prose p` is the intended way to style that content.
 */
const PASSTHROUGH = new Set(['Prose']);
const islandClasses = new Map();
for (const [dir, files] of [
  [ISLANDS, readdirSync(ISLANDS)],
  [COMPONENTS, readdirSync(COMPONENTS)],
]) {
  for (const f of files.filter((f) => f.endsWith('.astro'))) {
    const name = f.replace(/\.astro$/, '');
    if (PASSTHROUGH.has(name)) continue;
    const body = readFileSync(join(dir, f), 'utf8');
    const template = body.replace(/^---[\s\S]*?^---/m, '').replace(/<style>[\s\S]*?<\/style>/g, '');
    islandClasses.set(name, classesIn(template));
  }
}

/** Components the layout renders on every page, so every page must respect them. */
const GLOBAL = new Set(
  [...readFileSync('src/layouts/Base.astro', 'utf8').matchAll(
    /from\s+['"][^'"]*(?:components|islands)\/([A-Za-z0-9_]+)\.astro['"]/g,
  )].map((m) => m[1]),
);

const anyIslandClass = new Set();
for (const set of islandClasses.values()) for (const c of set) anyIslandClass.add(c);

/**
 * page SECTION -> islands it renders.
 *
 * Keyed by section, not by filename. The namespace in pages.css is
 * `.page-<section>` because that is what Essay.astro stamps on the wrapper,
 * and section does not always equal filename: index.astro is section "claim".
 * Keying this map by filename made `.page-claim` look up "claim", miss, and
 * fall through to an empty set, so the island-collision rule below passed
 * vacuously for the whole homepage.
 */
const pageIslands = new Map();
for (const f of readdirSync(PAGES).filter((f) => /\.(astro|mdx)$/.test(f))) {
  const body = readFileSync(join(PAGES, f), 'utf8');
  const section = body.match(/^section:\s*["']?([a-z0-9-]+)/m)?.[1]
    ?? body.match(/\bsection=["']([a-z0-9-]+)["']/)?.[1];
  if (!section) {
    console.error(`lint:pages-css  ${f} declares no section, so its CSS namespace is unknown.`);
    process.exit(1);
  }
  const used = new Set(GLOBAL);
  for (const m of body.matchAll(
    /from\s+['"][^'"]*(?:components|islands)\/([A-Za-z0-9_]+)\.astro['"]/g,
  )) {
    if (!PASSTHROUGH.has(m[1])) used.add(m[1]);
  }
  pageIslands.set(section, used);
}

const src = readFileSync(CSS, 'utf8');
const noComments = src.replace(/\/\*[\s\S]*?\*\//g, '');
const selectors = [];
const re = /(^|[};])\s*([^{};@][^{}]*?)\s*\{/g;
let m;
while ((m = re.exec(noComments)) !== null) {
  const raw = m[2].trim();
  if (!raw || raw.startsWith('@')) continue;
  for (const part of raw.split(',')) {
    const s = part.trim();
    if (s) selectors.push(s);
  }
}

const problems = [];

for (const sel of selectors) {
  const ns = sel.match(/^\.page-([a-z0-9-]+)\b/);
  if (!ns) {
    problems.push(`unanchored selector (must start with .page-<section>): ${sel}`);
    continue;
  }
  const page = ns[1];

  // Rule 4: the namespace has to name a section that actually exists. A rule
  // under `.page-index` when no page declares section "index" is dead CSS, and
  // dead CSS here means an unstyled page rather than a visible error. This
  // caught a rename that a BSD sed had silently declined to perform.
  if (!pageIslands.has(page)) {
    problems.push(
      `.page-${page} matches no page. Known sections: ` +
        `${[...pageIslands.keys()].sort().join(', ')}: ${sel}`,
    );
    continue;
  }

  const rest = sel.replace(/^\.page-[a-z0-9-]+\s*/, '');
  if (!rest) continue;

  // Walk the compound steps left to right. An element step is safe if the
  // previous step was ">" (a child of page-owned markup) or if some earlier
  // step was a class no island uses (a page-owned container).
  let expectChild = false;
  let underPageOnlyClass = false;
  const collisions = [];
  for (const step of rest.split(/\s+/)) {
    if (step === '>') {
      expectChild = true;
      continue;
    }
    const head = step.match(/^([a-zA-Z][a-zA-Z0-9]*)/);
    if (head && ELEMENTS.has(head[1].toLowerCase()) && !expectChild && !underPageOnlyClass) {
      problems.push(
        `element selector "${step}" can reach inside an island. Anchor it with ">" ` +
          `or nest it under a page-only class: ${sel}`,
      );
    }
    for (const c of step.matchAll(/\.([a-zA-Z][\w-]*)/g)) {
      // A class collision only matters if nothing upstream has already confined
      // the selector to markup the page owns. `.next .smallcaps` is safe even
      // though islands use .smallcaps, because no island sits inside .next.
      if (!underPageOnlyClass) collisions.push(c[1]);
      if (!anyIslandClass.has(c[1])) underPageOnlyClass = true;
    }
    expectChild = false;
  }

  // Rule 3: does this page render an island that uses a class this rule styles?
  const rendered = pageIslands.get(page) ?? new Set();
  for (const cls of collisions) {
    for (const island of rendered) {
      if (islandClasses.get(island)?.has(cls)) {
        problems.push(
          `.page-${page} styles ".${cls}", and ${island} renders on that page using ` +
            `the same class: ${sel}`,
        );
      }
    }
  }
}

if (problems.length) {
  const unique = [...new Set(problems)];
  console.error(`lint-pages-css  ${unique.length} problem(s) in ${CSS}\n`);
  for (const p of unique) console.error(`  - ${p}`);
  process.exit(1);
}

console.log(
  `lint-pages-css  ${selectors.length} selectors across ${pageIslands.size} pages, ` +
    `all namespaced and component-safe`,
);
