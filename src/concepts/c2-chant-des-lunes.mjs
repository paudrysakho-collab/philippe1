import { catalogue, domaine, euros, esc, graine, famille, nbReferences, planche } from './commun.mjs';

const C = {
  nuit: '#232B52', lune: '#F4EEE0', cers: '#6E8E6A', arlequin: '#D1537C',
  aube: '#E2884A', violet: '#67067C', or: '#E1C853',
};

/**
 * La figure du domaine : autant de points qu'il a de références au tarif.
 * Le tracé est tiré du numéro du domaine, donc toujours le même d'une édition à l'autre.
 */
function figure(d, taille = 300, epais = 1) {
  const n = nbReferences(d);
  const r = graine(d.numero * 31 + 7);
  const pts = [];
  const marge = taille * 0.1;
  let essais = 0;
  while (pts.length < n && essais < 4000) {
    essais++;
    const x = marge + r() * (taille - 2 * marge);
    const y = marge + r() * (taille - 2 * marge);
    // On écarte les points pour que la figure respire
    if (pts.every((p) => (p.x - x) ** 2 + (p.y - y) ** 2 > (taille / (2.4 + n / 7)) ** 2)) {
      pts.push({ x, y, r: 1.6 + r() * 3.4 });
    }
  }
  // Un chemin qui relie les points de proche en proche : la figure se lit d'un trait
  const reste = pts.slice(1);
  let cour = pts[0], chemin = `M${cour.x.toFixed(1)} ${cour.y.toFixed(1)}`;
  while (reste.length) {
    let k = 0, dmin = Infinity;
    reste.forEach((p, i) => {
      const dd = (p.x - cour.x) ** 2 + (p.y - cour.y) ** 2;
      if (dd < dmin) { dmin = dd; k = i; }
    });
    cour = reste.splice(k, 1)[0];
    chemin += ` L${cour.x.toFixed(1)} ${cour.y.toFixed(1)}`;
  }
  const etoiles = pts.map((p) =>
    `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${(p.r * epais).toFixed(1)}" fill="currentColor"/>`).join('');
  return `<svg viewBox="0 0 ${taille} ${taille}" class="figure">
    <path d="${chemin}" fill="none" stroke="currentColor" stroke-width="${(0.9 * epais).toFixed(2)}" opacity=".55"/>
    ${etoiles}</svg>`;
}

/** Le ciel de couverture : les quarante figures, à leur juste taille, sans jamais se toucher. */
function ciel() {
  const r = graine(2026);
  const cases = [];
  const cols = 5, rangs = 8;
  for (let i = 0; i < cols * rangs; i++) cases.push(i);
  // mélange déterministe
  for (let i = cases.length - 1; i > 0; i--) {
    const j = Math.floor(r() * (i + 1));
    [cases[i], cases[j]] = [cases[j], cases[i]];
  }
  return catalogue.domaines.map((d, i) => {
    const c = cases[i];
    const x = (c % cols) / cols * 100 + (r() * 6 - 3);
    const y = Math.floor(c / cols) / rangs * 100 + (r() * 4 - 2);
    const t = 11 + Math.min(nbReferences(d), 20) * 0.5;
    return `<div class="astre" style="left:${x.toFixed(2)}%;top:${y.toFixed(2)}%;width:${t.toFixed(1)}mm">
      ${figure(d, 300, 1.5)}</div>`;
  }).join('');
}

const PICTOS = {
  blanc: `<circle cx="7" cy="7" r="5.2" fill="none" stroke="#232B52" stroke-width="1.3"/>`,
  rouge: `<circle cx="7" cy="7" r="5.2" fill="#8E2F3E"/>`,
  rose: `<circle cx="7" cy="7" r="5.2" fill="#D1537C"/>`,
  bulles: `<circle cx="7" cy="7" r="5.2" fill="none" stroke="#232B52" stroke-width="1.1"/><circle cx="7" cy="7" r="2.2" fill="#232B52"/>`,
  doux: `<circle cx="7" cy="7" r="5.2" fill="#E1C853"/>`,
  sansalcool: `<path d="M7 1.8 A5.2 5.2 0 0 0 7 12.2 Z" fill="#6E8E6A"/><circle cx="7" cy="7" r="5.2" fill="none" stroke="#6E8E6A" stroke-width="1.2"/>`,
  jus: `<circle cx="7" cy="7" r="5.2" fill="#6E8E6A"/>`,
  biere: `<circle cx="7" cy="7" r="5.2" fill="#E2884A"/>`,
  spiritueux: `<circle cx="7" cy="7" r="5.2" fill="#67067C"/>`,
  autre: `<circle cx="7" cy="7" r="5.2" fill="none" stroke="#232B52" stroke-width="1" stroke-dasharray="2 2"/>`,
};
const picto = (f) => `<svg viewBox="0 0 14 14" class="picto">${PICTOS[f] || PICTOS.autre}</svg>`;

function tableau(t) {
  const paliers = t.paliers.map((p) => `<div class="cel-pal">${esc(p)}</div>`).join('');
  const lignes = t.lignes.map((l) => `<tr>
      <td class="c-picto">${picto(famille(l, t))}</td>
      <td class="c-vin"><span class="app">${esc(l.appellation)}</span>
        ${l.cuvee ? `<span class="cuv">${esc(l.cuvee)}</span>` : ''}</td>
      <td class="c-detail">${esc(l.millesime || '—')}</td>
      <td class="c-detail">${esc(l.contenance || '—')}</td>
      <td class="c-bloc"><div class="bloc-prix">
        ${l.prix_centimes.map((p) => `<div class="cel-prix">${euros(p)}<span>€</span></div>`).join('')}
      </div></td></tr>`).join('');
  return `<table class="tarif">
    <colgroup><col style="width:6mm"><col><col style="width:16mm"><col style="width:15mm"><col style="width:50mm"></colgroup>
    <thead><tr><th colspan="4" class="intit">${esc(t.intitule)}${t.famille ? ' · ' + esc(t.famille) : ''}</th>
      <th class="c-bloc"><div class="bloc-prix entete">${paliers}</div></th></tr></thead>
    <tbody>${lignes}</tbody></table>`;
}

export function construire() {
  const d = domaine();
  const styles = `
body { color: ${C.nuit}; font-family: 'Faustina', serif; font-size: 9.5pt; line-height: 1.45; }

/* ——— couverture : la nuit ——— */
.gauche { background: ${C.nuit}; color: ${C.lune}; }
.ciel { position: absolute; inset: 0; }
.astre { position: absolute; color: rgba(244,238,224,.62); }
.astre .figure { width: 100%; height: auto; display: block; }
.voile { position: absolute; left: 0; right: 0; bottom: 0; height: 132mm;
  background: linear-gradient(to bottom, rgba(35,43,82,0) 0%, rgba(35,43,82,.86) 32%, ${C.nuit} 62%); }
.lune-couv { position: absolute; right: -22mm; top: 18mm; width: 86mm; height: 86mm;
  border-radius: 50%; background: radial-gradient(circle at 34% 34%, #FFF8E6 0%, ${C.or} 58%, #C2A63F 100%);
  opacity: .92; }
.titre-couv { position: absolute; left: 18mm; bottom: 92mm; width: 150mm;
  font-family: 'Fraunces', serif; font-weight: 400; font-size: 44pt; line-height: .96;
  color: ${C.lune}; letter-spacing: -.012em; }
.titre-couv em { font-style: italic; color: ${C.or}; }
.sous-couv { position: absolute; left: 18mm; bottom: 72mm; width: 128mm;
  font-size: 10.5pt; line-height: 1.5; color: rgba(244,238,224,.82); }
.reserve-logo { position: absolute; left: 18mm; bottom: 20mm; background: #FFFFFF;
  border-radius: 1.5mm; padding: 6mm 7mm; }
.reserve-logo img { width: 58mm; display: block; }
.pied-couv { position: absolute; right: 18mm; bottom: 20mm; text-align: right; }
.pied-couv .cible { font: 500 9pt 'Archivo', sans-serif; letter-spacing: .1em;
  text-transform: uppercase; display: block; color: rgba(244,238,224,.9); margin-bottom: 1mm; }
.pied-couv .annee { font-family: 'Fraunces', serif; font-size: 34pt; line-height: 1;
  color: ${C.or}; display: block; }

/* ——— fiche domaine : la ligne d'horizon ——— */
.droite { background: ${C.lune}; }
.au-dessus { position: absolute; left: 0; right: 0; top: 0; height: 97mm;
  padding: 15mm 18mm 0; overflow: hidden; }
.horizon { position: absolute; left: 0; right: 0; top: 97mm; height: 0;
  border-top: 1.2pt solid ${C.nuit}; }
.horizon::after { content: ''; position: absolute; left: 18mm; top: -1.6mm; width: 3.2mm; height: 3.2mm;
  border-radius: 50%; background: ${C.or}; }
.au-dessous { position: absolute; left: 0; right: 0; top: 97mm; bottom: 0; padding: 6mm 18mm 11mm; }
.fig-domaine { position: absolute; right: 10mm; top: 7mm; width: 68mm; color: ${C.violet}; opacity: .92; }
.fig-domaine svg { width: 100%; height: auto; display: block; }
.fig-legende { position: absolute; right: 10mm; top: 78mm; width: 68mm; text-align: center;
  font: 500 7pt 'Archivo', sans-serif; letter-spacing: .1em; text-transform: uppercase;
  color: rgba(35,43,82,.6); }
.entete { display: flex; align-items: baseline; gap: 4mm; margin-bottom: 1.5mm; max-width: 100mm; }
.num { font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; color: ${C.arlequin}; line-height: 1; }
.entete h1 { font-family: 'Fraunces', serif; font-weight: 400; font-size: 23pt; line-height: 1.02;
  color: ${C.nuit}; letter-spacing: -.012em; }
.region { font: 500 8pt 'Archivo', sans-serif; letter-spacing: .18em; text-transform: uppercase;
  color: ${C.cers}; margin-bottom: 4mm; }
.identite { display: flex; flex-wrap: wrap; gap: 2mm; margin-bottom: 4mm; max-width: 104mm; }
.jeton { font: 500 7.5pt 'Archivo', sans-serif; border-radius: 6mm; padding: 1mm 2.6mm;
  background: rgba(35,43,82,.07); color: ${C.nuit}; }
.jeton.bio { background: rgba(110,142,106,.18); color: #41603E; }
.jeton.alloc { background: ${C.arlequin}; color: ${C.lune}; }
.texte { max-width: 104mm; font-size: 9.5pt; line-height: 1.5; }
.texte .lettrine { float: left; font-family: 'Fraunces', serif; font-weight: 400; font-size: 30pt;
  line-height: .78; padding: 1.2mm 1.8mm 0 0; color: ${C.arlequin}; }

table.tarif { width: 100%; border-collapse: collapse; table-layout: fixed;
  font-family: 'Archivo', sans-serif; font-variant-numeric: tabular-nums; }
.intit { text-align: left; font: 600 7.4pt 'Archivo', sans-serif; letter-spacing: .16em;
  text-transform: uppercase; color: ${C.cers}; padding: 0 0 1.6mm; vertical-align: bottom; }
th.c-bloc { vertical-align: bottom; padding: 0; }
.c-bloc { width: 50mm; padding: 0; }
.bloc-prix { display: flex; }
.bloc-prix > * { flex: 1 1 0; text-align: right; padding: 1.25mm 2mm 1.25mm 1mm;
  font-size: 9pt; font-weight: 500; color: ${C.nuit}; }
.bloc-prix .cel-prix span { font-size: 6.6pt; font-weight: 400; margin-left: .5mm; opacity: .7; }
.bloc-prix.entete .cel-pal { font-size: 6.6pt; font-weight: 500; line-height: 1.15;
  color: rgba(35,43,82,.72); border-bottom: 1.1pt solid ${C.nuit}; padding-bottom: 1.4mm; }
tbody tr { border-bottom: .3pt solid rgba(35,43,82,.18); }
td { padding: 1.05mm 1.4mm; vertical-align: middle; }
.c-picto { width: 6mm; }
.picto { width: 3.3mm; height: 3.3mm; display: block; }
.c-vin .app { display: block; font-size: 7.3pt; color: rgba(35,43,82,.62); }
.c-vin .cuv { display: block; font-size: 8.6pt; font-weight: 500; }
.c-detail { font-size: 7.3pt; color: rgba(35,43,82,.7); white-space: nowrap; text-align: right;
  padding-right: 2.5mm; }
.pied { margin-top: 3mm; padding-top: 2.2mm; border-top: .8pt solid ${C.nuit};
  display: flex; justify-content: space-between; gap: 4mm;
  font: 400 7.3pt 'Archivo', sans-serif; color: rgba(35,43,82,.85); }
.pied strong { color: ${C.arlequin}; font-weight: 600; }
.legende { margin-top: 2.2mm; display: flex; flex-wrap: wrap; gap: 1.2mm 4mm; align-items: center;
  font: 400 6.7pt 'Archivo', sans-serif; color: rgba(35,43,82,.7); }
.legende span { display: inline-flex; align-items: center; gap: 1.2mm; }
.legende .picto { width: 2.7mm; height: 2.7mm; }
`;

  const gauche = `
    <div class="ciel">${ciel()}</div>
    <div class="lune-couv"></div>
    <div class="voile"></div>
    <h1 class="titre-couv">Le chant<br>des <em>lunes</em></h1>
    <p class="sous-couv">Quarante domaines, quarante petites figures d'étoiles.<br>
      Au-dessus de la ligne, le monde ; en dessous, le prix.</p>
    <div class="reserve-logo"><img src="../src/images/logo-agence-scio-srgb.png" alt="Agence SCIO Vins &amp; Spirits"></div>
    <div class="pied-couv"><span class="cible">Tarifs cavistes Vendée (85)</span><span class="annee">2026</span></div>`;

  const texte = esc(d.texte_source);
  const droite = `
    <div class="au-dessus">
      <div class="fig-domaine">${figure(d, 300, 1)}</div>
      <div class="fig-legende">${nbReferences(d)} références</div>
      <div class="entete"><span class="num">${d.numero}</span><h1>${esc(d.nom)}</h1></div>
      <div class="region">${esc(d.region)}</div>
      <div class="identite">
        ${d.labels.map((l) => `<span class="jeton bio">${esc(l.label)}</span>`).join('')}
        ${d.allocation ? '<span class="jeton alloc">Allocation</span>' : ''}
        <span class="jeton">Panachage : toute la gamme</span>
      </div>
      <div class="texte"><span class="lettrine">${texte.slice(0, 1)}</span>${texte.slice(1)}</div>
    </div>
    <div class="horizon"></div>
    <div class="au-dessous">
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
      </div>
    </div>`;

  return planche({ titre: 'Concept 2 — Le Chant des Lunes', styles, gauche, droite });
}
