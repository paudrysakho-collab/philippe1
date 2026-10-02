#!/usr/bin/env python3
"""Les vins dégustés au Salon Privé : transcription du fichier de Mathéo, rapprochée du tarif.

Le fichier de Mathéo (reçu le 2 octobre 2026) est identique, octet pour octet, au Padlet
déjà déposé : sources/salon-prive-2026/padlet-vins-a-deguster.pdf. Il fait foi pour la
LISTE des vins dégustés. On n'en lit que les cartes de stand (pages 3 à 20) ; la page 1
(liste des domaines) et la page 2 (plan « version esthétique ») sont de l'habillage.
Sur les pages doubles, deux stands sont côte à côte, séparés par un trait vertical :
chaque colonne est transcrite à part (`colonne`).

Chaque vin est rapproché d'une ligne du tarif (data/fiches/NN.json : tableau, ligne).
Règle d'affichage, notée dans JOURNAL.md :
- la liste de Mathéo décide QUELS vins figurent, et leur millésime (la bouteille ouverte) ;
- pour un vin rapproché, appellation, cuvée, couleur et contenance viennent du tarif, seule
  source des faits ; tout désaccord avec la liste est noté dans `ecarts` et dans QUESTIONS.md ;
- un vin absent du tarif, ou qu'on ne peut rapprocher d'une seule ligne, s'affiche tel que
  la liste l'écrit (corrections de forme seulement), avec `tarif: null`, et va dans QUESTIONS.md ;
  ce qui le distingue d'un voisin (« Brut Blanc », « Rosé »…) reste dans son nom, puisque le
  tableau ne montre la couleur que par un picto ;
- un doublon de la liste n'est affiché qu'une fois (`doublons_matheo`).

Le script écrit `carte_matheo`, `vins` et `doublons_matheo` dans data/salon-prive-2026.json.
Il garde les prix déjà saisis (`prix_centimes`) d'un vin à l'autre, repérés par stand et
par ligne de la liste. Il ne sert qu'à refaire la transcription : les prix se saisissent
ensuite dans le JSON ou par le tableur (npm run tableur-salon / importer-salon).
"""
import json
import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data/salon-prive-2026.json"
fiches = {int(p.stem): json.loads(p.read_text(encoding="utf-8"))
          for p in (RACINE / "data/fiches").glob("*.json")}

# Rapprochement : (fiche, tableau, ligne) ; ou (fiche, None, {champs tels que la liste les écrit}).
# `ecart` : ce qui diffère entre la liste et le tarif, hors millésime (calculé plus bas).
# `doublon` : la ligne répète la précédente à l'identique ; elle n'est pas affichée.
def T(fiche, tableau, ligne, ecart=None):
    return {"fiche": fiche, "tarif": (tableau, ligne), "ecart": ecart}


def L(fiche, ecart=None, **champs):
    return {"fiche": fiche, "tarif": None, "ecart": ecart, "champs": champs}


DOUBLON = {"doublon": True}

STANDS = {
 1: dict(page=3, colonne="pleine page", nom="01 - Château Balac", vins=[
  ("Château Balac — AOC Cru Bourgeois Haut Médoc",
   L(29, appellation="AOC Cru Bourgeois Haut-Médoc", cuvee="Château Balac")),
  ("Balac sans sulfites 2022 — VDF", T(29, 0, 1)),
  ("L'inopine de Balac 2021 — VDF", T(29, 0, 0)),
  ("Syrah de Balac 2022 —VDF", T(29, 0, 2)),
 ]),
 2: dict(page=4, colonne="gauche", nom="02 — Champagne Denis Frézier", vins=[
  ("Trois Crus Brut — AOC Champagne", T(38, 0, 5, "le tarif a aussi une demi-bouteille (37,5 cl) ; la ligne retenue est la 75 cl")),
  ("Le Terroir Blanc Blanc de Blanc Brut — AOC Champagne", T(38, 0, 1)),
  ("le Terroir Meunier Blanc de Meuniers Extra-Brut — AOC Champagne", T(38, 0, 3)),
  ("Brut Nature — AOC Champagne", L(38, appellation="AOC Champagne", cuvee="Brut Nature")),
  ("Millésime Expression 2018 — AOC Champagne",
   L(38, appellation="AOC Champagne", cuvee="Millésime Expression", millesime="2018")),
 ]),
 3: dict(page=4, colonne="droite", nom="03 — Domaine Prieuré Sainte Marie D'Albas", vins=[
  ("Terre Rouge 2024 — AOC Corbières", T(36, 0, 3, "le tarif a aussi un magnum ; la ligne retenue est la 75 cl")),
  ("4 saisons 2024 — AOC Corbières", T(36, 0, 5, "le tarif a aussi un magnum ; la ligne retenue est la 75 cl")),
  ("La Poion 2024 — AOC Corbières", T(36, 0, 8, "« La Poion » dans la liste, « La Potion » au tarif")),
  ("Clos De Cassis 2023 — AOC Corbières", T(36, 0, 0, "le tarif a aussi un magnum ; la ligne retenue est la 75 cl")),
  ("Albas 2025— IGP Pays D'OC", T(36, 0, 11)),
 ]),
 4: dict(page=5, colonne="gauche", nom="04 — Domaine du Colombier / J.Y. Bretaudeau", vins=[
  ("Cuvée des deux Colombes 2025 — AOC Muscadet Sèvre et Maine", T(3, 0, 0)),
  ("L'envol 2023 — AOC Muscadet Sèvre et Maine",
   L(3, appellation="AOC Muscadet Sèvre et Maine", cuvee="L'envol", millesime="2023")),
  ("Cru Mouzillon-Tillières 2022 — AOC Muscadet Sèvre et Maine", T(3, 0, 1)),
  ("Le prestige de Beaulieu 2024 — IGP Chardonnay", T(3, 0, 2)),
  ("Cuvée domaine 2025 — IGP Sauvignon Gris", T(3, 0, 3)),
  ("Rouge au lèvres — IGP Val de Loire", T(3, 0, 6)),
  ("La perle — Méthode Trad", T(3, 0, 7)),
 ]),
 5: dict(page=5, colonne="droite", nom="05 — Domaine des Verchères", vins=[
  ("AOC Mâcon Chardonnay 2025", T(15, 0, 0)),
  ("AOC Mâcon Mancey Blanc 2024", T(15, 0, 1)),
  ("AOC Mâcon Rouge 2024", T(15, 0, 2, "« Mâcon Rouge » dans la liste ; le seul Mâcon rouge du tarif est le Mâcon Mancey rouge 2024")),
  ("AOC Bourgognes Passe-Tout-Grain 2025",
   L(15, appellation="AOC Bourgogne Passe-Tout-Grain", millesime="2025")),
  ("Les Bulles du Puits", L(15, cuvee="Les Bulles du Puits")),
 ]),
 6: dict(page=6, colonne="pleine page", nom="06 — Domaine Haut Marin", vins=[
  ("N°1 Littorine Blanc 2025 — IGP Côtes de Gascogne", T(23, 0, 0)),
  ("N°6 Fossiles Blanc 2025 — IGP Côtes de Gascogne", T(23, 0, 2)),
  ("N°3 Gulf Stream Rosé 2025 — IGP Côtes de Gascogne", T(23, 0, 6)),
  ("N°4 Triton Rouge 2024 — IGP Côtes de Gascogne", T(23, 0, 7)),
  ("N°8 Grand Pavois Rouge 2025 — IGP Côtes de Gascogne", T(23, 0, 5, "« Rouge » dans la liste, « Doux » au tarif")),
  ("N°7 Vénus Blanc Moelleux 2025 — IGP Côtes de Gascogne", T(23, 0, 4)),
  ("N°10 Pétillant — IGP Côtes de Gascogne",
   L(23, "le tarif a deux N°10, en Vin de France : Bulle/Blanc et Bulle/Rosé ; la liste ne dit pas lequel, et écrit IGP Côtes de Gascogne",
     appellation="IGP Côtes de Gascogne", cuvee="N°10", couleur="Pétillant")),
 ]),
 7: dict(page=7, colonne="pleine page (quatre rubriques)", nom="07 — Vignoble Strasser Radziwill", vins=[
  ("[Domaine de la Pousterle] Chardonnay-Viognier Blanc 2024 — VDF",
   L(19, "peut-être « La Pousterle » blanc, Vin de France 2022, au tarif ; le nom et le millésime diffèrent",
     appellation="Vin de France", cuvee="Chardonnay-Viognier", couleur="Blanc", millesime="2024")),
  ("[Domaine de la Pousterle] Syrah Rouge 2022 — VDF", T(19, 0, 1)),
  ("[Domaine de la Pousterle] Terroir d'Ansouis Blanc 2021 — AOC Luberon", T(19, 0, 3)),
  ("[Domaine de la Pousterle] Terroir d'Ansouis Blanc 2021 — AOC Luberon", DOUBLON),
  ("[Domaine Les Prieuré des Papes] Le Prieuré Rouge 2024— AOC Côtes du Rhône", T(16, 0, 0)),
  ("[Domaine Les Prieuré des Papes] Vieilles Vignes Rouge 2022— AOC Châteauneuf-du-Pape", T(16, 0, 1)),
  ("[Domaine Les Prieuré des Papes] Vieilles Vignes Rouge 2023 — AOC Châteauneuf-du-Pape", T(16, 0, 1)),
  ("[Domaine Les Prieuré des Papes] Le Couchant Rouge 2020 — AOC Châteauneuf-du-Pape",
   L(16, appellation="AOC Châteauneuf-du-Pape", cuvee="Le Couchant", couleur="Rouge", millesime="2020")),
  ("[Domaine de Coyeux] Premières Fleurs Blanc — IGP Méditérranée", T(17, 0, 4)),
  ("[Domaine de Coyeux] Premières Fleurs 2025 — IGP Méditérranée",
   L(17, "sans couleur dans la liste ; au tarif, « Première Fleur » est un blanc sans millésime, et le seul rouge IGP Méditerranée (2022) n'a pas de nom de cuvée",
     appellation="IGP Méditerranée", cuvee="Premières Fleurs", millesime="2025")),
  ("[Domaine de Coyeux] Or des Dentelles 2023 — AOC Muscat BDV",
   L(17, appellation="AOC Muscat BDV", cuvee="Or des Dentelles", millesime="2023")),
  ("[Domaine de Coyeux] Or des Dentelles 2022 — AOC Muscat BDV",
   L(17, appellation="AOC Muscat BDV", cuvee="Or des Dentelles", millesime="2022")),
  ("[Domaine du Moulin Blanc] Côtes du Rhône 2023 Rouge — AOC Côtes du Rhône", T(18, 0, 2)),
 ]),
 8: dict(page=8, colonne="gauche", nom="08 — Château Falfas", vins=[
  ("Les demoiselles de Falfas 2025— AOC Côtes de Bourg", T(27, 0, 0)),
  ("Château Falfas 2020 — AOC Côtes de Bourg", T(27, 0, 1)),
  ("Château Falfas 2021 — AOC Côtes de Bourg", T(27, 0, 1)),
  ("Château Falfas 2022 — AOC Côtes de Bourg", T(27, 0, 1)),
  ("Château Falfas Chevalier 2017— AOC Côtes de Bourg", T(27, 0, 2)),
  ("Château Falfas Chevalier 2019— AOC Côtes de Bourg", T(27, 0, 2)),
  ("Château Falfas 2023— AOC Côtes de Bourg", T(27, 0, 1)),
 ]),
 9: dict(page=8, colonne="droite", nom="09 — Domaine Boheler", vins=[
  ("AOC Crément D'Alsace 2024", T(8, 0, 12)),
  ("Molsce Blanc 2024— AOC Alsace", T(8, 0, 3)),
  ("Molsce Blanc 2024— AOC Alsace", DOUBLON),
  ("Leimen Sylvaner 2024— AOC Alsace", T(8, 0, 5)),
  ("Riesling Holderhurst 2023— AOC Alsace", T(8, 0, 8)),
  ("Riesling Hahnenberg 2024— AOC Alsace", T(8, 0, 9)),
  ("Gewurztraminer Grand Cru Bruderthal 2023", T(8, 0, 11)),
  ("Riesling Grand Cru Bruderthal 2023", T(8, 0, 10)),
 ]),
 10: dict(page=9, colonne="pleine page (deux colonnes de liste)", nom="10 — François Reverdy", vins=[
  ("AOP Anjou Blanc 2023", T(1, 0, 0)),
  ("La Grange Jaumain Blanc 2025 — IGP Val de Loire", T(1, 0, 6)),
  ("AOP Saumur Blanc 2024", T(1, 0, 1)),
  ("AOP Quincy 2023", T(1, 0, 3)),
  ("Les Villaudes - AOP Sancerre Blanc 2025", T(1, 0, 4)),
  ("La Grange Jaumain 2024 - Grolleau Noir",
   L(1, "le tarif a « François Reverdy – Grolleau Noir » (Vin de France rouge 2024) et « La Grange Jaumain – Les Soudannes » (IGP Val de Loire rouge) ; la liste mêle les deux noms",
     cuvee="La Grange Jaumain – Grolleau Noir", millesime="2024")),
  ("Franc 2021 - AOP Chinon Rouge 2021", T(1, 0, 2)),
  ("Cravant - AOP Chinon Rouge 2024",
   L(1, "peut-être le 2024 de « Franc / Graves » (AOP Chinon, 2021/2024) au tarif ; « Cravant » n'y figure pas",
     appellation="AOP Chinon", cuvee="Cravant", couleur="Rouge", millesime="2024")),
 ]),
 11: dict(page=10, colonne="pleine page", nom="11 — Champagne Dekeyne", vins=[
  ("Vogloniers Brut - AOC Champagne", T(37, 0, 2, "« Brut » dans la liste, « Blanc extra brut » au tarif")),
  ("Nature Sec - AOC Champagne", T(37, 0, 1, "« Nature Sec » dans la liste, « Nature », blanc extra brut, au tarif")),
  ("Chardonnay Extra-Brut — AOC Champagne", T(37, 0, 0)),
  ("Supernova Extra-Brut Zero Dosage— AOC Champagne",
   L(37, appellation="AOC Champagne", cuvee="Supernova Extra-Brut Zéro Dosage", couleur="Extra-brut, zéro dosage")),
 ]),
 12: dict(page=11, colonne="pleine page (deux colonnes de liste)", nom="12 — Domaine Trichon", vins=[
  ("Mas de Lusanne Brut Blanc— AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Brut Blanc", couleur="Blanc brut")),
  ("Mas de Lusanne Extra-Brut Blanc — AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Extra-Brut Blanc", couleur="Blanc extra-brut")),
  ("Mas de Lusanne Mondeuse 2023— AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Mondeuse", millesime="2023")),
  ("Mas de Lusanne Pinot Noir 2023 — AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Pinot Noir", millesime="2023")),
  ("Mas de Lusanne  2024 — AOC Côtes Du Rhône", T(21, 0, 0, "« Mas de Lusanne » dans la liste, sans couleur ; au tarif, le seul Côtes du Rhône est un rouge")),
  ("Mas de Lusanne Pétillant de Jus de Raisin 0 %",
   L(21, cuvee="Mas de Lusanne Pétillant de Jus de Raisin 0 %", couleur="Pétillant de jus de raisin, 0 %", famille="jus")),
  ("Mas de Lusanne Gamay— AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Gamay")),
  ("Mas de Lusanne Chardonnay 2020 — AOC Bugey",
   L(21, appellation="AOC Bugey", cuvee="Mas de Lusanne Chardonnay", millesime="2020")),
  ("Mas de Lusanne Vacqueyras Blanc 2025 — AOC Vacqueyras", T(21, 0, 1)),
  ("Mas de Lusanne Vacqueyras Rouge 2023 — AOC Vacqueyras", T(21, 0, 2)),
 ]),
 13: dict(page=12, colonne="gauche", nom="13 — Château de Gragnos", vins=[
  ("Léon 2024 — VDF", T(34, 0, 1)),
  ("Lou Daro 2023 — AOC Saint-Chinian", T(34, 0, 3)),
  ("Henri 2024 — AOC Saint-Chinian", T(34, 0, 0)),
  ("Juliette 2025 — AOC Saint-Chinian",
   L(34, appellation="AOC Saint-Chinian", cuvee="Juliette", millesime="2025")),
  ("Grain de Blanc  2025 - IGP Pays D'Hérault Monts de la Grage",
   T(34, 0, 4, "« IGP Pays d'Hérault Monts de la Grage » dans la liste, « AOP Saint Chinian » au tarif")),
 ]),
 14: dict(page=12, colonne="droite", nom="14 — Domaine des Noëls", vins=[
  ("AOC Anjou Blanc 2024",
   L(4, "le seul Anjou blanc du tarif est « Promenade des Noëls », listé à part juste après",
     appellation="AOC Anjou", couleur="Blanc", millesime="2024")),
  ("Promenade de Noëls - AOC Anjou Blanc 2024", T(4, 0, 0)),
  ("AOC Sauvignon 2025", T(4, 0, 1, "« AOC » dans la liste, « IGP Val de Loire » au tarif")),
  ("AOC Coteaux du Layon 2025", T(4, 0, 2)),
  ("AOC Coteaux du Layon Faye 2025", T(4, 0, 3)),
  ("AOC Crément de Loire", T(4, 0, 4, "le tarif a deux Crémant de Loire : « Crémant de Loire » et « Cuvée Prestige » ; la ligne retenue est la première")),
  ("AOC Rosé de Loire 2025", T(4, 0, 6)),
 ]),
 15: dict(page=13, colonne="pleine page", nom="15 — Vazart-Coquart & Fils", vins=[
  ("Cuvée Camille Extra-Brut Blanc de Blancs — Grand Cru Chouilly", T(40, 0, 0, "« Extra-Brut Blanc de Blancs » dans la liste, « Blanc brut » au tarif")),
  ("Brut Réserve Blanc de Blancs— Grand Cru Chouilly", T(40, 0, 1)),
  ("Rosé Brut — Grand Cru Chouilly",
   L(40, appellation="Grand Cru Chouilly", cuvee="Rosé Brut", couleur="Rosé brut")),
  ("Spécial Club 2017 Blanc de Blancs Extra-Brut — Grand Cru Chouilly", T(40, 0, 3)),
  ("Extra Brut — Grand Cru Chouilly", T(40, 0, 2)),
  ("82/17 Blanc de Blancs Zéro Dosage— Grand Cru Chouilly",
   # « Zéro Dosage » ne se dit que d'un vin effervescent : picto bulles
   L(40, appellation="Grand Cru Chouilly", cuvee="82/17 Blanc de Blancs Zéro Dosage", couleur="Blanc de Blancs, zéro dosage", famille="bulles")),
 ]),
 16: dict(page=14, colonne="pleine page", nom="16 — Château Pré la Lande", vins=[
  ("Cuvée Diane Rouge 2016 — AOC Sainte-Foy Côtes de Bordeaux", T(28, 0, 0)),
  ("Cuvée TerraCotta 2021 — AOC Sainte-Foy Côtes de Bordeaux", T(28, 0, 1)),
  ("Cuvée des Fontenelles 2025 — AOC Sainte-Foy Côtes de Bordeaux", T(28, 0, 2)),
 ]),
 17: dict(page=15, colonne="gauche", nom="17 — Domaine Jean de Villebois", vins=[
  ("AOC Menetou Rouge", L(6, "le tarif n'a qu'un Menetou-Salon, blanc",
                          appellation="AOC Menetou-Salon", couleur="Rouge")),
  ("AOC Menetou Blanc", T(6, 0, 7)),
  ("AOC Quincy", T(6, 0, 8)),
  ("Les Beltins 2022 Blanc — AOC Sancerre",
   L(6, appellation="AOC Sancerre", cuvee="Les Beltins", couleur="Blanc", millesime="2022")),
  ("Chêne à la rouline 2022 Blanc— AOC Sancerre", T(6, 0, 1)),
  ("Vignes de Tréleau 2023 — AOC Pouilly-Fumé",
   L(6, "au tarif, le Pouilly-Fumé 2023 nommé est « Les Silex Blancs »",
     appellation="AOC Pouilly-Fumé", cuvee="Vignes de Tréleau", millesime="2023")),
  ("La Louisonne 2023 Rouge - AOC Sancerre", T(6, 0, 13)),
  ("AOC Pouilly-Fumé 2025", T(6, 0, 6)),
  ("AOC Touraine Chenonceaux 2024", T(6, 0, 9)),
  ("AOC Sauvignon Blanc 2025", T(6, 0, 10, "« AOC » dans la liste, « IGP Val de Loire » au tarif")),
  ("AOC Pinot Noir Rosé 2024/25", T(6, 0, 12, "« AOC » dans la liste, « Vin de France » au tarif")),
  ("AOC Pinot Noir", T(6, 0, 15, "« AOC » dans la liste, « Vin de France » au tarif ; sans couleur dans la liste, rouge au tarif")),
 ]),
 18: dict(page=15, colonne="droite", nom="18 — Sebastien Magnien", vins=[
  ("[Blanc] AOC Hautes Côtes de Beaune 2024", T(10, 0, 2)),
  ("[Blanc] AOC Meursault 2024",
   L(10, "le tarif a deux Meursault 2023 : « Les Grands Charrons » et « Les Meix Chavaux » ; la liste ne dit pas lequel",
     appellation="AOC Meursault", couleur="Blanc", millesime="2024")),
  ("[Rouge] Clos de la Perrière 2023- AOC Hautes Côtes de Beaune", T(10, 0, 10)),
  ("[Rouge] Les Bons Feuvres 2023 — AOC Beaune", T(10, 0, 11)),
  ("[Rouge] Les Aigrots 2024— Beaune 1er Cru", T(10, 0, 14)),
  ("[Rouge] Les Perrières 2024— AOC Pommard", T(10, 0, 12)),
 ]),
 19: dict(page=16, colonne="gauche", nom="19 — Bastide de Blacailloux", vins=[
  ("St Probace Rouge 2025 — IGP Var Sainte Baume",
   L(31, "au tarif, SAINT PROBACE n'existe qu'en rosé et en blanc",
     appellation="IGP Var Sainte Baume", cuvee="SAINT PROBACE", couleur="Rouge", millesime="2025")),
  ("Joio Rosé 2025 — AOC Côteaux Varois en  Provence", T(31, 0, 2, "le tarif a aussi un 150 cl ; la ligne retenue est la 75 cl")),
  ("Joio Blanc 2025 — AOC Côteaux Varois en  Provence", T(31, 0, 4, "le tarif a aussi un 150 cl ; la ligne retenue est la 75 cl")),
  ("Joio Rouge 2024  — AOC Côteaux Varois en  Provence", T(31, 0, 6)),
  ("Miraia Blanc 2024 — AOC Côteaux Varois en  Provence",
   L(31, appellation="AOC Coteaux Varois en Provence", cuvee="Miraia", couleur="Blanc", millesime="2024")),
  ("Miraia Rouge 2022 — AOC Côteaux Varois en  Provence",
   L(31, appellation="AOC Coteaux Varois en Provence", cuvee="Miraia", couleur="Rouge", millesime="2022")),
  ("Aquino Rouge 2023 — AOC Côteaux Varois en  Provence",
   L(31, appellation="AOC Coteaux Varois en Provence", cuvee="Aquino", couleur="Rouge", millesime="2023")),
  ("Aquino Blanc 2024 — AOC Côteaux Varois en  Provence",
   L(31, appellation="AOC Coteaux Varois en Provence", cuvee="Aquino", couleur="Blanc", millesime="2024")),
 ]),
 20: dict(page=16, colonne="droite", nom="20 — Domaine Stratéus", vins=[
  ("Stratéus Rouge 2021 — AOC Madiran", T(22, 0, 1)),
  ("Néolithik Rouge 2022 — AOC Madiran", T(22, 0, 5)),
  ("Koloss Rouge 2022 — AOC Madiran", T(22, 0, 0)),
  ("Koloss Doux 2022 — VDF",
   L(22, "au tarif, le Koloss Vin de France est un rosé 2025, et le doux Vin de France s'appelle Strateus (2025)",
     appellation="Vin de France", cuvee="Koloss", couleur="Doux", millesime="2022")),
  ("Stratéus Blanc 2025 — AOC Pacherenc du Vic-Bilh sec", T(22, 0, 2)),
  ("Néolithik Blanc 2025 — AOC Pacherenc du Vic-Bilh sec",
   L(22, appellation="AOC Pacherenc du Vic-Bilh Sec", cuvee="Néolitik", couleur="Blanc sec", millesime="2025")),
 ]),
 21: dict(page=17, colonne="gauche", nom="21 — Famille d'Exéa", vins=[
  ("Chant de Lune Rouge 2024 — AOC Minervois", T(32, 0, 11)),
  ("Rouge Serame 2023 — AOC Corbières", T(32, 0, 7)),
  ("Blanc Serame — AOC Corbières", T(32, 0, 5)),
  ("Oena Rouge 2022 — AOC Corbières", T(32, 0, 10, "« Rouge » dans la liste, « Blanc » au tarif")),
  ("Jardin de Corbières Rouge 2025 — AOC Corbières", T(32, 0, 4)),
 ]),
 22: dict(page=17, colonne="droite", nom="22 — Domaine de la Barbinière", vins=[
  ("Les Silex Rouge 2023 — AOC Fiefs Vendéens Chantonnay", T(2, 0, 2)),
  ("Les Gorinières Blanc 2024 — AOC Fiefs Vendéens Chantonnay", T(2, 0, 3)),
  ("Les Courbes Blanc 2018 — AOC Fiefs Vendéens Chantonnay", T(2, 0, 4, "« Blanc » dans la liste, « Rouge » au tarif")),
  ("Les Amphibol Blanc 2025 — AOC Fiefs Vendéens Chantonnay", T(2, 0, 5)),
  ("Les Gneiss Rouge 2023 — AOC Fiefs Vendéens Chantonnay", T(2, 0, 6)),
  ("Le Bois Bouquet 2023 — IGP Val de Loire Pinot Noir", T(2, 0, 7)),
  ("L'O Brut — Méthode traditionnelle", T(2, 0, 8)),
 ]),
 23: dict(page=18, colonne="pleine page", nom="23 — Champagne Solemme", vins=[
  ("Terre de Solemme Brut — Premier Cru Champagne", T(39, 0, 0)),
  ("Plénitude de Solemme Extra-Brut — Premier Cru Champagne", T(39, 0, 1)),
  ("Esprit de Solemme Brut Nature— Premier Cru Champagne", T(39, 0, 2)),
  ("Nature de Solemme Blancs de Blancs Brut Nature — Premier Cru Champagne", T(39, 0, 3)),
  ("Ambre de Solemme Blanc de Noirs Brut Nature — Premier Cru Champagne", T(39, 0, 4)),
  ("Rose de Solemme Brut Nature— Premier Cru Champagne", T(39, 0, 5)),
 ]),
 24: dict(page=19, colonne="gauche", nom="24 — Château l'Escarderie", vins=[
  ("Château Lafargue 2020 — AOC Fronsac",
   L(30, appellation="AOC Fronsac", cuvee="Château Lafargue", millesime="2020")),
  ("Amphora 2021 — AOC Fronsac", T(30, 0, 3)),
  ("La Confiance 2023 — VDF", T(30, 0, 6)),
 ]),
 25: dict(page=19, colonne="droite", nom="25 - Chai Berthaud-Manceau", vins=[
  ("Courant Chenin 2025 — IGP Val de Loire", T(5, 0, 0)),
  ("Source Melon B. 2023 — IGP Val de Loire", T(5, 0, 1)),
  ("Reflet Gamay 2024 — IGP Val de Loire", T(5, 0, 2)),
  ("L'Eberluant Chardonnay 2025 — IGP Val de Loire",
   L(5, appellation="IGP Val de Loire", cuvee="L'Eberluant – Chardonnay", millesime="2025")),
  ("Courant Chenin 2025 — IGP Val de Loire", DOUBLON),
  ("Source Melon B. 2023 — IGP Val de Loire", DOUBLON),
  ("Reflet Gamay 2024 — IGP Val de Loire", DOUBLON),
  ("L'Eberluant Chardonnay 2025 — IGP Val de Loire", DOUBLON),
 ]),
 26: dict(page=20, colonne="pleine page (deux colonnes de liste)", nom="26 — Maison André Goichot", vins=[
  ("Château du Cray Blanc 2023 — AOC Bourgogne Chardonnay", T(13, 0, 1)),
  ("AOC Pouilly Vinzelles Blanc 2023",
   L(12, appellation="AOC Pouilly-Vinzelles", couleur="Blanc", millesime="2023")),
  ("AOC Auxey Duresses 2023", T(12, 0, 14)),
  ("Baron Auguste Blanc — AOC Crément de Bourgogne",
   L(12, appellation="AOC Crémant de Bourgogne", cuvee="Baron Auguste Blanc", couleur="Blanc")),
  ("Baron Auguste Rosé— AOC Crément de Bourgogne",
   L(12, appellation="AOC Crémant de Bourgogne", cuvee="Baron Auguste Rosé", couleur="Rosé")),
  ("Domaine les Guignottes Rouge 2023  — AOC Bourgogne Pinot Noir", T(14, 0, 2)),
  ("AOC Chassagne Montrachet Rouge 2023", T(12, 0, 12)),
  ("Aux Allots Rouge 2023 — AOC Nuits Saint Georges",
   L(12, appellation="AOC Nuits-Saint-Georges", cuvee="Aux Allots", couleur="Rouge", millesime="2023")),
  ("AOC Mercurey Blanc 2023",
   L(12, "au tarif, le Mercurey est un rouge 2022 (listé juste après)",
     appellation="AOC Mercurey", couleur="Blanc", millesime="2023")),
  ("AOC Mercurey Rouge 2022", T(12, 0, 9)),
  ("AOC Givry Rouge 2023",
   L(12, "le tarif a deux Givry rouges 2023 : « Champ La Dame » et le Givry 1er Cru ; la liste ne dit pas lequel",
     appellation="AOC Givry", couleur="Rouge", millesime="2023")),
  ("AOC Gervey Chambertin 2022", T(12, 0, 15, "« Gervey » dans la liste, « Gevrey-Chambertin » au tarif")),
 ]),
}

# Les couleurs que ni la liste ni le tarif ne donnaient, données par l'agence (2 octobre 2026),
# vin par vin : (stand, ligne de la liste) → couleur. Elles passent avant celle du tarif, qui
# n'en avait pas (Champagne Denis Frézier).
COULEURS_AGENCE = {
    (1, "Château Balac — AOC Cru Bourgeois Haut Médoc"): "Rouge",
    (2, "Trois Crus Brut — AOC Champagne"): "Blanc effervescent",
    (2, "Le Terroir Blanc Blanc de Blanc Brut — AOC Champagne"): "Blanc effervescent",
    (2, "le Terroir Meunier Blanc de Meuniers Extra-Brut — AOC Champagne"): "Blanc effervescent",
    (2, "Brut Nature — AOC Champagne"): "Blanc effervescent",
    (2, "Millésime Expression 2018 — AOC Champagne"): "Blanc effervescent",
    (4, "L'envol 2023 — AOC Muscadet Sèvre et Maine"): "Blanc",
    (5, "AOC Bourgognes Passe-Tout-Grain 2025"): "Rouge",
    (5, "Les Bulles du Puits"): "Rosé effervescent",
    (7, "Premières Fleurs 2025 — IGP Méditérranée"): "Blanc",
    (7, "Or des Dentelles 2023 — AOC Muscat BDV"): "Blanc moelleux",
    (7, "Or des Dentelles 2022 — AOC Muscat BDV"): "Blanc moelleux",
    (10, "La Grange Jaumain 2024 - Grolleau Noir"): "Rouge",
    (12, "Mas de Lusanne Mondeuse 2023— AOC Bugey"): "Rouge",
    (12, "Mas de Lusanne Pinot Noir 2023 — AOC Bugey"): "Rouge",
    (12, "Mas de Lusanne Gamay— AOC Bugey"): "Rouge",
    (12, "Mas de Lusanne Chardonnay 2020 — AOC Bugey"): "Blanc",
    (13, "Juliette 2025 — AOC Saint-Chinian"): "Blanc",
    (17, "Vignes de Tréleau 2023 — AOC Pouilly-Fumé"): "Blanc",
    (24, "Château Lafargue 2020 — AOC Fronsac"): "Rouge",
    (25, "L'Eberluant Chardonnay 2025 — IGP Val de Loire"): "Blanc pétillant",
}

ANNEE = re.compile(r"(19|20)\d{2}")


def annees(texte):
    """Les années qu'un millésime du tarif autorise : « 2024-2025 », « 2023-24 », « 2022/2024 »…"""
    if not texte:
        return set()
    t = str(texte)
    out = {int(m.group(0)) for m in ANNEE.finditer(t)}
    for m in re.finditer(r"(\d{4})\s*[-/]\s*(\d{2})(?!\d)", t):   # 2023-24, 2024/25
        out.add(int(m.group(1)[:2] + m.group(2)))
    return out


def millesime_liste(brut):
    """Le millésime que la liste donne (le dernier écrit : « Franc 2021 - AOP Chinon Rouge 2021 »)."""
    m = re.search(r"((?:19|20)\d{2})(?:/(\d{2}))?(?!.*(?:19|20)\d{2})", brut)
    if not m:
        return None
    return m.group(1) + (f"/{m.group(2)}" if m.group(2) else "")


def main():
    salon = json.loads(FICHIER.read_text(encoding="utf-8"))
    anciens = {}
    for s in salon["stands"]:
        for v in s.get("vins", []):
            anciens[(s["stand"], v["liste"])] = v.get("prix_centimes")

    total, affiches = 0, 0
    for s in salon["stands"]:
        spec = STANDS[s["stand"]]
        s["carte_matheo"] = {"page": spec["page"], "colonne": spec["colonne"], "titre": spec["nom"]}
        vins, doublons = [], []
        for brut, r in spec["vins"]:
            total += 1
            rubrique = None
            m = re.match(r"\[(.+?)\] (.*)", brut)
            if m:
                rubrique, brut = m.group(1), m.group(2)
            if r.get("doublon"):
                doublons.append(brut)
                continue
            fiche = fiches[r["fiche"]]
            assert r["fiche"] in s["domaines"], f"stand {s['stand']} : fiche {r['fiche']} hors du stand"
            mil = millesime_liste(brut)
            ecarts = [r["ecart"]] if r.get("ecart") else []
            if r["tarif"]:
                ti, li = r["tarif"]
                ligne = fiche["tableaux"][ti]["lignes"][li]
                v = {"appellation": ligne["appellation"], "cuvee": ligne["cuvee"],
                     "couleur": ligne["couleur"], "millesime": mil or ligne["millesime"],
                     "contenance": ligne["contenance"]}
                if ligne.get("note") == "*":   # l'étoile du tarif suit sa ligne (QUESTIONS.md, 6 et 7)
                    v["note"] = "*"
                if mil and annees(ligne["millesime"]) and int(mil[:4]) not in annees(ligne["millesime"]):
                    ecarts.insert(0, f"millésime {mil} dans la liste, {ligne['millesime']} au tarif")
                tarif = {"tableau": ti, "ligne": li}
            else:
                c = r["champs"]
                v = {"appellation": c.get("appellation"), "cuvee": c.get("cuvee"),
                     "couleur": c.get("couleur"), "millesime": c.get("millesime"), "contenance": None}
                if c.get("famille"):
                    v["famille"] = c["famille"]
                tarif = None
                ecarts.insert(0, "absent du tarif de septembre : affiché tel que la liste l'écrit")
            couleur = COULEURS_AGENCE.pop((s["stand"], brut), None)
            if couleur:
                assert not v.get("couleur"), f"stand {s['stand']} : « {brut} » avait déjà une couleur"
                v["couleur"] = couleur
                v["couleur_provenance"] = "l'agence, 2 octobre 2026"
            vins.append({"liste": brut, **({"rubrique": rubrique} if rubrique else {}),
                         "fiche": r["fiche"], "tarif": tarif, **v,
                         "ecarts": ecarts, "prix_centimes": anciens.get((s["stand"], brut))})
            affiches += 1
        s["vins"] = vins
        s["doublons_matheo"] = doublons

    assert not COULEURS_AGENCE, f"couleurs de l'agence sans vin : {list(COULEURS_AGENCE)}"
    salon["_vins"] = ("Vins dégustés : transcription du fichier de Mathéo (= padlet-vins-a-deguster.pdf), "
                      "cartes de stand seulement, rapprochée du tarif par scripts/transcrire-matheo.py. "
                      "`tarif` pointe la ligne de data/fiches/NN.json ; null = absent du tarif. "
                      "`ecarts` liste ce qui diffère (repris dans QUESTIONS.md, point 26).")
    salon.setdefault("mode_prix", "paliers")
    salon["_prix"] = ("Prix du salon, en centimes, vin par vin (`prix_centimes`). mode_prix = « paliers » : "
                      "une liste d'autant de prix que de paliers du tableau du domaine, ex. [1250, 1190, 1150]. "
                      "mode_prix = « unique » : un seul prix par vin, ex. [1250], et le tableau n'a plus "
                      "qu'une colonne « Prix salon ». Un stand peut avoir son propre `mode_prix`. "
                      "null = case vide. Ensuite : npm run salon.")
    FICHIER.write_text(json.dumps(salon, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{total} lignes lues sur les 26 cartes, {affiches} vins affichés, "
          f"{total - affiches} doublons écartés")


if __name__ == "__main__":
    main()
