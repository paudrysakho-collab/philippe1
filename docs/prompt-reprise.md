# Prompt pour reprendre dans une nouvelle session Claude

Copier le texte ci-dessous dans une nouvelle session Claude Code ouverte sur le dépôt
`paudrysakho-collab/philippe1`.

---

Tu reprends le projet « catalogue Agence SCIO 2026 » (Agence SCIO Vins & Spirits, Rezé) là où la session précédente l'a laissé. Tu travailles en français, pour l'agence, qui écrit vite et souvent à la voix.

1. Mets-toi à jour sans rien me demander, sur la branche de travail (ne pousse que là) :
   git fetch origin claude/design-skill-propositions-suwoa9 && git checkout -B claude/design-skill-propositions-suwoa9 origin/claude/design-skill-propositions-suwoa9
2. Lis avec l'outil de lecture, en entier : CLAUDE.md (le brief), puis docs/reprise.md — section 0 (comment je travaille et ce que j'attends), section 1 (installation : fais-la sans en parler), et surtout la section 9 (le catalogue caviste global, le travail en cours). L'historique détaillé est dans JOURNAL.md, les questions ouvertes dans QUESTIONS.md (point 32).
3. Le livrable en cours est le « Catalogue caviste — Vins & Terroirs » : `npm run global` → dist/catalogue-caviste-2026-ecran.pdf et -imprimeur.pdf (64 pages, 41 fiches, 598 prix, contrôles au vert). Tous ses prix, l'ordre des fiches, les domaines ajoutés et les corrections vivent dans scripts/prix-global.py : c'est là qu'on retouche, jamais dans le HTML.
4. Règles qui ne bougent pas : un prix ne s'invente ni ne se corrige jamais seul (il vient d'un tarif annoté ou de moi) ; après chaque changement, `npm run global` (et `npm run build` si une photo partagée change), contrôles au vert, pages touchées regardées en image, commit et push, puis tu m'envoies les PNG des pages touchées et le PDF avec leurs chemins sur GitHub. Réponses courtes, en français simple.
5. Banque d'images : l'ancien catalogue (sources/ancien-catalogue/, ses images seulement), mon Google Drive (connecteur Drive, dossier Domaines_et_vignerons et « _A_identifier »), puis les sites officiels des domaines. Des visages plutôt que des logos.

Quand tu es prêt, dis-moi en deux lignes où on en est et attends mes demandes. Agis sans me poser de questions, sauf s'il manque vraiment une donnée (un prix, un fait) : une seule question, à la fin.
