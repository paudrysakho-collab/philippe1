"""Trie les images extraites de l'ancien tarif et choisit celles de chaque fiche.

L'extraction ramène pêle-mêle des photographies, des logos et des CAPTURES D'ÉCRAN
des tableaux Excel. Ces dernières ne doivent jamais servir d'illustration — mais
elles sont précieuses pour la double lecture des prix, on les range à part.
"""
import json, os
from collections import defaultdict
from PIL import Image

SRC = "assets/photos/source"
OUT = "data/inventaire-images.json"
DPI_MINI = 200          # en dessous, la photo part dans « à remplacer »


def analyse(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    p = im.resize((60, 60))
    px = list(p.getdata())
    blancs = sum(1 for r, g, b in px if r > 235 and g > 235 and b > 235) / len(px)
    gris = sum(1 for r, g, b in px if max(r, g, b) - min(r, g, b) < 14) / len(px)
    teintes = len({(r // 32, g // 32, b // 32) for r, g, b in px})
    return {"l": w, "h": h, "ratio": round(w / h, 2), "blancs": round(blancs, 2),
            "gris": round(gris, 2), "teintes": teintes}


def classe(a):
    """Capture de tableau, logo, ou photographie."""
    # une capture de tableau : beaucoup de blanc, peu de teintes, très large
    if a["blancs"] > 0.34 and a["teintes"] <= 22 and a["ratio"] > 1.7:
        return "capture_tableau"
    if a["blancs"] > 0.55 and a["teintes"] <= 26:
        return "logo"
    if a["l"] < 260 and a["h"] < 260 and a["blancs"] > 0.3:
        return "logo"
    return "photo"


def main():
    tar = json.load(open("data/source-tarif.json"))
    par_fiche = defaultdict(list)
    for im in tar["images"]:
        p = os.path.join(SRC, im["fichier"])
        if not os.path.exists(p):
            continue
        a = analyse(p)
        rec = {**im, **a, "type": classe(a)}
        rec["dpi_a_108mm"] = round(rec["l"] / (108 / 25.4))
        rec["dpi_a_58mm"] = round(rec["l"] / (58 / 25.4))
        par_fiche[im["fiche"]].append(rec)

    choix, a_remplacer = {}, []
    for n, ims in par_fiche.items():
        photos = [i for i in ims if i["type"] == "photo"]
        logos = [i for i in ims if i["type"] == "logo"]
        paysages = sorted([i for i in photos if i["ratio"] >= 1.15],
                          key=lambda i: -i["l"])
        autres = sorted([i for i in photos if i["ratio"] < 1.15], key=lambda i: -i["l"])
        ambiance = paysages[0] if paysages else (autres[0] if autres else None)
        reste = [i for i in photos if i is not ambiance]
        second = sorted(reste, key=lambda i: -i["l"])[0] if reste else None
        logo = sorted(logos, key=lambda i: -i["l"])[0] if logos else None
        choix[n] = {"ambiance": ambiance, "second": second, "logo": logo,
                    "captures": [i["fichier"] for i in ims if i["type"] == "capture_tableau"]}
        for role, im, larg in (("ambiance", ambiance, 108), ("second", second, 58)):
            if im and im[f"dpi_a_{larg}mm"] < DPI_MINI:
                a_remplacer.append({"fiche": n, "role": role, "fichier": im["fichier"],
                                    "px": f"{im['l']}x{im['h']}",
                                    "dpi": im[f"dpi_a_{larg}mm"]})
            if im is None:
                a_remplacer.append({"fiche": n, "role": role, "fichier": None,
                                    "px": None, "dpi": 0})

    json.dump({"par_fiche": {str(k): v for k, v in choix.items()},
               "a_remplacer": a_remplacer, "dpi_mini": DPI_MINI},
              open(OUT, "w"), ensure_ascii=False, indent=1)

    from collections import Counter
    tous = [i for v in par_fiche.values() for i in v]
    print("classement des", len(tous), "images :", dict(Counter(i["type"] for i in tous)))
    print(f"captures de tableaux mises de côté pour la double lecture : "
          f"{sum(len(c['captures']) for c in choix.values())}")
    print(f"photos sous {DPI_MINI} dpi ou manquantes (liste « à remplacer ») : {len(a_remplacer)}")
    for n in (3, 32, 40):
        c = choix.get(n, {})
        print(f"\nfiche {n} :")
        for r in ("ambiance", "second", "logo"):
            im = c.get(r)
            print(f"   {r:<9} " + (f"{im['fichier']:<22} {im['l']}x{im['h']} "
                                   f"ratio {im['ratio']} blancs {im['blancs']} "
                                   f"teintes {im['teintes']}" if im else "— aucune"))
        print(f"   captures : {c.get('captures')}")


if __name__ == "__main__":
    main()
