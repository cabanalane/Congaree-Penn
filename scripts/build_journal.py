"""Build The Eleven journal from journal-src/*.md into website/journal/.

Each article: YAML-ish front matter + simple markdown (##, ###, >, - lists, paragraphs).
Writes the journal home, one page per category, one page per article, and updates sitemap.xml.
Usage: python3 -I scripts/build_journal.py   (run from the repo root)
"""
import html
import json
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "journal-src")
WEB = os.path.join(ROOT, "website")
SITE = "https://elevenjacksonville.com"

CATEGORIES = [
    ("farm-notes", "Farm Notes", "Seasons, crops, animals and the daily rhythm of the farm."),
    ("the-map-is-changing", "The Map Is Changing", "Progress at The Eleven: closings, groundbreakings and Claims named."),
    ("agrarian-revival", "Agrarian Revival", "The architecture and philosophy behind The Eleven."),
    ("claim-plans", "Claim Plans", "The Weekender Series, house plans and the Collective's designs."),
    ("from-the-lexicon", "From the Lexicon", "Claim, Dependency, Proving Up and the words we live by."),
    ("owning-a-claim", "Owning a Claim", "Plain guides to buying, building and living at The Eleven."),
]
CAT_BY_NAME = {name: (slug, name, desc) for slug, name, desc in CATEGORIES}
E = html.escape


def parse(path):
    text = open(path, encoding="utf-8").read()
    _, fm, body = text.split("---", 2)
    meta, faq, cur = {}, [], None
    for line in fm.strip().splitlines():
        if line.startswith("faq:"):
            continue
        m = re.match(r"\s+- q:\s*(.*)", line)
        if m:
            cur = {"q": m.group(1)}; faq.append(cur); continue
        m = re.match(r"\s+a:\s*(.*)", line)
        if m:
            cur["a"] = m.group(1); continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    meta["faq"] = faq
    meta["body"] = body.strip()
    return meta


def md(body):
    out, items = [], []
    def flush():
        if items:
            out.append("<ul class=\"art-list\">" + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for block in [b.strip() for b in body.split("\n\n") if b.strip()]:
        if block.startswith("- "):
            items.append(block[2:]); continue
        flush()
        if block.startswith("### "):
            out.append(f"<h3>{E(block[4:])}</h3>")
        elif block.startswith("## "):
            out.append(f"<h2>{E(block[3:])}</h2>")
        elif block.startswith("> "):
            out.append(f"<blockquote class=\"pull\"><p>{E(block[2:])}</p></blockquote>")
        else:
            out.append(f"<p>{E(block)}</p>")
    flush()
    return "\n".join(out)


def nice_date(d):
    y, m, dd = map(int, d.split("-"))
    return date(y, m, dd).strftime("%B %-d, %Y")


def head(title, desc, canonical, up, og_img, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(canonical)}">
<meta name="theme-color" content="#233025">
<meta property="og:site_name" content="The Eleven at Congaree &amp; Penn">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{E(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{up}assets/img/favicon.png">
<link rel="alternate" type="application/rss+xml" title="The Eleven Journal" href="{SITE}/journal/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=EB+Garamond:ital,wght@0,400;0,500;1,400&amp;family=Jost:wght@500&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/css/site.css">
{extra}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav">
  <div class="wrap">
    <a class="brand" href="{up}index.html" aria-label="The Eleven at Congaree &amp; Penn, home">
      <img src="{up}assets/img/the-eleven-script-logo-dark-500.png" alt="The Eleven" width="142" height="40" style="height:40px;width:auto">
      <span class="sep" aria-hidden="true"></span>
      <img src="{up}assets/img/congaree-penn-guinea-hen-dark-120.png" alt="Congaree &amp; Penn" width="26" height="26" style="height:26px;width:auto">
    </a>
    <nav aria-label="Main">
      <ul>
        <li><a href="{up}index.html#land">The Land</a></li>
        <li><a href="{up}index.html#life">The Life</a></li>
        <li><a href="{up}index.html#architecture">Architecture</a></li>
        <li><a href="{up}journal/index.html">Journal</a></li>
        <li><a class="btn btn-pine" href="{up}index.html#visit">Schedule a Tour</a></li>
      </ul>
    </nav>
  </div>
</header>
"""


def foot(up):
    return f"""<section class="dark j-cta" aria-label="Schedule a tour">
  <div class="wrap">
    <p class="ch">Stake your claim</p>
    <h2 class="h2">Come walk <em>the land.</em></h2>
    <p class="lede">Nine Claims remain, and there will only ever be eleven.</p>
    <div class="btns"><a class="btn btn-brass" href="sms:+18434756686?&amp;body=I%27d%20like%20to%20schedule%20a%20tour%20of%20The%20Eleven">Schedule a Tour</a><a class="btn btn-line" href="tel:+18434756686">Call John · 843.475.6686</a></div>
  </div>
</section>
<footer class="foot">
  <div class="wrap">
    <div class="marks">
      <img src="{up}assets/img/the-eleven-script-logo-ivory-500.png" alt="The Eleven" width="128" height="36" loading="lazy" style="height:36px;width:auto">
      <img src="{up}assets/img/congaree-penn-guinea-hen-ivory-120.png" alt="Congaree &amp; Penn" width="28" height="28" loading="lazy" style="height:28px;width:auto">
    </div>
    <p class="lbl">11830 Old Kings Road · Jacksonville, Florida 32219</p>
    <p>©2014–2026 Congaree and Penn. <a href="https://www.congareeandpenn.com/">congareeandpenn.com</a></p>
  </div>
</footer>
</body>
</html>
"""


def pic(up, name, w, h, alt, sizes="100vw", eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture><source type="image/webp" srcset="{up}assets/img/{name}-{w}.webp">'
            f'<img src="{up}assets/img/{name}-{w}.jpg" width="{w}" height="{h}" {load} alt="{E(alt)}"></picture>')


def card(a, up):
    slug, cname, _ = CAT_BY_NAME[a["category"]]
    href = a.get("external") or f"{up}journal/{a['slug']}/index.html"
    return f"""<article class="j-card">
  <a href="{E(href)}">
    {pic(up, a['hero'], a['hero_w'], a['hero_h'], '')}
    <p class="lbl">{E(cname)} · {nice_date(a['date'])} · {E(a['author'])}</p>
    <h3>{E(a['title'])}</h3>
    <p>{E(a['excerpt'])}</p>
  </a>
</article>"""


def article_page(a, all_articles):
    up = "../../"
    url = f"{SITE}/journal/{a['slug']}/"
    canonical = a.get("canonical") or url
    cslug, cname, _ = CAT_BY_NAME[a["category"]]
    og = f"{SITE}/assets/img/{a['hero']}-{a['hero_w']}.jpg"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "headline": a["title"], "description": a["meta_description"],
         "image": og, "datePublished": a["date"], "dateModified": a.get("modified", a["date"]),
         "author": {"@type": "Person", "name": a["author"], "jobTitle": a.get("author_role", "")},
         "publisher": {"@type": "Organization", "name": "Congaree and Penn", "url": "https://www.congareeandpenn.com/"},
         "mainEntityOfPage": canonical, "articleSection": cname, "url": url},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "The Eleven", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Journal", "item": SITE + "/journal/"},
            {"@type": "ListItem", "position": 3, "name": cname, "item": f"{SITE}/journal/{cslug}/"},
            {"@type": "ListItem", "position": 4, "name": a["title"], "item": url}]}]}
    if a["faq"]:
        ld["@graph"].append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in a["faq"]]})
    extra = '<meta property="og:type" content="article">\n<script type="application/ld+json">' + json.dumps(ld) + "</script>\n"
    first = ""
    if a.get("canonical"):
        first = (f'<p class="art-origin">First published at <a href="{E(a["canonical"])}">{E(a.get("original_name", "the original"))}</a>.</p>')
    faq = ""
    if a["faq"]:
        faq = '<section class="art-faq" aria-label="Questions"><p class="lbl">Questions, answered</p>' + "".join(
            f'<details><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in a["faq"]) + "</section>"
    more = [x for x in all_articles if x is not a][:2]
    more_html = ""
    if more:
        more_html = '<section class="sec journal" aria-label="More from the Journal"><div class="wrap"><p class="ch">More from the Journal</p><div class="cards">' + "".join(card(x, up) for x in more) + "</div></div></section>"
    return head(a["seo_title"], a["meta_description"], canonical, up, og, extra) + f"""<main id="main">
<article class="art">
  <header class="art-head">
    <div class="wrap art-narrow">
      <p class="lbl"><a href="{up}journal/index.html">Journal</a> · <a href="{up}journal/{cslug}/index.html">{E(cname)}</a></p>
      <h1>{E(a['title'])}</h1>
      <p class="art-by">By {E(a['author'])}<span>{E(a.get('author_role', ''))}</span> · <time datetime="{a['date']}">{nice_date(a['date'])}</time></p>
    </div>
  </header>
  <figure class="art-hero">{pic(up, a['hero'], a['hero_w'], a['hero_h'], a['hero_alt'], eager=True)}</figure>
  <div class="wrap art-narrow art-body">
{md(a['body'])}
{faq}
{first}
  </div>
</article>
{more_html}
</main>
""" + foot(up)


def list_page(title, desc, canonical, up, intro_h, intro_p, articles, active):
    chips = f'<a class="chip{" on" if active is None else ""}" href="{up}journal/index.html">All</a>' + "".join(
        f'<a class="chip{" on" if active == s else ""}" href="{up}journal/{s}/index.html">{E(n)}</a>' for s, n, _ in CATEGORIES)
    grid = "".join(card(a, up) for a in articles) or '<p class="j-empty">The first essays in this series are on their way.</p>'
    og = f"{SITE}/assets/img/og-the-eleven.jpg"
    return head(title, desc, canonical, up, og) + f"""<main id="main">
<section class="sec j-home">
  <div class="wrap">
    <p class="ch">The Journal</p>
    <h1 class="h2">{intro_h}</h1>
    <p class="lede" style="margin-top:18px;max-width:640px">{E(intro_p)}</p>
    <nav class="chips" aria-label="Journal categories">{chips}</nav>
    <div class="cards j-grid">{grid}</div>
  </div>
</section>
</main>
""" + foot(up)


def main():
    arts = [parse(os.path.join(SRC, f)) for f in sorted(os.listdir(SRC)) if f.endswith(".md")]
    for a in arts:
        a["hero_w"], a["hero_h"] = int(a["hero_w"]), int(a["hero_h"])
    arts.sort(key=lambda a: a["date"], reverse=True)
    local = [a for a in arts if not a.get("external")]
    os.makedirs(os.path.join(WEB, "journal"), exist_ok=True)
    for a in local:
        d = os.path.join(WEB, "journal", a["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(article_page(a, arts))
    open(os.path.join(WEB, "journal", "index.html"), "w", encoding="utf-8").write(list_page(
        "The Journal | The Eleven at Congaree & Penn",
        "Essays from The Eleven at Congaree & Penn: farm notes, Agrarian Revival architecture, Claim plans and plain guides to owning ten acres on a working Florida farm.",
        SITE + "/journal/", "../", "Notes from <em>the farm.</em>",
        "Essays on the land, the architecture and the life at The Eleven, written by the people who steward it.", arts, None))
    for s, n, desc in CATEGORIES:
        d = os.path.join(WEB, "journal", s); os.makedirs(d, exist_ok=True)
        these = [a for a in arts if a["category"] == n]
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(list_page(
            f"{n} | The Eleven Journal", desc, f"{SITE}/journal/{s}/", "../../", E(n), desc, these, s))
    # RSS
    items = "".join(f"<item><title>{E(a['title'])}</title><link>{SITE}/journal/{a['slug']}/</link><guid>{SITE}/journal/{a['slug']}/</guid><pubDate>{date.fromisoformat(a['date']).strftime('%a, %d %b %Y')} 12:00:00 -0500</pubDate><description>{E(a['excerpt'])}</description></item>" for a in local)
    open(os.path.join(WEB, "journal", "feed.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>The Eleven Journal</title><link>{SITE}/journal/</link><description>Essays from The Eleven at Congaree &amp; Penn</description>{items}</channel></rss>\n')
    # sitemap (own-canonical pages only)
    urls = [SITE + "/", SITE + "/journal/"] + [f"{SITE}/journal/{s}/" for s, _, _ in CATEGORIES if any(a["category"] == CAT_BY_NAME_REV[s] for a in arts)]
    urls += [f"{SITE}/journal/{a['slug']}/" for a in local if not a.get("canonical")]
    today = date.today().isoformat()
    open(os.path.join(WEB, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    print("built", len(local), "articles,", len(arts), "listed")


CAT_BY_NAME_REV = {s: n for s, n, _ in CATEGORIES}

if __name__ == "__main__":
    main()
