# The Eleven at Congaree & Penn — website

A fast, static, one-page site built from design "Option 2 — The Story of The Eleven".
No build step: plain HTML + CSS, ready for Cloudflare Pages or Netlify.

## Structure
- `index.html` — the page, with title/description, Open Graph, and JSON-LD (WebSite, WebPage, Organization, Place, Person, FAQPage)
- `assets/css/site.css` — all styles (brand tokens at the top)
- `assets/img/` — optimized images: WebP + JPEG/PNG fallback at two widths, SEO file names
- `robots.txt`, `sitemap.xml`, `404.html`, `_headers` (long cache for assets)

## Before going live
1. Choose the domain, then run `sh scripts/set-domain.sh https://www.YOUR-DOMAIN` to fill every `{{SITE_URL}}`.
2. Hosting: Cloudflare Pages → Create project → connect this GitHub repo → build output directory `website` (no build command).
3. Add the custom domain in Cloudflare Pages and the DNS record it shows at the domain registrar.

## Images
New photos: run `python3 -I scripts/optimize_images.py SOURCE_DIR website/assets/img` (edit the JOBS list),
which resizes, compresses to WebP/JPEG and strips camera data.

## Open items
- A real landscape/drone photo for the farm (the aerial here is the YouTube poster with its play button)
- "It All Begins" essay link points to /blog until the post is published there
- Move this folder into the private `cabanalane/websites` repo once it exists

## Journal
Articles live in `journal-src/*.md` (front matter + simple markdown). Run `python3 -I scripts/build_journal.py`
to rebuild `website/journal/` (home, six category pages, article pages, RSS feed) and `website/sitemap.xml`.
Copied articles carry `canonical:` pointing to their original; new originals omit it.
