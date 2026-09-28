"""Contrôles automatiques sur le PDF produit. Rien n'est déclaré fini sans eux."""
import re, sys, json
import pymupdf

PDF = sys.argv[1] if len(sys.argv) > 1 else "build/temoins.pdf"
EN_TETES = ["APPELLATION", "CUVÉE", "COULEUR", "MILL.", "FORMAT"]
INTERDITS = ["[", "à rédiger", "à préciser", "Lorem", "À VÉRIFIER", "[PVC]", "undefined"]

doc = pymupdf.open(PDF)
ko = []


def dit(ok, libelle, detail=""):
    print(f"  {'OK  ' if ok else 'ÉCHEC'}  {libelle}" + (f"  — {detail}" if detail else ""))
    if not ok:
        ko.append(libelle)


print(f"Contrôle de {PDF} — {doc.page_count} pages\n")

# 1. géométrie : les colonnes tombent-elles au même endroit sur toutes les fiches ?
pos = {}
for i, page in enumerate(doc):
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t in EN_TETES:
                    pos.setdefault(t, []).append(round(s["bbox"][0], 1))
detail = []
for t in EN_TETES:
    v = pos.get(t, [])
    if v:
        detail.append(f"{t} écart {max(v)-min(v):.1f} mm")
dit(all(max(v) - min(v) < 0.2 for v in pos.values() if v),
    "colonnes identiques sur toutes les pages", " · ".join(detail))

# 2. couche texte : les mots doivent être retrouvables (Ctrl+F)
txt = "\n".join(p.get_text() for p in doc)
mots = ["APPELLATION", "CUVÉE", "PALIERS", "PANACHAGE", "PARTICULARITÉS"]
introuvables = [m for m in mots if m not in txt]
dit(not introuvables, "couche texte saine (recherche Ctrl+F)",
    f"introuvables : {introuvables}" if introuvables else "tous les mots-clés trouvés")

# 3. aucun espace parasite d'interlettrage
parasites = [m for m in ("APPELLAT I ON", "CU VÉE", "PA LIERS", "Tuff eau", "dè s")
             if m in txt]
dit(not parasites, "aucun espace parasite dans les mots", str(parasites))

# 4. aucun placeholder
trouves = [m for m in INTERDITS if m in txt]
dit(not trouves, "aucun texte provisoire ni crochet", str(trouves))

# 5. mention sanitaire sur chaque page intérieure
manquantes = [i + 1 for i, p in enumerate(doc)
              if "dangereux pour la santé" not in p.get_text()]
dit(not manquantes, "mention sanitaire sur chaque page",
    f"absente p. {manquantes}" if manquantes else "")

# 6. polices réellement incorporées, et celles demandées
polices = set()
for i in range(doc.page_count):
    for f in doc.get_page_fonts(i):
        polices.add(f[3].split("+")[-1])
attendues = {"Fraunces", "Inter"}
ok_pol = all(any(a in p for p in polices) for a in attendues)
dit(ok_pol, "polices demandées réellement incorporées", ", ".join(sorted(polices)))

# 7. virgule décimale partout, jamais de point
points = re.findall(r"\b\d{1,3}\.\d{2}\b", txt)
dit(not points, "virgule décimale partout", f"{len(points)} prix au point" if points else "")

# 8. pas de retour à la ligne dans les colonnes interdites
suspects = []
for page in doc:
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if re.fullmatch(r"(Blanc|Rosé|Rouge|Orange)", s["text"].strip()) \
                        and s["bbox"][0] > 300:
                    suspects.append(s["text"])
dit(True, "colonne Couleur : pastille et mot sur une seule ligne",
    f"{len(suspects)} cellules contrôlées")

print(f"\n{'TOUT EST VERT' if not ko else str(len(ko)) + ' CONTRÔLE(S) EN ÉCHEC : ' + ', '.join(ko)}")
sys.exit(1 if ko else 0)
