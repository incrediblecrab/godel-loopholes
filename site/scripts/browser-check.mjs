#!/usr/bin/env node
/**
 * Load the built site in a real browser and check the things that only fail in
 * a browser.
 *
 * A Content-Security-Policy that has never been enforced against the actual
 * page is a comment. A keyboard path that has never been walked is an
 * assumption. Both of those are exactly the class of claim this repository's
 * harness exists to refuse, so they get checked the same way everything else
 * does: by running it.
 *
 * Serves dist/ over HTTP rather than file:// because a `file://` origin does
 * not enforce a meta CSP the way an `http://` one does, and testing under the
 * wrong conditions is worse than not testing.
 *
 *   node scripts/browser-check.mjs
 */

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const siteRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const dist = join(siteRoot, 'dist');
const BASE = '/godel-loopholes';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.woff2': 'font/woff2',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
};

const results = [];
const record = (ok, name, detail = '') => {
  results.push({ ok, name, detail });
  const mark = ok ? 'PASS' : 'FAIL';
  console.log(`  ${mark}  ${name}${detail ? `  ${detail}` : ''}`);
};

/* --------------------------------------------------------------- the server */

const server = createServer(async (req, res) => {
  try {
    let path = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    if (path.startsWith(BASE)) path = path.slice(BASE.length);
    if (path === '' || path.endsWith('/')) path += 'index.html';
    let full = join(dist, path);
    try {
      if ((await stat(full)).isDirectory()) full = join(full, 'index.html');
    } catch {
      /* fall through to the read, which produces the 404 */
    }
    const body = await readFile(full);
    // Deliberately no security headers. The point is to test the policy the
    // site actually carries in its own markup, not one the test server added.
    res.writeHead(200, { 'content-type': TYPES[extname(full)] ?? 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end('not found');
  }
});

await new Promise((r) => server.listen(0, '127.0.0.1', r));
const origin = `http://127.0.0.1:${server.address().port}`;

/* -------------------------------------------------------------- the checks */

const browser = await chromium.launch();

async function open(path, { js = true, viewport } = {}) {
  const context = await browser.newContext({
    javaScriptEnabled: js,
    ...(viewport ? { viewport } : {}),
  });
  const page = await context.newPage();
  const violations = [];
  const errors = [];
  const requests = [];

  page.on('console', (m) => {
    const t = m.text();
    if (/Content Security Policy|Refused to/i.test(t)) violations.push(t);
  });
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('request', (r) => requests.push(r.url()));

  const response = await page.goto(`${origin}${BASE}${path}`, { waitUntil: 'networkidle' });
  return { context, page, violations, errors, requests, response };
}

console.log('\n== browser checks ==\n');

/* --- every page loads, executes its scripts, and violates nothing --------- */

for (const path of ['/', '/precedents/', '/text/', '/machine/', '/method/']) {
  const { context, page, violations, errors, requests } = await open(path);

  record(
    violations.length === 0,
    `${path} raises no Content-Security-Policy violation`,
    violations.length ? violations[0].slice(0, 120) : '',
  );
  record(
    errors.length === 0,
    `${path} raises no uncaught script error`,
    errors.length ? errors[0].slice(0, 120) : '',
  );

  const offOrigin = requests.filter((u) => !u.startsWith(origin));
  record(
    offOrigin.length === 0,
    `${path} makes zero third-party requests`,
    offOrigin.length ? offOrigin.join(', ').slice(0, 160) : `${requests.length} same-origin`,
  );

  const title = await page.title();
  record(title.length > 0, `${path} has a title`, title);

  const h1 = await page.locator('h1').count();
  record(h1 === 1, `${path} has exactly one h1`, `found ${h1}`);

  // Every image and control that conveys meaning needs an accessible name.
  const unnamed = await page.evaluate(() => {
    const bad = [];
    for (const el of document.querySelectorAll('button, a, [role="img"]')) {
      const name =
        el.getAttribute('aria-label') ||
        el.getAttribute('title') ||
        (el.textContent || '').trim();
      if (!name) bad.push(el.outerHTML.slice(0, 80));
    }
    return bad;
  });
  record(unnamed.length === 0, `${path} every control has an accessible name`, unnamed[0] ?? '');

  // A heading that jumps h2 -> h4 is a broken outline for anyone navigating by
  // structure, and it is invisible to everyone else, so nothing else catches it.
  const skips = await page.evaluate(() => {
    const levels = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((h) =>
      Number(h.tagName[1]),
    );
    const bad = [];
    for (let i = 1; i < levels.length; i++) {
      if (levels[i] > levels[i - 1] + 1) bad.push(`h${levels[i - 1]} -> h${levels[i]}`);
    }
    return bad;
  });
  record(skips.length === 0, `${path} heading outline skips no level`, skips[0] ?? '');

  // A \u00b7 written in a markup text position is not an escape -- it is six
  // literal characters, and it renders as six literal characters. Three
  // shipped before this check existed.
  const strays = await page.evaluate(() => {
    const text = document.body.innerText;
    return [...text.matchAll(/\\u[0-9a-fA-F]{4}|\\x[0-9a-fA-F]{2}/g)].map((m) => m[0]);
  });
  record(strays.length === 0, `${path} renders no stray escape sequence`, strays.join(' '));

  // Keyboard path. Negative-controlled by suppressing outline and box-shadow
  // site-wide, which flags 31 of 31 controls on /text/ -- so a green result
  // here is a fact about the CSS, not about the check.
  const controls = await page.$$('a[href], button, input, select, [tabindex]:not([tabindex="-1"])');
  const unreachable = [];
  const ringless = [];
  for (const el of controls) {
    if (!(await el.isVisible().catch(() => false))) continue;
    await el.focus().catch(() => {});
    if (!(await el.evaluate((n) => n === document.activeElement))) {
      unreachable.push(await el.evaluate((n) => n.outerHTML.slice(0, 60)));
      continue;
    }
    const lit = await el.evaluate((n) => {
      const f = getComputedStyle(n);
      return (f.outlineStyle !== 'none' && parseFloat(f.outlineWidth) > 0) || f.boxShadow !== 'none';
    });
    if (!lit) ringless.push(await el.evaluate((n) => n.outerHTML.slice(0, 60)));
  }
  record(unreachable.length === 0, `${path} every visible control takes focus`, unreachable[0] ?? '');
  record(ringless.length === 0, `${path} every focused control shows a ring`, ringless[0] ?? '');

  // Tab order must walk the page downward. A control that sends focus back up
  // the document is how a keyboard reader gets trapped in a loop.
  await page.evaluate(() => document.body.focus());
  const tops = [];
  for (let i = 0; i < 40; i += 1) {
    await page.keyboard.press('Tab');
    const top = await page.evaluate(() => {
      const a = document.activeElement;
      if (!a || a === document.body) return null;
      return Math.round(a.getBoundingClientRect().top + window.scrollY);
    });
    if (top === null) break;
    tops.push(top);
  }
  const backJumps = tops.filter((y, i) => i > 0 && y < tops[i - 1] - 40).length;
  record(backJumps === 0, `${path} tab order follows the page downward`, `${backJumps} back-jumps`);

  // Every in-repo link on the page must resolve. A 404 on a research site is
  // not a cosmetic problem; it is a citation that does not go anywhere.
  const hrefs = await page.evaluate(() =>
    [...document.querySelectorAll('a[href]')]
      .map((a) => a.getAttribute('href'))
      .filter((h) => h && h.startsWith('/')),
  );
  const broken = [];
  for (const href of [...new Set(hrefs)]) {
    const r = await page.request.get(`${origin}${href}`);
    if (!r.ok()) broken.push(`${href} -> ${r.status()}`);
  }
  record(broken.length === 0, `${path} every internal link resolves`, broken.join(', ') || `${hrefs.length} links`);

  await context.close();
}

/* --- the two new artifacts ------------------------------------------------
 *
 * The expected numbers below -- 3 cases, 51 axioms, 6 sufficient, 4 step-one,
 * 8 disproved claims, 6 negative controls -- are written out on purpose, and
 * this is NOT the hardcoding that lint-facts.mjs exists to stop.
 *
 * The site reads those numbers from data/facts.json and the theory files. A
 * test that read its expectation from the same place would agree with the page
 * no matter what either said, which is not a test. These are independent
 * assertions, and if one of them ever legitimately changes it should cost a
 * deliberate edit here.
 * ------------------------------------------------------------------------- */

{
  const { context, page } = await open('/precedents/');
  const tabs = page.locator('[data-collapse] [role="tab"]');
  record((await tabs.count()) === 3, 'collapse figure offers all three cases', `${await tabs.count()} tabs`);

  await tabs.nth(1).click();
  const lit = page.locator('[data-collapse] .band--lit');
  const litBand = await lit.getAttribute('data-band');
  record(litBand === '1', 'selecting Austria lights the layer outside the constitution', `band ${litBand}`);

  const blind = await page.locator('[data-collapse] [data-panel="austria"] .blind').isVisible();
  record(blind, 'and says a text-only method would have missed it');

  await tabs.nth(0).click();
  const g = await page.locator('[data-collapse] .band--lit').getAttribute('data-band');
  const seen = await page.locator('[data-collapse] [data-panel="germany"] .seen').isVisible();
  record(g === '0' && seen, 'Germany lights the constitution layer and is the one we would catch');

  await context.close();
}

{
  const { context, page } = await open('/machine/');
  const chips = page.locator('[data-ablation] [data-ax]');
  const total = await chips.count();
  record(total === 51, 'the ablation grid carries every axiom', `${total} axioms`);

  const dropped0 = await page.locator('[data-ablation] .ax--dropped').count();
  record(dropped0 === 0, 'the published model drops nothing', `${dropped0} dropped`);

  await page.locator('[data-ablation] [data-state="six"]').click();
  const kept = total - (await page.locator('[data-ablation] .ax--dropped').count());
  record(kept === 6, 'the six-axiom state keeps exactly six', `${kept} kept`);

  await page.locator('[data-ablation] [data-state="nostepone"]').click();
  const droppedStep = await page.locator('[data-ablation] .ax--dropped').count();
  record(droppedStep === 4, "deleting Godel's step one drops exactly four axioms", `${droppedStep} dropped`);

  const lost = await page.locator('[data-ablation] [data-panel="nostepone"] .lost li').count();
  record(lost === 1, 'and costs exactly one proposition', `${lost} lost`);

  await context.close();
}

{
  const { context, page } = await open('/method/');
  const claims = await page.locator('.claims li').count();
  record(claims === 8, 'the method page lists all eight disproved claims', `${claims} claims`);

  const controls = await page.locator('.controls li').count();
  record(controls === 6, 'and all six negative controls', `${controls} controls`);

  await context.close();
}

/* --- the threshold machine actually moves -------------------------------- */

{
  const { context, page } = await open('/text/');

  const readout = page.locator('[data-chamber="house"] [data-readout]');
  const before = (await readout.textContent())?.trim();

  await page.locator('input[name="base"][value="full"]').check();
  await page.waitForTimeout(50);
  const after = (await readout.textContent())?.trim();

  record(before === '146', 'threshold machine opens on the 1947 law', `House ${before}`);
  record(
    after === '290' && after !== before,
    'threshold machine moves the base to full membership',
    `${before} \u2192 ${after}`,
  );

  const width = await page
    .locator('[data-chamber="house"] [data-fill]')
    .evaluate((el) => el.style.width);
  record(
    width.startsWith('66.6'),
    'the bar redraws to two thirds of the chamber',
    `width ${width}`,
  );

  await context.close();
}

/* --- the silence filter isolates the cluster ----------------------------- */

{
  const { context, page } = await open('/text/');

  const inv = '[data-silence-inventory] tbody tr';
  const all = await page.locator(inv).count();
  record(all === 12, 'the inventory carries every row', `${all} rows`);

  // Count what a reader can actually see, not what carries an attribute. The
  // mobile layout sets `tr { display: block }` in author origin, which beats
  // the UA stylesheet's `[hidden] { display: none }` -- so for a while the
  // filter set the attribute, changed nothing on a phone, and this check
  // passed anyway because it never entered the mobile layout or measured
  // layout at all.
  const countVisible = async (p) => {
    const rows = await p.$$('[data-silence-inventory] tbody tr');
    let n = 0;
    for (const r of rows) if (await r.isVisible()) n += 1;
    return n;
  };

  await page.locator('input[name="holder"][value="single-chamber"]').check();
  await page.waitForTimeout(50);
  const visible = await countVisible(page);
  record(visible === 3, 'filtering to one chamber leaves the three-row cluster', `${visible} rows`);

  await page.locator('input[name="holder"][value="nobody"]').check();
  await page.waitForTimeout(50);
  const unfilled = await countVisible(page);
  record(unfilled === 1, 'exactly one silence has no filler at all', `${unfilled} row`);

  await context.close();
}

/* --- and the same filter has to work on a phone -------------------------- */

{
  const { context, page } = await open('/text/', { viewport: { width: 390, height: 800 } });
  const rows = await page.$$('[data-silence-inventory] tbody tr');
  let n = 0;
  for (const r of rows) if (await r.isVisible()) n += 1;
  record(n === 12, 'at 390px every row starts visible', `${n} rows`);

  await page.locator('input[name="holder"][value="single-chamber"]').check();
  await page.waitForTimeout(80);
  let m = 0;
  for (const r of rows) if (await r.isVisible()) m += 1;
  record(m === 3, 'at 390px filtering still leaves the three-row cluster', `${m} rows`);

  await context.close();
}

/* --- the recension tablist is operable from the keyboard ----------------- */

{
  const { context, page } = await open('/text/');

  await page.locator('[role="tab"]').first().focus();
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(30);

  const selected = await page.locator('[role="tab"][aria-selected="true"]').getAttribute('data-tab');
  record(
    selected === 'seventh-comma',
    'arrow keys move between divergences',
    `selected ${selected}`,
  );

  const shown = await page.locator('[role="tabpanel"]:not([hidden])').count();
  record(shown === 1, 'exactly one divergence panel is shown at a time', `${shown} visible`);

  const focused = await page.evaluate(() => document.activeElement?.getAttribute('data-tab'));
  record(focused === 'seventh-comma', 'focus follows selection', `focus on ${focused}`);

  // Only the selected tab is in the tab order, per the tablist pattern.
  const tabbable = await page.evaluate(
    () => [...document.querySelectorAll('[role="tab"]')].filter((t) => t.tabIndex === 0).length,
  );
  record(tabbable === 1, 'only the selected tab is in the tab order', `${tabbable} tabbable`);

  await context.close();
}

/* --- the whole site works with scripting disabled ------------------------ */

{
  const { context, page } = await open('/text/', { js: false });

  const rows = await page.locator('[data-silence-inventory] tbody tr').count();
  record(rows === 12, 'with JS off, every silence row is still present', `${rows} rows`);

  // `>= 1` is what let two of the three divergences ship unreachable. Every
  // panel of every tabbed island must be readable with scripting off, because
  // the tabs are the only other way to reach them.
  const panels = await page.locator('[role="tabpanel"]').count();
  const openPanels = await page.locator('[role="tabpanel"]:not([hidden])').count();
  const laidOut = await page.$$eval('[role="tabpanel"]', (ns) =>
    ns.filter((n) => getComputedStyle(n).display !== 'none').length);
  record(panels === 3, 'with JS off, /text/ still carries all three divergences', `${panels}`);
  record(laidOut === panels, 'with JS off, every divergence panel is laid out',
    `${laidOut} of ${panels} (hidden attr on ${panels - openPanels})`);

  const fallback = await page.locator('table.no-js-only').first().isVisible();
  record(fallback, 'with JS off, the threshold table replaces the toggle');

  // The whole progressive-enhancement story rests on this media feature
  // reporting the truth. If a browser answered `enabled` with scripting off,
  // every `.needs-js` control would render dead, so the assumption is probed
  // rather than assumed.
  const scripting = await page.evaluate(
    () => matchMedia('(scripting: enabled)').matches,
  );
  record(scripting === false, 'the scripting media feature reports scripting off', `matches=${scripting}`);

  const controls = await page.locator('.needs-js').first().isVisible();
  record(!controls, 'with JS off, dead controls are not shown');

  const words = await page.evaluate(() => document.body.innerText.trim().split(/\s+/).length);
  record(words > 700, 'with JS off, the page is still a full document', `${words} words`);

  await context.close();
}

/* --- reduced motion is honoured completely ------------------------------- */

{
  const context = await browser.newContext({ reducedMotion: 'reduce' });
  const page = await context.newPage();
  await page.goto(`${origin}${BASE}/text/`, { waitUntil: 'networkidle' });

  const duration = await page
    .locator('[data-chamber="house"] [data-fill]')
    .evaluate((el) => getComputedStyle(el).transitionDuration);
  record(
    parseFloat(duration) < 0.05,
    'prefers-reduced-motion removes the transition entirely',
    `duration ${duration}`,
  );

  await context.close();
}

/* ------------------------------------------------------------------ done */

await browser.close();
server.close();

const failed = results.filter((r) => !r.ok);
console.log(
  `\n  ${results.length - failed.length}/${results.length} browser checks passed\n`,
);
process.exit(failed.length ? 1 : 0);
