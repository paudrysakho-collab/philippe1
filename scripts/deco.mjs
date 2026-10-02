/* Exporte en PNG les éléments dessinés du catalogue, pour les reposer dans le PPTX.
   On réutilise exactement le même HTML/CSS que le PDF : le PPTX ne réinvente rien. */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { REGIONS, STRATES, coupe, carotte, defsTrames, PICTOS_LABELS, BASE } from '../src/gabarits/pieces.mjs';
import { solTeinte, solRegion } from '../src/gabarits/pages.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
// une déco par édition : au salon, la coupe et les tranches n'ont que neuf régions
const DECO = path.join(RACINE, `build/deco-${BASE}`);
fs.mkdirSync(DECO, { recursive: true });

/** Identifiants sans accent ni espace : ils servent de noms de fichier et de sélecteurs. */
const cle = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/[^A-Za-z0-9]+/g, '-').toLowerCase();
const blocs = [];

// Ouverture de région : fond pleine page, couleur + trame + carotte verticale
REGIONS.forEach((r) => {
  const s = STRATES[r];
  blocs.push({ nom: `ouverture-${cle(r)}`, l: 216, h: 266, html:
    `<div style="position:absolute;inset:0;background:${s.hex}"></div>
     <div class="trame trame-${s.t}" style="position:absolute;inset:0;opacity:.5"></div>
     <div style="position:absolute;top:18mm;right:17mm;width:46mm;height:118mm;
       border-radius:23mm;overflow:hidden;
       box-shadow:0 0 0 .7mm rgba(${r === 'Champagne' ? '70,96,110,.38' : '251,248,241,.35'})">
       ${solRegion(r, REGIONS.indexOf(r) + 1)}</div>` });
  blocs.push({ nom: `carotte-${cle(r)}`, l: 12, h: 266, html:
    `<div style="position:absolute;inset:0">${carotte(r)}</div>` });
  blocs.push({ nom: `sol-${cle(r)}`, l: 170, h: 40, html:
    `<div style="position:absolute;inset:0;border-radius:1.5mm;overflow:hidden">
       ${solTeinte(r, 7)}</div>` });
});

// Les pictos de label, posés dans les jetons des fiches et dans la légende du sommaire.
Object.entries(PICTOS_LABELS).forEach(([nom, svg]) => {
  blocs.push({ nom: `label-${nom}`, l: 3, h: 3, html:
    `<svg viewBox="0 0 14 14" style="position:absolute;inset:0;width:100%;height:100%">${svg}</svg>` });
});

blocs.push({ nom: 'coupe-titree', l: 216, h: 151, html:
  `<div style="position:absolute;inset:0">${coupe({ largeur: 600, hauteur: 430 })}</div>` });
blocs.push({ nom: 'coupe-nue', l: 176, h: 42, html:
  `<div style="position:absolute;inset:0;border-radius:1.5mm;overflow:hidden">
     ${coupe({ largeur: 600, hauteur: 110, graineN: 2, etiquettes: false })}</div>` });
blocs.push({ nom: 'coupe-pleine', l: 216, h: 266, html:
  `<div style="position:absolute;inset:0">${coupe({ largeur: 600, hauteur: 430, graineN: 99 })}</div>` });

const html = `<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../src/styles/systeme.css">
<link rel="stylesheet" href="../src/styles/pages.css">
<style>body{margin:0;background:transparent}
.bloc{position:relative;overflow:hidden;background:transparent;margin:0 0 8mm}
.bloc:not(.bloc-nu) .coupe,.bloc:not(.bloc-nu) svg{position:absolute;inset:0;width:100%;height:100%}
.bloc-nu{display:flex;flex-direction:column}
.etiq-strate{font:600 11px 'IBM Plex Sans',sans-serif;letter-spacing:.03em}
.etiq-nb{font:400 11px 'IBM Plex Sans',sans-serif}</style></head><body>
${defsTrames()}
${blocs.map((b) => `<div class="bloc${b.nu ? ' bloc-nu' : ''}" id="${b.nom}"
  style="width:${b.l}mm;height:${b.h}mm">${b.html}</div>`).join('\n')}
</body></html>`;

const fichier = path.join(RACINE, `build/${BASE}-deco.html`);
fs.writeFileSync(fichier, html);

const nav = await chromium.launch();
const page = await nav.newPage({ deviceScaleFactor: 3 });   // ≈ 300 ppi à la taille d'usage
await page.goto(pathToFileURL(fichier).href, { waitUntil: 'networkidle' });
for (const b of blocs) {
  const el = page.locator(`#${b.nom}`);
  await el.screenshot({ path: path.join(DECO, `${b.nom}.png`), omitBackground: true });
}
await nav.close();
fs.writeFileSync(path.join(DECO, 'tailles.json'),
  JSON.stringify(Object.fromEntries(blocs.map((b) => [b.nom, { l: b.l, h: b.h }])), null, 1));
console.log(`${blocs.length} éléments → build/deco-${BASE}/`);
