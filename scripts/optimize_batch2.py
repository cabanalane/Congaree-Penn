"""Batch 2 (farm lifestyle) — crop, resize, WebP + JPEG, strip metadata.
Usage: python3 -I optimize_batch2.py SRC_DIR OUT_DIR
"""
import os
import sys
from PIL import Image

SRC, OUT = sys.argv[1], sys.argv[2]

# file, seo name, crop box (l, t, r, b) or None, widths
JOBS = [
    ("d09abd05-image.png", "live-oaks-spanish-moss-dog-days-congaree-penn", (0, 470, 1822, 1660), [800, 1400, 1822]),
    ("cf81b702-image.webp", "oyster-roast-fire-pit-pond-golden-hour-congaree-penn", None, [800, 1600]),
    ("e97cc8e2-image.webp", "shucking-oysters-farm-cider-congaree-penn", None, [800, 1400]),
    ("d258700c-image.webp", "oyster-roast-guests-under-live-oaks-congaree-penn", None, [700, 1100]),
    ("d994e318-image.webp", "oysters-over-open-fire-pond-congaree-penn", None, [700, 1100]),
    ("f4e49d4e-image.webp", "vintage-pickup-truck-pasture-congaree-penn", None, [800, 1600, 2400]),
    ("9f7571db-image.jpg", "grapevine-pavilion-vineyard-dining-congaree-penn", None, [800, 1600]),
    ("371a9e43-image.png", "grapevine-dinner-string-lights-dusk-congaree-penn", None, [775]),
]

for f, name, crop, widths in JOBS:
    im = Image.open(os.path.join(SRC, f)).convert("RGB")
    if crop:
        im = im.crop(crop)
    for w in widths:
        w = min(w, im.width)
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS) if w != im.width else im
        base = os.path.join(OUT, f"{name}-{w}")
        r.save(base + ".webp", "WEBP", quality=78, method=6)
        r.save(base + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)
        print(f"{name}-{w}", w, h, os.path.getsize(base + ".webp") // 1024, "KB webp", os.path.getsize(base + ".jpg") // 1024, "KB jpg")

# new social image from the live oak
oak = Image.open(os.path.join(SRC, "d09abd05-image.png")).convert("RGB").crop((0, 520, 1822, 1477))
oak.resize((1200, 630), Image.LANCZOS).save(os.path.join(OUT, "og-the-eleven.jpg"), "JPEG", quality=84, optimize=True, progressive=True)
print("og done")
