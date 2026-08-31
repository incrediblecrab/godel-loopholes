/**
 * Exercises the four-state ablation hero with JavaScript disabled.
 *
 * The whole point of building it from checkboxes and `:checked ~` selectors is
 * that it works without scripting, so testing it with JS enabled would prove
 * nothing about the claim being made.
 *
 * Serves dist/ itself rather than expecting a preview server on a known port,
 * so it can run unattended in the verify chain. A guard that needs a human to
 * start a server first is a guard that never runs.
 */
import { chromium } from 'playwright';
import { serveDist } from './lib/serve-dist.mjs';

const server = await serveDist();
const BASE = `${server.origin}${server.base}`;
const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  deviceScaleFactor: 2,
  javaScriptEnabled: false,
});
const page = await ctx.newPage();
await page.goto(`${BASE}/`, { waitUntil: 'load' });

const combos = [
  { ablate: false, repair: false, want: 'published-full' },
  { ablate: true, repair: false, want: 'published-ablated' },
  { ablate: false, repair: true, want: 'repaired-full' },
  { ablate: true, repair: true, want: 'repaired-ablated' },
];

async function setState(id, want) {
  const box = page.locator(`#${id}`);
  if ((await box.isChecked()) !== want) {
    await page.locator(`label[for="${id}"]`).click();
  }
  if ((await box.isChecked()) !== want) {
    throw new Error(`could not set ${id} to ${want} by clicking its label`);
  }
}

let failures = 0;
for (const c of combos) {
  await setState('inert-ablate', c.ablate);
  await setState('inert-repair', c.repair);

  const shown = await page.$$eval('.inert__state', (ns) =>
    ns.filter((n) => getComputedStyle(n).display !== 'none')
      .map((n) => n.getAttribute('data-state')));

  const ok = shown.length === 1 && shown[0] === c.want;
  if (!ok) failures += 1;
  console.log(
    `${ok ? 'PASS' : 'FAIL'}  ablate=${String(c.ablate).padEnd(5)} repair=${String(c.repair).padEnd(5)} -> [${shown.join(', ')}] want ${c.want}`,
  );

  if (!ok) {
    await page.locator('.inert').screenshot({ path: `/tmp/gl-state-${c.want}.png` });
    console.log(`      wrote /tmp/gl-state-${c.want}.png`);
  }
}

// The struck cells must be exactly the step-one axioms, and only when ablated.
await setState('inert-ablate', true);
await setState('inert-repair', false);
const struck = await page.$$eval(
  ".inert__state[data-state='published-ablated'] .inert__cell.is-struck",
  (ns) => ns.length);
console.log(`${struck === 4 ? 'PASS' : 'FAIL'}  published ablation strikes ${struck} cells, want 4`);
if (struck !== 4) failures += 1;

await setState('inert-repair', true);
const struckR = await page.$$eval(
  ".inert__state[data-state='repaired-ablated'] .inert__cell.is-struck",
  (ns) => ns.length);
console.log(`${struckR === 5 ? 'PASS' : 'FAIL'}  repaired ablation strikes ${struckR} cells, want 5`);
if (struckR !== 5) failures += 1;

await browser.close();
await server.close();
console.log(failures === 0 ? '\nall hero checks passed (JS disabled)' : `\n${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
