#!/usr/bin/env python3
"""Prépare les images des fiches : un cadrage rond, une bouteille détourée, un traitement unique.

D'où viennent les images : les dossiers de l'agence, copiés tels quels dans src/photos/brut/
(chemin ignoré par git : les originaux restent en local, seules les images traitées sont
versionnées).

    src/photos/brut/Bouteilles_de_vin/<Nom_du_domaine>/…       → la bouteille
    src/photos/brut/Domaines_et_vignerons/<Nom_du_domaine>/…   → le rond (vigneron ou logo)

Le nom du dossier est le nom du domaine. L'appariement dossier → domaine, et le choix d'une
image dans chaque dossier, sont écrits dans data/photos-locales.json une fois validés par
l'agence : ce script ne devine rien, il applique cette table et rien d'autre.

    python3 scripts/preparer-photos.py --inventaire   liste brut/, propose une correspondance,
                                                      fait une planche de contact par dossier
    python3 scripts/preparer-photos.py                prépare les images de la table validée

Sorties : src/photos/rond/dNN.jpg (pour le PDF, cerclé par la feuille de style),
src/photos/rond/dNN-cercle.png (le même, déjà masqué en cercle, pour le .pptx),
src/photos/bouteille/dNN.png (détourée, fond transparent) et data/photos-preparees.json.
Ce qui est écarté (trop petit, non détourable) l'est dans data/photos-ecartees.json, avec
la raison : l'emplacement garde alors son repère pointillé.

Le traitement est appliqué par cette seule fonction, à toutes les images : c'est ce qui
les fait appartenir au même catalogue plutôt qu'à quarante univers différents.
"""
import io, json, math, pathlib, re, subprocess, sys, unicodedata
from PIL import (Image, ImageChops, ImageCms, ImageDraw, ImageEnhance, ImageFilter, ImageOps,
                 ImageStat)

RACINE = pathlib.Path(__file__).resolve().parent.parent
BRUT = RACINE / "src/photos/brut"
ARBRES = {"bouteille": "Bouteilles_de_vin", "rond": "Domaines_et_vignerons"}
TABLE = RACINE / "data/photos-locales.json"
ROND = RACINE / "src/photos/rond"
BOUT = RACINE / "src/photos/bouteille"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".gif", ".heic"}

# Les emplacements, en millimètres : ils ne bougent pas, l'agence compte dessus.
MM_ROND = 40
MM_BOUT_L, MM_BOUT_H = 24, 62
PPI_CIBLE, PPI_PLANCHER = 300, 200
def px(mm, ppi=PPI_CIBLE):
    return round(mm / 25.4 * ppi)
PX_ROND = px(MM_ROND)                   # 472 px
PX_BOUT_L = px(MM_BOUT_L)               # 283 px
PX_BOUT_H = px(MM_BOUT_H)               # 732 px


class Ecartee(Exception):
    """Une image qu'on ne pose pas : l'emplacement reste vide, avec sa raison."""


def ouvrir(chemin):
    """Ouvre une image comme on la voit : redressée selon l'EXIF, ramenée en sRGB."""
    im = Image.open(chemin)
    im = ImageOps.exif_transpose(im)
    icc = im.info.get("icc_profile")
    if im.mode == "P":
        im = im.convert("RGBA")
    if icc and im.mode in ("RGB", "RGBA", "CMYK"):
        try:
            sortie = "RGBA" if im.mode == "RGBA" else "RGB"
            im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                           ImageCms.createProfile("sRGB"), outputMode=sortie)
        except Exception:
            pass
    if im.mode == "LA":
        im = im.convert("RGBA")
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    return im


def recadrer(im, entree):
    """'zone' [x0, y0, x1, y1], en fractions de l'image, isole une partie de la source :
    une bouteille dans une photo de gamme, un visage dans une scène. C'est un recadrage,
    jamais un agrandissement : la résolution se calcule ensuite sur la partie gardée."""
    z = entree.get("zone")
    if not z:
        return im
    l, h = im.size
    return im.crop((round(z[0] * l), round(z[1] * h), round(z[2] * l), round(z[3] * h)))


def a_de_la_transparence(im):
    return im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 250


def aplatir(im, fond=None):
    """Un logo en PNG transparent doit retomber sur un fond qui le laisse lisible :
    clair sous un logo sombre, sombre sous un logo clair. La table peut imposer ce fond
    ('fond': '#ffffff'), quand le logo porte déjà son propre cartouche clair."""
    if im.mode not in ("RGBA", "LA", "P"):
        return im.convert("RGB")
    im = im.convert("RGBA")
    opaque = im.getchannel("A").point(lambda a: 255 if a > 60 else 0)
    if not opaque.getbbox():
        return im.convert("RGB")
    r, v, b = ImageStat.Stat(im.convert("RGB"), mask=opaque).mean
    clarte = 0.2126 * r + 0.7152 * v + 0.0722 * b
    if fond is None:
        fond = (70, 96, 110) if clarte > 150 else (251, 248, 241)
    plat = Image.new("RGB", im.size, fond)
    plat.paste(im, (0, 0), im)
    return plat


def etalonner(im):
    """Le traitement unique : légèrement désaturé, réchauffé, contraste tenu.
    Les images viennent de quarante domaines ; elles doivent sortir d'une même main."""
    im = ImageEnhance.Color(im).enhance(0.82)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    r, v, b = im.split()
    r = r.point(lambda x: min(255, int(x * 1.035 + 3)))
    b = b.point(lambda x: max(0, int(x * 0.965)))
    return Image.merge("RGB", (r, v, b))


def traitement(im, fond=None):
    return etalonner(aplatir(im, fond))


def remplir_depuis_les_bords(proche, taille):
    """On ne retire que le fond ATTEINT DEPUIS LES BORDS. Sans cela, le corps d'une
    bouteille de blanc, presque aussi clair que son fond, serait effacé lui aussi."""
    larg, haut = taille
    masque = proche.tobytes()
    vus = bytearray(larg * haut)
    pile = []
    for i in list(range(larg)) + list(range((haut - 1) * larg, haut * larg)) \
            + list(range(0, haut * larg, larg)) + list(range(larg - 1, haut * larg, larg)):
        if masque[i] and not vus[i]:
            vus[i] = 1; pile.append(i)
    while pile:
        i = pile.pop()
        x = i % larg
        for j in ((i + 1) if x < larg - 1 else -1, (i - 1) if x > 0 else -1,
                  i + larg if i + larg < larg * haut else -1, i - larg):
            if j >= 0 and not vus[j] and masque[j]:
                vus[j] = 1; pile.append(j)
    return Image.frombytes("L", taille, bytes(vus)).point(lambda v: 0 if v else 255)


def couleur_des_coins(im):
    coins = [im.getpixel(p) for p in
             ((2, 2), (im.width - 3, 2), (2, im.height - 3), (im.width - 3, im.height - 3))]
    return tuple(sum(c[i] for c in coins) // 4 for i in range(3))


def silhouette(alpha):
    """Une bouteille vue de face n'a, sur chaque ligne, qu'une seule largeur pleine, et son
    corps est régulier. Le remplissage depuis les bords peut entrer dans l'objet quand une
    étiquette blanche touche le bord du verre : il la mange avec le fond blanc, et le papier
    apparaît au travers. On remplit donc chaque ligne d'un bord à l'autre, puis on vérifie le
    corps (la moitié basse) : une ligne nettement plus étroite que les autres dit que le
    détourage a creusé la bouteille. Rend l'alpha rempli, ou None si la silhouette est creusée.
    Au pied, la première ligne plus large que le corps est une ombre portée : la silhouette
    s'arrête là, quitte à perdre un ou deux pixels de fond de bouteille."""
    l, h = alpha.size
    donnees = alpha.tobytes()
    lignes = []
    for y in range(h):
        rang = donnees[y * l:(y + 1) * l]
        a = rang.find(255)
        lignes.append((a, rang.rfind(255)) if a >= 0 else None)
    pleines = [y for y, r in enumerate(lignes) if r]
    if not pleines:
        return None
    haut, bas = pleines[0], pleines[-1]
    corps = range(haut + (bas - haut) // 2, bas - (bas - haut) // 50)
    largeurs = sorted(lignes[y][1] - lignes[y][0] + 1 for y in corps if lignes[y])
    if not largeurs:
        return None
    mediane = largeurs[len(largeurs) // 2]
    etroites = [y for y in corps if not lignes[y] or lignes[y][1] - lignes[y][0] + 1 < 0.85 * mediane]
    # Le talon arrondi rétrécit la bouteille sur ses dernières lignes : ce n'est pas un trou.
    # Seule compte une ligne étroite prise entre deux lignes pleines du corps.
    fin = corps[-1]
    while etroites and etroites[-1] == fin:
        etroites.pop(); fin -= 1
    if len(etroites) > max(2, 0.005 * len(corps)):
        return None
    for y in range(bas - (bas - haut) // 12, bas + 1):
        if lignes[y] and lignes[y][1] - lignes[y][0] + 1 > 1.12 * mediane:
            bas = y - 1
            break
    sortie = bytearray(l * h)
    for y in range(haut, bas + 1):
        if lignes[y]:
            a, b = lignes[y]
            sortie[y * l + a:y * l + b + 1] = b"\xff" * (b - a + 1)
    return Image.frombytes("L", (l, h), bytes(sortie))


def detourer(im, tolerances=(24, 16, 11, 7), fond=None):
    """Retire le fond uni (blanc, noir ou gris) atteint depuis les bords. Rend l'alpha, la
    tolérance retenue et la part gardée ; l'alpha vaut None si aucune tolérance ne donne
    une bouteille entière. Le fond se lit dans les coins de l'image entière : au second
    passage, sur la bouteille recadrée, un coin peut tomber dans l'ombre portée."""
    fond = fond or couleur_des_coins(im)
    diff = ImageChops.difference(im, Image.new("RGB", im.size, fond)).convert("L")
    garde = 0.0
    for tolerance in tolerances:
        proche = diff.point(lambda x, t=tolerance: 255 if x < t else 0)
        alpha = remplir_depuis_les_bords(proche, im.size)
        garde = alpha.histogram()[255] / (im.width * im.height)
        # Une bouteille de blanc sur fond blanc se confond avec son fond : si le détourage
        # en garde trop peu, ou s'il creuse la bouteille, on resserre la tolérance.
        if garde <= 0.06 or garde > 0.92:
            continue
        plein = silhouette(alpha)
        if plein is not None:
            return plein, tolerance, garde
    return None, None, garde


def cercle(im):
    """Le rond, déjà masqué : pour le .pptx, où un masque de forme n'est pas sûr de survivre
    à l'import. Le bord est lissé par suréchantillonnage."""
    n, k = im.width, 4
    m = Image.new("L", (n * k, n * k), 0)
    ImageDraw.Draw(m).ellipse((0, 0, n * k - 1, n * k - 1), fill=255)
    rgba = im.convert("RGBA")
    rgba.putalpha(m.resize((n, n), Image.LANCZOS))
    return rgba


# ——————————————————————————————————————————————————————————— le rond ———

def plancher_rond(c):
    ppi = c / (MM_ROND / 25.4)
    if ppi < PPI_PLANCHER:
        raise Ecartee(f"trop petite : {c} px de côté utile, {ppi:.0f} ppi à {MM_ROND} mm "
                      f"(plancher {PPI_PLANCHER} ppi, soit {px(MM_ROND, PPI_PLANCHER)} px)")
    return ppi


def reculer(im, cadre):
    """Plusieurs personnes : on ne recadre pas serré, on recule, pour que toutes les têtes
    tiennent dans le cercle. 'cadre' [x0, y0, x1, y1], en fractions de l'image, désigne ce
    qui doit entrer ; le carré qui l'entoure peut déborder de la photo. Ce qui manque alors
    est rempli de la couleur du bord de la photo (le ciel, le plafond, l'herbe), et le
    raccord est fondu : le cercle reste plein et rien de net n'est inventé."""
    W, H = im.size
    x0, y0, x1, y1 = cadre[0] * W, cadre[1] * H, cadre[2] * W, cadre[3] * H
    c = round(max(x1 - x0, y1 - y0))
    g, h = round((x0 + x1 - c) / 2), round((y0 + y1 - c) / 2)
    if g >= 0 and h >= 0 and g + c <= W and h + c <= H:
        return im.crop((g, h, g + c, h + c)), c
    part = im.crop((max(0, g), max(0, h), min(W, g + c), min(H, h + c)))
    pw, ph = part.size
    L, T = max(0, -g), max(0, -h)
    R, B = c - L - pw, c - T - ph
    # chaque marge prend la couleur médiane du bord qu'elle prolonge : une tête qui touche
    # le bord ne s'étire pas en traînée dans le ciel
    k = max(3, min(pw, ph) // 40)
    mediane = lambda bande: tuple(round(v) for v in ImageStat.Stat(bande).median)
    fond = Image.new("RGB", (c, c), mediane(part))
    if T:
        fond.paste(mediane(part.crop((0, 0, pw, k))), (0, 0, c, T))
    if B:
        fond.paste(mediane(part.crop((0, ph - k, pw, ph))), (0, T + ph, c, c))
    if L:
        fond.paste(mediane(part.crop((0, 0, k, ph))), (0, T, L, T + ph))
    if R:
        fond.paste(mediane(part.crop((pw - k, 0, pw, ph))), (L + pw, T, c, T + ph))
    fond.paste(part, (L, T))
    net = fond.copy()
    fond = fond.filter(ImageFilter.GaussianBlur(c / 30))
    # le masque de la photo nette, fondu sur les seuls bords qui tombent dans le carré
    f = max(2, c // 40)
    masque = Image.new("L", (c, c), 0)
    ImageDraw.Draw(masque).rectangle((L + (f if L else -f), T + (f if T else -f),
                                      L + pw - 1 - (f if R else -f), T + ph - 1 - (f if B else -f)),
                                     fill=255)
    masque = masque.filter(ImageFilter.GaussianBlur(f / 2))
    return Image.composite(net, fond, masque), c


def diptyque(entree):
    """Deux portraits séparés de deux personnes nommées ensemble : chacun occupe une moitié
    du rond, son visage au milieu de sa moitié, avec un mince filet clair entre les deux."""
    moities, cotes = [], []
    for e in entree["diptyque"]:
        im = traitement(recadrer(ouvrir(BRUT / e["fichier"]), e))
        c = min(im.size)
        cx, cy = e.get("centre", [0.5, 0.4])
        g = max(0, min(im.width - c, round(cx * im.width - c / 2)))
        h = max(0, min(im.height - c, round(cy * im.height - c / 2)))
        moities.append((im.crop((g, h, g + c, h + c)), (cx * im.width - g) / c))
        cotes.append(c)
    c = min(cotes)
    ppi = plancher_rond(c)
    cote = min(PX_ROND, c)
    rond = Image.new("RGB", (cote, cote), (251, 248, 241))
    demi = cote // 2
    for i, (carre, fx) in enumerate(moities):
        carre = carre.resize((cote, cote), Image.LANCZOS)
        g = max(0, min(cote - demi, round(fx * cote - demi / 2)))
        rond.paste(carre.crop((g, 0, g + demi, cote)), (i * (cote - demi), 0))
    filet = max(2, cote // 160)
    ImageDraw.Draw(rond).rectangle((demi - filet // 2, 0, demi + filet - filet // 2 - 1, cote),
                                   fill=(251, 248, 241))
    return rond, ppi


def faire_rond(numero, entree):
    if entree.get("diptyque"):
        im, ppi = diptyque(entree)
        sortie = ROND / f"d{int(numero):02d}.jpg"
        im.save(sortie, "JPEG", quality=88, optimize=True, progressive=True)
        cercle(im).save(ROND / f"d{int(numero):02d}-cercle.png", "PNG", optimize=True)
        return sortie, " + ".join("x".join(map(str, Image.open(BRUT / e["fichier"]).size))
                                  for e in entree["diptyque"]), round(ppi)
    src = BRUT / entree["fichier"]
    im = ouvrir(src)
    l0, h0 = im.size
    im = recadrer(im, entree)
    if entree.get("mode", "couvrir") == "contenir":
        im, ppi = rond_logo(im, entree.get("forme"), entree.get("fond"))
    else:
        im = traitement(im)
        if entree.get("cadre"):
            im, c = reculer(im, entree["cadre"])
            ppi = plancher_rond(c)
        else:
            # Carré sans déformation. Par défaut on centre en largeur et on prend le tiers
            # haut plutôt que la moitié : les visages sont hauts. La table peut fixer le centre.
            c = min(im.size)
            ppi = plancher_rond(c)
            cx, cy = entree.get("centre", [None, None])
            g = (im.width - c) // 2 if cx is None else round(cx * im.width - c / 2)
            h = (im.height - c) // 3 if cy is None else round(cy * im.height - c / 2)
            g = max(0, min(im.width - c, g)); h = max(0, min(im.height - c, h))
            im = im.crop((g, h, g + c, h + c))
        # on ne grandit jamais une image : sous 300 ppi, elle garde ses pixels
        cote = min(PX_ROND, c)
        im = im.resize((cote, cote), Image.LANCZOS)
    sortie = ROND / f"d{int(numero):02d}.jpg"
    im.save(sortie, "JPEG", quality=88, optimize=True, progressive=True)
    cercle(im).save(ROND / f"d{int(numero):02d}-cercle.png", "PNG", optimize=True)
    return sortie, f"{l0}x{h0}", round(ppi)


def rond_logo(im, forme=None, fond=None):
    """Un logo ne se recadre jamais : il entre en entier, centré, à l'échelle, sur une
    réserve claire. C'est sa diagonale qui doit tenir dans le cercle, pas sa largeur :
    un logo carré posé au plus large aurait ses coins rognés par le masque. Un logo déjà
    rond ('forme': 'rond') tient par son diamètre, avec un liseré d'air."""
    plat = traitement(im, fond)
    fond = couleur_des_coins(plat)
    diff = ImageChops.difference(plat, Image.new("RGB", plat.size, fond)).convert("L")
    boite = diff.point(lambda x: 255 if x > 18 else 0).getbbox() or (0, 0, *plat.size)
    logo = plat.crop(boite)
    lw, lh = logo.size
    # la diagonale du logo occupe 86 % du diamètre : un peu d'air tout autour
    s = (0.92 * PX_ROND / max(lw, lh)) if forme == "rond" else 0.86 * PX_ROND / math.hypot(lw, lh)
    ppi = PPI_CIBLE / s
    if ppi < PPI_PLANCHER:
        raise Ecartee(f"logo trop petit : {lw}x{lh} px utiles, {ppi:.0f} ppi une fois posé "
                      f"(plancher {PPI_PLANCHER} ppi)")
    # sous 300 ppi, c'est le cercle qui se resserre autour du logo, jamais le logo qui grossit
    cote = round(PX_ROND / max(1.0, s))
    echelle = min(1.0, s)
    logo = logo.resize((max(1, round(lw * echelle)), max(1, round(lh * echelle))), Image.LANCZOS)
    reserve = Image.new("RGB", (cote, cote), fond)
    reserve.paste(logo, ((cote - logo.width) // 2, (cote - logo.height) // 2))
    return reserve, ppi


# ——————————————————————————————————————————————————————— la bouteille ———

def faire_bouteille(numero, entree):
    src = BRUT / entree["fichier"]
    im = ouvrir(src)
    l0, h0 = im.size
    im = recadrer(im, entree)

    if a_de_la_transparence(im):
        # déjà détourée : on garde son alpha tel quel
        alpha = im.getchannel("A")
        rgb = etalonner(im.convert("RGB"))
        boite = alpha.point(lambda a: 255 if a > 24 else 0).getbbox()
        if not boite:
            raise Ecartee("image entièrement transparente")
        rgba = rgb.convert("RGBA"); rgba.putalpha(alpha)
        rgba = rgba.crop(boite)
    else:
        rgb = etalonner(im.convert("RGB"))
        # Premier passage sur une copie réduite : il trouve la tolérance et la bouteille.
        f = min(1.0, 1200 / max(rgb.size))
        travail = rgb.resize((round(rgb.width * f), round(rgb.height * f)), Image.LANCZOS) \
            if f < 1 else rgb
        alpha, tolerance, garde = detourer(travail)
        if alpha is None:
            if garde > 0.92:
                raise Ecartee("fond non uni : le détourage ne trouve pas la bouteille "
                              f"(il garde {garde:.0%} de l'image)")
            if garde <= 0.06:
                raise Ecartee("le détourage n'a presque rien gardé (fond et bouteille confondus)")
            raise Ecartee("détourage incertain : l'étiquette ou le verre se confond avec le "
                          "fond et la bouteille sortirait trouée ; il faut une version détourée "
                          "(PNG transparent) ou sur un fond qui tranche")
        b = alpha.getbbox()
        marge = round(0.03 * max(rgb.size))
        boite = (max(0, round(b[0] / f) - marge), max(0, round(b[1] / f) - marge),
                 min(rgb.width, round(b[2] / f) + marge), min(rgb.height, round(b[3] / f) + marge))
        # Second passage, sur la bouteille seule, à une fois et demie la taille d'usage :
        # le bord est net, et une petite bouteille dans une grande image garde ses pixels.
        zone = rgb.crop(boite)
        k = min(1.0, 1.6 * min(PX_BOUT_L / zone.width, PX_BOUT_H / zone.height))
        if k < 1:
            zone = zone.resize((round(zone.width * k), round(zone.height * k)), Image.LANCZOS)
        alpha, _, _ = detourer(zone, (tolerance,), couleur_des_coins(travail))
        if alpha is None:
            raise Ecartee("détourage incertain au second passage")
        # On lisse le bord : un détourage dur se voit à l'impression.
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.9)).point(lambda x: 0 if x < 120 else 255)
        alpha = alpha.filter(ImageFilter.GaussianBlur(0.6))
        rgba = zone.convert("RGBA"); rgba.putalpha(alpha)
        b2 = rgba.getbbox()
        if not b2:
            raise Ecartee("le détourage n'a rien gardé")
        rgba = rgba.crop(b2)
        rgba.info["natif"] = (rgba.width / k, rgba.height / k)

    # Contenue dans 24 × 62 mm, sans déformation : c'est l'axe limitant qui fixe la résolution.
    nl, nh = rgba.info.get("natif", rgba.size)
    s = min(PX_BOUT_L / nl, PX_BOUT_H / nh)      # échelle qui donnerait 300 ppi
    ppi = PPI_CIBLE / s
    if ppi < PPI_PLANCHER:
        raise Ecartee(f"trop petite : bouteille de {nl:.0f}x{nh:.0f} px, {ppi:.0f} ppi "
                      f"dans {MM_BOUT_L}x{MM_BOUT_H} mm (plancher {PPI_PLANCHER} ppi)")
    # jamais agrandie : sous 300 ppi elle garde ses pixels, au-dessus elle descend à 300
    cible = (max(1, round(nl * min(1.0, s))), max(1, round(nh * min(1.0, s))))
    rgba = rgba.resize(cible, Image.LANCZOS)
    sortie = BOUT / f"d{int(numero):02d}.png"
    rgba.save(sortie, "PNG", optimize=True)
    return sortie, f"{l0}x{h0}", round(ppi)


# ——————————————————————————————————————————————————————— l'inventaire ———

MOTS_VIDES = {"domaine", "domaines", "chateau", "champagne", "maison", "famille", "et", "de",
              "du", "des", "la", "le", "les", "l", "d", "fils", "vins", "vin", "vignobles", "jus",
              "cepages", "sa", "sas", "earl", "scea", "gaec"}


def mots(texte):
    t = unicodedata.normalize("NFD", texte).encode("ascii", "ignore").decode().lower()
    return [m for m in re.split(r"[^a-z0-9]+", t) if m]


def proposer(dossier, domaines):
    """Une proposition, jamais une décision : la table se valide à l'œil, par l'agence."""
    plie = "".join(mots(dossier))
    meilleurs = []
    for d in domaines:
        cles = [m for m in mots(d["nom"]) if m not in MOTS_VIDES and len(m) > 1]
        if not cles:
            continue
        trouves = sum(1 for m in cles if m in plie)
        if trouves:
            meilleurs.append((trouves / len(cles), d["numero"], d["nom"]))
    meilleurs.sort(key=lambda t: (-t[0], t[1]))
    return meilleurs[:3]


def images_de(dossier):
    return sorted(p for p in dossier.rglob("*")
                  if p.is_file() and p.suffix.lower() in EXTENSIONS and not p.name.startswith("."))


def planche(dossier, fichiers, sortie, vign=220, cols=6):
    lignes = math.ceil(len(fichiers) / cols) or 1
    feuille = Image.new("RGB", (cols * (vign + 10) + 10, lignes * (vign + 34) + 10), "#3a3a3a")
    dess = ImageDraw.Draw(feuille)
    for k, p in enumerate(fichiers):
        x, y = 10 + (k % cols) * (vign + 10), 10 + (k // cols) * (vign + 34)
        try:
            im = ouvrir(p)
            l, h = im.size
            if im.mode == "RGBA":   # damier sous la transparence : on voit si c'est détouré
                fond = Image.new("RGB", im.size, "#d8d8d8")
                d2 = ImageDraw.Draw(fond)
                pas = max(8, max(im.size) // 40)
                for i in range(0, im.width, pas):
                    for j in range(0, im.height, pas):
                        if (i // pas + j // pas) % 2:
                            d2.rectangle((i, j, i + pas - 1, j + pas - 1), fill="#ffffff")
                fond.paste(im, (0, 0), im); im = fond
            im.thumbnail((vign, vign), Image.LANCZOS)
            feuille.paste(im, (x + (vign - im.width) // 2, y + (vign - im.height) // 2))
            etiquette = f"{k + 1}. {p.name[:26]}  {l}x{h}"
        except Exception as e:
            etiquette = f"{k + 1}. {p.name[:26]}  illisible"
        dess.text((x, y + vign + 6), etiquette, fill="#f0f0f0")
    feuille.save(sortie, "JPEG", quality=82)


def inventaire():
    domaines = json.loads((RACINE / "data/catalogue.json").read_text(encoding="utf-8"))["domaines"]
    if not BRUT.is_dir():
        raise SystemExit(f"{BRUT.relative_to(RACINE)} n'existe pas : copiez-y les deux arborescences.")
    planches = RACINE / "build/planches"; planches.mkdir(parents=True, exist_ok=True)
    rapport = ["| Arborescence | Dossier | Images | Proposition (à valider) | Plus grande image |",
               "|---|---|---|---|---|"]
    for arbre in sorted(p for p in BRUT.iterdir() if p.is_dir()):
        for dossier in sorted(p for p in arbre.iterdir() if p.is_dir()):
            fichiers = images_de(dossier)
            props = proposer(dossier.name, domaines)
            prop = "; ".join(f"n°{n} {nom} ({score:.0%})" for score, n, nom in props) or "aucune"
            plus = "—"
            if fichiers:
                tailles = []
                for p in fichiers:
                    try:
                        with Image.open(p) as im:
                            tailles.append((im.size[0] * im.size[1], f"{im.size[0]}x{im.size[1]}"))
                    except Exception:
                        pass
                plus = max(tailles)[1] if tailles else "illisible"
                planche(dossier, fichiers, planches / f"{arbre.name}--{dossier.name}.jpg")
            rapport.append(f"| {arbre.name} | {dossier.name} | {len(fichiers)} | {prop} | {plus} |")
        en_vrac = [p for p in arbre.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS]
        if en_vrac:
            rapport.append(f"| {arbre.name} | (fichiers hors dossier) | {len(en_vrac)} | — | — |")
    texte = "\n".join(rapport) + "\n"
    (RACINE / "build/inventaire-photos.md").write_text(texte, encoding="utf-8")
    print(texte)
    print(f"planches de contact → {planches.relative_to(RACINE)}/")


# ——————————————————————————————————————————————————————— la préparation ———

def obtenir(e):
    """Une image prise sur un site garde son adresse dans la table : si l'original manque
    dans brut/ (autre machine, dossier vidé), on le retélécharge tel quel. Les images de
    l'agence et du Canva, elles, se recopient à la main (voir README)."""
    chemin = BRUT / e["fichier"]
    if chemin.exists() or not e.get("url"):
        return
    chemin.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sS", "-L", "--max-time", "60", "-A", "Mozilla/5.0", "-o",
                    str(chemin), e["url"]], check=False)
    if chemin.exists() and chemin.stat().st_size < 2000:
        chemin.unlink()


def preparer():
    table = json.loads(TABLE.read_text(encoding="utf-8")) if TABLE.exists() else {}
    ROND.mkdir(parents=True, exist_ok=True); BOUT.mkdir(parents=True, exist_ok=True)
    # Ce script possède ces deux dossiers : une image d'un passage précédent qui n'est plus
    # dans la table ne doit pas survivre, sinon elle finirait sur la mauvaise fiche.
    for p in list(ROND.glob("d*.*")) + list(BOUT.glob("d*.*")):
        p.unlink()
    posees, ecartees = [], []
    for n, entree in sorted(((k, v) for k, v in table.items() if not k.startswith("_")),
                            key=lambda kv: int(kv[0])):
        for role, faire in (("rond", faire_rond), ("bouteille", faire_bouteille)):
            e = entree.get(role)
            if not e:
                continue
            sources = e.get("diptyque") or [e]
            for s in sources:
                obtenir(s)
            fichiers = " + ".join(s["fichier"] for s in sources)
            try:
                sortie, source_px, ppi = faire(n, e)
            except (Ecartee, FileNotFoundError) as raison:
                ecartees.append({"numero": int(n), "role": role, "fichier": fichiers,
                                 "raison": str(raison)})
                print(f"n°{int(n):>2} {role:<9} ÉCARTÉE  {fichiers} — {raison}")
                continue
            posees.append({"numero": int(n), "role": role,
                           "fichier": str(sortie.relative_to(RACINE)),
                           "source_url": " + ".join(s.get("url") or f"src/photos/brut/{s['fichier']}"
                                                    for s in sources),
                           "page": e.get("page") or sources[0].get("page"),
                           "provenance": e.get("provenance", "dossier de l'agence"),
                           "source_px": source_px, "ppi": ppi, "sujet": e.get("sujet", "")})
            print(f"n°{int(n):>2} {role:<9} {sortie.name:<8} source {source_px:>10}  {ppi} ppi")
    (RACINE / "data/photos-preparees.json").write_text(
        json.dumps(posees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (RACINE / "data/photos-ecartees.json").write_text(
        json.dumps(ecartees, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\n{len(posees)} images préparées → data/photos-preparees.json"
          f"\n{len(ecartees)} écartées → data/photos-ecartees.json")
    ecrire_credits(posees)


def ecrire_credits(posees):
    """Les deux tables de credits.md (une ligne par image, puis le récapitulatif par
    domaine) se réécrivent ici, entre leurs repères : elles ne peuvent pas dériver de ce
    qui est réellement posé."""
    chemin = RACINE / "credits.md"
    if not chemin.exists():
        return
    texte = chemin.read_text(encoding="utf-8")
    debut, fin = "<!-- images:debut -->", "<!-- images:fin -->"
    if debut not in texte or fin not in texte:
        return
    noms = {d["numero"]: d["nom"] for d in
            json.loads((RACINE / "data/catalogue.json").read_text(encoding="utf-8"))["domaines"]}
    taille = {"rond": f"{MM_ROND} mm", "bouteille": f"{MM_BOUT_L} × {MM_BOUT_H} mm"}

    def court(p):
        pr = p.get("provenance", "")
        return "site du domaine" if "site officiel" in pr else ("Canva de l'agence" if "Canva" in pr
                                                                 else "dossier de l'agence")

    lignes = ["| n° | Domaine | Image | Sujet | Provenance | Source | Résolution | Droits |",
              "|---|---|---|---|---|---|---|---|"]
    for p in posees:
        if "site officiel" in p.get("provenance", ""):
            source = f"page {p['page']} — image " + " + ".join(
                f"<{u}>" for u in p["source_url"].split(" + "))
            droits = "**autorisation à demander au domaine**"
        else:
            source = " + ".join(f"`{u.replace('src/photos/brut/', '')}`"
                                for u in p["source_url"].split(" + "))
            droits = "photothèque de l'agence"
        lignes.append(f"| {p['numero']} | {noms[p['numero']]} | {p['role']} (`{p['fichier']}`) | "
                      f"{p['sujet']} | {p.get('provenance', '')} | {source} | "
                      f"{p['source_px']} px → {p['ppi']} ppi à {taille[p['role']]} | {droits} |")
    par = {}
    for p in posees:
        par.setdefault(p["numero"], {})[p["role"]] = p
    recap = ["| n° | Domaine | Rond (40 mm) | Bouteille (24 × 62 mm) |", "|---|---|---|---|"]
    for n in sorted(noms):
        cases = []
        for role in ("rond", "bouteille"):
            p = par.get(n, {}).get(role)
            cases.append(f"{p['sujet']} — {court(p)}, {p['ppi']} ppi" if p else "**vide** (pointillé)")
        recap.append(f"| {n} | {noms[n]} | {cases[0]} | {cases[1]} |")
    bloc = (f"{debut}\n\n**{len(posees)} images posées sur 80 emplacements.**\n\n"
            "### Image par image\n\n" + "\n".join(lignes) +
            "\n\n### Récapitulatif par domaine\n\n" + "\n".join(recap) + f"\n\n{fin}")
    a, b = texte.index(debut), texte.index(fin) + len(fin)
    chemin.write_text(texte[:a] + bloc + texte[b:], encoding="utf-8")
    print("credits.md → tables des images réécrites")


if __name__ == "__main__":
    inventaire() if "--inventaire" in sys.argv else preparer()
