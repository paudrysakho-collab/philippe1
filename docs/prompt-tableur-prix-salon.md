# Prompt à donner à un autre Claude pour remplir le tableur des prix du salon

Joindre au message le fichier `tableur/prix-salon-prive-2026.xlsx` (sur GitHub, branche
`claude/design-skill-propositions-suwoa9`), plus la liste des prix de l'agence (PDF, photo,
Excel, mail…). Puis coller le texte ci-dessous.

---

Tu vas remplir un tableur de prix pour le **Salon Privé Vins & Terroirs** de l'Agence SCIO
(lundi 5 octobre 2026). Je te joins deux choses : le tableur vide
`prix-salon-prive-2026.xlsx` et la liste des prix de l'agence. Ton seul travail : **recopier
les prix dans le tableur, sans rien changer d'autre**, puis me rendre le fichier .xlsx rempli.
Un programme le relira automatiquement : il refusera le fichier si la forme n'est pas
respectée.

**Comment est fait le tableur** (onglet « Prix du salon », il doit garder ce nom) :
- Une ligne de titres : Réf. (A), Vin (B), Couleur (C), Millésime (D), Contenance (E),
  Prix salon (F), Palier 1 (G), Palier 2 (H), Palier 3 (I).
- Les vins sont rangés par stand. Chaque stand commence par une ligne « S01 », « S02 »… en
  colonne A, puis une ligne qui rappelle les intitulés de paliers du domaine en G à I (par
  exemple « À partir de 120 bts », « À partir de 180 bts », « À partir de 300 bts »).
- Puis une ligne par vin, avec en colonne A une référence « S01 V01 », « S01 V02 »…

**Les règles à respecter absolument :**
1. **Ne touche jamais à la colonne A**, ni aux colonnes B à E. Ne supprime, n'ajoute et ne
   déplace aucune ligne. Ne renomme pas l'onglet.
2. Tu écris seulement dans les colonnes **F, G, H, I**, sur les lignes de vin (« S.. V.. »).
3. **Pour chaque stand, choisis UN mode, jamais les deux :**
   - **un prix unique par vin** : colonne F (« Prix salon ») seulement, G à I vides ;
   - **ou les paliers du domaine** : colonnes G, H, I seulement (autant de colonnes que le
     stand a d'intitulés de paliers sur sa ligne de rappel), F vide.
   Le mode se décide d'après la liste de l'agence. Deux stands différents peuvent avoir des
   modes différents.
4. En mode paliers, **un vin a tous ses paliers remplis ou aucun**. Pas de prix dans une
   colonne de palier qui n'a pas d'intitulé pour ce stand.
5. **Format des prix** : en euros, nombre avec au plus deux décimales, par exemple `12.5` ou
   `12,50` ou `12,50 €`. Positif. Rien d'autre dans la case (pas de « HT », pas de texte,
   pas de « ? »).
6. **Un vin sans prix connu : laisse ses cases vides.** C'est permis, il apparaîtra avec des
   cases vides. N'invente jamais un prix, n'en déduis aucun d'un autre vin ou d'un autre
   millésime, ne corrige pas un prix qui te paraît faux.
7. Pour rapprocher un vin de la liste de l'agence et une ligne du tableur, appuie-toi sur le
   stand, le domaine, la cuvée, l'appellation, la couleur et le millésime. **Si tu hésites
   entre deux lignes, ou si un vin de la liste n'est pas dans le tableur (ou l'inverse), ne
   devine pas** : laisse vide et note-le.

**Ce que tu me rends :**
- le fichier `.xlsx` rempli, avec le même nom ;
- un court compte rendu : le mode choisi par stand (unique ou paliers), le nombre de prix
  remplis, et la liste de tout ce que tu n'as pas pu placer ou qui t'a fait douter (stand,
  vin, prix de la liste, raison).

Écris-moi en français simple.
