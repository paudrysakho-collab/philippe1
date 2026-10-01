#!/usr/bin/env python3
"""Assemble data/agence.json + data/fiches/*.json dans data/catalogue.json."""
import json, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
agence = json.loads((RACINE / "data/agence.json").read_text(encoding="utf-8"))
fiches = [json.loads(p.read_text(encoding="utf-8"))
          for p in sorted((RACINE / "data/fiches").glob("*.json"))]
fiches.sort(key=lambda f: f["numero"])

catalogue = {
    "edition": agence["edition"],
    "cible": agence["cible"],
    "devise": "EUR",
    "agence": agence,
    "domaines": fiches,
}
sortie = RACINE / "data/catalogue.json"
sortie.write_text(json.dumps(catalogue, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"{sortie.relative_to(RACINE)} : {len(fiches)} domaines")
