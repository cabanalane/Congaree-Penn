"""Optimize source images for The Eleven site.

For each photo: resize to display widths, write WebP (q80) and JPEG (q82, progressive),
strip metadata. Logos/line drawings: WebP + PNG, trimmed sizes.
Usage: python3 -I optimize_images.py SRC_DIR OUT_DIR
"""
import os
import sys
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
P = "mcp-claude-artifacts-blob-"

# source suffix -> (seo name, widths, kind)
JOBS = [
    ("chjuer-e4265dc2.png", "lake-bales-farmhouse-court-atkins-the-eleven", [800, 1414], "photo"),
    ("kujgp5-0c37710d.jpg", "congaree-penn-aerial-film-poster", [800, 1200], "photo"),
    ("stwbwd-f5f10fc0.jpg", "congaree-penn-farm-map-the-eleven", [800, 1200], "photo"),
    ("acyomu-e69f6f33.jpg", "the-eleven-claim-map-eleven-claims", [800, 1200], "photo"),
    ("h82m2c-e95ff162.jpg", "scott-lindsay-meyer-founders-congaree-penn", [800, 1600], "photo"),
    ("q8to3j-e4a5e40d.jpg", "john-hillman-broker-the-eleven", [800, 1600], "photo"),
    ("rc8nq7-5834d2fa.jpg", "clarke-design-group-claim-plan-the-eleven", [800, 1400], "photo"),
    ("tosqw6-cc9130de.png", "the-weekender-pearce-scott-architects", [520], "drawing"),
    ("097zeg-7c6268c0.png", "guest-cottage-dependency-the-eleven", [800, 1370], "drawing"),
    ("6fxxnn-257b411a.png", "gathering-barn-dependency-the-eleven", [800, 1400], "drawing"),
    ("fm55qz-b1924db6.png", "the-eleven-script-logo-dark", [500], "logo"),
    ("w4333z-c1ce39ed.png", "the-eleven-script-logo-ivory", [500], "logo"),
    ("ppjut0-e8fdfcc0.png", "congaree-penn-guinea-hen-dark", [120], "logo"),
    ("yp36rl-e9ea4edd.png", "congaree-penn-guinea-hen-ivory", [120], "logo"),
]

files = os.listdir(SRC)
report = []
for suffix, name, widths, kind in JOBS:
    match = [f for f in files if f.startswith(P) and f.endswith(suffix)]
    if not match:
        print("MISSING", suffix)
        continue
    im = Image.open(os.path.join(SRC, match[0]))
    im.load()
    for w in widths:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS) if w != im.width else im.copy()
        base = os.path.join(OUT, f"{name}-{w}")
        if kind == "photo":
            rgb = r.convert("RGB")
            rgb.save(base + ".webp", "WEBP", quality=80, method=6)
            rgb.save(base + ".jpg", "JPEG", quality=82, optimize=True, progressive=True)
        else:
            has_alpha = r.mode in ("RGBA", "LA", "P")
            rr = r.convert("RGBA") if has_alpha else r.convert("RGB")
            rr.save(base + ".webp", "WEBP", quality=85, method=6)
            rr.save(base + ".png", "PNG", optimize=True)
        report.append((f"{name}-{w}", w, h, os.path.getsize(base + ".webp") // 1024))

for row in report:
    print(*row)

# favicon from the dark hen
hen = [f for f in files if f.endswith("ppjut0-e8fdfcc0.png")][0]
im = Image.open(os.path.join(SRC, hen)).convert("RGBA")
im.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
im.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "favicon.png"), optimize=True)

# Open Graph image 1200x630 from the Lake Bales drawing on ivory
lb = [f for f in files if f.endswith("chjuer-e4265dc2.png")][0]
src = Image.open(os.path.join(SRC, lb)).convert("RGB")
scale = 1200 / src.width
s = src.resize((1200, round(src.height * scale)), Image.LANCZOS)
top = max(0, (s.height - 630) // 2)
s.crop((0, top, 1200, top + 630)).save(os.path.join(OUT, "og-the-eleven.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
print("done")
