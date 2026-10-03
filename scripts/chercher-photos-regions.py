#!/usr/bin/env python3
"""Cherche sur Wikimedia Commons des photos de paysages viticoles, une série par région.

Photos libres de droits, licence compatible avec un usage commercial (CC0, CC BY, CC BY-SA,
domaine public), assez grandes pour l'impression. Elles illustrent une RÉGION, jamais un
domaine précis (brief, « Photos »). Sortie : data/photos-regions-candidats.json, et des
vignettes dans build/photos-regions/ pour choisir à l'œil.
Usage : python3 scripts/chercher-photos-regions.py [région…]
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

RACINE = pathlib.Path(__file__).resolve().parent.parent
SORTIE = RACINE / "data/photos-regions-candidats.json"
VIGNETTES = RACINE / "build/photos-regions"
UA = "SCIO-catalogue/1.0 (catalogue Agence SCIO)"
API = "https://commons.wikimedia.org/w/api.php"
LICENCES = re.compile(r"^(CC0|CC BY(-SA)? [0-9.]+|Public domain|PD)", re.I)

REQUETES = {
    "Loire": ["Vouvray vignoble", "vignoble Saumur", "Sancerre vignes", "Muscadet vignoble"],
    "Alsace": ["vignoble Alsace village", "Alsace vineyard Riquewihr", "route des vins Alsace vignes"],
    "Beaujolais": ["Beaujolais vignoble paysage", "Beaujolais vineyards hills", "Fleurie vignoble", "Morgon vignes", "Pierres dorées vignes", "Brouilly vignoble"],
    "Bourgogne": ["Côte de Beaune vignes", "Burgundy vineyards Meursault", "Pommard vignoble"],
    "Rhône": ["Dentelles de Montmirail vignes", "Gigondas vignoble", "Châteauneuf-du-Pape galets vignes"],
    "Sud-Ouest": ["Madiran vignoble", "vignoble Gers", "Armagnac vignes paysage", "Jurançon vignoble", "Cahors vignoble", "Gascogne vignes"],
    "Bordeaux": ["Saint-Émilion vignoble", "Médoc vignoble", "Côtes de Bourg vignes"],
    "Provence": ["Provence vineyard", "vignoble Provence", "Côtes de Provence vignes", "Bandol vignoble", "Sainte-Victoire vignes", "Var vineyard landscape"],
    "Languedoc": ["Corbières vignoble", "Minervois vignes", "Languedoc vineyard garrigue", "Saint-Chinian vignoble", "Hérault vignes paysage", "vignoble Aude"],
    "Champagne": ["vignoble Champagne Hautvillers", "Champagne vineyards Marne", "Côte des Blancs vignes"],
    "_général": ["vineyard rows sunset France", "rangs de vigne automne", "vineyard autumn golden light France", "vignoble coucher de soleil", "vignes automne Bourgogne", "vineyard golden hour"],
}


def get(params, essais=6):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    for k in range(essais):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:  # 429 : on attend et on recommence
            time.sleep(8 * (k + 1))
    print(f"  (Commons ne répond pas, requête sautée)")
    return {}


def chercher(q):
    d = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap",
             "gsrnamespace": 6, "gsrlimit": 12, "prop": "imageinfo",
             "iiprop": "url|size|extmetadata", "iiurlwidth": 480,
             "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription"})
    out = []
    for p in d.get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]
        m = ii.get("extmetadata", {})
        lic = m.get("LicenseShortName", {}).get("value", "")
        if not LICENCES.match(lic) or ii["width"] < 2000 or ii["width"] < ii["height"]:
            continue
        out.append({"titre": p["title"], "page": ii["descriptionurl"], "image": ii["url"],
                    "vignette": ii["thumburl"], "largeur": ii["width"], "hauteur": ii["height"],
                    "licence": lic, "auteur": re.sub(r"<.*?>", "", m.get("Artist", {}).get("value", "")).strip(),
                    "requete": q})
    return out


def main():
    regions = sys.argv[1:] or list(REQUETES)
    tout = json.loads(SORTIE.read_text(encoding="utf-8")) if SORTIE.exists() else {}
    VIGNETTES.mkdir(parents=True, exist_ok=True)
    for r in regions:
        vus, liste = set(), []
        for q in REQUETES[r]:
            for c in chercher(q):
                if c["titre"] not in vus:
                    vus.add(c["titre"])
                    liste.append(c)
            time.sleep(5)
        for i, c in enumerate(liste):
            f = VIGNETTES / f"{r}-{i:02d}.jpg"
            if not f.exists():
                req = urllib.request.Request(c["vignette"], headers={"User-Agent": UA})
                try:
                    f.write_bytes(urllib.request.urlopen(req, timeout=30).read())
                except Exception:
                    time.sleep(3)
            c["fichier_vignette"] = str(f.relative_to(RACINE))
        tout[r] = liste
        print(f"{r} : {len(liste)} candidates")
        SORTIE.write_text(json.dumps(tout, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
