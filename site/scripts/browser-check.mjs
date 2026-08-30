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

async function open(path, { js = true } = {}) {
  const context = await browser.newContext({ javaScriptEnabled: js });
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

for (const path of ['/', '/text/']) {
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

  await page.locator('input[name="holder"][value="single-chamber"]').check();
  await page.waitForTimeout(50);
  const visible = await page.locator(`${inv}:not([hidden])`).count();
  record(visible === 3, 'filtering to one chamber leaves the three-row cluster', `${visible} rows`);

  await page.locator('input[name="holder"][value="nobody"]').check();
  await page.waitForTimeout(50);
  const unfilled = await page.locator(`${inv}:not([hidden])`).count();
  record(unfilled === 1, 'exactly one silence has no filler at all', `${unfilled} row`);

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

  const panels = await page.locator('[role="tabpanel"]:not([hidden])').count();
  record(panels >= 1, 'with JS off, at least one divergence is readable', `${panels} panels`);

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
