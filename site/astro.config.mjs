// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';

// The site is served from a GitHub Pages project page, so every asset and link
// sits under /godel-loopholes/. Getting this wrong produces a site that works
// perfectly in `astro dev` and is entirely broken once deployed, which is the
// single most common way a Pages project site fails.
export default defineConfig({
  site: 'https://incrediblecrab.github.io',
  base: '/godel-loopholes',
  trailingSlash: 'ignore',
  output: 'static',
  // Prose is authored as MDX, not typed into .astro templates. The rule this
  // enforces is the project's own: narrative is authored per audience, but it
  // is authored exactly once. Prose living inside HTML tags is how the Article
  // V paragraph ended up stating its own quotation twice, and how a number on
  // the page drifts from data/facts.json without anything failing.
  integrations: [mdx()],
  build: {
    // One stylesheet rather than a per-page cascade of small ones. The whole
    // design system is about forty custom properties; splitting it costs more
    // in requests than it saves in bytes.
    inlineStylesheets: 'auto',
    format: 'directory',
  },
  compressHTML: true,
  devToolbar: { enabled: false },
  vite: {
    build: {
      // No vendor chunk splitting: the islands are small and independent, and a
      // shared chunk would be downloaded by pages that use none of it.
      cssCodeSplit: false,
    },
  },
});
