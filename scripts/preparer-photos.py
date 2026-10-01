#!/usr/bin/env python3
"""Prépare les images retenues : un cadrage rond, une bouteille détourée, un traitement unique.

Le traitement est appliqué par cette seule fonction, à toutes les images : c'est ce qui
les fait appartenir au même catalogue plutôt qu'à quarante univers différents.
"""
import json, pathlib
from PIL import Image, ImageEnhance, ImageChops, ImageFilter

RACINE = pathlib.Path(__file__).resolve().parent.parent
inv = json.loads((RACINE / "data/images-moissonnees.json").read_text(encoding="utf-8"))
choix = json.loads((RACINE / "data/photos-choisies.json").read_text(encoding="utf-8"))
ROND = RACINE / "src/photos/rond"; ROND.mkdir(parents=True, exist_ok=True)
BOUT = RACINE / "src/photos/bouteille"; BOUT.mkdir(parents=True, exist_ok=True)

# Tailles d'usage, à 300 ppi : le rond fait 34 mm, la bouteille 26 mm de large.
PX_ROND = round(34 / 25.4 * 300)        # 402 px
PX_BOUT_L = round(26 / 25.4 * 300)      # 307 px

def aplatir(im):
    """Un logo en PNG transparent doit retomber sur un fond qui le laisse lisible :
    clair sous un logo sombre, sombre sous un logo clair."""
    if im.mode not in ("RGBA", "LA", "P"):
        return im.convert("RGB")
    im = im.convert("RGBA")
    pixels = [p for p in im.getdata() if p[3] > 60]
    if not pixels:
        return im.convert("RGB")
    clarte = sum(0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] for p in pixels) / len(pixels)
    fond = (70, 96, 110) if clarte > 150 else (251, 248, 241)
    plat = Image.new("RGB", im.size, fond)
    plat.paste(im, (0, 0), im)
    return plat

def traitement(im):
    """Le traitement unique : légèrement désaturé, réchauffé, contraste tenu.
    Les photos viennent de vingt sites différents ; elles doivent sortir d'une même main."""
    im = aplatir(im)
    im = ImageEnhance.Color(im).enhance(0.82)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    r, v, b = im.split()
    r = r.point(lambda x: min(255, int(x * 1.035 + 3)))
    b = b.point(lambda x: max(0, int(x * 0.965)))
    return Image.merge("RGB", (r, v, b))

def remplir_depuis_les_bords(proche, taille):
    """On ne retire que le fond ATTEINT DEPUIS LES BORDS. Sans cela, le corps d'une
    bouteille de blanc, presque aussi clair que son fond, serait effacé lui aussi."""
    larg, haut = taille
    masque = proche.load()
    vus = bytearray(larg * haut)
    pile = []
    for x in range(larg):
        for y in (0, haut - 1):
            if masque[x, y] and not vus[y * larg + x]:
                vus[y * larg + x] = 1; pile.append((x, y))
    for y in range(haut):
        for x in (0, larg - 1):
            if masque[x, y] and not vus[y * larg + x]:
                vus[y * larg + x] = 1; pile.append((x, y))
    while pile:
        x, y = pile.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = x + dx, y + dy
            if 0 <= a < larg and 0 <= b < haut and not vus[b * larg + a] and masque[a, b]:
                vus[b * larg + a] = 1; pile.append((a, b))
    return Image.frombytes("L", taille, bytes(0 if v else 255 for v in vus))

def chemin_source(numero, index):
    d = inv[str(numero)]
    for i in d["images"]:
        if pathlib.Path(i["fichier"]).stem == index:
            return RACINE / i["fichier"], i
    raise SystemExit(f"n°{numero} : image {index} introuvable")

def faire_rond(numero, index, mode="couvrir"):
    src, info = chemin_source(numero, index)
    im = Image.open(src)
    im = traitement(im)
    if mode == "contenir":
        # Un logo ne se recadre pas : il entre en entier, sur une réserve claire.
        c = max(im.size)
        bord = im.getpixel((1, 1))
        fond = Image.new("RGB", (c, c), bord)
        marge = round(c * 0.10)
        copie = im.copy()
        copie.thumbnail((c - 2 * marge, c - 2 * marge), Image.LANCZOS)
        fond.paste(copie, ((c - copie.width) // 2, (c - copie.height) // 2))
        im = fond
    else:
        # Carré centré, sans déformation : on ne coupe jamais au hasard, on prend le centre.
        c = min(im.size)
        g = (im.width - c) // 2
        h = (im.height - c) // 3      # un tiers plutôt que la moitié : les visages sont hauts
        im = im.crop((g, h, g + c, h + c))
    im = im.resize((PX_ROND, PX_ROND), Image.LANCZOS)
    sortie = ROND / f"d{int(numero):02d}.jpg"
    im.save(sortie, "JPEG", quality=86, optimize=True, progressive=True)
    return sortie, info, c

def faire_bouteille(numero, index):
    src, info = chemin_source(numero, index)
    im = Image.open(src).convert("RGB")
    im = traitement(im)
    # Le fond uni (blanc, noir ou gris) est retiré : pas de gros carré posé sur le papier.
    coins = [im.getpixel(p) for p in
             ((2, 2), (im.width - 3, 2), (2, im.height - 3), (im.width - 3, im.height - 3))]
    fond = tuple(sum(c[i] for c in coins) // 4 for i in range(3))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, fond)).convert("L")

    def alpha_pour(tolerance):
        proche = diff.point(lambda x: 255 if x < tolerance else 0)
        return remplir_depuis_les_bords(proche, im.size)

    # Une bouteille de blanc sur fond blanc se confond avec son fond : si le détourage
    # en garde trop peu, on resserre la tolérance jusqu'à retrouver un objet plausible.
    for tolerance in (24, 16, 11, 7):
        alpha = alpha_pour(tolerance)
        garde = sum(alpha.point(lambda x: 1 if x else 0).getdata())
        if garde > 0.06 * im.width * im.height:
            break

    # On lisse le bord : un détourage dur se voit à l'impression.
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.9)).point(lambda x: 0 if x < 120 else 255)
    alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    boite = rgba.getbbox()
    if boite:
        rgba = rgba.crop(boite)
    ratio = PX_BOUT_L / rgba.width
    rgba = rgba.resize((PX_BOUT_L, max(1, round(rgba.height * ratio))), Image.LANCZOS)
    sortie = BOUT / f"d{int(numero):02d}.png"
    rgba.save(sortie, "PNG", optimize=True)
    return sortie, info, rgba.size

lignes = []
for n, c in sorted(((k, v) for k, v in choix.items() if not k.startswith("_")), key=lambda kv: int(kv[0])):
    s, info, cote = faire_rond(n, c["rond"], c.get("mode", "couvrir"))
    ppi = round(cote / (34 / 25.4))
    lignes.append((int(n), "rond", s, info, ppi, c.get("rond_quoi", "")))
    print(f"n°{int(n):>2} rond      {s.name}  source {info['l']}x{info['h']}  {ppi} ppi à 34 mm")
    if "bouteille" in c:
        s, info, taille = faire_bouteille(n, c["bouteille"])
        ppi = round(info["l"] / (26 / 25.4))
        lignes.append((int(n), "bouteille", s, info, ppi, "bouteille du domaine"))
        print(f"n°{int(n):>2} bouteille {s.name}  source {info['l']}x{info['h']}  {ppi} ppi à 26 mm")

(RACINE / "data/photos-preparees.json").write_text(json.dumps(
    [{"numero": n, "role": r, "fichier": str(s.relative_to(RACINE)),
      "source_url": i["url"], "source_px": f"{i['l']}x{i['h']}", "ppi": p, "sujet": q}
     for n, r, s, i, p, q in lignes], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"\n{len(lignes)} images préparées → data/photos-preparees.json")
