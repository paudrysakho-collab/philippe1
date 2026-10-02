#!/usr/bin/env python3
"""Règle la taille de la lettrine du .pptx, domaine par domaine.

Dans le PDF, la lettrine tombe sur deux lignes (CSS). Un .pptx ne sait pas le faire : la
lettrine y monte au-dessus de la première ligne, qu'elle rend plus haute. Sur les textes
les plus longs, cette ligne de plus ferait toucher le texte au tableau de prix. Ce script
fabrique le .pptx, le fait rendre par LibreOffice, mesure chaque bloc de texte, et réduit
la lettrine des seuls domaines qui débordent, jusqu'à ce qu'aucun ne déborde.

    python3 scripts/regler-lettrines.py      écrit src/gabarits/lettrines-pptx.json

Demande LibreOffice (soffice) et PyMuPDF (pip install pymupdf). À relancer seulement si les
textes des domaines changent ; `npm run pptx` se contente de lire le fichier écrit.
"""
import json, pathlib, shutil, subprocess, sys, tempfile
import pymupdf

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "src/gabarits/lettrines-pptx.json"
PPTX = RACINE / "dist/catalogue-scio-2026-canva.pptx"
BOITES = RACINE / "build/pptx-textes.json"
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
    """n° → (débord en haut, débord en bas), en mm ; positif = le texte sort de sa place."""
    boites = json.loads(BOITES.read_text(encoding="utf-8"))
    doc = pymupdf.open(pdf)
    debords = {}
    for n, b in boites.items():
        page = doc[b["diapo"] - 1]
        haut, bas = None, None
        for bloc in page.get_text("dict")["blocks"]:
            for ligne in bloc.get("lines", []):
                for sp in ligne["spans"]:
                    if not sp["text"].strip():
                        continue
                    if not ("Spectral" in sp["font"] or "YoungSerif" in sp["font"]):
                        continue
                    x0, y0, x1, y1 = (mm(v) for v in sp["bbox"])
                    if x0 < b["x"] - 1 or x0 > b["x"] + b["w"]:
                        continue
                    if y1 < b["y"] - 12 or y0 > b["y"] + b["h"] + 12:
                        continue
                    if "YoungSerif" in sp["font"] and sp["size"] > 18 and y0 < b["y"] - 9:
                        continue        # le titre du domaine
                    haut = y0 if haut is None else min(haut, y0)
                    bas = y1 if bas is None else max(bas, y1)
        if haut is None:
            continue
        debords[int(n)] = (b["y"] - MARGE_HAUT - haut, bas - (b["y"] + b["h"] + MARGE_BAS))
    return debords


# Les réglages, du plus généreux au plus sage. Une lettrine reste toujours visible
# (1,3 fois le corps au moins) ; on resserre l'interligne avant de la ramener au corps.
ETAPES = [(1.8, 1.42), (1.55, 1.42), (1.3, 1.42), (1.3, 1.36), (1.3, 1.30), (1.3, 1.25), (1.0, 1.25)]


def ecrire(etat):
    SORTIE.write_text(json.dumps({str(n): {"lettrine": ETAPES[i][0], **({"interligne": ETAPES[i][1]}
                                  if ETAPES[i][1] != 1.42 else {})} for n, i in sorted(etat.items())},
                                 indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    textes = [int(p.stem) for p in sorted((RACINE / "data/fiches").glob("*.json"))
              if json.loads(p.read_text(encoding="utf-8")).get("texte_source")]
    etat = {n: 0 for n in textes}
    fautifs = []
    for tour in range(1, len(ETAPES) + 1):
        ecrire(etat)
        debords = mesurer(rendre())
        fautifs = [n for n, (h, b) in debords.items() if (h > 0 or b > 0) and n in etat]
        print(f"tour {tour} : {len(fautifs)} domaine(s) qui débordent" +
              (" — " + ", ".join(f"n°{n} ({max(debords[n]):.1f} mm, lettrine ×{ETAPES[etat[n]][0]}, "
                                 f"interligne {ETAPES[etat[n]][1]})" for n in fautifs) if fautifs else ""))
        bouges = 0
        for n in fautifs:
            if etat[n] + 1 < len(ETAPES):
                etat[n] += 1; bouges += 1
        if not bouges:
            break
    ecrire(etat)
    print(f"→ {SORTIE.relative_to(RACINE)}"
          + (f" ; encore justes au dernier réglage : {', '.join(map(str, fautifs))}" if fautifs else ""))


if __name__ == "__main__":
    sys.exit(main())
