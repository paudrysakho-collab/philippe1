/* Les pièces du système : strates, trames, carotte, pictos, tableau de prix.
   Tout est dessiné ici. Aucune bibliothèque d'icônes. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const catalogue = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/catalogue.json'), 'utf8'));

/** Les photos retenues, par domaine. Un domaine sans photo garde son dessin de sol. */
const _photos = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/photos-preparees.json'), 'utf8'));
export const photos = _photos.reduce((m, p) => {
  (m[p.numero] ||= {})[p.role] = p;
  return m;
}, {});
export const photoDe = (d, role) => photos[d.numero]?.[role] || null;
export const REGIONS = catalogue.agence.regions;

export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
export const euros = (c) => (c / 100).toFixed(2).replace('.', ',');

/** Générateur à graine fixe : un même numéro donne toujours le même dessin. */
export function graine(n) {
  let a = (n * 0x9e3779b1) >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Une couleur et une trame par région. */
export const STRATES = {
  Loire:       { c: 'var(--silex)',       hex: '#46606E', t: 'ecailles',  mot: 'schistes et tuffeau' },
  Alsace:      { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'veines',    mot: 'coteaux du Bruderthal' },
  Beaujolais:  { c: 'var(--gneiss)',      hex: '#A8515F', t: 'grains',    mot: 'le Clos des Nugues' },
  Bourgogne:   { c: 'var(--sables)',      hex: '#D08C3C', t: 'pointille', mot: 'climats et terrasses' },
  'Rhône':     { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'galets',    mot: 'sables, grès et Trias' },
  'Sud-Ouest': { c: 'var(--sables)',      hex: '#D08C3C', t: 'grains',    mot: 'sables fauves et fossiles marins' },
  Bordeaux:    { c: 'var(--gneiss)',      hex: '#A8515F', t: 'galets',    mot: 'graves et argilo-calcaire' },
  Provence:    { c: 'var(--silex)',       hex: '#46606E', t: 'pointille', mot: 'la Provence Verte' },
  Languedoc:   { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'ecailles',  mot: 'terrasses et garrigue' },
  Champagne:   { c: 'var(--craie)',       hex: '#FBF8F1', t: 'pointille', mot: 'la craie' },
};

/** Trames dessinées, déclarées une fois par document. */
export function defsTrames() {
  const e = 'rgba(0,0,0,.30)';
  return `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <pattern id="t-ecailles" width="14" height="9" patternUnits="userSpaceOnUse">
    <path d="M-2 9 Q5 1 12 9 M12 9 Q19 1 26 9" fill="none" stroke="${e}" stroke-width="1.1"/></pattern>
  <pattern id="t-veines" width="26" height="14" patternUnits="userSpaceOnUse">
    <path d="M0 4 C7 1 11 9 18 6 S26 3 30 7" fill="none" stroke="${e}" stroke-width="1"/>
    <path d="M-4 11 C3 8 7 15 14 12 S22 10 26 13" fill="none" stroke="${e}" stroke-width=".7"/></pattern>
  <pattern id="t-grains" width="11" height="11" patternUnits="userSpaceOnUse">
    <circle cx="2.5" cy="3" r="1.5" fill="${e}"/><circle cx="8" cy="7.5" r="1.1" fill="${e}"/>
    <circle cx="5" cy="9.5" r=".7" fill="${e}"/></pattern>
  <pattern id="t-pointille" width="9" height="9" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r=".9" fill="${e}"/><circle cx="6.5" cy="6" r=".9" fill="${e}"/></pattern>
  <pattern id="t-galets" width="22" height="14" patternUnits="userSpaceOnUse">
    <ellipse cx="6" cy="5" rx="5" ry="3.1" fill="none" stroke="${e}" stroke-width="1"/>
    <ellipse cx="17" cy="10" rx="4.2" ry="2.6" fill="none" stroke="${e}" stroke-width="1"/></pattern>
</defs></svg>`;
}

export const effectifs = () =>
  REGIONS.map((n) => catalogue.domaines.filter((d) => d.region === n).length);

/** Épaisseurs des strates : proportionnelles, avec un plancher pour rester lisibles. */
export function poidsStrates() {
  const e = effectifs();
  const p = e.map((n) => Math.max(n, 2.6));
  const total = p.reduce((a, b) => a + b, 0);
  return { effectifs: e, poids: p, total };
}

/** La coupe : dix strates empilées, le toit de chacune ondule. */
export function coupe({ largeur = 600, hauteur = 430, graineN = 26, etiquettes = true } = {}) {
  const r = graine(graineN);
  const { effectifs: eff, poids, total } = poidsStrates();
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * hauteur;
    const s = STRATES[nom];
    const pts = [];
    for (let x = 0; x <= largeur + 40; x += largeur / 7) pts.push(`${x} ${(y + (r() - 0.5) * 7).toFixed(1)}`);
    const d = `M-20 ${y.toFixed(1)} ${pts.map((p) => 'L' + p).join(' ')} L${largeur + 20} ${y.toFixed(1)} `
            + `L${largeur + 20} ${(y + h + 2).toFixed(1)} L-20 ${(y + h + 2).toFixed(1)} Z`;
    const clair = nom === 'Champagne';
    out += `<path d="${d}" fill="${s.hex}"/><path d="${d}" fill="url(#t-${s.t})"/>`;
    if (etiquettes) {
      out += `<text x="${largeur - 14}" y="${(y + h / 2 + 4).toFixed(1)}" text-anchor="end"
                class="etiq-strate" fill="${clair ? '#46606E' : 'rgba(255,255,255,.93)'}">${esc(nom.toUpperCase())}</text>`
           + `<text x="14" y="${(y + h / 2 + 4).toFixed(1)}" class="etiq-nb"
                fill="${clair ? '#46606E' : 'rgba(255,255,255,.72)'}">${eff[i]}</text>`;
    }
    y += h;
  });
  return `<svg viewBox="0 0 ${largeur} ${hauteur}" preserveAspectRatio="none" class="coupe"
            aria-hidden="true">${out}</svg>`;
}

/** La carotte de tranche : la strate de la région courante est pleine, repérée en or. */
export function carotte(regionActive) {
  const { poids, total } = poidsStrates();
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * 1000;
    const s = STRATES[nom];
    const actif = nom === regionActive;
    out += `<rect x="0" y="${y.toFixed(1)}" width="40" height="${h.toFixed(1)}" fill="${s.hex}"
              opacity="${actif ? 1 : 0.3}"/>`;
    if (actif) {
      out += `<rect x="0" y="${y.toFixed(1)}" width="40" height="${h.toFixed(1)}" fill="url(#t-${s.t})"/>`
           + `<rect x="0" y="${y.toFixed(1)}" width="7" height="${h.toFixed(1)}" fill="#E1C853"/>`;
    }
    out += `<rect x="0" y="${(y + h - 1).toFixed(1)}" width="40" height="1" fill="#F2EADA" opacity=".7"/>`;
    y += h;
  });
  return `<svg viewBox="0 0 40 1000" preserveAspectRatio="none" aria-hidden="true">${out}</svg>`;
}

/** Vue en coupe du sol d'un domaine : un disque de carotte, tiré de son numéro. */
export function carotteRonde(d, taille = 120) {
  const r = graine(d.numero * 7);
  const s = STRATES[d.region];
  const couches = ['#D08C3C', s.hex, '#46606E', '#A8515F'];
  let out = `<circle cx="60" cy="60" r="58" fill="#FBF8F1"/>`;
  let y = 2;
  couches.forEach((col, i) => {
    const h = 20 + r() * 18;
    out += `<path d="M2 ${y.toFixed(1)} Q30 ${(y - 5 + r() * 10).toFixed(1)} 60 ${(y + 2).toFixed(1)}
              T118 ${y.toFixed(1)} L118 ${(y + h).toFixed(1)} Q90 ${(y + h + 4).toFixed(1)} 60 ${(y + h - 2).toFixed(1)}
              T2 ${(y + h).toFixed(1)} Z" fill="${col}" opacity="${(0.55 + i * 0.12).toFixed(2)}"/>`;
    y += h;
  });
  out += `<circle cx="60" cy="60" r="58" fill="url(#t-${s.t})" opacity=".5"/>`
       + `<circle cx="60" cy="60" r="58" fill="none" stroke="#46606E" stroke-width="2.5"/>`;
  return `<svg viewBox="0 0 120 120" class="rond-sol" aria-hidden="true">${out}</svg>`;
}

/* ——— Pictos maison. Ils ne reprennent la forme d'aucun logo officiel. ——— */
export const PICTOS = {
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
export const NOM_FAMILLE = {
  blanc: 'Blanc', rouge: 'Rouge', rose: 'Rosé', bulles: 'Bulles', doux: 'Doux',
  sansalcool: 'Sans alcool', jus: 'Jus de cépages', biere: 'Bière', spiritueux: 'Spiritueux', autre: 'Autre',
};
export const picto = (f, cls = 'picto') =>
  `<svg viewBox="0 0 14 14" class="${cls}" aria-hidden="true">${PICTOS[f] || PICTOS.autre}</svg>`;

/** Famille d'une ligne : lue dans la source, jamais devinée au-delà de ce qu'elle écrit. */
export function famille(ligne, tableau) {
  const f = (tableau.famille || '').toLowerCase();
  if (f.includes('jus')) return 'jus';
  if (f.includes('bière')) return 'biere';
  if (f.includes('armagnac') || f.includes('ratafia')) return 'spiritueux';
  const c = (ligne.couleur || '').toLowerCase();
  const a = (ligne.appellation || '').toLowerCase();
  if (a.includes('sans alcool')) return 'sansalcool';
  if (a.includes('armagnac') || a.includes('ratafia')) return 'spiritueux';
  if (c.includes('bulle') || c.includes('pétillant') || c.includes('brut') || c.includes('champagne')
      || a.includes('champagne') || a.includes('crémant') || a.includes('méthode')) return 'bulles';
  if (c.includes('doux') || c.includes('moelleux') || c.includes('liquoreux') || c.includes('demi-sec')) return 'doux';
  if (c.includes('ros') || c.includes('clairet')) return 'rose';
  if (c.includes('rouge')) return 'rouge';
  if (c.includes('blanc')) return 'blanc';
  return 'autre';
}

export const nbReferences = (d) => d.tableaux.reduce((n, t) => n + t.lignes.length, 0);

/** Les familles présentes dans un domaine, dans l'ordre de la légende. */
export function famillesDe(d) {
  const ordre = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux', 'autre'];
  const vues = new Set();
  d.tableaux.forEach((t) => t.lignes.forEach((l) => vues.add(famille(l, t))));
  return ordre.filter((f) => vues.has(f));
}

/** Une ligne de tableau. `idx` sert au repérage lors de la passe de mesure. */
export function ligneHtml(l, t, cle) {
  const prix = l.prix_centimes.map((p) => `<div class="cel-prix">${euros(p)}<span>€</span></div>`).join('');
  const etoile = l.note === '*' ? ' <span class="etoile">*</span>' : '';
  return `<tr data-ligne="${cle}">
    <td class="c-picto">${picto(famille(l, t))}</td>
    <td class="c-vin"><span class="app">${esc(l.appellation)}${etoile}</span>
      ${l.cuvee ? `<span class="cuv">${esc(l.cuvee)}</span>` : ''}</td>
    <td class="c-detail">${esc(l.millesime || '—')}</td>
    <td class="c-detail">${esc(l.contenance || '—')}</td>
    <td class="c-bloc"><div class="bloc-prix">${prix}</div></td></tr>`;
}

/** Un tableau, ou une tranche de tableau quand il se poursuit sur la page suivante. */
export function tableauHtml(t, lignes, { suite = false, cleTableau = '' } = {}) {
  const paliers = t.paliers.map((p) => `<div class="cel-pal">${esc(p)}</div>`).join('');
  const titre = esc(t.intitule) + (t.famille ? ' · ' + esc(t.famille) : '') + (suite ? ' (suite)' : '');
  return `<table class="tarif" data-tableau="${cleTableau}">
    <colgroup><col style="width:6mm"><col><col style="width:15mm"><col style="width:14mm">
      <col style="width:var(--bloc-prix)"></colgroup>
    <thead><tr class="bandeau"><th colspan="4" class="intit">${titre}</th>
      <th class="c-bloc"><div class="bloc-prix entete">${paliers}</div></th></tr></thead>
    <tbody>${lignes.map((l) => ligneHtml(l.l, t, l.cle)).join('')}</tbody></table>`;
}

/** Légende des pictos, limitée aux familles réellement présentes. */
export function legendeHtml(familles) {
  return `<div class="legende">${familles.map((f) =>
    `<span>${picto(f)} ${esc(NOM_FAMILLE[f])}</span>`).join('')}
    <span class="legende-note">pictos de l'Agence SCIO, pas les logos officiels</span></div>`;
}

/** Les groupes de panachage entre domaines. */
export const groupes = catalogue.agence.groupes_panachage;
export const groupeDe = (d) => groupes.find((g) => g.id === d.panachage_groupe) || null;
