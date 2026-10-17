# Catalogue restaurant : ce qui manque pour que prix et quantités soient bons

Écrit par `scripts/manque-restaurant.py`. Référence : le **catalogue caviste 85**
(`dist/catalogue-caviste-2026-ecran.pdf`) — mêmes domaines, mêmes vins, mêmes textes ;
**seuls les minimums de commande (les colonnes) et les prix changent**. Sur les tarifs
annotés, on prend **le prix qui est écrit**, surligné ou non (l'agence, 10 octobre).

**État : 582 prix posés, 88 cases encore vides.**

## 1. Les quatre fiches sans aucun prix restaurant

| Page | Domaine | Lignes sans prix | Ce qu'il manque |
|---|---|---|---|
| p.12 | **Divin No Low** | 8 / 8 | les minimums de commande **et** les prix : aucune page scannée |
| p.16 | **Domaine des Nugues** | 11 / 11 | les prix : le tarif scanné ne donne que les BIB et une « sélection restaurant » (Brouilly, Crémant, Mâcon-Villages…), aucun vin de la fiche |
| p.30 | **Mas des Restanques** | 8 / 8 | les minimums de commande **et** les prix : aucune page scannée |
| p.51 | **Famille d’Exea — Jus de Cépages** | 0 / 6 | les minimums de commande **et** les prix : aucune page scannée |

## 2. Les lignes isolées sans prix

| Page | Domaine | Ligne | Pourquoi |
|---|---|---|---|
| p.8 | Domaine du Colombier / J.Y Bretaudeau | Rouge aux lèvres (IGP Val de Loire · Rouge · 75 cl) | le catalogue C.H.R. du domaine n'a été scanné que sur deux pages |
| p.8 | Domaine du Colombier / J.Y Bretaudeau | La Perle (Méthode traditionnelle · Blanc · 75 cl) | le catalogue C.H.R. du domaine n'a été scanné que sur deux pages |
| p.8 | Domaine du Colombier / J.Y Bretaudeau | AOP Muscadet (AOP Muscadet · Blanc · BIB) | le catalogue C.H.R. du domaine n'a été scanné que sur deux pages |
| p.8 | Domaine du Colombier / J.Y Bretaudeau | IGP Val de Loire Chardonnay (IGP Val de Loire Chardonnay · Blanc · BIB) | le catalogue C.H.R. du domaine n'a été scanné que sur deux pages |
| p.8 | Domaine du Colombier / J.Y Bretaudeau | IGP Val de Loire Cabernet Franc (IGP Val de Loire Cabernet Franc · Rosé · BIB) | le catalogue C.H.R. du domaine n'a été scanné que sur deux pages |
| p.11 | Domaine Jean de Villebois | AOC Menetou-Salon Rouge (AOC Menetou-Salon Rouge · Rouge · 75 cl) | le tarif n'a que le Menetou-Salon **blanc** |
| p.11 | Domaine Jean de Villebois | IGP Chenin Blanc (IGP Chenin Blanc · Blanc · 2025 · 75 cl) | absent du tarif restaurant (ajouté au caviste le 9 octobre) |
| p.19 | Maison et Domaine André Goichot | AOC Pouilly-Vinzelles Blanc (AOC Pouilly-Vinzelles Blanc · Blanc · 2023 · 75 cl) | absent du portfolio restaurant (il a le Pouilly-Fuissé, pas le Vinzelles) |
| p.36 | Domaine Haut Marin | N°10 Pétillant (IGP Côtes de Gascogne · Pétillant · 75 cl) | absent de la page restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 2003 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1998 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1993 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1992 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1986 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1983 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1981 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1980 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1979 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1978 · 70 cl) | absente du tarif restaurant |
| p.36 | Domaine Haut Marin | Millésimés (AOP Bas-Armagnac · Blanc · 1973 · 70 cl) | absente du tarif restaurant |

## 3. Les colonnes incomplètes (la ligne a un prix, mais pas partout)

| Page | Domaine | Ligne | Colonnes manquantes | Pourquoi |
|---|---|---|---|---|
| p.31 | Domaine Trichon | Beaumes de Venise Rouge (AOC Beaumes de Venise · Rouge · 2023 · Magnum 1,5 L) | À partir de 36 cols, À partir de 48 cols | le tarif met « – » dans ces colonnes |
| p.31 | Domaine Trichon | Mas de Lusanne Vacqueyras Rouge (AOC Vacqueyras · Rouge · 2023 · Magnum 1,5 L) | À partir de 36 cols, À partir de 48 cols | le tarif met « – » dans ces colonnes |

## 4. Les minimums de commande (colonnes)

**39 fiches sur 42** ont leurs colonnes relevées sur un tarif restaurant. Trois gardent
celles du catalogue caviste, faute de tarif : **Divin No Low**, **les jus de cépages de la
Famille d'Exea** et **le Mas des Restanques**.

Deux choix à confirmer :

- **Stratéus** : la grille va de 24 à 300 bouteilles et ne dit pas lesquelles garder.
  Pris **24 / 48 / 120 bts**. La gamme Koloss n'a pas de prix à 48 bts (le tarif met « / »).
- **Vazart-Coquart** : les colonnes s'appellent **« Par 24 / Par 48 / Par 78 »** sur le tarif,
  gardées telles quelles.

## 5. Les offres

Toutes les offres sont encore celles du catalogue caviste, sauf **Chai Berteaud Manceau**
(« Offre 11+1 à partir de 60 cols », écrite à la main sur le scan). L'agence les reprend
une par une.
