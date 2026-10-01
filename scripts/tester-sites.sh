#!/bin/bash
# Teste une liste d'URL candidates et retient la première qui répond 200.
for u in "$@"; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" -L --max-time 12 \
    -H 'User-Agent: Mozilla/5.0 (compatible; AgenceSCIO-catalogue/1.0)' "$u" 2>/dev/null)
  printf "%-48s %s\n" "$u" "${code:-000}"
done
