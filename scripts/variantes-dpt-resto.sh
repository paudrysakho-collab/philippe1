#!/bin/sh
# Le catalogue restaurant par département (l'agence, 17 octobre 2026) : le 85 est
# `npm run restaurant` ; ce script fait les autres, chacun = le 85 moins les domaines qui ne
# livrent pas le département (SANS_DEPARTEMENT de scripts/prix-global.py).
#     sh scripts/variantes-dpt-resto.sh          les cinq : 49 53 35 44 56
#     sh scripts/variantes-dpt-resto.sh 49       seulement celui-là
set -e
cd "$(dirname "$0")/.."
LISTE=${*:-"49 53 35 44 56"}
for d in $LISTE; do
  echo "——— catalogue restaurant Dpt $d"
  EDITION=restaurant DPT=$d node scripts/construire.mjs
  EDITION=restaurant DPT=$d node scripts/controler.mjs
done
