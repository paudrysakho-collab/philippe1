#!/usr/bin/env python3
"""Reporte sur les fiches les labels de la liste des vignerons du Salon Privé.

Décision de l'agence (2 octobre 2026, QUESTIONS.md point 22) : la liste des vignerons
fait foi pour les labels, au salon ET dans le catalogue général. Chaque fiche présente
au salon prend donc le label de la notice de son stand (`labels_affiches` de
data/salon-prive-2026.json), tel quel. Les fiches absentes du salon gardent les labels
du tarif. Les labels du tarif restent consignés dans `labels_tarif` : rien ne se perd.

Le script est idempotent : on peut le relancer après une correction du fichier du salon.
Ensuite : npm run donnees (assemble et vérifie).
"""
import json
import pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
salon = json.loads((RACINE / "data/salon-prive-2026.json").read_text(encoding="utf-8"))

PREUVE = ("liste des vignerons du Salon Privé, notice du stand {stand} — fait foi pour les "
          "labels, salon et catalogue général (l'agence, 2 octobre 2026)")

vus = {}
for s in salon["stands"]:
    affiches = dict(s["labels_affiches"])
    # Divin No Low n'entre au salon que si le fichier de Mathéo en liste des vins
    for n, labels in (s.get("labels_affiches_si_present") or {}).items():
        if int(n) in s.get("domaines", []):
            affiches[n] = labels
    for n, labels in affiches.items():
        vus[int(n)] = (s["stand"], labels)

def valeur(texte, cle):
    """Début et fin de la valeur (une liste) de `cle` dans le texte JSON mis en page à la main."""
    debut = texte.index(f'"{cle}": [') + len(f'"{cle}": ')
    profondeur, dans_chaine, i = 0, False, debut
    while True:
        c = texte[i]
        if dans_chaine:
            if c == "\\": i += 1
            elif c == '"': dans_chaine = False
        elif c == '"': dans_chaine = True
        elif c == "[": profondeur += 1
        elif c == "]":
            profondeur -= 1
            if profondeur == 0:
                return debut, i + 1
        i += 1


def compact(labels):
    return "[" + ", ".join("{ " + ", ".join(f'"{k}": {json.dumps(v, ensure_ascii=False)}'
                                            for k, v in l.items()) + " }" for l in labels) + "]"


changes = []
for n, (stand, labels) in sorted(vus.items()):
    chemin = RACINE / f"data/fiches/{n:02d}.json"
    texte = chemin.read_text(encoding="utf-8")
    fiche = json.loads(texte)
    avant = [l["label"] for l in fiche["labels"]]
    nouveaux = [{"label": l, "preuve": PREUVE.format(stand=stand)} for l in labels]
    # La mise en page à la main des fiches est gardée : on ne remplace que la valeur.
    d, f = valeur(texte, "labels")
    if "labels_tarif" not in fiche:
        texte = texte[:d] + compact(nouveaux) + ",\n  \"labels_tarif\": " + texte[d:f] + texte[f:]
    else:
        texte = texte[:d] + compact(nouveaux) + texte[f:]
    json.loads(texte)   # le fichier reste du JSON valide
    chemin.write_text(texte, encoding="utf-8")
    if avant != labels:
        changes.append(f"n°{n} : {' + '.join(avant) or 'aucun'} → {' + '.join(labels) or 'aucun'}")

print(f"{len(vus)} fiches au salon, labels de la liste des vignerons :")
for c in changes:
    print("  " + c)
