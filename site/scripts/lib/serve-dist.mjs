/**
 * Serve dist/ over HTTP on an ephemeral port, for the browser harnesses.
 *
 * Extracted so that every harness tests the same conditions. Two harnesses with
 * two hand-rolled servers is two chances to differ in a way that matters --
 * the security headers in particular, which are deliberately absent here so the
 * page is tested under the policy it carries in its own markup and not one a
 * test server helpfully supplied.
 *
 * Over HTTP rather than file:// because a `file://` origin does not enforce a
 * meta CSP the way an `http://` one does, and testing under the wrong
 * conditions is worse than not testing.
 *
 * Binds 127.0.0.1 explicitly. `astro preview` binds IPv6-only on this machine,
 * so a harness that assumed localhost resolved the same way for both would
 * intermittently fail to connect.
 */

import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const BASE = '/godel-loopholes';

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.woff2': 'font/woff2',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
};

/**
 * @returns {Promise<{ origin: string, base: string, close: () => Promise<void> }>}
 */
export async function serveDist() {
  const siteRoot = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
  const dist = join(siteRoot, 'dist');

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

  return {
    origin: `http://127.0.0.1:${server.address().port}`,
    base: BASE,
    close: () => new Promise((r) => server.close(r)),
  };
}
