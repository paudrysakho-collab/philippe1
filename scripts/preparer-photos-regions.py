#!/usr/bin/env python3
"""Prépare les photos de régions (data/photos-regions.json) : originaux de
src/photos/regions-brut/ (ignoré par git, rechargeables depuis Commons) → versions traitées
de src/photos/regions/, 2400 px de large au plus, même traitement pour toutes : couleurs un
peu adoucies et réchauffées, pour qu'elles appartiennent au tuffeau du catalogue.
2400 px sur 204 mm imprimés donnent environ 300 ppi : bien au-dessus du minimum de 200."""
import json
import pathlib

from PIL import Image, ImageEnhance

RACINE = pathlib.Path(__file__).resolve().parent.parent
REG = json.loads((RACINE / "data/photos-regions.json").read_text(encoding="utf-8"))


def traiter(src, dst, largeur=2400):
    im = Image.open(src).convert("RGB")
    im.thumbnail((largeur, largeur * 2))
    im = ImageEnhance.Color(im).enhance(0.86)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.03 + 4)))
    b = b.point(lambda v: int(v * 0.95))
    im = Image.merge("RGB", (r, g, b))
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=84, optimize=True, progressive=True)
    return im.size


for nom, x in REG.items():
    src, dst = RACINE / x["brut"], RACINE / x["fichier"]
    if not src.exists():
        print(f"✗ {nom} : original absent ({x['brut']}) — le recharger depuis {x['page']}")
        continue
    w, h = traiter(src, dst)
    print(f"✓ {nom} : {dst.relative_to(RACINE)} ({w} × {h})")
