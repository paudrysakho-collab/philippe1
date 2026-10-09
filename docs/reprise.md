# Reprise : où en est le projet (9 octobre 2026)

Ce fichier passe le relais d'une conversation à la suivante. **Lis-le en entier avant de
toucher à quoi que ce soit.** Le brief de `CLAUDE.md` reste la règle ; ce fichier dit ce qui
est fait, comment l'outil marche, ce que l'agence a décidé depuis le brief, et la suite.
L'historique détaillé (essais, erreurs, raisons) est dans `JOURNAL.md`.

## 0. Tu es la suite de la session précédente

Tu n'es pas une nouvelle personne sur le projet : **tu continues le travail de la
conversation précédente**, avec le même interlocuteur (l'agence SCIO), les mêmes outils et les
mêmes décisions. Tout ce qui a été tranché est ici, dans `JOURNAL.md` et dans
`QUESTIONS.md`. Ne refais rien, ne réexplique rien, **ne redemande rien de ce qui est déjà
décidé**. Pas de questionnaire en début de session : fais l'installation de la section 1
sans en parler, lis ce fichier, puis traite la demande.

### Comment il travaille, et ce qu'il attend

- **Il écrit vite, souvent à la voix**, en français familier, sans ponctuation, avec des
  fautes. Lis l'intention, pas la lettre (exemples plus bas).
- **Agis, ne demande pas.** Si la demande est claire à 80 %, fais-la avec le choix le plus
  raisonnable, montre le résultat, et dis en une ligne ce que tu as choisi : il corrigera
  s'il veut autre chose. Pas d'`AskUserQuestion` pour un choix de mise en page, de taille,
  de place ou de méthode : ces choix-là sont à toi.
- **Les seules choses qu'on ne fait jamais sans lui** : inventer ou corriger un prix ou un
  fait (on le note dans `QUESTIONS.md` et on continue le reste), et effacer son travail.
  Une question n'est permise que si une donnée manque vraiment et ne se déduit de rien.
  Une seule question à la fois, à la fin du message, jamais pour bloquer le reste.
- **Il a ses fichiers sur son Google Drive** (« tout est sur Drive ») ou les joint au
  message. Cherche toi-même dans le Drive (connecteur Google Drive, `list_recent_files`,
  `search_files`) avant de lui demander un fichier.
- **Il veut voir** : après chaque changement visible, envoie les PNG des pages touchées et
  les PDF refaits (`SendUserFile`), avec les chemins exacts dans le dépôt. Commit et push à
  chaque étape.
- **Réponses courtes** : ce qui est fait, ce qui reste ouvert, et c'est tout. Pendant une
  tâche longue, une ligne de temps en temps pour dire où tu en es.
- **Un fichier renvoyé identique** à ce qui est déjà appliqué : dis-le simplement, preuve à
  l'appui (comparaison au pixel), et ne refais rien.
- **Avant de dire « c'est fait »** : contrôles automatiques au vert et pages touchées
  regardées en image (compétence `epreuve-pages`).

### Ses demandes passées, et ce qu'elles voulaient dire

| Il a écrit | Ce qu'il voulait, et ce qui a été fait |
|---|---|
| « agrandis l'écriture mais pas les tableaux, c'est grave possible » | Texte des tableaux plus gros et plus gras, **lignes resserrées** pour que les tableaux ne grandissent pas |
| « 76 pages c'est beaucoup trop, une cinquantaine, 52 pages max » | Compacter sans toucher à la DA : lignes serrées, ouvertures de région retirées, bande du haut abaissée |
| « on voit vraiment pas la meuf, faut peut-être rétrécir l'image » | Recadrer plus large le rond (reculer), pour voir les deux personnes entières |
| « t'as trop découpé, c'est bizarre » (bouteilles) | Le détourage mangeait le verre : le refaire, vérifier sur fond magenta |
| « tout est bon dans son document maintenant » (Mathéo) | Le dossier de Mathéo fait foi pour les textes, labels et vins, **dans les deux éditions** |
| « juste pour toutes les listes, millésime, appellation, etc., il faut prendre le document de Mathéo » | Afficher les vins **tels que le dossier les écrit** (corrigés seulement dans la forme) |
| « il a mis un c à Mols et un i à demoiselle » | Corriger ces deux fautes, et elles seules |
| « mets en parenthèse au niveau du sommaire en petit » | Mention discrète sous le nom, sans tronquer le nom |
| « le plus facile à imprimer, celui qui coûte le moins de couleurs » | Version sobre en encre (pastille de couleur au lieu de bandes pleines) |
| « vas-y, tu continues » / « tu gères » | Feu vert : enchaîner sans redemander |
| « prends que les images, le reste est nul » (ancien catalogue) | Banque d'images = ses images seulement ; jamais ses textes ni sa mise en page |
| « les photos que t'as pas trouvées, cherche-les sur internet » | Sites officiels des domaines (puis Commons) ; noter l'URL dans `photos-locales.json` |
| « tu mets le millésime le plus récent quand tu as un doute » | Règle générale pour « 2022-23 », « 2016/2020 »… |
| « mets les pages à gauche » | Numéros de page à gauche partout (édition globale) |
| Messages vocaux transcrits, longs, avec du bruit (téléphone, blagues : « Philippe Audry ») | Ne garder que les consignes ; demander une seule fois ce qui reste obscur |

## 1. Avant tout : la branche et les outils

Tout le travail est sur **`claude/design-skill-propositions-suwoa9`**. **Commence toujours
par te mettre à jour sur GitHub** : un conteneur peut avoir été cloné avant les derniers
envois.

```sh
git fetch origin claude/design-skill-propositions-suwoa9
git status --short                      # vide : rien à toi, on peut s'aligner sans risque
git checkout -B claude/design-skill-propositions-suwoa9 origin/claude/design-skill-propositions-suwoa9
```

**Ta copie est périmée** si tu vois l'un de ces signes : `sources/salon-prive-2026/` sans
`matheo-dossier-reference.pdf`, un `docs/reprise.md` daté du 2 octobre qui parle de
« Livrable A : retouches », de « supprimer la page 3 », du « fichier de Mathéo à venir » ou
de la question des labels (point 22). Dans ce cas : resynchronise comme ci-dessus, puis
**relis `CLAUDE.md` et ce fichier avec l'outil de lecture** (ceux chargés au démarrage de la
session sont l'ancienne version) et oublie ce que l'ancienne version te faisait demander.

Le conteneur repart de zéro à chaque session :

```sh
npm install
apt-get install -y poppler-utils libreoffice-impress libreoffice-calc
pip install pymupdf openpyxl fonttools defusedxml lxml rembg onnxruntime
mkdir -p ~/.local/share/fonts && cp polices-canva/*.ttf ~/.local/share/fonts/ && fc-cache -f
# au besoin, pour relire un PDF-image : apt-get install -y tesseract-ocr tesseract-ocr-fra
```

Chromium est déjà installé pour Playwright. Les polices dans `~/.local/share/fonts` servent
au réglage des lettrines du .pptx (LibreOffice) ; sans elles, `regler-lettrines.py` échoue.

## 2. Ce qui est livré (`dist/`, tout est poussé)

| Livrable | Fichiers | État |
|---|---|---|
| **Catalogue général** « Sous nos pieds » | `catalogue-scio-2026-ecran.pdf`, `-imprimeur.pdf`, `-canva.pptx`, `-canva-recadrable.pptx` | **52 pages**, 40 domaines, 715 prix, 80 images |
| **Salon Privé Vins & Terroirs**, lundi 5 octobre 2026, Château de la Rairie | `salon-prive-2026-ecran.pdf`, `-imprimeur.pdf`, `-canva.pptx` | **48 pages**, 26 stands, 32 fiches, **prix posés le 3 octobre** (439 prix), nouveau design |
| **Liste des vins dégustés** | `salon-prive-2026-liste-des-vins.pdf` | 3 pages A4 |
| Tableurs (aller-retour des prix) | `tableur/tarifs-scio-2026.xlsx`, `tableur/prix-salon-prive-2026.xlsx` | à jour |
| Aperçus PNG | `epreuves/apercus/` (planches et pages détaillées des trois livrables) | à jour |
| **Catalogue caviste global** « Catalogue caviste — Vins & Terroirs » (**travail en cours**, section 9) | `catalogue-caviste-2026-ecran.pdf`, `-imprimeur.pdf` | **64 pages**, 41 fiches, 11 régions (Beaujolais et Bugey en plus), 598 prix ; pas encore de .pptx |
| Affiche QR du catalogue du salon | `salon-prive-2026-affiche-qr.pdf` (`npm run affiche-qr`) | A4, sobre en encre |

Le 2 et le 3 octobre, tout a été revérifié : contrôles automatiques au vert, liens de la
version écran, polices, et **chaque page regardée en image**.

## 3. Les commandes

```sh
npm run build          # catalogue général : données vérifiées, PDF, contrôle, deux .pptx
npm run salon          # Salon Privé : données, PDF, contrôle, .pptx, liste des vins
npm run liste-vins     # la liste seule (LISTE_FORMAT=catalogue pour le format 210 × 260)
npm run tableur        # tarifs → xlsx ; npm run importer -- fichier.xlsx [--essai]
npm run tableur-salon  # prix du salon → xlsx ; npm run importer-salon -- fichier.xlsx [--essai]
npm run transcrire-matheo            # refait les vins du salon depuis scripts/transcrire-matheo.py
python3 scripts/textes-matheo.py     # reporte textes et labels du dossier de Mathéo sur les fiches
python3 scripts/regler-lettrines.py  # lettrines du .pptx ; EDITION=salon pour le salon
```

- **Les données** : `data/fiches/NN.json` (prix en centimes) → `data/catalogue.json`
  (`scripts/assembler.py`), vérifiées par `scripts/verifier-donnees`. Le salon :
  `data/salon-prive-2026.json` (stands, vins, `prix_centimes: null`, `mode_prix`).
- **Le PDF** : `scripts/construire.mjs` (pagination mesurée dans Chromium), gabarits
  `src/gabarits/pages.mjs` et `pieces.mjs`, styles `src/styles/systeme.css` et `pages.css`.
  L'édition se choisit par `EDITION=salon` (objet `ED` de `pages.mjs`).
- **Le .pptx** : `scripts/pptx.mjs` reprend la géométrie mesurée (`build/<base>-mesures.json`
  et `-plan.json`). Si le haut des fiches ou un texte de domaine change, relance
  `regler-lettrines.py` (25 min environ par édition, en tâche de fond), puis `npm run pptx`
  et `npm run pptx-salon`.

### Piège : les photos

Les **originaux** des photos sont dans `src/photos/brut/`, **ignoré par git** : ils ne sont
pas dans le conteneur. Les images préparées (`src/photos/rond/`, `src/photos/bouteille/`) et
`data/photos-preparees.json` sont, elles, dans le dépôt.
- **Ne lance jamais `npm run photos` (tout) sans les originaux** : le script vide d'abord
  les dossiers d'images, puis écarte tout ce qu'il ne trouve pas. Tout serait perdu.
- Pour une seule image : remets son original dans `src/photos/brut/` (chemin écrit dans
  `data/photos-locales.json`) et lance
  `python3 scripts/preparer-photos.py --seulement N [--role bouteille]`.
- Les originaux sont sur le **Drive de l'agence** (« tout est sur Drive ») : dossiers
  `Bouteilles_de_vin/`, `Domaines_et_vignerons/`, et `les photos gemini/photo gemini/` pour les
  neuf bouteilles retouchées. Le connecteur Drive rend un fichier en base64 dans un fichier
  de `tool-results` : on le décode avec Python (voir `JOURNAL.md`, 2 octobre).
- Une bouteille détourée se vérifie sur un **fond magenta** : il montre la moindre bavure.

## 4. Ce qui fait foi (décisions de l'agence depuis le brief)

| Pour… | La source | Où c'est dans le dépôt |
|---|---|---|
| prix, paliers, contenances, note de prix, départements | **le tarif de septembre 2026** (seul, comme dit le brief) | `data/fiches/` |
| **textes et labels des 31 fiches présentes au salon**, dans les **deux** éditions | **le dossier de référence de Mathéo** (« tout est bon dans son document ») | `sources/salon-prive-2026/matheo-dossier-reference.pdf`, `scripts/textes-matheo.py` ; le texte du tarif reste dans `texte_tarif` |
| **les vins du salon** : cuvée, appellation, couleur, millésime, **tels qu'écrits** | le dossier de Mathéo, corrigé seulement dans la forme | `scripts/transcrire-matheo.py` (`CORRECTIONS`) ; le tarif ne donne que la contenance et le tableau |
| numéros de stand et salles | le plan des exposants | `data/salon-prive-2026.json` |
| les couleurs que personne ne donnait | l'agence, vin par vin | `COULEURS_AGENCE` de `transcrire-matheo.py` |
| les labels des 9 fiches absentes du salon | le tarif | `labels_tarif` |

- **Noms propres** : comme sur le logo du domaine, jamais comme une faute du dossier :
  **Berteaud Manceau**, **Boehler**. Corrections signalées par l'agence : « Molsce » →
  **Molse**, « demoiseilles » → **Demoiselles**.
- Le dossier de Mathéo a été renvoyé trois fois le 2 octobre au soir
  (`…_compressed.pdf`, `ma-sandbox-magnifique_board_…_2_2.pdf`, `…_2_3_compressed.pdf`) :
  c'est **la même exportation du Padlet (15 h 44 UTC)**, vérifiée au pixel et par OCR. Rien à
  réappliquer. **Le 3 octobre au matin, une vraie nouvelle exportation** (8 h 44 UTC) est
  arrivée et a été appliquée (`JOURNAL.md`, 3 octobre) ; au stand 26, l'agence veut « AOP
  Bourgogne Chardonnay 2023 », sans le nom du château. S'il change encore, comparer d'abord au pixel avec la version en place (méthode
  dans `JOURNAL.md`), puis relire par OCR (Tesseract lit souvent un 9 comme un 4 dans
  l'écriture du Padlet : vérifier les dates à l'image).

## 5. Les consignes de l'agence (à tenir)

- **Catalogue général : 52 pages au plus.** Pas de pages d'ouverture de région ni d'index des
  domaines (options `ouvertures` et `indexDomaines` de `ED`) ; le Salon Privé les garde.
  Quand une fiche déborde de peu, sa bande du haut s'abaisse (`BANDES`, `pieces.mjs`).
- **Tableaux** : écriture grande et grasse (cuvée 9,6 pt demi-gras, prix 10 pt) **mais lignes
  serrées** (8,6 mm) ; « agrandis l'écriture mais pas les tableaux ».
- **La note de prix** (H.T., franco, départ chai…) **juste sous le dernier tableau**, en
  10,5 pt : « hyper important ».
- **Sommaire simple**, « comme d'habitude », sobre en encre (une pastille de couleur par
  région). Les quatre domaines du groupe portent **« (Vignobles Strasser Radziwill) »** en petit
  sous leur nom (`mention_sommaire`, `data/agence.json`).
- **Couverture** : l'édition et la date en haut (« Tarifs cavistes Vendée (85) 2026 » ;
  « Lundi 5 octobre 2026 »). Pas de plan des exposants dans le salon.
- **Sobriété au salon** : « pour le 5, moins on en dit, moins on fait d'erreur ».
- **Pas de mot seul** en fin de ligne dans une cuvée (`sansVeuve()`, `pieces.mjs`).
- Avec l'agence : écrire en français simple, envoyer les PNG et PDF (et leurs chemins
  exacts sur GitHub), commit et push après chaque étape.

## 6. Questions encore ouvertes (`QUESTIONS.md`)

- **10** : « Rouge au lèvres » (tarif) ou « Rouge **aux** lèvres » (l'étiquette de la bouteille).
- **26** : les écarts entre le dossier de Mathéo et le tarif (46 vins absents du tarif, 53
  écarts), à relire avant impression.
- **27** : prix du salon (prix unique ou paliers : le tableau accepte les deux), format de la
  liste des vins, une seule graphie des noms de stand ?
- **29** : retirer aussi les ouvertures de région du Salon Privé ?
- **30** : le texte de Vazart-Coquart (n°40) n'a plus « Troisième domaine certifié HVE de
  France » (le dossier de Mathéo l'a retiré).
- Les anomalies du tarif (points 1 à 9, 11 à 14) restent signalées, jamais corrigées seules.

## 7. Où on en est (3 octobre, soir) et la suite

**Fait et validé par l'agence aujourd'hui** (tout est poussé, `dist/` à jour) :
- **Prix du Salon Privé posés** depuis les tarifs annotés (`sources/salon-prive-2026/scans-prix/`,
  relevé `data/prix-salon-releve.md`) par `scripts/prix-salon.py` : paliers du salon par fiche
  (`paliers_salon`, clé « fiche » ou « fiche:tableau »), prix, offres « 11+1 / 5+1 » après le nom
  du vin, offre du stand sous la note de prix (`offre_salon`), note de prix propre au salon
  (`note_prix_salon`, Boehler franco), magnums et lignes ajoutées (`AJOUTS`), contenance jamais
  vide (« 75 cl », « 1,5 L »). 439 prix, aucune case vide. Règles : prix **surlignés** ;
  « À partir de… » ; « cols » pour les offres ; un magnum surligné = une ligne de plus.
  Retoucher un prix : dans `scripts/prix-salon.py` (rejoué après `npm run transcrire-matheo`),
  puis `npm run salon`.
- **Nouveau design, les deux éditions** (choix de l'agence parmi les modèles de
  `concepts/retouches-oct/`) :
  - **couverture H** : photo de vignoble (Sud-Ouest) en haut, strates **droites et sobres**
    dessous (`coupeElegante({ style: 'fine' })`, `pieces.mjs`), titre craie et or, réserve claire
    sous le logo ; la responsable trouvait les anciennes bandes ondulées « enfantines » ;
  - **page 2 A** : texte en Spectral 14,5 pt avec filet or (plus de mots en violet), photo du
    Beaujolais au coucher du soleil (catalogue général ; au salon, l'encart du salon reste) ;
  - **ouverture de région A** (salon) : la photo de la région en fond, assombrie vers le bas ;
  - **bas de fiche A** : la photo de la région à la place du dessin de sol ;
  - page finale : bandeau de strates droites.
  - Les **tableaux ne bougent pas** (« la partie tableaux, c'est parfait »).
- **Photos de régions** : une par région, Wikimedia Commons, licences libres
  (`data/photos-regions.json`, `credits.md`, crédit en dernière page). Originaux dans
  `src/photos/regions-brut/` (ignoré par git), versions traitées dans `src/photos/regions/`
  (`scripts/preparer-photos-regions.py`). Recherche : `scripts/chercher-photos-regions.py`
  (Commons limite fort les téléchargements : 429 → attendre, passer par `iiurlwidth`).
- **.pptx** : les photos de la déco sont exportées en JPEG (`deco.mjs`), sinon > 50 Mo.
- Dessins maison disponibles (pas encore posés) : `src/gabarits/dessins.mjs` (bouteilles,
  feuille, cep, lune, soleil, paysage de coteaux).

**Relecture du salon appliquée (3 octobre, soir)** : validité « du 5 octobre au 14 novembre
2026 » en couverture, strates à 108 mm, date sur pastille gneiss ; offre avant la note de prix ;
deux notes de prix seulement ; « Possibilité de panacher avec… » réservé aux trois familles ;
Berteaud sans la colonne 36 ; folios toujours à droite (`JOURNAL.md`).

**8 octobre : catalogue caviste global** (`npm run global`, `EDITION=global`) : base salon, sans
numéros, domaines réintégrés depuis les scans du 8 octobre (`sources/catalogue-global-2026/`,
`scripts/prix-global.py`, relevé `data/catalogue-global-releve.md`, questions point 32). 64 pages.
En attente : précisions de l'agence sur Les Lys ; le .pptx de cette édition.

**À faire ensuite** :
1. ~~Recharger la photo de Bourgogne en grand~~ : **fait le 3 octobre au soir** (original
   3072 × 1461 px, traité en 2400 × 1141 ; les deux catalogues refaits).
2. ~~Pinot Noir des Guignottes~~ : 8,90 / 8,60 / 8,10 **confirmé** par l'agence (3 oct. soir).
   La photo de Bourgogne actuelle convient à l'agence.
   Couverture du salon : plus de date ni de lieu en haut à droite ; « Tarif et offres valables
   du 5 octobre au 14 novembre 2026 » en grand (21 pt). Stand 16 : formule « au volume ».
3. Si l'agence le demande : poser quelques petits dessins de `dessins.mjs` (jamais dans les
   tableaux), d'autres photos de lieux sur les fiches.

Règles qui tiennent : charger `da-scio` (et `tableau-tarif` pour un tableau) avant toute
retouche ; `npm run build` (≤ 52 pages) et `npm run salon` (48) ; regarder les pages touchées
en image ; un prix ne se corrige jamais seul ; commit et push à chaque étape.

## 8. Ce qu'on a appris à nos dépens

- **Canva et la lettrine** : à l'import d'un .pptx, Canva ramène un paragraphe à une police et
  une taille ; la lettrine est donc une boîte à part, calée par `regler-lettrines.py`. Canva
  remplace Young Serif et Spectral tant que l'agence ne les a pas téléversées
  (`polices-canva/LISEZ-MOI.md`).
- **OCR** : lancer Tesseract avec `OMP_THREAD_LIMIT=1` et 4 pages à la fois
  (`xargs -P 4`) ; vingt en parallèle saturent la machine.
- **`rm` avec une variable** est bloqué par la sécurité : chemins littéraux, ou `"${dossier:?}"`.
- **Le pptx suit le PDF par la géométrie mesurée** : toute retouche d'espacement dans
  `systeme.css` (fiche, tableau, pied) se reporte à la main dans `scripts/pptx.mjs`, puis se
  vérifie en rendant le .pptx dans LibreOffice à côté du PDF.


## 9. Le catalogue caviste global (8–9 octobre) : ce qu'il faut savoir

C'est **le travail en cours**. Commande : `npm run global` (= `prix-global.py`, construction,
contrôle) ; sorties `dist/catalogue-caviste-2026-ecran.pdf` et `-imprimeur.pdf` ; aperçus dans
`epreuves/apercus/global/`. Le catalogue général « Sous nos pieds » (`npm run build`) reste à
refaire **seulement quand une photo partagée change** (les deux éditions lisent les mêmes photos).

### D'où viennent les données
- **Base = le catalogue du Salon Privé** (l'agence l'a confirmé en renvoyant le PDF) : mêmes fiches,
  vins, prix et offres que `data/salon-prive-2026.json`, **plus** les domaines que l'agence a
  ajoutés. Les domaines de l'ancien catalogue général absents du salon (Divin No Low, Fabien
  Castaing…) **ne sont pas repris**.
- **Tout passe par `scripts/prix-global.py`** → `data/catalogue-global-2026.json` (lu par
  `editionSalon()` de `src/gabarits/pieces.mjs` quand `EDITION=global`). C'est **le seul endroit**
  où vivent les prix ajoutés, l'ordre des fiches (`ORDRE`), les régions (`REGIONS`), les domaines
  créés pour cette édition (`DOMAINES_AJOUTES` : n°41 Sardelles, n°42 Trichon Bugey, n°43 Mas des
  Restanques), les corrections de vins (`CORRECTIONS_VINS`), les notes de prix (`NOTES`), les
  départements (`DEPARTEMENTS`), les labels de tête retirés (`SANS_LABELS`), la phrase d'offre
  (`OFFRE_VOLUME`), la mention « catalogue complet » (`AVEC_CATALOGUE_COMPLET`) et les mentions
  légales du global. Pour retoucher : modifier ce script, puis `npm run global`.
- Sources rangées dans `sources/catalogue-global-2026/` : le gros scan (pages JPEG), le sommaire
  annoté, les tarifs annotés (Les Lys, La Gorce, Mas des Restanques, Trichon départ cave, BIB du
  Colombier). Relevé ligne à ligne : `data/catalogue-global-releve.md`.
- **Règles de lecture des tarifs annotés** : surligné = on prend ; barré = on retire ; une colonne
  non surlignée disparaît ; un millésime douteux (« 2022-23 ») → **le plus récent** ; pas de
  millésime sur le tarif → **aucun** (« — ») ; le prix d'un vin raturé mais marqué « ok » est bon.

### Ce que l'agence a décidé (à tenir)
- **Ordre = celui du sommaire.** Loire : Reverdy, **Sardelles**, Barbinière… ; **Beaujolais**
  (Nugues) entre Alsace et Bourgogne ; Bourgogne finit par **Nadine Ferrand** ; Rhône finit par
  Pasquiers, **Mas des Restanques**, **Trichon** ; puis **Bugey** (Trichon, vins surlignés en jaune,
  panachable avec Trichon Rhône) ; Bordeaux finit par l'Escarderie, **Château La Gorce**, **La
  Passion des Terroirs** ; Languedoc finit par **Les Lys**.
- **Plus de numéros** (ni stand, ni n° de tarif) : on ne parle que de pages. **Numéros de page à
  gauche partout** (bas de page, sommaire, index, ouvertures), gros et violets.
- **Couverture** = celle du salon, titre « **Catalogue caviste** / Vins & Terroirs », cartouche :
  « Tarif valable jusqu'au 31 décembre 2026 » / « Offres valables du 5 octobre au 14 novembre 2026 ».
- **Jamais de nombre de références** (page 2, ouvertures, fiches, index).
- **Pas de page « produits à part »** : BIB, jus, etc. sont dans l'index des vins.
- **Offre au volume** : toujours « Offre possible en fonction du nombre de cols et de la
  référence. » L'offre vient **avant** la note de prix. Deux notes de prix seulement (« hors frais
  de transport » / « franco de port »), sauf Mas des Restanques (« franco de port à partir de 96 bts »).
- **« Possibilité sur demande d'avoir le catalogue complet. »** : Goichot, Cray, Guignottes, Passion
  des Terroirs.
- **La Passion des Terroirs** : le picto Bio / HVE **sur chaque ligne** (pas en tête de fiche).
- **Mentions légales** (dernière page), dans cet ordre : millésimes qui évoluent, vente sous réserve
  des stocks, photos non contractuelles, sauf erreurs typographiques, puis le reste ; ensuite une
  ligne **© Agence SCIO, reproduction interdite**.
- **Photos** : des **visages** plutôt que des logos. Banque d'images : **l'ancien catalogue
  « Tarif septembre 2026 »** (`sources/ancien-catalogue/`, on n'en prend **que les images**), le
  **Drive** de l'agence, puis **les sites officiels** des domaines. Une photo petite mais voulue
  passe avec `plancher_ppi` dans `data/photos-locales.json` (signalée dans `QUESTIONS.md`). Les
  photos où le vigneron sent ou sert le vin sont acceptées par l'agence (« c'est un catalogue de vin »).
- Textes des nouveaux domaines écrits d'après leur site officiel, avec l'accord de l'agence
  (Sardelles, Mas des Restanques) : faits du site seulement, rien d'inventé.

### État au 9 octobre
- 64 pages, 41 fiches, 598 prix, **tous les contrôles au vert**, chaque page regardée en image.
- Questions encore ouvertes : `QUESTIONS.md`, point 32 (photos en basse définition à remplacer en HD
  si possible : Barbinière, Prieuré des Papes, Coyeux, Haut Marin, Exea ; Prieuré des Papes sans
  portrait).

### La suite possible
1. Ce que l'agence demandera en relisant (elle relit page par page, souvent par message vocal).
2. Le **.pptx pour Canva** de cette édition (pas encore fait : `scripts/pptx.mjs` ne connaît que
   général et salon ; il faudra `EDITION=global`, les lettrines, la couverture du global).
3. Photos HD pour les ronds signalés.
