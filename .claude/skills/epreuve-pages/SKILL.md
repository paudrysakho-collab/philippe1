---
name: epreuve-pages
description: Protocole de contrôle visuel du catalogue Agence SCIO — convertir le PDF en images et regarder chaque page pour traquer débordements, coupures, chevauchements, lignes isolées et textes trop petits. À charger à l'étape de contrôle, après toute génération du PDF, et avant de déclarer une page ou le catalogue terminé.
---

# Regarder chaque page

Un PDF qui se construit sans erreur n'est pas un PDF correct. **Le seul contrôle qui compte
est de regarder les pages en image.** Le navigateur ment : il ne pagine pas comme Chromium
en mode impression.

## Le cycle

```sh
npm run build                                   # données vérifiées, puis PDF
mkdir -p epreuves/pages && rm -f epreuves/pages/*.png
pdftoppm -r 120 -png dist/catalogue-ecran.pdf epreuves/pages/p
```

Puis **ouvrir chaque PNG et le regarder**. Pas un échantillon : toutes les pages.
Corriger, régénérer, **recommencer** jusqu'à ce que la liste ci-dessous soit vide.

## Ce qu'on cherche, page par page

| Défaut | Comment il se voit |
|---|---|
| **Débordement** | Du texte ou un filet sort de la zone de sécurité, ou passe sous le pied de page |
| **Coupure** | Un tableau coupé au milieu d'une ligne ; une cuvée séparée de son prix |
| **Chevauchement** | Un encart posé sur du texte (le PDF source le fait p.15 : ne pas le reproduire) |
| **Ligne isolée** | Une veuve ou une orpheline : un mot seul en fin de paragraphe, une ligne seule en haut de page |
| **Texte trop petit** | Sous 9 pt en courant, sous 7,5 pt en tableau |
| **Carré à la place d'un caractère** | Glyphe manquant : vérifier `pdffonts`, puis le sous-ensemble de la police |
| **Prix mal aligné** | Une colonne de prix qui ne tombe pas au même endroit que sur la fiche précédente |
| **Page à moitié vide** | Le défaut principal du catalogue concurrent. Densifier ou refondre la page |
| **Logo abîmé** | Recoloré, déformé, rogné, ou sans sa marge libre |

## Les contrôles qu'une machine fait mieux que l'œil

À lancer **en plus**, jamais à la place :

```sh
scripts/verifier-donnees                        # 40 domaines, paliers, centimes entiers
pdffonts dist/catalogue-imprimeur.pdf           # toutes incorporées, aucun repli
pdfinfo dist/catalogue-imprimeur.pdf            # format, nombre de pages multiple de 4
ls -l dist/*.pdf                                # aucun fichier de plus de 50 Mo
```

**Chaque prix du JSON doit se retrouver dans le texte du PDF final :**

```sh
pdftotext dist/catalogue-ecran.pdf - > /tmp/texte.txt
python3 -c "
import json,re
cat=json.load(open('data/catalogue.json')); t=open('/tmp/texte.txt').read()
manquants=[]
for d in cat['domaines']:
  for tb in d['tableaux']:
    for l in tb['lignes']:
      for p in l['prix_centimes']:
        s=f'{p/100:.2f}'.replace('.',',')
        if s not in t: manquants.append((d['numero'], l.get('cuvee') or l['appellation'], s))
print(len(manquants),'prix manquants'); [print(m) for m in manquants[:20]]"
```

Un prix absent du texte du PDF signifie qu'il a été rendu en image, tronqué, ou pas rendu
du tout. C'est bloquant.

## Les deux sorties

- `dist/*-imprimeur.pdf` : fond perdu 3 mm, traits de coupe.
- `dist/*-ecran.pdf` : sans fond perdu, navigation cliquable, liens `tel:`, `mailto:` et site.

Les deux se contrôlent. Un lien mort dans la version écran est un défaut au même titre
qu'un débordement.

## La règle de fin

Ne déclare jamais une page « propre » parce que le code paraît juste.
**Tu l'as regardée en image, ou elle n'est pas contrôlée.**
