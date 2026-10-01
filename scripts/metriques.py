#!/usr/bin/env python3
"""Relève les chasses des polices livrées, pour que le générateur .pptx sache
calculer la largeur d'un titre ou d'un jeton sans ouvrir de navigateur.

Sortie : src/fonts/metriques.json (versionné, pour que `npm run pptx`
n'ait pas besoin de fontTools). À relancer seulement si les polices changent.
"""
import json
import os
from fontTools.ttLib import TTFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES = {
    'Young Serif': 'YoungSerif-Regular.ttf',
    'Spectral': 'Spectral-Regular.ttf',
    'Spectral Bold': 'Spectral-SemiBold.ttf',
    'IBM Plex Sans': 'IBMPlexSans-Regular.ttf',
    'IBM Plex Sans Bold': 'IBMPlexSans-SemiBold.ttf',
}

sortie = {}
for nom, fichier in FACES.items():
    f = TTFont(os.path.join(RACINE, 'polices-canva', fichier))
    upm = f['head'].unitsPerEm
    hmtx = f['hmtx']
    cmap = f.getBestCmap()
    largeurs = {}
    for cp, glyphe in cmap.items():
        if glyphe in hmtx.metrics:
            largeurs[str(cp)] = round(hmtx[glyphe][0] / upm, 4)
    defaut = largeurs.get(str(ord('n')), 0.5)
    sortie[nom] = {'defaut': defaut, 'chasses': largeurs}
    print(f'{nom:22} {len(largeurs)} glyphes, chasse « n » {defaut}')

chemin = os.path.join(RACINE, 'src/fonts/metriques.json')
with open(chemin, 'w', encoding='utf-8') as fh:
    json.dump(sortie, fh, ensure_ascii=False, separators=(',', ':'))
print('→', chemin, os.path.getsize(chemin), 'octets')
