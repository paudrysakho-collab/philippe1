# Journal de bord

## 1er octobre — Remise à plat du dépôt

Le dépôt contenait le travail d'une session précédente, conduite sous un **autre cahier des
charges** : un `CAHIER-DES-CHARGES.md` client, un fichier Excel de tarifs, une maquette de
52 pages et un audit. Le brief de `CLAUDE.md` désigne `sources/tarif-septembre-2026.pdf`
comme **seule source des faits** et ne mentionne aucun de ces fichiers.

**Décision.** J'ai installé l'arborescence du brief et déplacé tout l'ancien dans
`archive-v1/` plutôt que de le supprimer : rien n'est perdu, l'historique git non plus.
J'ai **reparti de zéro sur les données**, sans réutiliser l'ancien `catalogue.json`, parce
qu'il mélangeait des prix venus de l'Excel et de la maquette — deux sources que le nouveau
brief n'autorise pas.

**Ce que ça coûte :** une transcription complète refaite. **Ce que ça évite :** un catalogue
dont on ne saurait plus dire d'où vient chaque prix.

*→ Si l'Excel et la maquette sont en réalité des sources légitimes que l'agence veut voir
prises en compte, c'est une question ouverte, posée dans le résumé de fin.*

## Étape 1 — Extraction

- 44 pages rendues en PNG à **200 dpi** (`data/pages/`), couche texte extraite avec
  `pdftotext -layout`, découpée par page (`data/texte/`).
- **Les tableaux de prix sont des images** : la couche texte ne contient aucun prix. Tout a
  été transcrit **à l'œil, page par page**, depuis les rendus.
- Les lettrines sont extraites séparément par `pdftotext` (« Q uatre », « E n 1976 ») : chaque
  début de texte a été recollé puis **vérifié sur l'image**.
- **p.15, Goichot** : la pastille rose de panachage recouvre une partie de la présentation.
  La couche texte livre le passage caché (« cuverie d'élevage de pointe inaugurée en 2020 »),
  rétabli dans les données.

**Essayé et rejeté.** J'ai d'abord envisagé de reprendre l'ancien `catalogue.json` et de le
vérifier ligne à ligne contre les images. Rejeté : une vérification est plus facile à biaiser
qu'une transcription — on valide ce qu'on lit au lieu de lire ce qui est écrit.

### Résultat

**40 domaines · 49 tableaux · 371 lignes · 733 prix.**
Une fiche JSON par domaine (`data/fiches/NN.json`), assemblée par `scripts/assembler.py`.

### Seconde passe

`scripts/recadrer-tableaux.py` détecte les tableaux sur les rendus **par leurs aplats de
couleur** (bandeau doré, lignes roses, lignes grises, en-tête magenta) et les recadre.

**Essayé et rejeté.** Premier jet : tout bandeau coloré était pris pour un tableau — les
pastilles « ALLOCATION ! » et les encarts de panachage remontaient aussi. Corrigé en exigeant
la présence du **bandeau doré**, que seuls les vrais tableaux portent. 47 recadrages pour
49 tableaux : deux tableaux sont contigus à leur voisin (Blacailloux, Frézier) et partagent
leur recadrage.

Les tableaux les plus denses ont été **relus un par un sur leur recadrage** : n°12 Goichot
(23 lignes), n°25 La Passion des Terroirs (31 lignes), n°8 Boehler (15), n°32 Exea (18).
Aucun écart.

### Contrôles

`scripts/verifier-donnees` vérifie : 40 domaines numérotés 1 à 40, effectifs par région
conformes au relevé manuel, domaine *n* en page *n+3*, régions groupées, autant de prix que
de paliers, centimes entiers et positifs, appellations non vides, départements au bon format
et triés, allocations et groupes de panachage conformes au relevé.

**Il sort au vert**, avec exactement les deux avertissements attendus : les dégressivités
inversées de Verchères et de la Pousterle, **signalées, non corrigées**.

**Corrigé en route.** Le contrôle de dégressivité prenait les BIB du Colombier pour des
anomalies : 5 L et 10 L ne sont pas des quantités, le prix y monte légitimement avec le
volume. Le contrôle ignore désormais les paliers qui désignent un contenant.

### Épreuve

`epreuves/epreuve-tarifs.pdf` — pour chaque domaine, **le tableau d'origine recadré à gauche,
la version recomposée depuis le JSON à droite**. 40 pages en 420 × 297 mm. C'est la pièce
qui permet à un humain de valider les prix sans ouvrir le PDF source.

## Étape 2 — Concepts

Les 38 pages du catalogue concurrent ont été regardées. `INSPIRATIONS.md` dit ce que j'en
garde (une identité tenue de bout en bout, un sommaire lisible d'un coup d'œil, une ligne
d'identité sous le nom du domaine, un bloc de prix détaché) et **comment je le transforme**
pour qu'on ne puisse jamais confondre les deux catalogues.

`CONCEPTS.md` propose trois directions. Chacune naît d'une matière déjà présente dans le PDF :
les **noms de sols** dans les cuvées ; les **noms de ciel et de musique** ; la **mention
« possibilité de panacher »**, la plus répétée du document.

**Relu et changé.** Le premier jet du Concept 2 posait un fond quasi noir avec une couleur
acide — exactement le tic que le brief interdit. Changé pour un **indigo franc** (`#232B52`)
et **quatre couleurs chaudes**, avec les pages de domaine sur fond clair pour que les tableaux
restent lisibles à l'impression.

**Essayé et rejeté.** Un quatrième concept « almanach » (saisons, phases de lune, calendrier) :
abandonné parce qu'il aurait suggéré des pratiques biodynamiques que la source n'affirme pas
pour la plupart des domaines. Le brief interdit d'ajouter un fait ; il interdit aussi de
l'insinuer par la mise en page.

Trois planches de 420 × 260 mm maquettées — **couverture + fiche du domaine n°26 Château la
Gorce** pour les trois, avec son vrai texte, ses 11 lignes et ses 3 paliers. Illustrations
dessinées en SVG dans le dépôt, génératives à graine fixe. Polices OFL copiées dans
`src/fonts/`, **toutes incorporées** (vérifié à `pdffonts`).

## Point d'arrêt — les arbitrages de l'agence

| Question | Réponse |
|---|---|
| Concept | **1 — Sous nos pieds** |
| Excel et maquette de la session précédente | **à ignorer**, le PDF fait seul foi |
| Tableau de champagnes du Colombier | **retiré** de la fiche n°3 (copier-coller de la n°40) |
| Photos | « un peu de tout » : sites des domaines, libres de droits, et fichiers de l'agence |

## Étape 3 — Le système

`src/styles/systeme.css` tient les variables (sept couleurs de terre plus le violet et l'or
de l'agence, trois typographies, la grille, le fond perdu) ; `src/styles/pages.css` tient les
gabarits ; `src/gabarits/pieces.mjs` tient les pièces dessinées.

**Décision tranchée : comment cohabitent le rêve et les prix.**
Dans `CONCEPTS.md` je recommandais un **cahier de tarifs détachable**. **Je ne l'ai pas fait**,
et voici pourquoi. Le brief impose qu'un caviste trouve en cinq secondes le domaine, le vin,
le prix et le palier. Un cahier séparé l'oblige à feuilleter entre l'histoire et le tarif :
il gagne une réimpression par an et perd l'essentiel. La maquette que vous avez validée
montrait d'ailleurs le texte et le tableau sur la même page.

La réponse retenue sépare donc **par zone, pas par page** :

- **le rêve occupe les ouvertures de région** (pleine page, à fond perdu, le sol de la région
  en carotte verticale) **et le haut de chaque fiche** (la coupe du sol du domaine, son texte) ;
- **le prix occupe une zone basse continue**, toujours de la même largeur (bloc de 52 mm)
  et toujours au même endroit sur les quarante fiches.

Ce qui change chaque saison est donc **un seul composant, alimenté par un seul fichier**.
Et le cahier détachable reste possible sans rien redessiner : il suffirait de changer
l'assemblage dans `scripts/construire.mjs`, pas la maquette.

## Étape 4 — La production

**La pagination est mesurée, pas estimée.** Une première passe charge toutes les fiches dans
Chromium et relève la hauteur réelle de chaque en-tête, de chaque ligne de tableau et de
chaque pied. La découpe se fait ensuite sur ces millimètres.

**Corrigé en route, et c'était un vrai bug.** Les premiers blocs étaient mesurés 11 mm trop
courts : les marges des enfants *sortaient* de la boîte mesurée (fusion des marges). Résultat,
l'encart de panachage de la Maison Goichot chevauchait la dernière ligne de son tableau.
`display: flow-root` sur les témoins de mesure a réglé le problème. Une marge de sécurité de
2 mm a été ajoutée : on ne remplit jamais au millimètre.

**Équilibrage.** Une fiche qui tient sur deux pages rabote son budget page par page jusqu'à ce
que les deux soient également remplies. Le Domaine Boehler passait de 11 + 4 lignes à 8 + 7.

**Règles de coupe.** Jamais une ligne seule sous un en-tête de tableau ; jamais une dernière
ligne orpheline sur la page suivante.

## Étape 5 — Le contrôle

`scripts/controler.mjs` fait ce qu'une machine fait mieux que l'œil : débordements hors cadre
mesurés dans Chromium, planchers de corps, pages multiples de 4, format et fond perdu,
polices incorporées, poids des fichiers, et **les 715 prix du JSON retrouvés un par un dans
le texte du PDF**.

**La découverte de l'étape.** Mon propre catalogue reproduisait le défaut que je reprochais au
PDF source : l'**interlettrage cassait la couche texte**. « BORDEAUX » sortait en
« BORD E AU X », introuvable au Ctrl+F. J'ai mesuré le seuil — à 8 pt, au-delà de **0,03 em**,
Chromium insère des espaces parasites — et bridé tout le catalogue à cette valeur, désormais
tenue par une variable (`--interlettre`) et vérifiée automatiquement.

**Ce que le regard a trouvé, et que la machine ne voyait pas.** La planche de contact des
68 pages a montré que le bandeau de sol, posé en bas des fiches courtes, **était devenu du
papier peint** : le même dégradé de quatre couleurs sur presque toutes les pages. Il est
désormais **monochrome, teinté par la région** — bleu en Loire, ocre en Bourgogne, rouge en
Bordeaux — plafonné à 40 mm sur les pages denses, et la craie de Champagne, trop claire pour
teinter un fond crème, bascule sur le silex.

**Les trois pages de bourrage** (pour atteindre un multiple de 4) sont devenues utiles :
*les produits à part* (bag-in-box, sans alcool, jus de cépages, bières, armagnacs et ratafias,
que le brief veut bien visibles), *l'index des quarante domaines de A à Z*, et une planche
pleine page de la coupe.

## Étape 6 — La livraison

Deux PDF dans `dist/`, un contrôle qui passe au vert, et les questions encore ouvertes
dans `QUESTIONS.md`.
