# AGENTS.md

Agent guide for the ICPS 2028 proposal website — Astro 7 static site, GitHub Pages.

## Context

Multi-page static site transcribing the **ICPS 2028 Project Proposal** (AISF)
**verbatim** from `../ICPS28_Project_Proposal/` (LaTeX source). It has a cover
page plus 13 chapter pages, mirroring the document chapter by chapter.

Read `README.md` (structure/deploy) and `src/COMPONENTS.md` (content +
component contract) before editing pages.

## Non-negotiables

- **Content is verbatim.** Never reword, rephrase, or "fix" the transcription —
  including quirks such as "Accomodation" and British spellings. You may split
  an over-long paragraph into multiple `<p>`, but never rewrite text.
- **Chapter metadata lives in `src/data/site.ts`** (`num`, `id`, `title`,
  `description`, `lead?`). Pages must stay body-only: `<Layout chapter="id">`
  plus `<ChapterHead chapter="id" />`. Do not reintroduce per-page
  `description`/`lead` props or `chapters.find(...)` lookups.
- **No Content Collections / MDX.** Deliberate decision (see git history):
  chapter bodies stay in `.astro` pages because they are component-rich
  (SpeakerCard, Figure, DataTable…) and must remain byte-faithful.
- **Images go through `astro:assets`.** Use `assetImage('path')` from
  `src/images.ts` with `<Image>` — never a raw `<img>`, never `/assets/…`
  URLs. Images live in `src/assets/<category>/<slug>`. Every `<Image>` needs
  `alt`; small fixed-size avatars get an explicit `width`.
- **One global stylesheet.** `src/styles/global.css` is the only CSS file. No
  `<style>` blocks in pages, no new CSS files, no inline `style=` unless the
  component contract shows one.
- **No client JS.** This is a static site; the only script is the mobile
  drawer in `src/layouts/Layout.astro`. No `client:*` directives, no islands.
- **Stable element ids.** Repeated components emit `data-od-id` (slugs via
  `src/ids.ts`): `speaker-…`, `person-…`, `figure-…`, `data-table-…`,
  `round-speaker-…`, `logo-row-…`. Keep them stable and unique — review
  tooling targets elements by these ids.

## Layout

- `src/layouts/Layout.astro` — global chrome: header, sidebar TOC, chapter
  pager, footer, mobile drawer, watermark, meta/OG. Title and description are
  derived from `site.ts` through the `chapter` prop.
- `src/components/` — Figure, DataTable, SpeakerCard, PersonCard, ChapterHead,
  Callout, Motto (contract in `COMPONENTS.md`).
- `src/pages/` — one `.astro` file per chapter plus the cover `index.astro`;
  bodies only.
- `src/assets/` — proposal images, optimized at build time by `astro:assets`.
- `src/fonts/SEGO.woff2` — the SEGO display typeface (single weight, 400).
- `public/` — static files copied as-is (`robots.txt`).

## Commands

```bash
npm run dev       # dev server on http://localhost:4321 (keep running for reviews)
npm run check     # astro check — must be 0 errors before committing
npm run build     # astro check + build → dist/
npm run preview   # serve the built site
```

## Review loop (Open Design)

Reviews happen in the browser against the dev server; elements are addressable
by `data-od-id` (e.g. `/finance/`, `data-table-…`). A burst of `/_image`
requests in dev is normal (astro:assets on-demand optimization); production
serves static `/_astro/` files.

## Git

- Repo root is this folder; branch `main`, remote `origin`
  (`github.com/ai-sf/icps28-proposal.git`).
- Short imperative commit messages. Build must pass before pushing: the Pages
  workflow in `.github/workflows/deploy.yml` deploys every push to `main`.
