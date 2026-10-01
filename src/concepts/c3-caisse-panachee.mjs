import { domaine, euros, esc, famille, nbReferences, planche } from './commun.mjs';

const C = {
  caisse: '#F7F1E4', encre: '#211E1C', violet: '#67067C', or: '#E1C853',
  courant: '#2E6E9E', jardin: '#4C8A57', folies: '#C24030', arlequin: '#DE6E95',
};

/** Les couleurs de case, par famille de vin. Chacune porte le nom d'une cuvée de la sélection. */
const COULEUR = {
  blanc: C.courant, rouge: C.folies, rose: C.arlequin, bulles: C.or, doux: C.or,
  sansalcool: C.jardin, jus: C.jardin, biere: C.or, spiritueux: C.violet, autre: C.encre,
};
const NOM_FAMILLE = {
  blanc: 'Blanc', rouge: 'Rouge', rose: 'Rosé', bulles: 'Bulles', doux: 'Doux',
  sansalcool: 'Sans alcool', jus: 'Jus de cépages', biere: 'Bière', spiritueux: 'Spiritueux', autre: 'Autre',
};

/** Douze motifs dessinés ici même, tirés des noms de cuvées de la sélection. */
const MOTIFS = {
  lune:    (a, fond) => `<circle cx="50" cy="50" r="36" fill="${a}"/>
                   <circle cx="68" cy="42" r="30" fill="${fond}"/>`,
  courant: (a) => `<path d="M8 36 Q25 20 42 36 T76 36 M8 54 Q25 38 42 54 T76 54 M8 72 Q25 56 42 72 T76 72"
                     fill="none" stroke="${a}" stroke-width="7" stroke-linecap="round"/>`,
  dolmen:  (a) => `<rect x="18" y="20" width="64" height="13" rx="5" fill="${a}"/>
                   <rect x="26" y="40" width="16" height="42" fill="${a}"/>
                   <rect x="58" y="40" width="16" height="42" fill="${a}"/>`,
  grains:  (a) => `${[...Array(5)].map((_, i) => [...Array(5)].map((_, j) =>
                     `<circle cx="${18 + j * 16}" cy="${18 + i * 16}" r="${3.4 + ((i + j) % 3) * 1.5}" fill="${a}"/>`).join('')).join('')}`,
  arlequin:(a) => `<path d="M50 10 L78 50 L50 90 L22 50 Z" fill="${a}"/>
                   <path d="M50 28 L64 50 L50 72 L36 50 Z" fill="${C.caisse}"/>`,
  oiseau:  (a) => `<path d="M12 62 Q32 26 50 56 Q68 26 88 62" fill="none" stroke="${a}" stroke-width="8" stroke-linecap="round"/>
                   <circle cx="50" cy="74" r="6" fill="${a}"/>`,
  jardin:  (a) => `<path d="M50 88 L50 44" stroke="${a}" stroke-width="6" stroke-linecap="round"/>
                   <path d="M50 54 Q20 50 18 20 Q48 22 50 54 Z" fill="${a}"/>
                   <path d="M50 60 Q80 56 82 30 Q52 32 50 60 Z" fill="${a}"/>`,
  lumiere: (a) => `<circle cx="50" cy="50" r="20" fill="${a}"/>
                   ${[...Array(8)].map((_, i) => {
                     const t = (i / 8) * Math.PI * 2;
                     return `<line x1="${50 + Math.cos(t) * 28}" y1="${50 + Math.sin(t) * 28}"
                              x2="${50 + Math.cos(t) * 42}" y2="${50 + Math.sin(t) * 42}"
                              stroke="${a}" stroke-width="7" stroke-linecap="round"/>`;
                   }).join('')}`,
  potion:  (a) => `<path d="M50 50 m0 -34 a34 34 0 1 1 -24 10" fill="none" stroke="${a}" stroke-width="8" stroke-linecap="round"/>
                   <path d="M50 50 m0 -16 a16 16 0 1 0 12 6" fill="none" stroke="${a}" stroke-width="8" stroke-linecap="round"/>`,
  saisons: (a) => `<rect x="14" y="14" width="33" height="33" fill="${a}"/>
                   <rect x="53" y="14" width="33" height="33" fill="none" stroke="${a}" stroke-width="6"/>
                   <circle cx="30" cy="70" r="17" fill="none" stroke="${a}" stroke-width="6"/>
                   <circle cx="69" cy="70" r="17" fill="${a}"/>`,
  cosmos:  (a) => `<path d="M50 8 L58 38 L88 42 L62 58 L72 88 L50 70 L28 88 L38 58 L12 42 L42 38 Z" fill="${a}"/>`,
  fossile: (a) => `<path d="M50 86 C20 70 20 30 50 14 C80 30 80 70 50 86 Z" fill="none" stroke="${a}" stroke-width="7"/>
                   <path d="M50 74 C32 62 32 38 50 26 C68 38 68 62 50 74 Z" fill="none" stroke="${a}" stroke-width="5"/>
                   <circle cx="50" cy="50" r="5" fill="${a}"/>`,
};

const motif = (nom, fond, trait) =>
  `<svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet" class="motif"
     style="background:${fond}">${MOTIFS[nom](trait, fond)}</svg>`;

/** La caisse de couverture : douze cases, douze motifs nés des noms de la sélection. */
function caisseCouverture() {
  const cases = [
    ['lune', C.violet, C.or], ['courant', C.or, C.violet], ['dolmen', C.caisse, C.encre],
    ['grains', C.folies, C.caisse], ['arlequin', C.courant, C.caisse], ['oiseau', C.jardin, C.caisse],
    ['jardin', C.caisse, C.jardin], ['lumiere', C.arlequin, C.caisse], ['potion', C.encre, C.or],
    ['saisons', C.or, C.folies], ['cosmos', C.violet, C.caisse], ['fossile', C.courant, C.or],
  ];
  return `<div class="caisse-couv">${cases.map(([m, f, t]) => `<div class="case">${motif(m, f, t)}</div>`).join('')}</div>`;
}

/** La caisse du domaine : douze cases réparties au prorata réel des couleurs de sa gamme. */
function caisseDomaine(d) {
  const comptes = {};
  d.tableaux.forEach((t) => t.lignes.forEach((l) => {
    const f = famille(l, t);
    comptes[f] = (comptes[f] || 0) + 1;
  }));
  const total = nbReferences(d);
  const entrees = Object.entries(comptes).sort((a, b) => b[1] - a[1]);
  // On distribue douze cases au prorata, en garantissant une case à chaque famille présente.
  const parts = entrees.map(([f, n]) => ({ f, n, cases: Math.max(1, Math.round((n / total) * 12)) }));
  let somme = parts.reduce((a, p) => a + p.cases, 0);
  while (somme > 12) { parts.sort((a, b) => b.cases - a.cases)[0].cases--; somme--; }
  while (somme < 12) { parts.sort((a, b) => b.n / b.cases - a.n / a.cases)[0].cases++; somme++; }
  const cases = parts.flatMap((p) => Array(p.cases).fill(p.f));
  return `<div class="caisse-dom">${cases.map((f) =>
    `<div class="case-dom" style="background:${COULEUR[f]}"></div>`).join('')}</div>
    <div class="caisse-leg">${parts.map((p) =>
      `<span><i style="background:${COULEUR[p.f]}"></i>${p.n} ${esc(NOM_FAMILLE[p.f].toLowerCase())}</span>`).join('')}</div>`;
}

function tableau(t) {
  const paliers = t.paliers.map((p) => `<div class="cel-pal">${esc(p)}</div>`).join('');
  const lignes = t.lignes.map((l) => {
    const f = famille(l, t);
    return `<tr>
      <td class="c-case"><span class="pastille" style="background:${COULEUR[f]}"></span></td>
      <td class="c-vin"><span class="app">${esc(l.appellation)}</span>
        ${l.cuvee ? `<span class="cuv">${esc(l.cuvee)}</span>` : ''}</td>
      <td class="c-detail">${esc(l.millesime || '—')}</td>
      <td class="c-detail">${esc(l.contenance || '—')}</td>
      <td class="c-bloc"><div class="bloc-prix">
        ${l.prix_centimes.map((p) => `<div class="cel-prix">${euros(p)}<span>€</span></div>`).join('')}
      </div></td></tr>`;
  }).join('');
  return `<table class="tarif">
    <colgroup><col style="width:7mm"><col><col style="width:15mm"><col style="width:14mm"><col style="width:50mm"></colgroup>
    <thead><tr><th colspan="4" class="intit">${esc(t.intitule)}${t.famille ? ' · ' + esc(t.famille) : ''}</th>
      <th class="c-bloc"><div class="bloc-prix entete">${paliers}</div></th></tr></thead>
    <tbody>${lignes}</tbody></table>`;
}

export function construire() {
  const d = domaine();
  const styles = `
body { background: ${C.caisse}; color: ${C.encre};
  font-family: 'Literata', serif; font-size: 9.5pt; line-height: 1.45; }
.motif { width: 100%; height: 100%; display: block; }
.gauche { min-height: 0; }

/* ——— couverture : une caisse de douze ——— */
.gauche { background: ${C.caisse}; padding: 16mm 16mm 14mm; display: flex; flex-direction: column; }
.titre-couv { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 40pt;
  line-height: .94; letter-spacing: -.028em; color: ${C.violet}; margin-bottom: 2.5mm; }
.titre-couv em { font-style: normal; color: ${C.folies}; }
.sous-couv { font-size: 10pt; line-height: 1.45; color: rgba(33,30,28,.78); margin-bottom: 6mm;
  max-width: 125mm; }
.caisse-couv { display: grid; grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(4, 1fr); gap: 2.5mm; flex: 1 1 0; min-height: 0;
  margin-bottom: 7mm; }
.case { overflow: hidden; border-radius: 1.5mm; min-height: 0;
  box-shadow: inset 0 0 0 .35mm rgba(33,30,28,.12); }
.bas-couv { display: flex; align-items: flex-end; justify-content: space-between; gap: 6mm; }
.bas-couv img { width: 58mm; display: block; }
.bas-couv .droite-bas { text-align: right; }
.bas-couv .cible { font: 600 8.5pt 'Hanken Grotesk', sans-serif; letter-spacing: .08em;
  text-transform: uppercase; display: block; color: rgba(33,30,28,.8); margin-bottom: .5mm; }
.bas-couv .annee { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 30pt;
  line-height: 1; color: ${C.violet}; display: block; letter-spacing: -.03em; }

/* ——— fiche domaine ——— */
.droite { background: ${C.caisse}; padding: 15mm 16mm 13mm; display: flex; flex-direction: column; }
.entete-dom { display: flex; gap: 6mm; align-items: flex-start; margin-bottom: 4mm; }
.bloc-caisse { flex: none; width: 62mm; }
.caisse-dom { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1.1mm; }
.case-dom { aspect-ratio: 1; border-radius: .8mm; }
.caisse-leg { margin-top: 2mm; display: flex; flex-wrap: wrap; gap: .8mm 3mm;
  font: 500 6.6pt 'Hanken Grotesk', sans-serif; color: rgba(33,30,28,.72); }
.caisse-leg span { display: inline-flex; align-items: center; gap: 1.1mm; }
.caisse-leg i { width: 2.2mm; height: 2.2mm; border-radius: .4mm; display: inline-block; }
.titre-dom { flex: 1; }
.titre-dom .ligne { display: flex; align-items: baseline; gap: 3mm; }
.num { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700; font-size: 26pt;
  line-height: 1; color: ${C.or}; letter-spacing: -.04em; }
.titre-dom h1 { font-family: 'Bricolage Grotesque', sans-serif; font-weight: 600; font-size: 21pt;
  line-height: 1.04; color: ${C.violet}; letter-spacing: -.022em; }
.region { font: 600 8pt 'Hanken Grotesk', sans-serif; letter-spacing: .16em; text-transform: uppercase;
  color: ${C.folies}; margin-top: 1.5mm; }
.identite { display: flex; flex-wrap: wrap; gap: 1.6mm; margin-top: 3mm; }
.jeton { font: 600 7.4pt 'Hanken Grotesk', sans-serif; border-radius: 1mm; padding: 1mm 2.4mm;
  background: ${C.violet}; color: ${C.caisse}; }
.jeton.bio { background: ${C.jardin}; }
.jeton.clair { background: rgba(33,30,28,.09); color: ${C.encre}; }
.texte { font-size: 9.5pt; line-height: 1.5; margin-bottom: 5mm; }
.texte .lettrine { float: left; font-family: 'Bricolage Grotesque', sans-serif; font-weight: 700;
  font-size: 27pt; line-height: .8; padding: 1.4mm 1.8mm 0 0; color: ${C.folies}; }

table.tarif { width: 100%; border-collapse: collapse; table-layout: fixed;
  font-family: 'Hanken Grotesk', sans-serif; font-variant-numeric: tabular-nums; }
.intit { text-align: left; font: 600 7.4pt 'Hanken Grotesk', sans-serif; letter-spacing: .14em;
  text-transform: uppercase; color: rgba(33,30,28,.55); padding: 0 0 1.4mm; vertical-align: bottom; }
th.c-bloc { vertical-align: bottom; padding: 0; }
.c-bloc { width: 50mm; padding: 0; }
.bloc-prix { display: flex; }
.bloc-prix > * { flex: 1 1 0; text-align: right; padding: 1.15mm 2mm 1.15mm 1mm;
  font-size: 9pt; font-weight: 600; color: ${C.encre}; }
.bloc-prix .cel-prix span { font-size: 6.6pt; font-weight: 500; margin-left: .5mm; opacity: .62; }
.bloc-prix.entete .cel-pal { font-size: 6.5pt; font-weight: 600; line-height: 1.14;
  color: ${C.caisse}; background: ${C.violet}; margin-left: .6mm; padding: 1.8mm 1.8mm;
  border-radius: 1mm 1mm 0 0; }
.bloc-prix.entete .cel-pal:first-child { margin-left: 0; }
tbody tr { border-bottom: .3pt solid rgba(33,30,28,.16); }
td { padding: 1.1mm 1.4mm; vertical-align: middle; }
.c-case { width: 7mm; }
.pastille { width: 3.4mm; height: 3.4mm; border-radius: .6mm; display: block; }
.c-vin .app { display: block; font-size: 7.2pt; color: rgba(33,30,28,.58); }
.c-vin .cuv { display: block; font-size: 8.6pt; font-weight: 600; }
.c-detail { font-size: 7.2pt; color: rgba(33,30,28,.66); white-space: nowrap; text-align: right;
  padding-right: 2.5mm; }
.bande-panachage { margin-top: 4mm; background: ${C.or}; border-radius: 1.5mm;
  padding: 2.6mm 3.5mm; display: flex; justify-content: space-between; gap: 5mm; align-items: center;
  font: 600 7.8pt 'Hanken Grotesk', sans-serif; color: ${C.encre}; }
.bande-panachage em { font-style: normal; font-weight: 500; }
.pied { margin-top: 3mm; display: flex; justify-content: space-between; gap: 4mm;
  font: 500 7.2pt 'Hanken Grotesk', sans-serif; color: rgba(33,30,28,.78); }
.pied strong { color: ${C.violet}; font-weight: 700; }
.legende { margin-top: 2.4mm; display: flex; flex-wrap: wrap; gap: 1.2mm 3.5mm; align-items: center;
  font: 500 6.6pt 'Hanken Grotesk', sans-serif; color: rgba(33,30,28,.68); }
.legende span { display: inline-flex; align-items: center; gap: 1.2mm; }
.legende i { width: 2.4mm; height: 2.4mm; border-radius: .5mm; display: inline-block; }
`;

  const leg = (f) => `<span><i style="background:${COULEUR[f]}"></i>${NOM_FAMILLE[f]}</span>`;
  const gauche = `
    <h1 class="titre-couv">La caisse<br><em>panachée</em></h1>
    <p class="sous-couv">Quarante domaines, dix régions, et le droit de mélanger.
      Une caisse de douze cases : c'est le module de tout le catalogue.</p>
    ${caisseCouverture()}
    <div class="bas-couv">
      <img src="../src/images/logo-agence-scio-detoure.png" alt="Agence SCIO Vins &amp; Spirits">
      <div class="droite-bas">
        <span class="cible">Tarifs cavistes Vendée (85)</span>
        <span class="annee">2026</span>
      </div>
    </div>`;

  const texte = esc(d.texte_source);
  const droite = `
    <div class="entete-dom">
      <div class="bloc-caisse">${caisseDomaine(d)}</div>
      <div class="titre-dom">
        <div class="ligne"><span class="num">${d.numero}</span><h1>${esc(d.nom)}</h1></div>
        <div class="region">${esc(d.region)}</div>
        <div class="identite">
          ${d.labels.map((l) => `<span class="jeton bio">${esc(l.label)}</span>`).join('')}
          ${d.allocation ? '<span class="jeton">Allocation</span>' : ''}
          <span class="jeton clair">${nbReferences(d)} références</span>
        </div>
      </div>
    </div>
    <div class="texte"><span class="lettrine">${texte.slice(0, 1)}</span>${texte.slice(1)}</div>
    ${d.tableaux.map(tableau).join('')}
    <div class="bande-panachage">
      <span>PANACHER · <em>toute la gamme du domaine</em></span>
      <span><em>paliers</em> ${d.tableaux[0].paliers.join(' · ')}</span>
    </div>
    <div class="pied">
      <div>${esc(d.note_prix)}</div>
      <div><strong>Distribution</strong> ${d.departements.join(' · ')}</div>
    </div>
    <div class="legende">
      ${leg('blanc')}${leg('rouge')}${leg('rose')}${leg('bulles')}${leg('sansalcool')}${leg('spiritueux')}
    </div>`;

  return planche({ titre: 'Concept 3 — La Caisse Panachée', styles, gauche, droite });
}
