"""Lit l'Excel de l'agence : source de vérité n° 1 des prix (20 domaines).

Structure constatée, régulière sur les 20 feuilles :
  r1  B = nom du domaine, dernière colonne = région
  r2  B = descriptif (porte souvent la certification exacte)
  r3  B = « Sélection Agence SCIO – Tarifs HT <port>, valables jusqu'au … »
  r5  G = marqueur « Tarif »
  r6  B = « Possibilité de panacher », puis libellés de paliers dans les colonnes
          de prix (leur position varie d'une feuille à l'autre)
  r7+ B = appellation, C = cuvée, D = couleur/style, E = millésime,
          F = format, puis les prix
  fin  notes libres (panachage inter-domaines…)

Aucune valeur n'est recalculée : les prix sont repris tels quels, seulement
formatés à deux décimales avec la virgule française.
"""
import json, re
import openpyxl
from openpyxl.utils import get_column_letter

SRC = "sources/Tarifs_Cavistes_SCIO_2026.xlsx"
OUT = "data/prix-excel.json"


def fr(v):
    """Formate un nombre à la française, deux décimales, sans rien arrondir de faux."""
    return f"{round(float(v) + 1e-9, 2):.2f}".replace(".", ",")


def est_prix(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0


def parse(ws):
    rows = {r: {c: ws.cell(r, c).value for c in range(1, ws.max_column + 1)}
            for r in range(1, ws.max_row + 1)}

    def txt(r, c):
        v = rows.get(r, {}).get(c)
        return str(v).strip() if v not in (None, "") else ""

    dom = {"feuille": ws.title, "nom": txt(1, 2), "region": None,
           "descriptif": txt(2, 2), "conditions_source": txt(3, 2),
           "paliers": [], "cuvees": [], "notes": []}
    # région : dernière cellule non vide de la ligne 1
    for c in range(ws.max_column, 2, -1):
        if txt(1, c):
            dom["region"] = txt(1, c)
            break

    # lignes de données : appellation + couleur renseignées + au moins un prix
    data_rows = [r for r in rows
                 if txt(r, 2) and txt(r, 4)
                 and any(est_prix(rows[r].get(c)) for c in range(5, ws.max_column + 1))]
    if not data_rows:
        return dom
    first = min(data_rows)
    prix_cols = sorted({c for r in data_rows for c in range(5, ws.max_column + 1)
                        if est_prix(rows[r].get(c))})

    # libellés de paliers : ligne d'en-tête la plus proche au-dessus des données
    head = None
    for r in range(first - 1, 0, -1):
        if any(isinstance(rows[r].get(c), str) and rows[r][c].strip() for c in prix_cols):
            head = r
            break
    for c in prix_cols:
        lib = txt(head, c) if head else ""
        if not lib:
            # colonne sans libellé = prix de base ; on cherche le marqueur « Tarif »
            for r in range(1, first):
                if txt(r, c).lower().startswith("tarif"):
                    lib = "Tarif"
                    break
        dom["paliers"].append({"colonne": get_column_letter(c), "libelle": lib or "Tarif"})

    for r in data_rows:
        dom["cuvees"].append({
            "ligne_excel": r,
            "appellation": txt(r, 2),
            "cuvee": txt(r, 3),
            "couleur_style": txt(r, 4),
            "millesime": txt(r, 5),
            "format": txt(r, 6),
            "prix": [fr(rows[r][c]) if est_prix(rows[r].get(c)) else "—"
                     for c in prix_cols],
        })
    for r in rows:
        t = txt(r, 2)
        if r > max(data_rows) and t:
            dom["notes"].append(t)
    return dom


def main():
    wb = openpyxl.load_workbook(SRC, data_only=True)
    domaines = [parse(wb[n]) for n in wb.sheetnames]
    json.dump({"source": SRC, "domaines": domaines},
              open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f"{len(domaines)} feuilles, {sum(len(d['cuvees']) for d in domaines)} cuvées\n")
    print(f"{'feuille':<28} {'cuv':>4}  paliers")
    for d in domaines:
        print(f"  {d['feuille']:<26} {len(d['cuvees']):>4}  "
              + " · ".join(p["libelle"] for p in d["paliers"]))
    print("\n--- dégressivités inversées dans l'EXCEL (source de vérité) ---")
    n = 0
    for d in domaines:
        for cu in d["cuvees"]:
            v = [float(p.replace(",", ".")) for p in cu["prix"] if p != "—"]
            if len(v) > 1 and any(v[i + 1] > v[i] for i in range(len(v) - 1)):
                n += 1
                print(f"   {d['feuille']} · {cu['cuvee']} {cu['format']} : "
                      + " → ".join(cu["prix"]))
    print(f"   total : {n} ligne(s)")


if __name__ == "__main__":
    main()
