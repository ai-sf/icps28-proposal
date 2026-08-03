import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// GitHub Pages project sites live at https://<user>.github.io/<repo>/ .
// Set BASE_PATH=/<repo>/ in the CI workflow (see .github/workflows/deploy.yml),
// or set SITE to your custom domain. Defaults to root for user/org pages.
export default defineConfig({
  output: 'static',
  site: process.env.SITE ?? 'https://example.github.io',
  base: process.env.BASE_PATH ?? '/',
  integrations: [sitemap()],
});
