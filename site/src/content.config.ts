import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

// Starlight routes every file under src/content/docs/. The five sections are
// MECE by construction: each answers a question no other section answers, and
// the sidebar order is the reading order, not an alphabetical accident.
export const collections = {
  docs: defineCollection({ loader: docsLoader(), schema: docsSchema() }),
};
