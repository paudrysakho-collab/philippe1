#!/usr/bin/env python3
"""Range les images du Canva de l'agence (« Tarif septembre 2026 ») dans src/photos/brut/canva/.

Le Canva ne se lit pas image par image à pleine taille : on l'exporte en PDF qualité « pro »
(Canva → Partager → Télécharger → PDF Impression), puis ce script en extrait les images
telles qu'elles y sont incorporées, avec leur transparence quand elles en ont une.

    python3 scripts/extraire-canva.py export.pdf            toutes les pages domaines
    python3 scripts/extraire-canva.py export.pdf 40 43      seulement les pages 40 à 43

Chaque image devient src/photos/brut/canva/dNN-pPP-XXX.png : NN est le numéro du domaine,
PP la page du Canva (le domaine n est en page n + 3, comme dans le PDF source), XXX le rang
de l'image dans le PDF. On choisit ensuite à l'œil, et on écrit le choix dans
data/photos-locales.json. Le design Canva n'est jamais modifié.
"""
import pathlib, subprocess, sys, tempfile
from PIL import Image

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "src/photos/brut/canva"

pdf = pathlib.Path(sys.argv[1])
premiere = int(sys.argv[2]) if len(sys.argv) > 2 else 4
derniere = int(sys.argv[3]) if len(sys.argv) > 3 else 43
SORTIE.mkdir(parents=True, exist_ok=True)

liste = subprocess.run(["pdfimages", "-list", "-f", str(premiere), "-l", str(derniere), str(pdf)],
                       capture_output=True, text=True, check=True).stdout.splitlines()[2:]
# une image et son masque de transparence partagent le même objet
objets = {}
for ligne in liste:
    c = ligne.split()
    if len(c) < 11:
        continue
    page, rang, genre, objet = int(c[0]), int(c[1]), c[2], c[10]
    objets.setdefault((page, objet), {})[genre] = rang

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["pdfimages", "-png", "-p", "-f", str(premiere), "-l", str(derniere),
                    str(pdf), f"{tmp}/c"], check=True)
    n = 0
    for (page, _), d in sorted(objets.items()):
        if "image" not in d or not 4 <= page <= 43:
            continue
        im = Image.open(f"{tmp}/c-{page:03d}-{d['image']:03d}.png")
        if min(im.size) < 150:
            continue        # pictos, pastilles : rien à poser dans un rond ou une bande
        if "smask" in d:
            masque = Image.open(f"{tmp}/c-{page:03d}-{d['smask']:03d}.png").convert("L")
            if masque.size == im.size and masque.getextrema()[0] < 250:
                im = im.convert("RGB")
                im.putalpha(masque)
        im.save(SORTIE / f"d{page - 3:02d}-p{page:02d}-{d['image']:03d}.png")
        n += 1
print(f"{n} images → {SORTIE.relative_to(RACINE)}/")
