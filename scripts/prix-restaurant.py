#!/usr/bin/env python3
"""Le catalogue restaurant : le catalogue caviste, avec les paliers et les prix du tarif
restaurant.

L'agence (9 octobre 2026) : « on prend les mêmes noms, c'est juste les prix qui vont
différencier et les colonnes, les quantités ». On repart donc de
`data/catalogue-global-2026.json` — mêmes fiches, mêmes vins, mêmes textes, mêmes photos —
et on n'y change que deux choses :

- **les paliers** (`PALIERS`), relevés sur les tarifs annotés du dossier
  `sources/catalogue-restaurant-2026/tarifs-restaurant-annotes.pdf` (relevé ligne à ligne
  dans `data/catalogue-restaurant-releve.md`) ;
- **les prix** (`PRIX`), relevés sur les mêmes tarifs.

Un vin dont le prix restaurant n'est pas encore relevé garde **une case vide** par palier :
le tableau sait l'afficher, et l'agence le remplit ensuite. Un prix ne s'invente jamais.

    python3 scripts/prix-restaurant.py     écrit data/catalogue-restaurant-2026.json
"""
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / "data/catalogue-global-2026.json"
SORTIE = RACINE / "data/catalogue-restaurant-2026.json"
RELEVE = "tarif restaurant annoté par l'agence (dossier du 9 octobre 2026)"


def eu(*prix):
    """« 5,80 » → 580 centimes ; None laisse la case vide."""
    return [None if p is None else round(float(p.replace(",", ".")) * 100) for p in prix]


def P(*quantites, unite="bts"):
    return [f"À partir de {q} {unite}" for q in quantites]


# ——————————————————————————————————————————————— les paliers du tarif restaurant ———
# Clé : « fiche » (tous ses tableaux) ou « fiche:tableau ». Relevés sur les tarifs annotés.
PALIERS = {}

# ——————————————————————————————————————————————————— les prix du tarif restaurant ———
# Clé : (fiche, cuvée ou appellation si le vin n'a pas de cuvée) → un prix par palier.
PRIX = {}

# ——————————————————————————————————————————————————————————————— les offres ———
# L'agence les reprend une par une (« je changerai les offres, page 1, page 2… ») :
# tant qu'elle ne les a pas données, la fiche garde l'offre du catalogue caviste.
OFFRES = {}


def cle_vin(v):
    return (v["fiche"], v["cuvee"] or v["appellation"])


def main():
    cat = json.loads(SOURCE.read_text(encoding="utf-8"))
    cat["edition"] = "Catalogue restaurant 2026"
    vides = 0
    poses = 0
    for s in cat["stands"]:
        for n in s.get("domaines") or []:
            if n in OFFRES:
                s["offre_salon"] = OFFRES[n]
        # les paliers : ceux du tarif restaurant quand on les a relevés
        paliers = dict(s.get("paliers_salon") or {})
        for cle, p in PALIERS.items():
            tete = str(cle).split(":")[0]
            if any(str(v["fiche"]) == tete for v in s["vins"]):
                paliers[str(cle)] = p
        s["paliers_salon"] = paliers
        for v in s["vins"]:
            # combien de colonnes ce vin a-t-il dans l'édition restaurant ?
            ti = (v.get("tarif") or {}).get("tableau", 0)
            p = paliers.get(f"{v['fiche']}:{ti}") or paliers.get(str(v["fiche"]))
            n = len(p) if p else len(v.get("prix_centimes") or [1])
            prix = PRIX.get(cle_vin(v))
            if prix is None:
                v["prix_centimes"] = [None] * n       # case vide, à remplir par l'agence
                vides += n
            else:
                v["prix_centimes"] = prix
                v["prix_source"] = RELEVE
                poses += len([x for x in prix if x is not None])
    SORTIE.write_text(json.dumps(cat, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {len(cat['ordre'])} fiches, "
          f"{poses} prix relevés, {vides} cases encore vides")


if __name__ == "__main__":
    main()
