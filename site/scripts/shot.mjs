/**
 * Screenshot helper for design iteration. Not a test -- nothing here asserts.
 *
 *   npm run dev            # or npm run preview, in another shell
 *   node scripts/shot.mjs / /text/ /machine/
 *
 * Writes a viewport shot and a full-page shot per path to /tmp/gl-*.png at 2x.
 * The 2x scale factor is why a shot looks twice the size of the layout it
 * represents; measure with getBoundingClientRect, not with a screenshot.
 *
 * Points at `localhost` rather than `127.0.0.1` deliberately: astro preview
 * binds IPv6-only here, so the numeric loopback refuses the connection.
 */
import { chromium } from 'playwright';

const BASE = 'http://localhost:4321/godel-loopholes';
const pages = process.argv.slice(2);
const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
  deviceScaleFactor: 2,
});

for (const p of pages) {
  const page = await ctx.newPage();
  await page.goto(`${BASE}${p}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);
  const name = p.replace(/\//g, '') || 'index';
  await page.screenshot({ path: `/tmp/gl-${name}.png`, fullPage: false });
  await page.screenshot({ path: `/tmp/gl-${name}-full.png`, fullPage: true });
  console.log(`shot ${p} -> /tmp/gl-${name}.png`);
  await page.close();
}

await browser.close();
