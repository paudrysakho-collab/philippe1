#!/usr/bin/env python3
"""Remet le .pptx dans l'ordre que les systèmes d'exploitation attendent.

pptxgenjs écrit l'archive en commençant par des entrées de dossier, et laisse
`[Content_Types].xml` au milieu. PowerPoint, LibreOffice et Canva s'en accommodent,
mais Windows, macOS et les navigateurs identifient un fichier en lisant son
**premier** élément : ils ne reconnaissent plus un PowerPoint et le confient au
premier lecteur venu — un lecteur vidéo, par exemple.

On réécrit donc l'archive avec `[Content_Types].xml` en tête, non compressé,
et sans les entrées de dossier, comme le fait PowerPoint lui-même.
"""
import os
import shutil
import sys
import zipfile

CARTE = '[Content_Types].xml'


def ranger(chemin):
    with zipfile.ZipFile(chemin) as source:
        if CARTE not in source.namelist():
            sys.exit(f'{chemin} : pas de {CARTE}, ce n\'est pas un fichier Office')
        entrees = [i for i in source.infolist() if not i.filename.endswith('/')]
        ordre = ([i for i in entrees if i.filename == CARTE]
                 + [i for i in entrees if i.filename != CARTE])
        provisoire = chemin + '.rangé'
        with zipfile.ZipFile(provisoire, 'w', zipfile.ZIP_DEFLATED) as sortie:
            for i, info in enumerate(ordre):
                # la carte d'identité reste non compressée : les renifleurs de type la lisent telle quelle
                sortie.writestr(info, source.read(info.filename),
                                zipfile.ZIP_STORED if i == 0 else zipfile.ZIP_DEFLATED)
    shutil.move(provisoire, chemin)
    with zipfile.ZipFile(chemin) as verif:
        premier = verif.namelist()[0]
    taille = os.path.getsize(chemin) / 1e6
    print(f'✓ {os.path.basename(chemin)} rangé — '
          f'premier élément « {premier} », {taille:.1f} Mo')
    return premier == CARTE


if __name__ == '__main__':
    cible = sys.argv[1] if len(sys.argv) > 1 else 'dist/catalogue-scio-2026-canva.pptx'
    sys.exit(0 if ranger(cible) else 1)
