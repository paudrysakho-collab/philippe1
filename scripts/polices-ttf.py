#!/usr/bin/env python3
"""Fabrique les .ttf à téléverser dans Canva, à partir des paquets @fontsource.

Les woff2 de fontsource sont découpés en sous-jeux : « latin » porte l'alphabet et les
accents français, « latin-ext » le reste. On réunit les deux, puis on déclare les graisses
SemiBold comme le « gras » de leur famille — sans quoi le bouton gras de Canva fabrique
un faux gras à la place du vrai dessin.

Nécessite fontTools (pip install fonttools brotli). À relancer seulement si les polices changent.
"""
import json
import os
import tempfile
from fontTools.ttLib import TTFont
from fontTools.merge import Merger

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, 'src/fonts')
SORTIE = os.path.join(RACINE, 'polices-canva')

# famille fontsource, graisse, style -> (fichier livré, gras de la famille ?)
FICHIERS = [
    ('young-serif', '400', 'normal', 'YoungSerif-Regular.ttf', None),
    ('spectral', '400', 'normal', 'Spectral-Regular.ttf', None),
    ('spectral', '400', 'italic', 'Spectral-Italic.ttf', None),
    ('spectral', '600', 'normal', 'Spectral-SemiBold.ttf', 'Spectral'),
    ('ibm-plex-sans', '400', 'normal', 'IBMPlexSans-Regular.ttf', None),
    ('ibm-plex-sans', '600', 'normal', 'IBMPlexSans-SemiBold.ttf', 'IBM Plex Sans'),
]


def reunir(famille, graisse, style, tmp):
    """Les deux sous-jeux d'une même police, fondus en un seul fichier."""
    morceaux = []
    for sous_jeu in ('latin', 'latin-ext'):
        police = TTFont(os.path.join(SOURCE, f'{famille}-{sous_jeu}-{graisse}-{style}.woff2'))
        police.flavor = None
        chemin = os.path.join(tmp, f'{famille}-{sous_jeu}-{graisse}-{style}.ttf')
        police.save(chemin)
        morceaux.append(chemin)
    return Merger().merge(morceaux)


def lier_en_gras(police, famille):
    """Déclare cette police comme le gras de `famille`, pour que le bouton gras tombe juste."""
    noms = police['name']
    for plateforme, encodage, langue in ((3, 1, 0x409), (1, 0, 0)):
        noms.setName(famille, 1, plateforme, encodage, langue)
        noms.setName('Bold', 2, plateforme, encodage, langue)
        noms.setName(f'{famille} Bold', 4, plateforme, encodage, langue)
        noms.setName(famille.replace(' ', '') + '-Bold', 6, plateforme, encodage, langue)
    # les noms « typographiques » recréeraient une famille à part : on les retire
    noms.names = [n for n in noms.names if n.nameID not in (16, 17, 21, 22)]
    police['OS/2'].fsSelection = (police['OS/2'].fsSelection & ~0b1000000) | 0b100000
    police['head'].macStyle |= 1


os.makedirs(SORTIE, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for famille, graisse, style, fichier, gras in FICHIERS:
        police = reunir(famille, graisse, style, tmp)
        if gras:
            lier_en_gras(police, gras)
        police.save(os.path.join(SORTIE, fichier))
        cmap = TTFont(os.path.join(SORTIE, fichier)).getBestCmap()
        manque = [c for c in 'éèêëàâçôûùîïœŒÉÀÇŸ’«»€°' if ord(c) not in cmap]
        etat = 'tous les caractères français' if not manque else 'MANQUE ' + ''.join(manque)
        print(f'{fichier:28} {len(cmap):4} glyphes, {etat}')
print('→', os.path.relpath(SORTIE, RACINE))
