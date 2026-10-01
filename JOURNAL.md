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


## Les photos des domaines

**Demande :** deux images par domaine — une ronde (logo ou personne) et une bouteille.

### Ce que j'ai fait

**Trouver les sites.** Sonder 408 URL candidates construites à partir des noms, puis vérifier
chaque réponse sur le titre de sa page d'accueil, puis compléter par recherche. **La
vérification était indispensable** : `domaineducolombier.com` est un hôtel de la Drôme,
`domainelys.fr` un château-hôtel de Loire-Atlantique, `papes.fr` un site sur la papauté.
Attribuer leur photo à nos domaines aurait été une faute grave dans un document commercial.
**29 sites retenus, 19 exploitables.**

**Moissonner.** Chromium ne faisait pas confiance au certificat du proxy sortant
(`ERR_CERT_AUTHORITY_INVALID`) et l'installation de l'autorité dans le magasin NSS n'a jamais
abouti — elle a été arrêtée au bout de son délai. **Contourné en passant la collecte en curl**,
qui lit le proxy sans problème : page d'accueil plus sept pages internes par site,
images, `srcset` (plus grande variante annoncée), `og:image` et fonds CSS. ~700 images.

**Choisir à l'œil.** Une planche de contact par domaine, regardée une par une. C'est là que
se trient les photos de mariage, les visuels de promotion, les photos de banque d'images
glissées dans un gabarit — et surtout **les images interdites par la loi Évin** : verres levés,
scènes de dégustation, trinquages. Il y en avait sur presque tous les sites.

### Essayé, raté, corrigé

- **Les logos sortaient rognés.** Un logo ne se recadre pas : il entre en entier. Mode
  « contenir » ajouté, sur une réserve de la couleur de son propre bord.
- **Les bouteilles de blanc disparaissaient.** Un seuil sur l'écart au fond effaçait le corps
  de la bouteille, presque aussi clair que le blanc derrière. Remplacé par un **remplissage
  depuis les bords** : seul le fond *atteint depuis l'extérieur* est retiré, et la tolérance
  se resserre automatiquement si le résultat garde trop peu de matière.
- **Un logo PNG clair devenait invisible** une fois aplati sur du crème. L'aplatissement
  choisit désormais son fond selon la clarté du logo.
- **Deux images écartées après coup** : un portrait d'époque qui ressortait délavé (remplacé),
  une bouteille de blanc sur blanc que le détourage mangeait quand même (retirée).

### Le résultat

**30 images sur 19 domaines**, dont **11 avec les deux images demandées**.
Le rond est **cerclé d'un anneau du sol de sa région** : la photo entre dans le concept au lieu
de s'y poser. La bouteille est **détourée**, sans cadre — aucun carré blanc sur le papier.
Les 30 passent par **la même fonction de traitement**, pour qu'elles sortent d'une même main.

Le catalogue passe de 68 à **72 pages**, toujours multiple de 4, tous contrôles au vert.

---

## Les emplacements réservés et le fichier Canva

L'agence préfère poser elle-même les ronds de vigneron et les bouteilles, dans Canva, où elle
pourra aussi corriger un texte. Deux conséquences.

### 1. Les images sortent, les emplacements restent

Les 30 photos sont retirées de la maquette. À leur place, sur les quarante fiches, **deux
formes vides au contour pointillé** : le rond de 32 mm en haut à gauche, la bande de
24 × 62 mm à droite, aux mêmes coordonnées partout. Une image s'y pose sans rien déplacer.

Le travail sur les photos n'est pas perdu : les fichiers préparés restent dans `src/photos/`
et `credits.md` garde les 30 lignes — domaine, sujet, site officiel, URL exacte, résolution,
statut d'autorisation. C'est le dossier à ouvrir au moment de remplir les emplacements.

La ligne « Crédits » de la dernière page le dit maintenant explicitement : le catalogue est
livré avec ses emplacements vides, les photos qui y seront posées restent à créditer.

### 2. Le .pptx n'est pas une capture, c'est le même plan

`scripts/pptx.mjs` ne redessine rien et ne re-paginie rien : il lit **le même
`build/plan.json`** que les PDF, un descripteur par page, et **les mêmes hauteurs mesurées**
dans `build/mesures.json`. Les tableaux sont de vrais tableaux PowerPoint (donc modifiables
dans Canva), les textes de vrais blocs de texte, les dessins des PNG à 300 ppi exportés par
`scripts/deco.mjs` depuis le HTML du catalogue. Les 715 prix viennent du JSON comme ailleurs.

Un second contrôle, `scripts/controler-pptx.mjs`, relit le texte des 76 diapositives dans le
XML du fichier : autant de diapositives que de pages, les 715 prix retrouvés, les 40 domaines
nommés, les contacts et le message sanitaire présents, aucune diapositive vide, moins de 50 Mo.
`npm run build` enchaîne maintenant données → PDF → contrôle → .pptx → contrôle.

### Essayé, raté, corrigé

- **Les hauteurs de tableau étaient estimées** (`9 + n × 7,2 mm`). Dans LibreOffice, les
  rangées font en réalité 10,7 mm quand l'appellation et la cuvée tiennent sur deux lignes :
  sur les fiches à plusieurs tableaux (Haut Marin, Fabien Castaing), l'en-tête du second
  tableau **recouvrait la dernière ligne du premier**. Remplacé par les hauteurs mesurées
  dans Chromium, ligne par ligne, passées en `rowH`. Plus aucune estimation.
- **Les titres longs passaient à la ligne** et le filet violet barrait le second rang
  (« Domaine du Colombier / J.Y Bretaudeau »). Plutôt que de descendre tout le contenu —
  ce qui aurait décalé une pagination calculée au millimètre — le corps du titre **se réduit
  juste assez pour tenir sur une ligne**, jamais sous 15 pt, et le « (suite) » repasse en
  italique 11 pt comme dans le PDF. Dix titres concernés, le plus serré descend à 17 pt.
- **Pour cela, il fallait savoir mesurer une chaîne hors du navigateur.** `scripts/metriques.py`
  relève les chasses des polices livrées dans `src/fonts/metriques.json` (versionné) ; le
  générateur calcule largeurs et retours à la ligne avec les vraies métriques. Les jetons
  (Bio, Allocation, Panachage…) y ont gagné aussi : leur largeur était estimée au nombre de
  caractères, elle est maintenant juste.
- **Trois planches identiques en fin de catalogue.** Les pages de calage vers le multiple de 4
  répétaient la même coupe pleine page — ça se lisait comme une erreur d'impression. Elles
  deviennent **deux pages « Vos notes » réglées** (un caviste commande en lisant), la coupe
  restant une seule fois, juste avant la page finale.
- **La légende de la planche était rognée** par le bas de page, en blanc sur la bande claire
  de Champagne. Elle remonte de 18 mm, dans la strate sombre.
- **Les deux sorties avaient divergé sur la page 3.** Le .pptx expliquait les emplacements
  d'image là où le PDF expliquait les pictogrammes. C'est le PDF qui avait raison : une fois
  les images posées, un encart décrivant des cases vides n'a plus de sens. Les six blocs du
  mode d'emploi, leurs textes et leurs six vignettes sont désormais **une seule source**
  (`figuresModeEmploi`, `BLOCS_MODE_EMPLOI`), lue par le HTML et par le .pptx.
- **Un sélecteur trop resserré a vidé les capsules** des dix ouvertures de région dans le
  .pptx, le temps d'une fabrication : en passant `.bloc svg` à `.bloc > svg` pour corriger
  une vignette, j'ai cessé d'atteindre le dessin imbriqué du sol. Vu au rendu, corrigé.
- **LibreOffice refusait d'ouvrir le fichier** (« source file could not be loaded ») : le
  paquet `libreoffice-impress` manquait sur la machine. Ce n'était pas le .pptx — un fichier
  d'essai de deux lignes échouait pareil.

- **Le fichier s'ouvrait dans un lecteur vidéo.** pptxgenjs écrit l'archive en commençant par
  des entrées de dossier et laisse `[Content_Types].xml` en 19ᵉ position. PowerPoint,
  LibreOffice et Canva s'en accommodent, mais Windows, macOS et les navigateurs identifient un
  fichier en lisant son **premier** élément : `file` répondait « Zip archive data » au lieu de
  « Microsoft PowerPoint 2007+ », et le système confiait le fichier au premier lecteur venu.
  `scripts/ranger-pptx.py` réécrit l'archive avec la carte d'identité en tête, non compressée,
  et sans entrées de dossier — comme le fait PowerPoint. Le contrôle le vérifie désormais.
  Effet de bord bienvenu : pptxgenjs stockait les images sans compression, le fichier passe de
  **13,3 à 6,0 Mo**.

### Les polices

Canva ne connaît ni Young Serif, ni Spectral, ni IBM Plex Sans : sans elles, il substitue et
les tableaux se déforment. `polices-canva/` contient les six `.ttf` à téléverser, avec leur
mode d'emploi et leurs licences (OFL, usage commercial autorisé). Ils sont fabriqués par
`npm run polices-ttf` à partir des paquets `@fontsource`, en **réunissant les sous-jeux latin
et latin-ext** (le sous-jeu `latin-ext` seul n'a ni « é », ni « € », ni « œ ») et en déclarant
les graisses SemiBold comme le **gras** de leur famille, pour que le bouton gras de Canva
tombe sur le vrai dessin et non sur un faux gras.

### Ce qui reste vrai

76 pages, multiple de 4. Tous les contrôles au vert des deux côtés, les 715 prix retrouvés
dans le texte des deux PDF **et** des 76 diapositives.

---

## Le vide sous les textes courts, et une seconde source

### Le trou blanc avant le tableau

L'agence a montré du doigt le vide entre la fin du texte de présentation et le tableau de
prix, en proposant une maquette où tout est plus gros. Le vide est structurel : la bande du
haut fait toujours la hauteur de l'emplacement bouteille (62 mm), alors qu'un texte médian
de 285 caractères n'occupe que 25 mm au corps de base. Trente-quatre millimètres de rien.

Trois pistes essayées, regardées côte à côte sur une fiche courte et sur la plus longue :

- **rond agrandi seul** : le rond prend sa place mais le texte flotte toujours ;
- **texte agrandi seul** : le texte remplit, mais le rond de 32 mm paraît perdu à côté ;
- **les deux** : c'est la bonne.

Retenu : **le rond passe de 32 à 40 mm** (même taille sur les quarante fiches, l'agence pose
ses images sans que rien ne bouge), **le corps du texte s'ajuste entre 9,5 et 13 pt** pour
remplir la bande, et **le texte se centre verticalement** pour que le peu d'air qui reste se
partage au lieu de tomber en bas. Vingt-cinq fiches arrivent au plafond de 13 pt, les deux
textes les plus longs (n°16 Prieuré des Papes, n°17 Coyeux) restent à 9,5 pt et font grandir
leur bande — la pagination mesurée s'en occupe toute seule.

`corpsDomaine()` vit dans `pieces.mjs` et sert au PDF comme au .pptx : une seule règle, deux
sorties. Pas d'estimation : le calcul se fait sur les chasses réelles des polices livrées.

### La liste du salon : une confirmation, un texte, quatorze questions

L'agence a fourni deux documents du Salon Privé du 5 octobre 2026. Le premier, la liste des
domaines, ne contient que des noms et des numéros de stand — aucun texte, contrairement à ce
qu'elle pensait. Le second, la liste des vignerons, contient bien 26 notices.

Comparaison notice par notice avec nos 40 fiches :

- **20 des 21 textes communs sont identiques au mot près** une fois ôtées les phrases propres
  au salon (« Vins sous allocation. », « Format BIB disponible. »…), que le catalogue porte
  déjà en jetons et en tableaux. C'est une vérification indépendante de la transcription.
- **n°1 François Reverdy**, le seul domaine sans présentation dans le tarif, en a une ici.
  Reprise telle quelle, avec un champ `texte_provenance` qui dit d'où elle vient ;
  `verifier-donnees` refuse désormais un texte sur ce domaine s'il n'est pas sourcé.
- **n°21 Trichon** : la liste du salon ajoute « associés dans le projet ». Non repris.
- **Quatorze labels divergent** entre les deux documents — n°4 Domaine des Noëls est Bio dans
  le tarif et HVE au salon, les deux ne peuvent pas être vrais. **Rien n'a été changé** : le
  catalogue affiche les labels du tarif. Une mention de certification engage l'agence, elle
  ne se décide pas sans elle. Table complète dans `QUESTIONS.md`, point 22.
