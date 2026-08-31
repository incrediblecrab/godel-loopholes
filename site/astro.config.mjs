// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// The site fetches no third-party origin, at build time or in the browser, so
// the policy can start from `none` and name only what actually ships.
//
// No `frame-ancestors`: the browser ignores it when it arrives in a meta
// element and logs a console warning saying so on every page load, and a
// directive that does nothing except generate a warning teaches readers of the
// console to ignore warnings. `wasm-unsafe-eval` is present because Starlight's
// search is Pagefind, which is WebAssembly -- it is still same-origin and still
// no weaker than 'self' for script.
const CSP = [
  "default-src 'none'",
  "script-src 'self' 'wasm-unsafe-eval'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' data:",
  "font-src 'self'",
  "connect-src 'self'",
  "form-action 'none'",
  "base-uri 'none'",
].join('; ');

// The site is served from a GitHub Pages project page, so every asset and link
// sits under /godel-loopholes/. Getting this wrong produces a site that works
// perfectly in `astro dev` and is entirely broken once deployed, which is the
// single most common way a Pages project site fails.
export default defineConfig({
  site: 'https://incrediblecrab.github.io',
  base: '/godel-loopholes',
  trailingSlash: 'ignore',
  output: 'static',

  integrations: [
    starlight({
      title: "Gödel's Loophole",
      description:
        'Does the Constitution of December 5, 1947 permit its own lawful end? A machine-checked search, and an honest account of not having found one.',

      // Starlight bundles MDX, so no separate @astrojs/mdx entry is needed or
      // wanted: registering it twice makes the integration order significant
      // for no benefit.
      customCss: [
        './src/styles/fonts.css',
        './src/styles/tokens.css',
        './src/styles/pages.css',
        './src/styles/starlight.css',
      ],

      // Starlight owns <head>, so the security headers the old hand-written
      // layout injected are declared here instead. scripts/seal-csp.mjs then
      // pins script-src to the SHA-256 of every inline script that actually
      // shipped, and fails the build if one is not covered.
      head: [
        {
          tag: 'meta',
          attrs: { 'http-equiv': 'Content-Security-Policy', content: CSP },
        },
        { tag: 'meta', attrs: { name: 'referrer', content: 'no-referrer' } },
        { tag: 'meta', attrs: { name: 'color-scheme', content: 'light dark' } },
      ],

      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/incrediblecrab/godel-loopholes',
        },
      ],

      // The reading order is the argument: a claim, why it is not absurd, what
      // reading the words found, what formalising it found, and only then the
      // reasons to believe any of it. Alphabetical order would destroy that.
      sidebar: [
        { label: 'The claim', link: '/' },
        { label: 'The precedents', link: '/precedents/' },
        { label: 'The text', link: '/text/' },
        { label: 'The machine', link: '/machine/' },
        { label: 'The method', link: '/method/' },
      ],

      editLink: {
        baseUrl: 'https://github.com/incrediblecrab/godel-loopholes/edit/main/site/',
      },

      lastUpdated: true,

      // No third-party origin, at build time or in the browser. Starlight's
      // default search is Pagefind, which is built locally and served from the
      // same origin, so it does not break that property.
      pagefind: true,
    }),
  ],

  build: {
    inlineStylesheets: 'auto',
    format: 'directory',
  },
  compressHTML: true,
  devToolbar: { enabled: false },
  vite: {
    build: {
      cssCodeSplit: false,
    },
  },
});
