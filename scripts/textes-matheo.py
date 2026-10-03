#!/usr/bin/env python3
"""Les textes de présentation et les labels du dossier de référence de Mathéo (2 octobre 2026).

L'agence : « il faut se référer à son document » pour le texte et les labels. Ce script les
écrit dans data/salon-prive-2026.json (`texte_reference`, `fiche_texte`, `label_liste_salon`,
`labels_affiches`), puis compare chaque texte à celui de la fiche (texte du tarif).
Les noms propres gardent la graphie des fiches (Boehler, Berteaud Manceau) ; les apostrophes
droites deviennent typographiques, comme partout dans le catalogue ; les espaces doubles
deviennent simples.

Le texte du stand 7 présente le groupe Strasser-Radziwill, pas un domaine : il n'a pas de
fiche à lui (`fiche_texte: null`). Celui du stand 26 présente la Maison André Goichot (n°12).

Au salon, chaque fiche prend le texte de sa carte, tel quel. Au catalogue général, la fiche
prend le même texte moins les phrases propres au salon (« Vins sous allocation. », « Format BIB
disponible. », « Ratafia disponible. », « Panachage possible… ») : le catalogue les dit déjà
par ses jetons, ses tableaux et ses encarts. Le texte du tarif reste dans `texte_tarif`.
"""
import difflib, json, pathlib, re

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHIER = RACINE / "data/salon-prive-2026.json"

# stand → (fiche dont c'est le texte, label, texte tel que le dossier l'écrit)
TEXTES = {
 1: (29, "Bio", "Au cœur d'une forêt de deux cents hectares, la famille Touchais veille depuis 1964 sur dix hectares de vignes à Saint-Laurent-Médoc. Classé Cru Bourgeois Supérieur et certifié bio, Balac cultive autour de sa chartreuse du XVIIIe siècle des vins de caractère et d'élégance."),
 2: (38, "En conversion Bio", "Enracinée depuis 7 générations à Monthelon, entre Côte des Blancs et Vallée de la Marne, la Maison Denis Frézier conjugue mémoire et durabilité. Certifiée HVE et VDC, engagée en conversion biologique, elle sculpte les cuvées : Trois Crus, Terroir Noir et Terroir Blanc. Ratafia disponible. Vins sous allocation."),
 3: (36, "HVE", "Au pied de la Montagne d'Alaric, au cœur des Corbières, Laurence et Vincent Licciardi-Pirot cultivent des vignes plantées en terrasses et balayées par le vent du Cers. Les vins sont élevés dans une ancienne cave de village à demi enterrée : des rouges chaleureux du Midi, des blancs et des rosés tout en fraîcheur."),
 4: (3, "HVE", "Quatre générations de passionnés et adhérent historique des Vignerons Indépendants : Jean-Yves Bretaudeau allie bon sens paysan et précision œnologique. Certifié HVE, le domaine préserve ses paysages ligériens pour des vins frais et expressifs. Format BIB disponible."),
 5: (15, "HVE", "Propriété familiale transmise depuis sept générations, établie à Mancey au cœur du Mâconnais. Certifié HVE, le domaine limite rigoureusement ses intrants pour préserver la vie des sols et alimente sa cave en énergie solaire, pour des vins purs, gourmands et équilibrés."),
 6: (23, "HVE 3", "En plein cœur de la Gascogne à Gondrin, les familles Jegerlehner et Prataviera subliment sables fauves et sous-sols argilo-calcaires riches en fossiles marins. Cette fraîcheur insuffle aux cépages gascons éclat aromatique et vivacité saline. IGP Côtes de Gascogne et Bas-Armagnac. Format BIB disponible."),
 7: (None, "Bio", "Regroupement de quatre domaines de la vallée du Rhône réunis au sein du groupe Maisons & Vignobles Strasser-Radziwill : le Prieuré des Papes à Châteauneuf-du-Pape, le Domaine de Coyeux au pied des Dentelles de Montmirail, le Domaine du Moulin Blanc et le Domaine de la Pousterle. Panachage possible entre les quatre domaines."),
 8: (27, "Biodynamie", "Sentinelle édifiée en 1612 sur les coteaux argilo-calcaires de Bayon, Falfas est une référence pionnière de la biodynamie bordelaise, membre fondateur de Biodyvin sous la houlette de John et Véronique Cochran. Vingt hectares vendangés à la main pour des Côtes de Bourg racés et de longue garde."),
 9: (8, "Bio", "Berceau de tradition vigneronne à Molsheim, le Domaine Boehler aborde une nouvelle ère sous l'impulsion de Julien et Aurélie. Converti à l'agriculture biologique, le tandem explore ses coteaux et le prestigieux Grand Cru Bruderthal pour des vins verticaux, précis et profonds."),
 10: (1, "Bio", "Créés ex nihilo en 2023, deux vignobles jardins conduits en agriculture biologique : l'un à Sancerre, où François Reverdy est le plus petit vigneron de l'appellation, l'autre à Roiffé entre Saumur et Chinon, en vieilles vignes de Grolleau noir, Cabernet Franc et Chenin blanc. Vendanges à la main et vins éco-conçus, en Anjou, Saumur, Chinon, Quincy et Sancerre."),
 11: (37, "En conversion Bio", "Fidèle à la ferme de La Voglonière depuis 1919, la famille Dekeyne cultive une relation intime avec la terre champenoise. Engagé en conversion biologique, ce domaine de quatre générations élabore des champagnes d'artisan à la vibrante énergie de sol. Ratafia disponible. Vins sous allocation."),
 12: (21, "Bio", "Les Vignobles Trichon-Bernard réunissent deux terroirs certifiés en agriculture biologique. Les Côtes du Rhône méridionales donnent le Grenache, la Syrah, le Mourvèdre, la Clairette, le Muscat et le Viognier ; le Bugey donne le Chardonnay, l'Altesse, le Gamay, le Pinot Noir et la Mondeuse. Claire et Stéphane, associés dans le projet, allient leurs savoir-faire à la vigne et dans la création des cuvées."),
 13: (34, "Bio", "Alain, Patricia et leurs fils révèlent l'âme de Gragnos par un soin méticuleux apporté à chaque pied de vigne. Engagé dans une conversion biologique, le domaine privilégie un accompagnement doux du végétal pour laisser rayonner l'identité du terroir sans le contraindre."),
 14: (4, "HVE", "Depuis 1921 à Faye-d'Anjou, cinq générations se transmettent 24 hectares de coteaux argilo-schisteux remarquablement exposés. Le Chenin donne aussi bien les liquoreux du Coteaux du Layon que des Anjou Blanc et Crémant de Loire d'une minéralité tactile."),
 15: (40, "En conversion Bio", "Maison de référence à Chouilly, Grand Cru de la Côte des Blancs, Vazart-Coquart célèbre le Chardonnay depuis 1954. Jean-Pierre et Caroline veillent sur trente parcelles (11 ha) où la craie révèle toute la finesse du cépage."),
 16: (28, "Biodynamie", "Perchée à 120 mètres au-dessus de la vallée de la Dordogne, cette propriété de 1860 conduit une biodynamie certifiée Demeter d'une remarquable précision. Vinifications douces, sulfites au strict minimum, élevages en barriques et amphores : des vins vivants, d'une grande vibration minérale."),
 17: (6, "ISO 26000", "Spécialiste du Sauvignon Blanc ligérien, le domaine explore les plus beaux terroirs de Loire (Sancerre, Pouilly-Fumé, Menetou-Salon, Touraine). Techniques modernes et respect de la typicité des sols calcaires et de silex pour des blancs d'une grande pureté."),
 18: (10, "Agriculture raisonnée", "Installé à Meursault depuis 2004, Sébastien Magnien conduit 12 hectares sur les terroirs d'élite de la Côte de Beaune et des Hautes-Côtes (Pommard, Volnay, Puligny, Saint-Romain). Vendanges manuelles et élevages en fûts de chêne signent des Pinots et Chardonnays d'élégance et de tension. Vins sous allocation."),
 19: (31, "Bio", "Écrin préservé à Tourves, Blacailloux incarne la Provence Verte depuis plus d'un siècle, conduit par la quatrième génération de la famille Chamoin. Chai bioclimatique à toit végétalisé et énergie photovoltaïque. Cuvées AOP Coteaux Varois et IGP Var, fraîches et aériennes. Format BIB disponible."),
 20: (22, "En conversion Bio", "Né de la transmission d'une vigne de 80 ans en Madiran par son grand-père, le projet de Simon cultive la rareté : produire peu pour produire sain. Environ six hectares en Madiran et Pacherenc-du-Vic-Bilh, en symbiose avec un élevage de bœufs Angus sur la ferme. Vins sous allocation."),
 21: (32, "Bio", "Depuis plusieurs générations, la famille d'Exea façonne sur les terroirs solaires du Languedoc des vins biologiques vibrants et sincères, alliant pureté du fruit et convivialité. Panachage possible avec la gamme de purs jus de cépages. Format BIB disponible."),
 22: (2, "Bio", "Sur les reliefs bocagers du Chantonnais, Vincent et Alban Orion sculptent 30 hectares reflétant la diversité des terroirs chantonnaisiens. Une démarche paysanne faite de travail manuel minutieux et d'attention à la faune et à la flore, qui porte le domaine en agriculture biologique. Vins sous allocation."),
 23: (39, "Biodynamie", "À Villers-aux-Nœuds, sur les terroirs Premier Cru de la Montagne de Reims, Olivier Langlais conduit 6 hectares en biodynamie. En cave, vinifications douces, sans chaptalisation, sans filtration et sans dosage : une Champagne d'émotion, minérale et d'une lumineuse franchise de terroir."),
 24: (30, "Bio", "Joyau intimiste à Saint-Germain-de-la-Rivière, en AOP Fronsac, qui renaît sous la conduite de Mélanie et Thomas. Vendanges manuelles, fermentations spontanées, sulfites mesurés et élevage sur-mesure (barriques, béton, amphores) pour des Merlots et Cabernets Francs veloutés et floraux."),
 25: (5, "Bio", "Premier chai urbain de La Roche-sur-Yon, à Mouilleron-le-Captif, fondé par deux amis d'enfance vendéens diplômés en ingénierie agricole à Angers. Les raisins proviennent de 8 domaines partenaires du Val de Loire. Levures indigènes : des jus digestes et éclatants."),
 26: (12, "HVE", "Fleuron familial et indépendant fondé en 1947, la Maison André Goichot porte l'exigence des grands climats de Bourgogne. Sélections parcellaires méticuleuses et cuverie d'élevage de pointe inaugurée en 2020. Panachage possible avec le Château du Cray et le Domaine Les Guignottes. Vins sous allocation."),
}


def typo(t):
    return re.sub(r"\s+", " ", t.replace("'", "’")).strip()


SALON_SEUL = re.compile(r"\s*(Vins sous allocation|Format BIB disponible|Ratafia disponible|"
                        r"Panachage possible [^.]*)\.")


def texte_general(t):
    return re.sub(r"\s+", " ", SALON_SEUL.sub("", t)).strip()


def ecrire_texte(chemin, texte):
    """Remplace texte_source dans la fiche mise en page à la main ; garde l'ancien dans texte_tarif."""
    brut = chemin.read_text(encoding="utf-8")
    fiche = json.loads(brut)
    if fiche["texte_source"] == texte:
        return False
    ancien = json.dumps(fiche["texte_source"], ensure_ascii=False)
    nouveau = json.dumps(texte, ensure_ascii=False)
    assert brut.count(f'"texte_source": {ancien}') == 1, chemin
    ajout = ""
    if "texte_tarif" not in fiche:
        ajout = f',\n  "texte_tarif": {ancien}'
    brut = brut.replace(f'"texte_source": {ancien}', f'"texte_source": {nouveau}{ajout}')
    fiche = json.loads(brut)
    fiche["texte_source"]   # toujours du JSON valide
    chemin.write_text(brut, encoding="utf-8")
    return True


def main():
    salon = json.loads(FICHIER.read_text(encoding="utf-8"))
    fiches = {int(p.stem): json.loads(p.read_text(encoding="utf-8"))
              for p in (RACINE / "data/fiches").glob("*.json")}
    rapport = []
    for s in salon["stands"]:
        fiche, label, texte = TEXTES[s["stand"]]
        texte = typo(texte)
        s["texte_reference"] = texte
        s["fiche_texte"] = fiche
        s["label_liste_salon"] = label
        # le label de la carte vaut pour chaque fiche du stand (Goichot : la Maison seule)
        doms = s["domaines"]
        s["labels_affiches"] = {str(n): ([label] if (s["stand"] != 26 or n == 12) else []) for n in doms}
        if fiche:
            avant = typo(fiches[fiche]["texte_source"] or "")
            if avant != texte:
                mots = [d for d in difflib.ndiff(avant.split(), texte.split()) if d[0] in "+-"]
                rapport.append((s["stand"], fiche, " ".join(mots)))
    FICHIER.write_text(json.dumps(salon, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ecrits = []
    for s in salon["stands"]:
        if s["fiche_texte"] and ecrire_texte(RACINE / f"data/fiches/{s['fiche_texte']:02d}.json",
                                             texte_general(s["texte_reference"])):
            ecrits.append(s["fiche_texte"])
    print(f"catalogue général : texte de {len(ecrits)} fiche(s) mis à jour : {ecrits}")
    print(f"{len(rapport)} textes de carte diffèrent de la fiche d'origine :")
    for st, n, m in rapport:
        print(f"  stand {st} (n°{n}) : {m}")


if __name__ == "__main__":
    main()
