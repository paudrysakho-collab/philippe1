---
name: tableau-tarif
description: Règles du composant tableau de prix du catalogue Agence SCIO. À charger avant d'écrire, de modifier ou de mettre en page un tableau de tarifs, une colonne de prix, un palier de quantité ou un pied de fiche domaine. Un seul composant sert les 49 tableaux des 40 domaines, dont les paliers diffèrent tous.
---

# Le tableau de prix

C'est l'objet que le caviste regarde. Tout le reste du catalogue est au service de sa clarté.

## La règle d'or

**Aucun prix n'est jamais tapé dans un gabarit.** Les prix vivent dans `data/catalogue.json`,
en **centimes entiers** (`14,75 €` → `1475`), et ne sont lus que par le composant.
Si tu te surprends à écrire un chiffre dans du HTML, tu es en train d'introduire un bug.

**Tu ne corriges jamais un prix, même s'il paraît faux.** Tu le signales dans `QUESTIONS.md`
et tu poses une `note` sur la ligne.

## Les paliers diffèrent d'un domaine à l'autre

Un même composant pour les 40 domaines, avec **les quantités exactes de chacun** :

```
36 / 48 / 120 bts    60 / 120 / 240 bts     78 / 126 bts         90 / 120 / 300 bts
120 / 180 / 300 bts  144 / 300 / 600 bts    198 / 300 / Palette  72 / 300 / 600 bouteilles
120 / 300 / 600 cols 60 à 120 / 120 à 300 / Plus de 300 bts      48 bts seul
50 BIB demi pal / 100 BIB palette           5 Litres / 10 Litres  Tarif unique
```

- **Ne jamais harmoniser** les seuils entre domaines.
- **Ne jamais traduire** les unités : « bts », « cols », « bouteilles », « Palette » restent
  tels que la source les écrit. Seul `A partir` → `À partir` est corrigé (accent).
- Le nombre de prix d'une ligne **doit toujours égaler** le nombre de paliers de son tableau.
  `scripts/verifier-donnees` le contrôle ; il doit passer avant toute génération.

## Le bloc de prix

- **Largeur fixe** (≈ 50 à 52 mm), **divisée en parts égales** entre les paliers.
  Conséquence : sur les 40 fiches, le prix tombe toujours au même endroit, qu'il y ait
  un palier ou trois. C'est le seul moyen pour qu'un caviste trouve son prix sans réfléchir.
- Chiffres **tabulaires** : `font-variant-numeric: tabular-nums`. Les virgules s'alignent.
- Virgule décimale française, symbole `€` plus petit et plus clair que le montant.
- Le prix est l'élément **le plus lourd typographiquement** de la ligne. Jamais un gris pâle.

## L'anatomie d'une ligne

```
[picto couleur] [appellation / cuvée]  [millésime] [contenance] [ prix │ prix │ prix ]
```

- **Appellation** au-dessus, plus petite et plus claire ; **cuvée** en dessous, plus lourde.
  C'est la cuvée que le caviste cherche.
- `millesime` et `contenance` à droite, alignés, en petit : ce sont des précisions, pas des titres.
- Une cuvée absente de la source laisse la cellule vide ou un tiret cadratin. **On n'invente pas.**
- Les filets horizontaux sont fins (≤ 0,3 pt). Pas de bordure verticale entre les colonnes
  de texte ; seul le bloc de prix peut être détaché.

## Ce qui doit rester visible sur la fiche

Dans les cinq secondes, le caviste doit trouver : **qui est le domaine, ce qu'il produit,
le prix, à partir de quelle quantité, avec quoi il peut panacher, et si c'est franco.**

- La **note de prix** exacte du domaine (`H.T.`, `franco de port`, `départ chai`,
  `départ cave`, `hors frais de transport`, `franco à partir de 180 bouteilles`…).
  Elle varie d'un domaine à l'autre : ne jamais en réutiliser une d'un autre domaine.
- Les **départements de distribution**, triés par ordre croissant.
- Le **panachage** : « Possibilité de panacher » vaut à l'intérieur du domaine ; les quatre
  groupes inter-domaines (`agence.groupes_panachage`) sont signalés explicitement, des deux
  côtés, et méritent leur propre page.
- Les mentions de la source : **allocation**, « consultez-nous », BIB, Armagnac, bières,
  jus de cépages, vins désalcoolisés, ratafia.

## Les cas particuliers à ne pas écraser

| Cas | Traitement |
|---|---|
| Tarif unique (un seul palier) | Le bloc garde sa largeur ; une seule part, alignée à droite |
| Paliers de **contenant** (5 L / 10 L, BIB 3 L) | Ce ne sont pas des quantités : la dégressivité ne s'y applique pas |
| Lignes sans couleur (BIB Pergola d'Exea) | Cellule vide + note. **Ne pas deviner la couleur** |
| Lignes étoilées (Goichot, Exea, Frézier) | L'étoile de la ligne et celle de la note de prix ne disent pas la même chose : séparer les deux signes |
| Prix affichés + « demander le tarif » (n°25) | Afficher les deux, comme la source |
| Dégressivité inversée (n°15, n°19) | **Transcrire tel quel**, poser une note, signaler dans `QUESTIONS.md` |

## Contrôle final

Après génération du PDF :

```sh
pdftotext dist/catalogue-ecran.pdf - | grep -c "14,75"   # chaque prix du JSON doit s'y retrouver
scripts/verifier-donnees                                  # doit sortir sans erreur
```

Un prix présent dans `data/catalogue.json` et absent du texte du PDF final est un défaut
bloquant, pas un détail.
