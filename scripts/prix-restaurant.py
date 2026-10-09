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
    39: P(36, 60, 120),          # Solemme, scan 2 : « 36 / 60 / 120 » écrits à la main, 240 et 360 rayés
    4: P(60, 120),               # Domaine des Noëls, scan 10 : colonnes C.H.R. « 60 à 119 » et « 120 et plus »
    5: P(36, 60, 120, unite="cols"),   # Berteaud Manceau, scan 11 : 36, 60 et 120 surlignés
    # Jean de Villebois, scans 12 et 13 : « à partir de 36 », puis 66, 126 et 246 écrits au-dessus
    # des colonnes 36-42, 66-120, 126-240 et 246-300 ; la colonne 18-30 est rayée.
    6: P(36, 66, 126, 246, unite="cols"),
    8: ["De 36 à 72 bts", "De 72 à 120 bts", "Plus de 120 bts"],   # Boehler, scan 14 (surlignés)
    9: P(36, 60, 120),           # Domaine des Nugues, scan 15 : 36, 60 et 120 surlignés
    # Goichot, Château du Cray et Les Guignottes (scans 17 à 21) : la colonne 1-36 est rayée ;
    # « à partir de 42 », « 72 » et « 126 » écrits au-dessus des trois autres.
    12: P(42, 72, 126),
    13: P(42, 72, 126),
    14: P(42, 72, 126),
    15: P(36, 60, 120),          # Domaine des Verchères, scan 22 : 36, 60 et 120 surlignés
    31: P(60, 120, 180),         # Bastide de Blacailloux, scan 34 : colonne « franco 36 » rayée
    32: P(72, 144, 300, unite="cols"),   # Famille d'Exea — Sérame, scan 35
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

    # ——— Champagne Solemme (scan 2) : colonnes « < 60 », « 60 » et « 120 » du tarif, renommées
    # 36 / 60 / 120 à la main ; les colonnes 240 et 360 et les magnums sont rayés.
    (39, "Terre de Solemme Brut"): eu("21,70", "21,20", "20,50"),
    (39, "Plénitude de Solemme Extra-Brut", "75 cl"): eu("22,70", "22,10", "21,60"),
    (39, "Esprit de Solemme Brut Nature"): eu("26,50", "25,80", "25,10"),
    (39, "Nature de Solemme Blanc de Blancs Brut Nature"): eu("32,80", "32,00", "31,20"),
    (39, "Ambre de Solemme Blanc de Noirs Brut Nature"): eu("34,30", "33,50", "32,60"),
    (39, "Rose de Solemme Brut Nature"): eu("36,90", "36,00", "35,10"),

    # ——— Domaine des Noëls (scan 10) : « Prix CHR », colonnes 60 à 119 et 120 et plus.
    (4, "AOC Anjou Blanc"): eu("3,90", "3,60"),
    (4, "Promenade de Noëls"): eu("5,90", "5,70"),
    (4, "AOC Sauvignon"): eu("4,00", "3,60"),
    (4, "AOC Coteaux du Layon"): eu("5,90", "5,70"),
    (4, "AOC Coteaux du Layon Faye"): eu("9,90", "9,70"),
    (4, "AOC Crémant de Loire"): eu("5,80", "5,60"),
    (4, "AOC Rosé de Loire"): eu("3,80", "3,50"),

    # ——— Chai Berteaud Manceau (scan 11) : 36 / 60 / 120 cols.
    (5, "Courant Chenin"): eu("6,95", "6,45", "5,95"),
    (5, "Source Melon B."): eu("5,95", "5,45", "4,95"),
    (5, "Reflet Gamay"): eu("6,95", "6,45", "5,95"),
    (5, "L’Eberluant Chardonnay Méthode ancestrale"): eu("6,95", "6,45", "5,95"),

    # ——— Jean de Villebois (scans 12 et 13) : 36 / 66 / 126 / 246 cols. Les trois cuvées
    # parcellaires n'ont pas de prix au-delà de 120 cols (« – » sur le tarif) : cases vides.
    # Le Menetou-Salon rouge et le Chenin IGP ne sont pas au tarif : cases vides.
    (6, "AOC Menetou-Salon Blanc"): eu("11,65", "10,55", "10,35", "10,05"),
    (6, "AOC Quincy"): eu("11,60", "10,50", "10,25", "9,95"),
    (6, "Les Beltins Blanc"): eu("28,00", "26,90", None, None),
    (6, "Chêne à la Rouline Blanc"): eu("28,00", "26,90", None, None),
    (6, "Vignes de Tréleau Blanc"): eu("28,00", "26,90", None, None),
    (6, "La Louisonne Rouge"): eu("28,00", "26,90", "26,55", "26,30"),
    (6, "AOC Pouilly-Fumé"): eu("13,90", "12,80", "12,55", "12,25"),
    (6, "AOC Touraine Chenonceaux"): eu("8,55", "7,45", "7,25", "6,95"),
    (6, "IGP Sauvignon Blanc"): eu("7,10", "6,05", "5,80", "5,50"),
    (6, "IGP Pinot Noir Rosé"): eu("6,85", "5,75", "5,50", "5,20"),
    (6, "IGP Pinot Noir"): eu("6,90", "5,75", "5,55", "5,25"),

    # ——— Domaine Boehler (scan 14) : colonnes 36-72, 72-120 et > 120 bt surlignées.
    (8, "AOC Crémant d’Alsace"): eu("8,90", "8,40", "8,00"),
    (8, "Molse Blanc"): eu("7,30", "6,80", "6,40"),
    (8, "Molse Rouge"): eu("8,90", "8,40", "7,80"),
    (8, "Leimen Sylvaner"): eu("9,20", "8,70", "8,10"),
    (8, "Riesling Holderhurst"): eu("9,20", "8,70", "8,30"),
    (8, "Riesling Hahnenberg"): eu("12,20", "11,40", "11,00"),
    (8, "Gewurztraminer Grand Cru Bruderthal"): eu("16,50", "15,40", "14,90"),
    (8, "Riesling Grand Cru Bruderthal"): eu("20,10", "18,80", "18,20"),
    (8, "Seiler Rouge"): eu("11,00", "10,30", "9,90"),

    # ——— Domaine Sébastien Magnien (scan 16) : colonne 2024 surlignée, prix unique.
    (10, "AOC Hautes-Côtes de Beaune"): eu("13,50"),
    (10, "AOC Meursault"): eu("35,00"),            # « Les Grands Charrons », comme au salon
    (10, "Les Aigrots", "2023"): eu("24,00"),      # Beaune 1er Cru blanc
    (10, "Les Aigrots", "2024"): eu("22,00"),      # Beaune 1er Cru rouge
    (10, "Clos de la Perrière"): eu("14,50"),
    (10, "Les Bons Feuvres"): eu("18,00"),
    (10, "Les Perrières"): eu("24,00"),

    # ——— Goichot, Château du Cray, Les Guignottes (scans 18 à 21) : 42 / 72 / 126 bts.
    # Le Pouilly-Vinzelles n'est pas au tarif : cases vides.
    (12, "AOC Auxey-Duresses Blanc"): eu("22,50", "22,20", "21,90"),
    (12, "Baron Auguste Blanc"): eu("9,30", "9,00", "8,70"),
    (12, "Baron Auguste Rosé"): eu("9,30", "9,00", "8,70"),
    (12, "AOC Chassagne-Montrachet Rouge"): eu("23,90", "23,60", "23,30"),
    (12, "Aux Allots Rouge"): eu("33,90", "33,60", "33,30"),
    (12, "AOC Mercurey Rouge"): eu("16,50", "16,20", "15,90"),
    (12, "AOC Givry Rouge"): eu("16,50", "16,20", "15,90"),
    (12, "AOC Gevrey-Chambertin"): eu("43,50", "43,20", "42,90"),
    (13, "AOC Mercurey Blanc"): eu("15,70", "15,40", "15,10"),        # « Les Doués »
    (14, "AOP Bourgogne Chardonnay"): eu("8,90", "8,60", "8,30"),
    (14, "Domaine les Guignottes Rouge"): eu("8,90", "8,60", "8,30"),

    # ——— Domaine des Verchères (scan 22) : 36 / 60 / 120 bts.
    (15, "AOC Mâcon Chardonnay"): eu("6,75", "6,40", "6,10"),
    (15, "AOC Mâcon Mancey Blanc"): eu("7,40", "7,05", "6,70"),
    (15, "AOC Mâcon Mancey Rouge"): eu("6,35", "6,05", "5,75"),
    (15, "AOC Bourgogne Passe-Tout-Grains Rouge"): eu("6,35", "6,05", "5,75"),
    (15, "Les Bulles du Puits Rosé Gamay Demi-Sec"): eu("6,75", "6,40", "6,40"),

    # ——— La Passion des Terroirs (scans 31 et 32) : prix à l'unité. Le dossier n'a que les
    # pages des blancs et des liquoreux : les rouges gardent leurs cases vides.
    (25, "Château Doyac Le Pélican"): eu("10,25"),
    (25, "Château Pontey Lamartine Cuvée Les Parcelles", "2023"): eu("6,25"),   # le blanc
    (25, "Château Lamothe-Bouscaut"): eu("12,85"),                             # le blanc
    (25, "Petit Valoux"): eu("8,90"),
    (25, "Château du Mayne"): eu("11,85"),        # millésime 2023 au tarif restaurant
    (25, "Cyprès de Climens"): eu("17,85"),       # 50 cl, millésime 2010

    # ——— Bastide de Blacailloux (scan 34) : « Tarif franco » 60 / 120 / 180.
    (31, "Sainte-Probace Rosé"): eu("5,40", "5,30", "5,15"),
    (31, "Sainte-Probace Blanc"): eu("5,65", "5,50", "5,35"),
    (31, "Sainte-Probace Rouge"): eu("5,65", "5,50", "5,35"),
    (31, "Joio Rosé"): eu("6,50", "6,30", "6,15"),
    (31, "Joio Blanc"): eu("6,50", "6,30", "6,15"),
    (31, "Joio Rouge"): eu("6,70", "6,40", "6,25"),
    (31, "Miraia Blanc"): eu("9,45", "9,30", "9,05"),
    (31, "Miraia Rouge"): eu("9,00", "8,70", "8,55"),
    (31, "Aquino Rouge"): eu("17,25", "16,30", "16,00"),
    (31, "Aquino Blanc"): eu("17,25", "16,30", "16,00"),

    # ——— Famille d'Exea — Sérame (scan 35) : seul « Oena » est au tarif du dossier.
    (32, "Oena Rouge"): eu("14,00", "14,00", "14,00"),
}

# ——————————————————————————————————————————————— les vins retirés du tarif restaurant ———
# Une ligne barrée sur le tarif annoté : le domaine ne la propose pas aux restaurants.
RETIRES = {
    (41, "Sancerre Rosé"),      # barré sur le tarif (scan 5)
    (39, "Plénitude de Solemme Extra-Brut", "1,5 L"),   # magnums rayés (scan 2)
}

# ——————————————————————————————————————————————————————————————— les offres ———
# L'agence les reprend une par une (« je changerai les offres, page 1, page 2… ») :
# tant qu'elle ne les a pas données, la fiche garde l'offre du catalogue caviste.
OFFRES = {
    5: "Offre 11+1 à partir de 60 cols.",   # écrit à la main sur le scan 11 (Berteaud Manceau)
}


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
        s["vins"] = [v for v in s["vins"] if cle_vin(v) not in RETIRES
                     and cle_vin(v) + (v["contenance"],) not in RETIRES]
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
