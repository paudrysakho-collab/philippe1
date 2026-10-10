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

    # ——————————————— dossier complet du 10 octobre (tarifs-restaurant-annotes-2.pdf) ———
    21: P(36, 48, 96, unite="cols"),   # Domaine Trichon, Rhône (p.48) : « Tarifs HT franco de port »
    42: P(36, 48, 96, unite="cols"),   # Domaine Trichon, Bugey (p.49) : 36, 48 et 96 surlignés
    # Stratéus (p.51) : la grille va de 24 à 300 bouteilles ; on garde les plus petits volumes.
    22: P(24, 48, 120),
    23: ["À partir de 60 bts"],        # Domaine Haut Marin (p.52) : une seule colonne
    26: P(36, 72, 120),                # Château La Gorce (p.57) : 36, 72 et 120 surlignés, 48 rayée
    29: ["Carton", "À partir de 120 bts", "À partir de 180 bts"],   # Balac (p.55) : 300 et 600 rayées
    34: P(36, 60, 120),                # Château de Gragnos (p.42) : « À partir de 36 / 60 / 120 »
    35: ["Prix"],                      # Les Lys (p.44) : tarif CHR, un seul prix
    38: P(36, 66, 126),                # Denis Frézier (p.46) : 186 et 240 rayées
    40: ["Par 24", "Par 48", "Par 78"],   # Vazart-Coquart (p.47) : tarifs franco surlignés
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

    # ——— Famille d'Exea (scan 35 et dossier du 10 octobre, p.34, 37 et 40) : 72 / 144 / 300 cols.
    (32, "Oena Rouge"): eu("14,00", "14,00", "14,00"),
    (32, "Chant de Lune Rouge"): eu("8,95", "7,78", "7,16"),          # Château d'Argens, p.37
    (32, "Rouge Sérame"): eu("8,95", "7,78", "7,16"),                 # p.36
    (32, "Blanc Sérame"): eu("8,95", "7,78", "7,16"),                 # p.36
    (32, "Jardins de Corbières Rouge", "75 cl"): eu("5,45", "4,74", "4,36"),       # p.40
    (32, "Jardins de Corbières Rouge, disponible en décembre 2026"): eu("11,40", "9,91", "9,12"),

    # ————————————————————————— dossier complet du 10 octobre ——————————————————————————
    # ——— Domaine des Pasquiers (p.50) : « TARIF HORS TAXES - DEPART CAVE », un seul prix.
    (20, "IGP Vaucluse", "Rouge", "2024", "75 cl"): eu("3,40"),
    (20, "IGP Vaucluse", "Rosé", "2025", "75 cl"): eu("3,80"),
    (20, "IGP Vaucluse", "Blanc", "2025", "75 cl"): eu("4,20"),
    (20, "Côtes du Rhône"): eu("4,50"),
    (20, "Plan de Dieu"): eu("6,20"),
    (20, "Sablet", "2023"): eu("6,20"),
    (20, "Sablet", "2024"): eu("7,50"),
    (20, "Gigondas"): eu("12,90"),

    # ——— Domaine Trichon, Rhône (p.48) : 36 / 48 / 96 cols, franco de port.
    (21, "Mas de Lusanne Rouge"): eu("7,24", "6,74", "6,24"),
    (21, "Mas de Lusanne Vacqueyras Blanc"): eu("11,64", "11,14", "10,64"),
    (21, "Mas de Lusanne Vacqueyras Rouge", "75 cl"): eu("11,43", "10,93", "10,43"),
    (21, "Mas de Lusanne Vacqueyras Rouge", "Magnum 1,5 L"): eu(None, None, "22,84"),
    (21, "Beaumes de Venise Rouge", "75 cl"): eu("10,26", "9,76", "9,26"),
    (21, "Beaumes de Venise Rouge", "Magnum 1,5 L"): eu(None, None, "18,46"),
    (21, "Muscat de Beaumes de Venise"): eu("11,97", "11,47", "10,97"),

    # ——— Domaine Trichon, Bugey (p.49) : 36 / 48 / 96 cols, franco de port.
    (42, "Mas de Lusanne Brut Blanc"): eu("9,13", "8,81", "8,49"),
    (42, "Mas de Lusanne Extra-Brut Blanc"): eu("9,13", "8,81", "8,49"),
    (42, "Mas de Lusanne Mondeuse Rouge"): eu("9,08", "8,73", "8,38"),
    (42, "Mas de Lusanne Pinot Noir Rouge"): eu("8,69", "8,17", "7,99"),
    (42, "Mas de Lusanne Gamay Rouge"): eu("7,55", "7,09", "6,85"),
    (42, "Mas de Lusanne Chardonnay Blanc"): eu("8,95", "8,74", "8,24"),
    (42, "Mas de Lusanne Pétillant de Jus de Raisin 0 %"): eu("6,78", "6,43", "6,08"),

    # ——— Domaine Stratéus (p.51) : grille 2026 + « Rajouter 0,70 cts sur toute la gamme »
    # (écrit par l'agence). Gamme Stratéus, gamme Koloss (pas de prix à 48 bts) et gamme Néolithik.
    (22, "Stratéus Rouge"): eu("13,20", "12,50", "11,70"),
    (22, "Stratéus Blanc"): eu("13,20", "12,50", "11,70"),
    (22, "Néolitik Rouge"): eu("16,70", "15,20", "13,20"),
    (22, "Néolitik Blanc"): eu("16,70", "15,20", "13,20"),
    (22, "Koloss Rouge"): eu("7,20", None, "6,70"),
    (22, "Koloss Doux"): eu("7,20", None, "6,70"),

    # ——— Domaine Haut Marin (p.52) : une colonne « À partir de 60 bts », franco de port.
    (23, "N°1 Littorine Blanc"): eu("4,35"),
    (23, "N°6 Fossiles Blanc"): eu("4,70"),
    (23, "N°3 Gulf Stream Rosé"): eu("4,70"),
    (23, "N°4 Triton Rouge"): eu("4,70"),
    (23, "N°8 Grand Pavois Moelleux"): eu("5,80"),
    (23, "N°7 Vénus Blanc Moelleux"): eu("5,25"),

    # ——— Château La Gorce (p.57) : « TARIFS CHR », franco de port, 36 / 72 / 120 bts.
    (26, "Château la Gorce", "75 cl"): eu("7,60", "7,25", "7,15"),
    (26, "Château la Gorce", "Magnum 1,5 L"): eu("14,90", "14,55", "14,45"),
    (26, "Prétexte"): eu("7,10", "6,75", "6,65"),
    (26, "Rouge Intense"): eu("6,75", "6,40", "6,30"),
    (26, "L'An 022"): eu("10,40", "10,05", "9,95"),
    (26, "La Bonne Résolution"): eu("6,90", "6,55", "6,45"),
    (26, "Château Canteloup"): eu("5,60", "5,25", "5,15"),

    # ——— Château Falfas (p.54), annoté « Idem » : les prix du catalogue caviste.
    (27, "Les Demoiselles de Falfas"): eu("9,50"),
    (27, "Château Falfas", "2020"): eu("12,30"),
    (27, "Château Falfas", "2021"): eu("12,30"),
    (27, "Château Falfas", "2022"): eu("12,40"),
    (27, "Château Falfas", "2023"): eu("20,10"),
    (27, "Château Falfas Chevalier", "2017"): eu("24,20"),
    (27, "Château Falfas Chevalier", "2019"): eu("23,90"),

    # ——— Château Pré La Lande (p.53), annoté « Idem ».
    (28, "Cuvée Diane Rouge"): eu("9,90"),
    (28, "Cuvée TerraCotta"): eu("8,90"),
    (28, "Cuvée des Fontenelles"): eu("7,50"),

    # ——— Château Balac (p.55) : colonnes Carton / 120 / 180 (300 et 600 rayées).
    # Le Château Balac lui-même n'est pas dans le courriel (« Rajouter Balac ») : cases vides.
    (29, "Balac sans sulfites"): eu("7,50", "6,90", "6,80"),
    (29, "L’inopiné de Balac"): eu("6,90", "6,30", "6,20"),
    (29, "Syrah de Balac"): eu("8,90", "8,50", "8,40"),

    # ——— Château l'Escarderie (p.56), annoté « Idem ».
    (30, "Château Lafargue Rouge"): eu("6,90"),
    (30, "Amphora Rouge"): eu("10,10"),
    (30, "La Confiance Rouge"): eu("8,45"),

    # ——— Château de Gragnos (p.42) : « À partir de 36 / 60 / 120 », franco.
    # Cosmos, BDM, Syrah nature et Dolmen sont barrés ; « Rajouter Juliette blanc 2025 ».
    (34, "Léon Rouge"): eu("5,95", "5,65", "5,35"),
    (34, "Henri Rouge"): eu("5,95", "5,65", "5,35"),
    (34, "Juliette Blanc"): eu("5,95", "5,65", "5,35"),
    (34, "Lou Daro Rouge"): eu("7,80", "7,50", "7,20"),
    (34, "Grain de Blanc"): eu("7,80", "5,50", "7,20"),   # 5,50 au palier 60 : relevé tel quel

    # ——— Les Lys (p.44) : « TARIF CHR », prix HT départ cave ; « La Soif » ajoutée à la main.
    (35, "Aillargues"): eu("7,55"),
    (35, "La Petite Syrah"): eu("5,95"),
    (35, "Duché"): eu("7,90"),
    (35, "Caillasses"): eu("19,90"),
    (35, "La Soif"): eu("4,95"),

    # ——— Prieuré Sainte-Marie d'Albas (p.43) : « TARIF PROFESSIONNEL RESTAURATION 2026 ».
    # Les magnums n'y figurent pas : cases vides.
    (36, "Terre Rouge", "75 cl"): eu("8,60"),
    (36, "4 saisons", "75 cl"): eu("7,20"),
    (36, "La Potion"): eu("4,10"),
    (36, "Clos de Cassis", "75 cl"): eu("9,60"),
    (36, "Albas"): eu("5,60"),

    # ——— Champagne Dekeyne (p.45, courriel du domaine) : HT départ cave.
    (37, "Voglonniers Brut"): eu("19,96"),
    (37, "Nature Brut"): eu("25,41"),
    (37, "Chardonnay Extra-Brut"): eu("26,48"),
    (37, "Supernova Extra-Brut Zéro Dosage"): eu("36,83"),

    # ——— Champagne Denis Frézier (p.46) : colonnes 1-60, 66-120 et 126-180 (186 et 240 rayées),
    # « Tarif Franco ». La première colonne est réécrite à la main par l'agence (« + 1 € »).
    (38, "Trois Crus Brut"): eu("16,92", "15,76", "15,45"),
    (38, "Le Terroir Blanc Blanc de Blancs Brut"): eu("19,72", "17,54", "17,20"),
    (38, "Le Terroir Meunier Blanc de Meuniers Extra-Brut"): eu("19,72", "17,54", "17,20"),
    (38, "Millésime Expression"): eu("20,34", "19,14", "18,77"),

    # ——— Champagne Vazart-Coquart (p.47) : tarifs franco « Par 24 / 48 / 78 » (surlignés).
    (40, "Cuvée Camille Extra-Brut Blanc de Blancs"): eu("20,40", "20,10", "19,90"),
    (40, "Brut Réserve Blanc de Blancs", "75 cl"): eu("21,10", "20,80", "20,60"),
    (40, "Brut Réserve Blanc de Blancs", "1,5 L"): eu("48,50", "47,90", "47,50"),
    (40, "Rosé Brut"): eu("23,20", "22,90", "22,70"),
    (40, "Spécial Club Blanc de Blancs Extra-Brut"): eu("41,40", "41,10", "40,90"),
    (40, "Extra Brut"): eu("25,30", "25,00", "24,80"),
    (40, "82/18 Blanc de Blancs Zéro Dosage"): eu("52,10", "51,80", "51,60"),

    # ——— La Passion des Terroirs (p.58 à 73) : « Tarif France Franco HT », prix à l'unité.
    (25, "Château de Camarsac Cuvée Vieilles Vignes"): eu("5,50"),
    (25, "Château de Camarsac Cuvée Prestige"): eu("7,65"),
    (25, "Château Haut-Moulin Vieilles Vignes"): eu("4,90"),
    (25, "Château Haut-Moulin Cuvée Vieilles Vignes"): eu("5,70"),
    (25, "L'Étoile de Villegeorge"): eu("6,50"),
    (25, "N°2 de Fourcas Dupré"): eu("7,70"),
    (25, "Château Doyac"): eu("10,80"),
    (25, "Esprit de Doyac"): eu("7,00"),
    (25, "Ceres de Haut-Bages Libéral, sans soufre ajouté"): eu("15,10"),
    (25, "Château Livran"): eu("8,80"),
    (25, "Les Sources de Livran"): eu("5,40"),
    (25, "Les Plantes de Durfort-Vivens"): eu("19,90"),
    (25, "Le Plateau de Durfort-Vivens", "75 cl"): eu("23,40"),
    (25, "Le Plateau de Durfort-Vivens", "Magnum 1,5 L"): eu("46,30"),
    (25, "Le Hameau de Durfort-Vivens", "75 cl"): eu("23,40"),
    (25, "Le Hameau de Durfort-Vivens", "Magnum 1,5 L"): eu("46,30"),
    (25, "La Petite Tour de Bessan"): eu("11,85"),
    (25, "Initial de Desmirail"): eu("16,40"),
    (25, "L'Oratoire de Chasse-Spleen"): eu("14,80"),     # millésime 2020
    (25, "Pavillon de Glana"): eu("15,85"),               # millésime 2022
    (25, "La Fleur de Haut-Bages Libéral"): eu("17,90"),
    (25, "Château Pontey Lamartine Cuvée Les Parcelles", "2020"): eu("6,00"),
    (25, "Graves de Bouscaut"): eu("7,80"),
    (25, "Château Lamothe Bouscaut", "75 cl"): eu("12,85"),
    (25, "Château Lamothe Bouscaut", "Magnum 1,5 L"): eu("25,90"),
    (25, "Château Valoux"): eu("8,85"),
    (25, "Château Tour Bel-Air", "75 cl"): eu("6,20"),
    (25, "Château Tour Bel-Air", "Magnum 1,5 L"): eu("14,30"),
    (25, "Château Macquin", "75 cl"): eu("7,50"),
    (25, "Château Macquin", "Magnum 1,5 L"): eu("17,25"),
    (25, "Les Parcelles de François Despagne"): eu("14,20"),
}

# ——————————————————————————————————————————————— les vins retirés du tarif restaurant ———
# Aucun : « par rapport aux catalogues cavistes, tout est bon et tout est à prendre ; la seule
# différence, c'est les minimums de commande, les colonnes et les prix » (l'agence, 10 octobre).
# Le catalogue restaurant a donc exactement les mêmes vins que le catalogue caviste. Deux lignes
# sont barrées sur les tarifs restaurant — le « Sancerre Rosé » des Sardelles (scan 5) et le
# magnum de Plénitude de Solemme (scan 2) : elles restent au catalogue, sans prix.
RETIRES = set()

# ——————————————————————————————————————————————————————————————— les offres ———
# L'agence les reprend une par une (« je changerai les offres, page 1, page 2… ») :
# tant qu'elle ne les a pas données, la fiche garde l'offre du catalogue caviste.
OFFRES = {
    5: "Offre 11+1 à partir de 60 cols.",   # écrit à la main sur le scan 11 (Berteaud Manceau)
}

# ————————————————————————————————————————————— les notes de prix du tarif restaurant ———
# Deux formulations seulement, comme dans les autres éditions : franco de port, ou hors frais
# de transport (le tarif dit « départ cave » ou « départ chai »).
HORS = "* Prix de la bouteille H.T. hors frais de transport."
FRANCO = "* Prix de la bouteille H.T. franco de port."
NOTES = {
    20: HORS,      # Pasquiers : « TARIF HORS TAXES - DEPART CAVE »
    21: FRANCO,    # Trichon Rhône : « Tarifs HT franco de port »
    22: FRANCO,    # Stratéus : « Franco de port 48 bouteilles »
    23: FRANCO,    # Haut Marin : « Prix de la bouteille H.T. Franco de port. »
    26: FRANCO,    # La Gorce : « Prix Franco de port par bouteille »
    34: FRANCO,    # Gragnos : « Franco », écrit par l'agence
    35: HORS,      # Les Lys : « départ cave », écrit par l'agence
    36: FRANCO,    # Albas : « Franco », écrit par l'agence sous « départ cave »
    37: HORS,      # Dekeyne : « HT départ cave »
    38: FRANCO,    # Frézier : « Tarif Franco », écrit par l'agence
    40: FRANCO,    # Vazart-Coquart : colonnes « TARIFS FRANCO »
    42: FRANCO,    # Trichon Bugey : « Tarifs HT franco de port »
    25: FRANCO,    # La Passion des Terroirs : « Tarif France Franco HT »
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
            if n in NOTES:
                s["note_prix_salon"] = NOTES[n]
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
