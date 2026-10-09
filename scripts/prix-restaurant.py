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
# Clé : « fiche » (tous ses tableaux) ou « fiche:tableau ». Relevés sur les tarifs annotés
# (scan indiqué en commentaire ; les scans 37 à 51 du dossier sont des doublons des 1 à 15).
PALIERS = {
    1: ["Jusqu'à 36 bts", "De 37 à 119 bts"],            # François Reverdy, scan 3
    41: P(36, 72, 144),                                  # Domaine des Sardelles, scans 4 et 5
    # Les quatre domaines Strasser Radziwill (scans 24 à 28) : le tarif restaurant a cinq
    # colonnes (36-72, 78-120, 120-240, ≥ 240 cols, 1 palette). On garde les trois premières,
    # les plus petits volumes, comme partout ailleurs dans le catalogue.
    16: ["De 36 à 72 cols", "De 78 à 120 cols", "De 120 à 240 cols"],
    17: ["De 36 à 72 cols", "De 78 à 120 cols", "De 120 à 240 cols"],
    18: ["De 36 à 72 cols", "De 78 à 120 cols", "De 120 à 240 cols"],
    19: ["De 36 à 72 cols", "De 78 à 120 cols", "De 120 à 240 cols"],
    # Domaine du Colombier (scans 8 et 9) : il a son propre « CATALOGUE C.H.R. et TARIF
    # FRANCO H.T ». Les bag-in-box n'y figurent pas : leur tableau garde ses 5 L / 10 L.
    "3:0": ["Minimum 60 bts", "Minimum 120 bts", "Minimum 240 bts"],
    2: P(24, 60, 120),                                   # Domaine de la Barbinière, scans 6 et 7
}

# ——————————————————————————————————————————————————— les prix du tarif restaurant ———
# Clé : (fiche, cuvée ou appellation si le vin n'a pas de cuvée) → un prix par palier.
PRIX = {
    # ——— François Reverdy (scan 3) : colonnes « jusqu'à 36 » et « de 37 à 119 » ;
    # les colonnes 120 et 300 sont rayées.
    (1, "AOC Anjou Blanc"): eu("14,75", "13,25"),
    (1, "La Grange Jaumain Blanc"): eu("10,00", "9,50"),
    (1, "AOC Saumur Blanc"): eu("16,00", "14,50"),
    (1, "AOC Quincy"): eu("19,95", "17,85"),
    (1, "Les Villaudes"): eu("19,00", "18,00"),
    (1, "La Grange Jaumain Rouge – Grolleau Noir"): eu("10,60", "10,60"),
    (1, "Franc Rouge"): eu("14,75", "13,75"),
    (1, "Cravant Rouge"): eu("18,00", "17,00"),
    (1, "La Grange Jaumain Les Soudannes Rouge"): eu("10,00", "9,50"),

    # ——— Domaine des Sardelles (scans 4 et 5) : 36 / 72 / 144 ; la colonne 288 est rayée.
    (41, "Sancerre Blanc"): eu("13,50", "13,20", "12,90"),
    (41, "Sancerre Blanc « La Cabane »"): eu("17,00", "16,70", "16,40"),
    (41, "Sancerre Rouge"): eu("13,50", "13,20", "12,90"),
    (41, "Pouilly-Fumé"): eu("12,10", "11,80", "11,50"),
    (41, "Les Courants Sauvignon Blanc"): eu("5,80", "5,50", "5,20"),
    (41, "Les Courants Rouge Gamay"): eu("5,80", "5,50", "5,20"),
    (41, "Les Courants Pinot Noir"): eu("5,80", "5,50", "5,20"),

    # ——— Domaine de Coyeux (scan 26)
    (17, "Premières Fleurs Blanc"): eu("6,50", "6,00", "5,50"),
    (17, "Premières Fleurs Rouge"): eu("6,50", "6,00", "5,50"),
    (17, "Or des Dentelles Blanc Moelleux", "75 cl"): eu("8,90", "8,40", "7,90"),
    (17, "Or des Dentelles Blanc Moelleux", "37,5 cl"): eu("5,30", "5,00", "4,70"),
    (17, "Les Jumelles Rouge"): eu("7,50", "7,00", "6,50"),

    # ——— Domaine Le Prieuré des Papes (scan 24) : les colonnes 36-72, 78-120 et 126-240 sont
    # surlignées, les deux dernières (246 cols et palette) rayées. Les deux lignes « Vieilles
    # Vignes » du tarif portent le même prix.
    (16, "Le Prieuré Rouge"): eu("6,70", "6,20", "5,70"),
    (16, "Vieilles Vignes Rouge"): eu("19,00", "18,50", "18,00"),
    (16, "Le Couchant Rouge"): eu("28,00", "27,50", "27,00"),

    # ——— Domaine du Moulin Blanc (scan 27)
    (18, "Côtes du Rhône Rouge"): eu("6,70", "6,20", "5,70"),

    # ——— Domaine de la Pousterle (scan 28)
    (19, "Chardonnay-Viognier Blanc"): eu("5,50", "5,00", "4,80"),
    (19, "Syrah Rouge"): eu("5,50", "5,00", "4,80"),
    (19, "Terroir d\u2019Ansouis Blanc"): eu("6,50", "6,00", "5,50"),
    (19, "Terroir d\u2019Ansouis Rouge"): eu("6,50", "6,00", "5,50"),

    # ——— Domaine du Colombier (scans 8 et 9), tarif C.H.R. : 60 / 120 / 240 bouteilles.
    # « Rouge aux lèvres », « La Perle » et les bag-in-box n'y figurent pas : cases vides.
    (3, "Cuvée des deux Colombes"): eu("4,80", "4,60", "4,35"),
    (3, "L\u2019Envol"): eu("5,90", "5,60", "5,30"),
    (3, "Cru Mouzillon-Tillières"): eu("10,00", "9,50", "9,10"),
    (3, "Le Prestige de Beaulieu"): eu("5,00", "4,75", "4,50"),
    (3, "Cuvée domaine"): eu("4,70", "4,50", "4,20"),

    # ——— Domaine de la Barbinière (scans 6 et 7) : « Tarifs Restauration HT 2026 »,
    # colonnes ≥ 24, ≥ 60 et ≥ 120, toutes trois surlignées. Les prix sont ceux du 75 cl
    # (la ligne « Les Courbes » 2017 est barrée, la 2018 surlignée).
    (2, "Les Silex Rouge"): eu("6,57", "5,72", "5,49"),
    (2, "Les Gorinières Blanc"): eu("11,37", "10,52", "10,10"),
    (2, "Les Courbes Rouge"): eu("10,57", "9,72", "9,33"),
    (2, "Les Amphibol Blanc"): eu("8,46", "7,61", "7,30"),
    (2, "Les Gneiss Rouge"): eu("7,75", "6,90", "6,62"),
    (2, "Le Bois Bouquet"): eu("9,87", "9,02", "8,66"),
    (2, "L\u2019O Brut"): eu("9,29", "8,44", "8,11"),

    # ——— Domaine Nadine Ferrand (scan 23) : « Tarif CHR 2026 », un prix unique.
    # Une note rouge « supprimer » barre un mot du titre : signalée dans QUESTIONS.md,
    # rien n'a été retiré sans l'agence.
    (11, "Lise-Marie"): eu("15,10"),
    (11, "Lise-Marie, caisse bois"): eu("46,80"),
    (11, "AOP Viré-Clessé", "Blanc", "2024", "75 cl"): eu("13,10"),
    (11, "AOP Viré-Clessé", "Blanc", "2024", "Magnum 1,5 L"): eu("24,70"),
    (11, "AOP Saint-Véran", "Blanc", "2024", "75 cl"): eu("11,90"),
    (11, "AOP Saint-Véran", "Blanc", "2024", "Magnum 1,5 L"): eu("24,40"),
    (11, "AOP Mâcon Solutré-Pouilly", "Blanc", "2024", "75 cl"): eu("10,10"),
    (11, "Signature"): eu("10,80"),
    (11, "AOP Mâcon", "Blanc", "2024", "75 cl"): eu("8,50"),
}

# ——————————————————————————————————————————————— les vins retirés du tarif restaurant ———
# Une ligne barrée sur le tarif annoté : le domaine ne la propose pas aux restaurants.
RETIRES = {
    (41, "Sancerre Rosé"),      # barré sur le tarif (scan 5)
}

# ——————————————————————————————————————————————————————————————— les offres ———
# L'agence les reprend une par une (« je changerai les offres, page 1, page 2… ») :
# tant qu'elle ne les a pas données, la fiche garde l'offre du catalogue caviste.
OFFRES = {}


def cle_vin(v):
    return (v["fiche"], v["cuvee"] or v["appellation"])


def prix_de(v):
    """Le prix restaurant d'un vin. Deux lignes peuvent partager une cuvée (deux millésimes,
    deux contenances) : la clé la plus précise gagne."""
    f, c = cle_vin(v)
    a, co, m, ct = v["appellation"], v["couleur"], v["millesime"], v["contenance"]
    for cle in ((f, a, co, m, ct), (f, c, m, ct), (f, c, ct), (f, c, m), (f, c)):
        if cle in PRIX:
            return PRIX[cle]
    return None


def main():
    cat = json.loads(SOURCE.read_text(encoding="utf-8"))
    cat["edition"] = "Catalogue restaurant 2026"
    for s in cat["stands"]:
        s["vins"] = [v for v in s["vins"] if cle_vin(v) not in RETIRES]
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
            prix = prix_de(v)
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
