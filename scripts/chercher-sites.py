#!/usr/bin/env python3
"""Génère des URL candidates pour chaque domaine et retient celles qui répondent.

Rien n'est déduit du contenu des sites : on cherche seulement une adresse.
Les faits du catalogue restent ceux du PDF source.
"""
import json, pathlib, re, subprocess, unicodedata
from concurrent.futures import ThreadPoolExecutor

RACINE = pathlib.Path(__file__).resolve().parent.parent
cat = json.loads((RACINE / "data/catalogue.json").read_text(encoding="utf-8"))

def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def slugs(nom):
    n = sansaccent(nom).lower()
    n = n.split(" / ")[0].split(" —")[0]
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    mots = [m for m in n.split() if m]
    petits = {"de", "du", "des", "la", "le", "les", "d", "et", "fils", "l"}
    cles = [m for m in mots if m not in petits]
    prefixes = {"domaine", "chateau", "champagne", "maison", "prieure", "bastide", "famille", "chai"}
    noyau = [m for m in cles if m not in prefixes] or cles
    out = []
    for base in ({"-".join(mots), "".join(mots), "-".join(cles), "".join(cles),
                  "-".join(noyau), "".join(noyau)}):
        if base:
            out.append(base)
    # variantes avec le préfixe collé devant le noyau
    for p in prefixes:
        if p in mots:
            for j in ("-".join(noyau), "".join(noyau)):
                out.append(f"{p}-{j}")
                out.append(f"{p}{j}")
    return sorted(set(out))

def candidats(nom):
    urls = []
    for s in slugs(nom):
        if len(s) < 4 or len(s) > 48:
            continue
        for tld in (".fr", ".com"):
            urls.append(f"https://www.{s}{tld}")
    return urls

def sonder(url):
    try:
        r = subprocess.run(
            ["curl", "-sS", "-L", "--max-time", "9", "-o", "/dev/null",
             "-w", "%{http_code} %{url_effective}",
             "-H", "User-Agent: Mozilla/5.0 (compatible; AgenceSCIO-catalogue/1.0)", url],
            capture_output=True, text=True, timeout=20)
        code, _, eff = r.stdout.strip().partition(" ")
        return (url, code, eff.strip())
    except Exception:
        return (url, "000", "")

taches = []
for d in cat["domaines"]:
    for u in candidats(d["nom"]):
        taches.append((d["numero"], d["nom"], u))

print(f"{len(taches)} URL à sonder pour {len(cat['domaines'])} domaines…")
trouves = {}
with ThreadPoolExecutor(max_workers=16) as ex:
    futs = {ex.submit(sonder, u): (n, nom, u) for n, nom, u in taches}
    for f in futs:
        n, nom, u = futs[f]
        url, code, eff = f.result()
        if code == "200":
            trouves.setdefault(n, {"numero": n, "nom": nom, "candidats": []})
            trouves[n]["candidats"].append(eff or url)

sortie = RACINE / "data/sites-candidats.json"
sortie.write_text(json.dumps(trouves, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
manquants = [d["numero"] for d in cat["domaines"] if d["numero"] not in trouves]
print(f"{len(trouves)} domaines avec au moins une piste ; sans piste : {manquants}")
