---
name: photos-domaines
description: Règles de collecte, de traitement et de créditation des photographies du catalogue Agence SCIO. À charger avant de chercher, télécharger, recadrer ou poser une photo, et avant d'écrire une ligne dans credits.md. Les illustrations dessinées restent le langage principal ; les photos sont l'exception.
---

# Les photos

**Les illustrations dessinées sont le langage principal du catalogue.** Les photos sont
permises **de temps en temps**, là où elles apportent vraiment quelque chose. Une photo qui
ne fait que remplir une page est une page à refaire.

## D'où elles viennent

| Source | Usage |
|---|---|
| **Site officiel du domaine** | Source principale. Vignes, paysages, chais, bouteilles, portraits de vignerons |
| **Wikimedia Commons, Unsplash, Pexels** | En complément, pour des sujets **génériques** : paysage d'une région, vigne, sol, ciel, matière |

**Jamais :**
- le site d'un caviste, d'un distributeur ou d'un concurrent ;
- le catalogue concurrent (`reference/`) ;
- **notre propre PDF source** : ni photo, ni étiquette, ni logo de domaine ;
- une image dont tu ne peux pas noter la source.

**Sur le site d'un domaine, tu ne prends que des photos.** Aucun texte, aucun chiffre, aucune
information : le contenu reste celui de `data/catalogue.json`. Si le site dit « 40 hectares »
et que notre PDF n'en parle pas, cela n'entre pas dans le catalogue.

**Une photo d'un domaine ne sert que pour ce domaine.** Une photo libre de droits n'est
**jamais** présentée comme un domaine précis.

Prends toujours la **plus grande version disponible**.

## Résolution

**Minimum 200 ppi à la taille imprimée.**

```
ppi = largeur en pixels / (largeur imprimée en mm / 25,4)
```

Exemple : une image posée sur 120 mm de large demande **au moins 945 px**.
Une image à fond perdu sur une page de 210 mm en demande **1654**.

En dessous du seuil :
1. utiliser la photo plus petite, ou
2. la réserver à la version écran, et
3. **noter dans `QUESTIONS.md` celles qu'il faudrait en haute définition.**

## Loi Évin

Elle vaut aussi pour les photos : **aucun verre levé, porté à la bouche ou trinqué**,
aucune scène de consommation ou de fête arrosée.
Paysages, vignes, sols, chais, bouteilles, portraits de vignerons : oui.

## Un traitement unique

Toutes les photos reçoivent **le même traitement** — même logique de cadrage, même
étalonnage ou même bichromie — pour qu'elles appartiennent à l'univers du catalogue et pas
à quarante univers différents. Le traitement est fixé par le concept retenu (voir `CONCEPTS.md`)
et appliqué par une seule règle CSS ou un seul script, jamais photo par photo.

**Cadrage :** respecter le ratio natif de la source. Un recadrage qui coupe un visage ou un
bâtiment est un défaut. Si le ratio ne rentre pas, change la place, pas la photo.

## `credits.md` — une ligne par photo, sans exception

L'agence s'en servira pour vérifier les autorisations et créditer. Format :

```md
| Fichier | Domaine ou sujet | Page de provenance | URL de l'image | Auteur | Licence |
|---|---|---|---|---|---|
| src/photos/d26-chai.jpg | n°26 Château la Gorce | https://… | https://… | — | site du domaine, autorisation à demander |
| src/photos/gen-craie.jpg | Craie (sujet générique) | https://commons.wikimedia.org/… | https://… | Nom Prénom | CC BY-SA 4.0 |
```

- Une photo sans ligne dans `credits.md` **ne part pas à l'impression**.
- Les licences doivent être **compatibles avec un usage commercial**, et créditées dans le
  catalogue quand elles l'exigent (CC BY, CC BY-SA).
- Les photos prises sur le site d'un domaine demandent une **autorisation de l'ayant droit** :
  la ligne le dit explicitement, pour que l'agence fasse la démarche.

## Si le réseau bloque

L'environnement filtre les domaines sortants. En cas de blocage (« host not in allowlist ») :
ne pas contourner, **dire à l'humain quel domaine autoriser** dans son environnement, et
continuer le travail qui n'en dépend pas.
