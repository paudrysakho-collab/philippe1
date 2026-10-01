# Catalogue Agence SCIO — édition 2026

Tarifs cavistes Vendée (85). 40 domaines, 10 régions.
Construit depuis `data/catalogue.json`, qui est la **seule vérité** du projet.

## Où en est le projet

**Terminé.** Concept retenu : **« Sous nos pieds »**. 68 pages, 210 × 260 mm.

| Livrable | Où |
|---|---|
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

## Reconstruire

**Une seule commande reconstruit tout :**

```sh
npm install
npm run build        # vérifie les données, fabrique les deux PDF, puis contrôle
```

Les étapes séparément :

```sh
npm run donnees      # assemble data/catalogue.json puis le vérifie
npm run catalogue    # fabrique dist/*.pdf (pagination mesurée dans Chromium)
npm run controle     # débordements, corps, polices, prix, mentions obligatoires
npm run epreuve      # régénère epreuves/epreuve-tarifs.pdf
npm run recadrages   # re-détecte les tableaux sur les rendus du PDF source
npm run polices      # recopie les polices OFL depuis node_modules
npm run concepts     # régénère les trois maquettes de l'étape 2
```

`npm run build` sort en erreur si un contrôle échoue : il est utilisable en intégration continue.

Outils supposés présents : `python3`, `node`, `poppler-utils` (`pdftoppm`, `pdftotext`,
`pdffonts`, `pdfinfo`), et `pip install pillow` pour les recadrages.

## Mettre à jour un prix ou un millésime

1. Ouvrir la fiche du domaine : `data/fiches/NN.json` (NN = son numéro au sommaire, 01 à 40).
2. Modifier la valeur. **Les prix sont en centimes entiers** : `14,75 €` s'écrit `1475`.
   Il doit toujours y avoir **autant de prix que de paliers** dans le tableau.
3. `npm run donnees` — le script refuse de passer si quelque chose cloche.
4. `npm run epreuve` pour revoir le tableau d'origine face à la nouvelle version.

**Ne jamais écrire un prix ailleurs que dans `data/fiches/`.** Les gabarits ne font que lire.

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
| 6 – 61 | Les dix régions : une ouverture pleine page, puis ses domaines |
| 62 – 64 | Index des vins par type, de A à Z |
| 65 | Les produits à part : bag-in-box, sans alcool, jus de cépages, bières, armagnacs, ratafias |
| 66 | Les quarante domaines, de A à Z |
| 67 | Planche : la coupe pleine page |
| 68 | Contacts, lexique, mentions légales, crédits, message sanitaire |

## Arborescence

```
sources/     notre PDF et notre logo (lecture seule)
reference/   catalogue concurrent (inspiration design, lecture seule)
docs/        pièges du PDF, notes sur le concurrent, présentation des compétences
data/        catalogue.json, fiches/, corrections.md, pages/ (rendus 200 dpi), recadrages/
concepts/    les trois pistes (HTML, PDF, PNG)
src/         concepts/, styles/, images/, fonts/ (polices OFL embarquées)
scripts/     assemblage, vérifications, recadrages, épreuve, maquettes
epreuves/    épreuve de contrôle des tarifs
dist/        PDF finaux (à venir, étape 6)
archive-v1/  travail d'une session précédente, conduite sous un autre cahier des charges
```
