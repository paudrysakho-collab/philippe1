"""Réextrait l'ossature du catalogue depuis la maquette 52 pages (texte vectoriel).

La maquette fournit l'OSSATURE (domaines, cuvées, appellations, couleurs, millésimes,
formats, paliers) et la mise en page. Les PRIX qu'elle contient sont repris tels quels
puis écrasés par l'Excel pour les 20 domaines qu'il couvre. Rien n'est deviné : une
donnée absente reste absente.
"""
import json, re
import pymupdf

SRC = "sources/maquette-52p.pdf"
OUT = "data/ossature-maquette.json"
NBSP = " "

# Bandes horizontales des colonnes, mesurées une fois : la grille du tableau est
# stable au millimètre sur les 44 pages de fiches (écart constaté 0,0 pt).
BANDS = [("appellation", 40, 145), ("cuvee", 145, 295), ("couleur", 295, 345),
         ("millesime", 345, 392), ("format", 392, 430)]
PRIX_X0 = 430

# Seuil calibré sur la maquette : un espace réel mesure 0,23 à 0,28 fois le corps,
# un espace parasite 0,15 à 0,22. La distribution est franchement bimodale
# (7 362 réels contre 1 499 parasites) : le seuil ne prête pas à discussion.
ESPACE_MINI = 0.225


def span_text(span):
    """Texte d'un span, débarrassé des espaces parasites d'interlettrage.

    La maquette interlettre ses petites capitales, ce qui insère dans la couche
    texte des espaces de largeur quasi nulle : « APPELLAT I ON », « Tuff eau »,
    « dè s 48 bt ». Conséquence, Ctrl+F ne trouve ni APPELLATION, ni CUVÉE, ni
    Tuffeau. On les retire en comparant la largeur de chaque espace au corps de la
    police : c'est géométrique, donc fiable, et rien d'autre n'est modifié.
    """
    sz = span["size"] or 1
    return "".join(c["c"] for c in span["chars"]
                   if not (c["c"] == " "
                           and (c["bbox"][2] - c["bbox"][0]) / sz < ESPACE_MINI))


def clean(s):
    return re.sub(r"\s{2,}", " ", s.replace(NBSP, " ")).strip()


def spans(page):
    out = []
    for b in page.get_text("rawdict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                t = span_text(s)
                if not t.strip():
                    continue
                x0, y0, x1, y1 = s["bbox"]
                out.append({"x": round(x0, 1), "y": round(y0, 1), "x1": round(x1, 1),
                            "h": round(y1 - y0, 1), "w": round(x1 - x0, 1),
                            "sz": round(s["size"], 1), "font": s["font"],
                            "t": clean(t)})
    return out


def band_of(x):
    for name, a, b in BANDS:
        if a <= x < b:
            return name
    return "prix" if x >= PRIX_X0 else None


def group_rows(items, tol=2.5):
    rows = []
    for it in sorted(items, key=lambda i: (i["y"], i["x"])):
        for r in rows:
            if abs(r["y"] - it["y"]) <= tol:
                r["items"].append(it)
                break
        else:
            rows.append({"y": it["y"], "items": [it]})
    return rows


def parse_sommaire(doc):
    """Régions et pages annoncées, lues sur la page Sommaire."""
    sp = spans(doc[2])
    seq = sorted(sp, key=lambda s: (round(s["x"] / 260), s["y"]))
    regions, mapping, cur = [], {}, None
    pend = None
    for s in seq:
        t = s["t"]
        if s["sz"] >= 9 and t.isupper() and len(t) > 3 and not t[0].isdigit():
            cur = t.title()
            if cur not in regions:
                regions.append(cur)
            pend = None
        elif re.fullmatch(r"\d{1,2}", t):
            if pend is None:
                pend = int(t)                      # numéro de fiche
            else:
                mapping[pend] = {"region": cur, "page_annoncee": int(t)}
                pend = None
        elif pend is not None:
            mapping[pend] = {"region": cur, "nom_sommaire": t}
    return regions, mapping


def parse_fiche(pg, page):
    sp = spans(page)
    num = None
    for s in sp:
        m = re.fullmatch(r"N°\s*(\d{1,2})", s["t"])
        if m:
            num = int(m.group(1))
            break
    if num is None:
        return None

    f = {"numero": num, "page_maquette": pg + 1, "suite": False, "nom": None,
         "sous_titre": None, "labels": [], "texte": "", "conditions": {},
         "tables": [], "pied_port": None}

    titres = [s for s in sp if "Lora" in s["font"] and s["sz"] >= 20]
    if titres:
        nom = titres[0]["t"]
        suite = [s for s in sp if s["t"].strip().lower().lstrip("— ").startswith("suite")]
        if suite or "suite" in nom.lower():
            f["suite"] = True
        f["nom"] = re.sub(r"\s*—?\s*suite\s*$", "", nom, flags=re.I).strip()

    subs = [s for s in sp if abs(s["sz"] - 10.0) < 0.3 and s["x"] < 250 and s["y"] < 200]
    if subs:
        f["sous_titre"] = subs[0]["t"]

    # labels de certification : petites capitales, à droite, au-dessus du texte.
    # L'onglet de région est exclu : il est pivoté, donc plus haut que large.
    f["labels"] = [s["t"] for s in sp if s["x"] > 480 and s["sz"] <= 7.2
                   and s["y"] < 200 and s["h"] <= s["w"]]

    txt = [s for s in sp if abs(s["sz"] - 9.8) < 0.3]
    f["texte"] = " ".join(s["t"] for s in sorted(txt, key=lambda s: s["y"]))

    def sans_espace(t):
        return t.upper().replace(" ", "")

    for lb in [s for s in sp if s["sz"] <= 7.2
               and sans_espace(s["t"]) in ("PORT", "PALIERS", "PANACHAGE",
                                           "PARTICULARITÉS")]:
        vals = [s for s in sp if abs(s["x"] - lb["x"]) < 6
                and lb["y"] < s["y"] < lb["y"] + 30 and abs(s["sz"] - 9.0) < 0.4]
        f["conditions"][sans_espace(lb["t"])] = " ".join(
            s["t"] for s in sorted(vals, key=lambda s: s["y"]))

    onglets = [s for s in sp if s["h"] > s["w"] and s["sz"] <= 8
               and len(s["t"]) >= 4 and s["t"] == s["t"].upper()
               and re.fullmatch(r"[A-ZÀ-ÜŒ' \-]{4,}", s["t"])]
    if onglets:
        brut = onglets[0]["t"].replace(" ", "")
        f["region"] = {"SUD-OUEST": "Sud-Ouest", "RHONE": "Rhône",
                       "RHÔNE": "Rhône"}.get(brut, brut.capitalize())

    pied = [s for s in sp if s["t"].startswith("Prix HT par bouteille")]
    if pied:
        f["pied_port"] = pied[0]["t"]

    # Une fiche peut porter PLUSIEURS tableaux de prix, avec des paliers différents :
    # chez Haut Marin, les vins ont trois paliers et les armagnacs un prix unique.
    # Chaque en-tête « PRIX HT / … » ouvre donc un tableau, et chaque ligne de
    # données appartient au dernier en-tête situé au-dessus d'elle.
    heads = sorted([s for s in sp if s["t"].upper().startswith("PRIX HT /")],
                   key=lambda s: s["y"])
    tables = []
    for h in heads:
        subs2 = [s for s in sp if s["x"] >= PRIX_X0 and h["y"] < s["y"] < h["y"] + 26
                 and s["sz"] <= 7.8 and not s["t"].upper().startswith("PRIX")]
        cols = {}
        for s in subs2:
            cols.setdefault(round(s["x1"] / 12), []).append(s)
        libelles = [clean(" ".join(x["t"] for x in sorted(cols[k], key=lambda s: s["y"])))
                    for k in sorted(cols)]
        tables.append({"type": "BIB" if "BIB" in h["t"].upper() else "BT",
                       "entete": h["t"], "y": h["y"], "libelles": libelles,
                       "lignes": []})

    # Lignes de données : corps 8.7 dans la police condensée du tableau, sous le
    # premier en-tête et au-dessus du pied de page. Le filtre sur la police et sur
    # la hauteur écarte le folio, qui tombait sinon dans la bande des prix.
    if tables:
        data = [s for s in sp
                if abs(s["sz"] - 8.7) < 0.4 and "Condensed" in s["font"]
                and s["y"] > tables[0]["y"] and s["y"] < 740]
        for r in group_rows(data):
            cells, prix = {}, []
            for it in sorted(r["items"], key=lambda i: i["x"]):
                b = band_of(it["x"])
                if b == "prix":
                    prix.append(it["t"])
                elif b:
                    cells[b] = (cells.get(b, "") + " " + it["t"]).strip()
            cible = tables[0]
            for t in tables:
                if r["y"] > t["y"]:
                    cible = t
            # Une « ligne » sans prix ni couleur ni format n'est pas une cuvée :
            # c'est la suite d'une cellule qui déborde sur une seconde ligne
            # (« AOP Muscadet Sèvre et / Maine »). On la recolle à la ligne
            # précédente, sinon la fin de l'appellation serait perdue.
            if not prix and not (cells.get("couleur") or cells.get("format")):
                if cible["lignes"] and cells:
                    prec = cible["lignes"][-1]
                    for k, v in cells.items():
                        prec[k] = (prec[k] + " " + v).strip() if prec[k] != "—" else v
                continue
            row = {k: cells.get(k, "—") for k, _, _ in BANDS}
            row["prix"] = prix
            cible["lignes"].append(row)
    f["tables"] = tables
    return f


def main():
    doc = pymupdf.open(SRC)
    regions, somm = parse_sommaire(doc)
    fiches, hors = [], []
    for pg in range(doc.page_count):
        fi = parse_fiche(pg, doc[pg])
        if fi:
            fiches.append(fi)
        else:
            hors.append(pg + 1)

    merged = []
    for f in fiches:
        if f["suite"] and merged and merged[-1]["numero"] == f["numero"]:
            merged[-1]["tables"] += f["tables"]
            merged[-1]["pages_maquette"].append(f["page_maquette"])
        else:
            f["pages_maquette"] = [f["page_maquette"]]
            merged.append(f)
    for f in merged:
        f.pop("suite", None)
        f.pop("page_maquette", None)
        f["region_sommaire"] = somm.get(f["numero"], {}).get("region")
        f["page_annoncee_sommaire"] = somm.get(f["numero"], {}).get("page_annoncee")

    json.dump({"source": SRC, "regions": regions, "fiches": merged,
               "pages_hors_fiches": hors},
              open(OUT, "w"), ensure_ascii=False, indent=1)

    nl = sum(len(t["lignes"]) for f in merged for t in f["tables"] if t["type"] == "BT")
    nb = sum(len(t["lignes"]) for f in merged for t in f["tables"] if t["type"] == "BIB")
    print(f"fiches={len(merged)}  cuvées={nl}  lignes BIB={nb}  régions={len(regions)}")
    print("régions:", regions)
    print("pages hors fiches:", hors)
    sans_region = [f["numero"] for f in merged if not f["region"]]
    print("fiches sans région:", sans_region or "aucune")
    print("fiches avec BIB:", [f["numero"] for f in merged
                                if any(t["type"] == "BIB" for t in f["tables"])])
    print("fiches à plusieurs tableaux:",
          [(f["numero"], [f"{t['type']}:{len(t['libelles'])}p/{len(t['lignes'])}l"
                          for t in f["tables"]])
           for f in merged if len(f["tables"]) > 1])
    print("fiches sur 2 pages:", [(f["numero"], f["pages_maquette"])
                                  for f in merged if len(f["pages_maquette"]) > 1])
    for f in merged[:1]:
        print(f"\n— n°{f['numero']} {f['nom']} ({f['region']}) p{f['pages_maquette']}")
        print("   labels:", f["labels"])
        print("   conditions:", f["conditions"])
        print("   tableaux:", [(t["type"], t["libelles"], len(t["lignes"]))
                                for t in f["tables"]])


if __name__ == "__main__":
    main()
