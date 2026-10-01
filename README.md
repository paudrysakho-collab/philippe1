# Catalogue Agence SCIO — édition 2026

Tarifs cavistes Vendée (85). 40 domaines, 10 régions.
Construit depuis `data/catalogue.json`, qui est la **seule vérité** du projet.

## Où en est le projet

**Étape 2 terminée — en attente du choix de concept.** Voir `CONCEPTS.md`.

| Fait | Où |
|---|---|
| Données des 40 domaines, vérifiées | `data/catalogue.json` |
| Épreuve de contrôle des tarifs | `epreuves/epreuve-tarifs.pdf` |
| Lecture du catalogue concurrent | `INSPIRATIONS.md` |
| Trois directions + maquettes | `CONCEPTS.md`, `concepts/*.png` |
| Questions en attente de réponse | `QUESTIONS.md` |
| Corrections appliquées | `data/corrections.md` |
| Compétences de design | `.claude/skills/`, présentées dans `docs/skills-design.md` |

## Reconstruire

```sh
npm install          # playwright + polices @fontsource
npm run donnees      # assemble data/catalogue.json puis le vérifie
npm run epreuve      # régénère epreuves/epreuve-tarifs.pdf
npm run build        # les deux
node scripts/concepts.mjs             # régénère les trois maquettes
node scripts/concepts.mjs c1-sous-nos-pieds   # une seule
```

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
