# Atlas Blogger Theme Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the approved mockup `mockup/home-v2.html` into a single, fast, bilingual (FR/AR, RTL) Blogger theme `theme.xml` that a small-business owner edits only through Blogger's Layout, Theme Designer and Posts.

**Architecture:** One XML file. CSS lives in `<b:skin>` (colour `Variable`s), markup per widget lives in `b:includable`s, one inline JS block at the end of `<body>` plus a tiny `<head>` language script. Projects are Blogger posts rendered server-side by the `Blog` widget; owner content lives in `Image`, `LinkList` and `HTML` widgets. Two stdlib-only test tools guard the file: a static checker (Python) and a JS unit runner (Node) that extracts the inline script.

**Tech Stack:** Blogger XML theme (layouts v3, widget v2), vanilla CSS/JS, Google Fonts (IBM Plex Sans Arabic). Tooling: Python 3 stdlib, Node 26 stdlib (`node:test`), `xmllint`.

**Spec:** `docs/superpowers/specs/2026-11-04-atlas-blogger-theme-design.md`

## Global Constraints

- One file `theme.xml`; `<html>` carries `b:css='false' b:js='false' b:layoutsVersion='3' b:defaultwidgetversion='2'` and `xmlns:b`, `xmlns:data`, `xmlns:expr`.
- No `<script src=…>` at all; the only external stylesheet is Google Fonts `IBM+Plex+Sans+Arabic:wght@400;500;600;700&display=swap` with `preconnect`.
- No emoji anywhere (theme, demo, README). Icons are SVG `<symbol>`s defined once.
- Short copy: one line per item.
- Inline end-of-body JS ≤ 9216 bytes (excluding the `<head>` language script).
- Bilingual hide rule, verbatim: `html[lang=fr] [lang=ar], html[lang=ar] [lang=fr]{display:none}`.
- Owner short text format: `Texte FR | النص بالعربية` split on ` | `; no `|` → shown as is.
- Default language: `data:blog.locale` starting with `ar` → `ar`, else `fr`; visitor choice in `localStorage` key `atlas-lang`.
- Every image from template data (`data:post.featuredImage`, Image widget `data:sourceUrl`) through `resizeImage`/`sourceSrcset`, with `width`/`height`; first hero image `fetchpriority="high"`, all others `loading="lazy"`.
- `prefers-reduced-motion: reduce` stops animations and autoplay.
- No horizontal scroll at 375px.
- One label per project post = its category.
- Colour variables (Theme Designer): `bg #f7f5f1`, `ink #151716`, `accent #1f5f4a`, `accent2 #c8a96a`. Font is fixed.
- Footer credit: `Thème par MuhDroid` / `قالب من MuhDroid` → `https://muhdroid.com`.
- Demo is the fictional « Atlas Rénovation / أطلس للترميم »; no real client name, photo or site.
- Commits: no attribution lines (user rule). Run the checker + JS tests, not a full suite loop.

## Review Focus

1. A post title with no ` | ` must render once, unchanged, in both languages (no empty half).
2. A post with no `<div lang>` blocks and no image must render its body in both languages and a neutral placeholder card, no broken `<img>`.
3. The contact LinkList with a missing `whatsapp` item: buttons fall back to `#contact`, JSON-LD still valid (no empty `telephone` key).
4. RTL: carousel arrows, testimonial dots and before/after handle move the right way (scroll sign flips under `dir=rtl`; the before/after widget stays `direction:ltr`).
5. Hero with only one Image widget: no dots, no autoplay timer, no JS error.

Each item is pinned by a test in the owning task (Tasks 2, 3, 4, 6).

---

## File Structure

```
theme.xml                 the theme (only shipped file)
tools/check_theme.py      static checks; one function per rule; exit 1 on failure
tools/test_js.mjs         extracts <script id="atlas-head"> and <script id="atlas-js"> from theme.xml, runs node:test on their pure functions
demo/widgets.md           the exact value to paste in each widget of the demo blog
demo/posts/*.html         six demo project posts (HTML view of the Blogger editor)
README.md, LICENSE        per the global README rule (FR + AR), MIT
```

Each inline script exposes its pure functions for tests without a module system: it ends with
`if (typeof module !== 'undefined') module.exports = { splitBi, waUrl, scrollSign, nextIndex };`.
`test_js.mjs` evaluates the script text with a fake `module` and no DOM; every DOM call sits inside `init()`, which only runs when `typeof document !== 'undefined'`.

---

### Task 1: Skeleton, checker, Blogger checkpoint

**Files:**
- Create: `theme.xml`, `tools/check_theme.py`, `tools/test_js.mjs`, `.gitignore` (`.superpowers/`)

**Interfaces:**
- Produces: sections (ids, in order) `header`, `hero`, `marquee`, `services`, `beforeafter`, `main`, `numbers`, `reviews`, `team`, `contact`; a top-level includable `icons` holding every `<symbol>` (ids `i-chat i-arrow i-left i-right i-lr i-home i-paint i-tile i-drop i-bolt i-shield i-phone i-pin i-clock i-star i-globe`); `<script id="atlas-js">` with `function init()` and the export line; checker CLI `python3 tools/check_theme.py theme.xml`; JS tests `node --test tools/test_js.mjs`.

- [ ] **Step 1: Write the checker with these rules, each a function returning a list of errors**
  `well_formed` (stdlib `xml.etree` parse), `html_attrs` (the four `b:` attributes above), `no_emoji` (no char in `U+1F000–U+1FAFF`, `U+2600–U+27BF`), `external_refs` (every `src=`/`href=` to `http` outside `fonts.googleapis.com`, `fonts.gstatic.com`, `blogger.googleusercontent.com`, `*.bp.blogspot.com`, `muhdroid.com`, `wa.me`, `www.google.com/maps` fails; `<script src=` always fails), `symbol_ids_unique`, `js_budget` (text of `#atlas-js` ≤ 9216 bytes), `sections_present` (the ten ids, in order), `bi_rule` (the verbatim hide rule present).
- [ ] **Step 2: Run `python3 tools/check_theme.py theme.xml` with no theme → exit 1, message names the missing file**
- [ ] **Step 3: Write `theme.xml`**: `<head>` with meta charset/viewport, fonts, `<b:skin>` holding the four colour `Variable`s plus the mockup's base CSS (tokens, reset, `.wrap`, `.btn*`, `.rv`, bilingual rule, reduced-motion block), the ten empty sections (`showaddelement='yes'`), `icons` includable called once at top of `<body>`, empty `atlas-js` script with `init()` and the export line.
- [ ] **Step 4: Write `test_js.mjs`** with one passing smoke test: the extracted script evaluates and exports an object.
- [ ] **Step 5: Run checker and tests** — `python3 tools/check_theme.py theme.xml && node --test tools/test_js.mjs` → `OK` and `pass 1`. Also `xmllint --noout theme.xml` → no output.
- [ ] **Step 6: Blogger checkpoint (needs the user)**: the user creates the test blog and uploads `theme.xml` (Theme → Customize ▸ Restore). Confirm: upload accepted; Layout shows the ten sections and accepts a new HTML widget; Theme Designer live preview opens and changes `accent`. If Layout or the preview breaks, remove `b:js='false'` and record why in the spec.
- [ ] **Step 7: Commit** `git add -A && git commit -m "feat: theme skeleton and checks"`

### Task 2: Contact data, WhatsApp, JSON-LD, footer

**Files:** Modify `theme.xml`, `tools/check_theme.py`, `tools/test_js.mjs`

**Interfaces:**
- Consumes: section `contact`, `icons`.
- Produces: LinkList widget `LinkList-contact` in section `contact` (item names `whatsapp`, `phone`, `hours`, `address`; text after `: ` in the name is the display value for `hours`/`address`); one hidden `<a id="wa-src" href="…">` rendered from the `whatsapp` item; every WhatsApp button in the theme is `<a data-wa href="#contact">`; `splitBi(s: string) -> {fr: string, ar: string}` (no ` | ` → both equal `s.trim()`); `waUrl(base: string, lines: string[]) -> string` (appends `?text=` with lines joined by `\n`, URI-encoded; `base` without `wa.me` → returns `base`).

- [ ] **Step 1: Failing JS tests**
  `splitBi('Cuisine | مطبخ')` → `{fr:'Cuisine', ar:'مطبخ'}`; `splitBi('Atlas')` → `{fr:'Atlas', ar:'Atlas'}`; `splitBi('A | B | C')` → `{fr:'A', ar:'B | C'}`; `waUrl('https://wa.me/212600000000', ['Nom: Sara','Msg: Salam'])` → `'https://wa.me/212600000000?text=Nom%3A%20Sara%0AMsg%3A%20Salam'`; `waUrl('#contact', ['x'])` → `'#contact'`.
- [ ] **Step 2: Run `node --test tools/test_js.mjs`** → the five fail (`splitBi is not a function`).
- [ ] **Step 3: Implement both functions in `#atlas-js`**; in `init()`: copy `#wa-src` href to every `[data-wa]`; the contact form's submit opens `waUrl(...)` with name, phone, message.
- [ ] **Step 4: Contact widget includable**: the CTA band of the mockup (Image widget `Image-contact-bg` as background), rows for phone/hours/address, the WhatsApp form, and server-rendered `<script type='application/ld+json'>` `LocalBusiness` with `name` = `data:blog.title`, `url` = `data:blog.homepageUrl`, `telephone`/`address`/`openingHours` only when the matching item exists. Footer + `.fab` written in the template, outside widgets, on every view.
- [ ] **Step 5: Checker rules**: `contact_everywhere` (section `contact` not wrapped in any `data:view` condition), `wa_buttons` (every `data-wa` anchor has `href='#contact'`), `jsonld_guarded` (each optional JSON-LD key sits inside a `b:if`).
- [ ] **Step 6: Run checker + tests** → all pass.
- [ ] **Step 7: Commit** `feat: contact data, whatsapp form, LocalBusiness`

### Task 3: Header, navigation, language switch

**Files:** Modify `theme.xml`, `tools/test_js.mjs`, `tools/check_theme.py`

**Interfaces:**
- Consumes: `splitBi`, `[data-wa]`.
- Produces: `<script id="atlas-head">` (before the stylesheet link, ≤ 400 bytes, ends with `if (typeof module !== 'undefined') module.exports = { pickLang };`) that sets `document.documentElement.lang`/`dir` from `localStorage['atlas-lang']` or `data-default` on `<html>` (rendered from `data:blog.locale`); `setLang(l: 'fr'|'ar')` in `#atlas-js`; elements with class `bi` get their text split into `<span lang=fr>`/`<span lang=ar>` by `applyBi(root)`; Header widget `Header1` (logo image if set, else the arch SVG mark + `bi` blog title); LinkList `LinkList-nav` whose hrefs are prefixed with `data:blog.homepageUrl` when they start with `#`.

- [ ] **Step 1: Failing JS test**: `pickLang(stored: string|null, def: string) -> 'fr'|'ar'` — `(null,'ar-MA')`→`'ar'`, `(null,'fr')`→`'fr'`, `('ar','fr')`→`'ar'`, `('xx','fr')`→`'fr'`.
- [ ] **Step 2: Run** → fails.
- [ ] **Step 3: Implement** `pickLang` in `#atlas-head` only (`#atlas-js` reads the `lang` already set on `<html>`), `setLang`, `applyBi` in `#atlas-js`; header markup, solid-on-scroll, segmented switch with sliding thumb, exactly as `mockup/home-v2.html`.
- [ ] **Step 4: Checker rule** `nav_absolute` (nav link hrefs built with `data:blog.homepageUrl`).
- [ ] **Step 5: Run checker + tests** → pass. Open the theme on the test blog with the user (or on the user's go-ahead, in the browser pane): FR and AR, 375px and 1280px, compare with the mockup header.
- [ ] **Step 6: Commit** `feat: header and language switch`

### Task 4: Hero slider and marquee

**Files:** Modify `theme.xml`, `tools/test_js.mjs`

**Interfaces:**
- Consumes: `applyBi`, `icons`.
- Produces: section `hero` holds up to 3 Image widgets (`Image-hero-1..3`); widget 1's `title` = H1 (`bi`), `caption` = subline (`bi`), `link` = primary button; slides from widgets 2–3 use only their image. `nextIndex(i: number, n: number, step: 1|-1) -> number` (wraps). Marquee from `LinkList-marquee`, items rendered once server-side, duplicated by JS.

- [ ] **Step 1: Failing tests**: `nextIndex(2,3,1)`→`0`, `nextIndex(0,3,-1)`→`2`, `nextIndex(0,1,1)`→`0`.
- [ ] **Step 2: Run** → fail.
- [ ] **Step 3: Implement** slider (crossfade, Ken Burns, progress dots, counter) with `nextIndex`; when only one slide exists, no dots, no timer. First image `fetchpriority='high'`, `sourceSrcset` widths 800/1400/1800.
- [ ] **Step 4: Checker rule** `hero_lcp` (exactly one `fetchpriority` in the theme, inside the hero includable).
- [ ] **Step 5: Run checker + tests**; on the test blog: 3 slides cycle; delete slides 2–3 → page still works, console clean.
- [ ] **Step 6: Commit** `feat: hero slider and marquee`

### Task 5: Services bento and before/after

**Files:** Modify `theme.xml`

**Interfaces:**
- Consumes: `icons`, `applyBi`.
- Produces: `Image-service-main` (big tile), `HTML-services` (small tiles: `<div class="tile" data-icon="paint">` with `bi` title and line; allowed icons `paint tile drop bolt shield clock chat home`, unknown → `home`), `Image-before`, `Image-after`, `LinkList-steps`.

- [ ] **Step 1: Implement** bento grid and before/after exactly as the mockup; the before/after container is `direction:ltr`; the `<input type=range>` drives `--pos`.
- [ ] **Step 2: Checker rule** `ba_ltr` (the `.ba` rule contains `direction:ltr`).
- [ ] **Step 3: Run checker + tests**; on the test blog in AR: dragging right reveals « بعد » on the right.
- [ ] **Step 4: Commit** `feat: services and before/after`

### Task 6: Blog widget — carousel, grids, project page, static page, 404

**Files:** Modify `theme.xml`, `tools/test_js.mjs`, `tools/check_theme.py`

**Interfaces:**
- Consumes: `applyBi`, `[data-wa]`, `icons`.
- Produces: includable `projCard` (image via `featuredImage` + `resizeImage` 800×1000, badge = first label `bi`, `h3.bi` title, year from `data:post.date`); homepage = carousel of `projCard`s with arrows using `scrollSign(dir: 'ltr'|'rtl') -> 1|-1`; label/search/archive = grid of `projCard`s + `noindex`; post page = `h1.bi` followed immediately by an inline `applyBi(document.currentScript.previousElementSibling)` call, body, WhatsApp CTA, newer/older links, link to the label page, `BreadcrumbList` JSON-LD; static page = same without gallery; 404 = short bilingual message + home link.

- [ ] **Step 1: Failing tests**: `scrollSign('ltr')`→`1`, `scrollSign('rtl')`→`-1`.
- [ ] **Step 2: Run** → fail.
- [ ] **Step 3: Implement** the views above. Post without image → card shows a neutral `.ph` block (no `<img>`). Post body without `div[lang]` → shown in both languages.
- [ ] **Step 4: Checker rules** `post_h1_inline_split` (the post `h1` is followed by the inline split script), `noindex_lists` (robots `noindex` emitted for `isLabelSearch`, `isSearch`, `isArchive`).
- [ ] **Step 5: Run checker + tests**; on the test blog: a post titled `Atlas` (no `|`), a post with no image and no lang divs, a normal post — all render cleanly; carousel arrows in AR move the right way.
- [ ] **Step 6: Commit** `feat: projects carousel, grids and post page`

### Task 7: Numbers, reviews, team

**Files:** Modify `theme.xml`

**Interfaces:**
- Consumes: `applyBi`, `nextIndex`, `scrollSign`.
- Produces: `HTML-numbers` (`<b data-count="340" data-suffix="+">`), `HTML-reviews` (`.review` blocks), team = Image widgets `Image-team-*` (title = name, caption = role `bi`).

- [ ] **Step 1: Implement** count-up on reveal, reviews slider with dots and autoplay paused on hover/touch, team grid with greyscale-to-colour hover, all as the mockup.
- [ ] **Step 2: Run checker + tests**; on the test blog: counters end on their values, review dots follow swipe in AR.
- [ ] **Step 3: Commit** `feat: numbers, reviews, team`

### Task 8: SEO head

**Files:** Modify `theme.xml`, `tools/check_theme.py`

**Interfaces:** Consumes the views from Task 6.

- [ ] **Step 1: Implement** `<title>` (home `data:blog.title`; post `data:post.title` + ` — ` + `data:blog.title`), `meta description` (home: blog description; post: search description else snippet), `link rel=canonical` from `data:view.url.canonical`, Open Graph + Twitter card (`og:image` = `data:blog.postImageUrl` on posts; none on other views, because widget images are not readable from `<head>` — a known gap against spec §10, report it), one `h1` per view.
- [ ] **Step 2: Checker rules** `one_canonical`, `og_present`.
- [ ] **Step 3: Run checker + tests**; Rich Results Test on a post URL and the home URL → `LocalBusiness` and `BreadcrumbList` valid.
- [ ] **Step 4: Commit** `feat: SEO head`

### Task 9: Demo content, README, LICENSE

**Files:** Create `demo/widgets.md`, `demo/posts/*.html` (6 posts from the mockup projects, one label each, FR/AR title format, `div[lang]` bodies), `README.md`, `LICENSE`.

- [ ] **Step 1: Write** `demo/widgets.md`: for every widget id from Tasks 2–7, the exact title / caption / link / HTML to paste. Images: the Unsplash photos already used by the mockup, plus a real « before » photo distinct from « after »; all uploaded to Blogger.
- [ ] **Step 2: Write README** per the global README rule (centered header, tool logos with verified simpleicons slugs, real badges, features, structure, install in Blogger, the one-label rule, the `FR | AR` rule, custom-domain note, credit). PageSpeed numbers left out until Task 10 measures them.
- [ ] **Step 3: Checker** runs `no_emoji` on `demo/` and `README.md` too.
- [ ] **Step 4: Run checker + tests** → pass.
- [ ] **Step 5: Commit** `docs: demo content and README`

### Task 10: Full verification in Blogger (with the user)

- [ ] **Step 1:** Fill the test blog from `demo/` (the user pastes, or Claude does it in the browser pane on the user's explicit go-ahead).
- [ ] **Step 2:** Run every point of spec §11 (1–11); screenshots at 375px and 1440px in FR and AR side by side with `mockup/home-v2.html`; list every difference and fix it in `theme.xml` (back through checker + tests).
- [ ] **Step 3:** PageSpeed mobile on home and one post; write the real scores in the README. Below 90 or CLS ≥ 0.1 → fix before done.
- [ ] **Step 4:** Commit `chore: verified on Blogger`; report honestly what passed, what did not.
