# Audit complet du catalogue « Vins & Champagnes » — Problèmes & Solutions

**Compilation structurée de l'ensemble des analyses réalisées sur les deux versions du catalogue de l'Agence SCIO** (« Copie de Tarif — septembre 2026 », la version tarif dense en fond gris, et « catalogue écran », la version 52 pages à charte crème/bordeaux avec onglets régionaux), **édition septembre 2026**.

Ce document reprend l'intégralité des problèmes relevés et des solutions proposées lors de plusieurs passes d'audit distinctes (analyse rapide, audit conversationnel détaillé, audit juridique et technique formel, audit technique mesuré au pixel/point près, et plan de refonte par paliers), sans en retirer aucun point. Il est réorganisé par thème plutôt que par ordre chronologique d'analyse, pour que chaque problème soit immédiatement suivi de la ou des solutions qui lui correspondent.

**Sommaire**

1. Verdicts globaux et diagnostics d'ensemble
2. Chantier 1 — Tarifs, grilles de prix et données commerciales
3. Chantier 2 — Direction artistique, mise en page et lisibilité
4. Chantier 3 — Photos, packshots et identité visuelle des bouteilles
5. Chantier 4 — Merchandising, hiérarchie commerciale et storytelling
6. Chantier 5 — Contenu œnologique et données B2B
7. Chantier 6 — Erreurs textuelles, coquilles et incohérences (relevé exhaustif)
8. Chantier 7 — Navigation, sommaire, index et outils PDF/digital
9. Chantier 8 — Conformité juridique et réglementaire
10. Plan d'action consolidé et feuilles de route de priorisation
11. Annexe — Sources consultées

---

## 1. Verdicts globaux et diagnostics d'ensemble

### 1.1 Les verdicts, tels qu'exprimés dans chaque analyse

- **Verdict n°1 :** *« Ce document n'est pas un outil de vente, c'est une liste de données mal déguisée. »* Un bon catalogue est un outil de vente ; celui-ci est un obstacle. Il dessert l'image des vignerons qu'il est censé promouvoir. Conclusion : reprendre à zéro — définir une charte graphique, structurer l'information par région et par gamme, aérer la mise en page, augmenter la taille des polices, penser à l'expérience du lecteur.

- **Verdict n°2 (audit conversationnel détaillé, 52 pages analysées) :** *« Un très bon tarif commercial maquillé en catalogue éditorial. »* Le document est propre, cohérent, sérieux, mais ne donne pas assez envie d'acheter. Il dit *« Voici notre liste tarifaire de 40 domaines »* alors que l'intro promet une sélection *« riche et audacieuse »* de 40 domaines et 10 régions — *« Voici une sélection de producteurs que vous devez absolument découvrir »*. C'est l'écart entre les deux qui est le principal problème. Point important : le catalogue a une bonne base éditoriale (structure identité → conditions → tableau, sommaire clair, typographie déjà logique) — il ne faut donc **pas tout détruire**, mais garder le moteur commercial et lui ajouter une vraie direction artistique de catalogue premium. Deux anomalies de prix plus graves qu'un problème esthétique ont été détectées (voir Chantier 1).

- **Verdict n°3 (audit juridique et technique formel, « déconstruction méthodique ») :** *« Effondrement structurel complet. »* L'examen exhaustif des 52 pages du catalogue « Tarifs cavistes Vendée (85) » met en lumière : des fautes d'exécution graphique intolérables, des aberrations mathématiques dans les grilles tarifaires qui pénalisent l'acheteur au volume, une absence totale d'informations organoleptiques indispensables, une chaîne de navigation brisée qui occulte des pans entiers de l'assortiment, et une série d'infractions manifestes au Code de commerce et au Code de la santé publique. Conclusion : *« L'édition de septembre 2026 des Tarifs cavistes Vendée de l'Agence SCIO constitue une faillite éditoriale, commerciale et technique totale »* ; retrait immédiat du circuit de diffusion recommandé, plan de redressement en quatre axes (voir section 10).

- **Verdict n°4 (audit technique mesuré : polices, couleurs, résolutions, contrastes) :** *« Ce n'est pas un catalogue, c'est un tableur habillé en beige. Il a été pensé pour l'imprimante, fabriqué par un navigateur web et envoyé comme "PDF écran". »* Le fichier vient de Chromium (moteur Skia/PDF) : c'est une page web imprimée en PDF, pas un document monté dans un logiciel de mise en page. Le document essaie d'être à la fois un livre de marque et un tarif, et échoue sur les deux : il informe mal (données trouées), ne persuade pas (rien ne ressort, photos bancales) et complique la décision (21 grilles de prix différentes).

### 1.2 Diagnostic élément par élément (grille de notation 🟢🟡🔴)

| Élément | Diagnostic |
|---|---|
| Format A4 | 🟢 Très bon |
| Grille | 🟢 Solide |
| Typographie (logique de style) | 🟢 Bonne |
| Cohérence graphique | 🟢 Très bonne |
| Sommaire (principe) | 🟢 Très bon |
| Navigation PDF (liens) | 🟢 Bonne |
| Identité SCIO | 🟢 Cohérente |
| Couleurs | 🟡 Trop sages |
| Couverture | 🟡 Jolie mais générique |
| Photos | 🟡 Potentiel sous-exploité |
| Mise en valeur des bouteilles | 🔴 Insuffisante |
| Variété des pages | 🔴 Trop répétitive |
| Hiérarchie commerciale | 🔴 Insuffisante |
| Taille des tableaux | 🟡 Trop petite en usage digital |
| Espaces vides | 🔴 Souvent mal exploités |
| Storytelling | 🟡 Correct mais générique |
| Aide à la vente | 🔴 Trop faible |
| Informations B2B | 🟡 Incomplètes |
| Bon de commande | 🟡 Fonctionnel mais basique |
| Version digitale | 🟡 Encore trop « PDF imprimé » |
| Qualité image de couverture | 🔴 À revoir pour impression |
| Données tarifaires | 🔴 2 anomalies à vérifier |
| Palier « 301 bt » | 🟠 À vérifier |

### 1.3 Tableau de bord comparatif (pratiques de référence vs catalogue SCIO)

| Paramètre d'audit | Pratiques de référence (catalogues B2B vins) | Catalogue Agence SCIO (édition septembre 2026) | Diagnostic d'impact commercial |
|---|---|---|---|
| Identité de marque | Bloc-marque vectorisé, zone d'exclusion protégée, stabilité nominale absolue | Raison sociale déformée à 6 reprises : ACENCE, HAGENCE, AVINSA, AVINSREPIRITS | Ruine totale de l'image de marque et suspicion d'amateurisme |
| Imagerie produit | Packshots bouteilles détourés en haute définition (300 DPI), valorisation de l'habillage | 0 packshot bouteille sur l'ensemble des pages, absence d'illustration des flacons | Impossibilité de juger du standing esthétique des bouteilles en rayon |
| Structure tarifaire | Paliers dégressifs constants récompensant les volumes (palette < vrac) | Paliers inversés sur des dizaines de lignes : le prix monte avec la quantité commandée | Destruction de la relation de confiance et paralysie des ventes volumiques |
| Ergonomie des BIB | Tableaux distincts, contenances ordonnées, couleurs et cépages explicites | Formats 10 L et 5 L aux tarifs croisés erratiques, 3 références de BIB sans mention de couleur | Offre inexploitable générant des erreurs de saisie de commande |
| Cohérence des données | Séparateur décimal uniforme (virgule française), alignement vertical strict | Alternance arbitraire de virgules et de points au sein des mêmes tableaux | Image d'improvisation et absence d'outils de gestion structurés |
| Architecture du document | Sommaire exhaustif, onglets de découpage géographique, index alphabétique exact | 4 pages majeures « zappées » (18, 30, 33, 41), index alphabétique pollué par des chiffres | Perte de visibilité sur les appellations les plus lucratives de la gamme |
| Confort de lecture | Utilisation maîtrisée des blancs tournants, 2 à 3 couleurs coordonnées, corps lisibles | Fonds saturés continus, micro-corps sous 7 pt, contrastes insuffisants, titrages brisés | Fatigue oculaire immédiate et rejet du support par les acheteurs |
| Contenu œnologique | Pourcentages d'encépagement, terroir, élevage, profil gustatif, potentiel de garde | Paragraphes promotionnels vagues, aucune donnée de vinification, aucun conseil sommelier | Déficit d'aide à la vente auprès des clients finaux du caviste |
| Conformité juridique | CGV intégrées, forme juridique, capital, TVA, mention Évin correcte, logo Triman | Pas de CGV, forme et capital omis, TVA absente, mention santé corrompue (« acoolest ») | Vulnérabilité pénale, amendes de 750 € et risques de contentieux clients |


### 1.4 Constats de la première passe rapide (à recouper avec les relevés détaillés)

Première analyse, plus générale, organisée en six thèmes. Ses constats sont repris en détail dans les chantiers suivants ; les points formulés à ce stade sont conservés ici tels quels :

- **Design général :** aucune charte graphique cohérente ; absence d'identité visuelle (seuls éléments graphiques : photos de vignerons en noir et blanc de qualité inégale, étiquettes de bouteilles collées sans logique) ; hiérarchie visuelle inexistante (prix, cuvée et région impossibles à distinguer, tout noyé dans un flux continu).
- **Typographie :** tailles de police microscopiques dans les tableaux de prix (< 6 pt estimés, pour une taille idéale de 8 à 10 pt) ; densité de texte extrême, interlignage insuffisant (110 % minimum recommandé), aucune « zone de respiration ».
- **Mise en page :** produits non regroupés logiquement (par type, région, prix) ; **le sommaire, qui liste les domaines par région, n'est pas respecté dans les pages suivantes** ; tableaux illisibles et incohérents (en-têtes répétitifs et mal alignés) ; **certains tableaux coupés sur plusieurs pages** (ex. Domaine des Pasquiers p. 26) ; bon de commande (p. 51) inutilisable — tableau quasiment vide, sans prix, références ni paliers de remise.
- **Couleurs :** utilisées sans codification (une couleur par région ou par type de vin permettrait de coder l'information) ; **fonds blancs omniprésents** jugés fades ; couleurs de police sans logique (prix parfois en rouge, parfois en noir).
- **Contenu et règles commerciales :** absence de storytelling (blocs standardisés « Situé à… », « La famille… », aucun bénéfice client, aucun récit) ; photos de vignerons souvent floues, mal cadrées ou pixelisées, et usage de noir et blanc « dénaturant l'aspect réel » (motif de refus sur certaines plateformes professionnelles) ; erreurs et incohérences (fautes de frappe dans « Maison André Goichot » et « Domaine des Pasquiers », appellations erronées comme « Côtes du Rhône Villages Sablet » au lieu de « Sablet », informations manquantes comme « N°10 effervescent » sans détail).
- **Conclusion :** catalogue à refaire de fond en comble — charte graphique, structuration par région et par gamme, mise en page aérée, polices plus grandes, expérience du lecteur.

### 1.5 Points de désaccord ou de nuance entre les analyses (à arbitrer)

Les différentes passes ne sont pas toujours d'accord ; ces écarts sont conservés pour arbitrage lors de la refonte :

| Sujet | Position A | Position B |
|---|---|---|
| **Fonds et couleurs** | Fonds trop saturés/agressifs à supprimer au profit de blanc ou ivoire très pâle ; 2 à 3 teintes maximum (audit formel) | Palette déjà trop sage et couleurs sous-exploitées comme outil de merchandising ; renforcer l'identité régionale par accents (audit conversationnel). La première passe demande aussi des nuances très légères (gris clair, beige) pour délimiter les fiches |
| **Couleurs régionales** | Un bandeau bleu pour la Loire, vert pour l'Alsace (première passe) | Loire en vert sauge/ivoire, Bourgogne en bordeaux profond/pierre, Rhône en terracotta/sable, Champagne en champagne clair/noir/or, Bordeaux en prune/pierre/brun (audit conversationnel) |
| **Format de page** | A4 est un très bon choix, ne pas le changer (audit conversationnel) | Première passe : passer à A4 pour les pages de prix « si le A5 est trop petit » ; audit technique : le format vertical est inadapté à l'écran, préférer le paysage pour la version numérique |
| **Uniformité des fiches** | Uniformiser strictement les fiches domaines pour créer un rythme professionnel (première passe) | Trop de répétition : garder la grille comme squelette mais autoriser 3-4 compositions différentes (types A/B/C/D) |
| **Typographie** | Typographie « désastre » (première passe et audit formel) | La logique typographique (serif titres, sans-serif info) est plutôt bonne, ne pas tout changer : travailler tailles, interlignage, contraste, hiérarchie (audit conversationnel) |
| **Navigation** | Chaîne de navigation « brisée » (audit formel : sommaire et index faux) | Navigation « bonne » sur le principe : liens cliquables présents ; il manque surtout les signets PDF (audit conversationnel) |
| **Taille des tableaux** | Corps < 6-7 pt (audit formel, première passe) | Environ 7,5 pt ; 8,7 pt condensé selon la mesure fine — trop petit pour un usage digital plutôt qu'« illisible » en impression A4 |
| **Cas des paliers** | Dizaines de paliers inversés (audit formel, relevé exhaustif) | Deux anomalies principales identifiées à vérifier : Verchères p. 21, Pousterle p. 25 (audit conversationnel) |

Ces divergences tiennent en partie au fait que les analyses ne portent pas toutes sur exactement la même version du fichier ni sur le même degré de rigueur de mesure : il est recommandé de **re-vérifier chaque point contre le fichier de référence** avant de le retenir comme correctif.


---

## 2. Chantier 1 — Tarifs, grilles de prix et données commerciales

### 2.1 Problèmes constatés

#### 2.1.1 L'aberration de la dégressivité inversée : la surtaxation du volume d'achat

Principe universel du commerce interentreprises : une hausse du volume unitaire commandé doit déclencher une baisse mécanique du prix de revient de la bouteille. Dans ce tarif, une multitude de grilles fonctionnent selon une logique inverse : l'achat de quantités supérieures entraîne un **surcoût** unitaire pour le caviste. Relevé exhaustif des lignes concernées :

| Page | Domaine | Cuvée / Format | Palier inférieur (prix HT) | Palier supérieur (prix HT) | Nature de l'aberration |
|---|---|---|---|---|---|
| p. 6 | François Reverdy | Anjou Blanc Schistes Vert, 75 cl | Dès 48 bt : 12,25 € | Dès 120 bt : 13,25 € | Hausse de +1,00 €/col imposée au palier supérieur |
| p. 6 | François Reverdy | Saumur Blanc Tuffeau, 75 cl | Dès 48 bt : 13,50 € | Dès 120 bt : 14,50 € | Pénalisation de +1,00 €/col pour un volume triplé |
| p. 6 | François Reverdy | Quincy Graves Argileuses, 75 cl | Dès 48 bt : 16,50 € | Dès 120 bt : 17,85 € | Surtaxe de +1,35 €/col au palier supérieur |
| p. 6 | François Reverdy | IGP Val de Loire Les Soudannes, 75 cl | Dès 48 bt : 9,25 € | Dès 120 bt : 9,50 € | Surtaxe de +0,25 €/col pour un volume de 120 cols |
| p. 17 | Maison André Goichot | Saint-Bris Blanc, 75 cl | Dès 78 bt : 6,90 € | Dès 126 bt : 7,20 € | Pénalisation de +0,30 €/col pour engagement accru |
| p. 17 | Maison André Goichot | Petit Chablis Blanc, 75 cl | Dès 78 bt : 9,30 € | Dès 126 bt : 9,60 € | Majoration de +0,30 €/col au palier supérieur |
| p. 17 | Maison André Goichot | Rully Rouge, 75 cl | Dès 78 bt : 14,90 € | Dès 126 bt : 15,20 € | Majoration unitaire de +0,30 €/col dès 126 cols |
| p. 17 | Maison André Goichot | Saint-Romain Rouge, 75 cl | Dès 78 bt : 15,90 € | Dès 126 bt : 16,20 € | Majoration unitaire de +0,30 €/col dès 126 cols |
| p. 21 | Domaine des Verchères | Mâcon Chardonnay Blanc, 75 cl | Dès 180 bt : 5,45 € | Dès 300 bt : 5,75 € | Surcoût de +0,30 €/col à l'achat de 300 bouteilles |
| p. 22 | Domaine du Prieuré des Papes | Châteauneuf-du-Pape Blanc, 75 cl | Dès 300 bt : 20,90 € | Commande Palette : 21,20 € | La palette complète coûte 0,30 €/col plus cher |
| p. 22 | Domaine du Prieuré des Papes | Châteauneuf-du-Pape Rouge, 75 cl | Dès 300 bt : 18,00 € | Commande Palette : 18,30 € | La palette complète coûte 0,30 €/col plus cher |
| p. 23 | Domaine de Coyeux | Gigondas Rouge, 75 cl | Dès 300 bt : 11,90 € | Commande Palette : 12,20 € | Surtaxe palette de +0,30 €/col |
| p. 23 | Domaine de Coyeux | Muscat Beaumes Solera, 75 cl | Dès 300 bt : 6,00 € | Commande Palette : 6,30 € | Surtaxe palette de +0,30 €/col |
| p. 23 | Domaine de Coyeux | Muscat Beaumes Vintage, 75 cl | Dès 300 bt : 9,00 € | Commande Palette : 9,30 € | Surtaxe palette de +0,30 €/col |
| p. 25 | Domaine de la Pousterle | Luberon Rosé, 75 cl | Dès 300 bt : 4,75 € | Commande Palette : 5,00 € | Surtaxe palette de +0,25 €/col |
| p. 25 | Domaine de la Pousterle | VDF Syrah Rouge, 75 cl | Dès 300 bt : 4,50 € | Commande Palette : 4,75 € | Surtaxe palette de +0,25 €/col |
| p. 25 | Domaine de la Pousterle | Luberon Rouge, 75 cl | Dès 198 bt : 5,00 € / Palette : 5,00 € | Dès 300 bt : 5,25 € | Pic de prix absurde sur le palier intermédiaire |
| p. 27 | Domaine Trichon | Vacqueyras Blanc, 75 cl | Dès 300 bt : 8,68 € | Dès 600 bt : 9,12 € | Surcoût de +0,44 €/col à partir de 600 cols |
| p. 27 | Domaine Trichon | Côtes du Rhône Rouge, 75 cl | Dès 300 bt : 4,54 € | Dès 600 bt : 4,67 € | Surcoût de +0,13 €/col à partir de 600 cols |
| p. 34 | Château La Gorce | Médoc — 11 cuvées de la gamme (ex. Canteloup) | Dès 120 bt : ex. 4,95 € | Dès 300 bt : 5,05 € | Majoration systématique de +0,10 €/col sur toute la grille |

Le cas du **Château La Gorce (p. 34)** illustre l'ampleur du problème : les onze cuvées proposées subissent **toutes** une hausse de dix centimes par col en passant du palier 120 au palier 300 bouteilles. La gestion des commandes à la palette pour les quatre domaines du **groupe Strasser-Radziwill (p. 22 à 25)** pénalise systématiquement l'achat logistique le plus optimisé (la palette complète), le rendant plus onéreux que l'expédition fragmentée.

Deux occurrences déjà repérées dans l'analyse conversationnelle comme les plus suspectes (avant le recensement exhaustif ci-dessus) :
- **Domaine des Verchères — p. 21** : 6,10 € → 5,45 € → 5,75 € pour dès 120 → dès 180 → dès 300 bt : le prix baisse, puis remonte.
- **Domaine de la Pousterle — p. 25** : 5,00 € → 5,25 € → 5,00 € : même anomalie, sur la dernière référence de la page.

#### 2.1.2 « 301 bt » : un palier atypique à vérifier

Domaine Boehler (conditions) : « dès 60 · 120 · **301** bt ». 301 bouteilles est suffisamment inhabituel pour interroger : n'est-ce pas plutôt 300 ? Ce n'est peut-être pas une erreur (condition contractuelle particulière possible), mais un lecteur se demandera naturellement pourquoi 301 et pas 300.

#### 2.1.3 Désorganisation des colonnes de données et collisions d'en-têtes

Absence complète de rigueur dans le paramétrage des grilles : fusions et permutations anarchiques des en-têtes de paliers.

| Page | Domaine | Défaut observé |
|---|---|---|
| p. 6 | François Reverdy | En-tête fusionnée sans délimitation : « jusqu'à 36 bt \| dès 120 dès 48 bt bt » — impossible de savoir quelle colonne correspond à quel palier |
| p. 9 | Domaine des Noëls | Ordre d'incrémentation renversé : « dès 120 bt \| dès 360 bt dès 240 bt » (le palier maximal précède l'intermédiaire) |
| p. 14 | Domaine des Nugues | Même inversion : « dès 60 bt \| dès 240 bt dès 120 bt » |
| p. 28 | Domaine Stratéus | Même inversion : « dès 36 bt \| dès 120 bt dès 60 bt » |
| p. 29 | Domaine Haut Marin | Même inversion : « dès 72 bt \| dès 600 bt dès 300 bt » |
| p. 39 | Bastide de Blacailloux | Même inversion : « dès 60 bt \| dès 180 bt dès 120 bt » |
| p. 47 | Champagne Denis Frézier | Même inversion : « dès 66 bt \| dès 186 dès 126 bt bt » |
| p. 48 | Champagne Solemme | Accident le plus destructeur : la ligne d'en-tête absorbe la première référence du domaine — l'intitulé de colonne et les spécifications de la cuvée « Terre de Solemme » se retrouvent amalgamés dans une cellule unique, mêlant intitulés de colonnes, millésime, format et prix |
| p. 42 | Famille d'Exea — Jus de cépages | La barre de conditions indique « dès 300 » alors que le tableau indique « dès 320 » |

#### 2.1.4 La débâcle des Bag-in-Box (BIB)

- **Page 8 — Domaine du Colombier :** le tableau BIB présente deux colonnes (10 L puis 5 L). Ligne Sauvignon : 10 L = 12,50 €, 5 L = 19,40 €. Ligne Merlot : les prix sont inversés, 10 L = 19,40 €, 5 L = 12,50 €. Ligne Cabernet Rosé : 10 L = 18,40 €, 5 L = 11,50 €. Ligne Cabernet Rouge : rebascule à 10 L = 12,50 €, 5 L = 19,40 €. Impossible pour un caviste de savoir si le 10 L est structurellement deux fois moins cher que le 5 L, ou si les données ont simplement été permutées par erreur.
- **Page 41 — Famille d'Exea :** trois lignes strictement identiques « Pergola d'Exea » en BIB 5 L, colonne couleur totalement vide, sans précision de cépage : trois montants identiques pour des produits rigoureusement anonymes (les couleurs Blanc/Rosé/Rouge ont disparu).

#### 2.1.5 L'anarchie des séparateurs décimaux

Règle de typographie financière française : virgule décimale exclusive, alignement vertical sur le signe décimal. Le document alterne arbitrairement points et virgules :
- **Page 6 (François Reverdy) :** 10.00 côtoie 9,25 et 9.50.
- **Page 13 (Domaine Boehler) :** la grille bascule de 15,40 à 14.90 puis 14.20.
- **Page 37 (Château Balac) :** une seule ligne mélange 6,40 / 6.30 / 6,20 / 6,10 / 6,00.
- **Page 47 (Champagne Denis Frézier) :** les dix références oscillent continuellement d'un standard à l'autre.

Ce défaut trahit une saisie manuelle sans masque de saisie ni import automatisé depuis un progiciel de gestion.

#### 2.1.6 Paliers bancals (trous, chevauchements, paliers inutiles, colonnes à géométrie variable)

- **Trous et chevauchements :** chez Reverdy, rien n'est prévu entre 37 et 47 bouteilles. Chez Balac, 120 bouteilles tombent à la fois dans « jusqu'à 120 » et « dès 120 ». Boehler a un palier à 301 quand tout le monde dit 300 (voir 2.1.2).
- **Paliers inutiles :** chez les Noëls, la colonne « dès 360 » est identique à « dès 240 » sur les 9 lignes. Chez Goichot, Cray et Guignottes, 31 lignes sur deux colonnes servent à afficher une remise uniforme de 0,30 €/bouteille — sur le Clos Vougeot à 138 €, cela représente 0,2 % : une phrase aurait suffi. Chez Balac, cinq colonnes de prix pour des marches de 10 à 20 centimes.
- **Inversions :** page 21, le Mâcon Chardonnay coûte 5,45 € dès 180 bouteilles mais 5,75 € dès 300 (déjà cité en 2.1.1). Page 25, le Luberon rouge passe de 5,00 € à 5,25 € en montant de 198 à 300 bouteilles.
- **Colonnes à géométrie variable :** les colonnes de prix désignent tantôt des paliers de quantité, tantôt des formats (5 L / 10 L au Colombier), tantôt des nombres de BIB (chez Exea), sans que la mise en forme du tableau ne change pour le signaler.
- **Absence de prix pour les petites quantités :** 25 domaines sur 40 n'affichent **aucun prix** sous leur premier seuil, qui va de 36 à 300 bouteilles selon les domaines. Un caviste qui veut deux cartons ne connaît pas son prix. Chez Exea, le transport est offert dès 72 bouteilles… mais les prix ne commencent qu'à 144.
- **Diversité des seuils :** 27 domaines sur 40 ont des paliers, répartis sur 21 grilles différentes ; les 13 autres sont en prix unique. On compte une vingtaine de seuils distincts et non harmonisés : 36, 48, 60, 66, 72, 78, 90, 96, 120, 126, 144, 180, 186, 198, 240, 300, 301, 320, 360 et 600 bouteilles, plus une mention « palette » jamais définie précisément.

#### 2.1.7 Opacité des conditions logistiques et transport

Sur la quasi-totalité des pages, la barre de conditions se borne à mentionner « Port en sus » sans grille de tarification kilométrique, forfait au carton ou barème par tranche de poids. Le caviste ne peut pas calculer son coût de revient unitaire au col. Pour le **Domaine Boehler (p. 13)** et **La Passion des Terroirs (p. 32)**, la mention « Port : Sur demande » ajoute une friction supplémentaire. Au global, **26 domaines sur 40** sont « port en sus » ou « sur demande », sans le moindre montant. Il n'y a par ailleurs ni date de validité des prix, ni délai de livraison, ni conditions de paiement précisées.

#### 2.1.8 Mention « Allocation » apposée sans règle

Le badge « Allocation » est apposé arbitrairement sur plusieurs domaines de prestige — **Sébastien Magnien (p. 15), Nadine Ferrand (p. 16), Maison Goichot (p. 17), Stratéus (p. 28)** — sans qu'aucune règle de contingentement, aucun historique de compte, ni aucun seuil maximal de commande par point de vente ne soit défini. Cette mention fonctionne comme un artifice marketing flou qui complique la gestion des stocks plutôt que d'organiser une distribution sélective rigoureuse.

#### 2.1.9 Bon de commande inadapté au volume de l'offre

Le bon de commande (p. 51) offre seulement **22 lignes pour environ 370 références** réparties sur 40 domaines. Il n'a :
- aucune ligne de total (HT, port, TTC) ;
- aucune case pour vérifier si le franco ou le palier de prix est atteint ;
- une colonne « quantité (bt) » qui ne convient pas aux formats BIB ;
- et il ne se remplit pas à l'écran (aucun champ de formulaire PDF).

Sur le plan financier, aucune colonne ne permet de calculer le sous-total HT, la ventilation par taux de TVA (écart entre boissons alcoolisées et jus de fruits), le montant des frais de livraison ou le total TTC. Aucune zone de validation légale : pas de date d'engagement, de signature autorisée, de cachet d'entreprise « Bon pour accord », ni de rappel des modes et échéances de paiement.

### 2.2 Solutions proposées

#### 2.2.1 Corrections immédiates (palier « 0 » — avant même de parler de direction artistique)

| Problème | Solution |
|---|---|
| Prix incohérents ou suspects | Vérification automatique de tous les paliers. Exemple : Domaine des Verchères 6,10 → 5,45 → 5,75 €, ce qui casse la logique de remise progressive |
| Autre anomalie tarifaire | Vérifier Domaine de la Pousterle : 5,00 → 5,25 → 5,00 €. Même problème potentiel |
| Palier « 301 bt » | Vérifier pourquoi 301 et non 300 (Domaine Boehler : « dès 60 · 120 · 301 bt ») |
| Format « — » | Vérifier chaque ligne où le format n'est pas renseigné ; le mode d'emploi du catalogue précise lui-même qu'il doit y avoir une ligne par cuvée et par format |
| Cohérence des paliers | Règle automatique : plus la quantité augmente, plus le prix doit être égal ou inférieur, sauf justification explicite et signalée |
| Uniformité des unités | Standardiser partout la formulation des seuils : 48 bt, 120 bt, 1 palette, BIB 3 L, etc. |
| Noms de cuvées | Vérification orthographique et typographique globale : accents, capitales, tirets, millésimes, appellations |
| Mentions légales | Garder les mentions nécessaires, mais revoir leur intégration graphique plutôt que les laisser peser visuellement sur chaque page |

**Objectif du palier 0 :** zéro anomalie de données + zéro incohérence typographique + zéro information ambiguë. C'est le palier le plus important, car un beau catalogue avec une erreur de prix reste un mauvais catalogue commercial.

#### 2.2.2 Assainissement mathématique et automatisation des tarifs (axe prioritaire du plan d'action final)

- **Rétablir la règle économique de la dégressivité :** les prix doivent impérativement diminuer au fil des paliers de volume. La commande à la palette doit systématiquement offrir le prix de revient unitaire le plus bas de la grille, jamais un surcoût pénalisant.
- **Centraliser sur un outil PIM ou tableur verrouillé :** interdire la saisie manuelle libre des prix sur la maquette. L'import des données dans le logiciel de PAO (InDesign) doit se faire via des flux automatisés (scripts ou base de données unifiée) pour éviter fautes de frappe et inversions de colonnes.
- **Normaliser les règles typographiques de prix :** appliquer exclusivement la virgule décimale française alignée verticalement sur la décimale ; clarifier sans ambiguïté les grilles BIB avec des colonnes strictement ordonnées (ex. 3 L, 5 L, 10 L) et des cépages/couleurs explicites.
- **Transparence logistique :** remplacer la mention opaque « Port en sus » par une annexe logistique claire (barème kilométrique / tranches de colisage), ou un seuil de franco précisément défini par région ou par producteur.
- **Encadrement strict des allocations :** définir clairement les règles d'attribution des cuvées sous allocation (quotas annuels, historique d'achat, réservation saisonnière) plutôt que d'apposer une mention anxiogène sans explication.

#### 2.2.3 Refonte du bon de commande (voir aussi Chantier 7 pour le volet navigation)

- Concevoir un bon de commande complet sur feuille dédiée ou document séparé, avec suffisamment de lignes, le rappel des paliers et des franco.
- Intégrer les colonnes de ventilation comptable : quantité commandée, prix unitaire HT, total HT, ventilation des taux de TVA (20 % pour l'alcool, 5,5 % pour les jus de raisin), frais de port et net à payer TTC.
- Ajouter les champs contractuels obligatoires : coordonnées complètes, n° SIRET, n° TVA intracommunautaire, date, case à cocher pour l'acceptation des CGV, cachet commercial et signature du gérant.
- Version idéale : un formulaire PDF réellement remplissable, avec menus déroulants pour sélectionner les produits, cases à cocher pour les quantités, et calcul automatique du total HT et TTC ; ou un lien vers une commande en ligne.


---

## 3. Chantier 2 — Direction artistique, mise en page et lisibilité

### 3.1 Problèmes constatés

#### 3.1.1 Absence de charte graphique cohérente (constat initial)

Le document ne possède aucune charte graphique cohérente au sens fort : pas d'homogénéité forte, pas d'identité de marque affirmée, une impression d'amateurisme se dégage de plusieurs pages. Les seuls éléments graphiques identifiés au premier passage sont des photos de vignerons en noir et blanc, de qualité inégale, et des étiquettes de bouteilles collées sans logique visuelle apparente ; hiérarchie visuelle difficile à lire (prix, cuvée, région pas clairement distingués du reste, le lecteur devant fournir un effort constant pour trouver l'information).

#### 3.1.2 Une palette de couleurs trop sage et sous-exploitée comme outil de merchandising

Le fond crème + bordeaux + vert/ocre fonctionne, mais fonctionne tellement uniformément qu'il finit par ne plus rien raconter. Palette essentiellement : crème, bordeaux, noir, couleurs régionales très discrètes. Le principe d'une palette limitée est bon (Adobe recommande de limiter la palette et d'utiliser la couleur pour créer du contraste et hiérarchiser l'information), mais ici la couleur n'est presque pas utilisée comme outil de merchandising : elle sert seulement à identifier la région, colorer les onglets, colorer quelques éléments. Aujourd'hui, la Bourgogne, le Champagne, le Bordeaux, le Rhône pourraient chacun porter une identité visuelle beaucoup plus forte que ce qu'ils ont (« un onglet coloré discret »).

**Mesures techniques précises (audit pixel/point) :**
- Le même beige **#F6F1E8** couvre **51 pages sur 52**.
- Le même bordeaux **#6F1D3B** coiffe chaque tableau.
- Sur les 34 pages produits qui n'ouvrent pas une région, la couleur régionale n'occupe qu'environ **0,4 %** de la surface, contre **3 à 6 %** pour le bordeaux de la marque : le code couleur de navigation est noyé par la charte elle-même.
- **Cinq bordeaux quasi identiques** cohabitent : celui de la marque, le foncé des en-têtes de prix, la pastille « Rouge », l'onglet Bourgogne, l'onglet Bordeaux. L'écart de couleur entre la pastille « Rouge » et l'onglet Bourgogne est de **ΔE 2,5**, c'est-à-dire indiscernable à l'œil.
- Le **vert** sert à trois significations différentes avec la même teinte exacte (**#3F6B3A**) : « AB·BIO », « CONVERSION » et le mot « Franco ».
- **Contrastes de couleur insuffisants (normes WCAG : minimum 3:1 pour un élément graphique porteur de sens) :** pastille « Blanc » (jaune pâle) à **1,5:1**, pastille « Rosé » à **2,1:1** ; alternance des lignes blanc/crème à **1,08:1** (invisible) ; tableau blanc sur fond beige à **1,13:1** (« il flotte »). Seul le contraste du texte lui-même passe correctement (gris à 5,2:1).
- **Saturation des fonds (audit formel) :** des arrière-plans colorés appliqués uniformément derrière les blocs d'en-tête et les matrices tarifaires génèrent une fatigue visuelle immédiate ; sous un éclairage artificiel de point de vente ou de cave, le manque de contraste entre l'encre noire des tableaux et les fonds colorés rend les chiffres et mentions techniques presque indiscernables. Effet « tapageur » opposé aux codes sobres du négoce de grands vins, sans nuances ni ruptures de rythme réfléchies.
- Sur chaque page, l'élément le plus sombre visuellement est la barre des intitulés de colonnes (« APPELLATION », « FORMAT ») — c'est-à-dire l'information la moins utile qui porte le plus de poids visuel. Aucun produit ne ressort ; il n'y a ni nouveauté, ni coup de cœur, ni meilleure vente mis en avant visuellement.

#### 3.1.3 Désastres typographiques

- **Tailles de police microscopiques :** les tableaux de prix utilisent des tailles qui semblent inférieures à 6 pt par endroits (mesure fine : **68,5 % des caractères du catalogue sont à 8,7 pt ou moins**). Détail des corps utilisés : tableaux en 8,7 pt condensé, mentions sous les cuvées (« sec », « carton de 6… ») en 7 pt, pastilles ALLOCATION et AB dans les tableaux en 6,5 pt, pieds de page en 7,5 pt. Les guides d'accessibilité recommandent environ 12 pt pour le corps de texte et jamais moins de 9 pt, même pour des notes de bas de page ; les recommandations courantes de catalogue placent le corps imprimé autour de 8,5–10 pt.
- **Police condensée qui aggrave le problème :** une chasse étroite donne des caractères serrés, un texte moins aéré.
- **Approche (espacement des lettres) cassée** dans presque tous les noms composés en gras, produisant des « trous » au milieu des mots : « Châte au Lamothe », « Re ve rdy », « Ville ge orge », « Cuvé e Camille », « Ré se rve », « Tuff eau ». C'est aussi ce qui casse la fonction recherche du PDF (voir 3.1.5 / Chantier 7).
- **Hiérarchie typographique inversée :** le nom du domaine est composé en 30 pt, alors que le prix — seule véritable raison d'être d'un tarif — est composé exactement comme le mot « AOP » de la première colonne : même police condensée, même 8,7 pt, même graisse maigre. La cuvée est en gras, donc le prix est l'élément visuellement le plus faible de chaque ligne. Dans les catalogues de référence, c'est l'inverse : le prix et le nom du produit sont mis en avant, le reste passe en petit.
- **Police de corps « subie », pas choisie :** la police sans empattement est TeX Gyre Heros, clone gratuit d'Helvetica issu du monde LaTeX — typiquement la police de remplacement qu'un système Linux utilise quand la feuille de style demande Helvetica ou Arial sans que la police ne soit installée. (Précision : la logique typographique de fond n'est en revanche pas mauvaise — serif élégante pour les titres, sans-serif pour l'information, italique pour certains éléments éditoriaux, titres hiérarchisés ; les polices identifiées sont Lora et TeX Gyre Heros. Il ne faut donc pas tout changer, mais retravailler tailles, interlignage, contraste, longueur de ligne, hiérarchie, usage du gras.)
- **Densité de texte extrême et interlignage insuffisant :** un interlignage de 110 % est un minimum recommandé ; ici, aucune « zone de respiration », lecture pénible, comparaison difficile.
- **Ruptures de césure catastrophiques** (mots disloqués par des espacements parasites ou une chasse mal maîtrisée) :
  - Page 14 : « BEA UJ OLA IS » au lieu de « BEAUJOLAIS » (bandeau régional).
  - Pages 25 et 27 : « RHO NE » au lieu de « RHÔNE ».
  - Page 18 : « BOURGO OGNE » au lieu de « BOURGOGNE ».
- **Répartition des graisses incohérente :** des mentions annexes ou des formats sont composés en gras agressif, alors que des AOP majeures sont reléguées en romain maigre délavé — aucun parcours visuel intuitif pour l'œil.

#### 3.1.4 Déséquilibre du chemin de fer éditorial : entre asphyxie et vide sidéral

Le catalogue oscille entre condensation maximale et vacuité absolue, sans logique de répartition homogène de la charge d'information :

- **Pages saturées (« apnée ») :** page 11 (Domaine Jean de Villebois) entasse 16 lignes de cuvées ; page 17 (Maison André Goichot) aligne 15 références ultra-denses avant d'expédier les 8 plus prestigieuses sur un feuillet suivant (page 18, non indexée — voir Chantier 7) ; page 40 (Famille d'Exea) comprime 17 références dans un tableau oppressant.
- **Pages désertes :** pages 35 (Château Falfas), 36 (Château Pré la Lande) et 37 (Château Balac) ne proposent chacune que trois références de rouge pour occuper l'intégralité du format A4. Dans une démarche professionnelle, ces espaces libérés devraient accueillir de grandes photographies de propriété, des vues de parcelles, des schémas pédologiques ou des portraits de vignerons.
- **Mesure globale :** sur chaque fiche, le tableau de prix commence en moyenne à **51 % de la hauteur de page** — tout ce qui précède doit être « franchi » par l'acheteur avant d'arriver à ce pour quoi il est venu. **16 pages produits sur 44** laissent au moins un quart de leur zone utile vide. **Les pages 18 et 41 sont vides aux deux tiers** (la page 41 ne contient qu'un seul vin réel et trois lignes identiques — voir Chantier 1, 2.1.4). **13 pages portent 5 références ou moins.** Au total, cela représente environ **9 pages de blanc**, dans un catalogue qui se présente comme « respectueux de la nature ».
- **Grille non constante :** le bandeau photo mesure 113 pt sur certaines fiches et 170 pt sur d'autres, avec deux ou trois encarts, un logo tantôt présent tantôt absent. Le tableau démarre donc à une hauteur différente selon la page, alors qu'une grille sert précisément à garantir l'alignement et la comparabilité d'une page à l'autre.

#### 3.1.5 Débordements et collisions de mise en page

| Localisation | Problème |
|---|---|
| Pages 17, 19, 20, 22 à 25 | Le texte de la case « Panachage » est rogné par l'en-tête du tableau (« Les Guignottes » et « Radziwill) » coupés en deux) |
| Page 31 | La dernière ligne de la présentation de Castaing (« une gamme de bières ») est cachée sous la barre des conditions |
| Page 37 | Deux intitulés de colonnes se télescopent en « jusqu'àdès » |
| Pages Nugues, Goichot | Les logos flottent en miniature au milieu de grandes cases vides |
| Page Solemme | Le logo n'affiche même pas le mot « Solemme » |

#### 3.1.6 Système de grille bon dans son principe, mais trop rigide / rythme trop répétitif

Le catalogue a clairement une grille — c'est une bonne chose (Adobe recommande justement l'usage de marges, colonnes et repères pour structurer un catalogue). Mais chaque page suit exactement le même schéma (titre, sous-titre, photo, texte, 4 cases de conditions, tableau, contact, numéro de page), ce qui devient une prison plutôt qu'un squelette : à la page 6 ça fonctionne, à la page 16 on connaît déjà la mécanique, à la page 46 il n'y a plus aucune surprise — exactement ce qu'il faut éviter dans un catalogue premium. Les bonnes pratiques recommandent un système de grille cohérent mais avec plusieurs types de pages (pages produit, pages éditoriales, pages de section, pages « hero », tableaux comparatifs) pour que la répétition serve la navigation sans tuer le rythme.

#### 3.1.7 Points techniques d'impression

- Le PDF utilise des images JPEG en RVB, notamment pour la couverture, dont l'image source fait 1200 × 800 px : sur une page A4 pleine largeur, cela ne représente qu'environ **145 dpi**. Suffisant pour un écran, insuffisant pour une impression professionnelle pleine page vraiment nette. Il faudrait demander les fichiers sources des photos et une couverture avec une image beaucoup plus grande.
- La couverture est imprimée jusqu'au bord, mais le PDF ne possède pas de véritable débord de fond perdu au-delà du format final. Si une impression avec fond perdu est prévue, il faut verrouiller ce point avec le graphiste/imprimeur (typiquement 3 mm de fond perdu, selon leurs spécifications).
- **A4 est en revanche un bon choix de format** (~210 × 297 mm) pour un catalogue B2B destiné aux cavistes ; les marges (environ 15 mm sur la structure principale) sont plutôt saines. Le problème n'est donc pas la taille de la page, mais ce qui est fait de cette page.

#### 3.1.8 Un document pensé pour le papier, envoyé comme fichier écran (voir aussi Chantier 7)

Les métadonnées confirment que le PDF sort de Chromium (moteur Skia/PDF) : une page web imprimée en PDF, pas un document monté dans un logiciel de mise en page — ce qui explique débordements et espacements cassés. Pour un usage écran, la logique est à l'envers : format A4 vertical alors que les écrans sont horizontaux, onglets de région pensés pour « feuilleter » une tranche de livre.

### 3.2 Solutions proposées

#### 3.2.1 Design général et charte graphique

**Problème résumé :** absence d'identité visuelle, aspect amateur.

- Créer une charte graphique stricte : palette de 3 couleurs maximum (une dominante, une secondaire, une pour les accents/prix) ; 2 polices maximum (une pour les titres, une pour le corps) ; un style de photo unique et cohérent (couleur ou noir et blanc, mais pas les deux mélangés sans logique).
- Uniformiser les fiches domaines sur une mise en page identique (photo du vigneron, logo, description, tableau de prix) pour créer un rythme visuel professionnel — **tout en introduisant plusieurs types de composition** (voir 3.2.4) pour éviter la monotonie sur 40+ fiches.
- Utiliser une grille de mise en page en colonnes et en blocs pour placer l'information de manière logique et aérée.
- Épuration des arrière-plans et discipline chromatique : abandonner les aplats colorés saturés au profit de fonds blancs ou ivoire très pâle ; limiter la palette à 2-3 teintes principales (ex. un bordeaux profond pour les repères de lecture, un gris anthracite pour les textes, un ton chaud pour les accents).
- Donner à chaque région une identité visuelle plus affirmée, sans tomber dans le « carnaval » — utiliser la couleur régionale comme **accent**, pas comme couleur dominante. Exemples de direction proposés :
  - **Loire** → vert sauge / ivoire / photographie de vignoble.
  - **Bourgogne** → crème / noir / petit accent bordeaux profond (ou « bordeaux profond / pierre / photographie de clos »).
  - **Rhône** → terracotta / sable / photographie méditerranéenne.
  - **Champagne** → crème très clair / noir / or, très discret.
  - **Bordeaux** → prune / pierre / brun.
  - **Provence** → crème / noir / accent terracotta.
  - L'objectif : donner au lecteur l'impression de changer réellement d'univers d'une région à l'autre, sans repeindre tout le catalogue.

#### 3.2.2 Typographie et lisibilité

**Problème résumé :** polices trop petites, densité de texte, manque d'aération, hiérarchie inversée.

- Augmenter les tailles de police : **8-10 pt minimum** pour le corps de texte et les tableaux (seuil de lisibilité confortable : minimum 8 à 9 pt, avec un contraste suffisant) ; titres nettement plus gros (14-18 pt) pour une hiérarchie claire.
- Aérer la mise en page : interlignage de **1,15 à 1,5** ; marges généreuses (au moins 1,5 cm de chaque côté).
- Utiliser des listes à puces plutôt que de longs paragraphes pour les caractéristiques clés (Appellation, Cépage, Millésime, Prix), pour un balayage visuel rapide.
- Définir un gabarit modulaire sous un logiciel de PAO professionnel (Adobe InDesign).
- Verrouiller les règles de césure automatique pour empêcher l'éclatement des noms de régions et d'appellations (supprimer des coupures parasites du type « BEA UJ OLA IS » ou « BOURGO OGNE »).
- Ne pas changer toute la typographie (la logique serif/sans-serif/italique est déjà bonne) : retravailler seulement tailles, interlignage, contraste, longueur de ligne, hiérarchie et usage du gras — et donner davantage de poids visuel au **prix** plutôt qu'à des mentions secondaires comme « AOP ».

#### 3.2.3 Mise en page, structure et rééquilibrage du chemin de fer

**Problème résumé :** organisation chaotique par endroits, tableaux illisibles, pages trop pleines / trop vides.

- Restructurer par région puis par type : sections distinctes pour chaque région, puis regroupement par couleur (Blancs, Rouges, Rosés), puis par prix croissant à l'intérieur de chaque groupe.
- Repenser les tableaux : en-têtes de colonnes clairs (« Prix Unitaire HT », « Prix dès 60 bt », « Prix dès 120 bt »), éviter les tableaux qui s'étalent sur deux pages sans que cela soit indexé.
- Homogénéiser la densité éditoriale : viser 2 à 4 cuvées détaillées par page, ou 6 à 8 avec des packshots standardisés, pour éviter à la fois la saturation (p. 11, 17, 40) et le vide (p. 35, 36, 37).
- Utiliser les espaces aujourd'hui vides des pages à faible nombre de références (Falfas, Balac, Pré la Lande, etc.) pour mettre en valeur des photos du domaine, des portraits de vignerons, des schémas de terroir, ou les encadrés de contenu proposés au Chantier 5.

#### 3.2.4 Créer plusieurs types de pages (contre la monotonie du gabarit unique)

Conserver la structure domaine → description → conditions → tableau pour 70-80 % des domaines, mais créer plusieurs types de composition :

- **Type A — Fiche standard :** domaine, identité, courte histoire, conditions, tableau (pour les domaines classiques).
- **Type B — Fiche « premium » :** grande photo du domaine, domaine + vigneron, histoire courte, 2-3 bouteilles mises en avant, conditions, tableau (pour les domaines à forte valeur).
- **Type C — Petite gamme :** pour un domaine à 3-4 références, éviter la zone vide en misant sur photo + storytelling + tableau compact + encadré « à retenir ».
- **Type D — Domaine exceptionnel / double page :** pour Champagne, grands crus, allocations, cuvées rares — une véritable fiche éditoriale premium.

Par région, une variante possible de rythme : 1 page d'ouverture de région (grande photo pleine page, nom de la région, 2-3 lignes, carte/terroir/chiffre clé), puis les fiches domaines, puis éventuellement 1 page « sélection / coups de cœur ».

#### 3.2.5 Rendre les conditions commerciales plus lisibles visuellement

**Problème résumé :** la section « Conditions par domaine » est utile sur le fond, mais certaines lignes (ex. « Avec n°16, 17 et 19 (groupe Strasser-Radziwill) », « dès 198 · dès 300 · palette bt ») demandent un décodage pour un nouveau caviste. Solution : remplacer une partie du texte par des pictogrammes scannables en 2 secondes, par exemple :
- 🚚 **Port** — ex. « Franco dès 120 bt »
- 📦 **Paliers** — ex. « 120 · 300 · 600 bt »
- 🔀 **Panachage** — ex. « Toute la gamme »
- ⭐ **Particularité** — ex. « Allocation »

#### 3.2.6 Ajouter des « moments forts » dans le rythme des 52 pages

Ajouter environ 5 à 8 pages ou doubles-pages spéciales qui cassent la répétition, par exemple : « Les 10 coups de cœur SCIO » (sélection de 10 bouteilles), « Nouveautés 2026 » (5-8 références), une grande introduction visuelle pour les Champagnes, une sélection « Bio & Biodynamie », une page « Formats » (magnums / BIB / etc.).

#### 3.2.7 Points techniques d'impression et de fabrication à verrouiller avant impression

- Demander les fichiers sources des photos en haute résolution, en particulier pour la couverture (actuellement ~145 dpi sur pleine page, insuffisant en impression).
- Prévoir un fond perdu (typiquement 3 mm, à confirmer avec l'imprimeur) si le document doit être imprimé bord perdu.


---

## 4. Chantier 3 — Photos, packshots et identité visuelle des bouteilles

### 4.1 Problèmes constatés

#### 4.1.1 Absence quasi totale de packshots bouteille

Le catalogue ne propose quasiment aucun packshot bouteille détouré. En dehors de quelques vignettes pixelisées insérées de manière erratique dans les cartouches de présentation des domaines, aucune référence n'est réellement illustrée. Or dans l'univers viticole, l'aspect visuel du flacon est un déclencheur d'achat déterminant pour le caviste :
- la silhouette de la bouteille (bourguignonne lourde, bordelaise à épaulement vif, flûte alsacienne élancée, flacon champenois armorié) positionne instantanément le niveau de gamme ;
- le graphisme de l'étiquette (typographie d'artisan, style néo-bistrot, blasonnage classique) indique la clientèle finale visée ;
- les attributs de conditionnement (capsule personnalisée, bouchon ciré, papier de soie) justifient les valorisations tarifaires élevées.

En supprimant l'image du produit, le catalogue ramène de grands crus de Bourgogne à 138 € (Clos Vougeot, p. 18) ou des cuvées de prestige de Champagne à près de 50 € (p. 49) à de simples lignes abstraites de feuille de calcul.

#### 4.1.2 Traitement photo qui ressemble à une fiche fournisseur, pas à un catalogue haut de gamme

Sur une fiche comme François Reverdy : portrait du vigneron, image des bouteilles, logo du domaine — l'intention est bonne, mais le traitement du « troisième bloc » (photo bouteilles / logo) est souvent statique et devient un rectangle blanc qui semble avoir été ajouté pour équilibrer la grille plutôt que pour informer. Sur certaines fiches, la bouteille elle-même est présentée dans un espace visuel réduit alors qu'elle devrait être l'élément dominant (le produit est la bouteille — sur la fiche Champagne Dekeyne par exemple, l'image principale est intéressante mais la bouteille reste secondaire dans le cadre).

#### 4.1.3 Statistiques de résolution des images (audit technique mesuré, 108 images)

- **84 images sur 108 sont sous les 300 ppi requis pour l'impression**, dont **30 sous 150 ppi** et **5 sous 100 ppi**.
- Le paysage du Château du Cray est à **62 ppi**, le portrait de Castaing à **60 ppi**.
- À l'inverse, le petit logo de Falfas est embarqué à **1 308 ppi** — un déséquilibre total dans la gestion des ressources.
- Les portraits noir et blanc se mélangent aux paysages en couleur sans cohérence visuelle voulue, et aucun visage n'est légendé.
- À La Passion des Terroirs, une personne est même coupée en deux par le cadrage de la photo.

#### 4.1.4 Photos fausses ou trompeuses (3 cas identifiés)

- **Page 19 — Château du Cray :** la fiche montre une bouteille André Goichot « Bourgogne Hautes-Côtes de Nuits », un vin qui n'est vendu nulle part dans le catalogue.
- **Page 37 — Château Balac :** les bouteilles en photo sont des Haut-Médoc Cru Bourgeois, alors que le tarif ne propose sur cette page que des Vins de France.
- **Page 24 — Domaine du Moulin Blanc (Tavel) :** le paysage en terrasses au-dessus du fleuve évoque plutôt l'Hermitage que Tavel ; la 4e de couverture crédite d'ailleurs « Adobe Stock » pour les photos.

#### 4.1.5 Image potentiellement générée par IA sans mention

Page 35 — Château Falfas : dans le coin bas-droit de la photo du château, une étoile à quatre branches semi-transparente correspond exactement à la marque visible de Gemini (étincelle semi-transparente placée dans le coin inférieur droit des images générées par cet outil). Cette image illustre pourtant le texte « une référence pionnière de la biodynamie ».

#### 4.1.6 Couverture peu représentative du produit et du calendrier

La couverture montre des moutons dans les vignes en hiver (vignes nues), pour une édition de **septembre**, en pleine période de vendanges. Elle ne montre aucune bouteille et ne représente qu'un seul des 40 fournisseurs du catalogue. Le message véhiculé est « nature / biodiversité / agriculture », alors que le catalogue annonce une « sélection riche et audacieuse » — un lecteur s'attendrait à une couverture plus mémorable, davantage « vin / dégustation / terroir / bouteille / caviste ».

#### 4.1.7 Logos mal intégrés

Les logos flottent en miniature au milieu de grandes cases vides sur certaines fiches (Nugues, Goichot) ; le logo de Solemme n'affiche même pas le mot « Solemme ».

### 4.2 Solutions proposées

#### 4.2.1 Standard photo unique et packshots systématiques

- Photographier ou détourer chaque bouteille en haute définition (300 DPI, mode colorimétrique CMJN), pour que le caviste puisse immédiatement apprécier le standing, la coiffe, l'étiquette et la forme de la bouteille.
- Associer visuellement chaque cuvée (ou au minimum chaque domaine) à son flacon.
- Investir dans des photos professionnelles cohérentes (couleur, ou noir et blanc artistique de haute qualité assumé partout) ; bouteilles détourées sur fond blanc ; portraits nets et bien éclairés et légendés.
- Assigner une fonction à chaque image plutôt que de remplir un bloc par défaut : Image 1 → identité du domaine / terroir ; Image 2 → vigneron / cave / vendanges ; Image 3 → bouteille / cuvée phare. Alternative : une seule très belle photo pleine largeur plutôt que trois petites cases (photo + photo + logo) qui donnent une impression de remplissage.

#### 4.2.2 Faire de la bouteille le héros visuel de la page

Inverser la logique actuelle : **Bouteille = star, Vigneron = storytelling, Logo = information secondaire**. Pour les cuvées importantes, une bouteille en grand format doit devenir l'élément principal de la composition (un visuel de bouteille géante l'emporte sur trois petites images), avec conditions et tarifs en bandeau inférieur.

#### 4.2.3 Refaire la couverture

La couverture actuelle est élégante mais générique (nature/biodiversité plutôt que vin). Directions proposées :
- **Option A — bouteille héros :** une bouteille exceptionnelle en plein cadre.
- **Option B — détail viticole :** vigne + lumière + main du vigneron.
- **Option C — composition de plusieurs bouteilles :** traitement extrêmement minimaliste.

Réduire le texte de couverture à l'essentiel : « VINS & CHAMPAGNES · Tarifs cavistes · 2026 », puis « 40 domaines · 10 régions » ; le reste de l'information éditoriale peut être déplacé à l'intérieur (voir Chantier 4, refonte de la première double-page).

#### 4.2.4 Fiabilité et exactitude des visuels

- Vérifier que chaque photo utilisée correspond réellement au produit vendu sur la page (corriger les trois cas de photos trompeuses relevés en 4.1.4).
- Écarter toute image générée par IA non assumée/non mentionnée, en particulier pour illustrer un argument d'authenticité ou de tradition (cas Falfas / biodynamie, 4.1.5).
- Choisir une image de couverture cohérente avec la période de publication (vendanges de septembre) et représentative de l'ensemble de la sélection, pas d'un seul fournisseur.
- Vectoriser et verrouiller les logos (voir aussi Chantier 6) pour éviter qu'ils flottent, disparaissent partiellement (Solemme) ou soient mal proportionnés dans la grille.


---

## 5. Chantier 4 — Merchandising, hiérarchie commerciale et storytelling

### 5.1 Problèmes constatés

#### 5.1.1 Le catalogue ne fait pas assez de « merchandising »

C'est identifié comme le défaut commercial numéro 1 par l'une des analyses. Le catalogue présente bien ce que le vin est et combien il coûte, mais aide insuffisamment le caviste à comprendre *pourquoi* il devrait prendre tel vin plutôt qu'un autre. Il manque des éléments de décision rapide (ex. pour un Sancerre — Les Villaudes, on pourrait imaginer : 🍇 Sauvignon blanc · 🪨 Sols calcaires · 🌱 Bio · 🍽 Fruits de mer / chèvre · 💰 Prix caviste · ⭐ Cuvée signature). Les catalogues produits performants séparent la présentation commerciale des données techniques pour permettre une comparaison rapide entre références.

#### 5.1.2 Absence de « produit héros » et de hiérarchie de mise en avant

Toutes les références semblent avoir à peu près la même importance visuelle, ce qui n'est pas crédible commercialement dans une sélection de 40 domaines. Il manque des repères visuels du type ⭐ Nos incontournables, 🆕 Nouveauté, ❤️ Coup de cœur, 🌱 Bio, 🏆 Cuvée signature, 💎 Haut de gamme, 💰 Rapport qualité/prix — sans transformer le catalogue en supermarché. Un catalogue de vins doit guider le caviste, pas seulement l'informer.

#### 5.1.3 Absence de hiérarchie de gamme au sein d'un même domaine

Exemple donné : chez Sébastien Magnien, l'écart va de 8,50 € (Bourgogne Aligoté) à 60 € (Puligny-Montrachet 1er Cru Les Folatières) sur la même fiche, mais les deux références sont traitées avec quasiment le même poids visuel. Il ne s'agit pas de « cacher » le prix, mais de faire comprendre la gamme.

#### 5.1.4 Textes de présentation trop « corporate » et uniformes

Les descriptions sont bien écrites individuellement, mais utilisent un registre répétitif d'un domaine à l'autre : « précision œnologique », « respect de la typicité des sols », « démarche paysanne », « vins friands et expressifs ». Sur 40 domaines avec le même registre, l'ensemble devient uniforme et manque de personnalité par domaine.

**Mesure statistique du texte (audit mots-clés) :** sur 40 présentations de 3-4 lignes, on compte **17 occurrences** de « famille »/« familial », **15** de « terroir », **12** de « génération(s) » et **19** de « depuis » — **19 textes sur 40** misent sur l'ancienneté comme argument principal. S'y ajoutent des tournures répétées comme « vibrante énergie de sol », « lumineuse franchise de terroir » ou « champagnes d'émotion ». L'accroche de couverture est en outre reprise mot pour mot dans l'édito. Par ailleurs, « Respectueux de la nature » est présenté comme une promesse globale du catalogue, alors que **24 fiches sur 40** n'affichent aucun label environnemental en en-tête.

Une occasion manquée spécifique à un catalogue « Tarifs Vendée » : deux producteurs sont eux-mêmes vendéens — **la Barbinière (Chantonnay)** et **Berteaud Manceau (Mouilleron-le-Captif)** — sans que rien ne les mette en avant, alors que c'est l'argument le plus évident face à un caviste local.

#### 5.1.5 Comparaison avec les catalogues de référence du secteur

Un acteur comme Milliet positionne son catalogue comme un outil d'accompagnement professionnel destiné à aider le CHR à construire sa carte, avec un catalogue en ligne filtrable par appellation, couleur, bio, origine, conditionnement, etc. Sa logique n'est pas « voici nos produits » mais « voici comment vous allez trouver le produit adapté à votre besoin ». C'est l'évolution recommandée pour le catalogue SCIO : une grille cohérente, une hiérarchie forte, suffisamment d'espace blanc, mais plusieurs types de compositions pour éviter la monotonie.

#### 5.1.6 Manque de « moments forts » dans le rythme du catalogue

Sur 52 pages, il manque des respirations éditoriales qui créeraient une sensation de catalogue vivant plutôt que de simple liste (voir aussi 3.2.6).

### 5.2 Solutions proposées

#### 5.2.1 Ajouter des badges commerciaux (avec parcimonie)

Introduire une hiérarchie commerciale visible via des badges, par exemple : **SIGNATURE** (cuvée phare du domaine), **COUP DE CŒUR SCIO** (sélection commerciale de l'agence), **NOUVEAUTÉ**, **ALLOCATION** (quantités limitées), **BIO**, **GRAND FORMAT** (magnum/BIB/etc.), **EXCLUSIVITÉ** (si réellement applicable). Recommandation explicite : ne pas multiplier les badges — viser un maximum de **4 badges** différents pour ne pas noyer le message.

#### 5.2.2 Créer une hiérarchie commerciale des domaines

Tous les domaines ne doivent pas nécessairement être traités de façon identique :
- 🟢 **Niveau 1 — Domaine cœur de gamme :** fiche standard.
- 🟠 **Niveau 2 — Domaine stratégique :** fiche enrichie.
- 🔴 **Niveau 3 — Domaine signature :** double page ou fiche premium.

Cela permet de donner davantage d'espace aux domaines qui justifient réellement une mise en avant.

#### 5.2.3 Transformer les descriptions en argumentaires de vente

Passer d'une « présentation institutionnelle » à un « argumentaire commercial » plus différencié par domaine. Exemple de structure proposée pour chaque fiche :
- **LE DOMAINE** (2 lignes) ;
- **POURQUOI IL EST INTÉRESSANT** (3 points concrets, ex. *« Un excellent point d'entrée en Bourgogne pour proposer du Chardonnay sans exploser le prix d'achat »*) ;
- **À RETENIR** (ex. Bio · 12 ha · Vendanges manuelles) ;
- **À METTRE EN AVANT** (la cuvée à recommander en priorité).

Objectif : que le caviste comprenne immédiatement pourquoi référencer le domaine, plutôt que de lire une fiche institutionnelle interchangeable avec les 39 autres.

#### 5.2.4 Mettre en avant les deux producteurs vendéens

Profiter du fait que la Barbinière (Chantonnay) et Berteaud Manceau (Mouilleron-le-Captif) sont vendéens pour en faire un argument commercial explicite dans un catalogue « Tarifs Vendée ».

#### 5.2.5 Créer une logique « caviste » par domaine (lecture commerciale de la gamme)

Pour chaque domaine, résumer 3 cuvées à retenir selon une lecture commerciale (pas une notation du vin) : **Entrée de gamme** (ex. 6,20 €), **Cœur de gamme** (ex. 9,50 €), **Signature** (ex. 18,00 €) — pour répondre en un coup d'œil à la question du caviste : « Qu'est-ce que je peux vendre ? »

#### 5.2.6 Créer une architecture commerciale globale du catalogue

Au-delà des fiches domaines, structurer l'ensemble du document en parties dédiées, par exemple :
1. L'Agence SCIO (présentation).
2. La sélection (40 domaines).
3. Les incontournables (10-15 cuvées).
4. Les nouveautés.
5. Les formats (magnums / BIB / etc.).
6. Index.
7. Bon de commande.

#### 5.2.7 Ajouter des offres et arguments de vente packagés

Intégrer des mentions du type « Coup de cœur de la maison », « Rapport qualité-prix imbattable », « Médaille d'or au Concours Général Agricole » (si applicable et vérifié) ; envisager des offres groupées (ex. « pack découverte » de 3 bouteilles de la Loire à prix promotionnel) pour augmenter le panier moyen.

#### 5.2.8 Ajouter des pages « moments forts »

Voir 3.2.6 : pages « Les 10 coups de cœur SCIO », « Nouveautés 2026 », introduction visuelle Champagnes, sélection « Bio & Biodynamie », page « Formats ».


---

## 6. Chantier 5 — Contenu œnologique et données B2B

### 6.1 Problèmes constatés

#### 6.1.1 Carence totale en descripteurs organoleptiques et données de vinification

Les fiches se contentent d'un court paragraphe promotionnel standardisé, souvent institutionnel, sans valeur d'usage pour apprécier la valeur intrinsèque du vin :
- **Omission des assemblages de cépages :** les cuvées de Bordeaux (p. 32 à 34), de la Vallée du Rhône (p. 22 à 26) et du Languedoc (p. 40 et 45) n'indiquent aucun pourcentage d'encépagement — le caviste ignore tout de la proportion de merlot/cabernet ou de grenache/syrah dans le vin.
- **Absence totale de profil de dégustation :** aucune information sur la texture de bouche, la structure tannique, le niveau de fraîcheur, la trame aromatique.
- **Silence sur les modes d'élevage :** durées de cuvaison, type de contenants (pièces bourguignonnes, demi-muids, foudres, jarres de grès, amphores), proportion de bois neuf — presque totalement ignorés, en dehors de mentions sporadiques glissées dans le nom même de certaines cuvées.
- **Néant sur les accords mets-vins et le potentiel de garde :** aucune fourchette d'apogée fournie, ce qui prive le revendeur d'arguments pour conseiller ses clients sur des millésimes anciens (ex. les Bas-Armagnacs 1990 et 2000 en page 30, ou le Château de Villegeorge 2015 en page 32).

#### 6.1.2 Données B2B structurantes manquantes

Pour un vrai catalogue destiné aux cavistes, l'ajout des éléments suivants est identifié comme nécessaire, sachant que le catalogue en couvre déjà une partie (format, millésime, appellation, prix) mais pas assez orientée vers la décision d'achat :
- référence interne / SKU ;
- EAN ;
- conditionnement carton / colisage (nombre de bouteilles par carton) ;
- poids éventuellement ;
- disponibilité ;
- minimum de commande ;
- franco ;
- prix HT (déjà présent) ;
- prix public conseillé (RRP) ;
- marge indicative ;
- indication des nouveautés ;
- allocation (déjà présent mais mal encadré, voir Chantier 1) ;
- millésime (déjà présent) ;
- cépages ;
- certification (déjà partiellement présent via les pastilles AB/HVE/Biodynamie/Conversion) ;
- format (déjà présent).

Un caviste s'appuie normalement, pour analyser un vin, sur l'appellation, le domaine, la cuvée, le millésime, les sols, les cépages, la vinification, l'élevage et le prix — le catalogue n'en fournit que cinq. Le degré, le prix de vente conseillé, les codes article, le conditionnement (sauf pour les jus de cépage) et la disponibilité n'apparaissent nulle part. Un catalogue B2B repose normalement sur un identifiant unique par produit, des paliers de prix, des minimums de commande et l'état du stock ; ici, pour commander un vin, il faut recopier cinq champs à la main.

#### 6.1.3 Incohérences internes des données déjà présentes

- Le mode d'emploi distingue « NM » (non millésimé) et « — » (information non communiquée), mais **les 18 vins en bouteille d'Exea sont tous en « — »** : aucun millésime n'est communiqué sur toute une gamme.
- **31 lignes ont un format « — »** : toute la gamme Barbinière, tout Villebois, le Cahors, le Fronton et les bières.
- Les liquoreux de Haut Marin et de Stratéus n'ont pas de couleur renseignée.
- L'information de cépage est positionnée tantôt entre parenthèses (Boehler), tantôt en sous-ligne (Colombier), tantôt après un tiret (Berteaud Manceau), et le plus souvent absente.
- La colonne « Appellation » sert de fourre-tout hétérogène : « Méthode traditionnelle », « Bière », « Pur jus de raisin », « Vin sans alcool ». Les IGP du Colombier n'ont même pas de nom précisé.
- Certaines cuvées portent un double nom sans qu'on sache lequel commander : « Franc / Graves » (millésime 2021/2024) ou « Cuvée des Fontenelles / Y'a Rien qui Presse ».

#### 6.1.4 Textes qui vendent des produits absents du tarif

Plusieurs présentations de domaine mentionnent des produits qui ne figurent finalement pas dans le tableau de prix : le Volnay chez Sébastien Magnien, le Bugey chez Trichon, le Cru Bourgeois chez Balac. La mention « Sur demande » apparaît **21 fois** dans le document, dont « gamme complète sur demande » pour deux domaines entiers (Jean de Villebois et Fabien Castaing) : un catalogue qui renvoie systématiquement à un coup de fil pour connaître la gamme réelle manque en partie sa mission.

#### 6.1.5 Millésimes proposés hors cohérence de saison

Des rosés 2022 et 2023 (Tavel 2022, Cabernet Franc rosé 2023, Rosé DADA 2023) sont proposés dans une édition de septembre 2026, sans un mot d'explication — ce qui, pour un caviste, évoque un « fond de cave » plutôt qu'un choix assumé.

#### 6.1.6 Risque de conformité loi Évin sur le registre rédactionnel

Même adressé à des professionnels, un catalogue fait partie des supports de publicité pour l'alcool encadrés par la loi Évin, qui limite le message à des informations objectives (degré, origine, composition, mode d'élaboration). Un mot comme « convivialité » (fiche Famille d'Exea) relève d'un registre historiquement exclu par cet encadrement — point à faire valider par un professionnel compétent en la matière.

### 6.2 Solutions proposées

#### 6.2.1 Fiches techniques normalisées par cuvée

- **Encépagement précis :** proportions d'assemblage en pourcentages (ex. 60 % Grenache, 40 % Syrah).
- **Données de vinification et d'élevage :** vendanges manuelles/mécaniques, type de contenants (cuves inox, foudres, barriques de chêne, amphores), durée d'élevage, présence ou absence de sulfites ajoutés.
- **Profil organoleptique synthétique :** repères visuels simples sur le nez (arômes dominants) et la bouche (acidité, tanins, rondeur, corps).
- **Potentiel de garde et conseils de service :** température idéale de dégustation, temps d'aération/décantation, accords mets-vins recommandés.

#### 6.2.2 Fiche produit enrichie, mais dosée

Si les données sont disponibles, ajouter selon pertinence : cépage, profil, accords, élevage, température de service, positionnement, prix de vente conseillé (RRP), marge indicative, EAN, colisage, disponibilité. Recommandation explicite : **ne pas tout mettre sur toutes les fiches** — maximum 3 informations supplémentaires par cuvée jugée stratégique, pour ne pas retomber dans la surcharge.

#### 6.2.3 Corriger les incohérences de données avant refonte graphique

- Distinguer clairement et systématiquement « NM » (non millésimé) de « — » (information non communiquée), et combler les cas où toute une gamme est en « — » par erreur (ex. Exea).
- Renseigner le format sur les 31 lignes actuellement à « — ».
- Harmoniser la position de l'information de cépage (un seul standard de présentation pour tout le catalogue).
- Clarifier les cuvées à double nom (choisir une dénomination unique ou expliciter la relation entre les deux noms).
- Vérifier que chaque produit mentionné dans le texte de présentation d'un domaine figure bien dans son tableau de prix (ou l'enlever du texte).
- Documenter ou retirer la mention « Sur demande » quand elle concerne une gamme entière, pour ne pas donner l'impression d'un catalogue incomplet.

#### 6.2.4 Vigilance rédactionnelle loi Évin

Faire relire les textes de présentation par une personne compétente sur l'encadrement légal de la communication sur l'alcool (loi Évin), et neutraliser les formulations trop proches du registre subjectif/lifestyle (ex. « convivialité »).


---

## 7. Chantier 6 — Erreurs textuelles, coquilles et incohérences (relevé exhaustif)

> **Note de lecture :** les numéros de page de ce chapitre sont ceux relevés par les audits successifs (numérotation du PDF « catalogue écran », 52 pages). Certains renvois de page issus de la passe formelle sont à revérifier contre le fichier final au moment de la correction, mais toutes les erreurs signalées y sont conservées.

### 7.1 Problèmes constatés

#### 7.1.1 Défiguration récurrente de l'identité de marque

L'acronyme et la raison sociale de l'agence subissent des corruptions typographiques répétées sur plusieurs feuillets :

| Page(s) | Ce qui est imprimé | Forme correcte |
|---|---|---|
| 4 et 5 | « AVINSREPIRITS » (bloc de tête) | VINS & SPIRITS |
| 6, 22, 28, 39 | « ACENCE SCIO » (le C remplace le G) | AGENCE SCIO |
| 2 et 51 | « AVINSA EPIRITS » | VINS & SPIRITS |
| 24 | « AVINS SPIRITS » (l'esperluette disparaît) | VINS & SPIRITS |
| 50 | « VINS SPIRITS » (esperluette remplacée par un double espace vide) | VINS & SPIRITS |
| 52 (4e de couverture) | « HAGENCE SCIO » (lettre H inaugurale parasite) | AGENCE SCIO |

Soit **six formes de corruption** de la raison sociale, ce qui produit une impression d'amateurisme et une « ruine totale de l'image de marque ».

#### 7.1.2 Défiguration systématique du message sanitaire légal

- Sur **plus de trente-cinq pages**, l'espace entre le substantif et le verbe est supprimé : « L'abus d'alcoolest dangereux pour la santé » (graphie agglutinée). La même corruption, côté couche texte, fait que « pour la santé » devient « pourla » sur les pages 2 à 51 (et empêche la recherche Ctrl+F sur ce passage).
- Sur le **bon de commande contractuel (p. 51)**, le mot « alcool » perd sa consonne : « L'abus d'**acoolest** dangereux… ».
- Sur **une quinzaine de pages**, l'accent aigu du mot final est omis : « à consommer avec **moderation** ».

#### 7.1.3 Césures et espaces parasites à l'intérieur des mots

| Page | Texte imprimé | Forme attendue |
|---|---|---|
| 4 | Domaine de la Barbiniè re | Domaine de la Barbinière |
| 4 | Chai Berteaud Mance au | Chai Berteaud Manceau |
| 8 | Domaine Jean de Ville bois ; « sur dem an de » | Domaine Jean de Villebois ; « sur demande » |
| 10 | Rouge au lèvre s | Rouge aux lèvres |
| 11 | Courant Che nin | Courant Chenin |
| 11 | Sile x | Silex |

À cela s'ajoutent, dans l'audit technique, les blancs parasites dans les noms en gras : « Châte au Lamothe », « Re ve rdy », « Ville ge orge », « Cuvé e Camille », « Ré se rve », « Tuff eau » (voir Chantier 2, 3.1.3). Ces « trous » sont aussi ce qui casse la recherche dans le PDF.

#### 7.1.4 Coquilles lexicales et fautes d'orthographe

| Page | Texte imprimé | Forme attendue / commentaire |
|---|---|---|
| 7 | Le Bois Bouquet **piriot** noir | Le Bois Bouquet **pinot** noir |
| 7 | Les Amphibol | Les Amphiboles (selon l'audit) |
| 9 | dem-sec | demi-sec |
| 13 | **derm** sec et Riesling **Bec** | demi-sec / Riesling sec |
| 16 | Les Coups de Folies sans **soutre** | Les Coups de Folies sans **soufre** |
| 20 | AOP **Macon** | AOP **Mâcon** |
| 29 | Château du **Crav** | Château du **Cray** |
| 30 | N°8 Grand **Pavojs** | N°8 Grand **Pavois** |
| 31 | **Banc**, **Rose**, Rouge, **Baric**, Rouge, **Bano** (BIB) | Blanc, Rosé, Rouge (orthographe de « Blanc » et « Rosé » à rétablir) |
| 42 | 100 % chardonnay **chardonnay** | 100 % chardonnay (bégaiement typographique — doublon) |
| 46 | gamme la **babe** | gamme la **barbe** |
| 48 | jus de **mis in** rouge | jus de **raisin** rouge |
| 50 | disponible **des septenbre** | disponible **dès septembre** |
| 52 | extra **brul** et Vie ux Ratafia | extra **brut** / Vieux Ratafia |
| 52 | **brul** nature | **brut** nature |
| 52 | **Manthélie** | **Monthélie** |
| 52 | Crédits **phatos** | Crédits **photos** |

#### 7.1.5 Altérations de ponctuation et de traits d'union

| Page | Texte imprimé | Forme attendue |
|---|---|---|
| 11 | AOP PouillyFumé- | AOP Pouilly-Fumé |
| 14 | AOP Moulin- -Vent | AOP Moulin-à-Vent |
| 15 | AOP HautesCôtes -de Beaune | AOP Hautes-Côtes de Beaune |
| 23 | AOP Beaumesde--Venise | AOP Beaumes-de-Venise |
| 32 | AOP Lalandede--Pomerol | AOP Lalande-de-Pomerol |
| 33 | AOP Moulisen--Médoc | AOP Moulis-en-Médoc |

#### 7.1.6 Mutilations d'unités et de conditions de transport

| Page | Texte imprimé | Forme attendue |
|---|---|---|
| 4 | palette **It** | palette **bt** (bouteilles) |
| 23 et 38 | « Avec les n° 16, 17 et 19 (groupe Strasser- » | groupe Strasser-Radziwill (texte amputé) |
| 40 | **francodes** 180 bt | franco dès 180 bt |
| 43 | **francodes** 72 **bit** | franco dès 72 bt (« bit » au lieu de « bt ») |
| (page non précisée) | **francodes** 180**b** | franco dès 180 bt (lettre « t » manquante) |

#### 7.1.7 Erreurs, contradictions et incohérences de contenu page par page

| Page | Ce qui cloche |
|---|---|
| 1 | Le titre « Vins & Champagnes » oublie les bières, jus de raisin, armagnacs, vins sans alcool et ratafias du catalogue. Le logo, lui, dit « Vins & Spirits ». |
| 1 à 3 | « 40 domaines » : le n° 33 n'est que la gamme de jus du n° 32, le n° 7 est une marque, le n° 25 une maison de distribution — le décompte est discutable. |
| 2 | Le mode d'emploi numérote cinq éléments de ① à ⑤ sans schéma annoté pour les montrer. HVE est défini deux fois (labels et abréviations). |
| 3 | « Conditions par domaine », qui est en page 4, est rangé à la fin du sommaire. |
| 7, 12, 31 | La règle de tri annoncée page 2 (effervescents d'abord, puis par couleur) est violée : Pop's (pétillant) est rangé dans les rosés, Divin No Low est trié au prix en mélangeant les couleurs, Fines Bulles vient après un blanc sec. |
| 8 | « Rouge au lèvres » ; des « IGP » sans nom d'IGP. |
| 14 | Un Mâcon-Villages dont la cuvée s'appelle… « Bourgogne ». |
| 15 | « AOP Hautes-Côtes de Beaune » au lieu de « Bourgogne Hautes-Côtes de Beaune », d'où deux entrées différentes dans l'index. |
| 30 | « AOP Bas-Armagnac » (voir 7.1.8) ; « Hors d'Age » sans accent. |
| 31 | « chardonnay · chardonnay » en doublon ; appellation « — » pour le vin effervescent Fines Bulles. |
| 34 | Le texte affirme que toutes les cuvées sont bio depuis le millésime 2022, mais le Rosé DADA 2023 n'a pas de pastille AB. |
| 41 | Trois lignes « Pergola d'Exea » strictement identiques : les couleurs ont disparu. |
| 42 | « Disponible dès septembre » dans l'édition… de septembre. |
| 47 | « VDC » n'est jamais expliqué. |
| 48 | « En biodynamie » dans le texte mais aucune pastille : certifié ou pas ? |
| 50 | « Pays d'Oc » apparaît en deux entrées séparées (pages 40 et 45). Le chapeau de l'index dit exclure les Vins de France et les IGP, qui y figurent pourtant. |
| 50–51 | L'index renvoie à des numéros de page, le bon de commande demande des numéros de fiche : deux systèmes de référence pour un même produit. |

#### 7.1.8 Erreur double sur l'Armagnac

L'INAO enregistre l'Armagnac comme indication géographique de boisson spiritueuse : « **AOP** » est donc impropre (on dit AOC, ou IG). Par ailleurs, la **Blanche Armagnac** est une AOC à part entière, reconnue depuis 2005, et non un Bas-Armagnac.

#### 7.1.9 Autres incohérences de définition dans la légende

- La légende définit « AB » comme une agriculture biologique « **confirmée par le domaine** » : or une certification est confirmée par un organisme certificateur, pas par le domaine lui-même.
- Le mot « **VDC** » (page 47) et la mention « En biodynamie » (page 48) affichent des labels ou pratiques sans définition ni pastille associée.

### 7.2 Solutions proposées

- **Vectoriser le bloc-marque** (logo « AGENCE SCIO — VINS & SPIRITS ») et l'insérer comme composant verrouillé dans le gabarit maître, pour interdire toute corruption textuelle (ACENCE, HAGENCE, AVINSA, AVINSREPIRITS, etc.).
- **Rétablir le libellé légal exact**, sans coquille ni mot agglutiné : « L'abus d'alcool est dangereux pour la santé, à consommer avec modération », le reproduire à l'identique sur toutes les pages, y compris sur le bon de commande — tout en réduisant sa présence visuelle à un niveau discret plutôt que de le supprimer (ne pas toucher à la conformité sans validation juridique).
- **Vérification orthographique et typographique globale** des noms de cuvées et d'appellations : accents, capitales, tirets, millésimes, appellations (palier 0).
- **Contrôle qualité et relecture croisée rigoureuse** avant toute validation du Bon à Tirer (BAT) : relire plusieurs fois le catalogue pour éliminer fautes de frappe, incohérences de noms et informations manquantes. Un catalogue avec des erreurs perd toute crédibilité.
- **Automatiser l'import des données** (base de données / tableur verrouillé) plutôt que de ressaisir manuellement les noms et les prix.
- **Corriger les libellés d'appellations** : Bourgogne Hautes-Côtes de Beaune (au lieu de « Hautes-Côtes de Beaune » seul), « Armagnac » à qualifier en AOC/IG selon le registre INAO, distinction Blanche Armagnac / Bas-Armagnac.
- **Supprimer les doublons et lignes ambiguës** (Pergola d'Exea × 3 sans couleur ; « chardonnay · chardonnay ») et **définir tous les sigles** utilisés (VDC, HVE une seule fois, etc.).
- **Corriger la règle de tri annoncée** : effervescents d'abord, puis par couleur, et appliquer la règle sur toutes les fiches (Pop's, Divin No Low, Fines Bulles).
- **Mettre à jour ou justifier les mentions incohérentes** : « Disponible dès septembre » dans l'édition de septembre ; pastille AB manquante sur le Rosé DADA 2023 si la cuvée est bien bio ; pastille biodynamie chez Solemme si certifiée.
- **Clarifier le titre et le décompte** : que recouvre exactement « Vins & Champagnes » vs. bières/jus/armagnacs/sans alcool/ratafias, et comment sont comptés les « 40 domaines ».


---

## 8. Chantier 7 — Navigation, sommaire, index et outils PDF / digital

### 8.1 Problèmes constatés

#### 8.1.1 Le sommaire escamote les pages paires et les grands crus

Le sommaire (page 3) attribue à chaque domaine un numéro unique associé à une seule page. Or quatre producteurs majeurs voient leur offre scindée sur deux pages consécutives sans que la seconde page ne soit jamais répertoriée dans le sommaire, ni identifiée par un rappel d'onglet :

| Domaine | Page indexée | Page oubliée | Ce que contient la page oubliée |
|---|---|---|---|
| Maison André Goichot (n° 12) | 17 | **18** | Les huit fleurons les plus rémunérateurs de la maison en Côte de Nuits et Côte de Beaune : Fixin, Chassagne-Montrachet, Aloxe-Corton, Gevrey-Chambertin, Corton Grand Cru, Clos Vougeot Grand Cru… |
| Domaine Haut Marin (n° 23) | 29 | **30** | Toute l'offre de Bas-Armagnacs (Blanche, VSOP, XO, Hors d'Âge, millésimes 1990 et 2000) et les Bag-in-Box |
| La Passion des Terroirs (n° 25) | 32 | **33** | Les appellations communales bordelaises prestigieuses : Pomerol, Pauillac, Saint-Julien, Sauternes, cuvées parcellaires de Durfort-Vivens |
| Famille d'Exea (n° 32) | 40 | **41** | La cuvée haut de gamme Chant de Lumière et les BIB 5 L |

Un acheteur qui planifie ses approvisionnements à l'aide du sommaire passe ainsi à côté des cuvées à plus forte valeur ajoutée du catalogue. Par ailleurs, l'entrée « Conditions par domaine » (page 4) est rangée à la fin du sommaire au lieu d'être en tête, et les ruptures de tri de la légende page 2 ne sont pas respectées (voir Chantier 6).

#### 8.1.2 L'index des appellations : faillite du tri alphabétique et renvois trompeurs

- Sur une douzaine de lignes, le **numéro de page est placé avant le nom de l'appellation**, ce qui détruit l'alignement et le principe même de classement. Exemples d'entrées aberrantes : « 15 Beaune », « 14, 15, 19, 20, 21 Bourgogne », « 44 Cévennes », « 46, 47 Champagne », « 39 Coteaux Varois en Provence », « 29 Côtes de Gascogne », « 15 Pommard », « 15, 17 Saint-Romain », « 16, 17 Saint-Véran », « 6, 11 Sancerre », « 20 Santenay », « 6, 7, 9, 10, 11 Val de Loire ».
- **« Vin de France »** est un cas d'école d'accident typographique : l'index affiche la séquence éclatée « Vin de 6, 7, 11, 25, 28, 29, 34, 37, 38, 40, France 43 » — l'énumération numérique s'intercale au cœur de la dénomination légale et rejette « France » et le folio 43 sur la ligne inférieure.
- **Renvois de pages trompeurs :** comme les pages paires 18, 30 et 33 n'ont jamais été prises en compte dans l'indexation, toutes les appellations qui y figurent renvoient vers la première page du domaine. Un caviste cherchant un **Pauillac, un Pomerol ou un Sauternes** est dirigé vers la page 32, où ces crus n'apparaissent pas (ils sont en page 33). De même, **Bas-Armagnac** renvoie à la page 29 (vins blancs et rosés frais de Gascogne), la page 30 étant absente des renvois.
- **Mesure d'ergonomie :** l'index est extrêmement dense — pratiquement une base de données ; il fonctionne pour rechercher une appellation mais ne donne pas envie de la consulter. « Pays d'Oc » apparaît en deux entrées séparées (pages 40 et 45), et le chapeau dit exclure IGP/Vins de France alors qu'ils y figurent (voir Chantier 6). Deux systèmes de référence coexistent (index → numéros de page ; bon de commande → numéros de fiche).

#### 8.1.3 Document pensé pour le papier, envoyé comme « PDF écran »

- Format **A4 vertical** alors que les écrans sont horizontaux.
- **Onglets de région** qui sautent de gauche à droite d'une page à l'autre, car prévus pour la tranche d'un livre ; le mode d'emploi explique qu'on retrouve une région « en feuilletant ».
- **Le bon de commande se remplit au stylo** : le PDF ne contient aucun champ de formulaire.
- La 4e de couverture dit « **Ne pas jeter sur la voie publique** » sur un fichier numérique.
- **Aucun signet** : 52 pages sans panneau de navigation, alors que les signets sont la technique recommandée pour se repérer dans un long PDF. Le fichier n'est pas balisé (« tagged ») et sa langue n'est pas déclarée. Les liens internes (sommaire, téléphones, mail) existent, ce qui est bien, mais c'est la moindre des choses.
- **Sur smartphone c'est illisible :** une page A4 affichée en pleine largeur sur un écran de 390 px réduit le texte des tableaux (8,7 pt) à environ 5,7 px ; Apple fixe pourtant à 11 pt la taille minimale de texte sur ses appareils.
- **La recherche Ctrl+F est cassée :** testée avec le moteur PDF de Chrome, **37 % des mots des noms de cuvées sont introuvables**. « Durfort-Vivens », « Villaudes » et « Pergola » donnent zéro résultat. Même « pour la santé » n'est trouvé que sur la 4e de couverture car sur les pages 2 à 51 la couche texte contient « pourla ».
- **Public visé :** le catalogue sera très probablement envoyé par mail, WhatsApp, consulté sur ordinateur, ouvert sur téléphone, projeté sur tablette — il est aujourd'hui pensé comme un document imprimé, pas comme un document print + digital.

Checklist digitale relevée (état actuel) : navigation PDF — ✔️ déjà partiellement présente ; **signets — ❌ à ajouter** ; sommaire cliquable — ✔️ déjà présent ; liens mail — ✔️ présents ; téléphone cliquable — ✔️ présent ; **QR code — ❌ absent** ; **QR vers commande / contact / catalogue actualisé — ❌ absent** ; **URL cliquable — à renforcer**.

#### 8.1.4 Le disclaimer légal est trop présent visuellement

La mention « Tous les prix sont indiqués HT. L'abus d'alcool est dangereux pour la santé… » revient extrêmement souvent, sur chaque page. Le cadre légal français de la publicité des boissons alcooliques prévoit des règles spécifiques sur le contenu publicitaire et le message sanitaire, avec certaines exceptions pour les documents professionnels/circulaires et certains tarifs en lieux de vente spécialisés. Il ne faut donc pas toucher à la conformité juridique sans validation, mais graphiquement la répétition systématique du même texte à chaque page crée un bruit visuel.

### 8.2 Solutions proposées

#### 8.2.1 Refonte du sommaire

- Indexer **l'ensemble des pages réelles** de l'ouvrage, en faisant apparaître explicitement les doubles pages : **page 18 pour Goichot, 30 pour Haut Marin / Bas-Armagnac, 33 pour Passion des Terroirs / Grands Crus de Bordeaux, 41 pour Famille d'Exea**.
- Placer l'entrée « Conditions par domaine » à sa place logique dans le sommaire.
- Identifier la deuxième page de chaque domaine concerné par un rappel d'onglet.

#### 8.2.2 Reconstruction de l'index alphabétique des appellations

- Trier rigoureusement par ordre alphabétique strict d'appellation, de A à Z.
- Aligner les numéros de page à l'aide de **tabulations calées sur la marge droite** (éliminer les numéros parasites placés devant les noms et la ligne éclatée des Vins de France).
- Vérifier que **chaque renvoi pointe vers le folio exact** où se situe le produit.
- Améliorer l'ergonomie : colonnes mieux espacées, appellations plus visibles, éventuellement région en couleur, repères alphabétiques A–B–C–D…
- Unifier les systèmes de référence : utiliser soit les numéros de page, soit les numéros de fiche, mais de façon identique dans l'index et le bon de commande.

#### 8.2.3 Transformer le PDF en véritable outil commercial digital

- **Signets PDF** avec arborescence complète : Catalogue SCIO → Loire (François Reverdy, Barbinière, Colombier…), Alsace, Beaujolais, Bourgogne, Rhône, Champagne, etc. — pour naviguer directement dans Acrobat/Preview. Conserver les liens internes déjà cliquables du sommaire.
- **Navigation permanente sur chaque fiche :** ← SOMMAIRE · RÉGION · ← DOMAINE PRÉCÉDENT · DOMAINE SUIVANT →. Particulièrement utile dans un PDF de 52 pages.
- **QR codes intelligents** (pas 40 QR codes, mais quelques-uns stratégiques) : catalogue à jour (dernière version) ; commander (formulaire) ; contacter SCIO (email/téléphone) ; fiche domaine (site du vigneron si pertinent) ; Instagram (univers SCIO).
- **Version écran réelle :** format paysage, signets, recherche fonctionnelle (corriger la couche texte pour éliminer « pourla » et les espaces parasites dans les noms), bon de commande remplissable (ou lien vers une commande en ligne), déclaration de la langue et balisage d'accessibilité du fichier, URL cliquables renforcées.
- **Corriger le tarif en fonction de l'usage mobile :** taille de texte des tableaux suffisante pour un affichage en pleine largeur sur téléphone (voir Chantier 2, tailles de police).
- **Retirer les mentions propres à l'imprimé** (« Ne pas jeter sur la voie publique ») du fichier numérique, ou les remplacer par la mention conforme (voir Chantier 8).
- **Disclaimer légal :** le garder (présent mais beaucoup moins perceptible), sans altérer le libellé légal ; en revoir l'intégration graphique plutôt que la répétition en pleine visibilité sur chaque page.


---

## 9. Chantier 8 — Conformité juridique et réglementaire

### 9.1 Problèmes constatés

#### 9.1.1 Infractions caractérisées au Code de commerce

L'article R. 123-237 du Code de commerce impose que tout document publicitaire, tarif ou correspondance émis par une entreprise commerciale mentionne lisiblement l'ensemble de ses coordonnées d'immatriculation. L'analyse de la couverture et de l'ours en 4e de couverture révèle plusieurs omissions :

- **Omission de la forme juridique** de la société : le document mentionne « Agence SCIO Vins et Spirits, 843 151 663 RCS Nantes » sans jamais préciser s'il s'agit d'une SAS, d'une SARL ou d'un exercice en nom personnel.
- **Absence du montant du capital social** : mention obligatoire pour toutes les sociétés par actions ou à responsabilité limitée, totalement absente.
- **Absence du numéro de TVA intracommunautaire** : information pourtant obligatoire sur tous les documents de facturation, bons de commande et catalogues marchands B2B.
- **Absence totale des Conditions Générales de Vente (CGV)** : en vertu de l'article L. 441-1 du Code de commerce, les CGV constituent le socle de la négociation commerciale et doivent pouvoir être communiquées ou consultées sur tout support contractuel de vente. Le catalogue n'intègre aucune page de CGV. Les clauses fondamentales — réserve de propriété jusqu'à complet paiement, transfert des risques au moment de la livraison, délais de règlement légaux (plafonnés par la loi LME à 60 jours nets ou 45 jours fin de mois), pénalités de retard, indemnité forfaitaire légale de 40 € pour frais de recouvrement — brillent par leur absence.

Le défaut de ces mentions obligatoires expose la structure à des **amendes pénales pouvant atteindre 750 € par infraction constatée**.

#### 9.1.2 Risques contentieux liés à la loi Évin

L'encadrement strict de la communication sur les boissons alcoolisées par le Code de la santé publique (loi Évin) impose un message sanitaire clair et non dénaturé. La mutilation continue du libellé obligatoire (« L'abus d'alcoolest… » et « L'abus d'acoolest… ») fragilise l'agence face aux contrôles de la répression des fraudes (DGCCRF), qui peut assimiler ces graphies altérées à une négligence dans l'obligation de prévention sanitaire. Par ailleurs, certaines formulations de la rédaction (ex. « convivialité » dans la fiche Exea) relèvent d'un registre historiquement exclu par l'encadrement Évin (voir Chantier 5, 6.1.6).

#### 9.1.3 Mention environnementale obsolète et absence de signalétique Triman

La mention laconique « Ne pas jeter sur la voie publique » (4e de couverture, page 52) est devenue obsolète. Conformément à la filière à responsabilité élargie du producteur (REP) pour les papiers graphiques gérée par l'éco-organisme Citeo, tout catalogue commercial imprimé diffusé sur le territoire national doit arborer le **logo normalisé Triman** accompagné de l'**info-tri** précisant la consigne de tri. L'omission de cette signalétique expose l'émetteur à des sanctions administratives spécifiques.

#### 9.1.4 Mentions et définitions de labels approximatives

La définition de « AB » comme agriculture biologique « confirmée par le domaine » (au lieu d'une certification par organisme certificateur) et la promesse globale « respectueux de la nature » alors que 24 fiches sur 40 n'affichent aucun label environnemental sont des sources de risque de communication trompeuse (voir Chantier 5, 5.1.4, et Chantier 6, 7.1.9).

### 9.2 Solutions proposées

- **Page de Conditions Générales de Vente (CGV)** conforme à l'article L. 441-1 du Code de commerce : clause de réserve de propriété jusqu'à complet encaissement ; modalités et délais de paiement (plafonds LME : 60 jours ou 45 jours fin de mois) ; taux des pénalités de retard ; indemnité forfaitaire légale de 40 € pour frais de recouvrement ; transfert des risques à la livraison. À intégrer en fin d'ouvrage.
- **Compléter l'ours commercial et les mentions obligatoires** : forme juridique (SAS, SARL, etc.), montant exact du capital social, numéro d'immatriculation au RCS complet, numéro de TVA intracommunautaire.
- **Rétablir le libellé sanitaire exact** sans coquille ni mot agglutiné (« L'abus d'alcool est dangereux pour la santé, à consommer avec modération »), sur toutes les pages, y compris sur le bon de commande.
- **Remplacer la mention caduque** « Ne pas jeter sur la voie publique » par le **logo officiel Triman** accompagné de l'**info-tri Citeo** pour les imprimés graphiques.
- **Champs contractuels du bon de commande** : coordonnées complètes, n° SIRET, n° TVA intracommunautaire, date, case à cocher d'acceptation des CGV, cachet commercial et signature du gérant (voir Chantier 1, 2.2.3).
- **Faire relire les textes et labels** par un professionnel (loi Évin, définitions AB/HVE/biodynamie, certifications réellement détenues par chaque domaine) et n'afficher « respectueux de la nature » qu'en cohérence avec les labels effectivement présents dans les fiches.
- **Stabiliser l'identité de marque** en composant verrouillé le bloc-marque (voir Chantier 6).


---

## 10. Plan d'action consolidé et feuilles de route de priorisation

Cette section réunit les différentes feuilles de route proposées dans les analyses. Elles sont complémentaires : la première (cinq chantiers) est la synthèse finale ; les suivantes offrent d'autres angles de priorisation (par urgence, par paliers de transformation, par grandes décisions).

### 10.1 Plan d'action final en cinq chantiers

**Chantier A — Assainissement mathématique et automatisation des tarifs** *(priorité absolue : éliminer les anomalies tarifaires qui ruinent la relation commerciale)*
- Rétablir la dégressivité : prix décroissants au fil des paliers, palette = prix le plus bas de la grille.
- Centraliser sur un PIM ou tableur verrouillé ; interdire la saisie manuelle libre sur la maquette ; import automatisé vers InDesign.
- Normaliser la typographie des prix (virgule décimale française, alignement sur la décimale) ; clarifier les grilles BIB (3 L, 5 L, 10 L, cépages/couleurs explicites).
- Remplacer « Port en sus » par une annexe logistique (barème kilométrique / tranches de colisage) ou un seuil de franco défini.

**Chantier B — Refonte graphique, direction artistique et mise en page**
- Épuration des fonds (blanc ou ivoire très pâle), palette stricte de 2 à 3 teintes (ex. bordeaux profond pour les repères de lecture, gris anthracite pour les textes, ton chaud pour les accents).
- Gabarit modulaire InDesign ; tailles de tableaux à 8-9 pt minimum ; contraste suffisant ; césures verrouillées (fin des « BEA UJ OLA IS », « BOURGO OGNE »).
- Packshots flacons systématiques (300 DPI, CMJN), chaque cuvée associée à son flacon.
- Rééquilibrage du chemin de fer : 2 à 4 cuvées détaillées par page ou 6 à 8 avec packshots standardisés ; utiliser les espaces vides (Falfas, Balac, Pré la Lande) pour photos du domaine, portraits de vignerons, schémas de terroirs.

**Chantier C — Enrichissement œnologique et aide à la vente**
- Fiches techniques normalisées : encépagement en %, vinification/élevage (vendanges, contenants, durée, sulfites), profil organoleptique (nez/bouche), potentiel de garde, température de service, aération, accords mets-vins.
- Encadrement strict des allocations (quotas annuels, historique d'achat, réservation saisonnière).

**Chantier D — Navigation et outils de commande**
- Refonte du sommaire (pages réelles incluant les doubles pages 18, 30, 33, 41).
- Reconstruction de l'index alphabétique (tri strict A-Z, tabulations à droite, renvois exacts).
- Bon de commande détachable ou numérique complet (TVA 20 % alcool / 5,5 % jus de raisin, port, net à payer TTC, champs légaux, CGV à cocher, cachet et signature).

**Chantier E — Sécurisation juridique et conformité**
- Page de CGV (art. L. 441-1 : réserve de propriété, délais LME 60 j / 45 j fin de mois, pénalités, indemnité de 40 €).
- Ours commercial complété (forme juridique, capital, RCS complet, TVA intracommunautaire).
- Bloc-marque vectorisé verrouillé (fin de ACENCE, HAGENCE, AVINSA…).
- Mention sanitaire exacte + logo Triman avec info-tri Citeo (remplace « Ne pas jeter sur la voie publique »).

### 10.2 Tableau récapitulatif du plan d'action

| Chantier | Action immédiate | Résultat attendu |
|---|---|---|
| Tarifs & Données | Automatisation des grilles via PIM / tableur, restauration de la dégressivité et clarification des BIB | Tarifs mathématiquement cohérents, fin des litiges et confiance acheteur restaurée |
| Graphisme & PAO | Gabarit InDesign épuré, fonds blancs, 2-3 couleurs max, typographie lisible (> 8 pt) et césures contrôlées | Confort de lecture optimal, perception haut de gamme conforme au secteur des vins |
| Visuels & Packshots | Détourage de photos flacons en 300 DPI (CMJN) pour l'ensemble des cuvées | Mise en valeur du packaging, facilitation du référencement en cave |
| Contenu œnologique | Ajout des assemblages (%), modes d'élevage, notes de dégustation et garde sur chaque vin | Outil de prescription actif et argumentaire d'aide à la vente pour le caviste |
| Navigation | Correction intégrale du sommaire (pages paires incluses) et réfection de l'index alphabétique | Visibilité restaurée sur 100 % de l'offre (notamment les grands crus) |
| Juridique | Insertion d'une page de CGV (art. L. 441-1), ajout de la forme juridique/TVA, logo Triman et mention Évin corrigée | Conformité légale stricte, neutralisation des risques de sanctions DGCCRF |

### 10.3 Protocole d'assainissement d'urgence (plan de redressement en quatre axes)

Recommandation de l'audit formel : **retirer immédiatement le catalogue actuel du circuit de diffusion**, puis mettre en œuvre sans délai un plan de redressement articulé autour de quatre axes.

1. **Reconstruction des bases de données et assainissement mathématique.** Reprogrammer l'ensemble des matrices de calcul sous un PIM ou une feuille de calcul automatisée. Rétablir une dégressivité rigoureuse garantissant un prix au col inférieur pour les commandes par cartons de 60, 120, 300 cols ou à la palette. Remettre les prix des Bag-in-Box « à l'endroit », renseigner les colonnes couleurs, harmoniser les séparateurs décimaux sous la virgule française, annexer une grille transparente des forfaits de transport (franco ou tranche de poids).
2. **Refonte globale de la maquette graphique et iconographique.** Confier l'exécution prépresse à un graphiste maîtrisant Adobe InDesign ; grille aérée sur fond blanc pur ou ivoire très pâle ; proscrire les aplats agressifs au profit d'une signalétique sobre (trois teintes maximum) ; rééquilibrer le chemin de fer pour intégrer systématiquement un packshot bouteille détouré en haute définition (300 DPI) par cuvée, éliminant les pages semi-vides ; vectoriser et verrouiller le bloc-marque.
3. **Restructuration de l'architecture éditoriale et des outils de commande.** Recomposer intégralement le sommaire (secondes pages de Goichot p. 18, Haut Marin p. 30, Passion des Terroirs p. 33, Famille d'Exea p. 41) ; reconstruire de zéro l'index alphabétique avec tabulations automatiques à droite et renvois pointant vers les folios exacts ; repenser le bon de commande sous la forme d'un encart A4 autonome, multi-lignes, avec champs de ventilation comptable de TVA, calcul de port et mentions d'acceptation contractuelle.
4. **Mise en conformité réglementaire et relecture prépresse impitoyable.** Page dédiée aux CGV rédigées conformément à l'article L. 441-1 (encadrement LME, pénalités, forfaits de recouvrement, clause de réserve de propriété) ; ours commercial complété (forme sociale, capital, TVA intracommunautaire) ; avertissement de santé publique rétabli sans mots soudés ni coquilles ; signalétique Triman/Citeo ; relecture croisée rigoureuse de toute la publication avant validation du BAT.

### 10.4 Les 10 changements à faire en premier (priorités de l'audit conversationnel)

1. 🔥 **Repenser la couverture** — plus « vin », moins photo générique de biodiversité.
2. 🍷 **Agrandir énormément les bouteilles** — le produit doit devenir le héros.
3. 🎨 **Donner une vraie identité à chaque région** — pas seulement un petit onglet coloré.
4. 📖 **Créer plusieurs types de pages** — standard / premium / découverte / domaine phare.
5. ⭐ **Ajouter des badges commerciaux** — coup de cœur, nouveauté, allocation, bio, signature, etc.
6. 📊 **Remonter légèrement la taille des tableaux** — particulièrement pour la consultation numérique.
7. 🧠 **Transformer les descriptions en argumentaires de vente** — moins « fiche institutionnelle », davantage « pourquoi le caviste doit le prendre ».
8. 🥂 **Ajouter des informations de dégustation** — cépages, profil, accords, style, positionnement.
9. 💰 **Vérifier tous les paliers tarifaires** — en particulier les deux anomalies identifiées aux pages 21 et 25.
10. 💻 **Faire une vraie version « PDF interactif »** — signets + navigation + liens + QR + commande.

**Principe directeur associé :** ne pas tout détruire. La structure « identité → conditions → tableau » est excellente pour un tarif caviste ; le sommaire, l'index, les conditions par domaine et les tableaux sont déjà organisés comme un vrai outil professionnel. Le problème est d'avoir construit un excellent squelette de tarif pro puis d'avoir essayé d'en faire un catalogue éditorial. Recommandation : **garder le moteur commercial et lui ajouter une vraie direction artistique de catalogue premium** — pour passer d'un document qui dit « Voici nos 40 domaines et leurs prix » à un document qui dit « Voici pourquoi ces 40 domaines méritent une place dans votre cave ». Il est également conseillé de ne pas tout refaire d'un coup, mais de procéder par paliers de transformation.

### 10.5 Les cinq décisions de réparation (audit technique mesuré)

1. **Un tarif dense :** une ligne par référence avec code article, cépages, degré et prix de vente conseillé, et le prix en gras.
2. **Des remises lisibles :** un prix de base pour les petites quantités, des paliers simples, et le coût du port affiché.
3. **Une vraie version écran :** format paysage, signets, recherche fonctionnelle, bon de commande remplissable (ou lien vers une commande en ligne).
4. **Un standard photo unique :** bouteille détourée et portrait légendé, pour chaque domaine.
5. **Une relecture complète.**

### 10.6 Feuille de route par paliers de transformation

| Palier | Objectif | Contenu (renvois) |
|---|---|---|
| 🔴 **Palier 0** — Corriger ce qui peut nuire | Zéro anomalie de données, zéro incohérence typographique, zéro information ambiguë | Vérification automatique des paliers de prix (Verchères, Pousterle, 301 bt), formats « — », uniformité des unités, orthographe globale, intégration graphique des mentions légales — voir 2.2.1 |
| 🟠 **Palier 1** — De « tarif propre » à « vrai catalogue » | Casser la monotonie et remettre la bouteille au centre | Plusieurs types de pages A/B/C/D (3.2.4) ; hiérarchie commerciale et badges, 4 max (5.2.1) ; bouteille = héros (4.2.2) ; chaque image a une fonction (4.2.1) ; transformer l'espace vide en encadrés « À retenir / Profil / Cépages / Accords » (voir ci-dessous) |
| 🟡 **Palier 2** — Améliorer l'expérience de lecture | Tableaux moins « Excel », prix lisibles, conditions scannables | Travail sur hauteur de ligne, espacement, graisse des références, alignement des prix, séparation des catégories, hiérarchie des colonnes, couleurs très légères, distinction des paliers (voir ci-dessous) ; prix en point d'ancrage visuel ; conditions en 4 pictogrammes (3.2.5) ; couleurs régionales en accent (3.2.1) ; pages « moments forts » (3.2.6) |
| 🟢 **Palier 3** — Niveau « catalogue premium » | Donner une véritable identité éditoriale | Refaire la couverture (4.2.3) ; repenser la première double page ; retravailler les textes des domaines (5.2.3) ; ajouter une vraie fiche produit dosée (6.2.2) |
| 🟢 **Palier 4** — PDF → outil commercial digital | Rendre le catalogue actionnable en ligne | Signets, navigation permanente, QR codes stratégiques — voir 8.2.3 |
| 🟢 **Palier 5** — Refaire le système commercial | Catalogue officiel SCIO sur plusieurs années | Architecture commerciale en parties (5.2.6) ; hiérarchie des domaines niveaux 1-2-3 (5.2.2) ; logique « caviste », 3 cuvées à retenir (5.2.5) |

**Détails complémentaires des paliers 1, 2 et 3** (points qui n'ont pas de section dédiée ci-dessus) :

- *Transformer l'espace vide en outil de vente* (palier 1) : ne pas combler le vide en ajoutant du texte partout (mauvaise solution), mais transformer une partie du vide en encadrés utiles — « À retenir » (ex. Bio · 20 ha · Vendanges manuelles · 3 appellations · Allocation · Franco dès 120 bt) ; « Profil » (ex. Frais · Minéral · Floral) ; « Cépages » (ex. Chardonnay · Pinot noir · Chenin) ; « Accords » (ex. Poissons · coquillages · cuisine végétale). Principe : *espace vide ≠ mauvais design ; le problème est l'espace vide sans fonction.* Deux options assumées : soit le luxe (grand vide maîtrisé, vraie composition éditoriale), soit le catalogue commercial (exploiter l'espace pour notes de dégustation, cépages, terroir, accords, points forts, grandes bouteilles, encadré « notre sélection », QR code, contact commercial, argumentaire caviste) — aujourd'hui, le catalogue reste entre les deux.
- *Tableaux moins « Excel »* (palier 2) : conserver la structure APPELLATION | CUVÉE | COULEUR | MILL. | FORMAT puis PRIX HT, avec les paliers bien séparés ; retravailler hauteur de ligne, espacement, graisse, alignement des prix, séparation des catégories, hiérarchie des colonnes, couleurs très légères, distinction visuelle des paliers.
- *Prix comme point d'ancrage commercial* (palier 2) : faire ressortir visuellement le prix (ex. « 6,90 € ») plutôt que de donner exactement le même poids à appellation, cuvée, millésime, format et prix.
- *Première double page* (palier 3) : remplacer la page 2 très « documentaire » (comment lire le tarif, labels, couleurs, abréviations, paliers) par : **À propos de SCIO** (un vrai éditorial) → **Comment utiliser ce catalogue** (avec 5 pictogrammes) → **Nos engagements** (Bio, Biodynamie, petits domaines, vignerons indépendants, etc.) — pour transformer l'introduction en manifeste commercial.
- *Pour la fiche produit* (palier 3) : informations possibles — cépage, profil, accords, élevage, température de service, positionnement, RRP conseillé, marge indicative, EAN, colisage, disponibilité ; maximum 3 informations supplémentaires par cuvée stratégique.

---

## 11. Annexe — Sources consultées

Références citées dans les analyses (guides de conception de catalogues, mentions légales des documents commerciaux, typographie et charte graphique) :

- afineo.com — *Comment faire un catalogue commercial : 8 conseils, 5 étapes*
- graphicstyle.fr — *Mise en page Catalogue : Méthode d'Expert & Impression Brochure*
- sortlist.fr — *Nos 10 meilleurs conseils pour une plaquette commerciale réussie*
- entreprendre.service-public.gouv.fr — *Documents commerciaux d'une société*
- corep.fr — *Mentions obligatoires sur les prospectus*
- youlovewords.com — *Le guide ultime pour créer sa charte graphique (+ templates)*
- one-learn.fr — *Comment faire une brochure professionnelle ?*
- easycom.fr — *Comment choisir le bon format pour vos catalogues ?*
- wearebold.co — *Mentions obligatoires d'un contrat commercial (BOLD Avocats)*
- bpifrance-creation.fr — *Les mentions à porter sur les documents commerciaux*
- legifrance.gouv.fr — *Sous-section 4 : Des mentions sur les papiers d'affaires (articles R. 123-237 et suivants)*
- assistant-juridique.fr — *Publicité : les mentions obligatoires*
- lamaisonducommercial.fr — *Les mentions obligatoires sur les documents commerciaux*
- hautes-alpes.cci.fr — *Les mentions obligatoires sur les documents commerciaux*
- *How to create and format a catalog* ; *Réaliser votre premier catalogue : les 10 erreurs à ne pas commettre* ; publication ChilliPrinting sur la transformation d'un catalogue en outil marketing
- Catalogue Milliet (référence de comparaison pour le CHR)
- Le fichier analysé : `catalogue_ecran.pdf`
