#!/usr/bin/env python3
"""Écrit `data/catalogue-restaurant-a-trouver.md` : la liste, domaine par domaine, des vins
du catalogue restaurant dont le prix n'est pas encore relevé — pour que l'agence les cherche.

    python3 scripts/liste-prix-manquants.py
"""
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "data/catalogue-restaurant-a-trouver.md"


def lire(nom):
    return json.loads((RACINE / nom).read_text(encoding="utf-8"))


def etiquette(v):
    bits = [v["cuvee"] or v["appellation"]]
    if v["cuvee"] and v["appellation"] and v["appellation"] not in v["cuvee"]:
        bits.append(f"— {v['appellation']}")
    extra = [v["couleur"]]
    if v["millesime"] and v["millesime"] != "—":
        extra.append(v["millesime"])
    if v["contenance"] != "75 cl":
        extra.append(v["contenance"])
    return " ".join(bits) + " (" + ", ".join(x for x in extra if x) + ")"


def main():
    cat = lire("data/catalogue.json")
    noms = {d["numero"]: d["nom"] for d in cat["domaines"]}
    glob = lire("data/catalogue-global-2026.json")
    for d in glob["domaines_ajoutes"]:
        noms[d["numero"]] = d["nom"]
    r = lire("data/catalogue-restaurant-2026.json")
    plan = lire("build/catalogue-restaurant-2026-plan.json")["domaines"]

    def stand(n):
        return next((s for s in r["stands"] if any(v["fiche"] == n for v in s["vins"])), None)

    def paliers(st, n):
        return (st["paliers_salon"].get(str(n))
                or next((p for k, p in st["paliers_salon"].items() if k.split(":")[0] == str(n)), []))

    L = []
    w = L.append
    w("# Catalogue restaurant : les prix qui manquent, domaine par domaine")
    w("")
    w("Pour chaque domaine : sa page dans le catalogue restaurant, ses colonnes, puis les vins")
    w("dont le prix restaurant n'est pas relevé. Il suffit de donner le prix de chaque ligne.")
    w("")
    total = 0
    for n in glob["ordre"]:
        st = stand(n)
        if not st:
            continue
        vins = [v for v in st["vins"] if v["fiche"] == n]
        manque = [v for v in vins if all(x is None for x in v["prix_centimes"])]
        if not manque:
            continue
        total += len(manque)
        pal = [p.replace("Prix salon", "Prix") for p in paliers(st, n)]
        w(f"## p.{plan[str(n)]} — {noms[n]} ({len(manque)} vin{'s' if len(manque) > 1 else ''})")
        w("")
        w(f"Colonnes : {' / '.join(pal)}")
        w("")
        for v in manque:
            w(f"- {etiquette(v)}")
        w("")
    w(f"**{total} vins en tout.**")
    w("")
    w("## Et quelques colonnes isolées")
    w("")
    w("Ces lignes ont déjà un prix, mais pas dans toutes les colonnes (le tarif met « – »).")
    w("")
    for n in glob["ordre"]:
        st = stand(n)
        if not st:
            continue
        pal = paliers(st, n)
        for v in st["vins"]:
            if v["fiche"] != n:
                continue
            pc = v["prix_centimes"]
            if len(pc) > 1 and any(x is None for x in pc) and any(x is not None for x in pc):
                cols = ", ".join(pal[i] for i, x in enumerate(pc) if x is None and i < len(pal))
                w(f"- p.{plan[str(n)]} {noms[n]} — {etiquette(v)} : il manque **{cols}**")
    SORTIE.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {total} vins sans prix")


if __name__ == "__main__":
    main()
