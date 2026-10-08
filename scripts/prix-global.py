#!/usr/bin/env python3
"""Le catalogue caviste global 2026 : les fiches du Salon Privé, plus les domaines réintégrés.

Source : le catalogue du salon imprimé, relu et annoté par l'agence, avec les tarifs des
domaines à réintégrer intercalés à leur place (sources/catalogue-global-2026/pages/scan-NN.jpg,
scan du 8 octobre 2026), le sommaire annoté (sources/catalogue-global-2026/sommaire-annote.pdf)
et les consignes vocales de l'agence du 8 octobre. Règles :
- ce qui est en rose dans le sommaire est réintégré, à l'endroit indiqué ;
- sur un tarif, les lignes et les colonnes SURLIGNÉES sont celles à mettre ; ce qui est barré
  est retiré ; une colonne non surlignée (souvent « 36 ») disparaît ;
- plus de numéros de stand : on ne parle que de pages ;
- les fiches venues du salon gardent leurs vins, prix et offres (le scan les reprend tels quels) ;
- Trichon est coupé en deux : Rhône (surligné rose) et Bugey (surligné jaune), panachables ;
- La Passion des Terroirs : le picto bio sur chaque ligne concernée, pas en tête de fiche.
Le relevé ligne à ligne est dans data/catalogue-global-releve.md ; les doutes dans QUESTIONS.md
(point 32).

Ce script lit data/salon-prive-2026.json (déjà complet de ses prix) et écrit
data/catalogue-global-2026.json, que `EDITION=global` lit (src/gabarits/pieces.mjs).
Usage : python3 scripts/prix-global.py, puis npm run global.
"""
import copy
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SALON = json.loads((RACINE / "data/salon-prive-2026.json").read_text(encoding="utf-8"))
SORTIE = RACINE / "data/catalogue-global-2026.json"
SOURCE = "tarif annoté par l'agence, scan du 8 octobre 2026"


def eu(*prix):
    """Des euros (« 7,71 ») aux centimes entiers, sans passer par un flottant."""
    out = []
    for p in prix:
        e, _, c = p.partition(",")
        out.append(int(e) * 100 + int((c + "00")[:2]))
    return out


def P(*paliers, unite="bts"):
    return [f"À partir de {n} {unite}" for n in paliers]


UNIQUE = ["Prix"]
HORS = "* Prix de la bouteille H.T. hors frais de transport."
FRANCO = "* Prix de la bouteille H.T. franco de port."


def V(fiche, tableau, appellation, cuvee, couleur, millesime, prix, contenance="75 cl", **autres):
    v = {"fiche": fiche, "tarif": {"tableau": tableau}, "appellation": appellation, "cuvee": cuvee,
         "couleur": couleur, "millesime": millesime, "contenance": contenance,
         "prix_centimes": prix, "prix_source": SOURCE}
    v.update(autres)
    return v


# Le texte des Sardelles : écrit d'après le site officiel du domaine
# (https://www.domaine-des-sardelles.com, pages Accueil, Histoire, Équipe), à la demande de
# l'agence (8 octobre 2026) — le tarif n'en donne pas.
TEXTE_SARDELLES = (
    "Au nord du vignoble de Sancerre, à Sainte-Gemme-en-Sancerrois, le Domaine des Sardelles est "
    "une aventure familiale : Christophe et Guillaume, rejoints en 2021 par leur neveu Cyprien, "
    "portent aujourd'hui les deuxième et troisième générations. Approche peu interventionniste à la "
    "vigne comme en cave, vendanges entièrement à la main et conversion à l'agriculture biologique "
    "pour des Sancerre et des IGP Val de Loire de terroir.")

# ——— l'ordre du catalogue (sommaire annoté) et ses régions ———
REGIONS = ["Loire", "Alsace", "Beaujolais", "Bourgogne", "Rhône", "Bugey", "Sud-Ouest",
           "Bordeaux", "Provence", "Languedoc", "Champagne"]
ORDRE = [1, 41, 2, 3, 4, 5, 6,          # Loire : Sardelles entre Reverdy et Barbinière
         8,                              # Alsace
         9,                              # Beaujolais : Domaine des Nugues
         10, 12, 13, 14, 15, 11,         # Bourgogne : Nadine Ferrand après Verchères
         16, 17, 18, 19, 20, 43, 21,     # Rhône : Pasquiers, Mas des Restanques, puis Trichon
         42,                             # Bugey : Domaine Trichon
         22, 23,                         # Sud-Ouest
         27, 28, 29, 30, 26, 25,         # Bordeaux : l'Escarderie, La Gorce, Passion des Terroirs
         31,                             # Provence
         32, 33, 34, 36, 35,             # Languedoc : Les Lys après Albas
         37, 38, 39, 40]                 # Champagne

# ——— les domaines qui n'existaient pas dans les fiches (numéros 41 et 42) ———
DOMAINES_AJOUTES = [
    {"numero": 41, "page_source": None, "region": "Loire", "nom": "Domaine des Sardelles",
     "nom_sommaire": "Domaine des Sardelles", "texte_source": TEXTE_SARDELLES, "texte_tarif": "",
     "texte_catalogue": "", "labels": [{"label": "Bio", "preuve": "logo AB sur le tarif (scan 8 oct., p.5)"}],
     "labels_tarif": [], "allocation": False, "mentions": [], "panachage_groupe": None,
     "note_prix": FRANCO, "departements": ["35", "44", "49", "53", "56", "85"],   # l'agence, 8 oct.
     "tableaux": [
         {"intitule": "", "paliers": P(72, 144, 288), "lignes": []},
         {"intitule": "IGP Val de Loire — Les Courants", "paliers": P(72, 144, 288), "lignes": []},
     ]},
    {"numero": 42, "page_source": None, "region": "Bugey", "nom": "Domaine Trichon",
     "nom_sommaire": "Domaine Trichon", "texte_source": None, "texte_tarif": "",
     "texte_catalogue": "", "labels": [{"label": "Bio", "preuve": "comme la fiche Trichon du Rhône (n°21)"}],
     "labels_tarif": [], "allocation": False, "mentions": [], "panachage_groupe": "trichon",
     "note_prix": HORS, "departements": ["35", "44", "49", "53", "56", "85"],
     "tableaux": [{"intitule": "Possibilité de panacher", "paliers": P(120, 300, 600, unite="cols"), "lignes": []}]},
]

DOMAINES_AJOUTES.append(
    {"numero": 43, "page_source": None, "region": "Rhône", "nom": "Mas des Restanques",
     "nom_sommaire": "Mas des Restanques",
     # le texte : l'en-tête du tarif, seul document du domaine
     "texte_source": "Vignoble et vins biologiques, certifiés par Ecocert : Gigondas, Vacqueyras et Côtes du Rhône.",
     "texte_tarif": "", "texte_catalogue": "",
     "labels": [{"label": "Bio", "preuve": "« Nos vins sont biologiques et certifiés par Ecocert », tarif 2026"}],
     "labels_tarif": [], "allocation": False, "mentions": [], "panachage_groupe": None,
     "note_prix": "", "departements": ["44", "49", "53", "85"],   # tous sauf 35 et 56 (l'agence, 8 oct.)
     "tableaux": [{"intitule": "", "paliers": ["Prix"], "lignes": []}]})

GROUPES_AJOUTES = [
    {"id": "trichon", "libelle": "Domaine Trichon, Rhône et Bugey", "domaines": [21, 42]},
]
NOMS_PANACHAGE = {"21": "Domaine Trichon (Rhône)", "42": "Domaine Trichon (Bugey)"}

# ——— les domaines réintégrés : vins surlignés, prix des colonnes surlignées ———
NOUVEAUX = {
    # Loire — Domaine des Sardelles (tarif HT franco, scan p.5) et sa marque Les Courants (p.6).
    # Colonnes surlignées : 72, 144, 288 bouteilles. « Les Courants Pinot Noir » : ajout manuscrit.
    41: {"paliers": {"41": P(72, 144, 288)}, "note": FRANCO,
         "offre": "Minimum de commande : 36 bts. Magnum sur demande.",
         "vins": [
             V(41, 0, "AOC Sancerre", "Sancerre Blanc", "Blanc", "—", eu("13,20", "12,90", "12,60")),
             V(41, 0, "AOC Sancerre", "Sancerre Blanc « La Cabane »", "Blanc", "—", eu("16,70", "16,40", "16,10")),
             V(41, 0, "AOC Sancerre", "Sancerre Rosé", "Rosé", "—", eu("10,30", "10,00", "9,70")),
             V(41, 0, "AOC Sancerre", "Sancerre Rouge", "Rouge", "—", eu("13,20", "12,90", "12,60")),
             V(41, 0, "AOC Pouilly-Fumé", "Pouilly-Fumé", "Blanc", "—", eu("11,80", "11,50", "11,20")),
             V(41, 1, "IGP Val de Loire", "Les Courants Sauvignon Blanc", "Blanc", "—", eu("5,50", "5,20", "4,90")),
             V(41, 1, "IGP Val de Loire", "Les Courants Rouge Gamay", "Rouge", "—", eu("5,50", "5,20", "4,90")),
             V(41, 1, "IGP Val de Loire", "Les Courants Pinot Noir", "Rouge", "—", eu("5,50", "5,20", "4,90")),
         ]},
    # Beaujolais — Domaine des Nugues (tarifs France HT départ cave 2026, scan p.14).
    # Colonnes surlignées : 120, 240, 360. Lignes : millésime et format surlignés.
    9: {"paliers": {"9": P(120, 240, 360)}, "note": HORS,
        "offre": "La tranche tarifaire s'applique pour l'ensemble de la commande.",
        "vins": [
            V(9, 0, "AOP Beaujolais-Villages Nouveau", "Nos Vins Primeurs", "Rouge", "2026", eu("5,25", "5,05", "5,00")),
            V(9, 0, "AOP Beaujolais-Villages Nouveau Sans Soufre", "Nos Vins Primeurs", "Rouge", "2026", eu("5,40", "5,15", "5,10")),
            V(9, 0, "AOP Beaujolais-Lancié", "Les Grands Classiques", "Blanc", "2023", eu("7,45", "7,15", "7,05")),
            V(9, 0, "AOP Beaujolais-Lancié", "Les Grands Classiques", "Rouge", "2023", eu("5,80", "5,55", "5,50")),
            V(9, 0, "AOP Beaujolais-Lancié", "Les Grands Classiques", "Rouge", "2022", eu("12,45", "11,95", "11,80"), "Magnum 1,5 L"),
            V(9, 0, "AOP Beaujolais-Villages", "Les Grands Classiques", "Rouge", "2017", eu("12,45", "11,95", "11,80"), "Magnum 1,5 L"),
            V(9, 0, "AOP Fleurie", "Les Grands Classiques", "Rouge", "2024", eu("8,25", "7,90", "7,85")),
            V(9, 0, "AOP Fleurie", "Les Grands Classiques", "Rouge", "2021", eu("18,20", "17,45", "17,25"), "Magnum 1,5 L"),
            V(9, 0, "AOP Moulin-à-Vent", "Les Grands Classiques", "Rouge", "2022", eu("8,50", "8,15", "8,05")),
            V(9, 0, "AOP Moulin-à-Vent", "Les Grands Classiques", "Rouge", "2023", eu("18,70", "17,90", "17,75"), "Magnum 1,5 L"),
            V(9, 0, "AOP Morgon", "Les Grands Classiques", "Rouge", "2023", eu("8,50", "8,15", "8,05")),
        ]},
    # Bourgogne — Domaine Nadine Ferrand (« Tarif Caviste 2026 », scan p.21), lignes surlignées.
    11: {"paliers": {"11": UNIQUE}, "note": HORS, "offre": None,
         "vins": [
             V(11, 0, "AOP Pouilly-Fuissé 1er Cru", "Lise-Marie", "Blanc", "2023", eu("14,00")),
             V(11, 0, "AOP Pouilly-Fuissé 1er Cru", "Lise-Marie, caisse bois", "Blanc", "2021", eu("39,80"), "Magnum 1,5 L"),
             V(11, 0, "AOP Viré-Clessé", "Nadine Ferrand", "Blanc", "2024", eu("11,90")),
             V(11, 0, "AOP Viré-Clessé", "Nadine Ferrand", "Blanc", "2024", eu("22,20"), "Magnum 1,5 L"),
             V(11, 0, "AOP Saint-Véran", "Nadine Ferrand", "Blanc", "2024", eu("11,00")),
             V(11, 0, "AOP Saint-Véran", "Nadine Ferrand", "Blanc", "2024", eu("21,40"), "Magnum 1,5 L"),
             V(11, 0, "AOP Mâcon Solutré-Pouilly", "Nadine Ferrand", "Blanc", "2024", eu("8,90")),
             V(11, 0, "AOP Mâcon Charnay-lès-Mâcon", "Signature", "Blanc", "2024", eu("9,80")),
             V(11, 0, "AOP Mâcon", "Nadine Ferrand", "Blanc", "2024", eu("7,70")),
         ]},
    # Rhône — Domaine des Pasquiers (tarif HT départ cave au 01/01/2026, scan p.27).
    # Barrés : La Singulière, Sablet rosé, Sablet Cuvée Prestige, Cuvée M.
    20: {"paliers": {"20": UNIQUE}, "note": HORS, "offre": None,
         "vins": [
             V(20, 0, "IGP Vaucluse", "Vin de Pays de Vaucluse", "Rouge", "2024", eu("3,30")),
             V(20, 0, "IGP Vaucluse", "Vin de Pays de Vaucluse", "Rosé", "2025", eu("3,65")),
             V(20, 0, "IGP Vaucluse", "Vin de Pays de Vaucluse", "Blanc", "2025", eu("4,05")),
             V(20, 0, "AOP Côtes du Rhône", "Côtes du Rhône", "Rouge", "2024", eu("4,30")),
             V(20, 0, "AOP Côtes du Rhône Villages Plan de Dieu", "Plan de Dieu", "Rouge", "2023", eu("6,00")),
             V(20, 0, "AOP Côtes du Rhône Villages Sablet", "Sablet", "Rouge", "2023", eu("6,00")),
             V(20, 0, "AOP Côtes du Rhône Villages Sablet", "Sablet", "Blanc", "2024", eu("7,25")),
             V(20, 0, "AOP Gigondas", "Gigondas", "Rouge", "2023", eu("12,50")),
         ]},
    # Bordeaux — La Passion des Terroirs (tarif France départ HT, scan p.37 à 55) : les vins
    # surlignés ; Villegeorge et Château la Tour de Bessan barrés. Le label de chaque ligne est
    # celui de son logo sur le tarif (AB → Bio ; Haute Valeur Environnementale → HVE).
    25: {"paliers": {"25": UNIQUE}, "note": HORS, "offre": "Commande minimum : 400 €.",
         "vins": [
             V(25, 0, "AOP Bordeaux Supérieur", "Château de Camarsac Cuvée Vieilles Vignes", "Rouge", "2020", eu("4,60"),
               label="HVE", offre="5+1", offre_detail="(3,83 € la bouteille pour 6 achetées)"),
             V(25, 0, "AOP Bordeaux Supérieur", "Château de Camarsac Cuvée Prestige", "Rouge", "2016", eu("6,75"), label="HVE"),
             V(25, 0, "AOP Bordeaux", "Château Haut-Moulin Vieilles Vignes", "Rouge", "2022", eu("4,00"), label="Bio"),
             V(25, 0, "AOP Haut-Médoc", "L'Étoile de Villegeorge", "Rouge", "2023", eu("5,60"), label="HVE"),
             V(25, 0, "AOP Listrac-Médoc", "N°2 de Fourcas Dupré", "Rouge", "2020", eu("6,80"), label="HVE"),
             V(25, 0, "AOP Haut-Médoc", "Château Doyac", "Rouge", "2020", eu("9,90"), label="Bio"),
             V(25, 0, "AOP Haut-Médoc", "Esprit de Doyac", "Rouge", "2020", eu("6,10"), label="Bio"),
             V(25, 0, "AOP Médoc", "Ceres de Haut-Bages Libéral, sans soufre ajouté", "Rouge", "2022", eu("14,20"), label="Bio"),
             V(25, 0, "AOP Médoc", "Château Livran", "Rouge", "2020", eu("7,90")),
             V(25, 0, "AOP Médoc", "Les Sources de Livran", "Rouge", "2018", eu("4,50")),
             V(25, 0, "AOP Margaux", "Les Plantes de Durfort-Vivens", "Rouge", "2019", eu("19,00"), label="Bio"),
             V(25, 0, "AOP Margaux", "Le Plateau de Durfort-Vivens", "Rouge", "2020", eu("22,50"), label="Bio"),
             V(25, 0, "AOP Margaux", "Le Plateau de Durfort-Vivens", "Rouge", "2020", eu("44,50"), "Magnum 1,5 L", label="Bio"),
             V(25, 0, "AOP Margaux", "Le Hameau de Durfort-Vivens", "Rouge", "2020", eu("22,50"), label="Bio"),
             V(25, 0, "AOP Margaux", "Le Hameau de Durfort-Vivens", "Rouge", "2020", eu("44,50"), "Magnum 1,5 L", label="Bio"),
             V(25, 0, "AOP Margaux", "La Petite Tour de Bessan", "Rouge", "2021", eu("10,95"), label="HVE"),
             V(25, 0, "AOP Margaux", "Initial de Desmirail", "Rouge", "2020", eu("15,50"), label="HVE"),
             V(25, 0, "AOP Moulis", "L'Oratoire de Chasse-Spleen", "Rouge", "2020", eu("13,90"), label="HVE"),
             V(25, 0, "AOP Saint-Julien", "Pavillon de Glana", "Rouge", "2022", eu("14,95")),
             V(25, 0, "AOP Pauillac", "La Fleur de Haut-Bages Libéral", "Rouge", "2020", eu("17,00"), label="Bio"),
             V(25, 0, "AOP Graves", "Château Pontey Lamartine Cuvée Les Parcelles", "Rouge", "2020", eu("5,10"), label="HVE"),
             V(25, 0, "AOP Graves", "Graves de Bouscaut", "Rouge", "2022", eu("6,90"), label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Château Lamothe Bouscaut", "Rouge", "2020", eu("11,95"), label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Château Lamothe Bouscaut", "Rouge", "2022", eu("25,00"), "Magnum 1,5 L", label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Château Lamothe Bouscaut", "Rouge", "2016", eu("59,00"), "3 L", label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Château Valoux", "Rouge", "2021", eu("7,95")),
             V(25, 0, "AOP Montagne-Saint-Émilion", "Château Tour Bel-Air", "Rouge", "2023", eu("5,30"), label="HVE"),
             V(25, 0, "AOP Montagne-Saint-Émilion", "Château Tour Bel-Air", "Rouge", "2022", eu("12,50"), "Magnum 1,5 L", label="HVE"),
             V(25, 0, "AOP Saint-Georges-Saint-Émilion", "Château Macquin", "Rouge", "2023", eu("6,60"), label="HVE"),
             V(25, 0, "AOP Saint-Georges-Saint-Émilion", "Château Macquin", "Rouge", "2022", eu("15,45"), "Magnum 1,5 L", label="HVE"),
             V(25, 0, "AOP Saint-Émilion Grand Cru", "Les Parcelles de François Despagne", "Rouge", "2023", eu("13,30"), label="Bio"),
             V(25, 0, "AOP Blaye-Côtes de Bordeaux", "Château Haut-Moulin Cuvée Vieilles Vignes", "Rouge", "2022", eu("4,80"), label="Bio"),
             V(25, 0, "AOP Bordeaux Blanc", "Château Doyac Le Pélican", "Blanc", "2021", eu("9,35"), label="Bio"),
             V(25, 0, "AOP Graves Blanc", "Château Pontey Lamartine Cuvée Les Parcelles", "Blanc", "2023", eu("5,35"), label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Château Lamothe-Bouscaut", "Blanc", "2021", eu("11,95"), label="HVE"),
             V(25, 0, "AOP Pessac-Léognan", "Petit Valoux", "Blanc", "2023", eu("8,00"), label="HVE"),
             V(25, 0, "AOP Sauternes", "Château du Mayne", "Doux", "2024", eu("10,95"), label="HVE"),
             V(25, 0, "AOP Barsac", "Cyprès de Climens", "Doux", "2010", eu("16,95"), "50 cl"),
         ]},
}


SCAN8 = "tarif annoté par l'agence, scan du 8 octobre 2026 (2e envoi)"
SCAN9 = "tarif professionnel 2026 du domaine, surligné par l'agence (scan du 8 octobre 2026, 3e envoi)"

# Rhône — Mas des Restanques (sources/catalogue-global-2026/scan-mas-des-restanques.pdf) : les vins
# surlignés ; « franco à partir de 96 bouteilles » (l'agence). Placé juste avant Trichon.
NOUVEAUX[43] = {"paliers": {"43": UNIQUE}, "note": "* Prix de la bouteille H.T. franco de port à partir de 96 bts.",
    "offre": None, "vins": [
        V(43, 0, "AOC Gigondas", "Gigondas", "Rouge", "2025", eu("12,85"), prix_source=SCAN9),
        V(43, 0, "AOC Vacqueyras", "Vacqueyras", "Rouge", "2025", eu("10,55"), prix_source=SCAN9),
        V(43, 0, "AOC Vacqueyras", "Cuvée Tombadou", "Rouge", "2024", eu("9,50"), prix_source=SCAN9),
        V(43, 0, "AOC Côtes du Rhône", "Côtes du Rhône", "Rouge", "2024", eu("6,50"), prix_source=SCAN9),
        V(43, 0, "AOC Vacqueyras", "Vacqueyras", "Blanc", "2025", eu("14,90"), prix_source=SCAN9),
        V(43, 0, "Vin de France", "Waouh !", "Blanc", "—", eu("6,50"), prix_source=SCAN9),
        V(43, 0, "AOC Gigondas", "Gigondas", "Rouge", "2025", eu("28,30"), "Magnum 1,5 L", prix_source=SCAN9),
        V(43, 0, "AOC Vacqueyras", "Vacqueyras", "Rouge", "2025", eu("23,20"), "Magnum 1,5 L", prix_source=SCAN9),
    ]}

# Loire — Domaine du Colombier : les bag-in-box surlignés (photo de l'agence, 8 oct.), dans le
# tableau BIBS de la fiche (5 L / 10 L). Le Sauvignon IGP est barré.
BIB_COLOMBIER = [
    V(3, 1, "AOP Muscadet", None, "Blanc", "—", eu("13,80", "22,70"), "BIB", prix_source="tarif des BIB annoté par l'agence, 8 octobre 2026"),
    V(3, 1, "IGP Chardonnay", None, "Blanc", "—", eu("12,50", "19,40"), "BIB", prix_source="tarif des BIB annoté par l'agence, 8 octobre 2026"),
    V(3, 1, "Tous nos rosés", "Cabernet, Abouriou, Gamay, Grolleau Gris", "Rosé", "—", eu("11,50", "18,40"), "BIB",
      prix_source="tarif des BIB annoté par l'agence, 8 octobre 2026"),
]

# Languedoc — Domaine Les Lys (sources/catalogue-global-2026/scan-les-lys.pdf) : les cinq vins non
# raturés, prix unique « à partir de 120 bouteilles » ; l'offre 11+1 vaut à partir de 180 cols.
# Barrés : Saint Anastasie, Librotte. Caillasses : prix raturé mais « ok » écrit à côté.
NOUVEAUX[35] = {"paliers": {"35": P(120)}, "note": HORS, "offre": "Offre 11+1 à partir de 180 cols.",
    "vins": [
        V(35, 0, "IGP Cévennes", "Aillargues", "Blanc", "2023", eu("5,70"), offre="11+1", prix_source=SCAN8),
        V(35, 0, "IGP Cévennes", "La Petite Syrah", "Rouge", "2023", eu("4,50"), offre="11+1", prix_source=SCAN8),
        V(35, 0, "AOP Duché d'Uzès", "Duché", "Rouge", "2023", eu("5,95"), prix_source=SCAN8),
        V(35, 0, "IGP Cévennes", "Caillasses", "Rouge", "2025", eu("14,90"), prix_source=SCAN8),
        V(35, 0, "IGP Cévennes", "La Soif", "Rouge", "2025", eu("3,90"), offre="11+1", prix_source=SCAN8),
    ]}

# Bordeaux — Château La Gorce (sources/catalogue-global-2026/scan-la-gorce.pdf) : les neuf vins non
# barrés, paliers 90 / 120 / 300 ; « 2019 » corrigé en 2020 sur les deux premières lignes ; les
# appellations raturées remplacées par « Médoc ». Barrés : Préface, Rosé DADA.
NOUVEAUX[26] = {"paliers": {"26": P(90, 120, 300)}, "note": FRANCO,
    "offre": "Offre possible à étudier en fonction du volume et de la référence.",
    "vins": [
        # « bio partout » (l'agence, 8 oct.) : les lignes 1-2 et 3-4 du tarif, qui ne différaient que
        # par le logo bio, sont le même vin
        V(26, 0, "AOP Médoc Cru Bourgeois", "Château la Gorce", "Rouge", "2020", eu("7,05", "7,00", "6,90"), prix_source=SCAN8),
        V(26, 0, "AOP Médoc Cru Bourgeois", "Château la Gorce", "Rouge", "2020", eu("14,15", "14,10", "14,00"), "Magnum 1,5 L", prix_source=SCAN8),
        V(26, 0, "AOP Médoc", "Prétexte", "Rouge", "2022", eu("6,60", "6,55", "6,45"), prix_source=SCAN8),
        V(26, 0, "AOP Médoc", "Rouge Intense", "Rouge", "2020", eu("6,25", "6,20", "6,10"), prix_source=SCAN8),
        V(26, 0, "AOP Médoc", "L'An 022", "Rouge", "2022", eu("9,80", "9,75", "9,65"), prix_source=SCAN8),
        V(26, 0, "AOP Médoc", "La Bonne Résolution", "Rouge", "2022", eu("6,35", "6,30", "6,20"), prix_source=SCAN8),
        V(26, 0, "AOP Médoc", "Château Canteloup", "Rouge", "2020", eu("5,10", "5,05", "4,95"), prix_source=SCAN8),
    ]}

# ——— Trichon : rose = Rhône, jaune = Bugey (scan p.28) ———
TRICHON_RHONE = {"Mas de Lusanne Rouge", "Mas de Lusanne Vacqueyras Blanc", "Mas de Lusanne Vacqueyras Rouge"}


def main():
    entrees = []
    for s in SALON["stands"]:
        s = copy.deepcopy(s)
        if s["stand"] == 12:      # Trichon : le salon avait tout sur une fiche
            bugey = [v for v in s["vins"] if v["cuvee"] not in TRICHON_RHONE]
            s["vins"] = [v for v in s["vins"] if v["cuvee"] in TRICHON_RHONE]
            for v in bugey:
                v["fiche"], v["tarif"] = 42, {"tableau": 0}
            b = copy.deepcopy(s)
            b.update({"domaines": [42], "noms_catalogue": ["Domaine Trichon"], "vins": bugey,
                      "fiche_texte": 42, "region": "Bugey",
                      "paliers_salon": {"42": s["paliers_salon"]["21"]}})
            entrees.append(b)
        if 3 in (s.get("domaines") or []):     # le Colombier gagne ses bag-in-box
            s["vins"] = s["vins"] + BIB_COLOMBIER
            s["paliers_salon"]["3:1"] = ["5 L", "10 L"]
        entrees.append(s)
    for n, x in NOUVEAUX.items():
        entrees.append({"stand": None, "nom_salon": None, "domaines": [n], "vins": x["vins"],
                        "paliers_salon": x["paliers"], "mode_prix": "unique" if x["paliers"][str(n)] == UNIQUE else "paliers",
                        "offre_salon": x["offre"], "note_prix_salon": x["note"],
                        "fiche_texte": None, "texte_reference": None,
                        # un vrai tarif remplace l'ancien « consultez-nous » (Passion des Terroirs)
                        "mentions": []})
    # la Passion des Terroirs : pas de label en tête de fiche, il est sur chaque ligne
    labels = {"25": []}
    sortie = {
        "_lisez_moi": "Écrit par scripts/prix-global.py — ne pas modifier à la main.",
        "edition": "Catalogue caviste global 2026",
        "regions": REGIONS, "ordre": ORDRE, "domaines_ajoutes": DOMAINES_AJOUTES,
        "groupes_ajoutes": GROUPES_AJOUTES, "noms_panachage": NOMS_PANACHAGE,
        "labels_entete": labels, "stands": entrees,
    }
    SORTIE.write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    fiches = {v["fiche"] for s in entrees for v in s["vins"]}
    nb = sum(len(s["vins"]) for s in entrees)
    prix = sum(len(v["prix_centimes"]) for s in entrees for v in s["vins"] if v.get("prix_centimes"))
    manque = [n for n in ORDRE if n not in fiches]
    assert not manque, f"fiches sans vin : {manque}"
    assert fiches <= set(ORDRE), f"fiches hors ordre : {fiches - set(ORDRE)}"
    print(f"✓ {SORTIE.relative_to(RACINE)} : {len(ORDRE)} fiches, {nb} vins, {prix} prix")


if __name__ == "__main__":
    main()
