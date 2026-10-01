# Propositions de compétences (« skills ») de design

Cinq compétences écrites pour ce projet, dans `.claude/skills/`. Elles sont **actives
immédiatement** : il suffit de les invoquer par leur nom, ou elles se chargent d'elles-mêmes
quand le travail les concerne. Elles sont là pour que la qualité ne dépende plus de la
mémoire d'une session.

| Compétence | Elle répond à | Quand elle se charge |
|---|---|---|
| **`da-scio`** | « Est-ce que cette page ressemble à toutes les autres ? » | Avant d'écrire une page, une feuille de style, une couverture, de choisir une couleur ou une typo |
| **`tableau-tarif`** | « Le caviste trouve-t-il son prix en deux secondes ? » | Avant de toucher à un tableau, une colonne de prix, un palier, un pied de fiche |
| **`picto-maison`** | « D'où sort cette icône, et a-t-on le droit de la dessiner ? » | Avant de créer une icône, une pastille, un symbole de label, une légende |
| **`epreuve-pages`** | « A-t-on vraiment regardé les pages ? » | Après chaque génération de PDF, avant de déclarer quoi que ce soit terminé |
| **`photos-domaines`** | « Cette image, on a le droit de l'imprimer ? » | Avant de chercher, télécharger, poser une photo, ou d'écrire dans `credits.md` |

---

## 1. `da-scio` — direction artistique

La charte, en une page lisible. Elle tient trois choses que la session a tendance à oublier
en route :

- **l'ordre qui tranche en cas de conflit** : exactitude des prix → lisibilité → joie ;
- **la liste des tics interdits**, explicitement, pour qu'on puisse se surprendre soi-même
  en train d'en écrire un ;
- **le protocole de validation** : retire un accessoire, une seule audace par page,
  regarde la page en image, relis le texte face à sa source, et dans le doute, demande.

Elle contient aussi les règles du logo (marge libre, jamais recoloré, 87 mm maximum à 300 dpi)
et les règles de la loi Évin, qui sont juridiques et ne doivent dépendre de personne.

## 2. `tableau-tarif` — le composant qui porte tout le catalogue

C'est l'objet que le caviste regarde ; tout le reste est à son service. Cette compétence fixe :

- **aucun prix tapé dans un gabarit**, jamais ; centimes entiers dans le JSON ;
- **le bloc de prix de largeur fixe divisé en parts égales** — c'est ce qui fait qu'un prix
  tombe au même endroit sur les 40 fiches, qu'il y ait un palier ou trois ;
- **les paliers ne s'harmonisent jamais** entre domaines (13 notations différentes dans la
  source, toutes légitimes) ;
- les cas particuliers qu'on écrase sans y penser : tarif unique, paliers de contenant
  (5 L / 10 L, où la dégressivité ne s'applique pas), lignes sans couleur, lignes étoilées,
  prix affichés avec « demander le tarif », dégressivité inversée.

## 3. `picto-maison` — dessiner ses signes sans copier ceux des autres

Deux interdits et une méthode.

- **Aucune bibliothèque d'icônes.**
- **Aucun logo officiel redessiné** (AB, Eurofeuille, HVE, Demeter, Biodyvin, AOP, IGP) :
  l'information qu'ils portent se reprend, leur forme non. On crée ses propres pictos et on
  les explique dans une légende. Si l'agence veut les vrais logos, c'est une démarche
  d'ayant droit, pas une décision de maquette.
- Le contrôle utile, qu'on ne fait jamais spontanément : **passer la page en niveaux de gris**
  et vérifier qu'on distingue encore rosé, rouge et doux. Le catalogue sera photocopié.

## 4. `epreuve-pages` — le contrôle que personne n'aime faire

Un PDF qui se construit sans erreur n'est pas un PDF correct. Cette compétence impose le
cycle *générer → convertir en images → regarder chaque page → corriger → recommencer*, avec
la liste des neuf défauts à traquer, et les contrôles qu'une machine fait mieux que l'œil :
polices incorporées, pages multiples de 4, fichiers sous 50 Mo, et surtout **chaque prix du
JSON retrouvé dans le texte du PDF final** (script fourni).

## 5. `photos-domaines` — ce qu'on a le droit d'imprimer

La partie du projet qui peut coûter cher si elle est faite de mémoire :

- la source principale est le **site officiel de chaque domaine** — jamais un caviste, un
  distributeur, un concurrent, ni notre propre PDF ;
- sur ces sites, **on ne prend que des photos**, aucune information ;
- **le calcul de résolution** est donné en toutes lettres (200 ppi minimum : une image posée
  sur 120 mm demande 945 px) ;
- **une ligne par photo dans `credits.md`**, avec le format exact du tableau, licence comprise.
  Une photo sans ligne ne part pas à l'impression.

---

## Ce que je n'ai pas fait, et pourquoi

- **Pas de compétence « génération du PDF »** : `npm run build` et les scripts de `scripts/`
  suffisent. Une compétence qui redit ce qu'un script fait déjà vieillit mal.
- **Pas de compétence « voix éditoriale »** tant que le concept n'est pas choisi : la voix
  du Concept 1 et celle du Concept 3 n'ont rien à voir. Elle s'écrira après votre décision,
  et elle tiendra la règle la plus importante du brief — *réécrire, oui ; ajouter un fait, jamais*.
- **Pas de compétence « loi Évin » séparée** : elle est dans `da-scio` et dans
  `photos-domaines`, c'est-à-dire aux deux endroits où on risque de l'enfreindre. Isolée,
  elle ne se serait jamais chargée au bon moment.
