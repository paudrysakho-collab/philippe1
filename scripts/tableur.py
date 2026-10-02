#!/usr/bin/env python3
"""Les tableaux de prix dans un tableur, et retour.

    python3 scripts/tableur.py exporter                 écrit tableur/tarifs-scio-2026.xlsx
    python3 scripts/tableur.py importer FICHIER.xlsx --essai   montre ce qui change, sans rien écrire
    python3 scripts/tableur.py importer FICHIER.xlsx    écrit les changements dans data/fiches/

Le tableur est un outil d'édition, pas une seconde source : data/fiches/ reste la vérité.
On exporte, l'agence modifie (Excel, Google Sheets, LibreOffice), on réimporte, puis
`npm run build` refait les deux PDF et le .pptx d'un coup, contrôles compris.

Dans l'onglet « Tarifs », la colonne A porte une référence par ligne (D12, D12 T1,
D12 T1 L03, D12 NOTE) : c'est elle qui permet de dire ce qui a changé. Une ligne ajoutée
n'a pas de référence ; une ligne supprimée disparaît du tableau. Le nombre de tableaux
d'un domaine, lui, ne change pas par le tableur.
"""
import json, pathlib, re, sys
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

RACINE = pathlib.Path(__file__).resolve().parent.parent
FICHES = RACINE / "data/fiches"
SORTIE = RACINE / "tableur/tarifs-scio-2026.xlsx"

# les couleurs du catalogue (src/styles/systeme.css)
VIOLET, TUFFEAU, CRAIE, ENCRE, SILEX = "67067C", "F2EADA", "FBF8F1", "2A3942", "46606E"
GRIS_REF, GRIS_VIDE, FILET = "8A8F94", "E4E1DA", "D9D2C3"
POLICE = "Arial"
COLONNES = ["Réf.", "Appellation", "Cuvée", "Couleur", "Millésime", "Contenance",
            "Prix 1", "Prix 2", "Prix 3", "Note"]
LARGEURS = [13, 36, 38, 18, 12, 12, 14, 14, 14, 16]
CHAMPS = ["appellation", "cuvee", "couleur", "millesime", "contenance"]
MAX_PALIERS = 3
FORMAT_PRIX = '#,##0.00 "€"'
LIGNE_TITRES = 4


def euros(c):
    return f"{c / 100:,.2f} €".replace(",", " ").replace(".", ",")


def charger_fiches():
    return {int(p.stem): json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(FICHES.glob("*.json"))}


# ——————————————————————————————————————————————————————————————— l'export ———

def exporter(sortie=SORTIE):
    fiches = charger_fiches()
    wb = Workbook()
    ws = wb.active
    ws.title = "Tarifs"
    fin = Side(style="thin", color=FILET)
    f_base = Font(name=POLICE, size=10, color=ENCRE)
    f_ref = Font(name=POLICE, size=8, color=GRIS_REF)

    def remplir(ligne, couleur, de=1, a=len(COLONNES)):
        for c in range(de, a + 1):
            ws.cell(ligne, c).fill = PatternFill("solid", fgColor=couleur)

    ws["A1"] = "Agence SCIO — Tarifs cavistes Vendée (85) 2026 — les tableaux de prix des 40 domaines"
    ws["A1"].font = Font(name=POLICE, size=14, bold=True, color=VIOLET)
    ws["A2"] = ("Cellules blanches et bandeaux violets : à modifier. Colonne A grise : ne pas y "
                "toucher (une ligne ajoutée la laisse vide). Mode d'emploi : onglet suivant.")
    ws["A2"].font = Font(name=POLICE, size=10, italic=True, color=SILEX)
    for c, (titre, larg) in enumerate(zip(COLONNES, LARGEURS), start=1):
        cel = ws.cell(LIGNE_TITRES, c, titre)
        cel.font = Font(name=POLICE, size=10, bold=True, color=ENCRE)
        cel.fill = PatternFill("solid", fgColor=CRAIE)
        cel.border = Border(bottom=Side(style="medium", color=VIOLET))
        cel.alignment = Alignment(horizontal="right" if 7 <= c <= 9 else "left", vertical="center",
                                  indent=1 if c == 10 else 0)
        ws.column_dimensions[get_column_letter(c)].width = larg
    ws.freeze_panes = ws.cell(LIGNE_TITRES + 1, 2)

    sommaire = []
    r = LIGNE_TITRES + 2
    for n, d in fiches.items():
        # le domaine
        ws.cell(r, 1, f"D{n:02d}").font = f_ref
        cel = ws.cell(r, 2, f"{n}  {d['nom']}")
        cel.font = Font(name=POLICE, size=12, bold=True, color=VIOLET)
        reg = ws.cell(r, 10, d["region"].upper())
        reg.font = Font(name=POLICE, size=8, bold=True, color=SILEX)
        reg.alignment = Alignment(horizontal="right")
        remplir(r, TUFFEAU, 2)
        ws.row_dimensions[r].height = 22
        sommaire.append((n, d["nom"], d["region"], len(d["tableaux"]), r))
        r += 1
        for ti, t in enumerate(d["tableaux"], start=1):
            # le bandeau du tableau : son intitulé et ses paliers
            ws.cell(r, 1, f"D{n:02d} T{ti}").font = f_ref
            remplir(r, VIOLET, 2)
            cel = ws.cell(r, 2, t["intitule"])
            cel.font = Font(name=POLICE, size=10, bold=True, color="FFFFFF")
            cel.alignment = Alignment(vertical="center")
            if t.get("famille"):
                fam = ws.cell(r, 3, t["famille"].upper())
                fam.font = Font(name=POLICE, size=8, bold=True, color=TUFFEAU)
            for pi in range(MAX_PALIERS):
                cel = ws.cell(r, 7 + pi, t["paliers"][pi] if pi < len(t["paliers"]) else None)
                cel.font = Font(name=POLICE, size=9, bold=True, color="FFFFFF")
                cel.alignment = Alignment(horizontal="right", wrap_text=True, vertical="center")
            ws.row_dimensions[r].height = 26
            r += 1
            for li, l in enumerate(t["lignes"], start=1):
                ws.cell(r, 1, f"D{n:02d} T{ti} L{li:02d}").font = f_ref
                for c, champ in enumerate(CHAMPS, start=2):
                    cel = ws.cell(r, c, l.get(champ))
                    cel.font = f_base
                    cel.number_format = "@"          # 2023, 75 cl, 2022/2023 : du texte
                for pi in range(MAX_PALIERS):
                    cel = ws.cell(r, 7 + pi)
                    if pi < len(t["paliers"]):
                        cel.value = l["prix_centimes"][pi] / 100
                        cel.number_format = FORMAT_PRIX
                        cel.font = Font(name=POLICE, size=10, bold=True, color=ENCRE)
                    else:
                        cel.fill = PatternFill("solid", fgColor=GRIS_VIDE)
                note = ws.cell(r, 10, l.get("note"))
                note.font = f_base
                note.alignment = Alignment(indent=1)
                for c in range(1, len(COLONNES) + 1):
                    ws.cell(r, c).border = Border(bottom=fin)
                r += 1
        # la note de prix du domaine
        ws.cell(r, 1, f"D{n:02d} NOTE").font = f_ref
        ws.cell(r, 2, "Note de prix").font = Font(name=POLICE, size=9, italic=True, color=SILEX)
        cel = ws.cell(r, 3, d.get("note_prix"))
        cel.font = Font(name=POLICE, size=9, italic=True, color=ENCRE)
        r += 2

    # le sommaire : un clic mène au domaine
    so = wb.create_sheet("Sommaire", 0)
    so["A1"] = "Sommaire — cliquer sur un domaine pour y aller"
    so["A1"].font = Font(name=POLICE, size=14, bold=True, color=VIOLET)
    for c, (titre, larg) in enumerate(zip(["N°", "Domaine", "Région", "Tableaux", "Ligne"],
                                          [6, 44, 14, 10, 8]), start=1):
        cel = so.cell(3, c, titre)
        cel.font = Font(name=POLICE, size=10, bold=True, color=ENCRE)
        cel.fill = PatternFill("solid", fgColor=CRAIE)
        cel.border = Border(bottom=Side(style="medium", color=VIOLET))
        so.column_dimensions[get_column_letter(c)].width = larg
    for i, (n, nom, region, nt, ligne) in enumerate(sommaire, start=4):
        so.cell(i, 1, n).font = Font(name=POLICE, size=10, color=ENCRE)
        cel = so.cell(i, 2, nom)
        cel.hyperlink = f"#Tarifs!B{ligne}"
        cel.font = Font(name=POLICE, size=10, color=VIOLET, underline="single")
        so.cell(i, 3, region).font = Font(name=POLICE, size=10, color=SILEX)
        so.cell(i, 4, nt).font = Font(name=POLICE, size=10, color=ENCRE)
        so.cell(i, 5, ligne).font = Font(name=POLICE, size=9, color=GRIS_REF)
    so.freeze_panes = "A4"

    # le mode d'emploi
    me = wb.create_sheet("Mode d'emploi")
    me.column_dimensions["A"].width = 110
    textes = [
        ("Mode d'emploi", "titre"),
        ("", None),
        ("Le principe", "inter"),
        ("1. Modifier les prix, les millésimes, les cuvées… directement dans l'onglet « Tarifs ».", None),
        ("2. Envoyer le fichier modifié (en .xlsx). Depuis Google Sheets : Fichier > Télécharger > Microsoft Excel.", None),
        ("3. Claude relit le fichier et montre chaque changement (ancien prix → nouveau prix) avant de l'appliquer.", None),
        ("4. Les deux PDF et le .pptx pour Canva sont refaits d'un coup, avec tous les contrôles (aucun prix perdu).", None),
        ("", None),
        ("Ce qu'on peut modifier", "inter"),
        ("• Les cellules blanches : appellation, cuvée, couleur, millésime, contenance, prix, note (l'astérisque, par exemple).", None),
        ("• Le bandeau violet de chaque tableau : son intitulé (colonne B) et les intitulés de paliers (colonnes G à I).", None),
        ("• La ligne « Note de prix » de chaque domaine (colonne C) : H.T., franco, départ chai…", None),
        ("", None),
        ("Ce qu'on ne touche pas", "inter"),
        ("• La colonne A, grise (D12, D12 T1, D12 T1 L03…) : c'est elle qui permet de retrouver chaque ligne.", None),
        ("• Les lignes de titre de domaine (fond beige).", None),
        ("• Le nombre de tableaux d'un domaine : pour en ajouter ou en retirer un, le demander.", None),
        ("", None),
        ("Les prix", "inter"),
        ("• Taper le prix seul : 14,75 — le symbole € s'ajoute tout seul. Deux décimales au plus.", None),
        ("• Un tableau à un seul palier n'a qu'une colonne de prix ; les cases grisées restent vides.", None),
        ("• Ajouter un palier : écrire son intitulé dans le bandeau violet, puis remplir cette colonne pour toutes les lignes du tableau.", None),
        ("", None),
        ("Ajouter ou retirer un vin", "inter"),
        ("• Ajouter : insérer une ligne à l'intérieur du tableau (clic droit > Insérer une ligne), laisser la colonne A vide, remplir le reste.", None),
        ("• Retirer : supprimer la ligne entière.", None),
        ("", None),
        ("Exemple d'une ligne ajoutée (à ne pas recopier telle quelle) :", "inter"),
    ]
    for i, (txt, style) in enumerate(textes, start=1):
        cel = me.cell(i, 1, txt)
        cel.alignment = Alignment(wrap_text=True, vertical="top")
        if style == "titre":
            cel.font = Font(name=POLICE, size=14, bold=True, color=VIOLET)
        elif style == "inter":
            cel.font = Font(name=POLICE, size=11, bold=True, color=ENCRE)
        else:
            cel.font = Font(name=POLICE, size=10, color=ENCRE)
    ex = len(textes) + 1
    exemple = ["(vide)", "AOP Muscadet Sèvre et Maine sur lie", "Nouvelle cuvée", "Blanc", "2025",
               "75 cl", 6.90, 6.50, 6.20, ""]
    me2 = me  # l'exemple prend la largeur de l'onglet Tarifs, sous le texte
    for c, (v, larg) in enumerate(zip(exemple, LARGEURS), start=1):
        cel = me2.cell(ex + 1, c, v)
        cel.font = Font(name=POLICE, size=10, color=GRIS_REF if c == 1 else ENCRE, italic=(c == 1))
        if isinstance(v, float):
            cel.number_format = FORMAT_PRIX
        cel.border = Border(bottom=Side(style="thin", color=FILET), top=Side(style="thin", color=FILET))
        t = me2.cell(ex, c, COLONNES[c - 1])
        t.font = Font(name=POLICE, size=9, bold=True, color=SILEX)
    for c, larg in enumerate(LARGEURS[1:], start=2):
        me.column_dimensions[get_column_letter(c)].width = larg

    for feuille in (ws, so, me):
        feuille.sheet_view.showGridLines = False
        feuille.page_setup.orientation = "landscape"
        feuille.page_setup.fitToWidth = 1
        feuille.page_setup.fitToHeight = 0
        feuille.sheet_properties.pageSetUpPr.fitToPage = True
    wb.active = 1
    sortie.parent.mkdir(parents=True, exist_ok=True)
    wb.save(sortie)
    nl = sum(len(t["lignes"]) for d in fiches.values() for t in d["tableaux"])
    nt = sum(len(d["tableaux"]) for d in fiches.values())
    print(f"✓ {sortie.relative_to(RACINE)} — {len(fiches)} domaines, {nt} tableaux, {nl} lignes")


# ——————————————————————————————————————————————————————————————— l'import ———

class Refus(Exception):
    pass


def texte(v):
    if v is None:
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    v = str(v).strip()
    return v or None


def prix(v, ou):
    """Un prix tel que le tableur le rend : un nombre (14.75) ou un texte (« 14,75 € »)."""
    if isinstance(v, (int, float)):
        x = float(v)
    else:
        s = str(v).replace("€", "").replace(" ", "").replace("\xa0", "").replace(" ", "")
        s = s.replace(",", ".")
        try:
            x = float(s)
        except ValueError:
            raise Refus(f"{ou} : « {v} » n'est pas un prix")
    c = round(x * 100)
    if abs(x * 100 - c) > 1e-6:
        raise Refus(f"{ou} : {v} a plus de deux décimales")
    if c <= 0:
        raise Refus(f"{ou} : un prix doit être positif ({v})")
    return c


def lire(fichier):
    wb = load_workbook(fichier, data_only=True)
    if "Tarifs" not in wb.sheetnames:
        raise Refus("le fichier n'a pas d'onglet « Tarifs »")
    ws = wb["Tarifs"]
    lu, dom, tab = {}, None, None
    for r in range(LIGNE_TITRES + 1, ws.max_row + 1):
        vals = [ws.cell(r, c).value for c in range(1, len(COLONNES) + 1)]
        ref = texte(vals[0])
        if ref is None and all(texte(v) is None for v in vals[1:]):
            continue
        ou = f"ligne {r}"
        if ref and re.fullmatch(r"D\d{2}", ref):
            dom = int(ref[1:]); tab = None
            lu[dom] = {"tableaux": [], "note_prix": None}
        elif ref and re.fullmatch(r"D\d{2} T\d+", ref):
            n, ti = int(ref[1:3]), int(ref.split("T")[1])
            if n != dom:
                raise Refus(f"{ou} : le tableau {ref} est rangé sous un autre domaine")
            paliers = [texte(v) for v in vals[6:9]]
            while paliers and paliers[-1] is None:
                paliers.pop()
            if None in paliers:
                raise Refus(f"{ou} : un palier vide entre deux paliers remplis")
            tab = {"ref": ref, "intitule": texte(vals[1]), "paliers": paliers, "lignes": []}
            lu[dom]["tableaux"].append(tab)
        elif ref and re.fullmatch(r"D\d{2} NOTE", ref):
            if int(ref[1:3]) != dom:
                raise Refus(f"{ou} : la note de prix {ref} est rangée sous un autre domaine")
            lu[dom]["note_prix"] = texte(vals[2]) or texte(vals[1] if texte(vals[1]) != "Note de prix" else None)
            tab = None
        elif ref is None or re.fullmatch(r"D\d{2} T\d+ L\d+", ref):
            if tab is None:
                raise Refus(f"{ou} : une ligne de vin hors de tout tableau")
            nb = len(tab["paliers"])
            les_prix = [vals[6 + i] for i in range(MAX_PALIERS)]
            remplis = [i for i, v in enumerate(les_prix) if texte(v) is not None]
            if remplis != list(range(nb)):
                raise Refus(f"{ou} : {len(remplis)} prix pour {nb} palier(s) dans le tableau {tab['ref']}")
            ligne = {champ: texte(vals[1 + i]) for i, champ in enumerate(CHAMPS)}
            ligne["prix_centimes"] = [prix(les_prix[i], ou) for i in range(nb)]
            ligne["note"] = texte(vals[9])
            ligne["_ref"] = ref
            ligne["_ou"] = ou
            tab["lignes"].append(ligne)
        else:
            raise Refus(f"{ou} : référence inconnue en colonne A : « {ref} »")
    return lu


def decrire(l):
    bouts = [l.get("appellation"), l.get("cuvee"), l.get("couleur"), l.get("millesime"),
             l.get("contenance")]
    return " ".join(b for b in bouts if b)


def ecrire_fiche(chemin, d):
    """Réécrit la fiche en ne touchant qu'à ses tableaux et à sa note de prix, dans le style
    du fichier : les autres lignes (textes, labels…) restent octet pour octet."""
    ancien = chemin.read_text(encoding="utf-8")
    if ancien == json.dumps(json.loads(ancien), ensure_ascii=False, indent=2) + "\n":
        neuf = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    else:
        val = lambda v: json.dumps(v, ensure_ascii=False)

        def bloc(t, retrait):
            r = " " * retrait
            l1 = [f'{r}  "{k}": {val(v)}' for k, v in t.items() if k != "lignes"]
            lignes = ",\n".join(f"{r}    {{ " + ", ".join(f'"{k}": {val(v)}' for k, v in l.items()) + " }"
                                for l in t["lignes"])
            return ",\n".join(l1) + f',\n{r}  "lignes": [\n' + lignes + f"\n{r}  ]"

        if '"tableaux": [{' in ancien and len(d["tableaux"]) == 1:
            # le style d'une fiche à un seul tableau : « [{ … }] »
            tableaux = '  "tableaux": [{\n' + bloc(d["tableaux"][0], 2) + "\n  }]"
        else:
            tableaux = ('  "tableaux": [\n'
                        + ",\n".join("    {\n" + bloc(t, 4) + "\n    }" for t in d["tableaux"])
                        + "\n  ]")
        debut = ancien.index('  "tableaux": [')
        fin = ancien.rindex("]") + 1
        neuf = ancien[:debut] + tableaux + ancien[fin:]
        lignes = neuf.split("\n")
        for i, l in enumerate(lignes):
            if l.strip().startswith('"note_prix":'):
                virgule = "," if l.rstrip().endswith(",") else ""
                lignes[i] = l[:len(l) - len(l.lstrip())] + f'"note_prix": {val(d["note_prix"])}{virgule}'
        neuf = "\n".join(lignes)
    if json.loads(neuf) != d:
        raise Refus(f"{chemin.name} : la réécriture ne redonne pas les données attendues")
    chemin.write_text(neuf, encoding="utf-8")


def importer(fichier, essai):
    fiches = charger_fiches()
    lu = lire(fichier)
    manquants = sorted(set(fiches) - set(lu))
    if manquants:
        raise Refus(f"domaines absents du tableur : {', '.join(map(str, manquants))}")
    changements, a_ecrire = [], {}
    for n, d in fiches.items():
        neuf = lu[n]
        if len(neuf["tableaux"]) != len(d["tableaux"]):
            raise Refus(f"n°{n} : {len(neuf['tableaux'])} tableau(x) dans le tableur, "
                        f"{len(d['tableaux'])} dans le catalogue — ce changement-là se demande")
        dn = json.loads(json.dumps(d))
        notes = []
        if (neuf["note_prix"] or "") != (d.get("note_prix") or ""):
            notes.append(f"note de prix : « {d.get('note_prix')} » → « {neuf['note_prix']} »")
            dn["note_prix"] = neuf["note_prix"]
        for ti, (t, tn) in enumerate(zip(d["tableaux"], neuf["tableaux"]), start=1):
            ref_t = f"D{n:02d} T{ti}"
            if tn["ref"] != ref_t:
                raise Refus(f"n°{n} : tableaux dans le désordre ({tn['ref']} à la place de {ref_t})")
            if tn["intitule"] != t["intitule"]:
                notes.append(f"tableau {ti}, intitulé : « {t['intitule']} » → « {tn['intitule']} »")
            if tn["paliers"] != t["paliers"]:
                notes.append(f"tableau {ti}, paliers : {t['paliers']} → {tn['paliers']}")
            anciennes = {f"{ref_t} L{li:02d}": l for li, l in enumerate(t["lignes"], start=1)}
            vues = set()
            nouvelles = []
            for l in tn["lignes"]:
                ref, ou = l.pop("_ref"), l.pop("_ou")
                ordre = list(anciennes[ref]) if ref in anciennes else list(t["lignes"][0]) if t["lignes"] else CHAMPS + ["prix_centimes", "note"]
                propre = {k: l.get(k) for k in ordre}
                nouvelles.append(propre)
                if ref is None:
                    notes.append(f"tableau {ti}, ajout ({ou}) : {decrire(propre)} — "
                                 + " / ".join(euros(c) for c in propre["prix_centimes"]))
                    continue
                if ref not in anciennes or ref in vues:
                    raise Refus(f"{ou} : la référence {ref} n'appartient pas à ce tableau, ou revient deux fois")
                vues.add(ref)
                a = anciennes[ref]
                for k in ordre:
                    if a.get(k) != propre.get(k):
                        if k == "prix_centimes":
                            notes.append(f"{decrire(propre)} : " + " / ".join(euros(c) for c in a[k])
                                         + " → " + " / ".join(euros(c) for c in propre[k]))
                        else:
                            notes.append(f"{decrire(a)} : {k} « {a.get(k)} » → « {propre.get(k)} »")
            for ref, a in anciennes.items():
                if ref not in vues:
                    notes.append(f"tableau {ti}, retrait : {decrire(a)} — "
                                 + " / ".join(euros(c) for c in a["prix_centimes"]))
            dn["tableaux"][ti - 1]["intitule"] = tn["intitule"]
            dn["tableaux"][ti - 1]["paliers"] = tn["paliers"]
            dn["tableaux"][ti - 1]["lignes"] = nouvelles
        if notes:
            changements.append((n, d["nom"], notes))
            a_ecrire[n] = dn
    if not changements:
        print("Aucun changement : le tableur dit exactement ce que disent les données.")
        return
    total = sum(len(x[2]) for x in changements)
    print(f"{total} changement(s) dans {len(changements)} domaine(s) :\n")
    for n, nom, notes in changements:
        print(f"n°{n} {nom}")
        for m in notes:
            print(f"   • {m}")
        print()
    if essai:
        print("(essai : rien n'a été écrit)")
        return
    for n, dn in a_ecrire.items():
        ecrire_fiche(FICHES / f"{n:02d}.json", dn)
    print(f"✓ {len(a_ecrire)} fiche(s) réécrite(s) dans data/fiches/. "
          "Prochaine étape : npm run build (refait et contrôle les PDF et le .pptx), "
          "puis npm run tableur (remet le tableur à jour).")


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if args[:1] == ["exporter"]:
            exporter(pathlib.Path(args[1]) if len(args) > 1 else SORTIE)
        elif args[:1] == ["importer"] and len(args) >= 2:
            importer(pathlib.Path(args[1]), "--essai" in args)
        else:
            print(__doc__)
            sys.exit(2)
    except Refus as e:
        print(f"REFUSÉ — {e}")
        sys.exit(1)
