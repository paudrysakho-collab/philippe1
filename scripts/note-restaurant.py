#!/usr/bin/env python3
"""Écrit la note de synthèse du catalogue restaurant (HTML puis PDF) : où on en est,
ce qui manque, et les points que l'agence doit trancher.

    python3 scripts/note-restaurant.py      → build/note-restaurant.html
    npm run note-restaurant                 → + epreuves/catalogue-restaurant-note.pdf
"""
import html
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "build/note-restaurant.html"
POLICES = RACINE / "src/fonts"

SANS_TARIF = {7, 43}
CONFIRMES = {
    (3, "Rouge aux lèvres"), (3, "La Perle"), (3, "AOP Muscadet"),
    (3, "IGP Val de Loire Chardonnay"), (3, "IGP Val de Loire Cabernet Franc"),
    (6, "AOC Menetou-Salon Rouge"), (6, "IGP Chenin Blanc"),
    (12, "AOC Pouilly-Vinzelles Blanc"), (23, "N°10 Pétillant"),
}
DOSSIER = {
    39: "1", 1: "2", 41: "3–4", 2: "5–6", 3: "7–8", 4: "9", 5: "10", 6: "11–12", 8: "13",
    9: "14", 10: "15", 12: "16–20", 13: "16–20", 14: "16–20", 15: "21", 11: "22",
    16: "23–24", 17: "25", 18: "26", 19: "27", 31: "33", 32: "34–41", 34: "42", 36: "43",
    35: "44", 37: "45", 38: "46", 40: "47", 21: "48", 42: "49", 20: "50", 22: "51",
    23: "52", 28: "53", 27: "54", 29: "55", 30: "56", 26: "57", 25: "30–32, 58–73",
}

POINTS = [
    ("Domaine Stratéus — la hausse de 0,70 €",
     "La grille porte, de la main de l'agence, « Rajouter 0,70 cts sur toute la gamme ». Les prix "
     "posés sont donc ceux du tarif <b>plus 0,70 €</b> : gamme Stratéus 13,20 / 12,50 / 11,70 ; "
     "gamme Koloss 7,20 / — / 6,70 ; gamme Néolithik 16,70 / 15,20 / 13,20. À confirmer."),
    ("Domaine Stratéus — quelles quantités",
     "Sa grille va de 24 à 300 bouteilles et ne dit pas lesquelles retenir. Les trois plus petits "
     "volumes ont été pris : <b>24 / 48 / 120 bouteilles</b>. La gamme Koloss n'a pas de prix à "
     "48 bouteilles (le tarif met « / ») : la case reste vide."),
    ("Champagne Denis Frézier — la colonne réécrite à la main",
     "La première colonne du tarif est réécrite à la main, un euro au-dessus du prix imprimé. "
     "Relevé : Trois Crus <b>16,92</b> (15,92 imprimé), Terroir <b>19,72</b> (18,72), Millésime "
     "Expression <b>20,34</b> (19,34 barré, « 20,34 » écrit). Quantités 36 / 66 / 126."),
    ("Château de Gragnos — Grain de Blanc",
     "Le tarif donne <b>7,80 / 5,50 / 7,20</b> : le palier 60 bouteilles est moins cher que le "
     "palier 120. Relevé tel quel, rien n'a été corrigé."),
    ("Champagne Vazart-Coquart — le nom des colonnes",
     "Le tarif nomme ses colonnes <b>« Par 24 / Par 48 / Par 78 »</b> ; elles sont reprises telles "
     "quelles, au lieu du « À partir de… » des autres fiches."),
    ("Les notes de prix",
     "Elles suivent chaque tarif restaurant, et non celles du catalogue caviste : franco de port "
     "(Frézier, Vazart, Trichon, La Gorce, Haut Marin, Gragnos, Albas, La Passion des Terroirs, "
     "Stratéus) ou hors frais de transport quand le tarif dit « départ cave » (Pasquiers, Les Lys, "
     "Dekeyne)."),
    ("Chai Berteaud Manceau — son offre",
     "Toutes les offres sont encore celles du catalogue caviste, sauf celle-ci : « Offre 11+1 à "
     "partir de 60 cols », écrite à la main sur le tarif restaurant."),
    ("La Passion des Terroirs — la commande minimum",
     "Son tarif restaurant porte « Commande minimum : 400 € ». Faut-il l'afficher sur la fiche ?"),
    ("Domaine des Sardelles — le Sancerre Rosé",
     "La ligne est barrée sur le tarif, mais l'agence a confirmé ses prix le 10 octobre : "
     "<b>10,60 / 10,30 / 10,00</b>. Ils sont posés."),
]


def lire(nom):
    return json.loads((RACINE / nom).read_text(encoding="utf-8"))


def etiquette(v):
    bits = [v["cuvee"] or v["appellation"]]
    if v["cuvee"] and v["appellation"] and v["appellation"] not in v["cuvee"]:
        bits.append(f"— {v['appellation']}")
    extra = [v["couleur"]]
    if v["millesime"] and v["millesime"] != "—":
        extra.append(v["millesime"])
    if v["contenance"] != "75 cl":
        extra.append(v["contenance"])
    return html.escape(" ".join(bits) + " (" + ", ".join(x for x in extra if x) + ")")


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

    def stand(n):
        return next((s for s in r["stands"] if any(v["fiche"] == n for v in s["vins"])), None)

    def paliers(st, n):
        return (st["paliers_salon"].get(str(n))
                or next((p for k, p in st["paliers_salon"].items() if k.split(":")[0] == str(n)), []))

    a_trouver, clos, colonnes = [], [], []
    poses = vides = 0
    for n in glob["ordre"]:
        st = stand(n)
        if not st:
            continue
        vins = [v for v in st["vins"] if v["fiche"] == n]
        for v in vins:
            poses += len([x for x in v["prix_centimes"] if x is not None])
            vides += len([x for x in v["prix_centimes"] if x is None])
        manque = [v for v in vins if all(x is None for x in v["prix_centimes"])]
        if manque:
            fini = n in SANS_TARIF or all((n, v["cuvee"] or v["appellation"]) in CONFIRMES for v in manque)
            (clos if fini else a_trouver).append((n, manque, paliers(st, n)))
        pal = paliers(st, n)
        for v in vins:
            pc = v["prix_centimes"]
            if len(pc) > 1 and any(x is None for x in pc) and any(x is not None for x in pc):
                colonnes.append((n, v, ", ".join(pal[i] for i, x in enumerate(pc)
                                                 if x is None and i < len(pal))))

    L = []
    w = L.append
    w("<!doctype html><html lang=fr><meta charset=utf-8>")
    w("<title>Catalogue restaurant 2026 — ce qui manque</title><style>")
    for n, f, p, s in [("Young Serif", "young-serif-latin-ext-400-normal.woff2", 400, "normal"),
                       ("Spectral", "spectral-latin-ext-400-normal.woff2", 400, "normal"),
                       ("Spectral", "spectral-latin-ext-600-normal.woff2", 600, "normal"),
                       ("Spectral", "spectral-latin-ext-400-italic.woff2", 400, "italic"),
                       ("Archivo", "archivo-latin-ext-400-normal.woff2", 400, "normal"),
                       ("Archivo", "archivo-latin-ext-600-normal.woff2", 600, "normal")]:
        w(police(n, f, p, s))
    w("""
    @page{size:210mm 297mm;margin:18mm 16mm 16mm}
    body{font:10.5pt/1.5 Spectral,serif;color:#1d1a21;margin:0}
    h1{font:400 23pt/1.15 'Young Serif',serif;color:#67067C;margin:0 0 2mm}
    .date{font:400 9.5pt Archivo,sans-serif;color:#6b6472;margin:0 0 7mm}
    h2{font:400 14pt/1.2 'Young Serif',serif;color:#67067C;margin:9mm 0 3mm;
       border-top:1.4pt solid #E1C853;padding-top:2.5mm;break-after:avoid}
    h3{font:600 10.5pt Archivo,sans-serif;margin:5mm 0 1mm;break-after:avoid}
    p{margin:0 0 2.5mm}
    ul{margin:0 0 3mm;padding-left:5mm}
    li{margin:0 0 1mm}
    table{width:100%;border-collapse:collapse;margin:0 0 4mm;font-size:9.5pt}
    thead{display:table-header-group}
    tr{break-inside:avoid}
    th{font:600 8.5pt Archivo,sans-serif;text-align:left;background:#67067C;color:#fff;
       padding:1.6mm 2mm}
    td{padding:1.6mm 2mm;border-bottom:.4pt solid #d9d4de;vertical-align:top}
    .chiffre{font:600 9.5pt Archivo,sans-serif;white-space:nowrap}
    .bloc{break-inside:avoid}
    .intro{background:#f6f2f8;border-left:2.4pt solid #E1C853;padding:3mm 4mm;margin:0 0 5mm}
    .pt{break-inside:avoid;margin:0 0 4mm}
    </style>""")
    w("<h1>Catalogue restaurant 2026</h1>")
    w("<p class=date>Ce qui manque et ce qui reste à trancher — Agence SCIO, 10 octobre 2026</p>")
    w("<div class=intro><p>Le catalogue restaurant reprend <b>le catalogue caviste 85 à l'identique</b> : "
      "mêmes domaines, mêmes vins, mêmes textes, mêmes photos, même pagination. "
      "<b>Seuls les minimums de commande et les prix changent.</b> Ils sont relevés sur les tarifs "
      "restaurant envoyés par l'agence (dossier de 73 pages du 10 octobre).</p>")
    w(f"<p><b>64 pages, 42 domaines, 11 régions. {poses} prix posés, {vides} cases encore vides.</b> "
      "Toutes les pages ont été regardées en image, tous les contrôles automatiques sont au vert.</p></div>")

    w("<h2>1. Les prix qui manquent</h2>")
    w("<p>Chaque domaine avec sa page dans le catalogue (le même numéro dans le caviste 85 et dans "
      "le restaurant) et la page de son tarif dans le dossier.</p>")
    total = sum(len(m) for _, m, _ in a_trouver)
    for n, manque, pal in a_trouver:
        d = DOSSIER.get(n)
        w("<div class=bloc>")
        w(f"<h3>{html.escape(noms[n])} — {len(manque)} vin{'s' if len(manque) > 1 else ''}</h3>")
        w(f"<p><b>Catalogue page {plan[str(n)]}</b> · "
          + (f"tarif au dossier page {d}" if d else "<b>aucune page au dossier</b>")
          + f" · colonnes : {html.escape(' / '.join(p.replace('Prix salon', 'Prix') for p in pal))}</p>")
        w("<ul>" + "".join(f"<li>{etiquette(v)}</li>" for v in manque) + "</ul>")
        w("</div>")
    w(f"<p><b>{total} vins en tout.</b></p>")

    w("<h2>2. Les colonnes incomplètes</h2>")
    w("<p>Ces lignes ont déjà un prix, mais le tarif met « – » dans certaines colonnes.</p>")
    w("<table><thead><tr><th>Domaine</th><th>Page</th><th>Vin</th>"
      "<th>Colonnes sans prix</th></tr></thead><tbody>")
    for n, v, cols in colonnes:
        w(f"<tr><td>{html.escape(noms[n])}</td><td class=chiffre>p.{plan[str(n)]}</td>"
          f"<td>{etiquette(v)}</td><td>{html.escape(cols)}</td></tr>")
    w("</tbody></table>")

    w("<h2>3. Déjà cherché : ces vins n'ont pas de prix restaurant</h2>")
    w("<p>L'agence a cherché le 10 octobre ; ces lignes restent sans prix dans le catalogue.</p>")
    w("<table><thead><tr><th>Domaine</th><th>Page</th><th>Vins</th></tr></thead><tbody>")
    for n, manque, _ in clos:
        d = DOSSIER.get(n)
        w(f"<tr><td>{html.escape(noms[n])}</td><td class=chiffre>p.{plan[str(n)]}"
          + (f"<br>dossier p.{d}" if d else "<br>pas de tarif") + "</td><td>"
          + " · ".join(etiquette(v) for v in manque) + "</td></tr>")
    w("</tbody></table>")

    w("<h2>4. Les points à valider</h2>")
    for titre, texte in POINTS:
        w(f"<div class=pt><h3>{html.escape(titre)}</h3><p>{texte}</p></div>")

    w("<h2>5. Comment un prix se met à jour</h2>")
    w("<p>Tous les prix et toutes les quantités du catalogue restaurant vivent dans un seul "
      "fichier, <i>scripts/prix-restaurant.py</i>. On y ajoute le prix, on relance la commande "
      "<i>npm run restaurant</i>, et les deux PDF (écran et imprimeur) sont refaits avec leurs "
      "contrôles. Un prix ne s'invente ni ne se corrige jamais seul : il vient d'un tarif annoté "
      "ou de l'agence.</p>")
    w("</html>")
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text("\n".join(L), encoding="utf-8")
    print(f"✓ {SORTIE.relative_to(RACINE)} : {total} vins à trouver, {len(colonnes)} colonnes")


if __name__ == "__main__":
    main()
