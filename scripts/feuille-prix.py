#!/usr/bin/env python3
"""Écrit la feuille des prix à remplir du catalogue restaurant : pour chaque domaine, sa page
dans le catalogue, ses colonnes, et une case vide par prix manquant.

    python3 scripts/feuille-prix.py     → build/feuille-prix.html
    npm run feuille-prix                → + epreuves/catalogue-restaurant-prix-a-remplir.pdf
"""
import html
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "build/feuille-prix.html"
POLICES = RACINE / "src/fonts"

# Les lignes que l'agence a déjà cherchées le 10 octobre : le domaine n'a pas de prix
# restaurant pour elles. Elles passent en fin de feuille, pour mémoire.
DEJA_CHERCHE = {
    (3, "Rouge aux lèvres"), (3, "La Perle"), (3, "AOP Muscadet"),
    (3, "IGP Val de Loire Chardonnay"), (3, "IGP Val de Loire Cabernet Franc"),
    (6, "AOC Menetou-Salon Rouge"), (6, "IGP Chenin Blanc"),
    (12, "AOC Pouilly-Vinzelles Blanc"), (23, "N\u00b010 P\u00e9tillant"),
}
DOMAINES_SANS_TARIF = {7, 43}


QUESTIONS = [
    "<b>Domaine des Nugues</b> (page 16) — le domaine a-t-il un tarif restaurant ? La page "
    "scannée ne donne que ses bag-in-box et une « sélection restaurant » (Brouilly, Crémant, "
    "Mâcon-Villages…), aucun de ses crus.",
    "<b>Domaine Haut Marin</b> (page 36) — les onze Armagnacs millésimés (2003 à 1973) n'ont pas "
    "de prix restaurant ; les cinq autres et les trois bag-in-box en ont un.",
    "<b>Domaine Trichon</b> (page 31) — les deux magnums n'ont de prix qu'à partir de 96 cols. "
    "S'il n'y a rien à 36 et 48 cols, faut-il <b>supprimer les deux lignes</b>, comme écrit sur "
    "la page ?",
    "<b>Domaine du Colombier</b> (page 8) — son catalogue C.H.R. n'a été scanné que sur deux "
    "pages, qui s'arrêtent aux blancs de cépage. Il manque la page des rouges, du pétillant et "
    "des bag-in-box.",
    "<b>Divin No Low</b> (page 12) et <b>Mas des Restanques</b> (page 30) — aucun tarif "
    "restaurant n'existe pour eux. On laisse les cases vides, ou on retire les deux fiches du "
    "catalogue restaurant ?",
    "<b>Les offres</b> — elles sont toutes supprimées, comme demandé. À confirmer que c'est bien "
    "valable pour les six catalogues départementaux.",
]


def lire(nom):
    return json.loads((RACINE / nom).read_text(encoding="utf-8"))


def police(nom, fichier, poids=400, style="normal"):
    return (f"@font-face{{font-family:'{nom}';src:url('{(POLICES / fichier).as_uri()}') "
            f"format('woff2');font-weight:{poids};font-style:{style};font-display:block}}")


def main():
    cat = lire("data/catalogue.json")
    noms = {d["numero"]: d["nom"] for d in cat["domaines"]}
    glob = lire("data/catalogue-global-2026.json")
    for d in glob["domaines_ajoutes"]:
        noms[d["numero"]] = d["nom"]
    r = lire("data/catalogue-restaurant-2026.json")
    plan = lire("build/catalogue-restaurant-2026-plan.json")["domaines"]

    vivants, clos_l, total, memoire = [], [], 0, 0
    for n in glob["ordre"]:
        st = next((s for s in r["stands"] if any(v["fiche"] == n for v in s["vins"])), None)
        if not st:
            continue
        # les vins incomplets, rangés par tableau (chaque tableau a ses colonnes)
        par_tableau = {}
        for v in st["vins"]:
            if v["fiche"] != n or not any(x is None for x in v["prix_centimes"]):
                continue
            ti = (v.get("tarif") or {}).get("tableau", 0)
            par_tableau.setdefault(ti, []).append(v)
        if not par_tableau:
            continue
        clos = n in DOMAINES_SANS_TARIF or all(
            (n, v["cuvee"] or v["appellation"]) in DEJA_CHERCHE
            for vs in par_tableau.values() for v in vs)
        bloc = []
        w = bloc.append
        w("<<TITRE>>")
        for ti, vins in sorted(par_tableau.items()):
            pal = (st["paliers_salon"].get(f"{n}:{ti}") or st["paliers_salon"].get(str(n)) or ["Prix"])
            pal = [p.replace("Prix salon", "Prix") for p in pal]
            w("<table><thead><tr><th>Vin</th><th>Millésime</th><th>Format</th>"
              + "".join(f"<th class=p>{html.escape(x)}</th>" for x in pal) + "</tr></thead><tbody>")
            for v in vins:
                manque = len([x for x in v["prix_centimes"] if x is None])
                if clos:
                    memoire += manque
                else:
                    total += manque
                nom = v["cuvee"] or v["appellation"]
                sous = v["appellation"] if v["cuvee"] and v["appellation"] not in v["cuvee"] else ""
                w(f'<tr><td><b>{html.escape(nom)}</b>'
                  + (f'<br><span class=app>{html.escape(sous)}</span>' if sous else "")
                  + f'</td><td class=c>{html.escape(v["millesime"] or "—")}</td>'
                    f'<td class=c>{html.escape(v["contenance"])}</td>'
                  + "".join('<td class="case"></td>' if x is None else
                            f'<td class=c>{x/100:.2f}'.replace(".", ",") + " €</td>"
                            for x in v["prix_centimes"]) + "</tr>")
            w("</tbody></table>")
        w("</section>")
        manque_fiche = sum(len([x for x in v["prix_centimes"] if x is None])
                           for vs in par_tableau.values() for v in vs)
        (clos_l if clos else vivants).append((n, bloc, manque_fiche, clos))

    H = ["<!doctype html><html lang=fr><meta charset=utf-8>",
         "<title>Catalogue restaurant — les prix à remplir</title><style>"]
    for nom, f, p, s in [("Young Serif", "young-serif-latin-ext-400-normal.woff2", 400, "normal"),
                         ("Spectral", "spectral-latin-ext-400-normal.woff2", 400, "normal"),
                         ("Spectral", "spectral-latin-ext-600-normal.woff2", 600, "normal"),
                         ("Archivo", "archivo-latin-ext-400-normal.woff2", 400, "normal"),
                         ("Archivo", "archivo-latin-ext-600-normal.woff2", 600, "normal")]:
        H.append(police(nom, f, p, s))
    H.append("""
    @page{size:210mm 297mm;margin:16mm 14mm}
    body{font:10pt/1.4 Spectral,serif;color:#1d1a21;margin:0}
    h1{font:400 22pt/1.15 'Young Serif',serif;color:#67067C;margin:0 0 1mm}
    .sous{font:400 11pt Archivo,sans-serif;color:#6b6472;margin:0 0 5mm}
    .num{display:inline-block;min-width:7mm;height:7mm;line-height:7mm;text-align:center;
      background:#E1C853;color:#1d1a21;font:600 10pt Archivo,sans-serif;border-radius:3.5mm;
      margin-right:2.5mm;vertical-align:.4mm}
    .cases{float:right;font:600 8.5pt Archivo,sans-serif;color:#6b6472}
    .note{display:block;font:400 8.5pt/1.35 Archivo,sans-serif;color:#6b6472;margin:0 0 2mm}
    ol.questions{font-size:10pt;padding-left:6mm}
    ol.questions li{margin:0 0 3mm}
    .chapeau{font:400 10pt/1.45 Spectral,serif;margin:0 0 7mm;
      background:#f6f2f8;border-left:2.4pt solid #E1C853;padding:3mm 4mm}
    section{break-inside:avoid;margin:0 0 6mm}
    h2{font:400 13pt/1.2 'Young Serif',serif;color:#67067C;margin:0 0 2mm;
       border-top:1.4pt solid #E1C853;padding-top:2.5mm}
    .page{font:600 8.5pt Archivo,sans-serif;background:#67067C;color:#fff;
      padding:.8mm 2mm;border-radius:1mm;vertical-align:.8mm;margin-left:3mm}
    table{width:100%;border-collapse:collapse;margin:0 0 2mm;font-size:9.5pt}
    thead{display:table-header-group}
    th{font:600 8pt Archivo,sans-serif;text-align:left;padding:1.4mm 2mm;
       border-bottom:1pt solid #67067C}
    th.p{text-align:center;width:24mm}
    td{padding:1.4mm 2mm;border-bottom:.4pt solid #d9d4de;vertical-align:middle}
    td.c{text-align:center;font:400 9pt Archivo,sans-serif;white-space:nowrap}
    td.case{border:.8pt solid #9a93a2;background:#fcfbfd;height:7mm}
    .app{font:400 8pt Archivo,sans-serif;color:#6b6472}
    h1.suite{margin-top:10mm;break-before:page}
    section.clos h2{color:#6b6472;border-top-color:#d9d4de}
    section.clos .page{background:#6b6472}
    </style>""")
    H.append("<h1>Catalogue restaurant 2026</h1>")
    H.append("<p class=sous>Ce qui manque pour qu'il soit complet</p>")
    tous = vivants + clos_l
    H.append(f'<p class=chapeau>Le catalogue compte <b>42 domaines</b> et <b>{582} prix</b> déjà '
             f'posés. <b>{len(tous)} domaines</b> ont encore des cases vides, <b>{total + memoire} '
             "en tout. Pour chacun : sa <b>page dans le catalogue</b>, ses colonnes, et une case "
             "vide par prix manquant — il suffit d'écrire le prix dedans. Les prix déjà connus "
             "sont rappelés en clair sur la même ligne.</p>")
    for i, (n, bloc, manque, clos) in enumerate(tous, 1):
        note = (" <span class=note>déjà cherché le 10 octobre : le domaine n'a pas de tarif "
                "restaurant pour ces lignes — à remplir seulement si un prix est retrouvé</span>"
                if clos else "")
        titre = (f'<section{" class=clos" if clos else ""}>'
                 f'<h2><span class="num">{i}</span>{html.escape(noms[n])}'
                 f'<span class="page">page {plan[str(n)]}</span>'
                 f'<span class="cases">{manque} prix</span></h2>{note}')
        H += [x.replace("<<TITRE>>", titre) for x in bloc]
    H.append("<h1 class=suite>Les questions</h1>")
    H.append("<ol class=questions>")
    for q in QUESTIONS:
        H.append(f"<li>{q}</li>")
    H.append("</ol></html>")
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text("\n".join(H), encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {total} prix à remplir")


if __name__ == "__main__":
    main()
