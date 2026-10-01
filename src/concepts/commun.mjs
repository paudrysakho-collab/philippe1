import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
export const catalogue = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/catalogue.json'), 'utf8'));

/** Le domaine servant de fiche témoin aux trois maquettes. */
export const TEMOIN = 26;
export const domaine = (n = TEMOIN) => catalogue.domaines.find((d) => d.numero === n);

export const euros = (c) => (c / 100).toFixed(2).replace('.', ',');
export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

/** Générateur pseudo-aléatoire à graine fixe : un même numéro donne toujours le même dessin. */
export function graine(n) {
  let a = (n * 0x9e3779b1) >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Nombre total de références au tarif d'un domaine (toutes familles confondues). */
export const nbReferences = (d) => d.tableaux.reduce((n, t) => n + t.lignes.length, 0);

/** Famille de couleur d'une ligne, pour les pictos. Lue dans la source, jamais devinée. */
export function famille(ligne, tableau) {
  const f = (tableau.famille || '').toLowerCase();
  if (f.includes('jus')) return 'jus';
  if (f.includes('bière')) return 'biere';
  if (f.includes('armagnac') || f.includes('ratafia')) return 'spiritueux';
  const c = (ligne.couleur || '').toLowerCase();
  const a = (ligne.appellation || '').toLowerCase();
  if (a.includes('sans alcool')) return 'sansalcool';
  if (c.includes('bulle') || c.includes('pétillant') || c.includes('brut') || c.includes('champagne')
      || a.includes('champagne') || a.includes('crémant') || a.includes('méthode')) return 'bulles';
  if (c.includes('doux') || c.includes('moelleux') || c.includes('liquoreux') || c.includes('demi-sec')) return 'doux';
  if (c.includes('ros') || c.includes('clairet')) return 'rose';
  if (c.includes('rouge')) return 'rouge';
  if (c.includes('blanc')) return 'blanc';
  return 'autre';
}

export const REGIONS = catalogue.agence.regions;

/** Enveloppe HTML commune : page de 210 × 260 mm, planche de deux pages côte à côte. */
export function planche({ titre, styles, gauche, droite, defs = '' }) {
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>${esc(titre)}</title>
<link rel="stylesheet" href="../src/fonts/polices.css">
<style>
@page { size: 420mm 260mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 420mm; height: 260mm; }
body { display: flex; }
.page { width: 210mm; height: 260mm; position: relative; overflow: hidden; }
.pli { position: absolute; top: 0; bottom: 0; left: 210mm; width: 0; border-left: .2mm dashed rgba(0,0,0,.18); z-index: 99; }
${styles}
</style></head><body>
${defs}
<div class="page gauche">${gauche}</div>
<div class="page droite">${droite}</div>
<div class="pli"></div>
</body></html>`;
}
