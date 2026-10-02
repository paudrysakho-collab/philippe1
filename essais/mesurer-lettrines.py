"""Mesure le calage des lettrines dans un PDF : un export PDF de Canva (les 40 premières pages
de fiche seulement, dans l'ordre) ou un rendu LibreOffice du .pptx entier.

    python3 essais/mesurer-lettrines.py export-canva.pdf

Pour chaque domaine : écart entre la ligne de base de la lettrine et celle de la première
ligne, et blanc entre la lettrine et le premier caractère qui la suit. Lit
build/pptx-textes.json, écrit par scripts/pptx.mjs."""
import json, pathlib, sys, pymupdf
b = json.load(open(pathlib.Path(__file__).resolve().parent.parent / "build/pptx-textes.json"))
pages = sorted(b.items(), key=lambda kv: kv[1]["diapo"])
doc = pymupdf.open(sys.argv[1])
mm = lambda v: v / 72 * 25.4
pire, blancs = 0, []
for i, (n, bo) in enumerate(pages):
    page = doc[i] if len(doc) == len(pages) else doc[bo["diapo"] - 1]
    lettre = None; chars = []
    for bl in page.get_text("rawdict")["blocks"]:
        for l in bl.get("lines", []):
            for sp in l["spans"]:
                base = mm(sp["origin"][1])
                vis = [c for c in sp["chars"] if c["c"].strip() and c["c"] != "\xa0"]
                if not vis: continue
                x0 = mm(vis[0]["bbox"][0])
                if x0 < bo["x"] - 1 or x0 > bo["x"] + bo["w"] or not bo["y"] - 14 < base < bo["y"] + bo["h"] + 14:
                    continue
                if abs(sp["size"] - bo["lettrine"]) < 0.6 and len(vis) == 1:
                    lettre = (base, mm(vis[0]["bbox"][2]), sp["font"])
                elif abs(sp["size"] - bo["corps"]) < 0.3:
                    chars += [(mm(c["origin"][1]), mm(c["bbox"][0]), sp["font"]) for c in vis]
    if lettre is None or not chars:
        print(f"n°{n}: introuvable"); continue
    b1 = min(c[0] for c in chars)
    l1 = [c for c in chars if abs(c[0] - b1) < 0.3]
    blanc = min(c[1] for c in l1) - lettre[1]
    ecart = lettre[0] - b1
    pire = max(pire, abs(ecart)); blancs.append(blanc)
    print(f"n°{n:>2} diapo {bo['diapo']:>2}  lettrine {bo['lettrine']:>5} pt ({lettre[2]})  écart ligne de base {ecart:+.2f} mm  blanc {blanc:+.2f} mm  ({l1[0][2]})")
print(f"pire écart de ligne de base : {pire:.2f} mm ; blanc de {min(blancs):.2f} à {max(blancs):.2f} mm")
