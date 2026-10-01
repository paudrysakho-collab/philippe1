# Prompt à donner à Cowork

> Copie tout ce qui est entre les deux lignes, et joins les trois fichiers :
> le catalogue `.pptx`, ton fichier de bouteilles, ton fichier d'images de domaine.

---

Tu dois poser des images dans un catalogue de vins déjà mis en page. **Tu ne touches à rien
d'autre** : pas un texte, pas un prix, pas un tableau, pas une couleur, pas une position.
Je m'occupe moi-même de la mise en forme ensuite.

## Les trois fichiers

1. **`catalogue-scio-2026-canva.pptx`** — le catalogue, 76 diapositives, 210 × 260 mm.
2. **Mon fichier de bouteilles** — toutes les bouteilles des domaines.
3. **Mon fichier d'images de domaine** — logos et portraits de vignerons.

**Commence par ouvrir les deux fichiers d'images et dis-moi ce que tu y trouves** : combien
d'images, dans quel format, et comment chacune est identifiée (nom de fichier, légende, ordre
des pages…). Ne pose rien tant que tu ne m'as pas dit comment tu comptes relier chaque image
à son domaine. Si les images ne sont pas nommées, propose-moi une table de correspondance que
je valide avant que tu commences.

## Où ça va

**40 diapositives sur 76** portent deux emplacements vides au contour pointillé : ce sont les
**premières** pages de chaque domaine. Les pages « (suite) », les ouvertures de région et les
pages d'index n'en ont pas et **ne se touchent pas**.

Sur ces 40 diapositives, les emplacements sont toujours à la même hauteur et à la même taille.
Seul le x change selon que la page est impaire (à droite) ou paire (à gauche) :

| Emplacement | Forme à remplacer | Taille | y | x page impaire | x page paire |
|---|---|---|---|---|---|
| **Rond du vigneron / logo** | ellipse pointillée étiquetée `ROND VIGNERON OU LOGO` | 40 × 40 mm | 37,7 mm | 17 mm | 23 mm |
| **Bouteille** | rectangle arrondi pointillé étiqueté `BOUTEILLE` | 24 × 62 mm | 37,7 mm | 163 mm | 169 mm |

Chaque emplacement est fait de **deux objets superposés** : la forme pointillée et un bloc de
texte qui porte l'étiquette. **Supprime les deux** une fois l'image posée — sinon le pointillé
et le mot « BOUTEILLE » restent imprimés sous l'image.

Le titre de chaque diapositive donne le numéro et le nom du domaine (« 1 François Reverdy »,
« 12 Maison et Domaine André Goichot »…). C'est lui qui fait foi pour l'appariement.

## Comment poser les images

**Le rond.** Une photo se recadre au carré puis se masque en cercle, et elle **remplit** tout
le rond de 40 mm. Un **logo ne se recadre jamais** : il entre en entier, centré, à l'échelle,
sur une réserve claire — un logo rogné est une faute.

**La bouteille.** Détourée, **fond transparent**, **contenue** dans les 24 × 62 mm sans
déformation (garde les proportions, ne l'étire pas). Aucun rectangle blanc ne doit apparaître
sur le papier crème. Si une bouteille arrive sur fond blanc non détouré, détoure-la.

**Résolution.** 200 ppi minimum à la taille imprimée : **rond ≥ 315 × 315 px**,
**bouteille ≥ 190 × 488 px**. En dessous, **laisse l'emplacement vide** et signale-le-moi.

## Ce que tu ne fais jamais

- **Ne devine pas un appariement.** Si tu n'es pas sûr qu'une image appartient bien à ce
  domaine-là, **laisse l'emplacement vide et dis-le-moi**. Une bouteille sur la mauvaise fiche
  est une erreur de commande chez le caviste : c'est pire qu'un trou.
- **Ne réutilise pas** l'image d'un domaine pour un autre, même s'ils se ressemblent.
- **Ne retouche aucun texte, prix, tableau, couleur ni position.** Les 715 prix du catalogue
  doivent être identiques avant et après.
- **Ne touche pas aux 36 autres diapositives.**
- **Loi Évin** : écarte toute image de verre levé, porté à la bouche ou trinqué, et toute
  scène de consommation. Vignes, paysages, chais, bouteilles, portraits : d'accord.

## Ce que tu me rends

1. **Un nouveau fichier**, `catalogue-scio-2026-canva-images.pptx` — garde l'original intact.
2. **Un tableau récapitulatif** : une ligne par domaine, avec pour chacun le rond posé (quelle
   image) ou vide (pourquoi), la bouteille posée (quelle image) ou vide (pourquoi).
3. **La liste des emplacements restés vides**, et pour chacun ce qu'il te faudrait.
4. **Une vérification visuelle** : convertis le fichier fini en images et **regarde les 40
   fiches une par une** avant de me le rendre. Tu cherches : un rond rogné, une bouteille
   déformée ou étirée, un rectangle blanc autour d'une bouteille, un pointillé ou une étiquette
   oublié dessous, une image qui dépasse sur le texte ou sur le tableau, une image floue.
   Corrige ce que tu trouves, puis dis-moi ce que tu as corrigé.

---

## Si Cowork a aussi le dépôt

Donne-lui en plus ces deux chemins, ça lui évite de tout re-déduire :

- `docs/emplacements-images.md` — la table des 40 diapositives : numéro de diapositive,
  numéro et nom du domaine, région, x du rond, x de la bouteille.
- `credits.md` — 30 images déjà repérées sur les sites officiels de 19 domaines, avec leur URL
  et leur résolution, si tu veux compléter ce que tes deux fichiers ne couvrent pas.
  **L'autorisation de chaque domaine reste à demander.**
