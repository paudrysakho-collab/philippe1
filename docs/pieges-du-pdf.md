# Pièges du PDF source (relevés et vérifiés à la main)

## Plan du PDF

- 44 pages A4. p.1 : couverture. p.2 : l'agence et ses contacts. p.3 : sommaire. p.4 à p.43 : domaines n°1 à n°40 (le domaine n est en page n+3, et son numéro est imprimé en bas sous la forme « -n- »). p.44 : contacts, mentions légales, lexique.
- Effectifs par région : Loire 7 (n°1 à 7), Alsace 1 (n°8), Beaujolais 1 (n°9), Bourgogne 6 (n°10 à 15), Rhône 6 (n°16 à 21), Sud-Ouest 3 (n°22 à 24), Bordeaux 6 (n°25 à 30), Provence 1 (n°31), Languedoc 5 (n°32 à 36), Champagne 4 (n°37 à 40).
- Champs absents, à laisser vides sans rien inventer : n°1 François Reverdy n'a pas de texte de présentation ; n°8 Domaine Boehler n'a ni note de prix ni départements de distribution.

## Ce que l'extraction de texte ne donne pas

- **Les tableaux de prix sont des images.** La couche texte ne contient aucun prix : tout se transcrit visuellement, depuis des rendus à 200 dpi ou plus.
- **Les lettrines peuvent être extraites à part.** Selon l'outil, la première lettre décorative de chaque présentation se retrouve isolée ailleurs dans le flux. Exemple p.37 : « lain, Patricia et leurs fils… » plus un « A » isolé donnent « Alain, Patricia et leurs fils… ». Vérifie chaque début de texte sur l'image.
- **Des tirets disparaissent en fin de ligne** : « BasArmagnacs » (p.26) se lit « Bas-Armagnacs » ; « VazartCoquart » (p.43) se lit « Vazart-Coquart ».
- **L'ordre du flux est mélangé** (titre, note, région, encarts) : la structure se lit sur l'image.
- **Les informations visuelles se relèvent sur l'image** : logos bio, HVE, AOP ou IGP, pastilles « ALLOCATION! », encarts « Possibilité de panacher… » et « consultez-nous », mots-titres « BIBS », « RATAFIA », « ARMAGNAC », « BIERES », « ALERT! VINS DÉSALCOOLISÉS ».

## Relevé utile pour vérifier tes données

- Pastilles d'allocation : n°2, 10, 11, 12 (« ALLOCATION * »), 22, 37, 38.
- Encarts « consultez-nous » (tarifs et offres de l'ensemble des vins) : n°6, 23, 24, 25.
- Groupes de panachage entre domaines : n°6 et 7 ; n°12, 13 et 14 ; n°16, 17, 18 et 19 (Strasser Radziwill) ; n°32 et 33 (vins et jus de la Famille d'Exea). Ailleurs, « Possibilité de panacher » en tête de tableau vaut à l'intérieur du domaine.
- Produits à part : BIB n°3, 23, 31, 32, 36 ; Armagnacs n°23 ; bières n°24 ; sans alcool n°7 (vins désalcoolisés) et n°33 (jus de cépages) ; ratafias n°37 et 38.

## Anomalies à mettre dans QUESTIONS.md (ne pas corriger seul)

1. **p.6, n°3 Domaine du Colombier** : le premier tableau (six Champagne Grand Cru : Cuvée Camille, Brut Réserve, Extra Brut, Special Club, TC, Parcellaire AD 191) est identique à celui de Vazart-Coquart (n°40, p.43). Probable copier-coller : ne l'attribue pas au Colombier sans confirmation.
2. **p.18, n°15 Verchères**, AOP Mâcon « Mâcon Chardonnay » 2025 : 6,10 € / 5,45 € / 5,75 €. Le palier 300 bts est plus cher que le palier 180 bts.
3. **p.22, n°19 Pousterle**, Luberon « Terroir d'Ansouis » rouge 2021 : 5,00 € / 5,25 € / 5,00 €. Le palier 300 bts est plus cher que le palier 198 bts.
4. **p.25, n°22 Stratéus**, VDF Koloss rosé 2025 : la colonne contenance affiche « 75,00 € » (sans doute 75 cl).
5. **p.15, n°12 Goichot** : pastille « ALLOCATION * » et cinq lignes étoilées (Meursault Les Vireuils, Chablis 1er Cru, Bourgogne Hautes-Côtes de Beaune, Rully, Corton Grand Cru Les Maréchaudes), mais la note de prix commence elle aussi par « * ». Lecture probable : l'étoile signale les cuvées en allocation.
6. **p.41, n°38 Denis Frézier** : « Grand Cru Exception 2016* », astérisque jamais expliqué.
7. **p.28, n°25 Passion des Terroirs** : des prix sont affichés, mais la note dit « * Demander le tarif et offre. » et un encart renvoie à « consultez-nous ».
8. **p.23, n°20 Pasquiers** : classé en Rhône (Côtes du Rhône, Plan de Dieu, Sablet, Gigondas), mais le texte parle d'« appellations prestigieuses de Provence ».
9. **p.40, n°37 Dekeyne** : « La Voglonière » dans le texte, cuvée « Voglonniers » dans le tableau. Ce sont peut-être deux graphies légitimes.
10. **p.6, n°3 Colombier** : cuvée « Rouge au lèvres » (« aux lèvres » ?). C'est un nom propre : n'y touche pas sans accord.

## Corrections évidentes permises (à noter dans data/corrections.md)

- Noms : « Villlebois » (p.9) devient Villebois ; « Nadine ferrand » (p.14) devient Nadine Ferrand.
- Appellations : « Fief Vendéens » (p.5) devient Fiefs Vendéens ; « Muscadet Sevre & Maine » (p.6) devient Muscadet Sèvre et Maine ; « IGP CHardonnay » (p.6) devient IGP Chardonnay ; « Côtes du Rhone » (p.21) devient Côtes du Rhône ; « Montbazillac » (p.27) devient Monbazillac ; « Péssac-Léognan » (p.28) devient Pessac-Léognan ; « Côteaux Varois en Provence » (p.34) devient Coteaux Varois en Provence ; « VDF : Vins de France » (p.44) devient Vin de France.
- Langue : « c'est de la que vient » (p.12) devient « de là » ; « les tendance actuelles » (p.17) devient « tendances » ; « leur origines » (p.21) devient « leurs origines » ; « pratiques respectueuse » (p.22) devient « respectueuses » ; « REZE » (p.44) devient Rezé.
- Dans une colonne de couleur, « Rose » devient « Rosé » (par exemple p.34). Les noms de cuvées (« Rose de Solemme », « ROSE SÉRAME », « Esprit Rose ») restent tels quels.
- Formats : virgule décimale (« 5.80 € » devient « 5,80 € »), « 75cl » devient « 75 cl », « A partir » devient « À partir », un seul mot pour les bouteilles (bts, cols, bouteilles), départements dans l'ordre croissant (p.29). Jamais de changement de quantité ni de montant.
- Noms dans les encarts de panachage : « Maison du Cray » (p.15 et p.17) désigne le Château du Cray ; « Domaine Coyeux » et « Domaine du Coyeux » (p.19, 21 et 22) désignent le Domaine de Coyeux ; « Domaine des Guignottes » (texte p.17) désigne le Domaine Les Guignottes.
- Le sommaire et les titres de page divergent : choisis une forme et tiens-la partout. n°3 « Domaine du Colombier / J.Y Bretaudeau » ; n°12 « Maison André Goichot » ou « Maison et Domaine André Goichot » ; n°24 « Fabien Castaing » (son texte parle du Domaine de Moulin-Pouzy) ; n°30 « Château l'Escarderie » ; n°36 « Prieuré Sainte-Marie d'Albas » ; n°40 « Vazart-Coquart & Fils ».

## Le document « deep research / plan directeur »

Ce n'est pas une source. Il contient des erreurs : « Cain et Patricia » (à Gragnos, c'est Alain et Patricia) ; « Sérame » présenté comme un lieu (c'est un nom de cuvée de la Famille d'Exea) ; Falfas étiqueté Demeter (le PDF dit Biodyvin ; Demeter, c'est Pré la Lande) ; « Inopine, sans soufre » (la cuvée sans sulfites est « Balac Sans Sulfites ») ; Solemme « sans collage » (absent du PDF) ; des paliers inventés pour les Armagnacs (le PDF donne un tarif unique) ; des lieux déduits des noms de cuvées (Moulin Blanc « à Tavel », Pasquiers « à Sablet »). N'en reprends ni les faits ni la direction artistique.
