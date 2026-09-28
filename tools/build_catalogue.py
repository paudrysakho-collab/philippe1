"""Fusionne les trois sources en une base unique : data/catalogue.json.

Priorité des sources, conformément à la feuille de route validée :
  1. l'Excel de l'agence  → prix, paliers, millésimes, formats (20 domaines)
  2. l'ancien tarif Canva → textes, conditions de port, départements (40 domaines)
  3. la maquette 52 pages → ossature des cuvées pour les 20 domaines hors Excel,
                            plus les textes de présentation déjà réécrits
Rien n'est inventé : une donnée absente vaut « — » et part dans le rapport.
"""
import json, re, unicodedata
from collections import OrderedDict

OSS = json.load(open("data/ossature-maquette.json"))
XLS = json.load(open("data/prix-excel.json"))
TAR = json.load(open("data/source-tarif.json"))
OUT = "data/catalogue.json"

TIRET = "—"
COULEURS = ("Blanc", "Rosé", "Rouge", "Orange")


def pli(s):
    """Forme repliée d'un nom, pour rapprocher deux graphies du même domaine."""
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\b(domaine|chateau|champagne|chai|maison|le|la|les|du|de|des|d|et|fils|&)\b",
               " ", s)
    return re.sub(r"[^a-z0-9]", "", s)


def split_couleur(brut):
    """Sépare la couleur du style : la colonne Couleur ne doit porter qu'une couleur.

    L'Excel mélange les deux (« Blanc brut », « Blanc de Blancs », « Blanc sec »).
    Le cahier des charges impose Blanc / Rosé / Rouge / Orange dans la colonne, et
    le style en ligne secondaire sous le nom de cuvée.
    """
    b = " ".join((brut or "").split())
    if not b:
        return TIRET, ""
    for c in COULEURS:
        if b.lower().startswith(c.lower()):
            return c, b[len(c):].strip(" -–")
    if b.lower().startswith("blanc"):
        return "Blanc", b[5:].strip(" -–")
    return TIRET, b


def split_millesime(brut):
    """« Base 2023 » n'est pas un millésime : c'est un non-millésimé sur base 2023."""
    b = " ".join((brut or "").split()).replace("–", TIRET)
    if not b or b in ("-", TIRET):
        return TIRET, ""
    m = re.fullmatch(r"[Bb]ase\s*(\d{4})", b)
    if m:
        return "NM", f"base {m.group(1)}"
    return b.replace("/20", "/"), ""


def norm_palier(lib):
    """Notation unique des paliers : « jusqu'à 36 bt », « dès 48 bt », « Palette ».

    L'Excel dit « À partir de 48 bts », « De 60 à 120 bts », « Plus de 300 bts »,
    « À partir de 120 cols ». Le catalogue doit parler d'une seule voix, et « bt »
    est invariable.
    """
    b = " ".join((lib or "").split())
    if not b or b.lower() == "tarif":
        return "Prix unique"
    if b.lower().startswith("palette"):
        return "Palette"
    m = re.search(r"jusqu.?à\s*(\d+)", b, re.I)
    if m:
        return f"jusqu’à {m.group(1)} bt"
    m = re.search(r"de\s*(\d+)\s*à\s*(\d+)", b, re.I)
    if m:
        return f"dès {m.group(1)} bt"
    m = re.search(r"plus de\s*(\d+)", b, re.I)
    if m:
        return f"dès {int(m.group(1)) + 1} bt"
    m = re.search(r"(?:à partir de|dès)\s*(\d+)", b, re.I)
    if m:
        return f"dès {m.group(1)} bt"
    return b


PIED = {"port_en_sus": "Prix HT par bouteille, transport en sus",
        "franco": "Prix HT par bouteille, franco de port",
        "inconnu": "Prix HT par bouteille, conditions de port sur demande"}


def pied_port(port):
    if port["type"] == "franco_seuil":
        return f"Prix HT par bouteille, franco dès {port['seuil']} bt"
    return PIED[port["type"]]


def case_port(port):
    if port["type"] == "franco_seuil":
        return f"Franco dès {port['seuil']} bt"
    return {"port_en_sus": "Port en sus", "franco": "Franco",
            "inconnu": "Sur demande"}[port["type"]]


def main():
    tar = {f["numero"]: f for f in TAR["fiches"]}
    # rapproche chaque feuille Excel de son numéro de fiche
    par_nom = {pli(f["nom"]): f["numero"] for f in OSS["fiches"]}
    xls_par_fiche, orphelines = OrderedDict(), []
    for d in XLS["domaines"]:
        num = par_nom.get(pli(d["nom"])) or par_nom.get(pli(d["feuille"]))
        if num is None:
            for k, v in par_nom.items():
                if k and (k in pli(d["feuille"]) or pli(d["feuille"]) in k):
                    num = v
                    break
        if num is None:
            orphelines.append(d["feuille"])
        else:
            xls_par_fiche.setdefault(num, []).append(d)

    fiches, alertes = [], []
    for o in OSS["fiches"]:
        n = o["numero"]
        t = tar.get(n, {"port": {"type": "inconnu", "seuil": None},
                        "departements": [], "port_source": None, "page_source": None})
        xs = xls_par_fiche.get(n, [])

        f = {
            "numero": n,
            "nom": o["nom"],
            "region": o["region"],
            "sous_titre": o["sous_titre"],
            "labels": o["labels"],
            "texte": o["texte"],
            "pages_maquette": o["pages_maquette"],
            "page_source_tarif": t.get("page_source"),
            "departements": t["departements"],
            "port": t["port"],
            "port_source": t.get("port_source"),
            "pied_port": pied_port(t["port"]),
            "conditions": {
                "PORT": case_port(t["port"]),
                "PALIERS": None,
                "PANACHAGE": o["conditions"].get("PANACHAGE", TIRET) or TIRET,
                "PARTICULARITÉS": o["conditions"].get("PARTICULARITÉS", TIRET) or TIRET,
            },
            "origine_prix": "excel" if xs else "maquette",
            "feuilles_excel": [d["feuille"] for d in xs],
            "descriptif_excel": " / ".join(d["descriptif"] for d in xs if d["descriptif"]),
            "validite": None,
            "paliers": [],
            "tables": [],
            "notes_source": [],
        }
        for d in xs:
            m = re.search(r"valables? jusqu.au\s*([\d/]+)", d["conditions_source"] or "", re.I)
            if m:
                f["validite"] = m.group(1)

        if xs:
            # --- source n° 1 : l'Excel. Une feuille = un tableau. Le Domaine
            # Trichon en a deux (Rhône et Savoie) : ils restent distincts, chacun
            # avec ses propres paliers, comme dans la source.
            for d in xs:
                titre = None
                if len(xs) > 1:
                    m = re.search(r"\(([^)]+)\)", d["feuille"])
                    titre = m.group(1) if m else d["feuille"]
                lignes = []
                for cu in d["cuvees"]:
                    coul, style = split_couleur(cu["couleur_style"])
                    mill, note = split_millesime(cu["millesime"])
                    lignes.append({
                        "appellation": cu["appellation"] or TIRET,
                        "cuvee": cu["cuvee"] or TIRET,
                        "note": " · ".join(x for x in (style, note) if x),
                        "couleur": coul, "millesime": mill,
                        "format": cu["format"] or TIRET, "prix": cu["prix"],
                        "source": f"excel:{d['feuille']}:L{cu['ligne_excel']}"})
                f["tables"].append({
                    "type": "BT", "titre": titre,
                    "paliers": [norm_palier(p["libelle"]) for p in d["paliers"]],
                    "lignes": lignes})
                for n_ in d["notes"]:
                    if n_ not in f["notes_source"]:
                        f["notes_source"].append(n_)
        else:
            # --- source n° 3 : ossature de la maquette, à contrôler sur image
            for t in o["tables"]:
                if t["type"] != "BT":
                    continue
                lignes = []
                for l in t["lignes"]:
                    coul, style = split_couleur(l["couleur"])
                    mill, note = split_millesime(l["millesime"])
                    lignes.append({
                        "appellation": l["appellation"], "cuvee": l["cuvee"],
                        "note": " · ".join(x for x in (style, note) if x),
                        "couleur": coul, "millesime": mill, "format": l["format"],
                        "prix": l["prix"],
                        "source": "maquette (à contrôler sur image)"})
                f["tables"].append({
                    "type": "BT", "titre": None,
                    "paliers": [norm_palier(x) for x in t["libelles"]] or ["Prix unique"],
                    "lignes": lignes})

        # Bag-in-box : toujours repris de la maquette, sur la même grille de colonnes.
        # Les sous-colonnes du bloc Prix y portent des contenances, pas des paliers.
        for t in o["tables"]:
            if t["type"] != "BIB":
                continue
            lignes = []
            for l in t["lignes"]:
                coul, style = split_couleur(l["couleur"])
                lignes.append({"appellation": l["appellation"], "cuvee": l["cuvee"],
                               "note": style, "couleur": coul,
                               "millesime": split_millesime(l["millesime"])[0],
                               "format": "BIB", "prix": l["prix"],
                               "source": "maquette (à contrôler sur image)"})
            f["tables"].append({"type": "BIB", "titre": "Bag-in-box",
                                "paliers": [norm_palier(x) for x in t["libelles"]],
                                "lignes": lignes})

        # L'extraction sépare parfois un tableau en deux parce que la maquette
        # répétait son en-tête en haut de la page suivante. Deux tableaux de même
        # type et de mêmes paliers sont un seul tableau : on les recolle, sinon une
        # cuvée isolée se retrouve sous un en-tête complet pour elle seule.
        fusion = []
        for t in f["tables"]:
            if (fusion and fusion[-1]["type"] == t["type"]
                    and fusion[-1]["paliers"] == t["paliers"]
                    and not t.get("titre") and not fusion[-1].get("titre")):
                fusion[-1]["lignes"] += t["lignes"]
            else:
                fusion.append(t)
        f["tables"] = fusion

        f["paliers"] = f["tables"][0]["paliers"] if f["tables"] else ["Prix unique"]
        f["conditions"]["PALIERS"] = (" · ".join(f["paliers"])
                                      if f["paliers"] != ["Prix unique"] else "Prix unique")

        # Contrôles de cohérence : on consigne, on ne corrige jamais.
        for t in f["tables"]:
            for l in t["lignes"]:
                v = [float(p.replace(",", ".")) for p in l["prix"]
                     if re.fullmatch(r"[\d,]+", p)]
                if len(v) < 2:
                    continue
                monte = any(v[i + 1] > v[i] for i in range(len(v) - 1))
                if monte and t["type"] == "BT" and len(t["paliers"]) > 1:
                    alertes.append({"type": "degressivite_inversee", "fiche": n,
                                    "cuvee": f"{l['cuvee']} {l['format']}",
                                    "prix": l["prix"], "source": l["source"]})
                elif monte and t["type"] == "BIB":
                    # Dans un tableau BIB, les colonnes sont des CONTENANCES, pas des
                    # paliers : un 10 L coûte normalement plus cher qu'un 5 L. Un prix
                    # qui monte est donc attendu. On ne signale que l'anomalie réelle :
                    # un prix au litre qui augmente avec la contenance.
                    lit = []
                    for lib, px in zip(t["paliers"], l["prix"]):
                        m = re.search(r"(\d+)\s*L", lib)
                        if m and re.fullmatch(r"[\d,]+", px):
                            lit.append(float(px.replace(",", ".")) / int(m.group(1)))
                    if len(lit) > 1 and any(lit[i + 1] > lit[i] for i in range(len(lit) - 1)):
                        alertes.append({"type": "bib_prix_au_litre_croissant", "fiche": n,
                                        "cuvee": l["cuvee"], "colonnes": t["paliers"],
                                        "prix": l["prix"], "source": l["source"]})
            for l in t["lignes"]:
                if t["paliers"] and len(t["paliers"]) > 1 and 0 < len(l["prix"]) < len(t["paliers"]):
                    alertes.append({"type": "moins_de_prix_que_de_paliers", "fiche": n,
                                    "cuvee": l["cuvee"],
                                    "detail": f"{len(l['prix'])} prix pour "
                                              f"{len(t['paliers'])} paliers"})
        fiches.append(f)

    cat = {
        "edition": "septembre 2026", "departement": "Vendée (85)", "devise": "EUR",
        "agence": {
            "nom": "Agence SCIO Vins & Spirits",
            "adresse": "71 avenue de la Libération, 44400 Rezé",
            "rcs": "843 151 663 RCS Nantes",
            "site": "www.agencescio.com", "email": "contact@agencescio.com",
            "contacts": [{"prenom": "Carline", "tel": "06 49 19 16 75"},
                         {"prenom": "Laurent", "tel": "06 80 88 07 55"}],
            "forme_juridique": None, "capital": None, "tva_intra": None,
        },
        "regions": [r for r in OSS["regions"] if r != "Et Aussi"],
        "fiches": fiches, "alertes": alertes,
        "feuilles_excel_non_rattachees": orphelines,
    }
    json.dump(cat, open(OUT, "w"), ensure_ascii=False, indent=1)

    nx = sum(1 for f in fiches if f["origine_prix"] == "excel")
    print(f"{len(fiches)} fiches — prix Excel : {nx} · prix maquette : {len(fiches)-nx}")
    nbt = sum(len(t["lignes"]) for f in fiches for t in f["tables"] if t["type"] == "BT")
    nbb = sum(len(t["lignes"]) for f in fiches for t in f["tables"] if t["type"] == "BIB")
    print(f"cuvées : {nbt} en bouteille + {nbb} en bag-in-box = {nbt + nbb}")
    print("feuilles Excel non rattachées :", orphelines or "aucune")
    print("\nrattachement Excel → fiche :")
    for n, ds in sorted(xls_par_fiche.items()):
        nom = next(f["nom"] for f in fiches if f["numero"] == n)
        print(f"   n°{n:>2} {nom:<34} ← {', '.join(d['feuille'] for d in ds)}")
    from collections import Counter
    print("\nalertes :", dict(Counter(a["type"] for a in alertes)))
    for a in alertes:
        if a["type"] == "degressivite_inversee":
            print(f"   inversion — fiche {a['fiche']} · {a['cuvee']} : "
                  f"{' → '.join(a['prix'])}  [{a['source']}]")


if __name__ == "__main__":
    main()
