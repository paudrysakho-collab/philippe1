# Crédits images

## 1. Photographies des fiches domaines

**79 images posées sur les 80 emplacements des 40 fiches** : 40 ronds (vigneron, logo ou lieu)
et 39 bouteilles. Le seul emplacement resté vide (la bouteille du n°18) garde son repère
pointillé (voir section 2). Les images entrent par la source : `data/photos-locales.json` dit quelle image va
sur quelle fiche, `npm run photos` les prépare, `npm run build` les pose dans les deux PDF et
dans le `.pptx`. Les tables ci-dessous sont réécrites par `npm run photos` : elles disent
toujours ce qui est réellement posé.

**D'où elles viennent, par ordre de priorité**

1. **Les dossiers de l'agence** (`Bouteilles_de_vin/`, `Domaines_et_vignerons/`) : 28 images,
   selon la table validée par l'agence (la 29e, la bouteille du n°36, a été remplacée par la
   même en haute définition). Le nom du fichier d'origine figure dans la colonne
   « Source ».
2. **Les sites officiels des domaines** : 30 images, dont 20 des 30 repérées en 2026 (les
   autres doublaient une image de l'agence, ou ont été remplacées par mieux). Sur les sites
   WordPress (Blacailloux, Trichon), la médiathèque complète a été parcourue pour trouver
   la plus grande version de chaque bouteille. **L'autorisation de chaque domaine reste à demander** avant impression : une
   ligne, un domaine, une adresse exacte.
3. **Le Canva de l'agence, « Tarif septembre 2026 »** : 20 images, prises à la demande de
   l'agence. La photo d'une page de domaine ne sert que pour ce domaine. Les fichiers viennent
   d'un export PDF qualité « pro » du design, en lecture seule : le design n'a pas été modifié.
   Canva réduit un peu les images à l'export ; la résolution indiquée est celle de l'export,
   donc la résolution réelle est égale ou meilleure.
4. **Les photos envoyées par les domaines à l'agence**, retrouvées dans la messagerie : le
   rond du n°21 vient de l'album que le Domaine Trichon a partagé le 18 septembre 2026 pour
   le catalogue du salon.

**Résolution.** Toutes sont au-dessus du plancher de 200 ppi à leur taille imprimée, aucune
n'a été agrandie. Les plus justes : bouteille n°21 (202 ppi), rond n°3 (213 ppi), rond n°35
(217 ppi). Une version plus grande de celles-là améliorerait l'impression.

**Traitement.** Une seule fonction pour toutes (`scripts/preparer-photos.py`) : saturation
0,82, contraste 1,06, rouge réchauffé, bleu refroidi. Rien n'est déformé.

- **Un portrait** est recadré au carré puis masqué en cercle.
- **Plusieurs personnes** (n°18, n°37) : on recule au lieu de recadrer serré, pour que toutes
  les têtes tiennent entières dans le cercle. Si le carré dépasse la photo, la marge prend la
  couleur du bord (ciel, plafond), fondue.
- **Deux portraits séparés de deux personnes** (n°12, n°30), ou deux visages d'une même
  photo trop large (n°21) : chacun occupe une moitié du rond, séparées par un filet clair.
  Au n°21, le cadrage s'arrête au-dessus des diplômes que tiennent les vignerons : aucune
  médaille ne figure dans notre tarif, elle ne doit pas entrer par la photo.
- **Un logo** n'est jamais rogné : il entre en entier, centré, sur une réserve claire (ou
  sombre sous un logo blanc).
- **Une bouteille** est détourée sur fond transparent et contenue dans 24 × 62 mm. Les 39
  ont été contrôlées une à une sur fond sombre (bords, bouchon, goulot, trous) et par un
  test automatique de symétrie. Celles du n°15 (devant une caisse) et du n°31 (verre rosé
  pâle sur fond blanc) sont détourées par un modèle de segmentation (`detourage: modele`),
  puis nettoyées par la symétrie de la bouteille : les lettres de la caisse tombent. Celle
  du n°24, bouchon blanc sur fond blanc, est détourée à tolérance très serrée
  (`tolerances`) pour garder le bouchon entier ; celle du n°28 est recadrée au ras du pied
  pour perdre son reflet ; celles des n°36 et n°39 perdent l'ombre translucide que leur
  PNG portait sous le pied (`ombre: couper`). La bouteille du n°36 est la même « 4 Saisons
  2020 » que dans le dossier de l'agence, reprise du site du domaine en haute définition
  (1013 × 1350 px au lieu de 172 × 605).

**Loi Évin.** Aucun verre levé, porté à la bouche ou trinqué, aucune scène de dégustation.
Écartées pour cette raison : les photos de dégustation des n°2, 6, 8, 30, 31, 35 et 39 (sites
ou Canva). **Deux ronds sont recadrés au-dessus d'un verre tenu en main**, qui n'apparaît pas
dans le cercle : n°10 (portrait au chai) et n°18 (le couple). Si l'agence préfère ne pas
partir de ces photos, il suffit de retirer leurs deux lignes de `data/photos-locales.json`.

**Autres images écartées.**
- Images générées par IA, signalées par leur nom de fichier : le portrait du Canva de la page
  Solemme, la bouteille de la page Noëls, et celles déjà écartées des dossiers de l'agence.
- Le site trouvé pour le n°3 (`domaineducolombier.com`) est un homonyme, un lieu de réception
  en Hauts-de-France : il a été retiré de `data/sites-domaines.json`.
- Le logo Denis Frézier du Canva : 256 × 197 px, soit 187 ppi, sous le plancher.

<!-- images:debut -->

**82 images posées sur 80 emplacements.**

### Image par image

| n° | Domaine | Image | Sujet | Provenance | Source | Résolution | Droits |
|---|---|---|---|---|---|---|---|
| 1 | François Reverdy | rond (`src/photos/rond/d01.jpg`) | portrait du vigneron, noir et blanc | dossier de l'agence | `Domaines_et_vignerons/Francois_Reverdy/Francois_Reverdy_Portrait_vigneron.png` | 486x463 px → 294 ppi à 40 mm | photothèque de l'agence |
| 1 | François Reverdy | bouteille (`src/photos/bouteille/d01.png`) | bouteille de Chinon, 3e de la photo de gamme | dossier de l'agence | `Bouteilles_de_vin/Francois_Reverdy/Francois_Reverdy_Gamme_5_bouteilles.jpg` | 8256x5505 px → 1865 ppi à 24 × 62 mm | photothèque de l'agence |
| 2 | Domaine de la Barbinière | rond (`src/photos/rond/d02.jpg`) | vendanges dans les vignes du domaine | site officiel du domaine | page https://www.domainedelabarbiniere.com/ — image <https://static.wixstatic.com/media/42f898_a63b2bbb4dbb4345b3bf6054137906e1~mv2_d_5184_3456_s_4_2.jpg/v1/fill/w_2500,h_1666,al_c/42f898_a63b2bbb4dbb4345b3bf6054137906e1~mv2_d_5184_3456_s_4_2.jpg> | 2500x1666 px → 1058 ppi à 40 mm | **autorisation à demander au domaine** |
| 2 | Domaine de la Barbinière | bouteille (`src/photos/bouteille/d02.png`) | bouteille Les Amphibol | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d02-barbiniere-les-amphibol.jpg` | 1024x3988 px → 1634 ppi à 24 × 62 mm | photothèque de l'agence |
| 3 | Domaine du Colombier / J.Y Bretaudeau | rond (`src/photos/rond/d03.jpg`) | le vigneron au chai | Canva de l'agence « Tarif septembre 2026 », page 6 | `canva/d03-p06-021.png` | 515x336 px → 213 ppi à 40 mm | photothèque de l'agence |
| 3 | Domaine du Colombier / J.Y Bretaudeau | bouteille (`src/photos/bouteille/d03.png`) | bouteille Rouge au lèvres | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d03-colombier-rouge-aux-levres.jpg` | 1056x3964 px → 1605 ppi à 24 × 62 mm | photothèque de l'agence |
| 4 | Domaine des Noëls | rond (`src/photos/rond/d04.jpg`) | portrait | Canva de l'agence « Tarif septembre 2026 », page 7 | `canva/d04-p07-038.png` | 994x1325 px → 631 ppi à 40 mm | photothèque de l'agence |
| 4 | Domaine des Noëls | bouteille (`src/photos/bouteille/d04.png`) | bouteille Promenade des Noëls, Anjou blanc | dossier de l'agence | `Bouteilles_de_vin/Domaine_des_Noels/Domaine_des_Noels_Anjou_Blanc_Promenade_des_Noels.jpg` | 2113x2195 px → 862 ppi à 24 × 62 mm | photothèque de l'agence |
| 5 | Chai Berteaud Manceau | rond (`src/photos/rond/d05.jpg`) | les deux fondateurs du chai | site officiel du domaine | page https://chai-berteaud-manceau.com/ — image <https://chai-berteaud-manceau.com/wp-content/uploads/2024/01/DSC8855-edited-scaled.jpg> | 1784x2560 px → 1133 ppi à 40 mm | **autorisation à demander au domaine** |
| 5 | Chai Berteaud Manceau | bouteille (`src/photos/bouteille/d05.png`) | bouteille du domaine | site officiel du domaine | page https://chai-berteaud-manceau.com/ — image <https://chai-berteaud-manceau.com/wp-content/uploads/2024/06/COURANT-Chenin-2023-768x2654.webp> | 768x2654 px → 1071 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 6 | Domaine Jean de Villebois | rond (`src/photos/rond/d06.jpg`) | dans les vignes | Canva de l'agence « Tarif septembre 2026 », page 9 | `canva/d06-p09-059.png` | 1800x1200 px → 762 ppi à 40 mm | photothèque de l'agence |
| 6 | Domaine Jean de Villebois | bouteille (`src/photos/bouteille/d06.png`) | bouteille Pouilly-Fumé Les Silex Blancs | site officiel du domaine | page https://www.jdevillebois.com/ — image <https://www.jdevillebois.fr/wp-content/uploads/2023/08/jdevillebois_pouillyfume_silexblancs_blanc_23.webp> | 237x861 px → 353 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 7 | Divin No Low | rond (`src/photos/rond/d07.jpg`) | vinification en cuverie | site officiel du domaine | page https://www.divinnolow.fr/ — image <https://www.divinnolow.fr/wp-content/uploads/2025/02/divin_officiel_alessandro_juin_24_158.png.webp> | 2000x1333 px → 846 ppi à 40 mm | **autorisation à demander au domaine** |
| 7 | Divin No Low | bouteille (`src/photos/bouteille/d07.png`) | bouteille du domaine | site officiel du domaine | page https://www.divinnolow.fr/ — image <https://www.divinnolow.fr/wp-content/uploads/2024/02/divin_0.5_chardonnay_vigneron_25.png.webp> | 800x2560 px → 1025 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 8 | Domaine Boehler | rond (`src/photos/rond/d08.jpg`) | logo du domaine | Canva de l'agence « Tarif septembre 2026 », page 11 | `canva/d08-p11-077.png` | 447x447 px → 447 ppi à 40 mm | photothèque de l'agence |
| 8 | Domaine Boehler | bouteille (`src/photos/bouteille/d08.png`) | bouteille Molse blanc | dossier de l'agence | `Bouteilles_de_vin/Domaine_Boehler/Domaine_Boehler_Alsace_Molse_Blanc.jpg` | 1503x2672 px → 1036 ppi à 24 × 62 mm | photothèque de l'agence |
| 9 | Domaine des Nugues | rond (`src/photos/rond/d09.jpg`) | portrait des vignerons | site officiel du domaine | page https://www.domainedesnugues.com/ — image <https://www.domainedesnugues.com/wp-content/uploads/2020/02/DSC_8874-1-1-370x555.jpg> | 370x555 px → 235 ppi à 40 mm | **autorisation à demander au domaine** |
| 9 | Domaine des Nugues | bouteille (`src/photos/bouteille/d09.png`) | bouteille Moulin-à-Vent 2022 | dossier de l'agence | `Bouteilles_de_vin/Domaine_des_Nugues/Domaine_des_Nugues_Moulin-a-Vent_2022_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 10 | Domaine Sébastien Magnien | rond (`src/photos/rond/d10.jpg`) | portrait au chai, recadré au-dessus du verre | Canva de l'agence « Tarif septembre 2026 », page 13 | `canva/d10-p13-088.png` | 1378x845 px → 258 ppi à 40 mm | photothèque de l'agence |
| 10 | Domaine Sébastien Magnien | bouteille (`src/photos/bouteille/d10.png`) | bouteille Bourgogne Pinot Noir 2023 | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d10-magnien-bourgogne-pinot-noir.jpg` | 528x2013 px → 823 ppi à 24 × 62 mm | photothèque de l'agence |
| 11 | Domaine Nadine Ferrand | rond (`src/photos/rond/d11.jpg`) | les vigneronnes au chai, noir et blanc | dossier de l'agence | `Domaines_et_vignerons/Domaine_Nadine_Ferrand/Domaine_Nadine_Ferrand_Vigneronnes_au_chai.jpg` | 1920x1080 px → 686 ppi à 40 mm | photothèque de l'agence |
| 11 | Domaine Nadine Ferrand | bouteille (`src/photos/bouteille/d11.png`) | bouteille Mâcon Charnay-lès-Mâcon | dossier de l'agence | `Bouteilles_de_vin/Domaine_Nadine_Ferrand/Domaine_Nadine_Ferrand_Macon-Charnay-les-Macon.jpg` | 2266x4032 px → 1112 ppi à 24 × 62 mm | photothèque de l'agence |
| 12 | Maison et Domaine André Goichot | rond (`src/photos/rond/d12.jpg`) | deux portraits de la maison, côte à côte | Canva de l'agence « Tarif septembre 2026 », page 15 | `canva/d12-p15-107.png` + `canva/d12-p15-108.png` | 491x510 + 491x510 px → 312 ppi à 40 mm | photothèque de l'agence |
| 12 | Maison et Domaine André Goichot | bouteille (`src/photos/bouteille/d12.png`) | bouteille Givry Champ la Dame 2023 | dossier de l'agence | `Bouteilles_de_vin/Maison_Andre_Goichot/Maison_Andre_Goichot_Givry_Champ_la_Dame_2023_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 13 | Château du Cray | rond (`src/photos/rond/d13.jpg`) | le vignoble du Château du Cray (bannière de sa page) | site officiel du domaine | page https://www.maisongoichot.com/fr/content/chateau-du-cray — image <https://www.maisongoichot.com/sites/default/files/styles/banner_md/public/banner-cray_0.jpg?itok=kYMCGWkV> | 1130x663 px → 421 ppi à 40 mm | **autorisation à demander au domaine** |
| 13 | Château du Cray | bouteille (`src/photos/bouteille/d13.png`) | bouteille Mercurey blanc Les Doues (cuvée absente du tarif) | dossier de l'agence | `Bouteilles_de_vin/Chateau_du_Cray/Chateau_du_Cray_Mercurey_Blanc_Les_Doues.png` | 180x673 px → 272 ppi à 24 × 62 mm | photothèque de l'agence |
| 14 | Domaine Les Guignottes | rond (`src/photos/rond/d14.jpg`) | nom du domaine sur ses vignes | Canva de l'agence « Tarif septembre 2026 », page 17 | `canva/d14-p17-122.png` | 530x332 px → 337 ppi à 40 mm | photothèque de l'agence |
| 14 | Domaine Les Guignottes | bouteille (`src/photos/bouteille/d14.png`) | bouteille Bourgogne Chardonnay 2023 | dossier de l'agence | `Bouteilles_de_vin/Domaine_des_Guignottes/Domaine_des_Guignottes_Bourgogne_Chardonnay_2023_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 15 | Domaine des Verchères | rond (`src/photos/rond/d15.jpg`) | portrait du vigneron | site officiel du domaine | page https://www.domainedesvercheres.com/ — image <https://images.squarespace-cdn.com/content/v1/68b02ccf60982e21017910b9/4120efd3-8e74-45e3-99eb-7111ee3b897e/IMG_3840.JPG> | 2500x2199 px → 1396 ppi à 40 mm | **autorisation à demander au domaine** |
| 15 | Domaine des Verchères | bouteille (`src/photos/bouteille/d15.png`) | bouteille Mâcon Chardonnay | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d15-vercheres-macon-chardonnay.jpg` | 1024x4142 px → 1694 ppi à 24 × 62 mm | photothèque de l'agence |
| 16 | Domaine Le Prieuré des Papes | rond (`src/photos/rond/d16.jpg`) | logo du domaine | Canva de l'agence « Tarif septembre 2026 », page 19 | `canva/d16-p19-133.png` | 750x500 px → 549 ppi à 40 mm | photothèque de l'agence |
| 16 | Domaine Le Prieuré des Papes | bouteille (`src/photos/bouteille/d16.png`) | bouteille Châteauneuf-du-Pape Vieilles Vignes | dossier de l'agence | `Bouteilles_de_vin/Le_Prieure_des_Papes/Le_Prieure_des_Papes_Chateauneuf-du-Pape_Vieilles_Vignes_2022_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 17 | Domaine de Coyeux | rond (`src/photos/rond/d17.jpg`) | le domaine | Canva de l'agence « Tarif septembre 2026 », page 20 | `canva/d17-p20-140.png` | 817x774 px → 491 ppi à 40 mm | photothèque de l'agence |
| 17 | Domaine de Coyeux | bouteille (`src/photos/bouteille/d17.png`) | bouteille Les Jumelles, Beaumes-de-Venise | dossier de l'agence | `Bouteilles_de_vin/Domaine_de_Coyeux/Domaine_de_Coyeux_Beaumes-de-Venise_Les_Jumelles_2023_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 18 | Domaine du Moulin Blanc | rond (`src/photos/rond/d18.jpg`) | le couple, cadrage élargi (les deux visages entiers), toujours au-dessus du verre | Canva de l'agence « Tarif septembre 2026 », page 21 | `canva/d18-p21-149.png` | 1200x630 px → 381 ppi à 40 mm | photothèque de l'agence |
| 18 | Domaine du Moulin Blanc | bouteille (`src/photos/bouteille/d18.png`) | bouteille de Côtes du Rhône blanc | dossier de l'agence (envoyée le 2 octobre 2026) | `Bouteilles_de_vin/Domaine_du_Moulin_Blanc/Domaine_du_Moulin_Blanc_Cotes_du_Rhone_Blanc.jpg` | 1500x2000 px → 667 ppi à 24 × 62 mm | photothèque de l'agence |
| 19 | Domaine de la Pousterle | rond (`src/photos/rond/d19.jpg`) | vendanges dans les vignes | Canva de l'agence « Tarif septembre 2026 », page 22 | `canva/d19-p22-151.png` | 640x575 px → 365 ppi à 40 mm | photothèque de l'agence |
| 19 | Domaine de la Pousterle | bouteille (`src/photos/bouteille/d19.png`) | bouteille Terroir d'Ansouis blanc 2021 | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d19-pousterle-terroir-d-ansouis.jpg` | 528x2013 px → 823 ppi à 24 × 62 mm | photothèque de l'agence |
| 20 | Domaine des Pasquiers | rond (`src/photos/rond/d20.jpg`) | portrait de la famille | site officiel du domaine | page https://domainedespasquiers.fr/ — image <https://domainedespasquiers.fr/wp-content/uploads/2021/04/Famille-Lambert.jpg> | 1920x1440 px → 914 ppi à 40 mm | **autorisation à demander au domaine** |
| 20 | Domaine des Pasquiers | bouteille (`src/photos/bouteille/d20.png`) | bouteille Plan de Dieu 2023 | dossier de l'agence | `Bouteilles_de_vin/Domaine_des_Pasquiers/Domaine_des_Pasquiers_Cotes-du-Rhone_Villages_Plan_de_Dieu_2023_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 21 | Domaine Trichon | rond (`src/photos/rond/d21.jpg`) | les deux vignerons, recadrés sur leurs visages | album photo envoyé par le domaine à l'agence pour le catalogue (mail du 18 septembre 2026) | `https://lh3.googleusercontent.com/pw/AP1GczOwhUdoCWgFdCxSik5VFvSe97Fl3gXOWPtwWJlx1fc07msALKWnAzVYB-HCaEfzcSGJoHc9jqFmY7wiMJ9j4nPGBIw96UQIIASnpA_DfgZRsnGoQjX2=d` + `https://lh3.googleusercontent.com/pw/AP1GczOwhUdoCWgFdCxSik5VFvSe97Fl3gXOWPtwWJlx1fc07msALKWnAzVYB-HCaEfzcSGJoHc9jqFmY7wiMJ9j4nPGBIw96UQIIASnpA_DfgZRsnGoQjX2=d` | 4096x3072 + 4096x3072 px → 878 ppi à 40 mm | photothèque de l'agence |
| 21 | Domaine Trichon | bouteille (`src/photos/bouteille/d21.png`) | bouteille de Mondeuse du Bugey (cuvée du domaine absente du tarif) | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d21-trichon-mondeuse.jpg` | 544x1916 px → 780 ppi à 24 × 62 mm | photothèque de l'agence |
| 22 | Domaine Stratéus | rond (`src/photos/rond/d22.jpg`) | logo du domaine | site officiel du domaine | page https://www.strateus-madiran.com/ — image <https://static.wixstatic.com/media/17aeb1_919520f3e4f949aa8782d0b6d0056cd9~mv2.png/v1/fill/w_586,h_586,al_c/17aeb1_919520f3e4f949aa8782d0b6d0056cd9~mv2.png> | 586x586 px → 405 ppi à 40 mm | **autorisation à demander au domaine** |
| 22 | Domaine Stratéus | bouteille (`src/photos/bouteille/d22.png`) | bouteille Madiran Strateus | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d22-strateus-madiran.jpg` | 960x4392 px → 1785 ppi à 24 × 62 mm | photothèque de l'agence |
| 23 | Domaine Haut Marin | rond (`src/photos/rond/d23.jpg`) | logo du domaine | site officiel du domaine | page https://www.domaine-hautmarin.com/ — image <https://www.domaine-hautmarin.com/wp-content/uploads/2025/12/Logo-Haut-Marin.png> | 1056x594 px → 698 ppi à 40 mm | **autorisation à demander au domaine** |
| 23 | Domaine Haut Marin | bouteille (`src/photos/bouteille/d23.png`) | bouteille N°4 Triton 2024 | dossier de l'agence | `Bouteilles_de_vin/Domaine_Haut-Marin/Domaine_Haut-Marin_IGP_Cotes_de_Gascogne_Triton_2024_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 24 | Fabien Castaing | rond (`src/photos/rond/d24.jpg`) | portrait du vigneron dans ses vignes | site officiel du domaine | page https://www.fabiencastaing.com/ — image <https://www.fabiencastaing.com/wp-content/uploads/2021/04/2-Genealogie-2015-fabien-scaled.jpg> | 1920x2560 px → 1219 ppi à 40 mm | **autorisation à demander au domaine** |
| 24 | Fabien Castaing | bouteille (`src/photos/bouteille/d24.png`) | bouteille ADN 24 rouge | Canva de l'agence « Tarif septembre 2026 », page 27 | `canva/d24-p27-214.png` | 225x699 px → 286 ppi à 24 × 62 mm | photothèque de l'agence |
| 25 | La Passion des Terroirs | rond (`src/photos/rond/d25.jpg`) | portrait de famille d'époque | site officiel du domaine | page https://lapassiondesterroirs.com/ — image <https://lapassiondesterroirs.com/wp-content/uploads/lucien-lurton-1.png> | 685x1086 px → 435 ppi à 40 mm | **autorisation à demander au domaine** |
| 25 | La Passion des Terroirs | bouteille (`src/photos/bouteille/d25.png`) | bouteille du domaine | site officiel du domaine | page https://lapassiondesterroirs.com/ — image <https://lapassiondesterroirs.com/wp-content/uploads/BOUT-DOYAC.png> | 1039x4242 px → 1737 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 26 | Château la Gorce | rond (`src/photos/rond/d26.jpg`) | portrait des vignerons | site officiel du domaine | page https://www.chateaulagorce.com/ — image <https://www.chateaulagorce.com/wp-content/uploads/2023/01/ChateauLaGorce_Portrait_ManaEmmanuel_Jardin.jpg> | 1000x1500 px → 635 ppi à 40 mm | **autorisation à demander au domaine** |
| 26 | Château la Gorce | bouteille (`src/photos/bouteille/d26.png`) | bouteille La Bonne Résolution 2022 | dossier de l'agence | `Bouteilles_de_vin/Chateau_La_Gorce/Chateau_La_Gorce_Medoc_La_Bonne_Resolution_2022.png` | 1080x1920 px → 671 ppi à 24 × 62 mm | photothèque de l'agence |
| 27 | Château Falfas | rond (`src/photos/rond/d27.jpg`) | logo du château | dossier de l'agence | `Domaines_et_vignerons/Chateau_Falfas/Chateau_Falfas_Logo.png` | 470x311 px → 391 ppi à 40 mm | photothèque de l'agence |
| 27 | Château Falfas | bouteille (`src/photos/bouteille/d27.png`) | bouteille Château Falfas | Canva de l'agence « Tarif septembre 2026 », page 30 | `canva/d27-p30-244.png` | 302x1040 px → 400 ppi à 24 × 62 mm | photothèque de l'agence |
| 28 | Château Pré la Lande | rond (`src/photos/rond/d28.jpg`) | vendanges au domaine | site officiel du domaine | page https://www.prelalande.com/ — image <https://www.prelalande.com/images/background/methode.jpg> | 800x640 px → 406 ppi à 40 mm | **autorisation à demander au domaine** |
| 28 | Château Pré la Lande | bouteille (`src/photos/bouteille/d28.png`) | bouteille du domaine | site officiel du domaine | page https://www.prelalande.com/ — image <https://www.prelalande.com/images/portfolio/Famille.png> | 2500x2500 px → 910 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 29 | Château Balac | rond (`src/photos/rond/d29.jpg`) | portrait des vignerons | site officiel du domaine | page https://chateaubalac.com/ — image <https://chateaubalac.com/wp-content/uploads/2025/03/portrait-chateau-balac_04.jpg> | 886x591 px → 375 ppi à 40 mm | **autorisation à demander au domaine** |
| 29 | Château Balac | bouteille (`src/photos/bouteille/d29.png`) | bouteille Château Balac Haut-Médoc (cuvée absente du tarif) | dossier de l'agence | `Bouteilles_de_vin/Chateau_Balac/Chateau_Balac_Medoc_Cru_Bourgeois_Superieur_2022_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 30 | Château l’Escarderie | rond (`src/photos/rond/d30.jpg`) | les deux vignerons, deux portraits côte à côte | site officiel du domaine | page https://lescarderievins.com/ — image <https://lescarderievins.com/wp-content/uploads/2023/03/melanie-lescarderie-chateau-fronsac.png> + <https://lescarderievins.com/wp-content/uploads/2023/03/thomas-vignoble-fronsac-bordeaux-saint-emillion.png> | 492x492 + 492x492 px → 312 ppi à 40 mm | **autorisation à demander au domaine** |
| 30 | Château l’Escarderie | bouteille (`src/photos/bouteille/d30.png`) | bouteille Château l'Escarderie | site officiel du domaine | page https://lescarderievins.com/ — image <https://lescarderievins.com/wp-content/uploads/2020/11/produit-chateau-lescarderie.png> | 683x1024 px → 394 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 31 | Bastide de Blacailloux | rond (`src/photos/rond/d31.jpg`) | borie en pierre sèche du domaine | site officiel du domaine | page https://blacailloux.fr/ — image <https://blacailloux.fr/wp-content/uploads/2026/07/art-de-rehabiliter-scaled.jpg.webp> | 2560x1709 px → 1085 ppi à 40 mm | **autorisation à demander au domaine** |
| 31 | Bastide de Blacailloux | bouteille (`src/photos/bouteille/d31.png`) | bouteille JOIO rosé | site officiel du domaine | page https://blacailloux.fr/ — image <https://blacailloux.fr/wp-content/uploads/2026/06/joio-rose.jpg> | 2000x2000 px → 752 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 32 | Famille d’Exea | rond (`src/photos/rond/d32.jpg`) | logo de la maison | site officiel du domaine | page https://www.laboutiquedexea.com/ — image <https://www.laboutiquedexea.com/cdn/shop/files/E_uXE_uA_blanc.png?v=1779183522&width=600> | 600x533 px → 468 ppi à 40 mm | **autorisation à demander au domaine** |
| 32 | Famille d’Exea | bouteille (`src/photos/bouteille/d32.png`) | bouteille Jardins de Corbières rouge | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d32-exea-jardin-de-corbieres.jpg` | 1056x4026 px → 1647 ppi à 24 × 62 mm | photothèque de l'agence |
| 33 | Famille d’Exea — Jus de Cépages | rond (`src/photos/rond/d33.jpg`) | brebis dans les vignes | Canva de l'agence « Tarif septembre 2026 », page 36 | `canva/d33-p36-303.png` | 1800x1200 px → 762 ppi à 40 mm | photothèque de l'agence |
| 33 | Famille d’Exea — Jus de Cépages | bouteille (`src/photos/bouteille/d33.png`) | bouteille de jus de Grenache | Canva de l'agence « Tarif septembre 2026 », page 36 | `canva/d33-p36-306.png` | 535x1024 px → 358 ppi à 24 × 62 mm | photothèque de l'agence |
| 34 | Château de Gragnos | rond (`src/photos/rond/d34.jpg`) | grappes à la vigne | site officiel du domaine | page https://www.chateaudegragnos.com/ — image <https://www.chateaudegragnos.com/web/image/9841-9b4b7150/DSCF4018.JPG> | 1280x1920 px → 813 ppi à 40 mm | **autorisation à demander au domaine** |
| 34 | Château de Gragnos | bouteille (`src/photos/bouteille/d34.png`) | bouteille Lou Daro 2022 | dossier de l'agence, retouchée par l'agence avec Gemini (fond refait), Drive « photo gemini », 2 octobre 2026 | `gemini/d34-gragnos-lou-daro.jpg` | 528x2024 px → 825 ppi à 24 × 62 mm | photothèque de l'agence |
| 35 | Domaine Les Lys | rond (`src/photos/rond/d35.jpg`) | logo du domaine | Canva de l'agence « Tarif septembre 2026 », page 38 | `canva/d35-p38-321.png` | 265x245 px → 217 ppi à 40 mm | photothèque de l'agence |
| 35 | Domaine Les Lys | bouteille (`src/photos/bouteille/d35.png`) | bouteille Duché | dossier de l'agence | `Bouteilles_de_vin/Domaine_Les_Lys/Domaine_Les_Lys_Duche_dUzes_Duche_Rouge.png` | 1080x1920 px → 671 ppi à 24 × 62 mm | photothèque de l'agence |
| 36 | Prieuré Sainte-Marie d’Albas | rond (`src/photos/rond/d36.jpg`) | les deux vignerons et leur rosé, noir et blanc | dossier de l'agence | `Domaines_et_vignerons/Prieure_Sainte_Marie_dAlbas/Prieure_Sainte_Marie_dAlbas_Vignerons_avec_rose_NB.jpg` | 1181x1181 px → 750 ppi à 40 mm | photothèque de l'agence |
| 36 | Prieuré Sainte-Marie d’Albas | bouteille (`src/photos/bouteille/d36.png`) | bouteille 4 Saisons 2020 (même image que celle de l'agence, en haute définition) | site officiel du domaine | page https://www.saintemariedalbas.com/ — image <https://www.saintemariedalbas.com/wp-content/uploads/2023/11/4-saisons.png> | 1013x1350 px → 472 ppi à 24 × 62 mm | **autorisation à demander au domaine** |
| 37 | Champagne Dekeyne | rond (`src/photos/rond/d37.jpg`) | les deux frères dans les vignes | Canva de l'agence « Tarif septembre 2026 », page 40 | `canva/d37-p40-345.png` | 1800x1200 px → 914 ppi à 40 mm | photothèque de l'agence |
| 37 | Champagne Dekeyne | bouteille (`src/photos/bouteille/d37.png`) | bouteille Chardonnay | dossier de l'agence | `Bouteilles_de_vin/Champagne_Dekeyne/Champagne_Dekeyne_Chardonnay_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 38 | Champagne Denis Frézier | rond (`src/photos/rond/d38.jpg`) | le village dans ses vignes | Canva de l'agence « Tarif septembre 2026 », page 41 | `canva/d38-p41-355.png` | 1024x768 px → 488 ppi à 40 mm | photothèque de l'agence |
| 38 | Champagne Denis Frézier | bouteille (`src/photos/bouteille/d38.png`) | bouteille Les Trois Crus | dossier de l'agence | `Bouteilles_de_vin/Champagne_Denis_Frezier/Champagne_Denis_Frezier_Les_Trois_Crus_catalogue.png` | 1600x2000 px → 574 ppi à 24 × 62 mm | photothèque de l'agence |
| 39 | Champagne Solemme | rond (`src/photos/rond/d39.jpg`) | logo de la maison | site officiel du domaine | page https://www.champagnesolemme.com/ — image <https://www.champagnesolemme.fr/wp-content/uploads/2022/10/champagne-solemme-logo-clair_4D4D4D.png> | 530x275 px → 437 ppi à 40 mm | **autorisation à demander au domaine** |
| 39 | Champagne Solemme | bouteille (`src/photos/bouteille/d39.png`) | bouteille Nature de Solemme | Canva de l'agence « Tarif septembre 2026 », page 42 | `canva/d39-p42-367.png` | 250x750 px → 307 ppi à 24 × 62 mm | photothèque de l'agence |
| 40 | Vazart-Coquart & Fils | rond (`src/photos/rond/d40.jpg`) | la maison de champagne | site officiel du domaine | page https://www.champagnevazartcoquart.com/ — image <https://www.champagnevazartcoquart.com/wp-content/uploads/2020/10/maison-champagne-vazart-coquart.jpg> | 1920x950 px → 603 ppi à 40 mm | **autorisation à demander au domaine** |
| 40 | Vazart-Coquart & Fils | bouteille (`src/photos/bouteille/d40.png`) | bouteille Special Club | Canva de l'agence « Tarif septembre 2026 », page 43 | `canva/d40-p43-382.png` | 466x640 px → 238 ppi à 24 × 62 mm | photothèque de l'agence |
| 41 | Domaine des Sardelles | rond (`src/photos/rond/d41.jpg`) | un vigneron du domaine dans les vignes, noir et blanc | site officiel du domaine | page https://www.domaine-des-sardelles.com/equipe — image <https://static.wixstatic.com/media/3a5ead_85120b5d0c594b03be709c2d85a6894c~mv2.jpg> | 3850x4812 px → 2445 ppi à 40 mm | **autorisation à demander au domaine** |
| 41 | Domaine des Sardelles | bouteille (`src/photos/bouteille/d41.png`) | bouteille de Sancerre rosé du domaine | site officiel du domaine | page https://www.domaine-des-sardelles.com/nos-vins — image <https://static.wixstatic.com/media/3a5ead_dbe252adb1f04ddeb7c1698466241b70~mv2.jpg> | 3911x5867 px → 1776 ppi à 24 × 62 mm | **autorisation à demander au domaine** |

### Récapitulatif par domaine

| n° | Domaine | Rond (40 mm) | Bouteille (24 × 62 mm) |
|---|---|---|---|
| 1 | François Reverdy | portrait du vigneron, noir et blanc — dossier de l'agence, 294 ppi | bouteille de Chinon, 3e de la photo de gamme — dossier de l'agence, 1865 ppi |
| 2 | Domaine de la Barbinière | vendanges dans les vignes du domaine — site du domaine, 1058 ppi | bouteille Les Amphibol — dossier de l'agence, 1634 ppi |
| 3 | Domaine du Colombier / J.Y Bretaudeau | le vigneron au chai — Canva de l'agence, 213 ppi | bouteille Rouge au lèvres — dossier de l'agence, 1605 ppi |
| 4 | Domaine des Noëls | portrait — Canva de l'agence, 631 ppi | bouteille Promenade des Noëls, Anjou blanc — dossier de l'agence, 862 ppi |
| 5 | Chai Berteaud Manceau | les deux fondateurs du chai — site du domaine, 1133 ppi | bouteille du domaine — site du domaine, 1071 ppi |
| 6 | Domaine Jean de Villebois | dans les vignes — Canva de l'agence, 762 ppi | bouteille Pouilly-Fumé Les Silex Blancs — site du domaine, 353 ppi |
| 7 | Divin No Low | vinification en cuverie — site du domaine, 846 ppi | bouteille du domaine — site du domaine, 1025 ppi |
| 8 | Domaine Boehler | logo du domaine — Canva de l'agence, 447 ppi | bouteille Molse blanc — dossier de l'agence, 1036 ppi |
| 9 | Domaine des Nugues | portrait des vignerons — site du domaine, 235 ppi | bouteille Moulin-à-Vent 2022 — dossier de l'agence, 574 ppi |
| 10 | Domaine Sébastien Magnien | portrait au chai, recadré au-dessus du verre — Canva de l'agence, 258 ppi | bouteille Bourgogne Pinot Noir 2023 — dossier de l'agence, 823 ppi |
| 11 | Domaine Nadine Ferrand | les vigneronnes au chai, noir et blanc — dossier de l'agence, 686 ppi | bouteille Mâcon Charnay-lès-Mâcon — dossier de l'agence, 1112 ppi |
| 12 | Maison et Domaine André Goichot | deux portraits de la maison, côte à côte — Canva de l'agence, 312 ppi | bouteille Givry Champ la Dame 2023 — dossier de l'agence, 574 ppi |
| 13 | Château du Cray | le vignoble du Château du Cray (bannière de sa page) — site du domaine, 421 ppi | bouteille Mercurey blanc Les Doues (cuvée absente du tarif) — dossier de l'agence, 272 ppi |
| 14 | Domaine Les Guignottes | nom du domaine sur ses vignes — Canva de l'agence, 337 ppi | bouteille Bourgogne Chardonnay 2023 — dossier de l'agence, 574 ppi |
| 15 | Domaine des Verchères | portrait du vigneron — site du domaine, 1396 ppi | bouteille Mâcon Chardonnay — dossier de l'agence, 1694 ppi |
| 16 | Domaine Le Prieuré des Papes | logo du domaine — Canva de l'agence, 549 ppi | bouteille Châteauneuf-du-Pape Vieilles Vignes — dossier de l'agence, 574 ppi |
| 17 | Domaine de Coyeux | le domaine — Canva de l'agence, 491 ppi | bouteille Les Jumelles, Beaumes-de-Venise — dossier de l'agence, 574 ppi |
| 18 | Domaine du Moulin Blanc | le couple, cadrage élargi (les deux visages entiers), toujours au-dessus du verre — Canva de l'agence, 381 ppi | bouteille de Côtes du Rhône blanc — dossier de l'agence, 667 ppi |
| 19 | Domaine de la Pousterle | vendanges dans les vignes — Canva de l'agence, 365 ppi | bouteille Terroir d'Ansouis blanc 2021 — dossier de l'agence, 823 ppi |
| 20 | Domaine des Pasquiers | portrait de la famille — site du domaine, 914 ppi | bouteille Plan de Dieu 2023 — dossier de l'agence, 574 ppi |
| 21 | Domaine Trichon | les deux vignerons, recadrés sur leurs visages — dossier de l'agence, 878 ppi | bouteille de Mondeuse du Bugey (cuvée du domaine absente du tarif) — dossier de l'agence, 780 ppi |
| 22 | Domaine Stratéus | logo du domaine — site du domaine, 405 ppi | bouteille Madiran Strateus — dossier de l'agence, 1785 ppi |
| 23 | Domaine Haut Marin | logo du domaine — site du domaine, 698 ppi | bouteille N°4 Triton 2024 — dossier de l'agence, 574 ppi |
| 24 | Fabien Castaing | portrait du vigneron dans ses vignes — site du domaine, 1219 ppi | bouteille ADN 24 rouge — Canva de l'agence, 286 ppi |
| 25 | La Passion des Terroirs | portrait de famille d'époque — site du domaine, 435 ppi | bouteille du domaine — site du domaine, 1737 ppi |
| 26 | Château la Gorce | portrait des vignerons — site du domaine, 635 ppi | bouteille La Bonne Résolution 2022 — dossier de l'agence, 671 ppi |
| 27 | Château Falfas | logo du château — dossier de l'agence, 391 ppi | bouteille Château Falfas — Canva de l'agence, 400 ppi |
| 28 | Château Pré la Lande | vendanges au domaine — site du domaine, 406 ppi | bouteille du domaine — site du domaine, 910 ppi |
| 29 | Château Balac | portrait des vignerons — site du domaine, 375 ppi | bouteille Château Balac Haut-Médoc (cuvée absente du tarif) — dossier de l'agence, 574 ppi |
| 30 | Château l’Escarderie | les deux vignerons, deux portraits côte à côte — site du domaine, 312 ppi | bouteille Château l'Escarderie — site du domaine, 394 ppi |
| 31 | Bastide de Blacailloux | borie en pierre sèche du domaine — site du domaine, 1085 ppi | bouteille JOIO rosé — site du domaine, 752 ppi |
| 32 | Famille d’Exea | logo de la maison — site du domaine, 468 ppi | bouteille Jardins de Corbières rouge — dossier de l'agence, 1647 ppi |
| 33 | Famille d’Exea — Jus de Cépages | brebis dans les vignes — Canva de l'agence, 762 ppi | bouteille de jus de Grenache — Canva de l'agence, 358 ppi |
| 34 | Château de Gragnos | grappes à la vigne — site du domaine, 813 ppi | bouteille Lou Daro 2022 — dossier de l'agence, 825 ppi |
| 35 | Domaine Les Lys | logo du domaine — Canva de l'agence, 217 ppi | bouteille Duché — dossier de l'agence, 671 ppi |
| 36 | Prieuré Sainte-Marie d’Albas | les deux vignerons et leur rosé, noir et blanc — dossier de l'agence, 750 ppi | bouteille 4 Saisons 2020 (même image que celle de l'agence, en haute définition) — site du domaine, 472 ppi |
| 37 | Champagne Dekeyne | les deux frères dans les vignes — Canva de l'agence, 914 ppi | bouteille Chardonnay — dossier de l'agence, 574 ppi |
| 38 | Champagne Denis Frézier | le village dans ses vignes — Canva de l'agence, 488 ppi | bouteille Les Trois Crus — dossier de l'agence, 574 ppi |
| 39 | Champagne Solemme | logo de la maison — site du domaine, 437 ppi | bouteille Nature de Solemme — Canva de l'agence, 307 ppi |
| 40 | Vazart-Coquart & Fils | la maison de champagne — site du domaine, 603 ppi | bouteille Special Club — Canva de l'agence, 238 ppi |
| 41 | Domaine des Sardelles | un vigneron du domaine dans les vignes, noir et blanc — site du domaine, 2445 ppi | bouteille de Sancerre rosé du domaine — site du domaine, 1776 ppi |

<!-- images:fin -->

## 2. L'emplacement vide, et ce qu'il faudrait

| n° | Domaine | Emplacement | Pourquoi | Ce qu'il faut |
|---|---|---|---|---|
| 18 | Domaine du Moulin Blanc | bouteille | ni le site du groupe Strasser-Radziwill, ni le Canva, ni le Drive n'en ont ; le « Catalogue VSR.pdf » joint au mail de Strasser-Radziwill du 4 juin 2025 en contient sans doute, mais une pièce jointe de mail ne se lit pas d'ici | une bouteille détourée (PNG transparent) ou sur fond uni, au moins 488 px de haut ; ou ce PDF déposé dans le Drive |

**À savoir, n°21 Domaine Trichon.** Le site du domaine ne montre que ses vins du Bugey
(Mondeuse, Pinot Noir, Altesse, Chardonnay…), aucun de ses Côtes du Rhône ou Vacqueyras du
tarif. La bouteille posée est une Mondeuse du Bugey : c'est bien le domaine, et notre texte
cite la Mondeuse, mais cette cuvée n'est pas au tarif. Pour la retirer, il suffit d'effacer
sa ligne dans `data/photos-locales.json`.

### Dossiers de l'agence qui ne correspondent à aucun des 40 domaines

Ignorés, rien n'en est tiré. `Bouteilles_de_vin/` : Chateau_Daugay, Chateau_David_Beaulieu,
Chateau_de_Set, Chateau_Fourcas-Borie, Chateau_Jalousie_Beaulieu, Chateau_La_Croix_Saint-Vincent,
Chateau_Lagrave, Chateau_Le_Coteau, Chateau_Mouresse, Chateau_Pascaud, Chateau_Queyssard,
Champagne_JM_Gobillard_et_Fils, Champagne_Leguedard, Domaine_Augeron, Domaine_Charpentier,
Domaine_de_la_Motte, Domaine_du_Rochouard, Fleur_des_Marguis, New_folder.
`Domaines_et_vignerons/` : Chateau_de_la_Rairie_lieu_salon, Chateau_Mouresse,
Domaine_Charpentier, Domaine_de_la_Motte, _A_identifier. Le dossier `_A_verifier` n'a pas
été ouvert.

## 3. Le logo de l'Agence SCIO

`sources/logo-agence-scio.jpg` — fourni par l'agence. JPG CMJN, 1030 × 251 px.

| Fichier | Transformation |
|---|---|
| `src/images/logo-agence-scio-srgb.png` | conversion CMJN → sRGB |
| `src/images/logo-agence-scio-detoure.png` | conversion sRGB **et** fond blanc rendu transparent (seuil 243/255) — le dessin n'est pas touché |

Posé sur la couverture, la page de l'agence et la dernière page, à sa proportion native, avec
une marge libre supérieure à la hauteur de son carré jaune. Ni recoloré, ni déformé, ni rogné,
ni ombré.

**Limite à connaître :** à 300 dpi, le fichier fourni ne dépasse pas **87 mm de large**. Il est
utilisé à 62, 74 et 70 mm — dans les clous, mais sans marge. Pour plus grand, il faut du
vectoriel (PDF, SVG, EPS ou AI). C'est dans `QUESTIONS.md`.

## 4. Illustrations

Tout le reste est **dessiné pour ce catalogue**, en SVG, dans ce dépôt
(`src/gabarits/pieces.mjs` et `src/gabarits/pages.mjs`) : coupes de sol, trames de strates,
carottes de région, anneaux des ronds, pictogrammes de type de vin et de label. Les dessins
génératifs sont tirés d'une **graine fixe** : une même entrée donne toujours le même dessin,
édition après édition. **Aucune bibliothèque d'icônes.**

## 5. Pictogrammes

Les pictogrammes de type de vin et les jetons de mention **sont dessinés par l'agence**.
Ils ne reproduisent **aucun logo officiel** d'organisme certificateur — ni AB, ni Eurofeuille,
ni HVE, ni Demeter, ni Biodyvin, ni AOP, ni IGP. L'information que ces logos portent est reprise
(c'est du contenu, lu dans le tarif source) ; leur forme, non. La page 3 l'écrit, et la légende
le répète en pied de chaque fiche.

## 6. Polices

Toutes sous licence **SIL Open Font License (OFL)**, récupérées via les paquets npm
`@fontsource` et **copiées dans `src/fonts/`** : la fabrication ne dépend d'aucun accès réseau.

| Police | Rôle |
|---|---|
| **Young Serif** | titres, noms de domaine, ouvertures de région |
| **Spectral** | textes de présentation |
| **IBM Plex Sans** | tableaux, paliers, légendes (chiffres tabulaires) |

Les six autres familles de `src/fonts/` servent aux maquettes des concepts 2 et 3, pas au
catalogue final.


## Photos de régions (Wikimedia Commons, licences libres, 3 octobre 2026)

Paysages viticoles illustrant une région, jamais un domaine précis. Crédit obligatoire en dernière page.

| Région | Page | Image | Auteur | Licence |
|---|---|---|---|---|
| Loire | https://commons.wikimedia.org/wiki/File:Sancerre_-_View_on_vineyards_-_2.jpg | https://upload.wikimedia.org/wikipedia/commons/0/00/Sancerre_-_View_on_vineyards_-_2.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Benjamin Smith | CC BY-SA 4.0 |
| Alsace | https://commons.wikimedia.org/wiki/File:Kaysersberg_Vignoble_c_2011.jpg | https://upload.wikimedia.org/wikipedia/commons/8/88/Kaysersberg_Vignoble_c_2011.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | JLPC | CC BY-SA 3.0 |
| Beaujolais | https://commons.wikimedia.org/wiki/File:Coucher_de_soleil_sur_les_vignobles_du_Beaujolais.jpg | https://upload.wikimedia.org/wikipedia/commons/0/0d/Coucher_de_soleil_sur_les_vignobles_du_Beaujolais.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Sebleouf | CC BY-SA 4.0 |
| Bourgogne | https://commons.wikimedia.org/wiki/File:IMG_Vignoble_%C3%A0_Pommard.JPG | https://upload.wikimedia.org/wikipedia/commons/c/cd/IMG_Vignoble_%C3%A0_Pommard.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Mpmpmp | CC BY-SA 3.0 |
| Rhône | https://commons.wikimedia.org/wiki/File:Dentelles_de_Montmirail_vue_du_Plan_de_Dieu.JPG | https://upload.wikimedia.org/wikipedia/commons/f/f2/Dentelles_de_Montmirail_vue_du_Plan_de_Dieu.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Véronique PAGNIER | Public domain |
| Sud-Ouest | https://commons.wikimedia.org/wiki/File:Vins_du_Sud-ouest,_en_Gascogne.jpg | https://upload.wikimedia.org/wikipedia/commons/5/5e/Vins_du_Sud-ouest%2C_en_Gascogne.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Interprofession des Vins du Sud-Ouest | CC BY-SA 4.0 |
| Bordeaux | https://commons.wikimedia.org/wiki/File:Saint-Emilion,_vignoble_3.jpg | https://upload.wikimedia.org/wikipedia/commons/6/61/Saint-Emilion%2C_vignoble_3.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Pascal MOULIN | CC BY-SA 4.0 |
| Provence | https://commons.wikimedia.org/wiki/File:Puyloubier-FR-13-vignes_et_Mont_Venturi-a2.jpg | https://upload.wikimedia.org/wikipedia/commons/8/87/Puyloubier-FR-13-vignes_et_Mont_Venturi-a2.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | François GOGLINS | CC BY-SA 4.0 |
| Languedoc | https://commons.wikimedia.org/wiki/File:Village_de_Saint-Chinian,_vue_sur_le_vignoble.jpg | https://upload.wikimedia.org/wikipedia/commons/a/a1/Village_de_Saint-Chinian%2C_vue_sur_le_vignoble.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | Gaylord Burguière | CC BY 4.0 |
| Champagne | https://commons.wikimedia.org/wiki/File:Blick_von_Ch%C3%A2tillon-sur-Marne_%C3%BCber_die_Weinberge_der_Champagne_06.jpg | https://upload.wikimedia.org/wikipedia/commons/2/20/Blick_von_Ch%C3%A2tillon-sur-Marne_%C3%BCber_die_Weinberge_der_Champagne_06.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original | JensKunstfreund | CC BY-SA 4.0 |
| Bugey (catalogue caviste global, 8 oct. 2026) | https://commons.wikimedia.org/wiki/File:Des_vignes_%C3%A0_Saint-Sorlin-en-Bugey_(ao%C3%BBt_2020).jpg | https://upload.wikimedia.org/wikipedia/commons/0/0c/Des_vignes_%C3%A0_Saint-Sorlin-en-Bugey_%28ao%C3%BBt_2020%29.jpg | Benoît Prieur | CC0 |
