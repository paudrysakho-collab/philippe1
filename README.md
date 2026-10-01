# Catalogue Agence SCIO — édition 2026

Tarifs cavistes Vendée (85). 40 domaines, 10 régions.
Construit depuis `data/catalogue.json`, qui est la **seule vérité** du projet.

## Où en est le projet

**Terminé.** Concept retenu : **« Sous nos pieds »**. **76 pages**, 210 × 260 mm.
Chaque fiche domaine réserve **deux emplacements d'image vides** — un rond de 40 mm pour le
vigneron ou le logo, une bande de 24 × 62 mm pour la bouteille — que l'agence remplit
elle-même dans Canva.

| Livrable | Où |
|---|---|
| **Fichier Canva** (76 diapositives, textes et tableaux modifiables) | `dist/catalogue-scio-2026-canva.pptx` |
| **Les polices à téléverser dans Canva**, avec leur mode d'emploi | `polices-canva/` |
| **Prompt pour faire poser les images par Cowork** | `PROMPT-COWORK.md` |
| Où sont les deux emplacements d'image, diapositive par diapositive | `docs/emplacements-images.md` |
| **Catalogue, version imprimeur** (fond perdu 3 mm, traits de coupe) | `dist/catalogue-scio-2026-imprimeur.pdf` |
| **Catalogue, version écran** (navigation cliquable, liens `tel:`, `mailto:`, site) | `dist/catalogue-scio-2026-ecran.pdf` |
| Données des 40 domaines, vérifiées | `data/catalogue.json` |
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

**Ne jamais écrire un prix ailleurs que dans `data/fiches/`.** Les gabarits ne font que lire,
et le contrôle vérifie que les 715 prix du JSON se retrouvent dans le texte des deux PDF
**et** dans celui des diapositives.

## Ajouter ou retirer un domaine

Ajouter `data/fiches/NN.json` sur le modèle des existants, puis ajuster le relevé d'effectifs
en tête de `scripts/verifier-donnees` (`ATTENDU`), qui est volontairement codé en dur : il
sert de garde-fou contre une perte silencieuse de domaine.

## Le catalogue, page par page

| Pages | Contenu |
|---|---|
| 1 | Couverture |
| 2 | L'agence, ses contacts |
| 3 | Comment lire ce catalogue (la tranche, le bloc de prix, les pictos, les mentions, les paliers, le pied de page) |
| 4 | **La coupe** — sommaire des dix régions |
| 5 | **Les quatre alliances** — ce qui se panache entre domaines |
| 6 – 67 | Les dix régions : une ouverture pleine page, puis ses domaines |
| 68 – 70 | Index des vins par type, de A à Z |
| 71 | Les produits à part : bag-in-box, sans alcool, jus de cépages, bières, armagnacs, ratafias |
| 72 | Les quarante domaines, de A à Z |
| 73 – 74 | Vos notes |
| 75 | Planche : la coupe pleine page |
| 76 | Contacts, lexique, mentions légales, crédits, message sanitaire |

*(La pagination est recalculée à chaque fabrication ; `build/plan.json` donne la page de
chaque domaine. Les pages 73 à 75 existent pour tomber sur un multiple de 4.)*

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
