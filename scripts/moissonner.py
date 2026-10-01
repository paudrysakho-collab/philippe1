#!/usr/bin/env python3
"""Collecte les images des sites officiels des domaines, via curl (qui passe par le proxy).

On ne prend que des images. Aucun texte, aucun chiffre n'entre dans le catalogue :
le contenu reste celui de sources/tarif-septembre-2026.pdf.
"""
import html, io, json, os, pathlib, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from PIL import Image

RACINE = pathlib.Path(__file__).resolve().parent.parent
SITES = json.loads((RACINE / "data/sites-domaines.json").read_text(encoding="utf-8"))
BRUT = RACINE / "src/photos/brut"
BRUT.mkdir(parents=True, exist_ok=True)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
PISTES = re.compile(r"(vin|bouteille|cuv|gamme|domaine|maison|famille|qui-sommes|about|"
                    r"histoire|equipe|boutique|shop|produit|chai|vigneron|nous|accueil|"
                    r"wine|estate|home)", re.I)
IGNORE = re.compile(r"(sprite|icon|favicon|logo-?(facebook|insta|twitter|x|linkedin)|"
                    r"placeholder|spinner|loader|pixel|flag|drapeau|cookie|paypal|visa|"
                    r"mastercard|cb\.|arrow|fleche|chevron|burger)", re.I)

def recuperer(url, binaire=False, max_octets=6_000_000):
    cmd = ["curl", "-sS", "-L", "--max-time", "25", "--max-filesize", str(max_octets),
           "--compressed", "-H", f"User-Agent: {UA}",
           "-H", "Accept-Language: fr-FR,fr;q=0.9,en;q=0.8", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=45)
        return r.stdout if binaire else r.stdout.decode("utf-8", "replace")
    except Exception:
        return b"" if binaire else ""

def urls_images(page_html, base):
    trouvees = []
    def ajoute(u):
        if not u or u.startswith("data:"):
            return
        u = html.unescape(u.strip())
        if not u:
            return
        a = urljoin(base, u)
        if a.lower().split("?")[0].endswith((".svg", ".gif", ".webm", ".mp4")):
            return
        if IGNORE.search(a):
            return
        trouvees.append(a)

    for m in re.finditer(r"<(?:img|source)[^>]+>", page_html, re.I):
        bal = m.group(0)
        for attr in ("src", "data-src", "data-lazy-src", "data-original"):
            v = re.search(rf'{attr}=["\']([^"\']+)["\']', bal, re.I)
            if v:
                ajoute(v.group(1))
        ss = re.search(r'(?:data-)?srcset=["\']([^"\']+)["\']', bal, re.I)
        if ss:
            # on garde la plus grande variante annoncée
            best, bw = None, -1
            for part in ss.group(1).split(","):
                bits = part.strip().split()
                if not bits:
                    continue
                w = int(re.sub(r"\D", "", bits[1])) if len(bits) > 1 and bits[1].endswith("w") else 0
                if w >= bw:
                    best, bw = bits[0], w
            ajoute(best)
    for m in re.finditer(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
                         page_html, re.I):
        ajoute(m.group(1))
    for m in re.finditer(r'url\((["\']?)([^)"\']+)\1\)', page_html):
        ajoute(m.group(2))
    vues, out = set(), []
    for u in trouvees:
        if u not in vues:
            vues.add(u); out.append(u)
    return out

def pages_a_voir(page_html, base, limite=7):
    origine = urlparse(base).netloc
    liens, vues = [], set()
    for m in re.finditer(r'<a[^>]+href=["\']([^"\'#]+)["\']', page_html, re.I):
        u = urljoin(base, html.unescape(m.group(1))).split("#")[0]
        if urlparse(u).netloc != origine or u in vues:
            continue
        if not PISTES.search(u):
            continue
        if re.search(r"\.(pdf|jpg|png|zip|docx?)$", u, re.I):
            continue
        vues.add(u); liens.append(u)
        if len(liens) >= limite:
            break
    return liens

def moissonner(numero, site):
    dossier = BRUT / f"d{int(numero):02d}"
    dossier.mkdir(parents=True, exist_ok=True)
    accueil = recuperer(site)
    titre = ""
    t = re.search(r"<title[^>]*>(.*?)</title>", accueil, re.S | re.I)
    if t:
        titre = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()[:70]
    urls = urls_images(accueil, site)
    for p in pages_a_voir(accueil, site):
        urls += urls_images(recuperer(p), p)
    vues, propres = set(), []
    for u in urls:
        if u not in vues:
            vues.add(u); propres.append(u)
    propres = propres[:90]

    retenues = []
    for i, u in enumerate(propres):
        data = recuperer(u, binaire=True)
        if len(data) < 9000:
            continue
        try:
            im = Image.open(io.BytesIO(data))
            im.load()
        except Exception:
            continue
        if max(im.size) < 450:
            continue
        ext = (im.format or "JPEG").lower().replace("jpeg", "jpg")
        nom = f"{i:03d}.{ext}"
        (dossier / nom).write_bytes(data)
        retenues.append({"fichier": f"src/photos/brut/d{int(numero):02d}/{nom}",
                         "url": u, "l": im.size[0], "h": im.size[1],
                         "octets": len(data)})
    return {"numero": int(numero), "site": site, "titre": titre, "images": retenues}

numeros = [k for k in SITES if not k.startswith("_")]
if len(sys.argv) > 1:
    numeros = [n for n in numeros if n in sys.argv[1:]]

inventaire = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    futs = {ex.submit(moissonner, n, SITES[n]["site"]): n for n in numeros}
    for f in futs:
        n = futs[f]
        try:
            r = f.result()
        except Exception as e:
            r = {"numero": int(n), "site": SITES[n]["site"], "titre": f"ERREUR {e}", "images": []}
        inventaire[n] = r
        print(f"n°{n:>2} {r['titre'][:46]:<48} {len(r['images']):>3} images")

chemin = RACINE / "data/images-moissonnees.json"
anciennes = {}
if chemin.exists():
    anciennes = json.loads(chemin.read_text(encoding="utf-8"))
anciennes.update(inventaire)
chemin.write_text(json.dumps(anciennes, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"→ {chemin.relative_to(RACINE)}")
