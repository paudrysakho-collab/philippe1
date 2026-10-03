# Reprise : où en est le projet (3 octobre 2026)

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
| **Salon Privé Vins & Terroirs**, lundi 5 octobre 2026, Château de la Rairie | `salon-prive-2026-ecran.pdf`, `-imprimeur.pdf`, `-canva.pptx` | **48 pages**, 26 stands, 31 fiches, 180 vins, **prix vides** |
| **Liste des vins dégustés** | `salon-prive-2026-liste-des-vins.pdf` | 3 pages A4 |
| Tableurs (aller-retour des prix) | `tableur/tarifs-scio-2026.xlsx`, `tableur/prix-salon-prive-2026.xlsx` | à jour |
| Aperçus PNG | `epreuves/apercus/` (planches et pages détaillées des trois livrables) | à jour |

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
  réappliquer. S'il change encore, comparer d'abord au pixel avec la version en place (méthode
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

## 7. La suite : ta mission, c'est **mettre les prix**

La mission principale (l'agence, 3 octobre) : **remettre les prix**. Des tâches annexes
peuvent venir s'y ajouter. Ne touche à rien d'autre de toi-même ; si l'agence le demande :
- **une retouche de page** : charge d'abord les compétences `da-scio` (et `tableau-tarif`
  pour un tableau), refais `npm run build` et `npm run salon`, regarde les pages touchées en
  image (`epreuve-pages`), tiens les 52 pages au plus ;
- **un texte de domaine ou le haut d'une fiche** change : relance aussi
  `regler-lettrines.py` (section 3) ;
- **une photo** : relis d'abord le « piège des photos » (section 3) et `photos-domaines` ;
- **un fait** (texte, label, vin) : seulement depuis les sources de la section 4, sinon
  `QUESTIONS.md` ;
- **`CLAUDE.md`** : la proposition du 2 octobre attend son feu vert (fin de section).
Chaque décision nouvelle de l'agence va dans `JOURNAL.md` et, si elle dure, dans les
sections 4 et 5 de ce fichier.

- **Prix du Salon Privé** (cases vides aujourd'hui) : l'agence remplit
  `tableur/prix-salon-prive-2026.xlsx` (une ligne par vin, rangée par stand). Pour chaque
  stand, **soit** la colonne « Prix salon » (prix unique), **soit** les colonnes de paliers.
  Puis `npm run importer-salon -- FICHIER.xlsx --essai` (montre chaque changement), sans
  `--essai` pour écrire, et `npm run salon`. Détail : README, « Ajouter les prix du salon ».
- **Un prix du catalogue général** change : `npm run tableur`, l'agence corrige
  `tableur/tarifs-scio-2026.xlsx`, `npm run importer -- FICHIER.xlsx --essai`, puis sans
  `--essai`, et `npm run build`.
- Les prix vivent dans les données, **en centimes**, jamais tapés dans un gabarit. Un prix
  qui paraît faux ne se corrige pas : il se signale (`QUESTIONS.md`).
- Après : contrôles au vert (chaque prix donné se retrouve dans le PDF), un coup d'œil en
  image aux fiches touchées, commit, push, et envoyer à l'agence les PDF et .pptx refaits.
  Les lettrines ne bougent pas : inutile de relancer `regler-lettrines.py`.

En attente de l'agence : la mise au point de `CLAUDE.md` (garder `CLAUDE.md` court, avec
l'ordre des sources de la section 4 et les consignes de la section 5 ; ce fichier reste
« état et reprise ») et les questions de la section 6.

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
