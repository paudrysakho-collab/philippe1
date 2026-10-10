#!/usr/bin/env python3
"""Écrit `data/catalogue-restaurant-manque.md` : tout ce qui manque au catalogue restaurant
pour que les prix et les minimums de commande soient complets.

    python3 scripts/manque-restaurant.py
"""
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "data/catalogue-restaurant-manque.md"

SANS_TARIF = {7, 33, 43}                            # aucune page dans les deux dossiers
RAISONS = {
    (41, "Sancerre Rosé"): "ligne **barrée en rouge** sur le tarif, mais ses prix y sont écrits "
                           "(10,60 / 10,30 / 10,00) — à trancher",
    (3, "Rouge aux lèvres"): "le catalogue C.H.R. du domaine n'a été scanné que sur deux pages",
    (3, "La Perle"): "le catalogue C.H.R. du domaine n'a été scanné que sur deux pages",
    (6, "AOC Menetou-Salon Rouge"): "le tarif n'a que le Menetou-Salon **blanc**",
    (6, "IGP Chenin Blanc"): "absent du tarif restaurant (ajouté au caviste le 9 octobre)",
    (12, "AOC Pouilly-Vinzelles Blanc"): "absent du portfolio restaurant (il a le Pouilly-Fuissé, pas le Vinzelles)",
    (23, "N°10 Pétillant"): "absent de la page restaurant",
    (29, "Château Balac Rouge"): "« Rajouter Balac » est écrit, mais le courriel ne donne pas ses prix",
    (32, "Chant de Lune Rouge, disponible en décembre 2026"): "le tarif n'a pas de ligne magnum",
}


def main():
    cat = json.loads((RACINE / "data/catalogue.json").read_text(encoding="utf-8"))
    noms = {d["numero"]: d["nom"] for d in cat["domaines"]}
    glob = json.loads((RACINE / "data/catalogue-global-2026.json").read_text(encoding="utf-8"))
    for d in glob["domaines_ajoutes"]:
        noms[d["numero"]] = d["nom"]
    r = json.loads((RACINE / "data/catalogue-restaurant-2026.json").read_text(encoding="utf-8"))
    plan = json.loads((RACINE / "build/catalogue-restaurant-2026-plan.json").read_text(encoding="utf-8"))["domaines"]

    def fiches():
        for n in glob["ordre"]:
            st = next((s for s in r["stands"] if any(v["fiche"] == n for v in s["vins"])), None)
            if st:
                yield n, st, [v for v in st["vins"] if v["fiche"] == n]

    def desc(v):
        bout = " · ".join(x for x in [v["appellation"], v["couleur"],
                                      v["millesime"] if v["millesime"] != "—" else None,
                                      v["contenance"]] if x)
        return f"{v['cuvee'] or v['appellation']} ({bout})"

    L = []
    w = L.append
    w("# Catalogue restaurant : ce qui manque pour que prix et quantités soient bons")
    w("")
    w("Écrit par `scripts/manque-restaurant.py`. Référence : le **catalogue caviste 85**")
    w("(`dist/catalogue-caviste-2026-ecran.pdf`) — mêmes domaines, mêmes vins, mêmes textes ;")
    w("**seuls les minimums de commande (les colonnes) et les prix changent**. Sur les tarifs")
    w("annotés, on prend **le prix qui est écrit**, surligné ou non (l'agence, 10 octobre).")
    w("")
    poses = sum(len([x for x in v["prix_centimes"] if x is not None]) for _, _, vs in fiches() for v in vs)
    vides = sum(len([x for x in v["prix_centimes"] if x is None]) for _, _, vs in fiches() for v in vs)
    w(f"**État : {poses} prix posés, {vides} cases encore vides.**")
    w("")
    w("## 1. Les quatre fiches sans aucun prix restaurant")
    w("")
    w("| Page | Domaine | Lignes sans prix | Ce qu'il manque |")
    w("|---|---|---|---|")
    for n, st, vs in fiches():
        if n in SANS_TARIF or n == 9:
            v0 = [v for v in vs if all(x is None for x in v["prix_centimes"])]
            quoi = ("les prix : le tarif scanné ne donne que les BIB et une « sélection restaurant » "
                    "(Brouilly, Crémant, Mâcon-Villages…), aucun vin de la fiche"
                    if n == 9 else "les minimums de commande **et** les prix : aucune page scannée")
            w(f"| p.{plan[str(n)]} | **{noms[n]}** | {len(v0)} / {len(vs)} | {quoi} |")
    w("")
    w("## 2. Les lignes isolées sans prix")
    w("")
    w("| Page | Domaine | Ligne | Pourquoi |")
    w("|---|---|---|---|")
    for n, st, vs in fiches():
        if n in SANS_TARIF or n == 9:
            continue
        for v in vs:
            if all(x is None for x in v["prix_centimes"]):
                c = v["cuvee"] or v["appellation"]
                pourquoi = RAISONS.get((n, c))
                if pourquoi is None:
                    if v["contenance"] in ("1,5 L", "Magnum 1,5 L"):
                        pourquoi = "le tarif restaurant n'a pas de ligne magnum"
                    elif v["contenance"] == "BIB":
                        pourquoi = "le catalogue C.H.R. du domaine n'a été scanné que sur deux pages"
                    else:
                        pourquoi = "absente du tarif restaurant"
                w(f"| p.{plan[str(n)]} | {noms[n]} | {desc(v)} | {pourquoi} |")
    w("")
    w("## 3. Les colonnes incomplètes (la ligne a un prix, mais pas partout)")
    w("")
    w("| Page | Domaine | Ligne | Colonnes manquantes | Pourquoi |")
    w("|---|---|---|---|---|")
    for n, st, vs in fiches():
        pal = st["paliers_salon"].get(str(n)) or next(
            (p for k, p in st["paliers_salon"].items() if k.split(":")[0] == str(n)), [])
        for v in vs:
            pc = v["prix_centimes"]
            if len(pc) > 1 and any(x is None for x in pc) and any(x is not None for x in pc):
                manque = ", ".join(pal[i] for i, x in enumerate(pc) if x is None and i < len(pal))
                w(f"| p.{plan[str(n)]} | {noms[n]} | {desc(v)} | {manque} | le tarif met « – » dans ces colonnes |")
    w("")
    w("## 4. Les minimums de commande (colonnes)")
    w("")
    w("**39 fiches sur 42** ont leurs colonnes relevées sur un tarif restaurant. Trois gardent")
    w("celles du catalogue caviste, faute de tarif : **Divin No Low**, **les jus de cépages de la")
    w("Famille d'Exea** et **le Mas des Restanques**.")
    w("")
    w("Deux choix à confirmer :")
    w("")
    w("- **Stratéus** : la grille va de 24 à 300 bouteilles et ne dit pas lesquelles garder.")
    w("  Pris **24 / 48 / 120 bts**. La gamme Koloss n'a pas de prix à 48 bts (le tarif met « / »).")
    w("- **Vazart-Coquart** : les colonnes s'appellent **« Par 24 / Par 48 / Par 78 »** sur le tarif,")
    w("  gardées telles quelles.")
    w("")
    w("## 5. Les offres")
    w("")
    w("Toutes les offres sont encore celles du catalogue caviste, sauf **Chai Berteaud Manceau**")
    w("(« Offre 11+1 à partir de 60 cols », écrite à la main sur le scan). L'agence les reprend")
    w("une par une.")
    SORTIE.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {poses} prix posés, {vides} cases vides")


if __name__ == "__main__":
    main()
