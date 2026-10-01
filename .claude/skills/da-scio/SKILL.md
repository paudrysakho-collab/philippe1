---
name: da-scio
description: Charte de direction artistique du catalogue Agence SCIO. À charger AVANT d'écrire la moindre page, feuille de style, illustration ou couverture du catalogue, et avant de choisir une couleur, une typo ou une composition. Contient les règles du logo, les tics de design interdits, les règles de la loi Évin et le protocole de validation d'une page.
---

# Direction artistique — catalogue Agence SCIO

Ce catalogue doit être **joyeux, rêveur, imaginatif**, et rester un **outil de travail
impeccable pour un caviste pressé**. En cas de conflit, cet ordre tranche :
**exactitude des faits et des prix → lisibilité → originalité et joie.**

## Avant d'écrire une ligne de CSS

1. Ouvre `CONCEPTS.md` et travaille **dans le concept retenu**, pas à côté.
2. Les valeurs de couleur, de typo et d'espacement vivent dans des **variables CSS**
   (`src/styles/systeme.css`). Jamais une couleur en dur dans un gabarit.
3. Le contenu vient de `data/catalogue.json`. **Aucun texte, aucun prix, aucun fait tapé
   à la main dans le HTML.**

## Le logo (non négociable)

- Présent au moins sur la couverture, la page de l'agence et la dernière page.
- **Jamais** recoloré, déformé, redessiné, rogné, ombré, ni posé en filigrane.
- Marge libre tout autour d'**au moins la hauteur du carré jaune** (≈ 28 % de la hauteur du logo).
- Fichier source : JPG CMJN 1030 × 251 px → **87 mm de large au maximum à 300 dpi**.
  Au-delà, il faut une version vectorielle ; le signaler dans `QUESTIONS.md`.
- Sur fond blanc ou très clair : `src/images/logo-agence-scio-detoure.png`.
  Sur fond foncé : une **réserve claire rectangulaire**, jamais le logo en blanc.
- Violet `#67067C` et or `#E1C853` : vérifier qu'ils restent fidèles après conversion sRGB.
- Ta palette **cohabite** avec ces deux couleurs : tu t'en inspires ou tu assumes un
  contraste, tu ne les fais jamais jurer.

## Les tics de design à ne jamais produire

Si tu te surprends à en écrire un, arrête-toi et change.

- Fond crème + grand titre serif + accent terracotta.
- Fond quasi noir + une seule couleur acide.
- Faux journal à filets fins.
- Cartes arrondies toutes identiques avec ombre grise.
- Surtitre en capitales espacées au-dessus de chaque titre.
- Informations reliées par des points médians en enfilade.
- Un seul mot en italique ou en couleur dans un titre « pour faire joli ».
- Des flèches partout.
- Police mono pour les petites étiquettes.
- Clichés du vin : noir et or, bordeaux et doré, papier kraft, taches de vin, verres qui
  trinquent, tire-bouchons, grappes clipart, photos génériques de banque d'images.

## Polices

Libres (licence OFL), prises sur Google Fonts ou `@fontsource`, **copiées dans `src/fonts/`**
et déclarées localement : la fabrication ne doit dépendre d'aucun accès réseau.
Tous les glyphes français : `é è ê ë à â ç ô û ù î ï œ Œ É À Ç ’ « » € °`.

**Jamais** : Inter, Roboto, Arial, Helvetica, Open Sans, Lato, Montserrat, Poppins,
Playfair Display.

Contrôle obligatoire après chaque génération : `pdffonts dist/*.pdf` → toutes les polices
`emb = yes`, aucune police de repli.

## Lisibilité (plancher absolu)

| Élément | Minimum |
|---|---|
| Texte courant | 9 pt |
| Tableaux de prix | 7,5 pt |
| Mesure de lecture | 70 à 75 signes par ligne, jamais plus |
| Couleurs | imprimables en quadrichromie, aucun fluo d'écran |
| Contraste | franc ; un gris clair sur fond clair est un défaut, pas une finesse |

## Loi Évin — c'est de la communication sur l'alcool en France

Même destiné aux professionnels.

**Interdit, en illustration comme en photo :** personnages qui boivent, trinquent ou portent
un verre à la bouche ; fête arrosée ; ivresse ; séduction ; sport ; réussite sociale associée
au vin.

**Permis :** terroirs, saisons, paysages, bêtes, plantes, ciels, matières, chais, bouteilles,
portraits de vignerons, jeux graphiques.

Le **message sanitaire** reste présent : « L'ABUS D'ALCOOL EST DANGEREUX POUR LA SANTÉ.
À CONSOMMER AVEC MODÉRATION. »

## Illustrations

Dessinées par toi en **SVG ou CSS**, ou génératives **à graine fixe** (une même entrée donne
toujours le même dessin). **Aucune bibliothèque d'icônes.** Voir la compétence `picto-maison`
pour les pictos de label et de couleur de vin.

## Le protocole de validation d'une page

Avant de déclarer une page terminée, dans cet ordre :

1. **Retire un accessoire.** Une page a presque toujours un élément de trop. Enlève-le.
2. **Sois audacieux à un seul endroit** et discipliné partout ailleurs. Deux audaces sur une
   page, c'est une de trop.
3. **Regarde la page en image**, pas dans le navigateur (voir la compétence `epreuve-pages`).
4. **Relis le texte face à `texte_source`** : aucun fait ajouté, aucun fait utile perdu.
5. Si quelque chose te semble ambigu dans la source, **n'arbitre pas** : écris-le dans
   `QUESTIONS.md`.
