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

### Les images des fiches : 77 sur 80, puis 79

L'agence a validé la table de ses propres dossiers (29 images), puis demandé de remplir tout
le reste : chercher sur les sites des domaines, reprendre les 30 images repérées en 2026, et
puiser dans son Canva « Tarif septembre 2026 ». Règle de priorité retenue : dossier de
l'agence, puis site officiel, puis Canva ; une image validée par l'agence n'est jamais
remplacée.

- **Le Canva** ne donne que des vignettes par son interface. Un export PDF « pro » du design,
  en lecture seule, en contient les images incorporées ; `scripts/extraire-canva.py` les
  range par domaine. La photo d'une page de domaine ne sert qu'à ce domaine. Les noms de
  fichiers ont permis d'écarter deux images générées par IA (portrait Solemme, bouteille
  Noëls).
- **Deux personnes dans un rond** : à la demande de l'agence, on recule au lieu de recadrer
  serré, pour qu'aucune tête ne soit coupée (n°18, n°37). Quand le carré déborde de la photo,
  la marge prend la couleur médiane du bord : un premier essai avec la photo floutée en fond
  faisait réapparaître un visage fantôme au-dessus des têtes, rejeté.
- **Deux portraits séparés** d'un couple ou d'une équipe (n°12, n°30) : un rond partagé en
  deux moitiés, plutôt que de choisir l'un des deux.
- **Le site du n°3** était un homonyme (un lieu de réception en Hauts-de-France) : retiré.
- **Loi Évin** : sept photos de dégustation écartées ; deux ronds (n°10, n°18) recadrés
  au-dessus d'un verre tenu en main, signalés dans `QUESTIONS.md`.
- La mention de dernière page qui disait les emplacements « livrés vides » est désormais
  calculée depuis ce qui est posé (`creditPhotos()`), dans le PDF comme dans le `.pptx`.

Restent vides : les bouteilles n°15, 18 et 21 (aucune photo détourable trouvée).

### Nuit du 1er au 2 octobre : chaque bouteille regardée

L'agence a tout validé, puis demandé de pousser jusqu'au bout : des bouteilles « vraiment
découpées, pas découpées bizarrement ». Les 39 bouteilles ont été regardées une à une, à
grande taille, sur fond sombre, puis passées à un test automatique de symétrie (une
bouteille est symétrique ; un bouchon mangé d'un côté ne l'est plus).

- **n°24 ADN 24** : le bouchon blanc, sur fond blanc, partait à moitié avec le fond. Le
  remplissage à tolérance large (24) le mangeait ; à tolérance 4 il reste entier. Option
  `tolerances` ajoutée.
- **n°15 Verchères** : la bouteille, photographiée devant une caisse en bois, n'était pas
  détourable par remplissage. Le modèle de segmentation `rembg` (isnet-general-use) la
  détoure ; il laissait deux lettres du logo de la caisse collées aux épaules. Corrigé par
  la géométrie de la bouteille : axe ajusté en droite (la photo est un peu de biais),
  symétrie autour de cet axe, médiane glissante du profil, et une bouteille ne s'élargit
  jamais en remontant vers le goulot. Essayé et rejeté : le seuil d'alpha seul, et la
  symétrie autour d'un axe vertical (décalé de 10 px, il laissait passer la lettre).
- **n°24 avec le modèle** : rejeté, le modèle voit la bouteille sombre comme à moitié
  transparente. Le remplissage serré est meilleur pour ce cas.
- **n°28 Pré la Lande** : le reflet sous la bouteille est coupé par un recadrage au ras du
  pied.
- **n°31 JOIO** : la petite image (156 px) est remplacée par la version 2000 px trouvée dans
  la médiathèque WordPress du domaine, détourée par le modèle.
- **n°21 Trichon** : le rond passe d'une photo de mise en bouteille au couple de vignerons,
  tiré de l'album que le domaine a envoyé à l'agence pour le catalogue, recadré au-dessus
  des diplômes de médailles qu'ils tiennent (aucune médaille n'est dans notre tarif). La
  bouteille : une Mondeuse du Bugey du site, faute de Rhône (signalé dans `QUESTIONS.md`).
- **n°18 Moulin Blanc** : cherché sur le site du groupe, dans les médiathèques, dans le
  Drive, dans quatre designs Canva et dans la messagerie ; la seule piste est une pièce
  jointe de mail illisible d'ici. Reste vide.

Faux positifs du test de symétrie, vérifiés à l'œil et laissés tels quels : n°11 et n°15
(photos légèrement de biais), n°14 (texte de capsule qui fait le tour du goulot), n°26
(pli réel de la capsule).

Deuxième passe, même nuit : deux contrôles automatiques de plus sur les 39 bouteilles.
Les pixels translucides détachés du corps signalent une ombre portée : n°39, et n°36 dont
la bouteille a été remplacée par la même en haute définition (site du domaine, 1013 px au
lieu de 172). Les deux perdent leur ombre (`ombre: couper`). Le test du liseré clair au
bord, lui, s'est révélé non concluant : il compte les étiquettes blanches qui touchent le
verre ; vu à l'œil, le liseré d'un pixel des bouteilles sombres se fond dans le papier
clair de la page et ne se verra pas. Laissé tel quel.

### Le .pptx : la lettrine, et des ronds qu'on peut recentrer

L'agence voulait retrouver dans le .pptx la lettrine du PDF (Young Serif violette) et
pouvoir recentrer une photo mal cadrée directement dans Canva.

- **La lettrine.** Un .pptx ne sait pas faire tomber une lettre sur deux lignes ; elle y
  monte au-dessus de la première ligne, qu'elle rend plus haute. À 2,1 fois le corps, les
  textes les plus longs (n°16, n°17, qui touchaient déjà leur tableau sans lettrine)
  débordaient dans le rendu. Une estimation théorique de la place libre donnait des tailles
  très inégales d'une fiche à l'autre : rejetée. Retenu : `scripts/regler-lettrines.py`
  rend le .pptx dans LibreOffice, mesure chaque bloc de texte (PyMuPDF, par la police :
  Spectral et Young Serif, pas le tableau en IBM Plex Sans) et ne réduit que les fautifs,
  d'abord la lettrine (1,8 → 1,55 → 1,3), puis l'interligne. Résultat : 1,8 fois partout,
  1,3 au n°26, 1,3 avec un interligne resserré aux n°16 (1,30) et n°17 (1,36).
- **Les ronds recadrables.** Un second fichier, `…-canva-recadrable.pptx`, pose les 25
  photos simples en entier (à l'échelle du rond) avec un recadrage carré et un masque en
  ellipse, au lieu du rond déjà découpé. LibreOffice les rend à l'identique. Ce que Canva
  fait de ce recadrage à l'import n'a pas pu être vérifié d'ici : la version découpée
  reste le fichier principal. Les ronds n°10 et n°18 restent figés exprès (leur photo
  entière montre un verre).

### La lettrine disparaissait à l'import : un .pptx hors norme

Retour de l'agence : dans son import, la première lettre des présentations n'était pas
stylée. Le rendu LibreOffice, lui, la montrait. En relisant le XML : pptxgenjs répète les
propriétés du paragraphe (`<a:pPr>`) devant **chaque** morceau de texte, donc entre la
lettrine et la suite. La norme Office n'en admet qu'une, en tête du paragraphe ; le
validateur de schéma rejetait 71 diapositives sur 76 (1 417 paragraphes : lettrines,
mots en gras du mode d'emploi, index…). LibreOffice passe outre ; un import strict lit la
seconde `<a:pPr>` comme une rupture et perd la mise en forme du premier morceau, c'est-à-dire
la lettrine.

- **Réparation** dans `scripts/ranger-pptx.py`, qui réécrivait déjà l'archive : une seule
  `<a:pPr>` par paragraphe, en tête. Les répétitions étaient toutes identiques à la
  première (vérifié ; le script s'arrête si un jour elles diffèrent).
- **Contrôle** dans `scripts/controler-pptx.mjs` : aucun paragraphe hors norme, et les 40
  présentations ouvrent bien sur leur lettrine (premier morceau, Young Serif, violet
  67067C). Testé à rebours : le fichier non réparé sort en rouge sur ces deux lignes.
- **Résultat** : 76 diapositives sur 76 conformes au schéma, dans les deux .pptx. Rendu
  identique à l'œil : rien n'a bougé, seul le XML a changé.

### Dans Canva, la lettrine devient une boîte à part

La réparation du XML n'a pas suffi : importé dans Canva (essai fait depuis le dépôt public),
le « S » du n°2 arrivait violet, mais à la taille et dans la police du texte. Une planche
de six variantes (`essais/lettrine-canva.mjs`) a tranché :
- **Lettrine écrite dans le paragraphe** (en Young Serif, dans la même police, en IBM
  Plex Sans que Canva connaît, en gras) : Canva garde la couleur et le gras, et ramène tout
  le paragraphe à une seule police et une seule taille.
- **Lettrine dans sa propre boîte** : Canva garde sa taille et sa couleur. Il jette le
  retrait de première ligne (`indent`).

Retenu : la lettrine a sa boîte, et des espaces insécables lui gardent sa place en tête
du texte (Spectral n'a pas d'espace cadratin ; l'insécable fait 0,25 cadratin).

**Le calage vertical.** Une planche de calibrage (`essais/calibrage-canva.mjs`), importée
dans Canva et rendue par LibreOffice, mesurée dans les deux PDF avec PyMuPDF, donne :
- **LibreOffice, comme PowerPoint** : la première ligne de base tombe à l'ascendante,
  plus le supplément d'interligne posé au-dessus (1,2 × corps × (interligne − 1)).
- **Canva** : la première ligne de base tombe à l'ascendante seule, quel que soit
  l'interligne : 0,854 corps pour Spectral, remplacée par Arimo tant qu'elle n'est pas
  téléversée, et 0,92 pour Young Serif, remplacée par TYSerif.

On pose la lettrine pour Canva, puis on lui donne un interligne à elle, que Canva ignore et
que LibreOffice applique, calculé pour qu'elle retombe aussi sur la ligne de base dans
LibreOffice et PowerPoint. Si l'agence téléverse ensuite les vraies polices, les deux
ascendantes changent ensemble (1,059 et 1,046) : le décalage reste sous 0,2 mm.

Le texte est désormais ancré en haut, et non plus au milieu de sa bande : c'est la seule
façon de savoir où tombe la première ligne. Pour garder le bloc centré comme dans le PDF,
`regler-lettrines.py` compte les lignes de chaque texte dans le rendu LibreOffice et les
note dans `lettrines-pptx.json`.

**Le calage horizontal.** Premier import des 40 fiches dans Canva : les lettrines tombent
toutes sur la ligne de base (écart de 0 à 0,2 mm ; 0,47 mm pour la petite lettrine du
n°16). Mais le blanc entre la lettre et la suite du mot va de 1 à 3 mm (« S  ur »),
contre 0,2 à 0,6 mm dans LibreOffice. Deux causes, mesurées :
- les espaces d'Arimo sont plus larges que celles de Spectral (la réserve fait 1 mm de plus) ;
- TYSerif est plus étroite que Young Serif (le S : 4,4 mm au lieu de 6,0).

Corrigé de trois façons :
- **Insécables seules.** L'espace fine, encore plus large chez Arimo, est abandonnée.
- **Corps ajusté.** La lettrine prend le corps exact qui remplit la place réservée, à
  quelques pour cent de la taille visée (de 11 à 25 pt selon le corps du texte).
- **Alignement à droite.** La lettrine est alignée à droite dans sa boîte, contre son mot.

Avec les vraies polices (LibreOffice, ou Canva une fois Young Serif et Spectral
téléversées), la lettre est au ras de la colonne et le blanc fait 0,25 mm. Avec les
polices de remplacement de Canva, la lettre reste collée à son mot ; c'est son bord
gauche qui rentre un peu.

Contrôle final dans Canva (import du fichier poussé, export PDF des 40 fiches, mesuré par
`essais/mesurer-lettrines.py`) :
- **blanc avant la suite du mot** : de 0,6 à 1,3 mm, avec les polices de remplacement ;
- **ligne de base** : de −0,48 à +0,21 mm.

Ce dernier écart vient des arrondis de Canva, différents d'un corps à l'autre (0,90
cadratin sous le haut de la boîte à 13 pt, 0,84 à 11 pt), et non du calage. Il ne se
corrige pas d'un réglage global et ne se voit pas à la lecture (vérifié à 200 dpi).
LibreOffice : 0,15 mm au plus, blanc de 0,2 mm.

### Passage de relais : le Salon Privé du 5 octobre

L'agence ouvre une nouvelle session pour la suite. Le relais est dans `docs/reprise.md`,
chargé par `CLAUDE.md`. La suite comprend trois livrables :
- les retouches du catalogue général : pages 3 et 5 supprimées, sommaire simple, note de
  prix agrandie et remontée sous le tableau ;
- l'édition du Salon Privé (26 stands, sans prix pour l'instant) ;
- la liste des vins dégustés.

Les quatre documents du salon sont dans `sources/salon-prive-2026/`.
`data/salon-prive-2026.json` rapproche les 26 stands de 31 fiches. Les numéros de stand
viennent de la liste des domaines et du plan, recoupés avec les cartes du Padlet, numérotées
de même. Les questions ouvertes sont au point 25 de `QUESTIONS.md` ; Strasser Radziwill
(« En conversion Bio » au salon, « Bio » au tarif) s'ajoute au point 22.

Réponses de l'agence, le 2 octobre :
- **le plan fait foi** ; sa version 2 est identique à la première ;
- **prix** : on ne sait pas encore si ce sera un prix unique ou des paliers ;
- **Exea** : pas de jus de cépages ;
- **Divin No Low** : « normalement » présent ;
- **Goichot** : la composition des tables fait foi ;
- **labels** : « pour le 5, moins on en dit, moins on fait d'erreur ».

Pour les labels, la règle retenue : un label ne s'affiche au salon que si le tarif et la
liste du salon disent la même chose. Elle est appliquée d'avance, stand par stand, dans
`data/salon-prive-2026.json` : 13 stands gardent leur label, 13 n'en ont aucun.

Précision de l'agence, le même jour : **pour les labels, la liste des vignerons fait foi**.
Le document renvoyé est identique à celui de `sources/salon-prive-2026/`. Au salon, chaque
fiche affiche donc le label de la notice de son stand, tel quel. La règle « seulement si
tarif et liste s'accordent » est abandonnée. Reste à savoir si cela vaut aussi pour le
catalogue général.

## 2 octobre 2026 — reprise : le catalogue général retouché (livrable A)

**Labels.** Question posée en début de session : la liste des vignerons du salon vaut-elle
aussi pour le catalogue général ? Réponse : **oui, partout**. `scripts/reporter-labels.py`
reporte le label de chaque notice sur les 31 fiches du salon (18 changent : n°4 Bio → HVE,
n°6 → ISO 26000, n°10 AOP → Agriculture raisonnée, n°12 et n°36 → HVE, n°16 à 19, 22, 34,
37, 38, 40 → En conversion Bio, n°23 → HVE 3, n°27 et n°28 → Biodynamie, n°39 → Bio &
Biodynamie). Le script garde la mise en page à la main des fiches et consigne l'ancien
label dans `labels_tarif`. Les 9 fiches absentes du salon gardent le tarif.

**Pictos de label.** Les nouveaux libellés demandaient leurs pictos. Une seule géométrie,
une feuille, et le remplissage dit le label : pleine (Bio), à moitié (En conversion),
évidée avec un cœur (Biodynamie), pleine au cœur clair (Bio & Biodynamie), nervure
verticale (HVE, HVE 3), nervure transversale (Agriculture raisonnée), contour pointillé
(ISO 26000). Tout se distingue en niveaux de gris, rien ne ressemble aux logos officiels,
et le mot reste toujours écrit à côté, dans le jeton. AOP et IGP disent une origine, pas une
pratique : pas de feuille.

**Pages 3 et 5 supprimées.** « Comment lire ce catalogue » et « Les quatre alliances »
sortent des gabarits (`pages.mjs`), de la pagination (`AVANT = 3`), du .pptx, de la déco
et des styles. Le panachage reste sur chaque fiche (jeton, encart « Se panache avec… »).
Aucun texte ne renvoyait plus à ces pages, sauf le mode d'emploi lui-même (« les quatre
alliances sont page 7 »), parti avec lui.

**Le sommaire, comme d'habitude.** Une liste par région, sur deux colonnes équilibrées
par le calcul (`colonnesSommaire`) : Loire à Rhône à gauche, Sud-Ouest à Champagne à
droite. Chaque région ouvre sur une bande de sa strate (couleur et trame), le nom écrit en
craie dessus, à l'encre sur la craie de Champagne : la règle « le nom de région dans sa
couleur de strate » est tenue sans écrire de l'ocre sur du tuffeau, trop pâle à lire.
Les hauteurs sont fixes (`SOMMAIRE`), le .pptx les reprend. La légende complète des
pictos, qui vivait sur la page 3, descend en pied du sommaire.

**La note de prix sous le tableau.** Elle sort du pied de fiche et vient juste après le
dernier tableau, en IBM Plex Sans 10,5 pt, filet violet à gauche. Dans la pagination, sa
hauteur mesurée s'ajoute à la dernière ligne du dernier tableau : elle voyage avec elle et
ne se retrouve jamais seule en haut d'une page. Le descripteur de page porte `note: true`
pour le .pptx, qui la pose à la même place. Les départements restent en pied de fiche.

**Résultat.** 72 pages (multiple de 4 sans page de remplissage), 715 prix retrouvés dans le
texte du PDF, polices embarquées, tous les contrôles au vert ; .pptx à 72 diapositives,
contrôles au vert. Chaque page regardée en image. `regler-lettrines.py` relancé : rien ne
bouge (il faut d'abord installer les .ttf de `polices-canva/` dans `~/.local/share/fonts`,
sinon LibreOffice substitue les polices et le script ne trouve aucune lettrine).

## 2 octobre 2026 — l'édition du Salon Privé (livrables B et C)

**Le fichier de Mathéo** est le Padlet déjà déposé, octet pour octet (même empreinte). On n'en a
lu que les cartes de stand, pages 3 à 20. Les pages doubles (deux cartes séparées par un trait
vertical) ont été transcrites colonne par colonne, sur des recadrages agrandis, puis relues
une seconde fois face à la transcription. 177 lignes, 26 stands, 6 doublons (dont les quatre
vins du stand 25, écrits deux fois). La transcription et le rapprochement vivent dans
`scripts/transcrire-matheo.py`, une décision par ligne, lisible et corrigeable.

**La règle de rapprochement.** La liste dit quels vins et quel millésime ; le tarif dit tout
le reste. Un vin rapproché reprend appellation, cuvée, couleur et contenance du tarif ; le
millésime est celui de la liste (c'est la bouteille ouverte), et un millésime absent du tarif
devient un écart signalé. Un vin absent du tarif (45 sur 171 !) s'affiche tel que la liste
l'écrit, aux corrections de forme près, sans contenance. Écarté : afficher seulement les vins
du tarif, qui aurait fait disparaître un quart de la dégustation ; et compléter les absents
avec des informations prises ailleurs, ce qui serait inventer.

Une erreur rattrapée à l'épreuve : les absents dont la couleur faisait la différence (« Mas
de Lusanne Brut Blanc » et « Extra-Brut Blanc », « Baron Auguste Blanc » et « Rosé ») se
retrouvaient avec le même nom, puisque le tableau ne montre la couleur que par un picto. Leur
nom garde maintenant les mots de la liste.

**Une édition, pas une copie.** `EDITION=salon` (dans `pieces.mjs`) construit un catalogue
réduit à partir du catalogue général : les 31 fiches des 26 stands, leurs tableaux réduits
aux vins dégustés, chacun rangé dans le tableau du tarif d'où il vient (avec ses paliers).
Tous les gabarits sont partagés ; ce qui diffère tient dans un objet `ED` (les mots et les
nombres) et dans `numero(d)` : au salon, c'est le **numéro du stand**, dans une pastille or
(la couleur du logo) avec sa salle, qui prend la place du numéro du tarif. C'est lui qu'on
cherche sur le plan. Les fichiers de sortie et de mesure portent le nom de l'édition.

**Le plan des exposants**, page 4 : un schéma maison (les deux salles, l'accueil, les 26
pastilles à leur place relevée sur le plan de l'agence, chacune dans la couleur de strate de
sa région), et la liste des stands avec leur page. Le dessin du plan de l'agence (bordeaux,
Playfair) n'est pas repris. Les pastilles sont des liens dans la version écran. Dans le .pptx,
les salles sont une image et les pastilles de vraies formes avec du vrai texte.

**Les prix absents.** Une case de prix vide (`null`) porte un pointillé fin, là où l'on
écrirait le prix ; rien d'autre ne bouge, puisque le bloc de prix garde sa largeur fixe. Le
mode « unique » remplace les paliers par une colonne « Prix salon » : c'est la donnée qui
bascule, pas le gabarit. Essayé avec des prix factices (un stand en prix unique, deux en
paliers, un stand qui mélange les deux et que l'import refuse), puis remis à vide.

**La strate de couverture** compte les stands au salon (26), pas les fiches (31) : sinon le
sous-titre « vingt-six vignerons » et la coupe se contredisaient.

**La liste des vins** (livrable C) : 3 pages A4, deux colonnes, stands dans l'ordre du plan,
jamais coupés. La répartition est mesurée dans Chromium. Un vin tient sur une ligne : la
cuvée en gras, l'appellation à la suite, la couleur et le millésime alignés. Première version
à 5 pages (cuvée et appellation sur deux lignes) : trop aérée pour un document de salon.
Proposé en A4 pour une impression au bureau ; le format du catalogue reste à un réglage près.

## 2 octobre 2026 — retour de l'agence : la date en haut, un sommaire sobre

« C'est beau, c'est clean, c'est carré. » Deux retouches demandées :

**La date en haut de la première page.** Sur les deux couvertures, l'édition passait en bas,
dans un cartouche posé sur la coupe. Elle remonte en haut à droite, en face du logo :
« Tarifs cavistes Vendée (85) / 2026 » pour le catalogue général, « Lundi 5 octobre 2026 /
Château de la Rairie / Pont-Saint-Martin » pour le salon, sous le titre « Salon Privé Vins &
Terroirs ». Le bas de la couverture ne porte plus que la coupe, sans cartouche : c'est plus
net. Même chose dans les deux .pptx.

**Un sommaire qui coûte le moins d'encre.** Les bandes de région pleines (couleur et trame)
coûtaient cher à l'impression. Le sommaire passe en version sobre et uniforme : le nom de la
région en violet, un filet violet dessous, et de la couleur de strate seulement dans une
pastille de 3 mm, comme un repère de tranche. Les listes de domaines ne changent pas. Les
images de bandes de la déco du .pptx disparaissent : le .pptx dessine la pastille et le filet
en formes simples, modifiables dans Canva.

**Le plan des exposants reste** : « pas besoin, mais j'aime bien ». Il se retire d'une ligne
dans `scripts/construire.mjs` si l'agence change d'avis.

**Le plan des exposants, finalement retiré** (l'agence, même jour : « la version sans le plan
des exposants »). La page, son schéma, sa diapositive, sa déco et la position des stands dans
`data/salon-prive-2026.json` sont supprimés ; le numéro de stand et la salle restent sur
chaque fiche, pour se repérer sur le plan de l'agence. Le salon garde 52 pages : la
pagination complète seule avec deux pages « Vos notes » au lieu d'une.

**Les 21 couleurs manquantes.** L'agence les a données vin par vin. Elles vivent dans
`COULEURS_AGENCE` de `transcrire-matheo.py` (repérées par stand et ligne de la liste, pour
qu'une couleur ne se pose jamais sur le mauvais vin ; le script refuse une couleur sans vin ou
un vin qui en avait déjà une). « Effervescent » rejoint « pétillant » et « brut » parmi les
mots qui donnent le picto bulles. Les nouvelles couleurs, plus longues, faisaient passer la
liste des vins à 4 pages : l'en-tête et les interlignes ont été resserrés d'un rien, retour à
3 pages. Le tableur des couleurs manquantes, désormais vide, est retiré.

## 2 octobre 2026 — le dossier de référence de Mathéo, des tableaux plus lisibles, 52 pages

**Le dossier de référence de Mathéo** remplace le Padlet pour tout le salon : textes, labels et
listes de vins (« tout est bon dans son document maintenant »). Deux scripts :
`scripts/textes-matheo.py` reporte les 26 textes et labels sur les fiches (le texte du tarif
reste dans `texte_tarif` ; les mentions propres au salon, « Vins sous allocation. », « Format
BIB disponible. »…, sont retirées du texte du catalogue général, qui les porte en jetons) ;
`scripts/transcrire-matheo.py` relit les 26 cartes. La règle d'affichage change : **tout ce
qui s'affiche d'un vin vient du dossier** (cuvée, appellation, couleur, millésime), le tarif ne
donne plus que la contenance et le tableau. Corrections de forme seulement, plus les deux
fautes signalées par l'agence (Molse, Demoiselles) ; les noms propres gardent leur graphie
(Berteaud Manceau comme sur le logo, Boehler). Une couleur de l'agence l'emporte désormais
sur celle de la liste (l'assertion qui refusait ce cas est retirée) : c'est le cas de
Premières Fleurs, rouge dans le dossier, blanc pour l'agence — signalé (QUESTIONS 26).
180 vins, 1 doublon. Le contrôle « chaque vin est imprimé » compare sans espaces ni traits
d'union : un « Extra-Brut » coupé en fin de ligne passait pour absent.

**Moulin Blanc (n°18).** La bouteille envoyée par l'agence est détourée par le modèle
(le fond n'était pas uni : le remplissage échouait) ; `preparer-photos.py --seulement 18`
ne retraite que ce domaine. Le rond du couple est recadré plus large : les deux visages
entiers, toujours au-dessus du verre (loi Évin).

**Tableaux plus lisibles.** Cuvée 9,6 pt demi-gras, prix 10 pt, appellation et détails 8 pt
500. Effet de bord : les lignes passaient de 9,6 à 11,7 mm et le catalogue à 76 pages.

**52 pages au plus** (l'agence : « agrandis l'écriture mais pas les tableaux »). Essais, dans
l'ordre :
1. L'interligne hérité du corps de texte (1,45) gonflait chaque ligne de tableau. Interligne
   1,12 et marges de cellule de 0,7 mm : 8,6 mm par ligne, même écriture. 76 → 68 pages.
2. Les dix ouvertures de région et l'index des domaines retirés du catalogue général (le
   sommaire par région les remplace ; options `ouvertures` et `indexDomaines` de `ED`,
   `pages.mjs`). Le salon les garde. 68 → 56 pages.
3. En-têtes et pieds de fiche resserrés d'un à deux millimètres chacun.
4. **La bande du haut s'abaisse** quand cela épargne une page : la pagination essaie 62, 56,
   50, 46 et 44 mm et garde la plus haute qui donne le moins de pages (`BANDES`,
   `emplacementPour()` dans `pieces.mjs`). La bouteille rapetisse dans ses proportions, le
   rond garde ses 40 mm, la colonne de texte s'élargit et le corps se recalcule. n°6, 8, 10
   et 24 tiennent ainsi sur une page. Écarté : supprimer la bouteille ou le rond de ces
   fiches (on perdait des photos sourcées une à une), ou mettre deux petits domaines sur une
   page (on perdait « un domaine, une page », qui fait la navigation).
→ **52 pages**, sans page de remplissage. Le .pptx suit : la bande vient du descripteur
(`desc.bande`), les marges des cellules et l'interligne sont serrés comme dans le PDF, et le
pied est recalé sur le nouveau pied du PDF. Lettrines du .pptx réglées de nouveau.

## 2 octobre 2026 — les bouteilles retouchées par l'agence (Gemini)

L'agence a refait neuf bouteilles avec Gemini, sur un fond propre, et les a déposées dans
son Drive (« les photos gemini / photo gemini ») : Barbinière, Colombier, Magnien, Verchères,
Pousterle, Trichon, Stratéus, Exea, Gragnos. Elles remplacent les bouteilles de ces neuf
fiches. Le dossier ne contenait pas de Moulin Blanc (la dixième image était la Verchères
exportée de notre .pptx, plus petite) : sa bouteille reste celle du matin.

- Téléchargées par le connecteur Drive (le contenu arrive en base64 dans un fichier, décodé
  dans `src/photos/brut/gemini/`, renommé `dNN-domaine-cuvée.jpg`). L'identifiant Drive de
  chaque image est dans `page` de `data/photos-locales.json`.
- `--seulement` refaisait aussi les ronds : trois originaux de ronds (n°3, 10, 19) ne sont
  pas dans ce conteneur et ces ronds tombaient. Option `--role bouteille` ajoutée.
- Détourage au modèle pour huit ; Exea au remplissage depuis les bords (fond blanc uni ; le
  modèle laissait le centre de la bouteille incertain). Stratéus : le modèle prenait les
  plages blanches de l'étiquette pour du fond. Option `remplir` : l'intérieur de la
  silhouette est rendu opaque et le profil ne se creuse pas (une rangée plus étroite que ses
  voisines du dessus et du dessous reprend leur largeur).
- Vérifié sur le fond du catalogue et sur un fond magenta (qui montre la moindre bavure),
  puis dans les fiches. Toutes au-dessus de 780 ppi.

**Retour de l'agence : Verchères et Barbinière « trop découpées ».** Deux blancs en verre
clair : le modèle prenait le verre pour du fond (la bouteille devenait en partie transparente)
et grignotait le pied. Verchères passe au remplissage depuis les bords (fond blanc uni) :
pied entier, verre opaque. Barbinière a en plus un bouchon blanc sur fond blanc légèrement
dégradé : le remplissage mangeait le bouchon, le modèle le pied. Nouveau mode
`"detourage": "modele+bords"` : l'union des deux silhouettes, avec `remplir`. Vérifié sur
fond magenta et dans les deux éditions.

## 2 octobre 2026, soir — « le nouveau fichier de Mathéo » : rien de nouveau

L'agence a renvoyé deux fois le dossier de Mathéo, « avec les derniers changements » :
`mateo_le_dossier_r_ference_compressed.pdf`, puis
`ma-sandbox-magnifique_board_…_2_3_compressed.pdf` (et l'original non compressé `…_2_2`).
Les trois sont **la même exportation du Padlet** (créée le 2 octobre à 15 h 44 UTC, comme le
dossier appliqué à 16 h 14), seulement recompressée :
- au pixel près, à 150 et 300 dpi, la version `_2_3` est identique au dossier appliqué
  (écart maximal 0) ; les autres ne diffèrent que par le bruit de compression ;
- relecture OCR (Tesseract, français) des 20 pages : chaque vin des 26 stands retrouvé, aucune
  puce du dossier sans vin ; les millésimes et les dates douteuses à l'OCR (Falfas Chevalier
  2019, Vazart-Coquart 1954, Balac 1964) vérifiés à l'image : la transcription est juste
  (l'écriture du Padlet fait lire un 9 comme un 4).
Les « petites différences » dont parle Mathéo sont celles entre le Padlet du matin et ce
dossier : 19 stands, textes et labels, déjà appliquées (QUESTIONS, points 26 et 30). S'il a
retouché le Padlet après 15 h 44, il faut une nouvelle exportation.

## 2 octobre 2026, soir — revérification complète

`npm run build` et `npm run salon` : tous les contrôles au vert (715 prix, 40 domaines,
26 stands, 180 vins, polices incorporées, 52 / 48 / 3 pages). En plus : liens de la version
écran (tel, mailto, site, et 447 / 276 liens internes, tous vers la bonne page), polices de
chaque PDF, et chaque page regardée en image. Trois défauts trouvés et corrigés :
- **Mot seul en fin de cuvée** dans un tableau (« …Extra- / Brut », « …Brut / Nature ») :
  `sansVeuve()` (pieces.mjs) garde ensemble les deux derniers mots et ne coupe jamais un mot
  composé ; le .pptx lie aussi les deux derniers mots par une espace insécable.
- **Liste des vins** : les jus de cépages d'Exea y portaient la couleur de leur ligne
  (rouge, blanc, rosé) avec une pastille de vin ; ils prennent la famille de leur tableau,
  comme dans le catalogue (« Jus de cépages »). « Vazart-Coquart » ne se coupe plus au trait
  d'union ; plus de mot isolé.
- QUESTIONS 26 : le dossier liste deux Premières Fleurs (Blanc et Rouge 2025), pas une.

## 3 octobre 2026 — le sommaire nomme les Vignobles Strasser Radziwill

Demande de l'agence : dans le sommaire, les quatre domaines du groupe (n°16 à 19, stand 7
au salon) portent « (Vignobles Strasser Radziwill) » en petit. La mention vit dans les
données (`mention_sommaire` du groupe, `data/agence.json`) et s'écrit sous le nom : sur la
même ligne, « Domaine Le Prieuré des Papes (Vignobles Strasser Radziwill) » ne tenait pas
dans la colonne et le nom aurait été tronqué. Ces quatre lignes passent de 5,6 à 8,8 mm ;
le partage des colonnes en tient compte. Même chose dans les deux .pptx, et dans l'édition
du salon.

## 3 octobre 2026 — nouveau dossier de Mathéo, et le stand 26

L'agence envoie une nouvelle exportation du dossier de Mathéo (`…_1790850846_3.pdf`, créée le
3 octobre à 8 h 44 UTC) et demande, au stand 26, « AOP Bourgogne Chardonnay 2023 », sans le
nom du château. Cette fois ce n'est pas la même exportation : comparée au pixel (rendus
flous, seuil 50) à celle du 2 octobre, 14 pages diffèrent. Chaque écart relu à l'image :
- **Contenu** : « Rouge aux lèvres » (n°3) ; « AOC Mâcon Mancey Rouge 2024 » et « Les Bulles
  du Puits Rosé Gamay Demi-Sec » (n°15) ; « L'inopiné de Balac » (n°29) ; « Sainte-Probace »
  (n°31) ; chez François Reverdy (n°1), « AOC » au lieu de « AOP » (Anjou, Saumur, Quincy,
  Sancerre, Chinon) ; texte du stand 6 (n°23) : « Bas-Armagnac » au singulier.
- **Forme** (déjà corrigée chez nous pour la plupart) : Crémant, Molse, traits d'union,
  majuscules (L'Envol, Le Prestige, La Perle, Chêne à la Rouline), titres de cartes (Boehler,
  Sébastien Magnien, Pré La Lande, Vignobles Strasser-Radziwill), noms de région des cartes.
- **Stand 26** : le dossier écrit « AOC Bourgogne Chardonnay Blanc 2023 » ; on affiche ce
  que l'agence demande, « AOP Bourgogne Chardonnay 2023 » (couleur Blanc, du tarif).
Le dossier remplace `sources/salon-prive-2026/matheo-dossier-reference.pdf`. Lignes mises à
jour dans `transcrire-matheo.py` (deux corrections de forme élargies : « Pays D'Oc »,
« Méthode Traditionnelle »), texte dans `textes-matheo.py`. Le changement de texte du n°23
est en fin de paragraphe : la lettrine ne bouge pas, pas de `regler-lettrines.py`.

## 3 octobre 2026 — prix du salon : en attente

Les prix du salon ne sont pas encore connus (« pour l'instant il y a rien ») : l'agence
enverra ses documents au fil de l'eau, avec les détails. Prêt en attendant :
`scripts/preremplir-prix-salon.py` sort un tableur pré-rempli avec les prix du tarif
(134 vins rapprochés, dont 53 à regarder ; 46 absents du tarif), au cas où l'agence voudrait
partir du tarif. Rien n'est importé.

## 3 octobre 2026 — les prix du Salon Privé

L'agence a scanné ses tarifs annotés (bourrage papier : 4 PDF dans le Drive, dossier
« tableau catalogue », plus un cinquième pour Trichon), rangés par stand, et dicté ses
consignes domaine par domaine. Le connecteur Drive refuse les fichiers de plus de 10 Mo : le
dossier a été partagé par lien, téléchargé par `drive.usercontent.google.com`. Les scans sont
dans `sources/salon-prive-2026/scans-prix/` (41 Mo).

- **Relevé** : chaque page lue en image (rendus à 200 dpi, recadrés, tournés), prix surlignés
  notés dans `data/prix-salon-releve.md` avec la page du scan, puis **seconde passe** : chaque
  tableau relu face aux données saisies avant la saisie définitive.
- **Données** : `scripts/prix-salon.py` (nouveau, `npm run prix-salon`, enchaîné après
  `npm run transcrire-matheo`) écrit dans `data/salon-prive-2026.json` les paliers du salon
  par fiche (`paliers_salon`), les prix vin par vin, les offres (`offre`) et le bas de fiche
  (`offre_salon`). Prix en centimes, convertis depuis le texte sans flottant.
- **Gabarit** : un tableau du salon prend les paliers du salon ; quatre paliers élargissent le
  bloc de prix (`table.tarif.p4`, 66 mm) ; un prix seul sur une ligne à paliers (magnum à
  prix unique) occupe toute la largeur (`.cel-prix.seul`) ; l'offre est une petite étiquette
  or et violet après le nom du vin (`.offre`) ; l'offre du stand suit la note de prix
  (`.offre-salon`). « Magnum 1,5 L » passe sur deux lignes dans un tableau à paliers. Même
  chose dans le .pptx.
- **Retouches de liste** demandées : « Brut Nature » retiré chez Frézier (`RETIRE`) ; « AOP
  Bourgogne Chardonnay 2023 » rangé sur la fiche des Guignottes (le tarif annoté barre le Cray) ;
  Auxey-Duresses en blanc et Mercurey blanc sur la fiche du Cray, d'après le surlignage.
- **Lignes ajoutées** (9) : Balac 2018, trois magnums d'Albas, Les Jumelles chez Coyeux
  (« Rajouter Beaumes de Venise »), magnum de Brut Réserve (Vazart), deux magnums d'Exea,
  magnum de Plénitude (Solemme). Les magnums ne vont pas dans la liste des vins dégustés
  (`liste_vins: false`).
- **Tableur** : `tableur/prix-salon-prive-2026.xlsx` suit les paliers du salon, quatre colonnes
  de paliers ; une ligne peut avoir un prix unique (colonne F) dans un stand à paliers.
  Aller-retour vérifié : 0 changement.
- Le dossier de Mathéo renvoyé avec les consignes est identique, octet pour octet, à celui en
  place.
Les doutes sont dans QUESTIONS, point 31.

Réponses de l'agence le même jour : Goichot (Chardonnay des Guignottes, Auxey blanc, Mercurey
Maison), magnum et bouteille de Brut Réserve, Les Jumelles sans millésime : confirmés ; offre du
Triton (Haut Marin) **dès 250 cols**, corrigé. Six questions restent pour Laurent
(`docs/questions-laurent.md`). L'agence : on ne s'occupe que du Salon Privé pour l'instant.

Nouvelles réponses (3 octobre, soir) : **contenance** jamais vide au salon : « 75 cl » quand
rien n'est précisé, « 1,5 L » pour un magnum (`contenance()`, prix-salon.py) ; **Terroir
d'Ansouis rouge** ajouté (5,50 / 5,20 / 5,00, offre 5+1) ; **Verchères** : les deux derniers
prix inversés sur le Mâcon Chardonnay et les Bulles du Puits (6,10 / 5,75 / 5,45 et 6,40 /
5,75 / 5,45), sur instruction de l'agence ; **Boehler** : « Prix de la bouteille H.T. franco
de port. » au salon (`note_prix_salon`) ; **jus de cépages d'Exea** : six lignes, 50 cl 2,75 /
2,39 et 25 cl 1,84 / 1,74, d'après la photo du tarif (`scans-prix/photo-exea-jus-de-cepages.jpg`),
colonnes « À partir de 144 / 300 bts » comme sur la photo (l'agence a dit 72 et 144 : question
posée). Falfas confirmé. Salon : 192 lignes avec prix, aucune case vide.
Jus de cépages, précision de l'agence : **50 cl à partir de 72 / 144 bts, 25 cl à partir de
144 / 300 bts**. Deux tableaux sur la fiche (les 25 cl rangés dans le 2e tableau du tarif) ;
`paliers_salon` accepte une clé « fiche:tableau » (« 33:1 »), lue par le gabarit et le tableur.

## 3 octobre 2026, soir — le nouveau design choisi par l'agence

Retours : pas assez de photos, page 2 « un peu gamin », page 1 pas assez rêveuse, puis les
bandes de la couverture « pas esthétiques, enfantines ». Modèles successifs dans
`concepts/retouches-oct/` (A–C, D–F, G–I). Choix : couverture **H** (photo + strates droites),
page 2 **A** (Spectral, photo du Beaujolais), bas de fiche **A** (photo de région), ouverture
**A** (photo de région en fond). Appliqué aux deux éditions et aux .pptx ; photos de régions
de Wikimedia Commons (licences libres, `credits.md`). Le .pptx dépassait 50 Mo (photos en
PNG répétées sur chaque fiche) : déco photo exportée en JPEG, 28 Mo. Contrôles au vert :
52 et 48 pages, 715 et 439 prix retrouvés.

## 3 octobre, soir — relecture du Salon Privé par l'agence

- **Couverture** : « Tarif et offres valables du 5 octobre au 14 novembre 2026 » dans un
  cartouche violet à filet or, sous le sous-titre ; bande de strates ramenée de 148 à 108 mm
  (le ciel descend d'autant) ; la date et le lieu, blancs et perdus dans le ciel, posés sur une
  pastille gneiss. Même chose dans le .pptx (`deco.mjs` rend ciel et strates aux hauteurs du salon).
- **Bas de fiche** : l'offre du stand d'abord, la note de prix dessous.
- **Deux notes de prix seulement** au salon (`noteUniforme`, `pieces.mjs`) : « hors frais de
  transport » (dont tous les « départ ») ou « franco de port ».
- **Offres** : formule unique « Offre possible à étudier en fonction du volume et de la
  référence. » (Balac, Blacailloux, L'Escarderie) ; Trichon 11+1 dès 300 cols ; Falfas 11+1
  dès 120 cols ; Exea et jus 11+1 dès 240 cols. Les autres offres restent telles que l'agence
  les a dictées (stands 6, 16, 17 compris).
- **« Possibilité de panacher »** retiré des en-têtes, sauf les trois familles (Goichot / Cray /
  Guignottes ; Strasser Radziwill ; Exea et jus), où l'en-tête nomme les **autres** membres.
- Berteaud Manceau : colonne « à partir de 36 » supprimée (435 prix au lieu de 439) ;
  « AOC Auxey-Duresses Blanc » ; Koloss Doux 2025.
- **Folios toujours à droite**, dans les deux éditions (le message sanitaire passe à gauche
  sur les pages paires).
- User-Agent de `chercher-photos-regions.py` : retiré l'adresse e-mail.
## 3 octobre 2026, soir — la photo de Bourgogne en grand

L'original de Commons (Pommard, 3072 × 1461 px) remplace la vignette de 1280 px, floue à
l'impression : traité en 2400 × 1141 (`preparer-photos-regions.py`, seule la Bourgogne a son
original dans le conteneur, les autres gardent leur version déjà traitée). Commons répondait
429 à l'original : il est passé au 7e essai, une requête toutes les 75 s (la vignette de
1920 px, elle, passe tout de suite : solution de repli). Comparaison au pixel avec les PDF
d'avant : seules changent les pages qui portent la photo (catalogue général p.14 à 19 ; salon
p.13 à 18). Refait après fusion avec la relecture du salon : contrôles au vert, 52 et 48
pages, 715 et 435 prix, polices embarquées.
Aperçus : `epreuves/apercus/bourgogne-hd/`.

### 3 octobre, soir (suite)

- L'agence confirme le Pinot Noir des Guignottes (8,90 / 8,60 / 8,10) et garde la photo de
  Bourgogne.
- Stand 16 : « Offre possible à étudier en fonction du volume et de la référence. »
- Couverture du salon : la date et le lieu en haut à droite sont retirés ; le cartouche de
  validité passe en grand (deux lignes en Young Serif 21 pt, la première en or), PDF et .pptx.

### 3 octobre, soir — affiche du QR code

Affiche A4 portrait (`npm run affiche-qr` → `dist/salon-prive-2026-affiche-qr.pdf`) : photo du
Sud-Ouest et titre de la couverture, « Le catalogue du Salon Privé », le QR code fourni par
l'agence (`src/images/qr-catalogue-salon.png`, il mène au PDF du salon sur le Drive), « Scannez
pour découvrir le catalogue », message sanitaire. QR relu dans le PDF rendu : bon lien.
- Refaite sobre en encre à la demande de l'agence : plus de photo en haut, fond blanc, logo,
  « Salon Privé / Vins & Terroirs », « Le catalogue du salon », QR de 120 mm, une ligne.
- Nouveau QR code fourni par l'agence (l'ancien était une erreur) : il mène à https://drive.google.com/file/d/1MqKTUrDruyCBBxMYoCU3CH6Gh9NiZILF/view ; relu dans le PDF rendu.

## 8 octobre — catalogue caviste global

Le salon est passé : l'agence veut le catalogue caviste global (tous les vins), sur la base du
catalogue du salon. Scans relus (`data/catalogue-global-releve.md`), consignes vocales appliquées :
- troisième édition `EDITION=global` (`npm run global`) : données `scripts/prix-global.py` →
  `data/catalogue-global-2026.json` ; sorties `dist/catalogue-caviste-2026-ecran.pdf` et `-imprimeur.pdf` ;
- plus de numéros (ni stand ni tarif) : on ne parle que de pages ; sommaire plus gros ; folios
  plus gros (12 pt gras violet, craie sur les pages sombres) ; ouvertures de région et index gardés ;
- réintégrés à leur place : Sardelles (+ Les Courants en petit tableau), Beaujolais / Nugues,
  Nadine Ferrand, Pasquiers, Passion des Terroirs (label sur chaque ligne), Les Lys ;
- Trichon coupé en deux : Rhône puis nouvelle région Bugey, panachables entre eux ;
- photo de région Bugey (Commons, CC0) ; un dessin maison quand un domaine n'a pas de photo ;
- 64 pages, 39 fiches, 554 prix retrouvés dans le PDF, contrôles au vert, chaque page regardée.
- Pas encore de .pptx pour cette édition.

### 8 octobre, après-midi — catalogue caviste global, 2e passe
- Base confirmée : le catalogue du salon (le PDF renvoyé par l'agence est le nôtre, même texte).
- Couverture = celle du salon, titre « Catalogue / Vins & Terroirs », cartouche « Tarif valable
  jusqu'au 31 décembre 2026 / Offres valables du 5 octobre au 14 novembre 2026 ».
- Sommaire : la page à gauche, puis le domaine.
- Sardelles : texte d'après le site du domaine, photos du site (portrait, Sancerre rosé détouré).
- Les Lys et Château La Gorce depuis leurs tarifs annotés ; La Gorce entre l'Escarderie et Passion.
- Contrôle : les mentions propres à la couverture globale ; 64 pages, 40 fiches, 579 prix, au vert.
