#!/usr/bin/env python3
"""Remet le .pptx dans l'ordre que les systèmes d'exploitation attendent.

pptxgenjs écrit l'archive en commençant par des entrées de dossier, et laisse
`[Content_Types].xml` au milieu. PowerPoint, LibreOffice et Canva s'en accommodent,
mais Windows, macOS et les navigateurs identifient un fichier en lisant son
**premier** élément : ils ne reconnaissent plus un PowerPoint et le confient au
premier lecteur venu — un lecteur vidéo, par exemple.

On réécrit donc l'archive avec `[Content_Types].xml` en tête, non compressé,
et sans les entrées de dossier, comme le fait PowerPoint lui-même.

Au passage, on répare les paragraphes à plusieurs morceaux (la lettrine et la suite
du texte, un mot en gras…). pptxgenjs y répète les propriétés du paragraphe
(`<a:pPr>`) devant chaque morceau, alors que la norme n'en admet qu'une, en tête.
LibreOffice passe outre ; un import plus strict, comme celui de Canva, peut perdre
la mise en forme du premier morceau : la lettrine redevient une lettre ordinaire.
Les répétitions sont toujours identiques à la première : on les retire.
"""
import os
import re
import shutil
import sys
import zipfile

CARTE = '[Content_Types].xml'
DIAPO = re.compile(r'ppt/(slides|slideLayouts|slideMasters|notesSlides)/[^/]+\.xml')
PARAGRAPHE = re.compile(r'(<a:p>)(.*?)(</a:p>)', re.S)
PROPRIETES = re.compile(r'<a:pPr\b[^>]*/>|<a:pPr\b[^>]*>.*?</a:pPr>', re.S)


def reparer(xml):
    """Une seule <a:pPr> par paragraphe, en tête. Rend le XML et le nombre de paragraphes repris."""
    repris = 0

    def un(m):
        nonlocal repris
        corps = m.group(2)
        props = PROPRIETES.findall(corps)
        if not props or (len(props) == 1 and corps.startswith(props[0])):
            return m.group(0)
        if any(p != props[0] for p in props):
            sys.exit('propriétés de paragraphe différentes dans un même paragraphe : '
                     'à regarder avant de réparer\n' + corps[:400])
        repris += 1
        return m.group(1) + props[0] + PROPRIETES.sub('', corps) + m.group(3)

    return PARAGRAPHE.sub(un, xml), repris


def ranger(chemin):
    with zipfile.ZipFile(chemin) as source:
        if CARTE not in source.namelist():
            sys.exit(f'{chemin} : pas de {CARTE}, ce n\'est pas un fichier Office')
        entrees = [i for i in source.infolist() if not i.filename.endswith('/')]
        ordre = ([i for i in entrees if i.filename == CARTE]
                 + [i for i in entrees if i.filename != CARTE])
        provisoire = chemin + '.rangé'
        repris = 0
        with zipfile.ZipFile(provisoire, 'w', zipfile.ZIP_DEFLATED) as sortie:
            for i, info in enumerate(ordre):
                contenu = source.read(info.filename)
                if DIAPO.fullmatch(info.filename):
                    xml, n = reparer(contenu.decode('utf-8'))
                    contenu, repris = xml.encode('utf-8'), repris + n
                # la carte d'identité reste non compressée : les renifleurs de type la lisent telle quelle
                sortie.writestr(info, contenu,
                                zipfile.ZIP_STORED if i == 0 else zipfile.ZIP_DEFLATED)
    shutil.move(provisoire, chemin)
    with zipfile.ZipFile(chemin) as verif:
        premier = verif.namelist()[0]
    taille = os.path.getsize(chemin) / 1e6
    print(f'✓ {os.path.basename(chemin)} rangé — '
          f'premier élément « {premier} », {repris} paragraphes remis à la norme, {taille:.1f} Mo')
    return premier == CARTE


if __name__ == '__main__':
    cible = sys.argv[1] if len(sys.argv) > 1 else 'dist/catalogue-scio-2026-canva.pptx'
    sys.exit(0 if ranger(cible) else 1)
