#!/usr/bin/env python3
"""Repère les tableaux de prix sur les rendus de page et les recadre dans data/recadrages/.

Les tableaux du PDF source sont des images : on les localise par leurs aplats
(bandeau doré, lignes roses, lignes grises, en-tête magenta « Tarif »).
"""
import json, pathlib
from PIL import Image

RACINE = pathlib.Path(__file__).resolve().parent.parent
PAGES = RACINE / "data/pages"
SORTIE = RACINE / "data/recadrages"
SORTIE.mkdir(parents=True, exist_ok=True)

TEINTES = [(219, 189, 119), (214, 188, 108),   # bandeau doré « possibilité de panacher »
           (241, 230, 238), (239, 230, 233),   # lignes roses
           (190, 190, 190),                    # lignes grises
           (173, 58, 113), (176, 60, 115)]     # en-tête magenta « Tarif »
TOLERANCE = 18
MARGE = 14          # px ajoutés autour du recadrage
TROU_MAX = 26       # px de blanc tolérés à l'intérieur d'un même tableau
HAUTEUR_MIN = 40    # px : en dessous, ce n'est pas un tableau

def est_teinte(px):
    for r, g, b in TEINTES:
        if abs(px[0] - r) <= TOLERANCE and abs(px[1] - g) <= TOLERANCE and abs(px[2] - b) <= TOLERANCE:
            return True
    return False

def bandes(img):
    larg, haut = img.size
    px = img.load()
    lignes = []
    for y in range(haut):
        n = sum(1 for x in range(0, larg, 4) if est_teinte(px[x, y]))
        lignes.append(n > larg / 4 / 4)      # au moins un quart de la largeur échantillonnée
    out, debut, trou = [], None, 0
    for y, plein in enumerate(lignes):
        if plein:
            if debut is None:
                debut = y
            trou = 0
        elif debut is not None:
            trou += 1
            if trou > TROU_MAX:
                if y - trou - debut >= HAUTEUR_MIN:
                    out.append((debut, y - trou))
                debut, trou = None, 0
    if debut is not None and haut - debut >= HAUTEUR_MIN:
        out.append((debut, haut))
    return out

DORE = [(219, 189, 119), (214, 188, 108)]

def est_dore(px):
    for r, g, b in DORE:
        if abs(px[0] - r) <= TOLERANCE and abs(px[1] - g) <= TOLERANCE and abs(px[2] - b) <= TOLERANCE:
            return True
    return False

def a_bandeau_dore(img, haut_bande):
    """Un vrai tableau porte le bandeau doré « possibilité de panacher » ou « BIB ».
    Les pastilles roses (ALLOCATION!, encarts de panachage) ne l'ont pas."""
    larg, _ = img.size
    px = img.load()
    for y in range(haut_bande[0], haut_bande[1]):
        n = sum(1 for x in range(0, larg, 4) if est_dore(px[x, y]))
        if n > larg / 4 * 0.30:
            return True
    return False

def bornes_x(img, haut_bande):
    larg, _ = img.size
    px = img.load()
    y0, y1 = haut_bande
    xmin, xmax = larg, 0
    for y in range(y0, y1, 2):
        for x in range(larg):
            if est_teinte(px[x, y]):
                xmin = min(xmin, x); break
        for x in range(larg - 1, -1, -1):
            if est_teinte(px[x, y]):
                xmax = max(xmax, x); break
    return xmin, xmax

def main():
    index = {}
    for numero in range(1, 41):
        page = numero + 3
        img = Image.open(PAGES / f"p-{page:02d}.png").convert("RGB")
        larg, haut = img.size
        fichiers = []
        retenues = [b for b in bandes(img) if a_bandeau_dore(img, b)]
        for i, bande in enumerate(retenues, 1):
            x0, x1 = bornes_x(img, bande)
            if x1 <= x0:
                continue
            boite = (max(0, x0 - MARGE), max(0, bande[0] - MARGE),
                     min(larg, x1 + MARGE), min(haut, bande[1] + MARGE))
            nom = f"d{numero:02d}-t{i}.png"
            img.crop(boite).save(SORTIE / nom, optimize=True)
            fichiers.append(nom)
        index[numero] = fichiers
        print(f"n°{numero:>2} (p.{page}) : {len(fichiers)} recadrage(s)")
    (RACINE / "data/recadrages/index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
