"""Batch 3 — lakes drone, full farm map (+ Eleven detail), inspiration images, film poster.
Usage: python3 -I optimize_batch3.py UPLOAD_DIR OUT_DIR POSTER_JPG
"""
import os, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
SRC, OUT, POSTER = sys.argv[1], sys.argv[2], sys.argv[3]

def save(im, name, widths, q=78):
    im = im.convert("RGB")
    for w in widths:
        w = min(w, im.width); h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS) if w != im.width else im
        b = os.path.join(OUT, f"{name}-{w}")
        r.save(b + ".webp", "WEBP", quality=q, method=6)
        r.save(b + ".jpg", "JPEG", quality=80, optimize=True, progressive=True)
        print(f"{name}-{w}", w, h, os.path.getsize(b + ".webp") // 1024, "KB")

save(Image.open(os.path.join(SRC, "e0328b3e-image.jpg")), "the-eleven-lakes-drone-cary-state-forest", [800, 1600, 1920], q=74)
fm = Image.open(os.path.join(SRC, "Overall_Farm_Map.jpg"))
fm.draft("RGB", (3900, 2782)); fm = fm.convert("RGB")
save(fm, "congaree-penn-overall-farm-map", [1000, 2000, 2800], q=76)
# The Eleven detail from the full-resolution map (western third)
full = Image.open(os.path.join(SRC, "Overall_Farm_Map.jpg")).convert("RGB")
W, H = full.size
det = full.crop((0, int(H * 0.27), int(W * 0.37), int(H * 0.80)))
save(det, "the-eleven-claims-detail-farm-map", [900, 1800], q=76)
save(Image.open(os.path.join(SRC, "2a3d5689-image.webp")), "inspiration-indoor-outdoor-living-illustrative", [800, 1248])
save(Image.open(os.path.join(SRC, "edfd28af-image.jpg")), "inspiration-open-air-pavilion-living", [800, 1135])
save(Image.open(os.path.join(SRC, "26200ab9-image.png")), "inspiration-quonset-hut-dining", [778])
save(Image.open(POSTER), "the-eleven-film-poster-sunset-lake", [800, 1280])
