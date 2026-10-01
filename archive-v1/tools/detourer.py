"""Remplace le fond blanc des packshots et des logos par l'ivoire de la page.

Les packshots et les logos fournis sont sur fond blanc. Posés sur le papier ivoire,
ils y dessinent un rectangle blanc — exactement la « carte flottante » que la
direction artistique proscrit. Le moteur d'impression ne gère pas les modes de
fusion : on traite donc l'image en amont.

Le détourage est progressif : chaque pixel reçoit une opacité calculée à partir de
sa distance au blanc, ce qui préserve les bords doux du flacon et les ombres
portées, au lieu de les découper au couteau.
"""
import os, sys
from PIL import Image

IVOIRE = (246, 241, 232)
SEUIL_OPAQUE = 232      # en dessous, le pixel appartient au sujet
SEUIL_FOND = 253        # au dessus, c'est du fond
DST = "assets/photos/detoures"


def detoure(chemin_src, chemin_dst):
    im = Image.open(chemin_src).convert("RGB")
    px = im.load()
    l, h = im.size
    for y in range(h):
        for x in range(l):
            r, v, b = px[x, y]
            mini = min(r, v, b)
            if mini >= SEUIL_FOND:
                px[x, y] = IVOIRE
            elif mini > SEUIL_OPAQUE:
                a = (SEUIL_FOND - mini) / (SEUIL_FOND - SEUIL_OPAQUE)
                px[x, y] = tuple(round(c * a + f * (1 - a))
                                 for c, f in zip((r, v, b), IVOIRE))
    os.makedirs(os.path.dirname(chemin_dst), exist_ok=True)
    im.save(chemin_dst)
    return im.size


def main():
    for rel in sys.argv[1:]:
        src = os.path.join("assets/photos", rel)
        dst = os.path.join(DST, os.path.basename(rel))
        taille = detoure(src, dst)
        print(f"   {os.path.basename(rel):<30} {taille[0]}x{taille[1]} → {dst}")


if __name__ == "__main__":
    main()
