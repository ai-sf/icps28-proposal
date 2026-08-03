import type { ImageMetadata } from 'astro';

// Every site image, eagerly imported so `<Image>` can consume it by
// category-relative path (e.g. assetImage('brand/firme.png')).
// Images live in src/assets/<category>/<slug> and are optimized at build time
// by astro:assets (AVIF/WebP output, responsive srcset, base-path-safe URLs).
const allImages = import.meta.glob<ImageMetadata>('./assets/**/*.{png,jpg,jpeg,webp,avif}', {
  eager: true,
  import: 'default',
});

export const assetImage = (rel: string): ImageMetadata => {
  const mod = allImages[`./assets/${rel}`];
  if (!mod) throw new Error(`Unknown image asset: ${rel}`);
  return mod;
};
