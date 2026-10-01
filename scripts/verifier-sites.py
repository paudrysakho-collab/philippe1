#!/usr/bin/env python3
"""Vérifie qu'une URL candidate est bien le site du domaine viticole, et pas un homonyme.

On lit le titre et la description de la page d'accueil, rien d'autre : aucun fait n'en sort.
"""
import html, json, pathlib, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor

RACINE = pathlib.Path(__file__).resolve().parent.parent
cat = json.loads((RACINE / "data/catalogue.json").read_text(encoding="utf-8"))
cands = json.loads((RACINE / "data/sites-candidats.json").read_text(encoding="utf-8"))
par_numero = {d["numero"]: d for d in cat["domaines"]}

MOTS_VIN = ("vin", "vigne", "vignoble", "domaine", "château", "chateau", "champagne",
            "cuvée", "cuvee", "appellation", "aoc", "aop", "igp", "millésime", "millesime",
            "vigneron", "cave", "chai", "winery", "wine", "terroir", "bouteille", "caviste")

def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

def jetons(nom):
    petits = {"de", "du", "des", "la", "le", "les", "et", "fils", "domaine", "chateau",
              "champagne", "maison", "jus", "cepages", "famille"}
    mots = re.findall(r"[a-z]{4,}", sansaccent(nom))
    return [m for m in mots if m not in petits] or mots

def page(url):
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "14", "--max-filesize", "600000",
             "-H", "User-Agent: Mozilla/5.0 (compatible; AgenceSCIO-catalogue/1.0)", url],
            capture_output=True, text=True, timeout=30, errors="replace")
        return r.stdout[:200000]
    except Exception:
        return ""

def resume(h):
    t = re.search(r"<title[^>]*>(.*?)</title>", h, re.S | re.I)
    d = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', h, re.S | re.I)
    o = re.search(r'<meta[^>]+property=["\']og:site_name["\'][^>]+content=["\'](.*?)["\']', h, re.S | re.I)
    net = lambda s: html.unescape(re.sub(r"\s+", " ", s or "")).strip()[:160]
    return net(t.group(1) if t else ""), net(d.group(1) if d else ""), net(o.group(1) if o else "")

def examiner(numero, url):
    h = page(url)
    titre, desc, site = resume(h)
    corps = sansaccent(f"{titre} {desc} {site} {h[:60000]}")
    nom = par_numero[numero]["nom"]
    js = jetons(nom)
    nom_ok = any(j in corps for j in js)
    vin_ok = any(sansaccent(m) in corps for m in MOTS_VIN)
    return {"numero": numero, "url": url, "titre": titre, "description": desc,
            "nom_trouve": nom_ok, "vocabulaire_vin": vin_ok,
            "verdict": "probable" if (nom_ok and vin_ok) else ("vin mais nom absent" if vin_ok else "hors sujet")}

taches = [(int(k), u) for k, v in cands.items() for u in sorted(set(v["candidats"]))]
print(f"{len(taches)} pages à examiner…")
with ThreadPoolExecutor(max_workers=10) as ex:
    res = list(ex.map(lambda t: examiner(*t), taches))

res.sort(key=lambda r: (r["numero"], r["verdict"] != "probable"))
(RACINE / "data/sites-examen.json").write_text(
    json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

for r in res:
    marque = {"probable": "OUI", "vin mais nom absent": " ? ", "hors sujet": "non"}[r["verdict"]]
    print(f"{r['numero']:>2} [{marque}] {r['url'][:52]:<52} {r['titre'][:60]}")
