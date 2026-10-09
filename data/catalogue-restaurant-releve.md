# Relevé du tarif restaurant (dossier de l'agence, 9 octobre 2026)

Source : `sources/catalogue-restaurant-2026/tarifs-restaurant-annotes.pdf` (51 pages, envoyé
par l'agence en lien Drive le 9 octobre). Ce fichier note, page par page, **à quel domaine
correspond chaque scan** et **quels paliers de quantité** le tarif restaurant donne. Les prix
se relèvent ensuite ligne à ligne, et se posent dans `scripts/prix-restaurant.py`.

**Règles de lecture** (les mêmes que le 8 octobre) : surligné = on prend ; barré ou rayé en
rouge = on retire ; une colonne non surlignée disparaît ; un millésime douteux → le plus
récent ; pas de millésime → aucun. **Un prix ne s'invente ni ne se corrige jamais.**

## Carte des pages

| Scan | Domaine (fiche) | Paliers lus sur le tarif | Remarques |
|---|---|---|---|
| 1 | — | — | le sommaire annoté du 8 octobre (déjà appliqué au catalogue caviste) |
| 2 | Champagne Solemme (39) | **36 / 60 / 120** (écrits à la main) | les colonnes 240 et 300 sont rayées ; « Franco » en bas |
| 3 | François Reverdy (1) | à confirmer | colonnes imprimées « jusqu'à 36 / 37 à 119 / 120 / 300 » ; prix annotés en rouge |
| 4 | Domaine des Sardelles — Les Courants (41, tableau 1) | **36 / 72 / 144** | la colonne 288 est rayée ; prix surlignés 5,80 / 5,50 / 5,20 |
| 5 | Domaine des Sardelles — AOC (41, tableau 0) | **36 / 72 / 144** | la colonne 288 est rayée ; « Sancerre Rosé » barré |
| 6–7 | Domaine de la Barbinière (2) | **≥ 24 / ≥ 60 / ≥ 120** | « Tarifs Restauration HT 2026 » ; conditions au verso |
| 8–9 | Domaine du Colombier (3) | **60 / 120 / 240** | « CATALOGUE C.H.R. et TARIF FRANCO H.T » : un tarif restaurant à lui |
| 10 | Domaine des Noëls (4) | à confirmer | « à partir de 120 », « Franco » en rouge |
| 11 | Chai Berteaud Manceau (5) | **36 / 60 / 120 / 240** | courriel du domaine ; offre 11+1 à partir de 120 bouteilles jusqu'à mi-novembre |
| 12–13 | Domaine Jean de Villebois (6) | **36–42 / 48–90 / 96–150 / 156–240 / 246 cols et +** | « Tarif franco » en rouge |
| 14 | Domaine Boehler (8) | à confirmer | grille « < 36 bt / 36–72 bt / 72–120 bt / > 120 bt » |
| 15 | Domaine des Nugues (9) | **36 / 60 / 120 / 240 / 360 / 600** | tarifs France HT départ cave 2026 |
| 16 | Domaine Sébastien Magnien (10) | tarif unique | offre 11+1 à partir de 72 bouteilles, panachage par 24 |
| 17–21 | Maison et Domaines André Goichot (12) + Château du Cray (13) | **1–36 / 37–72 / 73–120 / + de 120 bts** | portfolio 2026, « Tarif franco » |
| 22 | Domaine des Verchères (14) | **36 / 60 / 120 / 180 / 300** | tarif HT départ chai |
| 23 | Domaine Nadine Ferrand (11) | tarif unique | « Tarif CHR 2026 » |
| 24–25 | Domaine Le Prieuré des Papes (16) | **36–72 / 78–120 / 126–240 / 246 cols et + / palette** | offres 11+1 et 5+1 ; p.25 = grands formats |
| 26 | Domaine de Coyeux (17) | **36–72 / 78–120 / 120–240 / 240 et + / palette** | offres 11+1 et 5+1 |
| 27 | Domaine du Moulin Blanc (18) | **36–72 / 78–120 / 120–240 / 240 et + / palette** | offre 5+1 |
| 28 | Domaine de la Pousterle (19) | **36–72 / 78–120 / 126–240 / 240 et + / palette** | offre 5+1 |
| 29–30 | les quatre domaines Strasser Radziwill | — | bons de commande des offres 5+1 et 11+1 |
| 31–33 | La Passion des Terroirs (25) | à confirmer | tarif à l'unité |
| 34 | Bastide de Blacailloux (31) | **36 / 120 / 240 / 380** (francos) | tarif PRO HT France |
| 35–36 | Famille d'Exea — Sérame (32) | **72 / 144 / 300 cols** | « Les Couleurs » et « Les Vins de Paysage » |
| 37–42 | à relever | — | suite du dossier |
| 43–48 | **doublons** des scans 6 à 12 | — | Barbinière, Colombier, Noëls, Berteaud, Villebois |
| 49–51 | à relever | — | fin du dossier |

## Ce qui reste à faire

1. Finir la carte (scans 37 à 42 et 49 à 51).
2. Relever les prix ligne à ligne, domaine par domaine, puis les poser dans `PRIX` de
   `scripts/prix-restaurant.py` ; **seconde passe indépendante** avant de déclarer la fiche faite.
3. Les offres : l'agence les reprend une par une (« je changerai les offres, page 1, page 2… »).
