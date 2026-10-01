# Les polices à téléverser dans Canva

Canva ne connaît pas ces trois polices. **Tant qu'elles ne sont pas téléversées, Canva les
remplace** par une police par défaut : les titres changent de dessin, les tableaux de largeur,
et des lignes peuvent se mettre à déborder. Téléversez-les une fois, avant d'ouvrir le
catalogue, et tout retombe en place.

## Comment faire

1. Dans Canva : **Marque → Polices de la marque → Téléverser une police**
   (il faut un compte Canva Pro ou Teams ; sans Pro, Canva substituera les polices).
2. Téléversez les six fichiers de ce dossier.
3. Ouvrez ensuite `dist/catalogue-scio-2026-canva.pptx`
   (**Créer un design → Importer un fichier**).

## Les six fichiers

| Fichier | Famille dans Canva | Où elle sert |
|---|---|---|
| `YoungSerif-Regular.ttf` | Young Serif | tous les titres, les numéros de domaine, le nom des cuvées en gros |
| `Spectral-Regular.ttf` | Spectral | les textes de présentation des domaines |
| `Spectral-Italic.ttf` | Spectral *italique* | les mentions « (suite) », les légendes |
| `Spectral-SemiBold.ttf` | Spectral **gras** | les mots mis en avant dans les textes |
| `IBMPlexSans-Regular.ttf` | IBM Plex Sans | les tableaux, les jetons, les bas de page |
| `IBMPlexSans-SemiBold.ttf` | IBM Plex Sans **gras** | les prix, les en-têtes de tableau, les cuvées |

Les deux fichiers « SemiBold » sont déclarés comme le **gras** de leur famille : le bouton
gras de Canva tombe donc sur le bon dessin, et non sur un faux gras épaissi.

## Licences

Les trois familles sont sous **SIL Open Font License 1.1** : usage commercial, impression et
modification autorisés, y compris pour un catalogue vendu ou diffusé.

- Young Serif — Uncut.wtf / Nolan Paparelli — <https://fonts.google.com/specimen/Young+Serif>
- Spectral — Production Type pour Google — <https://fonts.google.com/specimen/Spectral>
- IBM Plex Sans — IBM / Mike Abbink, Bold Monday — <https://fonts.google.com/specimen/IBM+Plex+Sans>

Les fichiers de ce dossier sont fabriqués à partir des paquets npm `@fontsource/*` (sous-jeux
latin et latin-ext réunis) par `npm run polices-ttf`. Ils contiennent tous les caractères
français : é è ê ë à â ç ô û ù î ï œ Œ É À Ç Ÿ ’ « » € °.
