import { catalogue, domaine, euros, esc, graine, famille, REGIONS, planche } from './commun.mjs';

const C = {
  tuffeau: '#F2EADA', craie: '#FBF8F1', silex: '#46606E', gneiss: '#A8515F',
  amphibolite: '#3C5B47', sables: '#D08C3C', violet: '#67067C', or: '#E1C853',
};

/** Une couleur et une trame par région : la strate se reconnaît à l'œil et au doigt. */
const STRATES = {
  Loire:      { c: C.silex,       t: 'ecailles' },
  Alsace:     { c: C.amphibolite, t: 'veines' },
  Beaujolais: { c: C.gneiss,      t: 'grains' },
  Bourgogne:  { c: C.sables,      t: 'pointille' },
  'Rhône':    { c: C.amphibolite, t: 'galets' },
  'Sud-Ouest':{ c: C.sables,      t: 'grains' },
  Bordeaux:   { c: C.gneiss,      t: 'galets' },
  Provence:   { c: C.silex,       t: 'pointille' },
  Languedoc:  { c: C.amphibolite, t: 'ecailles' },
  Champagne:  { c: C.craie,       t: 'pointille' },
};

/** Trames dessinées : rien n'est importé d'une bibliothèque, tout est tracé ici. */
function trames() {
  const encre = 'rgba(0,0,0,.30)';
  return `<svg width="0" height="0" style="position:absolute"><defs>
  <pattern id="t-ecailles" width="14" height="9" patternUnits="userSpaceOnUse">
    <path d="M-2 9 Q5 1 12 9 M12 9 Q19 1 26 9" fill="none" stroke="${encre}" stroke-width="1.1"/></pattern>
  <pattern id="t-veines" width="26" height="14" patternUnits="userSpaceOnUse">
    <path d="M0 4 C7 1 11 9 18 6 S26 3 30 7" fill="none" stroke="${encre}" stroke-width="1"/>
    <path d="M-4 11 C3 8 7 15 14 12 S22 10 26 13" fill="none" stroke="${encre}" stroke-width=".7"/></pattern>
  <pattern id="t-grains" width="11" height="11" patternUnits="userSpaceOnUse">
    <circle cx="2.5" cy="3" r="1.5" fill="${encre}"/><circle cx="8" cy="7.5" r="1.1" fill="${encre}"/>
    <circle cx="5" cy="9.5" r=".7" fill="${encre}"/></pattern>
  <pattern id="t-pointille" width="9" height="9" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r=".9" fill="${encre}"/><circle cx="6.5" cy="6" r=".9" fill="${encre}"/></pattern>
  <pattern id="t-galets" width="22" height="14" patternUnits="userSpaceOnUse">
    <ellipse cx="6" cy="5" rx="5" ry="3.1" fill="none" stroke="${encre}" stroke-width="1"/>
    <ellipse cx="17" cy="10" rx="4.2" ry="2.6" fill="none" stroke="${encre}" stroke-width="1"/></pattern>
</defs></svg>`;
}

/** La coupe : dix strates empilées, d'épaisseur proportionnelle au nombre de domaines. */
function coupe(largeur, hauteur) {
  const r = graine(26);
  const effectifs = REGIONS.map((n) => catalogue.domaines.filter((d) => d.region === n).length);
  // Une région à un seul domaine garderait une strate illisible : on applique un plancher.
  // L'épaisseur reste proportionnelle, le chiffre exact est écrit dans la strate.
  const poids = effectifs.map((n) => Math.max(n, 2.6));
  const total = poids.reduce((a, b) => a + b, 0);
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * hauteur;
    const s = STRATES[nom];
    // Le toit de chaque strate ondule : une couche de terre n'est jamais plate.
    const pts = [];
    for (let x = 0; x <= largeur + 40; x += largeur / 7) {
      pts.push(`${x} ${y + (r() - 0.5) * 7}`);
    }
    const toit = `M-20 ${y + 12} L${pts.map((p, k) => (k ? 'L' : 'L') + p).join(' ')} L${largeur + 20} ${y + 12}`;
    const d = `M-20 ${y} ${pts.map((p) => 'L' + p).join(' ')} L${largeur + 20} ${y} L${largeur + 20} ${y + h + 2} L-20 ${y + h + 2} Z`;
    out += `<path d="${d}" fill="${s.c}"/><path d="${d}" fill="url(#t-${s.t})"/>`
         + `<text x="${largeur - 14}" y="${y + h / 2 + 4}" text-anchor="end" class="etiq-strate"
             fill="${nom === 'Champagne' ? C.silex : 'rgba(255,255,255,.92)'}">${esc(nom.toUpperCase())}</text>`
         + `<text x="14" y="${y + h / 2 + 4}" class="etiq-nb"
             fill="${nom === 'Champagne' ? C.silex : 'rgba(255,255,255,.72)'}">${effectifs[i]}</text>`;
    y += h;
  });
  return `<svg viewBox="0 0 ${largeur} ${hauteur}" preserveAspectRatio="none" class="coupe">${out}</svg>`;
}

/** La carotte : bande de tranche indexée, la strate active est pleine. */
function carotte(regionActive) {
  const effectifs = REGIONS.map((n) => catalogue.domaines.filter((d) => d.region === n).length);
  const poids = effectifs.map((n) => Math.max(n, 2.6));
  const total = poids.reduce((a, b) => a + b, 0);
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * 1000;
    const s = STRATES[nom];
    const actif = nom === regionActive;
    out += `<rect x="0" y="${y}" width="40" height="${h}" fill="${s.c}" opacity="${actif ? 1 : 0.3}"/>`
         + `<rect x="0" y="${y + h - 1}" width="40" height="1" fill="${C.tuffeau}" opacity=".7"/>`;
    if (actif) {
      out += `<rect x="0" y="${y}" width="40" height="${h}" fill="url(#t-${s.t})"/>`
           + `<rect x="0" y="${y}" width="7" height="${h}" fill="${C.or}"/>`;
    }
    y += h;
  });
  return `<svg viewBox="0 0 40 1000" preserveAspectRatio="none" class="carotte">${out}</svg>`;
}

/** Vue en coupe du sol d'un domaine : un disque de carotte, tiré du numéro du domaine. */
function carotteRonde(d) {
  const r = graine(d.numero * 7);
  const s = STRATES[d.region];
  const couches = [C.sables, s.c, C.silex, C.gneiss];
  let out = `<circle cx="60" cy="60" r="58" fill="${C.craie}" stroke="${C.silex}" stroke-width="2"/>`;
  let y = 2;
  couches.forEach((col, i) => {
    const h = 20 + r() * 18;
    out += `<path d="M2 ${y} Q30 ${y - 5 + r() * 10} 60 ${y + 2} T118 ${y} L118 ${y + h} Q90 ${y + h + 4} 60 ${y + h - 2} T2 ${y + h} Z"
             fill="${col}" opacity="${0.55 + i * 0.12}"/>`;
    y += h;
  });
  out += `<circle cx="60" cy="60" r="58" fill="url(#t-${s.t})" opacity=".5"/>`;
  out += `<circle cx="60" cy="60" r="58" fill="none" stroke="${C.silex}" stroke-width="2.5"/>`;
  return `<svg viewBox="0 0 120 120" class="rond-sol">${out}</svg>`;
}

const PICTOS = {
  blanc: `<circle cx="7" cy="7" r="5.4" fill="#FBF8F1" stroke="#46606E" stroke-width="1.2"/>`,
  rouge: `<circle cx="7" cy="7" r="5.4" fill="#A8515F"/>`,
  rose: `<path d="M7 1.6 A5.4 5.4 0 0 1 7 12.4 Z" fill="#D98FA0"/><circle cx="7" cy="7" r="5.4" fill="none" stroke="#A8515F" stroke-width="1.2"/>`,
  bulles: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#46606E" stroke-width="1.2"/><circle cx="5" cy="8" r="1.3" fill="#46606E"/><circle cx="9" cy="6.4" r="1.1" fill="#46606E"/><circle cx="7.4" cy="4.2" r=".9" fill="#46606E"/>`,
  doux: `<circle cx="7" cy="7" r="5.4" fill="#E1C853"/>`,
  sansalcool: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#3C5B47" stroke-width="1.2"/><path d="M3.6 10.4 L10.4 3.6" stroke="#3C5B47" stroke-width="1.2"/>`,
  jus: `<circle cx="7" cy="7" r="5.4" fill="#3C5B47"/>`,
  biere: `<circle cx="7" cy="7" r="5.4" fill="#D08C3C"/>`,
  spiritueux: `<rect x="2.2" y="2.2" width="9.6" height="9.6" fill="#8A6230"/>`,
  autre: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#46606E" stroke-width="1.2" stroke-dasharray="2 2"/>`,
};
const picto = (f) => `<svg viewBox="0 0 14 14" class="picto">${PICTOS[f] || PICTOS.autre}</svg>`;

function tableau(t) {
  const lignes = t.lignes.map((l) => {
    const prix = l.prix_centimes.map((p) => `<div class="cel-prix">${euros(p)}<span>€</span></div>`).join('');
    return `<tr>
      <td class="c-picto">${picto(famille(l, t))}</td>
      <td class="c-vin"><span class="app">${esc(l.appellation)}</span>
        ${l.cuvee ? `<span class="cuv">${esc(l.cuvee)}</span>` : ''}</td>
      <td class="c-detail">${esc(l.millesime || '—')}</td>
      <td class="c-detail">${esc(l.contenance || '—')}</td>
      <td class="c-bloc"><div class="bloc-prix">${prix}</div></td></tr>`;
  }).join('');
  const paliers = t.paliers.map((p) => `<div class="cel-pal">${esc(p)}</div>`).join('');
  return `<table class="tarif">
    <colgroup><col style="width:6mm"><col><col style="width:16mm"><col style="width:15mm"><col style="width:52mm"></colgroup>
    <thead><tr class="bandeau"><th colspan="4" class="intit">${esc(t.intitule)}${t.famille ? ' · ' + esc(t.famille) : ''}</th>
      <th class="c-bloc"><div class="bloc-prix entete">${paliers}</div></th></tr></thead>
    <tbody>${lignes}</tbody></table>`;
}

export function construire() {
  const d = domaine();
  const styles = `
body { background: ${C.tuffeau}; color: ${C.silex};
  font-family: 'Spectral', serif; font-size: 9.5pt; line-height: 1.42; }
.etiq-strate { font: 600 11px 'IBM Plex Sans', sans-serif; letter-spacing: .14em; }
.etiq-nb { font: 400 11px 'IBM Plex Sans', sans-serif; }

/* ——— couverture ——— */
.gauche { background: ${C.tuffeau}; }
.coupe { position: absolute; left: 0; right: 0; bottom: 0; width: 210mm; height: 148mm; }
.logo-couv { position: absolute; left: 18mm; top: 17mm; width: 62mm; }
.titre-couv { position: absolute; left: 18mm; top: 44mm; width: 170mm;
  font-family: 'Young Serif', serif; font-size: 46pt; line-height: .92;
  color: ${C.silex}; letter-spacing: -.012em; }
.titre-couv em { font-style: normal; color: ${C.violet}; }
.sous-couv { position: absolute; left: 18mm; top: 96mm; width: 120mm;
  font-size: 10.5pt; line-height: 1.5; color: ${C.silex}; opacity: .85; }
.pied-couv { position: absolute; left: 0; bottom: 14mm; padding: 5mm 7mm 4mm 18mm;
  background: ${C.tuffeau}; border-radius: 0 3mm 3mm 0; }
.pied-couv .cible { font: 500 9pt 'IBM Plex Sans', sans-serif; letter-spacing: .1em;
  text-transform: uppercase; display: block; margin-bottom: .5mm; color: ${C.silex}; }
.pied-couv .annee { font-family: 'Young Serif', serif; font-size: 34pt; line-height: 1;
  color: ${C.violet}; display: block; }

/* ——— fiche domaine ——— */
.droite { background: ${C.tuffeau}; padding: 16mm 23mm 14mm 16mm; }
.carotte { position: absolute; right: 0; top: 0; width: 9mm; height: 260mm; }
.tranche-nom { position: absolute; right: 2.2mm; top: 50%; transform: translateY(-50%) rotate(180deg);
  writing-mode: vertical-rl; font: 600 7pt 'IBM Plex Sans', sans-serif; letter-spacing: .22em;
  color: ${C.craie}; text-transform: uppercase; }
.entete { display: flex; align-items: flex-start; gap: 5mm; border-bottom: 1.6pt solid ${C.violet};
  padding-bottom: 3mm; margin-bottom: 5mm; }
.num { font-family: 'Young Serif', serif; font-size: 30pt; line-height: .8; color: ${C.violet}; }
.entete h1 { font-family: 'Young Serif', serif; font-size: 22pt; line-height: 1.02;
  font-weight: 400; color: ${C.silex}; flex: 1; letter-spacing: -.01em; }
.region { font: 500 8.5pt 'IBM Plex Sans', sans-serif; letter-spacing: .16em;
  text-transform: uppercase; color: ${C.gneiss}; padding-top: 2mm; white-space: nowrap; }
.identite { display: flex; flex-wrap: wrap; gap: 2mm 3mm; margin-bottom: 5mm; }
.jeton { font: 500 7.5pt 'IBM Plex Sans', sans-serif; letter-spacing: .04em;
  border: .8pt solid ${C.silex}; border-radius: 1mm; padding: .9mm 2.2mm; color: ${C.silex}; }
.jeton.bio { border-color: ${C.amphibolite}; color: ${C.amphibolite}; }
.jeton.alloc { background: ${C.violet}; border-color: ${C.violet}; color: ${C.craie}; }
.haut { display: flex; gap: 6mm; margin-bottom: 6mm; align-items: flex-start; }
.rond-sol { width: 34mm; height: 34mm; flex: none; }
.texte { flex: 1; font-size: 9.5pt; line-height: 1.5; }
.texte .lettrine { float: left; font-family: 'Young Serif', serif; font-size: 29pt;
  line-height: .78; padding: 1mm 1.6mm 0 0; color: ${C.violet}; }
table.tarif { width: 100%; border-collapse: collapse; font-family: 'IBM Plex Sans', sans-serif;
  font-variant-numeric: tabular-nums; }
tr.bandeau th { background: ${C.violet}; vertical-align: bottom; }
.intit { text-align: left; font: 600 7.5pt 'IBM Plex Sans', sans-serif; letter-spacing: .14em;
  text-transform: uppercase; color: ${C.or}; padding: 2mm 0 2mm 2.6mm; }
.c-bloc { width: 52mm; padding: 0; }
.bloc-prix { display: flex; }
.bloc-prix > * { flex: 1 1 0; text-align: right; padding: 1.3mm 2mm 1.3mm 1mm; font-size: 9pt;
  font-weight: 500; color: ${C.silex}; }
.bloc-prix .cel-prix span { font-size: 6.6pt; font-weight: 400; margin-left: .5mm; opacity: .75; }

.bloc-prix.entete { align-items: flex-end; }
.bloc-prix.entete .cel-pal { color: ${C.craie}; font-size: 6.6pt; font-weight: 500;
  line-height: 1.16; letter-spacing: .02em; text-align: right; padding: 2mm 2mm 2mm 1mm;
  border-left: .4pt solid rgba(251,248,241,.32); }
.bloc-prix.entete .cel-pal:first-child { border-left: 0; }
tbody tr { border-bottom: .3pt solid rgba(70,96,110,.26); }
tbody tr:nth-child(odd) { background: rgba(251,248,241,.72); }
td { padding: 1.3mm 1.4mm; vertical-align: middle; }
.c-picto { width: 6mm; padding-left: 1.6mm; }
.picto { width: 3.4mm; height: 3.4mm; display: block; }
.c-vin .app { display: block; font-size: 7.4pt; color: ${C.gneiss}; letter-spacing: .01em; }
.c-vin .cuv { display: block; font-size: 8.6pt; font-weight: 500; color: ${C.silex}; }
.c-detail { font-size: 7.4pt; color: rgba(70,96,110,.82); white-space: nowrap; text-align: right;
  padding-right: 2.5mm; }
table.tarif { table-layout: fixed; }
table.tarif + table.tarif { margin-top: 5mm; }
.pied { margin-top: 4mm; padding-top: 2.5mm; border-top: .8pt solid ${C.silex};
  display: flex; justify-content: space-between; gap: 4mm;
  font: 400 7.4pt 'IBM Plex Sans', sans-serif; color: rgba(70,96,110,.9); }
.pied strong { font-weight: 600; color: ${C.violet}; }
.legende { margin-top: 3mm; display: flex; flex-wrap: wrap; gap: 1.4mm 4mm;
  font: 400 6.8pt 'IBM Plex Sans', sans-serif; color: rgba(70,96,110,.8); align-items: center; }
.legende span { display: inline-flex; align-items: center; gap: 1.2mm; }
.legende .picto { width: 2.8mm; height: 2.8mm; }
`;

  const gauche = `
    <img class="logo-couv" src="../src/images/logo-agence-scio-detoure.png" alt="Agence SCIO Vins & Spirits">
    <h1 class="titre-couv">Sous<br>nos<br><em>pieds</em></h1>
    <p class="sous-couv">Quarante domaines, dix régions,<br>et la terre qu'ils ont sous les pieds.</p>
    ${coupe(600, 430)}
    <div class="pied-couv">
      <span class="cible">Tarifs cavistes Vendée (85)</span>
      <span class="annee">2026</span>
    </div>`;

  const texte = esc(d.texte_source);
  const droite = `
    ${carotte(d.region)}
    <div class="tranche-nom">${esc(d.region)}</div>
    <div class="entete">
      <div class="num">${d.numero}</div>
      <h1>${esc(d.nom)}</h1>
      <div class="region">${esc(d.region)}</div>
    </div>
    <div class="identite">
      ${d.labels.map((l) => `<span class="jeton bio">${esc(l.label)}</span>`).join('')}
      ${d.allocation ? '<span class="jeton alloc">Allocation</span>' : ''}
      <span class="jeton">Panachage : toute la gamme</span>
      <span class="jeton">${d.tableaux[0].paliers.length} paliers</span>
    </div>
    <div class="haut">
      ${carotteRonde(d)}
      <div class="texte"><span class="lettrine">${texte.slice(0, 1)}</span>${texte.slice(1)}</div>
    </div>
    ${d.tableaux.map(tableau).join('')}
    <div class="pied">
      <div>${esc(d.note_prix)}</div>
      <div><strong>Distribution</strong> ${d.departements.join(' · ')}</div>
    </div>
    <div class="legende">
      <span>${picto('blanc')} Blanc</span><span>${picto('rouge')} Rouge</span>
      <span>${picto('rose')} Rosé</span><span>${picto('bulles')} Bulles</span>
      <span>${picto('doux')} Doux</span><span>${picto('sansalcool')} Sans alcool</span>
      <span>${picto('spiritueux')} Spiritueux</span>
    </div>`;

  return planche({ titre: 'Concept 1 — Sous nos pieds', styles, gauche, droite, defs: trames() });
}
