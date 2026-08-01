# ICPS 2028 website — content & component contract

This document is the single source of truth for fixers building chapter pages.
**Read it fully before writing any page.** All content must be **verbatim** from
the proposal `.tex` files — do not add, remove, rephrase, or "fix" anything.
British spellings and even quirks ("Accomodation", "exploraing") stay as-is.

## 1. Page skeleton (every chapter page)

```astro
---
import Layout from '../layouts/Layout.astro';
import { chapters } from '../data/site';
const ch = chapters.find((c) => c.id === 'introduction')!; // use YOUR chapter id
---
<Layout title={ch.title} description="…" chapter={ch.id}>
  <header class="chapter-head">
    <p class="chapter-head__kicker">Chapter {String(ch.num).padStart(2, '0')}</p>
    <h1>{ch.title}</h1>
    {lead && <p class="chapter-head__lead">{lead}</p>}
  </header>

  <article class="prose">
    <!-- sections -->
  </article>
</Layout>
```

- The chapter lead is the intro paragraph(s) of the chapter (before the first `\section`), shortened only by *splitting*; if long, put the rest as the first prose paragraph.
- Every `\section{...}` → `<section>` with `<h2>` (add `<span class="sec-num">N.</span>` only when the source numbers sections).
- `\subsection*{...}` → `<h3>`. `\paragraph*{...}` / `\subsubsection*{...}` → `<h4>`.
- `\item` lists → `<ul>/<ol><li>`. Inline `\textbf`→`<strong>`, `\textit`→`<em>`.
- `\url{...}` / `\href{url}{label}` → `<a href="url" target="_blank" rel="noopener noreferrer">label</a>`.
- `\ldots` → `…`, `--` → `–`, `---` → `—`, `\&`→`&amp;`, `\%`→`%`, `\\` → paragraph break (or `<br>` inside list items).
- Escape `<`/`>` in HTML. Numbers: keep exact decimal formatting (`1,450.00`).

## 2. Components

| Component | Import | Props | Use for |
|---|---|---|---|
| `Figure` | `../components/Figure.astro` | `src` (relative to `/assets/`, no slash), `alt`, `caption?`, `layout: 'full'\|'inset'`, `imageFirst?`, `wide?` | any image; `inset` = image + text side by side (use the default slot for the text) |
| `Callout` | `../components/Callout.astro` | `variant: 'default'\|'rose'` | quoted asides (e.g. sustainability note), default slot text |
| `DataTable` | `../components/DataTable.astro` | `headers: string[]`, `rows: (string\|number)[][]`, `foot?`, `caption?` | finance, visa, excursion tables |
| `PersonCard` | `../components/PersonCard.astro` | `photo` (name under `/assets/oc/`), `name`, `role?`, `bio` | OC members |
| `SpeakerCard` | `../components/SpeakerCard.astro` | `photo` (under `/assets/speakers/`), `name`, `affiliation?`, `detail?`, `connection?: {label, href?}`, `reverse?` | keynote speakers |
| `Motto` | `../components/Motto.astro` | `text` | "Curiosity takes flight" |

Wrapping utilities (plain HTML + classes from global.css):
- `.team-block` + `.team-block__title` — OC team sections.
- `.keywords` list with `.keywords__term` / `.keywords__def` — the 5 keywords.
- `.logo-row` + `.logo-row__label` + `<img>` — sponsor logo bars.
- `.tag-list` — two-column country lists (visa).
- `.card-grid` + `.card` + `.card__title` / `.card__body` / `.card__meta` — museum/venue cards.
- `.link-table` — contact / social media table.
- `.brandingbox` — white box with CherryRose border (logo description box).
- `.eyebrow` — small caps label. `.grid-2` — two columns.
- `.chip` — small tag/badge; `.chip--rose` variant.

## 3. Image slug manifest (tex source → `/assets/<path>`)

### oc (photos/oc or photos_orig/oc)
`Cante.png→oc/federico-canterucci.png`, `Julia.png→oc/julia-favaro.png`, `Deb.png→oc/debora-marrone.png`, `Valerio.png→oc/valerio-tinari.png`, `Luca.png→oc/luca-attina.png`, `Cla.png→oc/claudia-franco.png`, `Giacomo.png→oc/giacomo-galli.png`, `Cicca.png→oc/roberto-ciccarelli.png`, `Adele.png (orig)→oc/adele-peluso.png`, `Davide.png→oc/davide-perillo.png`, `Tomislav.png (orig)→oc/tomislav-vojvodic.png`, `Francesco.png→oc/francesco-ottone.png`, `Giorgia.png→oc/giorgia-cantore.png`, `Raimondo.png→oc/raimondo-lucariello.png`, `Sara.png→oc/sara-atlante.png`, `Tassa.png→oc/valerio-tassarotti.png`, `Virginia.png→oc/virginia-marchignoli.png`, `Rares.png→oc/rares-drosu.png`, `Mario.png→oc/mario-lisciandrello.png`, `Elisa.png→oc/elisa-sogno.png`, `Marta.png→oc/marta-giacomet.png`, `Dario.png→oc/dario-zarcone.png`, `Alice.png→oc/alice-dautilio.png`, `Claudio.png→oc/claudio-scarasciullo.png`, `Mattia.png→oc/mattia-magaletti.png`, `Lorenzo.png→oc/lorenzo-sabadini.png`, `Alessandro.png→oc/alessandro-lupi.png`, `Mara.png→oc/maria-rosaria-sivo.png`, `gruppo.jpg→oc/gruppo.jpg`

### cities
`image5.png→cities/torino-panorama.png`, `image1.png→cities/torino-piazza.png`, `mole antonelliana.png→cities/mole-antonelliana.png`, `Milano_skyline.jpg→cities/milano-skyline.jpg`, `Castello-Sforzesco.jpg→cities/castello-sforzesco.jpg`, `Navigli.jpg→cities/navigli.jpg`

### accomodation
`Program_A.png→accomodation/program-a.png`, `Program_B.png→accomodation/program-b.png`, `CX_TO_Marconi.png→accomodation/campusx-torino-marconi.png`, `CX_TO_Vanchiglia.png→accomodation/campusx-torino-vanchiglia.png`, `CX_MI_Bicocca.png→accomodation/campusx-milano-bicocca.png`, `Meininger_MI.png→accomodation/meininger-milano.png`, `Olimpia_TO.png→accomodation/olimpia-torino.png`, `Bicocca_Magna.png→accomodation/bicocca-magna.png`, `Shuster_Milano.png→accomodation/casa-shuster.png`, `Palazzo_Nuovo_Torino.png→accomodation/palazzo-nuovo.png`, `Campus_Einaudi_Torino.png→accomodation/campus-einaudi.png`

### food
`Pizza-cropped.png→food/pizza.png`, `Cappuccino-cropped.png→food/cappuccino.png`, `Tiramisu-cropped.png→food/tiramisu.png`, `gorgonzola-cropped.png→food/gorgonzola.png`, `panettone-cropped.png→food/panettone.png`, `bagna cauda-cropped.png→food/bagna-cauda.png`, `bicerin-cropped.png→food/bicerin.png`

### speakers (photos_orig/speaker)
`Gianotti.png→speakers/fabiola-gianotti.png`, `Tonelli.png→speakers/guido-tonelli.png`, `Maiani.png→speakers/luciano-maiani.png`, `Parisi.png→speakers/giorgio-parisi.png`, `Zapperi.png→speakers/stefano-zapperi.png`, `Battiston.png→speakers/federico-battiston.png`, `Ferlaino.png→speakers/francesca-ferlaino.png`, `Amano.png→speakers/hiroshi-amano.png`, `L'Huillier.png→speakers/anne-lhuillier.png`, `Maggiore.png→speakers/michele-maggiore.png`, `Rovelli.png→speakers/carlo-rovelli.png`, `Branchesi.png→speakers/marica-branchesi.png`, `Bisogni.png→speakers/maria-giuseppina-bisogni.png`, `Carrozza.png→speakers/maria-chiara-carrozza.png`, `Rossi.png→speakers/sandro-rossi.png`, `Gianotti2.png→speakers/fosca-giannotti.png`, `Bartoletti.png→speakers/ivana-bartoletti.png`, `Fabris.png→speakers/adriano-fabris.png`, `Broccoli.png→speakers/bobbybroccoli.png`, `Battiston2.png→speakers/roberto-battiston.png`, `Ferrero.png→speakers/andrea-ferrero.png`, `Scarpetta.png→speakers/ersilia-vaudo-scarpetta.png`, `Cristoforetti.png→speakers/samanta-cristoforetti.png`, `Parmitano.png→speakers/luca-parmitano.png`

### lab
`square-venaria.jpg→lab/venaria-reale.jpg`, `square-inrim.jpg→lab/inrim.jpg`, `square-marioboella.jpg→lab/links-mario-boella.jpg`, `square-polito.jpg→lab/politecnico-torino.jpg`, `square-merate.jpg→lab/merate-observatory.jpg`, `square-ifom.png→lab/ifom.jpg`, `square-lasa.jpg→lab/lasa.jpg`, `square-milanobicocca.jpg→lab/milano-bicocca.jpg`

### social (programma sociale)
`Ca_Granda.jpg→social/ca-granda.jpg`, `Genova.jpg→social/genova.jpg`, `5Terre.jpg→social/cinque-terre.jpg`, `Lago.jpg→social/lake-como.jpg`, `Resinelli.jpg→social/pian-dei-resinelli.jpg`, `Canzo.jpg→social/canzo.jpg`, `Leonardo.jpg→social/leonardo.jpg`, `Nations1.png→social/nations-1.png`, `Nations2.png→social/nations-2.png`, `Nations3.png→social/nations-3.png`, `Alice_in_Turinland.png→social/alice-in-turinland.png`, `Museo_Egizio1.jpg→social/museo-egizio-1.jpg`, `Museo_Egizio2.jpg→social/museo-egizio-2.jpg`, `Torino_Notturna.jpg→social/torino-notturna.jpg`, `Gran_Madre.jpg→social/gran-madre.jpg`, `Villa_Regina.jpg→social/villa-regina.jpg`, `Duomo_Milano.jpg→social/duomo-milano.jpg`, `Museo_Torino.jpg→social/museo-torino.jpg`

### pr
`palette.jpg→pr/palette.jpg`, `BW.png→pr/logo-bw.png`, `BW tot .jpg→pr/banner-bw.jpg`, `colored tot.jpg→pr/banner-colored.jpg`, `yellow left.jpg→pr/wing-warm-left.jpg`, `blue right.jpg→pr/wing-blue-right.jpg`

### sponsors
`IAPS.jpg→sponsors/iaps.jpg`, `IUPAP.png→sponsors/iupap.png`, `EPS.png→sponsors/eps.png`, `UNITO.png→sponsors/unito.png`, `UNIMI.png→sponsors/unimi.png`, `UNI_BICOCCA.png→sponsors/unimib.png`, `INFN.jpg→sponsors/infn.jpg`, `inrim.jpg→sponsors/inrim.jpg`, `POLIMI.png→sponsors/polimi.png`, `POLITO.png→sponsors/polito.png`, `Intesa_Sanpaolo.png→sponsors/intesa-sanpaolo.png`

### brand
`AISF_LOGO_BG.png→brand/aisf-logo-bg.png`, `logo_icps28.jpg→brand/logo-icps28.jpg`, `filigrana.jpg→brand/filigrana.jpg`, `Firme.png→brand/firme.png`

## 4. Design rules (do not break)

- Fonts: display contexts (`--font-display`) use the bundled **SEGO** face at weight 400 (single-weight font — do not set heavier weights; use `font-synthesis-weight: none`). Archivo covers glyphs SEGO lacks. Keep body text in Georgia / Source Serif 4.
- No new CSS files. Use existing classes/components only.
- No `<style>` blocks in pages. No inline `style=` unless the component contract shows one.
- Accent (`--accent`, blue) appears max 2× per screen: it's used for the kicker + links. Keep links as `<a>` only.
- Every `<img>` must have `alt`. `loading="lazy"` is already in components.
- Keep the verbatim text EXACTLY; if a paragraph is very long, you may split it into multiple `<p>` — never reword.
- `\LaTeX` renders as "LaTeX". Math `\(2 \pm 1\)` → `2 ± 1` (plain text is fine).
