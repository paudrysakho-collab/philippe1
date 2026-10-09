#!/bin/sh
# Les catalogues caviste par département (l'agence, 10 octobre 2026) : le 85 est
# `npm run global` ; ce script fait les autres, chacun = le 85 moins les domaines qui ne livrent
# pas le département (SANS_DEPARTEMENT de scripts/prix-global.py).
#     sh scripts/variantes-dpt.sh            les cinq : 49 53 35 44 56
#     sh scripts/variantes-dpt.sh 49 53      seulement ceux-là
set -e
cd "$(dirname "$0")/.."
LISTE=${*:-"49 53 35 44 56"}
for d in $LISTE; do
  echo "——— catalogue caviste Dpt $d"
  EDITION=global DPT=$d node scripts/construire.mjs
  EDITION=global DPT=$d node scripts/controler.mjs
  EDITION=global DPT=$d node scripts/deco.mjs
  EDITION=global DPT=$d node scripts/pptx.mjs
  python3 scripts/ranger-pptx.py "dist/catalogue-caviste-2026-dpt$d-canva.pptx"
  EDITION=global DPT=$d node scripts/controler-pptx.mjs
done
