#!/usr/bin/env python3
"""Règle la lettrine et la place du texte du .pptx, domaine par domaine.

Dans le PDF, la lettrine tombe sur deux lignes (CSS). Dans le .pptx, elle a sa propre boîte
de texte (Canva ne garde pas une lettre plus grande dans un paragraphe) et monte au-dessus
de la première ligne. Le bloc, de la tête de la lettrine au pied de la dernière ligne, se
centre dans la bande ; pour cela, scripts/pptx.mjs doit savoir combien de lignes fait le
texte. Ce script fabrique le .pptx, le fait rendre par LibreOffice, et, pour chaque domaine :
- compte les lignes du texte et les note (le .pptx suivant centre le bloc juste) ;
- vérifie que la lettrine est posée sur la ligne de base de la première ligne ;
- si le bloc déborde de la bande, réduit la lettrine, puis resserre l'interligne.
Il recommence jusqu'à ce que rien ne bouge.

    python3 scripts/regler-lettrines.py                écrit src/gabarits/lettrines-pptx.json
    EDITION=salon python3 scripts/regler-lettrines.py  écrit src/gabarits/lettrines-pptx-salon.json

Demande LibreOffice (soffice) et PyMuPDF (pip install pymupdf). À relancer seulement si les
textes des domaines changent ; `npm run pptx` se contente de lire le fichier écrit.
"""
import json, os, pathlib, shutil, subprocess, sys, tempfile
import pymupdf

RACINE = pathlib.Path(__file__).resolve().parent.parent
SALON = os.environ.get("EDITION") == "salon"
BASE = "salon-prive-2026" if SALON else "catalogue-scio-2026"
SORTIE = RACINE / f"src/gabarits/lettrines-pptx{'-salon' if SALON else ''}.json"
PPTX = RACINE / f"dist/{BASE}-canva.pptx"
BOITES = RACINE / f"build/{BASE}-pptx-textes.json"
MARGE_BAS = 3.0                      # mm : le tableau commence 4,5 mm sous la bande
MARGE_HAUT = 3.5                     # mm : la ligne d'étiquettes est au-dessus


def mm(pt):
    return pt / 72 * 25.4


def rendre():
    subprocess.run(["node", "scripts/pptx.mjs"], cwd=RACINE, check=True, stdout=subprocess.DEVNULL)
    tmp = pathlib.Path(tempfile.mkdtemp())
    shutil.copy(PPTX, tmp / "c.pptx")
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp),
                    str(tmp / "c.pptx")], check=True, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=600)
    return tmp / "c.pdf"


def mesurer(pdf):
    """n° → {lignes, ecart, haut, bas} : nombre de lignes du texte, écart en mm entre la ligne
    de base de la lettrine et celle de la première ligne, et débords du bloc en haut et en bas
    (positif = le bloc sort de sa bande)."""
    boites = json.loads(BOITES.read_text(encoding="utf-8"))
    doc = pymupdf.open(pdf)
    res = {}
    for n, b in boites.items():
        page = doc[b["diapo"] - 1]
        lettre, bases = None, set()
        for bloc in page.get_text("dict")["blocks"]:
            for ligne in bloc.get("lines", []):
                for sp in ligne["spans"]:
                    if not sp["text"].strip():
                        continue
                    x0, y0 = mm(sp["bbox"][0]), mm(sp["bbox"][1])
                    base = mm(sp["origin"][1])
                    if x0 < b["x"] - 1 or x0 > b["x"] + b["w"] or not b["y"] - 12 < base < b["y"] + b["h"] + 12:
                        continue
                    if "YoungSerif" in sp["font"] and abs(sp["size"] - b["lettrine"]) < 0.3:
                        lettre = base
                    elif "Spectral" in sp["font"]:
                        bases.add(round(base, 1))
        if lettre is None or not bases:
            continue
        bases = sorted(bases)
        haut = lettre - 0.75 * b["lettrine"] * 25.4 / 72
        bas = bases[-1] + 0.25 * b["corps"] * 25.4 / 72
        res[int(n)] = {"lignes": len(bases), "ecart": lettre - bases[0],
                       "haut": b["y"] - MARGE_HAUT - haut, "bas": bas - (b["y"] + b["h"] + MARGE_BAS)}
    return res


# Les réglages, du plus généreux au plus sage. Une lettrine reste toujours visible
# (1,3 fois le corps au moins) ; on resserre l'interligne avant de la ramener au corps.
ETAPES = [(1.8, 1.42), (1.55, 1.42), (1.3, 1.42), (1.3, 1.36), (1.3, 1.30), (1.3, 1.25), (1.0, 1.25)]


def ecrire(etat, lignes):
    SORTIE.write_text(json.dumps({str(n): {"lettrine": ETAPES[i][0], **({"interligne": ETAPES[i][1]}
                                  if ETAPES[i][1] != 1.42 else {}), **({"lignes": lignes[n]} if n in lignes else {})}
                                  for n, i in sorted(etat.items())},
                                 indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    # les domaines qui ont une lettrine : ceux que le .pptx de l'édition a posés
    if not SORTIE.exists():
        SORTIE.write_text("{}\n", encoding="utf-8")
    subprocess.run(["node", "scripts/pptx.mjs"], cwd=RACINE, check=True, stdout=subprocess.DEVNULL)
    textes = sorted(int(n) for n in json.loads(BOITES.read_text(encoding="utf-8")))
    etat = {n: 0 for n in textes}
    lignes = {}
    for tour in range(1, 3 * len(ETAPES) + 1):
        ecrire(etat, lignes)
        m = mesurer(rendre())
        manquants = [n for n in textes if n not in m]
        if manquants:
            sys.exit(f"lettrine ou texte introuvable dans le rendu : n°{', '.join(map(str, manquants))}")
        recompte = [n for n in textes if lignes.get(n) != m[n]["lignes"]]
        fautifs = [n for n in textes if m[n]["haut"] > 0 or m[n]["bas"] > 0]
        decales = [n for n in textes if abs(m[n]["ecart"]) > 0.15]
        print(f"tour {tour} : {len(recompte)} recompte(s) de lignes, {len(fautifs)} débord(s)"
              + (" — " + ", ".join(f"n°{n} ({max(m[n]['haut'], m[n]['bas']):.1f} mm)" for n in fautifs) if fautifs else "")
              + (f" ; lettrine hors ligne de base : " + ", ".join(f"n°{n} ({m[n]['ecart']:+.2f} mm)" for n in decales)
                 if decales else ""))
        for n in textes:
            lignes[n] = m[n]["lignes"]
        bouges = 0
        if not recompte:            # les lignes sont justes : on peut juger les débords
            for n in fautifs:
                if etat[n] + 1 < len(ETAPES):
                    etat[n] += 1; bouges += 1
        if not recompte and not bouges:
            break
    ecrire(etat, lignes)
    ecart = max(abs(m[n]["ecart"]) for n in textes)
    print(f"→ {SORTIE.relative_to(RACINE)} ; lettrine à {ecart:.2f} mm au plus de la ligne de base"
          + (f" ; encore justes au dernier réglage : {', '.join(map(str, fautifs))}" if fautifs else ""))
    return 1 if fautifs or ecart > 0.15 else 0


if __name__ == "__main__":
    sys.exit(main())
