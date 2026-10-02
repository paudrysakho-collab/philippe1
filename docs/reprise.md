# Reprise : où en est le projet, et la suite (2 octobre 2026)

> **Fait le 2 octobre (seconde session)** : les trois livrables sont livrés.
> - A : `dist/catalogue-scio-2026-*` (**52 pages au plus**, demande de l'agence : plus
>   d'ouvertures de région ni d'index des domaines, lignes de tableau serrées, bande du haut
>   abaissée sur les fiches qui débordent de peu ; sommaire simple, note de prix sous le
>   tableau ; textes et labels du dossier de Mathéo sur les 31 fiches du salon) ;
> - B : `dist/salon-prive-2026-*` (48 pages, sans plan des exposants, `npm run salon`), prix
>   vides, à remplir par `tableur/prix-salon-prive-2026.xlsx` (README, « Le Salon Privé ») ;
>   vins, textes et labels du **dossier de référence de Mathéo**
>   (`sources/salon-prive-2026/matheo-dossier-reference.pdf`), qui fait foi ;
> - C : `dist/salon-prive-2026-liste-des-vins.pdf` (3 pages A4, 180 vins).
> Ce qui reste ouvert : `QUESTIONS.md`, points 26 (écarts dossier / tarif), 27, 29 (ouvertures
> au salon ?) et 30 (n°40 « Troisième domaine certifié HVE »).

Ce fichier passe le relais à une nouvelle session. Le brief de `CLAUDE.md` reste la règle ;
ce qui suit dit ce qui est déjà fait, comment l'outil marche, et ce qu'on attend maintenant.

## 1. Avant tout : la bonne branche

Tout le travail est sur **`claude/design-skill-propositions-suwoa9`**. Si ta session a
démarré sur une autre branche, rapatrie celle-ci d'abord, sans rien perdre :

```sh
git fetch origin claude/design-skill-propositions-suwoa9
git merge origin/claude/design-skill-propositions-suwoa9   # ou checkout, si ta branche est vide
```

Vérifie ensuite que `docs/reprise.md`, `data/salon-prive-2026.json` et
`sources/salon-prive-2026/` sont là.

Outils à installer en début de session (le conteneur repart de zéro) :

```sh
npm install
apt-get install -y poppler-utils libreoffice-impress libreoffice-calc
pip install pymupdf openpyxl fonttools defusedxml lxml
```

Chromium est déjà installé pour Playwright, sans téléchargement.

## 2. Ce qui est fait : le catalogue général, étapes 1 à 6 du brief

**Ne rien refaire.**

- **Concept retenu** : « Sous nos pieds ». Chaque région est une strate de sol (couleur et
  trame), la tranche du catalogue fermé montre les dix bandes, et chaque fiche ouvre sur
  son sol. Le détail est dans `CONCEPTS.md`, concept 1, et les décisions dans `JOURNAL.md`.
- **Format** : 210 × 260 mm, 76 pages.
- **Palette** : tuffeau `F2EADA`, craie `FBF8F1`, silex `46606E`, gneiss `A8515F`,
  amphibolite `3C5B47`, sables `D08C3C`, violet `67067C`, or `E1C853`, encre `2A3942`.
- **Polices** : Young Serif pour les titres et la lettrine, Spectral pour les textes,
  IBM Plex Sans pour les tableaux.
- **Livrables** dans `dist/` :
  - `catalogue-scio-2026-ecran.pdf` et `catalogue-scio-2026-imprimeur.pdf` ;
  - `catalogue-scio-2026-canva.pptx` et `catalogue-scio-2026-canva-recadrable.pptx`, pour
    Canva, avec textes et tableaux modifiables.
- **Images** : 79 photos posées sur 80 emplacements. Il manque la bouteille du n°18. Tout est
  sourcé dans `credits.md`.
- **Tableur des prix** : `tableur/tarifs-scio-2026.xlsx`, aller et retour avec l'agence
  (`npm run tableur`, puis `npm run importer -- fichier.xlsx`).

### La chaîne de fabrication

- **Les données** : `data/fiches/NN.json` (une fiche par domaine, prix en centimes) sont
  assemblées en `data/catalogue.json` par `scripts/assembler.py`, puis vérifiées par
  `scripts/verifier-donnees`.
- **Le PDF** : `scripts/construire.mjs` pagine (`build/plan.json`) avec les gabarits
  `src/gabarits/pages.mjs` et `pieces.mjs` et le style `src/styles/systeme.css`, rend dans
  Chromium et mesure les hauteurs (`build/mesures.json`). Il complète seul jusqu'à un
  multiple de 4 avec des pages « respiration » (Vos notes).
- **Le contrôle** : `scripts/controler.mjs` retrouve chaque prix dans le texte du PDF,
  vérifie les polices et le nombre de pages.
- **Le .pptx** : `scripts/pptx.mjs` reprend la même géométrie (`build/mesures.json`), puis
  `scripts/ranger-pptx.py` remet le XML à la norme et `scripts/controler-pptx.mjs` vérifie.
- **Une seule commande** : `npm run build` enchaîne données, PDF, contrôle et pptx.

### Les compétences à charger

Elles sont dans `.claude/skills/` : `da-scio` avant toute page, `tableau-tarif` avant tout
tableau, `picto-maison`, `photos-domaines` et `epreuve-pages` (regarder chaque page en image
avant de livrer).

### Ce qu'on a appris à nos dépens sur Canva

- **La lettrine.** À l'import d'un .pptx, Canva ramène un paragraphe à une seule police et une
  seule taille. La lettrine est donc une **boîte de texte à part**, calée sur la première
  ligne. Si les textes des domaines ou le haut des fiches changent, relance
  `python3 scripts/regler-lettrines.py` (voir `JOURNAL.md`, « La lettrine disparaissait » et
  suivants).
- **Les polices.** Canva ne connaît ni Young Serif ni Spectral : il les remplace (TYSerif,
  Arimo) tant que l'agence ne les a pas téléversées (`polices-canva/LISEZ-MOI.md`).
- **Tester un import.** Le dépôt est public : on importe dans Canva depuis l'adresse
  `raw.githubusercontent.com` d'un commit poussé, puis on exporte le PDF et on le mesure
  (`essais/mesurer-lettrines.py`).

### Questions encore ouvertes

Elles sont dans `QUESTIONS.md` :
- point 22 : les labels du tarif et ceux du salon divergent ;
- point 24 : la bouteille du n°18, et la Mondeuse posée au n°21 ;
- point 20 : le texte du n°1, repris de la liste du salon ;
- point 25 : les questions du salon.

## 3. La suite : trois livrables

### Livrable A : le catalogue général, avec les retouches du responsable

1. **Supprimer la page 3**, « Comment lire ce catalogue » (`mode-emploi`), **et la page 5**,
   « Les quatre alliances » (`alliances`). Voir `scripts/construire.mjs` (descripteurs, et
   `AVANT = 5`), `src/gabarits/pages.mjs` et `scripts/pptx.mjs`. Le panachage reste visible
   sur chaque fiche (jeton « Panachage », ligne « Se panache avec… ») ; vérifie qu'aucun
   texte ne renvoie encore à ces pages.
2. **Un sommaire simple** à la place de « La coupe » (page 4) : « comme on faisait
   d'habitude ». C'est une liste par région ; sous chaque région, les domaines numérotés
   avec leur page, sur deux colonnes, dans les couleurs et les polices du catalogue (le nom
   de région dans sa couleur de strate). Pour la *structure* seulement, voir le sommaire du
   tarif source (`data/pages/p-03.png`) ; son dessin, lui, reste ignoré (règle d'or 4).
3. **La note de prix, plus grosse et juste sous le tableau.** Par exemple « * Prix de la
   bouteille H.T. hors frais de transport. » : aujourd'hui elle est en petit dans le pied de
   page de la fiche (`pages.mjs`, vers la ligne 407 ; `pptx.mjs`, vers la ligne 417). Elle
   doit venir **à la suite immédiate du dernier tableau**, en plus gros (au moins 10 pt),
   bien visible. C'est « hyper important » pour l'agence. Les départements de distribution
   peuvent rester en pied de page. À faire sur toutes les fiches, et dans le .pptx aussi.
4. **Après** : `npm run build`, regarde chaque page (`epreuve-pages`), et relance
   `regler-lettrines.py` si le haut des fiches a bougé. Le nombre de pages se recale seul
   sur un multiple de 4.

### Livrable B : le catalogue du Salon Privé Vins & Terroirs

- **L'événement** : lundi 5 octobre 2026, Château de la Rairie, Pont-Saint-Martin.
  26 vignerons exposants, 9 régions (pas de Beaujolais), organisé par l'Agence SCIO.
- **La même DA que le catalogue général** (demande expresse) : même concept, mêmes polices,
  mêmes composants. C'est une **édition** du même générateur (par exemple
  `EDITION=salon npm run build`), pas une copie des gabarits. Les retouches du livrable A
  s'y appliquent aussi.
- **On voit tout de suite que c'est le salon.** Sur la couverture et la page de l'agence :
  le nom du salon, la date, le lieu. Sur chaque fiche, le **numéro de stand**, pour la
  retrouver sur le plan.
- **Le plan des exposants fait foi** (réponse de l'agence, 2 octobre) : en cas de
  divergence entre les documents du salon, le plan l'emporte.
- **Les exposants** : `data/salon-prive-2026.json` rapproche les 26 stands de 31 fiches.
  Strasser Radziwill (stand 7) couvre les quatre fiches n°16 à 19 ; Goichot (stand 26)
  couvre les fiches n°12, 13 et 14. Pas de jus de cépages d'Exea (fiche n°33 exclue).
  Divin No Low (fiche n°7) est « normalement » sur le stand de Jean de Villebois : la fiche
  entre si le fichier de Mathéo en liste des vins. Les fiches 9, 11, 20, 24, 25, 26, 33 et 35
  ne sont pas au salon.
- **Les tableaux ne montrent que les vins dégustés**, d'après le **fichier de Mathéo**, qui
  fait foi pour cette liste.
  - **Comment le lire** (consigne de l'agence) : ne prends que **les listes de vins des
    cartes de stand**. Ignore les pages d'habillage (liste des domaines, plan « version
    esthétique »).
  - **Attention aux pages doubles** : une même page peut porter **deux vignerons côte à côte,
    séparés par un trait vertical**, chacun avec son numéro de stand, son nom et sa propre
    « Liste des vins ». Ne mélange jamais leurs vins : rattache chaque ligne au stand de sa
    colonne, et vérifie le total (26 stands).
  - Le Padlet déjà déposé (`padlet-vins-a-deguster.pdf`, 20 pages) a cette forme : page 1 la
    liste des domaines, page 2 le plan, puis les cartes, une ou deux par page.
  - Chaque vin se rapproche d'une ligne du tarif (`data/fiches/`) : appellation, cuvée,
    couleur, millésime, contenance.
  - Un vin absent du tarif, ou d'un autre millésime, va dans `QUESTIONS.md`. On n'invente
    rien.
  - Le Padlet (`sources/salon-prive-2026/padlet-vins-a-deguster.pdf`, en images : zoomer)
    est une version antérieure des listes par stand, utile pour recouper.
- **Les prix ne sont pas encore connus** : l'agence les ajoutera après.
  - Les colonnes de prix sont là, avec des cases **vides**.
  - Les prix vivent dans les données (par exemple `prix_centimes: null` dans
    `data/salon-prive-2026.json`). Les remplir et relancer le build doit suffire ;
    prévois aussi l'aller-retour par le tableur, en étendant `scripts/tableur.py`.
  - Le contrôle « chaque prix du JSON est dans le PDF » doit accepter ces prix absents
    tant qu'ils le sont.
  - **Un seul prix par vin, ou les paliers du domaine : l'agence ne le sait pas encore.**
    Le tableau doit accepter les deux sans retouche de gabarit. Par défaut, il reprend les
    paliers du tarif du domaine, cases vides. Si l'agence donne un prix unique, la même donnée
    bascule le tableau sur une seule colonne « Prix salon ».
- **Les labels : la liste des vignerons fait foi** (`sources/salon-prive-2026/liste-des-vignerons.pdf`).
  - Chaque fiche du salon affiche le label de la notice de son stand, tel quel ; c'est déjà
    rapproché dans `labels_affiches` de `data/salon-prive-2026.json`.
  - Nouveaux libellés : « En conversion Bio », « Biodynamie », « ISO 26000 », « Agriculture
    raisonnée », « HVE 3 », « Bio & Biodynamie ». Ils demandent de nouveaux pictos maison
    (compétence `picto-maison` ; jamais les logos officiels), légendés.
  - Pour le reste, l'agence veut de la sobriété : « pour le 5, moins on en dit, moins on fait
    d'erreur ». Rien que le tarif ne dise. Les textes des documents du salon ne sont pas une
    source de faits.
  - **À demander en début de session** : cette liste vaut-elle aussi pour les labels du
    catalogue général (point 22) ?
- **Sorties** : `dist/salon-prive-2026-ecran.pdf`, `dist/salon-prive-2026-imprimeur.pdf`
  et un `.pptx` pour Canva. C'est le seul des trois livrables qu'on modifiera encore, pour
  les prix.

### Livrable C : la liste des vins dégustés, par domaine (2 à 3 pages)

- Pour chaque stand : numéro, nom, région, puis la liste des vins dégustés (cuvée,
  appellation, couleur, millésime).
- Même DA, mêmes données que le livrable B, sans prix.
- Sortie : `dist/salon-prive-2026-liste-des-vins.pdf`.

## 4. Les documents du salon (`sources/salon-prive-2026/`)

| Fichier | Ce qu'il apporte |
|---|---|
| `liste-des-domaines.pdf` | les 26 domaines par région avec leur **numéro de stand** |
| `plan-des-exposants.pdf` | **fait foi** (version 2 du 2 octobre, identique à la première) : le plan des salles (Salle Blanche, Salle Noire), les stands 1 à 26, l'accueil, les contacts |
| `liste-des-vignerons.pdf` | une notice par vigneron (numérotée 1 à 26 par région : ce **ne sont pas** les numéros de stand) |
| `padlet-vins-a-deguster.pdf` | une carte par stand, numérotée comme les stands, avec une « liste des vins » |
| *à venir* : le fichier de Mathéo | **les vins dégustés**, qui font foi |

Ces documents ont leur propre habillage (serif bordeaux, Padlet). **On n'en reprend pas le
dessin** : le salon garde la DA du catalogue.

## 5. Les réponses de l'agence (2 octobre) et ce qui reste ouvert

Les réponses sont au point 25 de `QUESTIONS.md` et dans `reponses_agence` de
`data/salon-prive-2026.json`. Rien n'empêche de commencer.

Restent ouverts :
- prix unique ou paliers, d'où le tableau qui accepte les deux ;
- Divin No Low, que le fichier de Mathéo tranchera ;
- le format de la liste des vins (A4 ou le format du catalogue) : propose-le à l'agence.
