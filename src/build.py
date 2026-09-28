"""Construit le catalogue : lit data/catalogue.json, écrit le HTML, produit le PDF.

Aucun prix n'est saisi dans la mise en page : tout vient de la base.
Usage :  python3 src/build.py --fiches 40 3 32 --couverture --pdf build/temoins.pdf
"""
import argparse, json, os, re, sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(RACINE, "src", "templates")

# Une teinte sourde par région, réservée à l'onglet de bord de page et à la puce
# du sommaire. Jamais dans les tableaux, pour ne pas concurrencer le lie-de-vin.
COULEURS_REGION = {
    "Loire": "#7C8F6B", "Alsace": "#3E6150", "Beaujolais": "#9E3B4F",
    "Bourgogne": "#7E2433", "Rhône": "#A4502F", "Sud-Ouest": "#A87332",
    "Bordeaux": "#4F1B3A", "Provence": "#7E6E9E", "Languedoc": "#9A5B34",
    "Champagne": "#B8974F",
}
CLASSE_COULEUR = {"Blanc": "blanc", "Rosé": "rose", "Rouge": "rouge", "Orange": "orange"}


def classe_couleur(c):
    return CLASSE_COULEUR.get(c, "autre")


def entete_prix(t):
    if t["type"] == "BIB":
        return "Prix HT / BIB (€)"
    return "Prix HT / bt (€)"


def prepare_table(t):
    """Aligne le nombre de cellules de prix sur le nombre de paliers.

    Le bloc Prix a toujours la même largeur totale ; il se divise en autant de
    colonnes égales que de paliers. Une cuvée qui n'a qu'un prix dans une grille
    à plusieurs paliers affiche « — » dans les colonnes manquantes : on ne
    recopie pas un prix d'une colonne à l'autre, ce serait inventer une donnée.
    """
    paliers = t["paliers"] or ["Prix unique"]
    n = len(paliers)
    lignes = []
    for l in t["lignes"]:
        prix = list(l["prix"])[:n]
        prix += ["—"] * (n - len(prix))
        lignes.append({**l, "prix_cellules": prix,
                       "classe_couleur": classe_couleur(l["couleur"])})
    return {**t, "paliers": paliers, "lignes": lignes,
            "entete_prix": entete_prix(t), "sous_tableau": t["type"] == "BIB"}


def prepare_fiche(f, folio, ordre_region):
    img = json.load(open(os.path.join(RACINE, "data", "inventaire-images.json")))
    choisies = json.load(open(os.path.join(RACINE, "data", "photos-choisies.json")))
    sel = choisies.get(str(f["numero"]), {})

    def chemin(nom):
        return os.path.join(RACINE, "assets", "photos", nom) if nom else None

    cases = []
    port = f["conditions"]["PORT"]
    port_html = re.sub(r"(Franco)", r'<span class="franco">\1</span>', port)
    cases.append(("PORT", port_html))
    cases.append(("PALIERS", f["conditions"]["PALIERS"]))
    cases.append(("PANACHAGE", f["conditions"]["PANACHAGE"] or "—"))
    cases.append(("PARTICULARITÉS", f["conditions"]["PARTICULARITÉS"] or "—"))

    n_lignes = sum(len(t["lignes"]) for t in f["tables"])
    texte = f["texte"] or ""
    # la maquette répète parfois le sous-titre en tête du texte : on l'ôte
    if f.get("sous_titre") and texte.startswith(f["sous_titre"]):
        texte = texte[len(f["sous_titre"]):].lstrip(" ·—-")

    return {
        **f,
        "texte": texte,
        "dense": n_lignes > 12,
        "folio": folio,
        "suite": False,
        "couleur_region": COULEURS_REGION.get(f["region"], "#6B635B"),
        "onglet_top": 40 + (ordre_region % 10) * 18,
        "cases": cases,
        "tables": [prepare_table(t) for t in f["tables"]],
        "photo_ambiance": chemin(sel.get("ambiance")),
        "photo_bouteilles": chemin(sel.get("bouteilles")),
        "focal_ambiance": sel.get("focal", "center 45%"),
        "logo": chemin(sel.get("logo")),
        "encadre_demande": f["port"]["type"] == "inconnu",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fiches", nargs="*", type=int, default=[])
    ap.add_argument("--couverture", action="store_true")
    ap.add_argument("--html", default="build/temoins.html")
    ap.add_argument("--pdf", default="build/temoins.pdf")
    a = ap.parse_args()

    cat = json.load(open(os.path.join(RACINE, "data", "catalogue.json")))
    env = Environment(loader=FileSystemLoader(TPL),
                      autoescape=select_autoescape(["html"]))
    morceaux = []
    if a.couverture:
        choisies = json.load(open(os.path.join(RACINE, "data", "photos-choisies.json")))
        cat = {**cat, "photo_couverture": os.path.join(RACINE, choisies["_couverture"])}
        morceaux.append(env.get_template("couverture.html").render(cat=cat))

    tpl = env.get_template("fiche.html")
    regions = cat["regions"]
    folio = 6
    for num in a.fiches:
        f = next(x for x in cat["fiches"] if x["numero"] == num)
        ordre = regions.index(f["region"]) if f["region"] in regions else 0
        morceaux.append(tpl.render(f=prepare_fiche(f, folio, ordre)))
        folio += 1

    html = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Agence SCIO — Tarifs cavistes Vendée — septembre 2026</title>
<link rel="stylesheet" href="{os.path.join(RACINE,'src','styles','catalogue.css')}">
</head><body>{''.join(morceaux)}</body></html>"""

    os.makedirs(os.path.join(RACINE, "build"), exist_ok=True)
    chemin_html = os.path.join(RACINE, a.html)
    open(chemin_html, "w").write(html)

    from weasyprint import HTML
    HTML(filename=chemin_html, base_url=RACINE).write_pdf(os.path.join(RACINE, a.pdf))
    print("HTML :", a.html)
    print("PDF  :", a.pdf, f"({os.path.getsize(os.path.join(RACINE,a.pdf))/1024:.0f} Ko)")


if __name__ == "__main__":
    main()
