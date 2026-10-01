---
name: picto-maison
description: Comment dessiner les pictos du catalogue Agence SCIO (couleurs de vin, labels, allocation, panachage, BIB) en SVG maison. À charger avant de créer une icône, une pastille, un symbole de label ou une légende. Interdit d'importer une bibliothèque d'icônes ou de redessiner un logo officiel.
---

# Les pictos maison

## Deux interdits, d'abord

1. **Aucune bibliothèque d'icônes.** Pas de Lucide, Feather, Font Awesome, Material, Phosphor,
   Heroicons, ni jeu d'emoji. Chaque picto est tracé à la main en SVG dans ce dépôt.
2. **Aucun logo officiel redessiné.** AB, Eurofeuille, HVE, Demeter, Biodyvin, AOP, IGP :
   ce sont des marques déposées avec des chartes strictes. On **ne les imite pas**.
   - L'**information** qu'ils portent est du contenu : elle se reprend (`labels[].label`).
   - Leur **forme** ne se reprend pas.
   - On crée donc **ses propres pictos**, visiblement différents des officiels, et on les
     **explique dans une légende** présente sur la fiche ou en page finale.
   - Si l'agence veut les vrais logos officiels, c'est une décision et une démarche d'ayant
     droit : à poser dans `QUESTIONS.md`, pas à trancher soi-même.

## Ce qu'il faut couvrir

**Couleurs de vin** (le repère n°1 pour un caviste) : blanc · rouge · rosé · bulles · doux ·
sans alcool · jus de cépages · bière · spiritueux (armagnac, ratafia).

**Mentions du catalogue** : allocation · panachage · panachage entre domaines ·
« consultez-nous » · BIB · magnum / 1,5 L.

**Labels relevés dans la source** : Bio · HVE · Demeter · Biodyvin · AOP · IGP.

## Comment les dessiner

- **Une seule géométrie de base pour toute la famille** : si les couleurs de vin sont des
  disques, elles le sont toutes ; la différence se joue sur le remplissage, pas sur la forme.
  Un caviste doit sentir « c'est la même famille » sans y penser.
- **Taille d'usage : 3 à 3,5 mm.** Dessine dans un `viewBox="0 0 14 14"` et vérifie le rendu
  **à la taille réelle, en image** — pas à l'écran agrandi. Un détail de 0,2 mm disparaît
  à l'impression.
- **Épaisseur de trait minimale : 0,25 mm** à la taille d'usage. En dessous, l'encre comble.
- **Pas d'ombre, pas de dégradé, pas de contour sur contour.** Un aplat, un trait, c'est tout.
- **Le blanc est un piège** : un picto « blanc » sur fond crème a besoin d'un contour, sinon
  il disparaît.
- Les pictos vivent dans un objet JS unique (`PICTOS`) et sortent par une seule fonction
  `picto(famille)` : jamais de SVG recopié dans un gabarit.

## La famille doit se distinguer sans la couleur

Le catalogue sera parfois photocopié, faxé, lu par quelqu'un qui distingue mal le rouge du vert.
**Chaque picto doit rester identifiable en nuances de gris.** Teste-le : passe la page en
niveaux de gris et regarde si tu peux encore séparer rosé, rouge et doux. Si non, change la
forme ou le remplissage, pas la teinte.

## La légende

Dès qu'un picto apparaît, sa légende est accessible :

- Une **légende courte** en pied de chaque fiche domaine (les familles présentes sur la fiche).
- Une **légende complète** sur l'entrée visuelle du catalogue et en page finale, avec la phrase
  qui explique que ce sont **nos pictos**, pas les logos officiels des organismes certificateurs.

## Illustrations génératives

Si un dessin est généré (figure d'un domaine, trame d'un sol, caisse d'un domaine) :

- **Graine fixe**, dérivée d'une donnée stable (le numéro du domaine). Deux générations
  successives doivent produire **exactement le même dessin**.
- Le dessin ne doit **jamais encoder une information fausse**. Compter les références d'un
  domaine est un fait ; déduire une qualité, un style ou un classement n'en est pas un.
