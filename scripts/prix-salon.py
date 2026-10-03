#!/usr/bin/env python3
"""Les prix du Salon Privé (5 octobre 2026), relevés sur les tarifs annotés par l'agence.

Source : les scans du 3 octobre 2026 (sources/salon-prive-2026/scans-prix/Scan03102026*.pdf),
rangés par stand, et les consignes de l'agence données le même jour. Règles de l'agence :
- les prix SURLIGNÉS sont ceux à mettre ; les paliers sont ceux du tarif annoté, écrits
  « À partir de… » ; un tarif sans paliers donne un prix unique (colonne « Prix salon ») ;
- une offre (« 11+1 », « 5+1 ») se met juste après le nom du vin ;
- « offre à partir de N cols » va en bas de la fiche ; on écrit « cols », pas « bouteilles » ;
- un magnum surligné fait une ligne de plus ;
- on ne change pas les mots du catalogue.
Le relevé ligne à ligne, avec la page du scan, est dans data/prix-salon-releve.md ; les doutes
sont dans QUESTIONS.md (point 31).

Ce script écrit dans data/salon-prive-2026.json, stand par stand : `paliers_salon` (par fiche),
`offre_salon` (le bas de fiche), et vin par vin `prix_centimes`, `offre`, plus les lignes
ajoutées (`ajout`). Il se relance sans risque : les lignes qu'il a ajoutées sont d'abord retirées.
Après `npm run transcrire-matheo`, le relancer (npm run prix-salon), puis `npm run salon`.
Un prix retouché ensuite par le tableur (npm run importer-salon) serait écrasé par une
nouvelle exécution de ce script : corriger alors le prix ici aussi.
"""
import json
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data/salon-prive-2026.json"


def eu(*prix):
    """Des euros (« 7,71 ») aux centimes entiers, sans passer par un flottant."""
    out = []
    for p in prix:
        e, _, c = p.partition(",")
        out.append(int(e) * 100 + int((c + "00")[:2]))
    return out


def P(*paliers, unite="bts"):
    return [f"À partir de {n} {unite}" for n in paliers]


UNIQUE = ["Prix salon"]

# stand → paliers (pour toutes les fiches du stand, sauf mention par fiche)
PALIERS = {
    1: P(120, 180, 300), 2: P(66, 126, 186), 3: UNIQUE, 4: UNIQUE, 5: P(120, 180, 300),
    6: P(72, 300, 600, unite="cols"), 7: P(126, 246, 540, unite="cols"), 8: UNIQUE,
    9: P(60, 120, 300), 10: P(42, 120, 300), 11: UNIQUE, 12: P(120, 300, 600, unite="cols"),
    13: UNIQUE, 14: P(120, 240), 15: P(48, 78, 96), 16: UNIQUE, 17: UNIQUE, 18: UNIQUE,
    19: P(120, 180, 600), 20: P(60, 120, 300),
    21: {32: P(144, 300, unite="cols") + ["1 palette"]},   # les jus (n°33) : pas de prix au salon
    22: UNIQUE, 23: P(60, 120, 240), 24: UNIQUE, 25: P(36, 60, 120, 240, unite="cols"),
    26: P(60, 120, 300),
}

# le bas de fiche : l'offre du stand, telle que l'agence l'a dite
OFFRE = {
    1: "Offre possible en fonction du volume.",
    3: "Offre 11+1 à partir de 180 cols.",
    4: "Offre 11+1 à partir de 300 cols.",
    6: "Offre à partir de 300 cols.",
    7: "Offre 11+1 à partir de 240 cols ; offre 5+1 à partir de 540 cols.",
    8: "Offre 11+1 à partir de 42 cols.",
    9: "Offre 11+1 à partir de 240 cols.",
    13: "Offre 11+1 à partir de 180 cols.",
    14: "Offre 11+1 à partir de 240 cols.",
    16: "Offre à partir de 120 cols, en général 11+1, selon le volume.",
    17: "Offre à partir de 120 cols.",
    18: "Offre 11+1 à partir de 120 cols.",
    19: "Offre en fonction du volume.",
    20: "Offre 11+1 à partir de 120 cols.",
    23: "Offre 11+1 à partir de 120 cols.",
    24: "Offre possible à étudier en fonction du volume et de la référence.",
    25: "Offre 11+1 à partir de 120 cols.",
    26: "Offre 11+1 à partir de 126 cols.",
}

O11, O5 = "11+1", "5+1"

# stand → [(début de la ligne de la liste, prix, offre, autres champs)] dans l'ordre de la carte.
# `None` à la place des prix : pas de prix au salon (la case reste vide).
VINS = {
 1: [("Château Balac Rouge", eu("7,71", "7,59", "7,50"), None, {"millesime": "2022"}),
     ("Balac sans sulfites", eu("6,90", "6,80", "6,70"), None, {}),
     ("L'inopiné de Balac", eu("6,30", "6,20", "6,10"), None, {}),
     ("Syrah de Balac", eu("8,50", "8,40", "8,30"), None, {})],
 2: [("Trois Crus Brut", eu("15,76", "15,45", "15,16"), None, {}),
     ("Le Terroir Blanc", eu("17,54", "17,20", "16,87"), None, {}),
     ("Le Terroir Meunier", eu("17,54", "17,20", "16,87"), None, {}),
     ("Millésime Expression", eu("19,14", "18,77", "18,42"), None, {})],
 3: [("Terre Rouge", eu("7,20"), O11, {}), ("4 saisons", eu("5,40"), None, {}),
     ("La Poion", eu("3,40"), None, {}), ("Clos de Cassis", eu("8,30"), None, {}),
     ("Albas", eu("4,70"), O11, {})],
 4: [("Cuvée des deux Colombes", eu("2,95"), None, {}), ("L'Envol", eu("3,65"), None, {}),
     ("Cru Mouzillon", eu("7,30"), None, {}), ("Le Prestige de Beaulieu", eu("3,10"), O11, {}),
     ("Cuvée domaine", eu("2,85"), O11, {}), ("Rouge aux lèvres", eu("3,45"), O11, {}),
     ("La Perle", eu("4,60"), None, {})],
 5: [("AOC Mâcon Chardonnay", eu("6,10", "5,45", "5,75"), None, {}),
     ("AOC Mâcon Mancey Blanc", eu("6,70", "6,50", "6,30"), None, {}),
     ("AOC Mâcon Mancey Rouge", eu("5,75", "5,60", "5,40"), None, {}),
     ("AOC Bourgognes Passe", eu("5,75", "5,60", "5,40"), None, {}),
     ("Les Bulles du Puits", eu("6,40", "5,45", "5,75"), None, {})],
 6: [("N°1 Littorine", eu("2,68", "2,60", "2,28"), O11, {}),
     ("N°6 Fossiles", eu("2,99", "2,91", "2,56"), O11, {}),
     ("N°3 Gulf Stream", eu("2,99", "2,91", "2,56"), O5, {}),
     ("N°4 Triton", eu("2,99", "2,91", "2,56"), O5, {"offre_detail": "dès 200 cols"}),   # l'agence, à l'oral
     ("N°8 Grand Pavois", eu("3,98", "3,87", "3,40"), None, {}),
     ("N°7 Vénus", eu("3,45", "3,35", "3,08"), O11, {}),
     ("N°10 Pétillant", eu("4,00", "3,90", "3,60"), O5, {"offre_detail": "dès 250 cols"})],
 7: [("Chardonnay-Viognier", eu("4,80", "4,50", "4,20"), O5, {"contenance": "75 cl"}),
     ("Syrah Rouge", eu("4,80", "4,50", "4,20"), O5, {}),
     ("Terroir d'Ansouis Blanc", eu("5,50", "5,20", "5,00"), O5, {}),
     ("Le Prieuré Rouge", eu("5,70", "5,40", "5,20"), O11, {}),
     ("Vieilles Vignes Rouge 2022", eu("18,00", "17,50", "17,00"), O11, {}),
     ("Vieilles Vignes Rouge 2023", eu("18,00", "17,50", "17,00"), O5, {}),
     ("Le Couchant", eu("27,00", "26,50", "26,00"), O11, {"contenance": "75 cl"}),
     ("Premières Fleurs Blanc", eu("5,50", "5,20", "5,00"), O11, {}),
     ("Premières Fleurs Rouge", eu("5,50", "5,20", "5,00"), O11, {"contenance": "75 cl"}),
     ("Or des Dentelles Blanc Moelleux 2023", eu("7,90", "7,40", "6,90"), O11, {"contenance": "75 cl"}),
     ("Or des Dentelles Blanc Moelleux 2022", eu("4,70", "4,40", "4,10"), O11, {"contenance": "37,5 cl"}),
     ("Côtes du Rhône Rouge", eu("5,70", "5,40", "5,20"), O5, {})],
 8: [("Les demoiseilles", eu("9,50"), O11, {}), ("Château Falfas 2020", eu("12,30"), O11, {}),
     ("Château Falfas 2021", eu("12,30"), O11, {}), ("Château Falfas 2022", eu("12,40"), O11, {}),
     ("Château Falfas Chevalier 2017", eu("24,20"), None, {}),
     ("Château Falfas Chevalier 2019", eu("23,90"), O11, {}),
     ("Château Falfas 2023", eu("20,10"), O11, {})],
 9: [("AOC Crémant", eu("8,70", "8,10", "7,60"), None, {}),
     ("Molse Blanc", eu("6,80", "6,40", "5,90"), None, {}),
     ("Molse Rouge", eu("8,40", "7,80", "7,30"), O11, {}),
     ("Leimen Sylvaner", eu("8,70", "8,10", "7,60"), None, {}),
     ("Riesling Holderhurst", eu("8,70", "8,10", "7,60"), O11, {}),
     ("Riesling Hahnenberg", eu("11,40", "11,00", "10,50"), None, {}),
     ("Gewurztraminer Grand Cru", eu("15,40", "14,90", "14,20"), None, {}),
     ("Riesling Grand Cru", eu("18,80", "18,20", "17,30"), O11, {}),
     ("Seiler Rouge", eu("10,30", "9,90", "9,50"), O11, {})],
 10: [("AOC Anjou Blanc", eu("13,25", "12,25", "11,75"), None, {}),
      ("La Grange Jaumain Blanc", eu("9,50", "9,25", "9,00"), None, {}),
      ("AOC Saumur Blanc", eu("14,50", "13,50", "13,00"), None, {}),
      ("AOC Quincy", eu("17,85", "16,50", "15,50"), None, {}),
      ("Les Villaudes", eu("18,00", "16,50", "15,50"), None, {}),
      ("La Grange Jaumain Rouge", eu("10,60", "10,60", "10,60"), None, {"contenance": "75 cl"}),
      ("Franc Rouge", eu("13,75", "12,85", "12,25"), None, {}),
      ("Cravant Rouge", eu("17,00", "15,75", "14,75"), None, {"contenance": "75 cl"}),
      ("La Grange Jaumain Les Soudannes", eu("9,50", "9,25", "9,00"), None, {})],
 11: [("Vogloniers Brut", eu("19,96"), None, {}), ("Nature Brut", eu("25,41"), None, {}),
      ("Chardonnay Extra-Brut", eu("26,48"), None, {}), ("Supernova", eu("36,83"), None, {})],
 12: [("Mas de Lusanne Brut Blanc", eu("7,43", "6,90", "6,73"), None, {"contenance": "75 cl"}),
      ("Mas de Lusanne Extra-Brut", eu("7,43", "6,90", "6,73"), None, {"contenance": "75 cl"}),
      ("Mas de Lusanne Mondeuse", eu("7,38", "6,98", "6,58"), None, {"contenance": "75 cl"}),
      ("Mas de Lusanne Pinot Noir", eu("6,99", "6,67", "6,35"), None, {"contenance": "75 cl"}),
      ("Mas de Lusanne  Rouge 2024", eu("4,80", "4,67", "4,54"), None, {}),
      ("Mas de Lusanne Gamay", eu("5,85", "5,59", "5,32"), O11, {"contenance": "75 cl"}),
      ("Mas de Lusanne Chardonnay", eu("7,25", "6,80", "6,35"), O11, {"contenance": "75 cl"}),
      ("Mas de Lusanne Vacqueyras Blanc", eu("9,55", "9,12", "8,68"), None, {}),
      ("Mas de Lusanne Vacqueyras Rouge", eu("9,35", "8,93", "8,50"), None, {}),
      ("Mas de Lusanne Pétillant", eu("5,08", "5,08", "5,08"), None, {"contenance": "75 cl"})],
 13: [("Léon Rouge", eu("4,85"), O11, {}), ("Lou Daro", eu("6,70"), O11, {}),
      ("Henri", eu("4,85"), O11, {}), ("Juliette Blanc", eu("4,85"), O11, {}),
      ("Grain de Blanc", eu("6,70"), O11, {})],
 14: [("AOC Anjou Blanc 2024", eu("3,60", "3,40"), None, {}),
      ("AOC Anjou Blanc 2024 - Promenade", eu("5,70", "5,60"), O11, {}),
      ("AOC Sauvignon", eu("3,60", "3,40"), O11, {}),
      ("AOC Coteaux du Layon 2025", eu("5,70", "5,60"), O11, {}),
      ("AOC Coteaux du Layon Faye", eu("9,70", "9,60"), None, {}),
      ("AOC Crémant de Loire", eu("5,80", "5,60"), O11, {}),
      ("AOC Rosé de Loire", eu("3,50", "3,30"), None, {})],
 15: [("Cuvée Camille", eu("20,10", "19,90", "19,60"), None, {}),
      ("Brut Réserve", eu("20,80", "20,60", "20,30"), None, {}),
      ("Rosé Brut", eu("22,90", "22,70", "22,40"), None, {"contenance": "75 cl"}),
      ("Spécial Club", eu("41,10", "40,90", "40,60"), None, {}),
      ("Extra Brut", eu("25,00", "24,80", "24,50"), None, {}),
      ("82/18", eu("51,80", "51,60", "51,30"), None, {"contenance": "75 cl"})],
 16: [("Cuvée Diane", eu("9,90"), None, {}), ("Cuvée TerraCotta", eu("8,90"), None, {}),
      ("Cuvée des Fontenelles", eu("7,50"), None, {})],
 17: [("AOC Menetou Rouge", eu("9,25"), None, {"contenance": "75 cl"}),
      ("AOC Menetou Blanc", eu("9,25"), None, {"contenance": "75 cl"}),
      ("AOC Quincy", eu("9,20"), None, {"contenance": "75 cl"}),
      ("Les Beltins", eu("25,40"), None, {"contenance": "75 cl"}),
      ("Chêne à la Rouline", eu("25,40"), None, {"contenance": "75 cl"}),
      ("Vignes de Tréleau", eu("25,40"), None, {"contenance": "75 cl"}),
      ("La Louisonne", eu("25,40"), None, {"contenance": "75 cl"}),
      ("AOC Pouilly-Fumé 2025", eu("11,50"), None, {"contenance": "75 cl"}),
      ("AOC Touraine Chenonceaux", eu("6,15"), None, {"contenance": "75 cl"}),
      ("AOC Sauvignon Blanc", eu("4,70"), None, {"contenance": "75 cl"}),
      ("AOC Pinot Noir Rosé", eu("4,45"), None, {"contenance": "75 cl"}),
      ("AOC Pinot Noir 2024", eu("4,50"), None, {"contenance": "75 cl"})],
 18: [("AOC Hautes Côtes de Beaune", eu("13,50"), O11, {}), ("AOC Meursault", eu("35,00"), None, {}),
      ("Les Aigrots 2023", eu("24,00"), None, {}), ("Clos de la Perrière", eu("14,50"), O11, {}),
      ("Les Bons Feuvres", eu("18,00"), O11, {}), ("Les Aigrots 2024", eu("22,00"), O11, {}),
      ("Les Perrières", eu("24,00"), O11, {})],
 19: [("Sainte-Probace Rosé", eu("5,30", "5,15", "4,85"), None, {}),
      ("Sainte-Probace Blanc", eu("5,50", "5,35", "4,85"), None, {}),
      ("Sainte-Probace Rouge", eu("5,50", "5,35", "4,85"), None, {"contenance": "75 cl"}),
      ("Joio Rosé", eu("6,30", "6,15", "5,90"), None, {}),
      ("Joio Blanc", eu("6,30", "6,15", "5,95"), None, {}),
      ("Joio Rouge", eu("6,40", "6,25", "6,10"), None, {}),
      ("Miraia Blanc", eu("9,30", "9,05", "8,80"), None, {"contenance": "75 cl"}),
      ("Miraia Rouge", eu("8,70", "8,55", "8,30"), None, {"contenance": "75 cl"}),
      ("Aquino Rouge", eu("16,30", "16,00", "15,60"), None, {"contenance": "75 cl"}),
      ("Aquino Blanc", eu("16,30", "16,00", "15,60"), None, {"contenance": "75 cl"})],
 20: [("Stratéus Rouge", eu("11,45", "11,00", "10,50"), O11, {}),
      ("Néolithik Rouge", eu("14,00", "12,50", "12,00"), O11, {}),
      ("Koloss Rouge", eu("6,50", "6,00", "5,50"), O11, {}),
      ("Koloss Doux", eu("6,50", "6,00", "5,50"), O11, {}),
      ("Stratéus Blanc", eu("11,45", "11,00", "10,50"), O11, {}),
      ("Néolithik Blanc", eu("14,00", "12,50", "12,00"), O11, {})],
 21: [("Chant de Lune", eu("7,78", "7,16", "6,13"), O11, {}),
      ("Rouge Serame", eu("7,78", "7,16", "6,13"), O11, {}),
      ("Blanc Serame", eu("7,78", "7,16", "6,13"), O11, {}),
      ("Oena", eu("14,00", "14,00", "14,00"), None, {}),
      ("Jardin de Corbières", eu("4,74", "4,36", "4,08"), O11, {}),
      ("Jus de cépages — Syrah", None, None, {}),
      ("Jus de cépages — Chardonnay", None, None, {}),
      ("Jus de cépages — Grenache", None, None, {})],
 22: [("Les Silex", eu("4,25"), None, {}), ("Les Gorinières", eu("7,84"), None, {}),
      ("Les Courbes", eu("7,23"), O11, {}), ("Les Amphibol", eu("5,66"), None, {}),
      ("Les Gneiss", eu("5,13"), O11, {}), ("Le Bois Bouquet", eu("6,72"), None, {}),
      ("L'O Brut", eu("6,28"), None, {})],
 23: [("Terre de Solemme", eu("21,20", "20,50", "20,00"), None, {}),
      ("Plénitude de Solemme", eu("22,10", "21,60", "21,10"), O11, {}),
      ("Esprit de Solemme", eu("25,80", "25,10", "24,50"), None, {}),
      ("Nature de Solemme", eu("32,00", "31,20", "30,50"), None, {}),
      ("Ambre de Solemme", eu("33,50", "32,60", "31,85"), None, {}),
      ("Rose de Solemme", eu("36,00", "35,10", "34,20"), None, {})],
 24: [("Château Lafargue", eu("6,90"), None, {}), ("Amphora", eu("10,10"), None, {}),
      ("La Confiance", eu("8,45"), None, {})],
 25: [("Courant Chenin", eu("6,95", "6,45", "5,95", "5,75"), O11, {}),
      ("Source Melon", eu("5,95", "5,45", "4,95", "4,75"), O11, {}),
      ("Reflet Gamay", eu("6,95", "6,45", "5,95", "5,75"), O11, {}),
      ("L'Eberluant", eu("6,95", "6,45", "5,95", "5,75"), None, {})],
 26: [("AOP Bourgogne Chardonnay", eu("8,90", "8,60", "8,10"), O11, {}),
      ("AOC Pouilly-Vinzelles", eu("15,30", "15,00", "14,30"), O11, {}),
      ("AOC Auxey-Duresses", eu("22,50", "22,20", "21,20"), O11, {}),
      ("Baron Auguste Blanc", eu("9,30", "9,00", "8,40"), O11, {}),
      ("Baron Auguste Rosé", eu("9,30", "9,00", "8,40"), O11, {}),
      ("Domaine les Guignottes Rouge", eu("8,90", "8,60", "8,10"), O11, {}),
      ("AOC Chassagne-Montrachet", eu("23,90", "23,60", "22,60"), O11, {}),
      ("Aux Allots", eu("33,90", "33,60", "32,30"), O11, {}),
      ("AOC Mercurey Blanc", eu("15,70", "15,40", "14,60"), None, {}),
      ("AOC Mercurey Rouge", eu("16,50", "16,20", "15,40"), None, {}),
      ("AOC Givry", eu("16,50", "16,20", "15,40"), None, {}),
      ("AOC Gervey-Chambertin", eu("43,50", "43,20", "41,60"), None, {})],
}

# Les lignes en plus : un magnum surligné, un millésime de plus, un vin à rajouter.
# (stand, après la ligne qui commence par…, champs). `liste_vins` : figure aussi dans la liste
# des vins dégustés (False pour les magnums, qui ne sont pas sur la carte de Mathéo).
AJOUTS = [
 (1, "Château Balac Rouge", dict(fiche=29, appellation="AOC Haut-Médoc Cru Bourgeois Supérieur",
     cuvee="Château Balac Rouge", couleur="Rouge", millesime="2018", contenance=None,
     prix_centimes=eu("7,25", "7,13", "7,00"), liste_vins=True,
     source="mail d'Amélie Touchais du 3 octobre (scan 1, p.3) : 2018 et 2022 surlignés")),
 (3, "Terre Rouge", dict(fiche=36, tarif={"tableau": 0, "ligne": 4}, appellation="AOC Corbières",
     cuvee="Terre Rouge", couleur="Rouge", millesime="2022/2024", contenance="Magnum 1,5 L",
     prix_centimes=eu("17,90"), liste_vins=False, source="tarif 2026 annoté (scan 1, p.5)")),
 (3, "4 saisons", dict(fiche=36, tarif={"tableau": 0, "ligne": 6}, appellation="AOC Corbières",
     cuvee="4 saisons", couleur="Rouge", millesime="2023/2024", contenance="Magnum 1,5 L",
     prix_centimes=eu("13,40"), liste_vins=False, source="tarif 2026 annoté (scan 1, p.5)")),
 (3, "Clos de Cassis", dict(fiche=36, tarif={"tableau": 0, "ligne": 1}, appellation="AOC Corbières",
     cuvee="Clos de Cassis", couleur="Rouge", millesime="2022/2023", contenance="Magnum 1,5 L",
     prix_centimes=eu("20,80"), liste_vins=False, source="tarif 2026 annoté (scan 1, p.5)")),
 (7, "Or des Dentelles Blanc Moelleux 2022", dict(fiche=17, tarif={"tableau": 0, "ligne": 1},
     appellation="Beaumes de Venise", cuvee="Les Jumelles Rouge", couleur="Rouge", millesime="—",
     contenance="75 cl", prix_centimes=eu("6,50", "6,00", "5,50"), offre=O11, liste_vins=True,
     source="carte du stand 7 annotée « Rajouter Beaumes de Venise » (scan 1, p.10) ; "
            "tarif juillet 2026 de Coyeux, millésime 2023 barré (scan 1, p.19)")),
 (15, "Brut Réserve", dict(fiche=40, tarif={"tableau": 0, "ligne": 1}, appellation="Grand Cru Chouilly",
     cuvee="Brut Réserve Blanc de Blancs", couleur="Blanc de Blancs", millesime="—",
     contenance="Magnum 1,5 L", prix_centimes=eu("47,90", "47,50", "46,90"), liste_vins=False,
     source="tarif 2026 annoté (scan 2, p.13)")),
 (21, "Chant de Lune", dict(fiche=32, tarif={"tableau": 0, "ligne": 11}, appellation="AOC Minervois",
     cuvee="Chant de Lune Rouge, disponible en décembre 2026", couleur="Rouge", millesime="—",
     contenance="Magnum 1,5 L", prix_centimes=eu("16,00", "14,72", "12,60"), liste_vins=False,
     source="tarif « Salon Vins & Terroirs 05 octobre 2026 » (scan 4, p.2)")),
 (21, "Jardin de Corbières", dict(fiche=32, tarif={"tableau": 0, "ligne": 4}, appellation="AOC Corbières",
     cuvee="Jardins de Corbières Rouge, disponible en décembre 2026", couleur="Rouge", millesime="—",
     contenance="Magnum 1,5 L", prix_centimes=eu("9,91", "9,12", "7,81"), liste_vins=False,
     source="tarif « Salon Vins & Terroirs 05 octobre 2026 » (scan 4, p.2)")),
 (23, "Plénitude de Solemme", dict(fiche=39, tarif={"tableau": 0, "ligne": 1},
     appellation="Premier Cru Champagne", cuvee="Plénitude de Solemme Extra-Brut",
     couleur="Blanc extra brut", millesime="2022", contenance="Magnum 1,5 L",
     prix_centimes=eu("58,00"), liste_vins=False,
     source="tarif annoté (scan 4, p.4) : un seul prix pour le magnum")),
]


def norm(t):
    return " ".join(str(t).replace("’", "'").split())


def main():
    salon = json.loads(FICHIER.read_text(encoding="utf-8"))
    erreurs, n_prix, n_vides, n_offres = [], 0, 0, 0
    for st in salon["stands"]:
        n = st["stand"]
        st["vins"] = [v for v in st["vins"] if not v.get("ajout")]
        # paliers, par fiche
        pal = PALIERS[n]
        par_fiche = pal if isinstance(pal, dict) else {f: pal for f in st["domaines"]}
        st["paliers_salon"] = {str(f): p for f, p in par_fiche.items()}
        st["mode_prix"] = "unique" if all(p == UNIQUE for p in par_fiche.values()) else "paliers"
        if OFFRE.get(n):
            st["offre_salon"] = OFFRE[n]
        else:
            st.pop("offre_salon", None)
        # les vins de la carte, dans l'ordre
        spec = VINS[n]
        if len(spec) != len(st["vins"]):
            erreurs.append(f"stand {n} : {len(spec)} prix pour {len(st['vins'])} vins")
            continue
        for (debut, prix, offre, autres), v in zip(spec, st["vins"]):
            if not norm(v["liste"]).startswith(norm(debut)):
                erreurs.append(f"stand {n} : « {debut} » ne correspond pas à « {v['liste']} »")
                continue
            paliers = par_fiche.get(v["fiche"])
            if prix is not None and paliers is not None and len(prix) not in (1, len(paliers)):
                erreurs.append(f"stand {n} « {debut} » : {len(prix)} prix pour {len(paliers)} paliers")
            v["prix_centimes"] = prix
            for k in ("offre", "offre_detail"):
                v.pop(k, None)
            if offre:
                v["offre"] = offre
                n_offres += 1
            for k, val in autres.items():
                v[k] = val
            v["prix_source"] = "scans de l'agence, 3 octobre 2026"
            n_prix += prix is not None
            n_vides += prix is None
        # les lignes en plus
        for (s, apres, champs) in [a for a in AJOUTS if a[0] == n]:
            i = next((k for k, v in enumerate(st["vins"]) if norm(v["liste"]).startswith(norm(apres))), None)
            if i is None:
                erreurs.append(f"stand {n} : pas de ligne « {apres} » pour l'ajout")
                continue
            while i + 1 < len(st["vins"]) and st["vins"][i + 1].get("ajout"):
                i += 1
            ligne = {"liste": f"(ajout) {champs['cuvee']} {champs['millesime']} {champs['contenance'] or ''}".strip(),
                     "ajout": True, "tarif": None, "note": None, "ecarts": [], **champs}
            if ligne.get("offre"):
                n_offres += 1
            st["vins"].insert(i + 1, ligne)
            n_prix += 1
    if erreurs:
        print("✗ " + "\n✗ ".join(erreurs))
        sys.exit(1)
    salon["_prix"] = ("Prix du salon, en centimes, vin par vin (`prix_centimes`), relevés sur les tarifs "
                      "annotés par l'agence (scans du 3 octobre 2026) par scripts/prix-salon.py. "
                      "`paliers_salon` : les intitulés de colonnes, par fiche ; « Prix salon » = prix unique. "
                      "Un seul prix sur une ligne à plusieurs paliers : un prix unique pour cette ligne. "
                      "null = case vide. `offre` : l'offre du vin (11+1, 5+1) ; `offre_salon` : le bas de fiche.")
    FICHIER.write_text(json.dumps(salon, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"✓ prix du salon : {n_prix} lignes avec prix, {n_vides} sans prix, {n_offres} offres, "
          f"{sum(1 for a in AJOUTS)} lignes ajoutées")


if __name__ == "__main__":
    main()
