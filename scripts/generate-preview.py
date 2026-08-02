#!/usr/bin/env python3
"""Generate icps28-proposal-preview.html — a single self-contained, scrollable,
interactive version of the ICPS 2028 Project Proposal.

Content is extracted verbatim from the built Astro site (dist/<chapter>/), the
compiled CSS is inlined with fonts embedded as data URIs, and image paths are
rewritten to relative workspace paths so the file renders when served from the
Design Files workspace root (/home/dario/AISF/icps-pp).

Usage: python3 scripts/generate-preview.py  (run from icps28-website/)
Output: ../icps28-proposal-preview.html
"""
import base64
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # icps28-website
OUT = os.path.join(os.path.dirname(ROOT), 'icps28-proposal-preview.html')
DIST = os.path.join(ROOT, 'dist')

# Order mirrors main.tex / data/site.ts
CHAPTERS = [
    ('introduction', '01', 'Introduction'),
    ('organizing-committee', '02', 'Organizing Committee'),
    ('italy', '03', 'A few words about Italy'),
    ('getting-there', '04', 'How do I get there?'),
    ('food-accomodation', '05', 'Food & Accomodation'),
    ('scientific-program', '06', 'Scientific program'),
    ('social-program', '07', 'Social program'),
    ('transportation', '08', 'Transportation'),
    ('internal-communication', '09', 'Internal communication'),
    ('pr-socials', '10', 'PR & Socials'),
    ('finance', '11', 'Finance'),
    ('sponsorships', '12', 'Sponsorship strategy'),
    ('conclusions', '13', 'Conclusions'),
]

IMG_RE = re.compile(r'src="(/assets/[^"]+)"')
HREF_RE = re.compile(r'href="(/[a-z][a-z0-9-]*/)"')


def asset_rel(path: str) -> str:
    """/assets/x/y.png -> icps28-website/public/assets/x/y.png (from workspace root)."""
    return 'icps28-website/public' + path


def inline_css() -> str:
    css_file = sorted(glob.glob(os.path.join(DIST, '_astro', 'Layout.*.css')))[0]
    css = open(css_file, encoding='utf-8').read()

    def repl(m):
        url = m.group(1)
        # only inline woff2 from _astro (fonts); leave other urls alone
        if url.startswith('/_astro/') and url.endswith('.woff2'):
            fpath = os.path.join(DIST, '_astro', os.path.basename(url))
            if os.path.exists(fpath):
                b64 = base64.b64encode(open(fpath, 'rb').read()).decode()
                return f'url(data:font/woff2;base64,{b64})'
        return m.group(0)

    return re.sub(r'url\(([^)]+)\)', repl, css)


def extract_chapter(cid: str) -> str:
    """Pull <article class="prose">…</article> from the built page.

    The prose article may contain nested <article> elements (e.g.
    PersonCard renders <article class="person">), so a naive non-greedy
    match stops early. Instead we cut from the prose opening tag to
    </main> and drop the trailing prose </article>.
    """
    html = open(os.path.join(DIST, cid, 'index.html'), encoding='utf-8').read()
    start = html.find('<article class="prose">')
    if start == -1:
        return ''
    end = html.find('</main>', start)
    if end == -1:
        end = len(html)
    body = html[start:end]
    # remove the trailing </article> that closes the prose wrapper
    body = body.rsplit('</article>', 1)[0]
    body = IMG_RE.sub(lambda mm: f'src="{asset_rel(mm.group(1))}"', body)
    # internal chapter links → anchor links within the single page
    body = HREF_RE.sub(lambda mm: f'href="#{mm.group(1).strip("/")}"', body)
    return body


def cover_html() -> str:
    idx = open(os.path.join(DIST, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<section class="cover".*?</section>', idx, re.S)
    cover = m.group(0) if m else ''
    cover = IMG_RE.sub(lambda mm: f'src="{asset_rel(mm.group(1))}"', cover)
    return cover


def chapter_lead(cid: str) -> str:
    """Extract the chapter-head lead paragraph (if any) from the built page."""
    html = open(os.path.join(DIST, cid, 'index.html'), encoding='utf-8').read()
    m = re.search(r'<header class="chapter-head">(.*?)</header>', html, re.S)
    if not m:
        return ''
    inner = m.group(1)
    lm = re.search(r'<p class="chapter-head__lead">(.*?)</p>', inner, re.S)
    return lm.group(1) if lm else ''


def build() -> None:
    css = inline_css()
    chapters_html = []
    for cid, num, title in CHAPTERS:
        body = extract_chapter(cid)
        lead = chapter_lead(cid)
        # wrap each chapter in a section with an anchor
        chapters_html.append(
            f'<section class="preview-chapter" id="{cid}" data-od-id="{cid}">'
            f'<header class="chapter-head">'
            f'<p class="chapter-head__kicker">Chapter {num}</p>'
            f'<h1>{title}</h1>'
            + (f'<p class="chapter-head__lead">{lead}</p>' if lead else '')
            + f'</header>'
            f'<div class="prose">{body}</div>'
            f'</section>'
        )
    chapters = '\n'.join(chapters_html)

    toc_items = '\n'.join(
        f'<a class="toc__item" href="#{cid}" data-od-id="toc-{cid}">'
        f'<span class="toc__num">{num}</span><span class="toc__title">{title}</span></a>'
        for cid, num, title in CHAPTERS
    )

    # Sidebar nav (mirrors the site TOC)
    sidebar = '\n'.join(
        f'<a class="sidebar__link" href="#{cid}"><span class="sidebar__num">{num}</span>'
        f'<span>{title}</span></a>'
        for cid, num, title in CHAPTERS
    )

    # Keep the JS outside the f-string to avoid brace-escaping errors.
    script = """
// Mobile drawer + scroll lock (same behaviour as the site)
const burger = document.querySelector('[data-burger]');
const drawer = document.querySelector('[data-drawer]');
if (burger && drawer) {
  const close = () => {
    drawer.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  };
  burger.addEventListener('click', () => {
    drawer.classList.add('is-open');
    burger.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  });
  drawer.querySelectorAll('[data-drawer-close]').forEach((el) => el.addEventListener('click', close));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
}
// Highlight the active chapter in the sidebar on scroll
const sections = Array.from(document.querySelectorAll('.preview-chapter'));
const links = Array.from(document.querySelectorAll('.sidebar__link'));
const syncNav = () => {
  const probe = window.scrollY + window.innerHeight * 0.3;
  let active = null;
  for (const s of sections) {
    if (s.offsetTop <= probe) active = s;
    else break;
  }
  links.forEach((l) => l.removeAttribute('aria-current'));
  if (active) {
    const link = links.find((l) => l.getAttribute('href') === '#' + active.id);
    if (link) link.setAttribute('aria-current', 'page');
  }
};
window.addEventListener('scroll', syncNav, { passive: true });
window.addEventListener('load', syncNav);
syncNav();
"""

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>ICPS 2028 · Italy — Project Proposal</title>
<meta name="description" content="Interactive single-page version of the ICPS 2028 Project Proposal — hosted in Torino and Milano, presented at the IAPS Annual General Meeting 2026." />
<style>
{css}
/* ---- single-page preview additions ---- */
html {{ scroll-behavior: smooth; }}
.preview-chapter {{ padding-top: 2.75rem; }}
.preview-chapter + .preview-chapter {{ border-top: 1px solid var(--border-soft); margin-top: 1rem; }}
.layout--bare {{ grid-template-columns: minmax(0, 1fr); }}
.preview-toc {{ padding-bottom: 3rem; }}
</style>
</head>
<body>
<div class="watermark" aria-hidden="true"></div>

<header class="site-header" data-od-id="site-header">
  <div class="site-header__inner">
    <a class="site-header__logo" href="#top" aria-label="ICPS 2028 home">
      <img src="{asset_rel('/assets/brand/logo-icps28.jpg')}" alt="ICPS 2028 logo" />
      <span class="site-header__wordmark">ICPS 2028<em> · ITALY</em></span>
    </a>
    <span class="site-header__right">Project Proposal</span>
    <button class="site-header__burger" data-burger aria-label="Open menu" aria-expanded="false" aria-controls="drawer">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="layout">
  <nav class="sidebar" aria-label="Table of contents" data-od-id="site-toc">
    <p class="sidebar__label">Table of contents</p>
    <div class="sidebar__list">
      {sidebar}
    </div>
  </nav>

  <main class="main" id="main" data-od-id="main-content">
    <section id="top" class="preview-cover">
      {cover_html()}
    </section>

    <section class="toc preview-toc" data-od-id="table-of-contents">
      <p class="toc__label">Table of contents</p>
      <div class="toc__grid">
        {toc_items}
      </div>
    </section>

    {chapters}
  </main>
</div>

<footer class="site-footer" data-od-id="site-footer">
  <div class="site-footer__inner">
    <span class="site-footer__logo"><img src="{asset_rel('/assets/brand/logo-icps28.jpg')}" alt="ICPS 2028 logo" /></span>
    <span class="site-footer__center">Project Proposal</span>
    <span class="site-footer__right"><b>ICPS 2028</b> · Italy</span>
  </div>
</footer>

<div class="drawer" id="drawer" data-drawer>
  <div class="drawer__backdrop" data-drawer-close></div>
  <div class="drawer__panel">
    <div class="drawer__head">
      <span class="sidebar__label" style="margin:0">Table of contents</span>
      <button class="drawer__close" data-drawer-close aria-label="Close menu">×</button>
    </div>
    <div class="sidebar__list">{sidebar}</div>
  </div>
</div>

<script>{script}</script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'wrote {OUT} ({os.path.getsize(OUT)/1024:.0f} KB)')


if __name__ == '__main__':
    build()
