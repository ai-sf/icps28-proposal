# ICPS 2028 Website — Refactor Plan

> **Status: EXECUTED** (2026-08-03). A1 (metadata centralization), B (astro:assets
> image pipeline), and C (og/twitter + sitemap + robots) are all implemented and
> verified (`astro check` 0 errors, `npm run build` 14 pages, base-path build
> verified). `scripts/copy-assets.sh` and `scripts/generate-preview.py` removed
> as obsolete utilities. This file is kept as the design record; nothing here
> needs action.

> Working plan for the remaining Astro best-practice modifications.
> Source of truth for the next implementation run. Edit freely; every open
> decision is marked `[TODO]`.

## 1. Intent

Bring `icps28-website` (Astro 7.1.6, static, GitHub Pages) in line with current
Astro conventions for a content-heavy chapter site, without breaking the core
property the site is built around: **content is a verbatim transcription of the
LaTeX proposal** (`../ICPS28_Project_Proposal/`).

Two deferred items from the review are planned here: **(A) content/data
modeling** and **(B) the image pipeline**. A third low-effort item, **(C) SEO
completeness**, is included because the canonical/site plumbing was already fixed.

### Already done (previous session — do not redo)
- Watermark `url('/assets/...')` bug → BASE_URL-aware inline style (`Layout.astro`).
- `ChapterHead.astro` component; 13 chapter pages de-duplicated onto it.
- Absolute canonical via `new URL(Astro.url.pathname, Astro.site)` + `SITE` env in `deploy.yml`.
- `DataTable` inline caption style → `.data-caption` class; README deploy section updated.
- Verified: `npm run build` passes (14 pages, `astro check` clean).

## 2. Goals / Non-goals

**Goals**
- Single source of truth for chapter metadata (title, number, id, lead, description).
- Optimized, CLS-free images that work under any `base` path.
- Correct meta/social output now that `site` is real.
- Zero behavior change to rendered content.

**Non-goals**
- No redesign, no copy changes, no new content.
- No client-side framework / islands (site stays zero-JS).
- No server rendering, actions, or middleware (static GH Pages only).

## 3. Modification A — Content modeling (decision point)

### 3.1 Phase A1 (recommended): centralize chapter metadata
Today the 13 pages still repeat per-chapter data: each has
`const ch = chapters.find(...)!`, a `description` prop on `<Layout>`, and a
`lead` (const or inline prop). Only `num/id/title` live in `src/data/site.ts`.

- Extend the `Chapter` interface in `src/data/site.ts` with `description: string`
  and `lead?: string` for all 13 chapters.
- `Layout` derives its `description` default from `chapters` when the page omits it.
- `ChapterHead` already takes `chapter` + `lead`; pages pass `lead` only where the
  chapter has one (7 of 13), and drop their inline `const lead = ...` definitions.
- Result: `site.ts` becomes the single metadata source; pages become body-only.

**Verdict:** cheap (1 file + ~13 small edits), zero risk to verbatim content,
kills the remaining duplication. Recommended regardless of A2.

### 3.2 Phase A2 (decision): full Content Layer + MDX migration
The "textbook" Astro answer is a content collection
(`src/content.config.ts` with `glob()` loader, Zod schema, `[slug].astro` route,
`render()`). For this site it requires `@astrojs/mdx` and transcribing each
chapter body into MDX — but the bodies are **component-rich** (SpeakerCard,
Figure, DataTable, Callout, Motto, PersonCard embedded in prose) and must remain
byte-faithful to the LaTeX source.

- **Option A — full MDX migration:** 13 MDX files in `src/content/chapters/`,
  each importing the components it needs; `[slug].astro` renders via `render()`.
  Most idiomatic; largest effort (~13 transcriptions + route + schema) and the
  only option that can silently alter whitespace/punctuation vs the verbatim
  guarantee.
- **Option B — metadata-only collection:** keep `.astro` bodies, load chapter
  metadata through a `glob()` collection (`src/content/chapters/*.yaml`) with a
  Zod schema; `[slug].astro` still uses `getStaticPaths()`. Adds schema
  validation over A1 but is otherwise equivalent work to A1 with more machinery.
- **Option C — skip:** accept A1 as the end state; document in `COMPONENTS.md`
  that bodies stay in `.astro` by design.

**Verdict:** A2-A is high effort / low ROI for a one-shot proposal site and
jeopardizes the verbatim property. **Recommend A1 + C** unless the site is
expected to grow into a long-lived content platform.

## 4. Modification B — Image pipeline (`astro:assets`)

Current: all images live in `public/assets/` (copied verbatim by
`scripts/copy-assets.sh`), referenced by 33 plain `<img>` tags via the
`asset()` helper. No optimization, no dimensions → CLS risk; several source
files are large (up to ~2 MB).

- Move the copy target from `public/assets` to `src/assets` in
  `scripts/copy-assets.sh` (`DEST` var), and remove `public/assets` from the repo.
- Replace `<img>` with `import { Image } from 'astro:assets'` in:
  - `src/components/Figure.astro` (3 usages — full/inset layouts)
  - `src/components/SpeakerCard.astro`, `PersonCard.astro` (portraits)
  - `src/layouts/Layout.astro` (header + footer logo; watermark background via an
    imported image's `src` instead of `asset()`)
  - `src/pages/scientific-program.astro` (9 roundtable photos),
    `sponsorships.astro` (11 sponsor logos), `index.astro` (cover logos)
- `Figure` keeps a string `src` prop but resolves it via a static `import`
  map per category (or the pages pass imported images); decide in implementation.
- `Image` infers intrinsic width/height (CLS fix); keep `loading="lazy"` on
  below-the-fold images; `quality`/`format` defaults are fine (AVIF/WebP emitted).
- The `asset()` helper in `src/utils.ts` becomes obsolete for templates; keep it
  only if still needed (e.g., favicon/link refs in `Layout`). `[TODO: decide
  favicon handling — keep `logo-icps28.jpg` in `public/` for the `<link rel=icon>`,
  or import it too]`.
- Confirm the default image service (sharp) resolves in this install; add
  `sharp` as a dependency if `astro check`/build warns.

**Benefit:** AVIF/WebP + resize (big win on the 1–2 MB PNGs), CLS elimination,
base-path-safe hashed URLs, cache busting.

## 5. Modification C — SEO / meta completeness (low effort)

- Add `og:image` + `twitter:card` (`summary_large_image`) to `Layout.astro`
  using a shared cover asset (e.g., `logo-icps28.jpg` or a banner) — absolute URL
  via `new URL(...)` against `Astro.site`.
- Add `@astrojs/sitemap` integration (`sitemap.xml`; site is now set in CI).
  `[TODO: confirm desired — a one-shot proposal site may not need it]`.
- `public/robots.txt` (`User-agent: * / Allow: /`).
- Optionally pin `trailingSlash` / `build.format` explicitly in `astro.config.mjs`
  to match GH Pages output.

## 6. Optional polish (P2 — skip unless wanted)

- `<ClientRouter />` from `astro:transitions` in `Layout` + `prefetch` config for
  snappy chapter-to-chapter navigation on a 14-page site. Requires testing the
  drawer script + scroll restoration under view transitions.
- Not recommended: RSS, pagination, i18n — out of scope for a proposal site.

## 7. File-by-file change map

| File | Change | Effort | Risk |
|---|---|---|---|
| `src/data/site.ts` | add `description`, `lead?` per chapter | S | L |
| 13 × `src/pages/*.astro` | drop per-page `lead` consts / inline props; body-only (A1) | S each | L |
| `src/content.config.ts` + `src/content/chapters/*` | only if A2 chosen | L | M |
| `src/components/ChapterHead.astro` | unchanged (already props-driven) | – | – |
| `src/components/Figure.astro`, `SpeakerCard.astro`, `PersonCard.astro` | `<Image>` swap + import map | M | M |
| `src/layouts/Layout.astro` | `<Image>`, og/twitter meta, watermark via imported image | M | M |
| `src/pages/scientific-program.astro`, `sponsorships.astro`, `index.astro` | `<Image>` swap | M | M |
| `scripts/copy-assets.sh` | `DEST` → `src/assets` | S | L |
| `public/assets/*` → `src/assets/*` | move + delete from public | S (git mv) | L |
| `src/utils.ts` | drop or trim `asset()` helper | S | L |
| `astro.config.mjs` | sitemap integration (C); explicit trailingSlash | S | L |
| `package.json` | add `@astrojs/sitemap` (and `sharp` if needed) | S | L |
| `src/COMPONENTS.md`, `README.md` | document new data/asset contracts | S | L |

## 8. Acceptance checks

1. `npm run check` → 0 errors.
2. `npm run build` → 14 pages, no warnings; compare `dist` size before/after
   (images should shrink substantially).
3. Build once with `BASE_PATH=/icps28-website/ SITE=https://example.github.io`
   and confirm: watermark renders, all `<img src>`/`<Image>` URLs are
   base-prefixed, canonicals + og:image are absolute. No `/assets/...` root
   refs in emitted HTML/CSS.
4. Spot-diff 2 chapters (e.g., `transportation`, `scientific-program`) rendered
   HTML against pre-refactor output — text must be identical.
5. Mobile pass: no horizontal scroll at 360/390/430 px (image widths honor
   `max-width: 100%` with intrinsic dims).

## 9. Open questions / TODOs

- [ ] **A2 decision:** full MDX migration, metadata-only collection, or A1-only (recommended)?
- [ ] Keep `src/data/site.ts` (typed, works) vs a metadata content collection?
- [ ] Favicon: keep in `public/` or import via `astro:assets`?
- [ ] Sitemap + og/twitter meta worth it for a one-shot proposal? (default: og/twitter yes, sitemap yes-if-cheap)
- [ ] P2 view transitions in or out?

## 10. Next step

Review and edit this document — especially section 9 — then approve. On
approval, the implementation run executes **A1 → B → C** in that order
(sequential, each verified with `npm run check` + `npm run build` before the
next), and reports the diff summary + acceptance-check results.
