# Trois directions pour le catalogue 2026

Même contenu, même exigence de clarté, trois mondes qui n'ont rien à voir.
Chacun est né d'une matière déjà présente dans `sources/tarif-septembre-2026.pdf`,
et chacun répond à sa façon à la question posée par le brief :
**comment le rêve et les prix cohabitent-ils ?**

Format commun aux trois : **210 × 260 mm**, à l'italienne du A4 — un peu plus large et plus
court, assez inhabituel pour qu'on le remarque sur une pile, assez proche du A4 pour
n'inquiéter aucun imprimeur. Fond perdu 3 mm. Nombre de pages multiple de 4.

---

## Concept 1 — « SOUS NOS PIEDS »

### L'idée en deux phrases
Le catalogue se lit comme une coupe géologique : on descend d'une région à l'autre comme on
descend dans les couches d'un sol. Chaque région est une strate, avec sa couleur, sa matière
dessinée et son épaisseur, et le caviste se repère au doigt sur la tranche avant même d'ouvrir.

### Ce qui, dans notre contenu, le fait naître
Les vignerons de cette sélection nomment leurs cuvées d'après ce qu'ils ont sous les pieds.
**Les Silex**, **Les Gneiss**, **Les Amphibol** (Barbinière), **Tuffeau** et **Schistes Vert**
et **Graves Argileuses** (Reverdy), **Marnes Kimméridgiennes** et **Silex** (Villebois),
**Caillasses** (Les Lys), **Dolmen** et **Néolitik** (Gragnos, Stratéus), **Fossiles** et
**Littorine** (Haut Marin). Et les textes continuent : *coteaux argilo-schisteux*,
*sables fauves riches en fossiles marins*, *la formation géologique du Trias*,
*la craie révèle toute la finesse du cépage*, *coteaux argilo-calcaires*, *sols de sable*,
*vignes plantées en terrasses*, *une ancienne cave de village à demi enterrée*,
*élevage en amphores*, *perchée à 120 mètres au-dessus de la vallée de la Dordogne*.
Le sol est le seul sujet que les quarante domaines ont en commun. Il devient la structure.

### Ce qu'il retient du concurrent
Leur tenue : une matière unique du début à la fin. Leur ligne d'identité sous le nom du
domaine. Leur bloc de prix détaché. Rien de leur forme : pas de carte de France, pas de rond,
pas d'encre grattée.

### Couleurs — sept strates qui cohabitent avec le logo
| Nom | Hex | Rôle |
|---|---|---|
| Tuffeau | `#F2EADA` | le papier de tout le catalogue |
| Craie | `#FBF8F1` | les fonds de tableau, un ton au-dessus |
| Silex | `#46606E` | le bleu-gris de la Loire et du texte courant |
| Gneiss | `#A8515F` | le rouge sourd du Beaujolais et de la Bourgogne |
| Amphibolite | `#3C5B47` | le vert profond du Rhône et du Languedoc |
| Sables fauves | `#D08C3C` | l'ocre du Sud-Ouest et de la Provence |
| Violet SCIO | `#67067C` | **la couleur de l'agence** : numéros de domaine, index, titres de section |
| Or SCIO | `#E1C853` | le repère de la strate active sur la tranche |

Le violet et l'or du logo ne sont pas décoratifs : ce sont les deux seules couleurs qui
traversent toutes les strates. Les six autres sont des couleurs de terre, franches mais
imprimables sans difficulté en quadrichromie.

### Typographies (toutes OFL)
- **Young Serif** — titres, nom du domaine, ouvertures de région. Une antique à empattements
  épais et un peu rustique, taillée dans la masse : exactement le registre « roche ».
- **Spectral** — textes de présentation, 9,5 pt. Un sérif d'écran devenu excellent sur papier,
  très lisible en petites tailles.
- **IBM Plex Sans** — tableaux, paliers, légendes, 7,5 pt minimum. Chiffres tabulaires
  (`font-variant-numeric: tabular-nums`) : les prix s'alignent à la virgule, colonne par colonne.

### Le principe de mise en page
```
┌────────────────────────────────────────────────┬──┐
│  ③ CHÂTEAU LA GORCE                 Bordeaux  │▓▓│ ← tranche indexée :
│  ──────────────────────────────────────────    │░░│   dix strates empilées,
│                                                │░░│   celle de la région
│   ╭──────────╮   En activité depuis 1822,      │██│   est pleine + un repère
│   │ dessin   │   reconnu cru bourgeois dans    │░░│   or. On la trouve au
│   │ du sol : │   le classement de 1932, le     │░░│   doigt, catalogue fermé.
│   │ argile + │   domaine a été repris en       │░░│
│   │ graves   │   2018 par Emmanuel et Mana…    │░░│
│   ╰──────────╯                                 │░░│
│                                                │░░│
│  ┌──────────────────────────┬────┬────┬────┐   │░░│
│  │ AOP Médoc Cru Bourgeois  │7,05│7,00│6,90│   │░░│ ← bloc de prix de largeur
│  │ Château la Gorce  ● 2019 │ €  │ €  │ €  │   │░░│   FIXE (52 mm), divisé en
│  ├──────────────────────────┼────┼────┼────┤   │░░│   autant de parts qu'il y
│  │ …                        │    │    │    │   │░░│   a de paliers
│  └──────────────────────────┴────┴────┴────┘   │░░│
│  * Prix H.T. franco de port · 35 44 49 53 56 85│░░│
└────────────────────────────────────────────────┴──┘
```

### L'élément signature — **la carotte**
Une bande verticale de 9 mm court sur le bord extérieur de **chaque page**. Elle montre les
dix régions empilées comme les dix couches d'une carotte de sondage, chacune avec sa couleur
et sa trame dessinée (points pour les sables, écailles pour les schistes, veines pour le
gneiss, pointillé pour la craie). La strate de la région où l'on se trouve est pleine ;
les autres sont en réserve. Catalogue fermé, la tranche affiche les dix bandes : **on ouvre
directement à la bonne région sans passer par le sommaire.** C'est la seule chose qui se voie
avant d'ouvrir, et personne d'autre ne l'a.

### Rêve et prix — **le cahier détachable**
Les histoires durent, les prix changent chaque saison. Alors on les sépare physiquement :
les **pages de monde** (couverture, agence, entrée visuelle, dix ouvertures de région,
quarante portraits de domaine) forment le corps du livre ; les **pages de tarif** forment un
**cahier central**, imprimé sur un papier plus mince et légèrement plus étroit (3 mm de moins),
que l'on repère au toucher et que l'on réimprime seul à chaque saison sans retoucher le reste.
Le renvoi se fait par le numéro du domaine, qui est le même des deux côtés.
*Si vous préférez une brochure d'un seul tenant, la même maquette fonctionne en vis-à-vis :
monde à gauche, tarif à droite. Le cahier détachable est ma recommandation ; c'est votre
décision, et elle n'engage pas le reste du concept.*

### La place des photos
Rares et toujours au même sujet : **la matière**. Gros plans de sol, de roche, de craie, de
muret, d'amphore, de cave. Traitées en **bichromie Silex + Tuffeau**, elles ne cherchent jamais
à être jolies : elles documentent. Trois à cinq par région au maximum, jamais de portrait
souriant, jamais de bouteille sur fond flou. Les illustrations dessinées restent le langage
principal.

---

## Concept 2 — « LE CHANT DES LUNES »

### L'idée en deux phrases
Cette sélection est pleine de noms qui regardent en l'air et qui chantent : on en fait un
catalogue nocturne, où chaque région est un morceau de ciel et chaque domaine une petite
figure d'étoiles. Une ligne d'horizon traverse toutes les pages : au-dessus le monde, en
dessous le tarif, toujours à la même hauteur.

### Ce qui, dans notre contenu, le fait naître
**Chant de Lune**, **Chant Libre**, **Chant de Lumière** (Famille d'Exea, trois cuvées
voisines), **Clair de Lune de l'Escarderie**, **Cosmos** (Gragnos), **Venus** et
**Gulf Stream** et **Triton** et **Littorine** (Haut Marin, une gamme entière de noms de mer
et de ciel), **Sonate**, **Tempo**, **4 Saisons**, **Arlequin** (Sainte-Marie d'Albas),
**Pop's**, **Rosé DADA**, **Les Coups de Folies**, **La Potion**, **Y'a Rien qui Presse**.
Et les deux oiseaux cachés dans la gamme d'Exea : **Lullula**, qui est l'alouette lulu, et
**Carduelis**, qui est le chardonneret. Les textes font le reste : *bercé par le mistral*,
*balayées par le vent du Cers*, *au pied des Dentelles de Montmirail*, *à 300 mètres
d'altitude, la température est plus fraîche*, *une lumineuse franchise de terroir*,
*la vibrante énergie de sol*, *appréciés à tout moment de la journée ou de la nuit*.

### Ce qu'il retient du concurrent
Le jeu d'échelle sur un même signe (ils le font avec leur nom de marque, nous avec la figure
du domaine : minuscule dans l'index, grande en ouverture de région). Et la discipline de leur
colonne de prix.

### Couleurs
| Nom | Hex | Rôle |
|---|---|---|
| Nuit de craie | `#232B52` | l'indigo profond du ciel — **jamais un noir** |
| Lune | `#F4EEE0` | le papier crème, chaud |
| Cers | `#6E8E6A` | le vert du vent, pour les ouvertures du Languedoc et du Rhône |
| Arlequin | `#D1537C` | le rose vif des pointes et des pictos |
| Aube | `#E2884A` | l'orange des levers, pour le Sud-Ouest et la Provence |
| Violet SCIO | `#67067C` | **la couleur de l'agence**, qui fait le lien entre la nuit et le rose |
| Or SCIO | `#E1C853` | les étoiles et les repères de palier |

> **Relecture.** Mon premier jet posait un fond quasi noir avec une seule couleur acide : c'est
> exactement le tic que le brief interdit, et on l'a vu cent fois. J'ai changé deux choses.
> Le fond n'est pas noir mais un **indigo franc** (`#232B52`), qui est une couleur, pas une
> absence. Et il ne reçoit pas un accent acide mais **quatre couleurs chaudes** — or, rose,
> orange, vert — qui se répondent. Par ailleurs l'indigo ne couvre pas tout : il est réservé
> aux ouvertures de région et au bandeau d'horizon. **Les pages de domaine sont claires**,
> sur le crème « Lune », pour que les tableaux restent lisibles à l'impression et que le
> catalogue ne pèse pas deux kilos d'encre.

### Typographies (toutes OFL)
- **Fraunces** — titres et nom du domaine. Une variable dont les axes *SOFT* et *WONK*
  permettent des formes douces et légèrement de travers : le rêve sans la mièvrerie.
- **Faustina** — textes de présentation, 9,5 pt. Un sérif chaleureux, large d'œil, qui tient
  très bien les petites tailles.
- **Archivo** — tableaux et paliers, 7,5 pt minimum, chiffres tabulaires.

### Le principe de mise en page
```
┌──────────────────────────────────────────────┐
│          ·  ✦   ·        ·      ✦            │ ← le ciel du domaine :
│      ✦         ╱╲    ·         ·             │   onze points, un par
│   ·      ·    ╱  ╲ ✦                         │   référence au tarif.
│        ✦ ────╱────╲──── ·    ✦               │   Rien d'inventé : on
│                                              │   compte les lignes.
│   ③ CHÂTEAU LA GORCE              Bordeaux   │
│   En activité depuis 1822, reconnu cru       │
│   bourgeois dans le classement de 1932…      │
│                                              │
│ ═══════════════ ligne d'horizon ════════════ │ ← toujours à 148 mm du
│                                              │   haut, sur toutes les
│  AOP Médoc Cru Bourgeois   │7,05│7,00│6,90│  │   pages du catalogue
│  Château la Gorce  ● 2019  │ €  │ €  │ €  │  │
│  AOP Médoc – Série limitée │5,55│5,50│5,40│  │
│  Préface           ● 2013  │ €  │ €  │ €  │  │
│  …                                           │
│  * Prix H.T. franco de port · 35 44 49 53 …  │
└──────────────────────────────────────────────┘
```

### L'élément signature — **la figure du domaine**
Chaque domaine reçoit **une figure d'étoiles tracée à la main, comportant exactement autant
de points qu'il a de références au tarif** : huit pour François Reverdy, onze pour Château la
Gorce, trente-et-un pour La Passion des Terroirs, vingt-trois pour la Maison Goichot. La
figure est générée à graine fixe à partir du numéro du domaine, puis reliée par des traits
fins : elle est différente pour chacun, reproductible d'une édition à l'autre, et elle **dit
une vérité utile** — la taille de la gamme — avant même qu'on lise le tableau. On la retrouve
en petit dans l'index, en grand sur la page du domaine, et toutes ensemble sur l'entrée
visuelle du catalogue, qui devient une carte du ciel des quarante domaines.

### Rêve et prix — **la ligne d'horizon**
Un filet horizontal traverse **toutes les pages à la même hauteur**. Au-dessus : le ciel, la
figure, le texte, le monde. En dessous : le tarif, posé au sol, sur un fond clair uni, dans
sa grille stricte. Le lecteur pressé ne regarde jamais qu'en dessous de la ligne et trouve son
prix au même endroit sur les quarante fiches ; le lecteur curieux lève les yeux. Les prix
changent chaque saison : ils occupent une bande continue et homogène, facile à régénérer sans
toucher à ce qui est au-dessus.

### La place des photos
Une seule par région, en **bandeau de 50 mm à fond perdu** en haut de l'ouverture de région :
un paysage, un ciel, un relief. Traitée en **duotone Nuit de craie + Lune**, ce qui l'absorbe
dans le ciel. Sur les pages de domaine, **aucune photo** : la figure d'étoiles et le texte
suffisent. Dix photos pour tout le catalogue, donc dix autorisations à obtenir, pas quarante.

---

## Concept 3 — « LA CAISSE PANACHÉE »

### L'idée en deux phrases
Ce tarif n'est pas une liste, c'est un jeu de combinaisons : presque chaque tableau s'ouvre
sur « Possibilité de panacher », et quatre groupes de domaines se panachent entre eux. On en
fait le principe graphique du catalogue entier — une caisse de douze cases que l'on remplit,
page après page, de vins, d'images et de couleurs.

### Ce qui, dans notre contenu, le fait naître
« Possibilité de panacher » est la **mention la plus répétée du document** : elle est en tête
de presque tous les tableaux. Quatre groupes se panachent entre domaines — Villebois avec
Divin No Low ; Goichot, le Château du Cray et Les Guignottes ; les quatre domaines Strasser
Radziwill ; les vins et les jus de cépages de la Famille d'Exea. Les paliers eux-mêmes sont
des multiples de caisses : 36, 48, 60, 72, 78, 90, 96, 120, 126, 144, 180, 186, 198, 240, 300,
320, 360, 600, et la palette. Et les noms vont avec le jeu : **Arlequin**, **Pop's**,
**Rosé DADA**, **Les Coups de Folies**, **Petit Jardin**, **La Potion**, **Cosmos**,
**4 Saisons**, **Y'a Rien qui Presse**, **La Bonne Résolution**, **Préface**, **Prétexte**.

### Ce qu'il retient du concurrent
La pastille de couleur par type de vin — indispensable — et la rigueur de leur colonne de prix.
Rien d'autre : c'est le concept le plus éloigné des Jules, et c'est voulu.

### Couleurs — six couleurs de case, franches
| Nom | Hex | Rôle |
|---|---|---|
| Caisse | `#F7F1E4` | le papier, un blanc cassé chaud |
| Encre | `#211E1C` | le texte courant |
| Violet SCIO | `#67067C` | **la couleur de l'agence** : structure, titres, numéros |
| Or SCIO | `#E1C853` | les cases de bulles et de doux, les repères de palier |
| Courant | `#2E6E9E` | le bleu des blancs (d'après la cuvée « Courant », Berteaud Manceau) |
| Petit Jardin | `#4C8A57` | le vert des sans-alcool et des jus (d'après la cuvée d'Exea) |
| Coups de Folies | `#C24030` | le rouge des rouges (d'après la cuvée du Domaine des Nugues) |
| Arlequin | `#DE6E95` | le rose des rosés (d'après la cuvée de Sainte-Marie d'Albas) |

Chaque couleur porte le nom d'une cuvée de la sélection. Le violet et l'or de l'agence sont
deux des huit : ils ne sont pas plaqués, ils font partie du jeu.

### Typographies (toutes OFL)
- **Bricolage Grotesque** — titres, numéros, nom du domaine. Une variable contemporaine,
  un peu dégingandée, avec un axe optique : elle est joyeuse sans être enfantine.
- **Literata** — textes de présentation, 9,5 pt. Un sérif dessiné pour la lecture longue.
- **Hanken Grotesk** — tableaux et paliers, 7,5 pt minimum, chiffres tabulaires.

### Le principe de mise en page
```
┌───────────────────────────────────────────────┐
│ ┌────┬────┬────┬────┬────┬────┐    ③          │ ← la caisse : 6 × 2 cases.
│ ├────┼────┼────┼────┼────┼────┤  CHÂTEAU      │   Ici elle sert de portrait
│ └────┴────┴────┴────┴────┴────┘  LA GORCE     │   du domaine : une case par
│   11 références · Bordeaux · Bio               │   couleur de vin, remplie à
│                                                │   proportion de la gamme,
│  En activité depuis 1822, reconnu cru          │   plus une case d'image et
│  bourgeois dans le classement de 1932…         │   une case de label.
│                                                │
│  ╔═══════════════════════════╤════╤════╤════╗  │
│  ║ ■ AOP Médoc Cru Bourgeois │7,05│7,00│6,90║  │ ← ■ = la case de couleur
│  ║   Château la Gorce   2019 │ €  │ €  │ €  ║  │   du vin, reprise de la
│  ╟───────────────────────────┼────┼────┼────╢  │   caisse du haut
│  ║ ■ AOP Médoc – Série lim.  │5,55│5,50│5,40║  │
│  ║   Préface            2013 │ €  │ €  │ €  ║  │
│  ╚═══════════════════════════╧════╧════╧════╝  │
│  ┌──────────────────────────────────────────┐  │
│  │ PANACHER : toute la gamme, dès 90 bts    │  │ ← la bande de panachage,
│  └──────────────────────────────────────────┘  │   toujours en pied
└───────────────────────────────────────────────┘
```

### L'élément signature — **la caisse de douze**
Une grille de 6 × 2 cases, aux proportions d'une caisse de douze bouteilles, est le module
unique du catalogue. **La couverture** est une caisse de douze cases illustrées, une par
région plus deux. **L'entrée visuelle** est une caisse dont chaque case mène à une région.
**Chaque domaine** a sa petite caisse, remplie des couleurs de sa gamme dans leurs proportions
réelles — un coup d'œil dit « ici, surtout du rouge », « ici, que du blanc ». **Les quatre
groupes de panachage** ont leur double page : une grande caisse où les domaines partagent les
cases, ce qui montre d'un seul regard ce qu'on a le droit de mélanger. Le même objet, cinq
échelles.

### Rêve et prix — **tout dans la case**
Pas de séparation : c'est le pari de ce concept. Le rêve est **dans la grille elle-même** —
les cases illustrées, les couleurs qui portent des noms de cuvées, les proportions qui
dessinent un portrait. Le prix est **dans la case du vin**, à sa place, lisible. Ce qui change
chaque saison, ce sont les montants, et ils occupent trois colonnes de largeur fixe en bout de
ligne : une régénération ne déplace jamais rien d'autre. C'est la réponse la plus économique
des trois à l'impression, et celle qui demande le moins de pages.

### La place des photos
Dans les cases, et uniquement là : **carrées, pleine case**, jamais détourées, jamais en fond
perdu. Une à trois par domaine au maximum, en couleur mais avec **un même étalonnage chaud**
(hautes lumières crème, ombres chaudes) pour qu'elles appartiennent à la caisse. Une case
photo a exactement le même poids qu'une case de couleur : la photo devient un élément du jeu,
pas une illustration qui vient se poser dessus.

---

## Ma recommandation : **Concept 1, « Sous nos pieds »**

Trois raisons, dans l'ordre.

**1. C'est celui qui naît le plus directement du contenu, et le contenu est notre seul
avantage sur le concurrent.** Le sol est le point commun des quarante domaines : il est dans
les noms de cuvées, dans les textes, dans les appellations. Un caviste qui lit « Les Gneiss »
en face d'un dessin de gneiss comprend le domaine en une seconde — et nous n'avons rien
inventé pour cela.

**2. La carotte en tranche est une vraie fonction, pas un ornement.** Dix régions repérables
au doigt, catalogue fermé : c'est le seul des trois éléments signature qui fait gagner du
temps à un caviste pressé, et c'est le seul qu'on remarque sur une pile de catalogues avant
même d'ouvrir.

**3. Le cahier de tarifs détachable répond vraiment à la question posée.** Les prix changent
chaque saison, les histoires durent. Séparer les deux physiquement coûte une page de plus et
économise une réimpression complète chaque année.

**Ce que je perds en le choisissant :** c'est le plus sage des trois. « Le Chant des Lunes »
est plus beau à feuilleter et sa figure du domaine est l'idée dont je suis le plus content ;
« La Caisse Panachée » est le plus joyeux, le moins cher à imprimer et le plus immédiatement
utile sur le panachage, qui est la vraie mécanique de ce tarif.

**Si vous hésitez, un mot suffit :**
- vous voulez **le plus singulier et le plus utile au quotidien** → Concept 1 ;
- vous voulez **le plus beau, celui qu'on garde sur le comptoir** → Concept 2 ;
- vous voulez **le plus joyeux et le plus économique** → Concept 3.

Et si vous répondez « choisis », je pars sur le Concept 1.
