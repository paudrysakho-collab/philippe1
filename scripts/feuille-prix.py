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

    L, total = [], 0
    w = L.append
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
        w(f'<section><h2><span class="page">page {plan[str(n)]}</span> {html.escape(noms[n])}</h2>')
        for ti, vins in sorted(par_tableau.items()):
            pal = (st["paliers_salon"].get(f"{n}:{ti}") or st["paliers_salon"].get(str(n)) or ["Prix"])
            pal = [p.replace("Prix salon", "Prix") for p in pal]
            w("<table><thead><tr><th>Vin</th><th>Millésime</th><th>Format</th>"
              + "".join(f"<th class=p>{html.escape(x)}</th>" for x in pal) + "</tr></thead><tbody>")
            for v in vins:
                total += len([x for x in v["prix_centimes"] if x is None])
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
    h1{font:400 22pt/1.15 'Young Serif',serif;color:#67067C;margin:0 0 2mm}
    .chapeau{font:400 10pt/1.45 Spectral,serif;margin:0 0 7mm;
      background:#f6f2f8;border-left:2.4pt solid #E1C853;padding:3mm 4mm}
    section{break-inside:avoid;margin:0 0 6mm}
    h2{font:400 13pt/1.2 'Young Serif',serif;color:#67067C;margin:0 0 2mm;
       border-top:1.4pt solid #E1C853;padding-top:2.5mm}
    .page{font:600 8.5pt Archivo,sans-serif;background:#67067C;color:#fff;
      padding:.8mm 2mm;border-radius:1mm;vertical-align:.6mm;margin-right:2mm}
    table{width:100%;border-collapse:collapse;margin:0 0 2mm;font-size:9.5pt}
    thead{display:table-header-group}
    th{font:600 8pt Archivo,sans-serif;text-align:left;padding:1.4mm 2mm;
       border-bottom:1pt solid #67067C}
    th.p{text-align:center;width:24mm}
    td{padding:1.4mm 2mm;border-bottom:.4pt solid #d9d4de;vertical-align:middle}
    td.c{text-align:center;font:400 9pt Archivo,sans-serif;white-space:nowrap}
    td.case{border:.8pt solid #9a93a2;background:#fcfbfd;height:7mm}
    .app{font:400 8pt Archivo,sans-serif;color:#6b6472}
    </style>""")
    H.append("<h1>Catalogue restaurant 2026 — les prix à remplir</h1>")
    H.append(f'<p class=chapeau>Il reste <b>{total} prix</b> à donner. Pour chaque domaine : '
             "sa <b>page dans le catalogue</b>, ses colonnes, et une case vide par prix manquant. "
             "Il suffit d'écrire le prix dans la case. Les prix déjà connus sont rappelés en clair "
             "sur la même ligne.</p>")
    H += L
    H.append("</html>")
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text("\n".join(H), encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {total} prix à remplir")


if __name__ == "__main__":
    main()
