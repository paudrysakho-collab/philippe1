# Crédits images

## Photographies

**Ce catalogue ne contient aucune photographie.**

Toutes les illustrations sont dessinées pour lui, en SVG, dans ce dépôt
(`src/gabarits/pieces.mjs` et `src/gabarits/pages.mjs`) : les coupes de sol, les trames de
strates, les carottes de région, les pictogrammes de type de vin et de label. Les dessins
génératifs (coupes, carottes) sont tirés d'une **graine fixe** : une même entrée donne
toujours le même dessin, édition après édition.

Aucune bibliothèque d'icônes n'a été utilisée.

## Le logo

`sources/logo-agence-scio.jpg` — fourni par l'Agence SCIO. JPG CMJN, 1030 × 251 px.

Deux copies dérivées, sans aucune retouche du dessin :

| Fichier | Transformation |
|---|---|
| `src/images/logo-agence-scio-srgb.png` | conversion CMJN → sRGB |
| `src/images/logo-agence-scio-detoure.png` | conversion sRGB **et** fond blanc rendu transparent (seuil 243/255) — le dessin n'est pas touché |

Le logo est posé sur la couverture, la page de l'agence et la dernière page, toujours à sa
proportion native, avec une marge libre supérieure à la hauteur de son carré jaune.
Il n'est ni recoloré, ni déformé, ni rogné, ni ombré.

**Limite à connaître :** à 300 dpi, le fichier fourni ne dépasse pas **87 mm de large**.
Il est utilisé à 62 mm (couverture), 74 mm (page agence) et 70 mm (page finale) — donc dans
les clous, mais sans marge. Pour un usage plus grand, il faut une version vectorielle
(PDF, SVG, EPS ou AI). C'est noté dans `QUESTIONS.md`.

## Pictogrammes

Les pictogrammes de type de vin (bulles, blanc, rosé, rouge, doux, sans alcool, jus de
cépages, bière, spiritueux) et les jetons de mention (Bio, HVE, Allocation, Panachage,
Consultez-nous) **sont dessinés par l'agence pour ce catalogue**.

Ils ne reproduisent **aucun logo officiel** d'organisme certificateur — ni AB, ni Eurofeuille,
ni HVE, ni Demeter, ni Biodyvin, ni AOP, ni IGP. L'information que ces logos portent est
reprise (c'est du contenu, lu dans le tarif source) ; leur forme, non. La page 3 du catalogue
l'écrit noir sur blanc, et la légende le répète en pied de chaque fiche.

Si l'agence souhaite faire figurer les logos officiels, c'est une démarche auprès des
organismes concernés, pas une décision de maquette.

## Polices

Toutes sous licence **SIL Open Font License (OFL)**, récupérées via les paquets npm
`@fontsource` et **copiées dans `src/fonts/`** : la fabrication du PDF ne dépend d'aucun
accès réseau.

| Police | Rôle | Licence |
|---|---|---|
| **Young Serif** | titres, noms de domaine, ouvertures de région | OFL |
| **Spectral** | textes de présentation | OFL |
| **IBM Plex Sans** | tableaux, paliers, légendes (chiffres tabulaires) | OFL |

Les six autres familles présentes dans `src/fonts/` (Fraunces, Faustina, Archivo, Bricolage
Grotesque, Literata, Hanken Grotesk) servent aux maquettes des concepts 2 et 3 de
`concepts/`, pas au catalogue final.
