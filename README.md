# Catalogue Agence SCIO — édition 2026

Tarifs cavistes Vendée (85). 40 domaines, 10 régions.
Construit depuis `data/catalogue.json`, qui est la **seule vérité** du projet.

## Où en est le projet

**Terminé.** Concept retenu : **« Sous nos pieds »**. **52 pages** (le maximum voulu par
l'agence), 210 × 260 mm ; le Salon Privé en fait 48.
Chaque fiche domaine porte **deux images** : un rond de 40 mm pour le vigneron ou le logo,
une bande de 24 × 62 mm pour la bouteille (un peu plus basse sur quatre fiches, voir « Le
catalogue, page par page »). **Les 80 sont posées.** Provenance et droits, image par image :
`credits.md`.

| Livrable | Où |
|---|---|
| **Fichier Canva** (52 diapositives, textes et tableaux modifiables) | `dist/catalogue-scio-2026-canva.pptx` |
| **Le même, ronds recadrables** : photos entières sous un masque rond qu'on fait glisser (à essayer dans Canva) | `dist/catalogue-scio-2026-canva-recadrable.pptx` |
| **Les polices à téléverser dans Canva**, avec leur mode d'emploi | `polices-canva/` |
| **Prompt pour faire poser les images par Cowork** | `PROMPT-COWORK.md` |
| Où sont les deux emplacements d'image, diapositive par diapositive | `docs/emplacements-images.md` |
| **Catalogue, version imprimeur** (fond perdu 3 mm, traits de coupe) | `dist/catalogue-scio-2026-imprimeur.pdf` |
| **Salon Privé du 5 octobre, version écran** (sans prix pour l'instant) | `dist/salon-prive-2026-ecran.pdf` |
| **Salon Privé, version imprimeur** | `dist/salon-prive-2026-imprimeur.pdf` |
| **Salon Privé, fichier Canva** | `dist/salon-prive-2026-canva.pptx` |
| **Salon Privé, liste des vins dégustés** (3 pages A4) | `dist/salon-prive-2026-liste-des-vins.pdf` |
| **Salon Privé, les prix à remplir** | `tableur/prix-salon-prive-2026.xlsx` |
| Aperçus PNG des pages | `epreuves/apercus/` |
| **Catalogue, version écran** (navigation cliquable, liens `tel:`, `mailto:`, site) | `dist/catalogue-scio-2026-ecran.pdf` |
| Données des 40 domaines, vérifiées | `data/catalogue.json` |
| **Tous les tableaux de prix dans un tableur**, à modifier puis réimporter | `tableur/tarifs-scio-2026.xlsx` |
| Épreuve de contrôle des tarifs | `epreuves/epreuve-tarifs.pdf` |
| Lecture du catalogue concurrent | `INSPIRATIONS.md` |
| Les trois directions et leurs maquettes | `CONCEPTS.md`, `concepts/*.png` |
| Questions encore ouvertes | `QUESTIONS.md` |
| Corrections et arbitrages | `data/corrections.md` |
| Crédits images, polices, pictogrammes | `credits.md` |
| Journal de bord | `JOURNAL.md` |
| Compétences de design | `.claude/skills/`, présentées dans `docs/skills-design.md` |

## Travailler le catalogue dans Canva

1. **Téléverser les six polices** de `polices-canva/` (voir `polices-canva/LISEZ-MOI.md`).
   Sans elles, Canva substitue les polices et les tableaux se déforment.
2. Dans Canva : **Créer un design → Importer un fichier**, et choisir
   `dist/catalogue-scio-2026-canva.pptx`.
3. Sur chaque fiche domaine, **deux formes au contour pointillé** attendent une image :
   le rond de 40 mm en haut à gauche, la bande de 24 × 62 mm à droite. Posez l'image
   par-dessus, puis supprimez la forme pointillée. Elles sont à la même place et à la même
   taille sur les quarante fiches : rien ne bouge autour.
4. **Les tableaux sont de vrais tableaux** : on clique dans une cellule et on tape.
   Les textes aussi.
5. **Deux versions du fichier.** `…-canva.pptx` pose des ronds déjà découpés : ils
   s'affichent partout à l'identique, mais on ne peut pas y déplacer la photo.
   `…-canva-recadrable.pptx` pose les 25 photos simples en entier sous un masque rond :
   dans PowerPoint, et dans Canva s'il garde ce recadrage à l'import, on recentre la photo
   en la faisant glisser. Les logos, les ronds à deux portraits et les ronds élargis (dont
   les n°10 et n°18, cadrés pour laisser un verre hors champ) restent figés. Si Canva
   rend les ronds carrés ou déformés à l'import, garder la première version.
6. **La lettrine** (première lettre du texte, Young Serif violette) est une **boîte de
   texte à part**, posée devant la première ligne et montant au-dessus d'elle : à l'import,
   Canva ramène chaque paragraphe à une seule police et une seule taille, et une lettrine
   écrite dans le texte n'y gardait que sa couleur. Dans le texte, quelques espaces
   insécables lui gardent sa place. Pour corriger le premier mot dans Canva, corrigez la
   lettre dans sa boîte et la suite dans le texte. Si vous déplacez le texte, sélectionnez
   les deux boîtes ensemble. Tant que Young Serif et Spectral ne sont pas téléversées,
   Canva dessine la lettrine dans une serif plus fine, qui rentre un peu dans la colonne ;
   une fois les polices téléversées, elle tombe au ras, comme dans le PDF. Sa taille, et le nombre de lignes qui sert à centrer le bloc,
   sont réglés domaine par domaine dans `src/gabarits/lettrines-pptx.json` par
   `python3 scripts/regler-lettrines.py`. Ce script rend le .pptx, compte les lignes, vérifie
   que la lettrine est sur la ligne de base de la première ligne, et réduit la lettrine
   (puis l'interligne) des seuls textes qui toucheraient leur tableau. À relancer si un
   texte de domaine ou le haut des fiches change (demande LibreOffice, `pip install pymupdf`
   et les polices de `polices-canva/` copiées dans `~/.local/share/fonts`). Chaque édition a
   son réglage : `EDITION=salon python3 scripts/regler-lettrines.py` écrit
   `src/gabarits/lettrines-pptx-salon.json`. Puis `npm run pptx` et `npm run pptx-salon`.

**Attention** : une fois le catalogue modifié dans Canva, Canva devient la nouvelle source.
Si un prix change après coup, corrigez-le d'abord dans `data/fiches/`, relancez
`npm run build`, et réimportez — sinon les deux versions divergent.

## Reconstruire

**Une seule commande reconstruit tout :**

```sh
npm install
npm run build        # données, PDF, contrôles, puis le .pptx et son contrôle
```

Les étapes séparément :

```sh
npm run donnees      # assemble data/catalogue.json puis le vérifie
npm run catalogue    # fabrique dist/*.pdf (pagination mesurée dans Chromium)
npm run controle     # débordements, corps, polices, prix, mentions obligatoires
npm run deco         # exporte en PNG les éléments dessinés, pour le .pptx
npm run pptx         # fabrique dist/*.pptx depuis le même plan, puis le contrôle
npm run epreuve      # régénère epreuves/epreuve-tarifs.pdf
npm run recadrages   # re-détecte les tableaux sur les rendus du PDF source
npm run polices      # recopie les polices OFL (woff2) depuis node_modules
npm run polices-ttf  # refabrique les .ttf de polices-canva/ et src/fonts/metriques.json
npm run concepts     # régénère les trois maquettes de l'étape 2
```

`npm run build` sort en erreur si un contrôle échoue : il est utilisable en intégration continue.

Outils supposés présents : `python3`, `node`, `poppler-utils` (`pdftoppm`, `pdftotext`,
`pdffonts`, `pdfinfo`), `unzip`, et `pip install pillow` pour les recadrages.
`npm run polices-ttf` demande en plus `pip install fonttools brotli` ; il n'est utile que
si les polices changent, car ses deux sorties sont versionnées.

## Mettre à jour un prix ou un millésime

1. Ouvrir la fiche du domaine : `data/fiches/NN.json` (NN = son numéro au sommaire, 01 à 40).
2. Modifier la valeur. **Les prix sont en centimes entiers** : `14,75 €` s'écrit `1475`.
   Il doit toujours y avoir **autant de prix que de paliers** dans le tableau.
3. `npm run build` — les scripts refusent de passer si quelque chose cloche, et le `.pptx`
   est refait avec la même pagination que les PDF.
4. `npm run epreuve` pour revoir le tableau d'origine face à la nouvelle version.

### Beaucoup de changements d'un coup : le tableur

`tableur/tarifs-scio-2026.xlsx` contient les 48 tableaux de prix des 40 domaines, à la suite,
présentés comme dans le catalogue (un bandeau par domaine, un bandeau violet par tableau avec
ses paliers), plus un sommaire cliquable et un mode d'emploi. Il s'ouvre dans Excel, Google
Sheets ou LibreOffice.

1. On modifie le tableur : prix, millésimes, cuvées, notes, intitulés de paliers, note de
   prix ; on ajoute un vin en insérant une ligne (colonne A vide), on en retire un en
   supprimant sa ligne. La colonne A (grise) ne se touche pas.
2. `npm run importer -- FICHIER.xlsx --essai` montre chaque changement (ancien prix → nouveau
   prix, ajouts, retraits) sans rien écrire. On relit.
3. `npm run importer -- FICHIER.xlsx` écrit les changements dans `data/fiches/` (seules les
   lignes modifiées bougent), puis `npm run build` refait et contrôle les PDF et le `.pptx`.
4. `npm run tableur` remet le tableur à jour pour la fois suivante.

Le tableur refuse ce qui casserait le catalogue (un prix illisible, plus de prix que de
paliers, un tableau ajouté ou retiré) et dit à quelle ligne. Il demande `pip install openpyxl`.

**Ne jamais écrire un prix ailleurs que dans `data/fiches/`.** Le tableur n'est qu'un moyen
de les modifier. Les gabarits ne font que lire,
et le contrôle vérifie que les 715 prix du JSON se retrouvent dans le texte des deux PDF
**et** dans celui des diapositives.

## Le Salon Privé du 5 octobre 2026

C'est une **édition** du même générateur, pas une copie : mêmes gabarits, mêmes styles,
mêmes fiches. `EDITION=salon` change trois choses :
- **ce qui entre** : les 31 fiches des 26 stands (`data/salon-prive-2026.json`, rapprochées
  d'après le plan des exposants, qui fait foi), et dans leurs tableaux **seulement les vins
  dégustés** (le dossier de référence de Mathéo, qui donne aussi les textes et les labels) ;
- **ce qu'on montre** : le numéro du stand et sa salle à la place du numéro du tarif, une
  couverture (date et lieu en haut) et une page de l'agence au nom du salon ;
- **les prix** : vides tant que l'agence ne les a pas donnés.

Le salon garde aussi les pages d'ouverture de région et l'index des domaines, que le
catalogue général n'a plus (options `ouvertures` et `indexDomaines` de `ED`,
`src/gabarits/pages.mjs`).

```sh
npm run salon        # PDF écran et imprimeur, contrôles, .pptx, liste des vins
```

### Ajouter les prix du salon

Les prix vivent dans `data/salon-prive-2026.json`, vin par vin (`prix_centimes`, en centimes,
`null` tant qu'il n'y en a pas). **Un prix unique ou les paliers du domaine : les deux marchent
sans toucher aux gabarits.**
- `"mode_prix": "paliers"` (par défaut) : le tableau garde les paliers du tarif du domaine ;
  chaque vin reçoit autant de prix que de paliers, par exemple `[1250, 1190, 1150]`.
- `"mode_prix": "unique"` : le tableau n'a plus qu'une colonne « Prix salon » ; chaque vin
  reçoit un prix, par exemple `[1250]`.
Le mode se règle pour tout le salon (en tête du fichier) ou stand par stand.

Le plus simple, par le tableur :
1. `npm run tableur-salon` écrit `tableur/prix-salon-prive-2026.xlsx` : une ligne par vin,
   rangée par stand, avec les intitulés de paliers du domaine rappelés en violet.
2. Pour chaque stand, remplir **soit** la colonne « Prix salon », **soit** les colonnes de
   paliers. Le mode du stand se déduit de ce qui est rempli ; un stand qui mêle les deux est
   refusé.
3. `npm run importer-salon -- FICHIER.xlsx --essai` montre chaque changement, sans rien
   écrire ; sans `--essai`, il l'écrit.
4. `npm run salon`. Le contrôle vérifie que chaque prix donné est dans le PDF et compte les
   cases encore vides.

### Refaire la liste des vins

La transcription du dossier de référence de Mathéo
(`sources/salon-prive-2026/matheo-dossier-reference.pdf`) et son rapprochement avec le tarif
sont dans `scripts/transcrire-matheo.py`, ligne par ligne, avec les écarts (QUESTIONS.md,
point 26). **Ce qui s'affiche d'un vin (cuvée, appellation, couleur, millésime) est ce que le
dossier écrit**, corrigé seulement dans la forme (liste `CORRECTIONS` du script) ; le tarif
donne la contenance et le tableau. Si une ligne change, on la corrige là, puis
`npm run transcrire-matheo` (les prix déjà saisis sont gardés) et `npm run salon`.

Les textes et les labels du dossier sont dans `scripts/textes-matheo.py` : il les reporte
sur les fiches (`data/fiches/NN.json`, le texte du tarif restant dans `texte_tarif`), dans
les deux éditions. Ensuite `npm run build` et `npm run salon`.

La liste des vins dégustés (`npm run liste-vins`) sort en A4 pour une impression au bureau ;
`LISTE_FORMAT=catalogue npm run liste-vins` la sort au format du catalogue (210 × 260 mm).

## Poser les images des domaines

Les images se posent **dans la source**, jamais dans le `.pptx` : `npm run build` les fait
entrer d'un coup dans les deux PDF et dans le `.pptx`, et un changement de prix ne les perd pas.

1. Copier les deux arborescences de l'agence dans `src/photos/brut/` (ignoré par git :
   les originaux restent en local) : `Bouteilles_de_vin/<Domaine>/` et
   `Domaines_et_vignerons/<Domaine>/`. **Le nom du dossier est le nom du domaine.**
2. `python3 scripts/preparer-photos.py --inventaire` liste les dossiers, propose un
   appariement avec les 40 domaines et fait une planche de contact par dossier
   (`build/planches/`). C'est une proposition : **on la valide à l'œil.**
3. Écrire la table validée dans `data/photos-locales.json` (format décrit en tête du fichier).
4. `npm run photos` prépare les images retenues (traitement unique, rond de 40 mm, bouteille
   détourée dans 24 × 62 mm, 300 ppi visés, jamais agrandies, refus sous 200 ppi), puis
   `npm run build`. `python3 scripts/preparer-photos.py --seulement 18` ne retraite que les
   images d'un domaine (ou de plusieurs : `--seulement 18 21`) et garde les autres ;
   `--seulement 2 3 --role bouteille` ne refait que les bouteilles, les ronds restent.

Un domaine sans image garde ses deux emplacements pointillés. Les images écartées, et
pourquoi, sont dans `data/photos-ecartees.json`. `npm run photos` réécrit aussi les tables
d'images de `credits.md`.

**Trois provenances**, dans cet ordre de priorité, toutes écrites dans `data/photos-locales.json` :

- **les dossiers de l'agence**, copiés dans `src/photos/brut/` (voir plus haut) ;
- **les sites officiels des domaines** : l'entrée garde l'adresse de l'image (`url`) et de la
  page (`page`). Si l'original manque dans `src/photos/brut/`, `npm run photos` le
  retélécharge tout seul. `python3 scripts/moissonner.py 13 14` recueille les images des sites
  listés dans `data/sites-domaines.json`, à trier à l'œil ;
- **le Canva de l'agence** (« Tarif septembre 2026 ») : exporter le design en PDF qualité
  « pro », puis `python3 scripts/extraire-canva.py export.pdf` range ses images dans
  `src/photos/brut/canva/dNN-pPP-XXX.png` (NN = domaine, PP = page du Canva).

Options d'une entrée de la table : `zone` (isoler une bouteille dans une photo de gamme),
`centre` (déplacer le carré d'un portrait), `cadre` (reculer pour faire tenir plusieurs
têtes entières dans le rond), `diptyque` (deux portraits séparés, une moitié chacun),
`mode: contenir` (un logo, jamais rogné), `forme: rond` (un logo déjà rond), `fond` (couleur
de réserve imposée sous un logo), `tolerances` (resserrer le détourage d'une bouteille au
bouchon blanc sur fond blanc), `ombre: couper` (retirer l'ombre translucide d'un PNG déjà
détouré), `detourage: modele` (une bouteille photographiée devant un
décor : détourage par le modèle de segmentation de `rembg`, à installer une fois avec
`pip install rembg onnxruntime` ; le modèle, 180 Mo, se télécharge au premier usage).

## Ajouter ou retirer un domaine

Ajouter `data/fiches/NN.json` sur le modèle des existants, puis ajuster le relevé d'effectifs
en tête de `scripts/verifier-donnees` (`ATTENDU`), qui est volontairement codé en dur : il
sert de garde-fou contre une perte silencieuse de domaine.

## Le catalogue, page par page

| Pages | Contenu |
|---|---|
| 1 | Couverture |
| 2 | L'agence, ses contacts |
| 3 | **Sommaire** : une liste par région, les domaines numérotés avec leur page, et la légende complète des pictos (types de vin, labels) |
| 4 – 47 | Les quarante domaines, région par région (le sommaire et la tranche colorée disent la région) |
| 48 – 50 | Index des vins par type, de A à Z |
| 51 | Les produits à part : bag-in-box, sans alcool, jus de cépages, bières, armagnacs, ratafias |
| 52 | Contacts, lexique, mentions légales, crédits, message sanitaire |

*(La pagination est recalculée à chaque fabrication ; `build/catalogue-scio-2026-plan.json`
donne la page de chaque domaine. Quand il le faut, des pages « Vos notes » et la planche en
coupe complètent le catalogue jusqu'à un multiple de 4 ; avec 52 pages, il n'en faut aucune.)*

**Un domaine, une page**, sauf les quatre tarifs les plus longs (n°12, 23, 25, 32), sur deux.
Quand une fiche déborde de peu, la bande du haut s'abaisse (62, 56, 50, 46 ou 44 mm) : la
bouteille rapetisse dans ses proportions, le rond garde sa taille, la colonne de texte
s'élargit. La pagination garde la plus haute bande qui donne le moins de pages (`BANDES` dans
`src/gabarits/pieces.mjs`) ; aujourd'hui n°6, 8, 10 et 24. Les lignes de tableau font 8,6 mm :
l'écriture est grande (cuvée 9,6 pt, prix 10 pt), l'interligne serré.

Sur chaque fiche, **la note de prix** (« * Prix de la bouteille H.T. hors frais de
transport. », « franco de port », « départ chai »…) vient **juste sous le dernier tableau**,
en 10,5 pt, avec un filet violet : c'est ce que le prix comprend. Les départements de
distribution restent en pied de fiche.

Les **labels** affichés sont ceux de la liste des vignerons du Salon Privé pour les 31
fiches présentes au salon (décision de l'agence du 2 octobre 2026), ceux du tarif pour les
9 autres. Les labels du tarif restent dans `labels_tarif` de chaque fiche ;
`python3 scripts/reporter-labels.py` refait le report.

## Arborescence

```
sources/       notre PDF et notre logo (lecture seule)
reference/     catalogue concurrent (inspiration design, lecture seule)
docs/          pièges du PDF, notes sur le concurrent, présentation des compétences
data/          catalogue.json, fiches/, corrections.md, pages/ (rendus 200 dpi), recadrages/
concepts/      les trois pistes (HTML, PDF, PNG)
src/           concepts/, styles/, gabarits/, images/, fonts/ (polices OFL + métriques), photos/
scripts/       assemblage, vérifications, recadrages, épreuve, maquettes, déco, pptx
polices-canva/ les .ttf à téléverser dans Canva, et leur mode d'emploi
epreuves/      épreuve de contrôle des tarifs
dist/          les deux PDF et le .pptx
archive-v1/    travail d'une session précédente, conduite sous un autre cahier des charges
```
