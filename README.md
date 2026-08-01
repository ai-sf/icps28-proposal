# ICPS 2028 — Project Proposal website

An interactive, static website version of the **ICPS 2028 Project Proposal** by
the Italian Association of Physics Students (AISF), built with
[Astro](https://astro.build/) and ready to deploy on **GitHub Pages**.

Everything on the site — text, figures, tables, and images — comes **verbatim**
from the LaTeX proposal in `../ICPS28_Project_Proposal/`. No external content
was added. The visual identity follows the proposal's own design system
(`config.tex` official palette + the PR chapter's branding rules).

## Contents

The site mirrors the document structure, chapter by chapter:

01. Introduction
02. Organizing Committee
03. A few words about Italy
04. How do I get there?
05. Food & Accomodation
06. Scientific program
07. Social program
08. Transportation
09. Internal communication
10. PR & Socials
11. Finance
12. Sponsorship strategy
13. Conclusions

plus a cover page reproducing the frontespizio (logo, motto
*"Curiosity takes flight"*, ICPS 2028 wordmark) with a table of contents.

## Design system

- **Palette** (verbatim from `config.tex`): PaleOak `#E2D1B7`, DarkCoffee
  `#382514`, BrightBalticBlue `#0060A6`, CarbonBlack `#242424`, CherryRose
  `#991E3B`. Derived tints use `oklch()`.
- **Type**: display headings use Archivo (geometric grotesque, standing in for
  the proposal's SEGO font, which is not redistributable); body text uses
  Georgia with Source Serif 4 Variable as the bundled web fallback.
- **Layout**: filigrana watermark background, PaleOak header rule, CherryRose
  footer rule — mirroring the compiled PDF's `fancyhdr` chrome.

## Develop

```bash
npm install
npm run dev       # local dev server
npm run build     # astro check + astro build → dist/
npm run preview   # serve the built site locally
```

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository (branch `main`).
2. Repo **Settings → Pages → Source: GitHub Actions**.
3. The included workflow (`.github/workflows/deploy.yml`) builds the site and
   publishes it automatically on every push to `main`.

The workflow sets `BASE_PATH=/<repo>/`, so the site works at
`https://<user>.github.io/<repo>/` without changes. For a user/org page
(`https://<user>.github.io/`) or a custom domain, set `SITE` and omit
`BASE_PATH` in the workflow.

## Project structure

```
src/
  pages/           one page per chapter + index (cover)
  components/      Figure, DataTable, PersonCard, SpeakerCard, Callout, Motto…
  layouts/         Layout.astro (header, sidebar, footer, watermark, drawer)
  data/site.ts     chapter registry
  styles/global.css  design-system tokens + all styling
  COMPONENTS.md    component + content contract (for contributors)
public/assets/     proposal images, copied verbatim by scripts/copy-assets.sh
scripts/copy-assets.sh  copies referenced images from ../ICPS28_Project_Proposal
```
