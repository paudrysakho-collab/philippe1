#!/usr/bin/env python3
"""Une planche de contact par domaine : pour choisir les images à l'œil, pas au hasard."""
import json, math, pathlib, sys
from PIL import Image, ImageDraw

RACINE = pathlib.Path(__file__).resolve().parent.parent
inv = json.loads((RACINE / "data/images-moissonnees.json").read_text(encoding="utf-8"))
SORTIE = pathlib.Path("/tmp/claude-0/-home-user-philippe1/82df59d0-bf07-5fcb-8765-5c3bb40b9013/scratchpad/planches")
SORTIE.mkdir(parents=True, exist_ok=True)

COLS, VIGN = 8, 190
for n, d in sorted(inv.items(), key=lambda kv: int(kv[0])):
    imgs = [i for i in d["images"] if max(i["l"], i["h"]) >= 450]
    if not imgs:
        continue
    imgs = sorted(imgs, key=lambda i: -(i["l"] * i["h"]))[:40]
    rangs = math.ceil(len(imgs) / COLS)
    planche = Image.new("RGB", (COLS * (VIGN + 8) + 8, rangs * (VIGN + 30) + 8), "#333")
    dess = ImageDraw.Draw(planche)
    for k, info in enumerate(imgs):
        try:
            im = Image.open(RACINE / info["fichier"]).convert("RGB")
        except Exception:
            continue
        im.thumbnail((VIGN, VIGN), Image.LANCZOS)
        x = 8 + (k % COLS) * (VIGN + 8)
        y = 8 + (k // COLS) * (VIGN + 30)
        planche.paste(im, (x + (VIGN - im.width) // 2, y + (VIGN - im.height) // 2))
        etiquette = f"{pathlib.Path(info['fichier']).stem}  {info['l']}x{info['h']}"
        dess.text((x + 2, y + VIGN + 6), etiquette, fill="#eee")
    chemin = SORTIE / f"d{int(n):02d}.png"
    planche.save(chemin)
    print(f"n°{int(n):>2} {len(imgs):>3} vignettes → {chemin.name}")
