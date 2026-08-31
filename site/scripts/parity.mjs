/**
 * Records or checks the rendered geometry of every page.
 *
 * The MDX migration must not move anything. Text equality is not enough: the
 * nested-<p> bug produced identical text and a broken box, and the namespaced
 * CSS leak moved an island 32px while every word stayed put. So the baseline is
 * per-element height and margin, captured from the .astro build before the
 * migration and compared against the MDX build after it.
 *
 *   node scripts/parity.mjs record <baseUrl>   -> writes parity-baseline.json
 *   node scripts/parity.mjs check  <baseUrl>   -> exits 1 on any drift
 */
import { chromium } from 'playwright';
import { readFileSync, writeFileSync } from 'node:fs';

const PAGES = ['', 'text', 'machine', 'method', 'precedents'];
const FILE = 'parity-baseline.json';
const [mode, baseUrl] = process.argv.slice(2);
if (!['record', 'check'].includes(mode) || !baseUrl) {
  console.error('usage: parity.mjs <record|check> <baseUrl>');
  process.exit(2);
}

const browser = await chromium.launch();
const seen = {};
for (const page of PAGES) {
  const p = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  const url = `${baseUrl.replace(/\/$/, '')}/${page}${page ? '/' : ''}`;
  await p.goto(url, { waitUntil: 'networkidle' });
  seen[page || 'index'] = await p.evaluate(() =>
    [...document.querySelectorAll('.page > *, .page section > *, .page > div.wide > *')].map((e) => {
      const cs = getComputedStyle(e);
      return [
        e.tagName + '.' + (e.className || '').toString().trim().split(/\s+/).join('.'),
        Math.round(e.getBoundingClientRect().height),
        cs.marginTop,
      ].join('|');
    }),
  );
  await p.close();
}
await browser.close();

if (mode === 'record') {
  writeFileSync(FILE, JSON.stringify(seen, null, 2) + '\n');
  const n = Object.values(seen).reduce((a, b) => a + b.length, 0);
  console.log(`parity  recorded ${n} elements across ${PAGES.length} pages -> ${FILE}`);
  process.exit(0);
}

const base = JSON.parse(readFileSync(FILE, 'utf8'));
let bad = 0;
for (const [name, list] of Object.entries(base)) {
  const now = seen[name] ?? [];
  if (now.length !== list.length) {
    console.error(`  ${name}: element count ${list.length} -> ${now.length}`);
    bad++;
    continue;
  }
  list.forEach((want, i) => {
    if (want !== now[i]) {
      console.error(`  ${name}[${i}]\n     was: ${want}\n     now: ${now[i]}`);
      bad++;
    }
  });
}
if (bad) {
  console.error(`\nparity  ${bad} element(s) moved`);
  process.exit(1);
}
const n = Object.values(base).reduce((a, b) => a + b.length, 0);
console.log(`parity  ${n} elements across ${PAGES.length} pages unchanged`);
