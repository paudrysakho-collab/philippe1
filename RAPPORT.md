# Rapport de contrôle — Catalogue Agence SCIO, édition septembre 2026

État au terme de la **phase 0** (outillage et base de données) et de la **phase 2**
(direction artistique et pages témoins). En attente de la **validation n° 1**.

---

## 1. Ce qui est construit

| Élément | État |
|---|---|
| Base unique `data/catalogue.json` | **40 fiches, 359 cuvées en bouteille et 19 en bag-in-box** |
| Prix issus de votre Excel | **19 fiches sur 40** (20 feuilles, le Domaine Trichon en ayant deux) |
| Prix issus de l'ancien tarif, via la maquette | 21 fiches — **à confirmer sur image en phase 1 bis** |
| Conditions de port et départements | 40 fiches sur 40, repris de l'ancien tarif |
| Gabarit HTML/CSS unique | Couverture + fiche, trois thèmes prévus (écran, imprimeur, bureau) |
| Images extraites de l'ancien tarif | 255, triées et inventoriées |

**Aucun prix n'est saisi dans la mise en page.** Tout est généré depuis la base.

---

## 2. Les anomalies réelles, à votre arbitrage

### 2.1 Dégressivité inversée — 2 cas, et seulement 2

Le prix monte alors que la quantité augmente. **Conformément à votre consigne, rien
n'a été modifié.**

| Fiche | Cuvée | Prix constatés | Source |
|---|---|---|---|
| **n° 15 Domaine des Verchères** | Mâcon Chardonnay 75 cl | 6,10 → 5,45 → **5,75** | **votre Excel**, feuille « Domaine des Verchères », ligne 7 |
| **n° 19 Domaine de la Pousterle** | Terroir d'Ansouis 75 cl | 5,00 → **5,25** → 5,00 | maquette, à confirmer sur l'image du tarif |

### 2.2 Conditions de port absentes de la source — 4 fiches

Aucune mention de port dans l'ancien tarif pour les fiches **n° 8 Boehler, n° 25 La
Passion des Terroirs, n° 32 et n° 33 Famille d'Exea**. Conformément à votre arbitrage,
elles portent « Sur demande » dans la barre Conditions **et** en pied de page, et un
encadré « Tarifs et offres sur demande » remplace le tableau absent.

> À noter : la maquette affichait « franco dès 72 bt » pour la Famille d'Exea. Cette
> valeur n'existe **dans aucune source**. Elle a été retirée.

### 2.3 Le palier « 301 bt » du Domaine Boehler — résolu

L'audit s'interrogeait sur ce palier inhabituel. **Votre Excel donne la réponse** : il
dit « **Plus de 300 bts** ». La maquette l'avait transcrit « 301 ». Le catalogue écrit
désormais « dès 301 bt », qui est la traduction exacte de « plus de 300 ».
**Confirmez-moi si vous préférez la formulation « au-delà de 300 bt ».**

### 2.4 Château Balac — 5 paliers conservés

Conformément à votre arbitrage. Le chevauchement est réel et confirmé par l'Excel :
« Jusqu'à 120 bts » et « À partir de 120 bts » portent tous deux sur 120 bouteilles.
**Non corrigé, signalé ici.**

### 2.5 Famille d'Exea — trois lignes de bag-in-box sans couleur

Trois lignes « Pergola d'Exea », BIB, à 11,85 et 11,65 €, **sans couleur renseignée**.
L'audit le signalait, et c'est exact. Les couleurs Blanc / Rosé / Rouge manquent
dans la source. **Pouvez-vous me les donner ?**

### 2.6 Millésimes : « NM » et « — » ne disent pas la même chose

La maquette écrivait « NM » (non millésimé) là où l'Excel dit « – » (non communiqué),
par exemple chez François Reverdy sur La Grange Jaumain. Le catalogue respecte
désormais la distinction : « — » quand l'information manque.

---

## 3. Important : l'audit fourni contient des erreurs de lecture

L'audit a manifestement été produit en lisant des **images rendues** du catalogue.
Les erreurs de cette lecture automatique y ont été consignées comme des défauts. J'ai
confronté chaque affirmation vérifiable au contenu réel des fichiers.

### 3.1 Affirmations infirmées

| Affirmation de l'audit | Mesure réelle |
|---|---|
| Message sanitaire corrompu : « alcoolest », « acoolest », « pourla », « moderation » | **0 occurrence.** La mention est présente correctement, **52 fois, une par page** |
| « Anarchie des séparateurs décimaux », points mêlés aux virgules | **726 prix à la virgule, 0 au point** |
| Raison sociale déformée 6 fois (ACENCE, HAGENCE, AVINSREPIRITS…) | **0 occurrence.** Le nom est dans le **logo, une image** : c'est elle que la lecture automatique a mal interprétée |
| Césures « BEA UJ OLA IS », « BOURGO OGNE », « RHO NE », « Cuvé e » | **0 occurrence** |
| Coquilles « piriot », « soutre », « Crav », « Pavojs », « babe », « phatos », « Manthélie » | **0 occurrence** |
| « Durfort-Vivens », « Villaudes », « Pergola » introuvables par Ctrl+F | **Tous trouvés** |

### 3.2 Le cas le plus grave : les dégressivités inversées

L'audit annonçait une vingtaine d'inversions de prix. **Votre Excel en confirme une
seule** (Verchères). Sur François Reverdy, l'audit annonçait quatre inversions :

| Cuvée | Excel (vérité) | Ce qu'affirmait l'audit |
|---|---|---|
| Anjou Schistes Vert | 14,75 → 13,25 → 12,25 (décroissant) | « 12,25 → 13,25, +1,00 € » |
| Saumur Tuffeau | 16,00 → 14,50 → 13,50 (décroissant) | « 13,50 → 14,50, +1,00 € » |
| Quincy Graves Argileuses | 19,95 → 17,85 → 16,50 (décroissant) | « 16,50 → 17,85, +1,35 € » |
| IGP Les Soudannes | 10,00 → 9,50 → 9,25 (décroissant) | « 9,25 → 9,50, +0,25 € » |

**L'audit a lu les colonnes à l'envers**, parce que les en-têtes de paliers étaient
entremêlés sur deux lignes dans la maquette. Même mécanisme pour le Prieuré des Papes
(la palette est bien **moins** chère : 5,50 contre 5,80) et pour les bag-in-box du
Domaine du Colombier (le 5 L est bien moins cher que le 10 L, sur les six lignes).

**Appliquer ces corrections aurait modifié des prix justes.**

### 3.3 Affirmations confirmées

- **La couche texte est bien cassée** : j'avais d'abord conclu l'inverse, à tort. La
  maquette interlettre ses petites capitales, ce qui insère **1 499 espaces parasites**
  de largeur quasi nulle. Résultat : « APPELLATION », « CUVÉE », « PALIERS » et
  « Tuffeau » sont **introuvables par Ctrl+F**. Le nouveau catalogue est propre : le
  contrôle automatique le vérifie à chaque génération.
- **Les pages 18, 30, 33 et 41 sont bien absentes du sommaire** (pages de suite de
  Goichot, Haut Marin, La Passion des Terroirs et Famille d'Exea). Elles seront
  réintégrées, conformément à votre arbitrage.
- **Les mentions légales manquantes sont réelles** (forme juridique, capital, TVA
  intracommunautaire, CGV, logo Triman).
- **Les photographies sont insuffisantes** pour l'impression (voir § 4).

---

## 4. Photos : le point le plus préoccupant

Les images récupérables dans l'ancien tarif sont **trop petites pour un catalogue
imprimé**. Les meilleures plafonnent à 1 241 pixels de large, soit 105 mm à 300 dpi.
Les photographies réellement exploitables tournent entre **420 et 607 pixels**.

| Fiche témoin | Photo d'ambiance | Résolution à la taille d'impression |
|---|---|---|
| n° 40 Vazart-Coquart | vignoble | 420 px → **99 dpi** à 108 mm |
| n° 3 Colombier | le vigneron au chai | 462 px → **86 dpi** à 136 mm |
| n° 32 Famille d'Exea | la propriété | 597 px → **140 dpi** à 108 mm |

Le minimum acceptable est 200 dpi, l'idéal 300. **Il faut les fichiers d'origine.**
Sans eux, le catalogue sera correct à l'écran et décevant à l'impression.

**La couverture** est pour cette raison entièrement typographique dans cette version :
une photo pleine page demanderait une image d'au moins 2 480 pixels de large, et la
meilleure disponible tomberait à 150 dpi. La variante photo est prête côté code.

---

## 5. Ce que le nouveau gabarit corrige

| Défaut de la maquette | État |
|---|---|
| Sous-colonnes de paliers à 5 positions différentes | **Bloc Prix de largeur fixe (53 mm)**, divisé en parts égales. Écart mesuré : **0,0 mm** sur toutes les pages |
| En-têtes de paliers coupés et entremêlés | Une seule ligne, casse normale, alignés sur leurs chiffres |
| 22 notations de paliers différentes | Notation unique : « jusqu'à 36 bt », « dès 48 bt », « Palette ». « bt » invariable |
| Couche texte cassée (Ctrl+F) | Réparée et vérifiée automatiquement |
| Polices remplacées en silence | **Fraunces et Inter réellement incorporées**, vérifié dans le PDF |
| Colonne Appellation tronquée | « AOP Muscadet Sèvre et Maine sur lie » désormais complet |
| Nombre de photos inégal | Bande de hauteur fixe ; sans seconde photo, l'ambiance occupe la place |
| Pied de page recouvert par les tableaux | En-tête et pied paginés : le contenu coule proprement sur deux pages |

Contrôles automatiques au dernier passage : **8 sur 8 au vert.**

---

## 6. Ce que j'attends de vous

### Pour la validation n° 1
1. **Les 4 pages témoins** vous conviennent-elles ? (couverture, n° 40, n° 3, n° 32)
2. La **couverture typographique** vous va-t-elle, ou attendons-nous une photo HD ?

### Pour la suite, dès que possible
3. **Les photos et logos en haute définition** — le point le plus bloquant (§ 4).
4. Les **mentions légales** : forme juridique, capital social, n° de TVA
   intracommunautaire. **Je ne les inventerai pas.**
5. Les **couleurs des trois bag-in-box « Pergola d'Exea »** (§ 2.5).
6. Les **conditions de port** des fiches n° 8, 25, 32 et 33 (§ 2.2).
7. Les **labels exacts** par domaine (bio certifié, en conversion, biodynamie
   certifiée, HVE). L'Excel en donne déjà pour ses 20 domaines — par exemple « Vins
   biologiques certifiés FR-BIO-01 » chez Reverdy, « certifiée HVE » chez Verchères.
8. Les cuvées **« Nouveau »** de la saison et celles **en allocation**.

### Deux points de forme à trancher
9. Le palier Boehler : « dès 301 bt » ou « au-delà de 300 bt » ? (§ 2.3)
10. Votre Excel indique **« tarifs valables jusqu'au 31/12/2026 »**. L'audit signalait
    justement l'absence de date de validité. **Faut-il la faire figurer ?**

---

## 7. Réserves

- Les **21 fiches hors Excel** portent des prix repris de la maquette. Ils seront
  confrontés un par un aux images des tableaux d'origine en **phase 1 bis** — ces
  images sont lisibles, la vérification est donc possible et fiable.
- Le **tri des 255 images** a été fait à la main pour les 3 fiches témoins. Le tri
  automatique n'est pas assez sûr : il confond photographies et captures d'écran des
  tableaux Excel. Chaque fiche sera contrôlée à l'œil en phase 3.
- La règle d'ordre des lignes (effervescents, blancs, rosés, rouges, moelleux, autres,
  puis bag-in-box) n'est **pas encore appliquée** : les lignes suivent l'ordre des
  sources. Ce sera fait en phase 3, et tout changement d'ordre sera signalé.
