"""Extrait les images de la maquette 52 pages et les inventorie par fiche.

La maquette est une meilleure source visuelle que l'ancien tarif : ses images y sont
souvent plus grandes (jusqu'à 1883 × 2353 px, contre 1241 px au mieux dans le tarif).
"""
import json, os
import pymupdf

SRC = "sources/maquette-52p.pdf"
DST = "assets/photos/maquette"
OUT = "data/images-maquette.json"

# pages de suite : elles appartiennent à la fiche précédente
SUITE = {18: 12, 30: 23, 33: 25, 41: 32}


def fiche_de(pg):
    if pg in SUITE:
        return SUITE[pg]
    if 6 <= pg <= 49:
        n = pg - 5
        for s in sorted(SUITE):
            if pg > s:
                n -= 1
        return n
    return None


def main():
    os.makedirs(DST, exist_ok=True)
    doc = pymupdf.open(SRC)
    vus, images = set(), []
    for pg in range(1, doc.page_count + 1):
        for info in doc[pg - 1].get_images(full=True):
            x = info[0]
            if x in vus:
                continue
            vus.add(x)
            try:
                px = pymupdf.Pixmap(doc, x)
            except Exception:
                continue
            if px.width < 100 or px.height < 100:
                continue
            if px.n - px.alpha >= 4:
                px = pymupdf.Pixmap(pymupdf.csRGB, px)
            nom = f"m{pg:02d}-x{x}-{px.width}x{px.height}.png"
            px.save(os.path.join(DST, nom))
            images.append({
                "fichier": nom, "page": pg, "fiche": fiche_de(pg),
                "l": px.width, "h": px.height,
                "ratio": round(px.width / px.height, 2),
                # résolution utile aux deux largeurs du gabarit
                "dpi_a_110mm": round(px.width / (110 / 25.4)),
                "dpi_a_66mm": round(px.width / (66 / 25.4)),
            })
    json.dump({"source": SRC, "images": images}, open(OUT, "w"),
              ensure_ascii=False, indent=1)
    print(f"{len(images)} images extraites vers {DST}")
    for n in (3, 32, 40):
        print(f"\nfiche {n} :")
        for i in [i for i in images if i["fiche"] == n]:
            r = "paysage" if i["ratio"] > 1.2 else ("vertical" if i["ratio"] < 0.85 else "carré")
            print(f"   {i['fichier']:<28} {r:<8} {i['dpi_a_110mm']:>4} dpi à 110 mm | "
                  f"{i['dpi_a_66mm']:>4} dpi à 66 mm")
    print("\nmeilleures images paysage du document (couverture) :")
    for i in sorted([i for i in images if i["ratio"] > 1.3], key=lambda i: -i["l"])[:5]:
        print(f"   {i['fichier']:<28} p{i['page']:<3} {i['l']}x{i['h']} → "
              f"{round(i['l']/(210/25.4))} dpi en pleine largeur A4, "
              f"{round(i['l']/(210/25.4))} dpi en bandeau")


if __name__ == "__main__":
    main()
