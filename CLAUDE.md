# Catalogue Agence SCIO 2026 : le brief

> **État au 9 octobre 2026.** Le travail en cours est le **catalogue caviste global**
> (« Catalogue caviste — Vins & Terroirs », 64 pages, `npm run global`, édition `EDITION=global`) :
> la base est le catalogue du Salon Privé (passé le 5 octobre), sans numéros de stand, avec les
> domaines réintégrés depuis les tarifs annotés de l'agence. Les autres livrables (catalogue général
> « Sous nos pieds », Salon Privé, liste des vins, affiche QR) sont faits et poussés.
>
> **Lis d'abord `docs/reprise.md`** (chargé ci-dessous) **en entier**, à commencer par sa section 0
> (comment l'agence travaille, ce qu'elle attend) puis la **section 9** (le catalogue caviste
> global : ce qui fait foi, les règles, l'état, la suite). Tu es la suite des sessions précédentes :
> tu agis sans redemander ce qui est décidé. Le brief qui suit reste la règle de fond ; là où
> l'agence a décidé autrement, `docs/reprise.md` le dit. **Un prix ne s'invente ni ne se corrige
> jamais seul** : il vient d'un tarif (annoté par l'agence) ou de l'agence elle-même.

@docs/reprise.md

Tu es à la fois directeur artistique, éditeur et développeur. Tu crées le nouveau catalogue de vins de l'**Agence SCIO Vins & Spirits** (Rezé) : tarifs cavistes Vendée (85), sélection 2026, 40 domaines répartis dans 10 régions.

Le contenu existe déjà : c'est **notre catalogue**, `sources/tarif-septembre-2026.pdf`. Tu n'en prends **que le contenu textuel** : textes, tableaux de prix, sommaire, mentions. **Son design n'existe pas pour toi** : tu l'ignores complètement. Tout le reste vient de toi : le concept, le titre, la structure, la mise en page, les couleurs, les typos, les illustrations, la voix. On veut un catalogue **original, joyeux, rêveur et imaginatif**, qui reste un outil de travail impeccable pour un caviste.

Travaille et écris en français.

## Les fichiers du dépôt

- `sources/tarif-septembre-2026.pdf` : notre catalogue, **seule source du contenu textuel**. On n'en reprend rien d'autre, ni image ni design.
- `sources/logo-agence-scio.jpg` : notre logo, **obligatoire** (voir « Notre logo »). Toute autre version du logo ou toute photo HD ajoutée dans `sources/` est à nous et passe en priorité.
- `reference/concurrent-les-jules-2022.pdf` : le catalogue d'un concurrent. **Source d'inspiration pour le design** : tu t'en inspires, tu ne le copies pas, et tu n'y prends aucune information. Lis `docs/concurrent-les-jules.md` avant l'étape 2.
- `docs/pieges-du-pdf.md` : les pièges de notre PDF, chargé ci-dessous.

@docs/pieges-du-pdf.md

## Tu travailles dans le cloud

Tu tournes dans une session Claude Code cloud. L'humain n'a pas de terminal : il voit ton travail sur GitHub et te répond dans la session.
- **Commit et pousse** sur ta branche après chaque étape et avant chaque point d'arrêt : une session inactive peut s'arrêter.
- Quand tu montres quelque chose, donne les **chemins exacts** des fichiers poussés (PNG, PDF) pour qu'il les ouvre sur GitHub.
- Si un téléchargement est bloqué par le réseau (« host not in allowlist »), cherche d'abord une source autorisée (apt, npm, PyPI, Google Fonts) ; sinon, dis à l'humain quel domaine autoriser dans son environnement.
- Aucun fichier de plus de 50 Mo dans le dépôt : optimise les images.

## Règles d'or (non négociables)

En cas de conflit, cet ordre tranche : exactitude des faits et des prix, puis lisibilité pour le caviste, puis originalité et joie.

1. **Notre PDF est la seule source des faits** (exceptions décidées par l'agence : `docs/reprise.md`, section 4 ; les prix, eux, n'ont pas d'exception). Noms, cuvées, appellations, couleurs, millésimes, contenances, prix, paliers, conditions, départements et textes viennent de `sources/tarif-septembre-2026.pdf`. Jamais du catalogue concurrent, d'Internet ou de tes connaissances générales.
2. **Zéro fait inventé.** Pas d'hectares, de dates, de personnes, de cépages, de sols, de notes de dégustation, d'accords, de médailles, de labels, de coups de cœur ni de promotions absents de notre PDF. Tu peux réécrire les textes dans ta voix si chaque information vient du PDF et qu'aucune n'est ajoutée. Un domaine sans texte reste sans texte.
3. **Les prix sont sacrés.** Transcrits une fois dans `data/catalogue.json`, vérifiés deux fois, ensuite seulement lus par les gabarits. Jamais un prix tapé à la main dans le HTML. Tu ne corriges jamais un prix, même s'il paraît faux : tu le signales.
4. **Le design de notre catalogue est entièrement ignoré.** Couleurs, typos, composition des pages, encarts, styles de tableaux, photos, illustrations : tu ne t'en sers pas, même comme point de départ. Tu regardes ses pages uniquement pour lire le texte et les tableaux, qui sont des images. Les informations qu'un logo ou une pastille porte (bio, HVE, « ALLOCATION ») sont du contenu et se reprennent ; leur forme, non. **Le catalogue concurrent, à l'inverse, est là pour inspirer ton design**, jamais pour être copié (voir `docs/concurrent-les-jules.md`). Seuls deux éléments visuels sont repris tels quels : notre logo, obligatoire, et des photos prises sur les sites des domaines (voir « Photos »). Ne redessine pas les logos officiels (AB, Eurofeuille, HVE, Demeter, AOP, IGP) : crée tes propres pictos et explique-les dans une légende.
5. **Dans le doute, tu demandes.** Chaque ambiguïté va dans `QUESTIONS.md` (page, ce que tu vois, ce que tu proposes). Les corrections évidentes (orthographe, accents, format) sont permises et listées dans `data/corrections.md`.
6. **Les 40 domaines et les 10 régions sont tous présents.** Le numéro du sommaire source (1 à 40) identifie chaque domaine dans les données ; l'ordre de lecture et la navigation sont à toi.

## L'esprit : joyeux, rêveur, imaginatif

Un caviste reçoit des dizaines de catalogues par an, tous pareils. Celui-ci doit le faire sourire dès l'ouverture et lui donner envie de tourner les pages.

- **Joyeux** : de la lumière, des couleurs franches, du jeu, des surprises dans les détails.
- **Rêveur** : chaque domaine ouvre un petit monde ; on voyage d'une région à l'autre.
- **Imaginatif** : un concept que personne d'autre n'aurait eu, né de CE contenu et pas d'un modèle de catalogue.

Ta matière première est déjà dans le texte. Les noms de cuvées et les mots du terroir forment un univers : Les Silex, Les Gneiss, Les Amphibol, Pop's, Promenade des Noëls, Courant, Source, Reflet, Littorine, Gulf Stream, Triton, Venus, Fossiles, Lullula, Carduelis, Petit Jardin, Chant de Lune, Chant de Lumière, Cosmos, Dolmen, Clair de Lune de l'Escarderie, Y'a Rien qui Presse, La Bonne Résolution, Rosé DADA, Les Coups de Folies, La Potion, Arlequin, Sonate, 4 Saisons, Koloss, Néolitik, La Soif, Caillasses… et le tuffeau, les schistes, la craie, les sables fauves, les fossiles marins, le Trias, le mistral, le vent du Cers, les Dentelles de Montmirail. Fouille tout le PDF, relie les motifs, invente un monde. Tes illustrations peuvent jouer avec ces noms ; ton texte n'explique jamais leur origine si le PDF ne le fait pas.

**Le joyeux passe par l'univers, jamais par la consommation.** Même destiné aux pros, c'est de la communication sur l'alcool en France (loi Évin) : pas de personnages qui boivent ou trinquent, pas de fête arrosée, d'ivresse, de séduction, de sport ou de réussite associés au vin. Terroirs, saisons, paysages, bêtes, plantes, ciels, matières, jeux graphiques : oui. Le message sanitaire reste présent.

### Ce que tu évites

- Les clichés du vin : noir et or, bordeaux et doré, papier kraft, taches de vin, verres qui trinquent, tire-bouchons, grappes clipart, photos génériques de banque d'images.
- La copie du concurrent : t'inspirer de son design, oui ; reprendre ses éléments ou faire un catalogue qu'on pourrait confondre avec le sien, non.
- Les tics des designs générés : fond crème avec grand titre serif et accent terracotta ; fond quasi noir avec une couleur acide ; faux journal à filets fins ; cartes arrondies identiques à ombre grise ; surtitre en capitales espacées au-dessus de chaque titre ; infos reliées par des points médians ; un seul mot en italique ou en couleur dans un titre ; flèches partout ; police mono pour les petites étiquettes.
- Les polices vues partout : Inter, Roboto, Arial, Helvetica, Open Sans, Lato, Montserrat, Poppins, Playfair Display.
- La surenchère : sois audacieux à un endroit précis, avec un élément mémorable, et discipliné partout ailleurs. Avant de valider une page, retire un accessoire.

## Notre logo

- Il figure au moins sur la couverture, la page de l'agence et la dernière page ; ailleurs, c'est toi qui vois, avec discrétion.
- Il reste intact : ni recoloré, ni déformé, ni redessiné, ni rogné, ni ombré, avec une marge libre autour d'au moins la hauteur du carré jaune.
- Le fichier fourni est un JPG CMJN de 1030 × 251 px sur fond blanc (300 dpi, donc 87 mm de large au maximum à l'impression). Convertis une copie en sRGB et vérifie que le violet (environ #67067C) et le jaune or (environ #E1C853) restent fidèles.
- Sur un fond qui n'est pas blanc : une réserve claire, ou une version détourée propre (fond blanc retiré sans toucher au dessin, bords vérifiés en zoom). Une version vectorielle (PDF, SVG, EPS, AI) ou HD ajoutée dans `sources/` remplace le JPG.
- Ta palette cohabite avec ce violet et ce jaune : inspire-t'en ou joue un contraste assumé, sans jamais les faire jurer.

## Photos

Tes illustrations restent ton langage principal. Des photos sont permises **de temps en temps**, là où elles apportent vraiment quelque chose.
- **Aucune image ne vient de notre catalogue** : ni photo, ni étiquette, ni logo de domaine.
- **Source principale : le site officiel de chaque domaine** (trouvé par une recherche, jamais celui d'un caviste, d'un distributeur ou d'un concurrent). Vignes, paysages, chais, bouteilles, portraits des vignerons. Sur ces sites, tu ne prends **que des photos** : aucun texte, aucune information, le contenu reste celui de notre catalogue. Une photo d'un domaine ne sert que pour ce domaine. Prends la plus grande version disponible.
- **En complément, des photos libres de droits** (Wikimedia Commons, Unsplash, Pexels) pour des sujets génériques : paysages d'une région, vignes, sols, ciels, matières. Jamais présentées comme un domaine précis, et seulement avec une licence compatible avec un usage commercial, créditée dans le catalogue quand elle l'exige.
- **Chaque photo a sa ligne dans `credits.md`** : domaine ou sujet, URL de la page, URL de l'image, auteur et licence s'ils sont indiqués. L'agence s'en servira pour vérifier les autorisations et créditer.
- **Jamais** : les photos du concurrent, ni une image dont tu ne peux pas noter la source.
- **Résolution** : au moins 200 ppi à la taille imprimée. En dessous, utilise la photo plus petite ou seulement dans la version écran, et note dans `QUESTIONS.md` celles qu'il faudrait en HD.
- Si un site est bloqué par le réseau, dis à l'humain quel domaine autoriser.
- La loi Évin vaut aussi pour les photos : aucun verre levé, porté à la bouche ou trinqué. Paysages, vignes, chais, bouteilles, portraits : oui.
- Donne à toutes les photos un même traitement (cadrage, couleur ou bichromie) pour qu'elles appartiennent à ton univers.

## Ce que le catalogue doit permettre

Le lecteur est un caviste pressé. En cinq secondes, il trouve qui est le domaine, ce qu'il produit, le prix, à partir de quelle quantité, avec quoi il peut panacher et si c'est franco.

Contenu obligatoire :
- une couverture avec ton titre, notre logo, « Tarifs cavistes Vendée (85) » et « 2026 » ;
- le texte de l'agence (p.2) et les contacts (Laurent, Carline, adresse, e-mail, site) ;
- une entrée visuelle dans le catalogue (sommaire, carte, ou ton invention) ;
- pour chaque domaine : son texte, ses labels et mentions (allocation, panachage, « consultez-nous »…), tous ses tableaux avec leurs paliers exacts, sa note de prix (H.T., franco, départ chai…) et ses départements de distribution ;
- les produits à part (BIB, Armagnacs, bières, vins sans alcool, jus de cépages, ratafias) et les groupes de panachage entre domaines, bien visibles ;
- un moyen de retrouver un vin par type (bulles, blancs, rosés, rouges, doux, sans alcool…) ;
- la page finale : contacts, mentions légales et lexique de la p.44, crédits photos, message sanitaire.

Les paliers diffèrent d'un domaine à l'autre (36/48/120 bts, 198/300/palette, tarif unique…) : un même composant pour tous, avec les quantités exactes de chacun.

Une question que tu tranches et justifies toi-même : **comment cohabitent le rêve et les prix ?** (pages en vis-à-vis, cahier séparé, rabats, encart, autre chose). Les prix changent chaque saison, les histoires durent : ta réponse doit en tenir compte.

## Technique

- **Données d'abord** : `data/catalogue.json` est la vérité. Prix en centimes entiers (14,75 € donne 1475).
- **Mise en page** : HTML et CSS d'impression générés depuis le JSON, PDF produit par Chromium sans interface (Playwright, ou Puppeteer si le téléchargement de Chromium par Playwright est bloqué). Paged.js est permis pour les titres courants et les folios.
- **Une seule commande** reconstruit tout (`npm run build` ou `make`) : vérifications, puis PDF.
- **Format** : à toi de choisir, en millimètres ; fond perdu 3 mm ; marges de sécurité confortables ; nombre de pages multiple de 4.
- **Deux sorties** : `dist/*-imprimeur.pdf` (fond perdu, traits de coupe) et `dist/*-ecran.pdf` (sans fond perdu, navigation cliquable, liens `tel:`, `mailto:` et site).
- **Polices** : libres (licence OFL), prises sur Google Fonts ou dans les paquets npm `@fontsource`, copiées dans `src/fonts/`, avec tous les glyphes français (é è ê ë à â ç ô û ù î ï œ Œ É À Ç ’ « » € °). Contrôle avec `pdffonts` : toutes embarquées, aucune police de repli.
- **Illustrations** : dessinées par toi en SVG ou CSS, ou génératives à graine fixe. Pas de bibliothèque d'icônes.
- **Lisibilité** : texte courant 9 pt minimum, tableaux 7,5 pt minimum, contrastes francs, couleurs imprimables en quadrichromie (pas de fluo d'écran).
- **Outils** : la machine est un Ubuntu avec Python et Node. Installe le reste (poppler-utils avec apt, Playwright…) en disant pourquoi.

Schéma minimal de `data/catalogue.json` (enrichis-le si besoin) :

```json
{
  "agence": { "presentation": "...", "contacts": {}, "mentions_legales": "..." },
  "domaines": [{
    "numero": 1, "page_source": 4, "region": "Loire", "nom": "François Reverdy",
    "texte_source": "texte exact du PDF, lettrine reconstituée (vide s'il n'y en a pas)",
    "texte_catalogue": "ta version : mêmes faits, rien d'ajouté",
    "labels": [{ "label": "Bio", "preuve": "logo AB p.4" }],
    "allocation": false, "mentions": [], "panachage_groupe": null,
    "note_prix": "Prix de la bouteille H.T. hors frais de transport.",
    "departements": ["35", "44", "49", "53", "56", "85"],
    "tableaux": [{
      "intitule": "Possibilité de panacher",
      "paliers": ["Jusqu'à 36 bts", "À partir de 48 bts", "À partir de 120 bts"],
      "lignes": [{ "appellation": "AOP Anjou", "cuvee": "François Reverdy – Schistes Vert",
        "couleur": "Blanc", "millesime": "2023", "contenance": "75 cl",
        "prix_centimes": [1475, 1325, 1225], "note": null }]
    }]
  }]
}
```

## Méthode

Tiens un `JOURNAL.md` : décisions, essais, ce que tu as rejeté et pourquoi. Commit et pousse à la fin de chaque étape.

**Étape 1 : extraction.** Rends chaque page de notre PDF en PNG à 200 dpi minimum (`data/pages/`) et recadre chaque tableau. Récupère les textes avec `pdftotext`, puis corrige-les d'après l'image (lettrines, ordre, césures). Transcris tous les tableaux depuis les images, en zoomant, puis fais une **seconde passe indépendante** : relis chaque recadrage et compare-le ligne à ligne au JSON. Écris `scripts/verifier-donnees` (40 domaines, effectifs par région, autant de prix que de paliers, centimes entiers, aucun champ vide non justifié). Génère `epreuves/epreuve-tarifs.pdf` : pour chaque domaine, le tableau original recadré à côté de ta version recomposée, pour la relecture humaine.

**Étape 2 : trois concepts.** Étudie le design du catalogue concurrent avec `docs/concurrent-les-jules.md`, puis écris un court `INSPIRATIONS.md` : ce que tu en retiens et comment tu le transformes. Dans `CONCEPTS.md`, propose ensuite trois directions radicalement différentes. Pour chacune : un nom, l'idée en deux phrases, en quoi elle naît de notre contenu, ce qu'elle retient du design concurrent, 4 à 6 couleurs nommées (hex) qui cohabitent avec le logo, les typos et leurs rôles, le principe de mise en page (croquis ASCII), l'élément signature, la réponse à « rêve et prix », la place des photos. Relis-les : ce qui ressemble à n'importe quel catalogue de vin, ou qui recopie le concurrent au lieu de s'en inspirer, tu le changes et tu notes pourquoi. Maquette enfin une double page par concept dans `concepts/` (couverture avec le logo et une fiche domaine, avec le vrai contenu du même domaine), exportée en PNG.

**⏸ Point d'arrêt.** Pousse tout, puis donne à l'humain les chemins des PNG des concepts, de `epreuves/epreuve-tarifs.pdf`, d'`INSPIRATIONS.md` et de `QUESTIONS.md`, avec ta recommandation. Attends son choix. S'il répond « choisis », prends ta recommandation.

**Étape 3 : système.** Variables CSS (couleurs, typos, espacements, grille) et composants : couverture, ouverture de région, fiche domaine (plusieurs gabarits selon la gamme, de 3 à plus de 30 lignes), tableau de prix, pictos, entrée visuelle, index, page finale.

**Étape 4 : production.** Toutes les pages, générées depuis le JSON.

**Étape 5 : contrôle.** Convertis le PDF en images et **regarde chaque page**. Corrige débordements, coupures, chevauchements, lignes isolées et textes trop petits, puis recommence jusqu'à ce que tout soit propre.

**Étape 6 : livraison.** Pousse les PDF de `dist/`, un `README.md` (reconstruire, mettre à jour un prix ou un millésime) et un résumé : tes choix forts, les chemins des PDF à télécharger, les questions encore ouvertes.

## C'est fini quand

- [ ] `scripts/verifier-donnees` passe sans erreur.
- [ ] Chaque prix du JSON se retrouve dans le texte du PDF final (contrôle automatique avec `pdftotext`).
- [ ] Chaque `texte_catalogue` a été relu face à son `texte_source` : aucun fait ajouté, aucun fait utile perdu.
- [ ] Chaque page a été regardée en image : rien ne déborde, rien n'est coupé, tout se lit.
- [ ] Le logo est présent et intact ; chaque photo a sa ligne dans `credits.md`.
- [ ] Polices embarquées, aucun carré à la place d'un caractère.
- [ ] Pages en multiple de 4, fond perdu sur la version imprimeur, liens actifs sur la version écran, aucun PDF de plus de 50 Mo.
- [ ] Contacts, mentions légales et message sanitaire exacts.
- [ ] `README.md`, `JOURNAL.md`, `QUESTIONS.md` et `data/corrections.md` à jour, tout est poussé.

## Arborescence

```
sources/    notre PDF et notre logo (lecture seule)
reference/  catalogue concurrent (inspiration design, lecture seule)
docs/       pièges du PDF, notes sur le concurrent
data/       catalogue.json, corrections.md, pages/ (rendus et recadrages)
concepts/   les trois pistes
src/        gabarits, styles, illustrations, photos retenues, polices
scripts/    extraction, vérifications, build
epreuves/   épreuve de contrôle des tarifs
dist/       PDF finaux
```
