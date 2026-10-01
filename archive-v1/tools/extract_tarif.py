"""Lit l'ancien tarif Canva : source des textes, conditions de port, départements,
photos et logos. Les prix y sont dans des images : ils ne sont pas lus ici.
"""
import json, re, os
import pymupdf

SRC = "sources/tarif-2026-source.pdf"
OUT = "data/source-tarif.json"
IMGDIR = "assets/photos/source"

PORT_RE = re.compile(r"Prix de la bouteille H\.?T\.?\s*(.{0,90}?)"
                     r"(?=Distribution|Possibilit|\*|$)", re.I | re.S)
DEP_RE = re.compile(r"Distribution (?:sur|dans) les d[ée]partements\s*([\d,\s]+)", re.I)


def norm_port(brut):
    """Ramène les formulations de l'ancien tarif à une notation unique.

    « départ chai », « départ cave » et « hors frais de transport » disent la même
    chose côté caviste : le transport est en sus. On unifie, sans rien perdre :
    la formulation d'origine reste conservée dans `port_source`.
    """
    b = " ".join(brut.split()).rstrip(" .").lower()
    if not b:
        return {"type": "inconnu", "seuil": None}
    m = re.search(r"(?:à partir de|dès)\s*(\d+)", b)
    if m and "franco" in b:
        return {"type": "franco_seuil", "seuil": int(m.group(1))}
    if "franco" in b:
        return {"type": "franco", "seuil": None}
    if any(k in b for k in ("hors frais", "départ chai", "départ cave", "depart")):
        return {"type": "port_en_sus", "seuil": None}
    return {"type": "inconnu", "seuil": None}


def main():
    doc = pymupdf.open(SRC)
    os.makedirs(IMGDIR, exist_ok=True)
    fiches, images = [], []

    for pg in range(doc.page_count):
        page = doc[pg]
        raw = page.get_text()
        plat = " ".join(raw.split())
        num = re.search(r"-\s*(\d{1,2})\s*-", plat)
        if not num:
            continue
        mp, md = PORT_RE.search(plat), DEP_RE.search(plat)
        brut = mp.group(1).strip() if mp else ""
        # le texte de présentation : ce qui reste une fois ôtés en-tête et pied
        corps = plat
        for pat in (r"\*?\s*Prix de la bouteille.*$", r"Distribution (?:sur|dans).*$",
                    r"-\s*\d{1,2}\s*-"):
            corps = re.sub(pat, " ", corps)
        fiches.append({
            "numero": int(num.group(1)),
            "page_source": pg + 1,
            "port_source": brut or None,
            "port": norm_port(brut),
            "departements": [d.strip() for d in md.group(1).split(",") if d.strip()] if md else [],
            "texte_source": " ".join(corps.split())[:1200],
        })

        for i, info in enumerate(page.get_images(full=True)):
            xref = info[0]
            try:
                px = pymupdf.Pixmap(doc, xref)
            except Exception:
                continue
            nom = f"p{pg+1:02d}-{i:02d}-x{xref}.png"
            if px.n - px.alpha >= 4:
                px = pymupdf.Pixmap(pymupdf.csRGB, px)
            if px.width < 40 or px.height < 40:
                continue                       # pastilles et filets, sans intérêt
            px.save(os.path.join(IMGDIR, nom))
            images.append({"fichier": nom, "page_source": pg + 1,
                           "fiche": int(num.group(1)), "px_l": px.width, "px_h": px.height,
                           "mm_300dpi": round(px.width * 25.4 / 300, 1),
                           "mm_200dpi": round(px.width * 25.4 / 200, 1)})

    json.dump({"source": SRC, "fiches": fiches, "images": images},
              open(OUT, "w"), ensure_ascii=False, indent=1)

    print(f"fiches lues : {len(fiches)} | images extraites : {len(images)}")
    from collections import Counter
    print("\nrépartition des conditions de port (normalisées) :")
    for k, v in Counter(f["port"]["type"] for f in fiches).most_common():
        print(f"   {k:<14} {v}")
    print("\ndomaines sans mention de port dans la source :",
          [f["numero"] for f in fiches if f["port"]["type"] == "inconnu"])
    trop_petit = [i for i in images if i["mm_300dpi"] < 60]
    print(f"\nimages < 60 mm à 300 dpi (donc limitées en impression) : "
          f"{len(trop_petit)} sur {len(images)}")
    gros = sorted(images, key=lambda i: -i["px_l"] * i["px_h"])[:5]
    print("les 5 plus grandes :",
          [(g["fichier"], f"{g['px_l']}x{g['px_h']}", f"{g['mm_300dpi']}mm") for g in gros])


if __name__ == "__main__":
    main()
