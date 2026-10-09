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
| 3 | François Reverdy (1) | **jusqu'à 36 / 37 à 119** | colonnes imprimées « jusqu'à 36 / 37 à 119 / 120 / 300 » ; prix annotés en rouge |
| 4 | Domaine des Sardelles — Les Courants (41, tableau 1) | **36 / 72 / 144** | la colonne 288 est rayée ; prix surlignés 5,80 / 5,50 / 5,20 |
| 5 | Domaine des Sardelles — AOC (41, tableau 0) | **36 / 72 / 144** | la colonne 288 est rayée ; « Sancerre Rosé » barré |
| 6–7 | Domaine de la Barbinière (2) | **≥ 24 / ≥ 60 / ≥ 120** | « Tarifs Restauration HT 2026 » ; conditions au verso |
| 8–9 | Domaine du Colombier (3) | **60 / 120 / 240** | « CATALOGUE C.H.R. et TARIF FRANCO H.T » : un tarif restaurant à lui |
| 10 | Domaine des Noëls (4) | **60 / 120** (colonnes « Prix CHR » surlignées) | « Franco » en rouge |
| 11 | Chai Berteaud Manceau (5) | **36 / 60 / 120** (surlignés) | courriel du domaine ; l'offre imprimée est rayée, « Offre 11+1 à partir de 60 cols » écrit à la main |
| 12–13 | Domaine Jean de Villebois (6) | **36 / 66 / 126 / 246 cols** (écrits au-dessus des colonnes 36-42, 66-120, 126-240, 246-300) | « Tarif franco » en rouge ; colonne 18-30 rayée |
| 14 | Domaine Boehler (8) | **36–72 / 72–120 / > 120 bt** (surlignés) | frais de port inclus |
| 15 | Domaine des Nugues (9) | **36 / 60 / 120** (surlignés) | « Restaurants » ; BIB et « Nos sélections » seulement : aucun vin de la fiche |
| 16 | Domaine Sébastien Magnien (10) | tarif unique (colonne 2024 surlignée) | la phrase d'offre 11+1 (72 bouteilles) est raturée au bleu |
| 17–21 | Goichot (12), Château du Cray (13), Les Guignottes (14) | **42 / 72 / 126 bts** (écrits au-dessus ; colonne 1-36 rayée) | portfolio 2026, « Tarif franco » |
| 22 | Domaine des Verchères (15) | **36 / 60 / 120** (surlignés) | tarif HT départ chai |
| 23 | Domaine Nadine Ferrand (11) | tarif unique | « Tarif CHR 2026 » |
| 24–25 | Domaine Le Prieuré des Papes (16) | **36–72 / 78–120 / 126–240 / 246 cols et + / palette** | offres 11+1 et 5+1 ; p.25 = grands formats |
| 26 | Domaine de Coyeux (17) | **36–72 / 78–120 / 120–240 / 240 et + / palette** | offres 11+1 et 5+1 |
| 27 | Domaine du Moulin Blanc (18) | **36–72 / 78–120 / 120–240 / 240 et + / palette** | offre 5+1 |
| 28 | Domaine de la Pousterle (19) | **36–72 / 78–120 / 126–240 / 240 et + / palette** | offre 5+1 |
| 29–30 | les quatre domaines Strasser Radziwill | — | bons de commande des offres 5+1 et 11+1 |
| 31–33 | La Passion des Terroirs (25) | prix à l'unité | seulement les blancs et les liquoreux (p.33 = couverture arrière) |
| 34 | Bastide de Blacailloux (31) | **60 / 120 / 180** (« Tarif franco » ; la colonne 36 est rayée) | tarif PRO HT France |
| 35–36 | Famille d'Exea — Sérame (32) | **72 / 144 / 300 cols** | Oena, Lullula, Carduelis ; p.36 sans prix |
| 37–51 | **doublons** des scans 1 à 15 | — | vérifié par comparaison d'images (même ordre, mêmes annotations) |

## Relevé posé (dans `scripts/prix-restaurant.py`)

Relu deux fois : une lecture page par page, puis une seconde passe sur des recadrages zoomés
(Villebois, Goichot), comparée ligne à ligne au script.

| Fiche | Domaine | Paliers restaurant | Prix |
|---|---|---|---|
| 1 | François Reverdy | jusqu'à 36 / de 37 à 119 bts | 9 vins (les colonnes 120 et 300 sont rayées) |
| 2 | Domaine de la Barbinière | ≥ 24 / ≥ 60 / ≥ 120 bts | 7 vins (prix du 75 cl ; « Les Courbes » 2017 barrée, 2018 surlignée) |
| 3 | Domaine du Colombier | 60 / 120 / 240 bts | 5 vins ; « Rouge aux lèvres », « La Perle » et les BIB ne sont pas au tarif C.H.R. |
| 4 | Domaine des Noëls | 60 / 120 bts | 7 vins |
| 5 | Chai Berteaud Manceau | 36 / 60 / 120 cols | 4 vins ; offre « 11+1 à partir de 60 cols » (écrite à la main) |
| 6 | Domaine Jean de Villebois | 36 / 66 / 126 / 246 cols | 11 vins ; les 3 parcellaires sans prix au-delà de 120 cols (« – ») ; Menetou-Salon rouge et Chenin IGP absents du tarif |
| 8 | Domaine Boehler | 36-72 / 72-120 / > 120 bts | 9 vins |
| 9 | Domaine des Nugues | 36 / 60 / 120 bts | **aucun** : le tarif restaurant n'a que des BIB et d'autres vins |
| 10 | Domaine Sébastien Magnien | prix unique (2024) | 7 vins (Meursault = « Les Grands Charrons », comme au salon) |
| 11 | Domaine Nadine Ferrand | prix unique | 9 vins |
| 12, 13, 14 | Goichot, Cray, Guignottes | 42 / 72 / 126 bts | 11 vins ; le Pouilly-Vinzelles n'est pas au tarif |
| 15 | Domaine des Verchères | 36 / 60 / 120 bts | 5 vins |
| 16–19 | les quatre Strasser Radziwill | 36-72 / 78-120 / 120(126)-240 cols | 13 vins |
| 25 | La Passion des Terroirs | prix à l'unité | 6 blancs et liquoreux ; les 31 rouges n'ont pas de page dans le dossier |
| 31 | Bastide de Blacailloux | 60 / 120 / 180 bts | 10 vins |
| 32 | Famille d'Exea | 72 / 144 / 300 cols | Oena seul (les autres vins ne sont pas au tarif du dossier) |
| 39 | Champagne Solemme | 36 / 60 / 120 bts | 6 vins ; le magnum de Plénitude est rayé, donc retiré |
| 41 | Domaine des Sardelles | 36 / 72 / 144 bts | 7 vins ; « Sancerre Rosé » est barré, donc retiré |

**Sans tarif restaurant dans le dossier** (cases vides, en attente de l'agence) : Divin No Low (7),
Pasquiers (20), Trichon Rhône et Bugey (21, 42), Stratéus (22), Haut Marin (23), La Gorce (26),
Falfas (27), Pré la Lande (28), Balac (29), Escarderie (30), Exea jus (33), Gragnos (34), Les Lys
(35), Albas (36), Dekeyne (37), Frézier (38), Vazart-Coquart (40), Mas des Restanques (43).

## Ce qui reste à faire

1. Les tarifs restaurant des domaines ci-dessus, et les pages manquantes (Nugues, rouges de la
   Passion des Terroirs).
2. Les offres : l'agence les reprend une par une (« je changerai les offres, page 1, page 2… ») ;
   les fiches gardent pour l'instant celles du catalogue caviste (sauf Berteaud).
