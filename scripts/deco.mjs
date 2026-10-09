/* Exporte en PNG les éléments dessinés du catalogue, pour les reposer dans le PPTX.
   On réutilise exactement le même HTML/CSS que le PDF : le PPTX ne réinvente rien. */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { REGIONS, STRATES, coupe, coupeElegante, carotte, defsTrames, PICTOS_LABELS, BASE, EDITION, photoRegion } from '../src/gabarits/pieces.mjs';
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
  // ouverture A (choix de l'agence, 3 octobre) : la photo de la région, assombrie vers le bas
  // le fond seul : la capsule de sol est exportée à part, car elle change de côté selon
  // que la page est à droite ou à gauche (.page.verso .ouv-carotte)
  blocs.push({ photo: true, nom: `ouverture-${cle(r)}`, l: 216, h: 266, html:
    `<div style="position:absolute;inset:0;background:#2E3F48"></div>
     <img src="${photoRegion(r)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
     <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(70,96,110,0) 0%, rgba(70,96,110,.25) 45%, rgba(46,63,72,.88) 66%, rgba(46,63,72,.95) 100%)"></div>` });
  // la capsule, avec 1 mm d'air tout autour pour que son liseré tienne dans l'image
  blocs.push({ nom: `capsule-${cle(r)}`, l: 48, h: 120, html:
    `<div style="position:absolute;top:1mm;left:1mm;width:46mm;height:118mm;
       border-radius:23mm;overflow:hidden;
       box-shadow:0 0 0 .7mm rgba(${r === 'Champagne' ? '70,96,110,.38' : '251,248,241,.35'})">
       ${solRegion(r, REGIONS.indexOf(r) + 1)}</div>` });
  blocs.push({ nom: `carotte-${cle(r)}`, l: 12, h: 266, html:
    `<div style="position:absolute;inset:0">${carotte(r)}</div>` });
  // bas de fiche A : la photo de la région
  blocs.push({ photo: true, nom: `sol-${cle(r)}`, l: 170, h: 40, html:
    `<div style="position:absolute;inset:0;border-radius:1.5mm;overflow:hidden">
       <img src="${photoRegion(r)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>` });
});

// Les pictos de label, posés dans les jetons des fiches et dans la légende du sommaire.
Object.entries(PICTOS_LABELS).forEach(([nom, svg]) => {
  blocs.push({ nom: `label-${nom}`, l: 3, h: 3, html:
    `<svg viewBox="0 0 14 14" style="position:absolute;inset:0;width:100%;height:100%">${svg}</svg>` });
});

// couverture H (choix de l'agence, 3 octobre) : le ciel en photo, les strates droites dessous
// au salon, la bande de strates est plus basse (108 mm) : le ciel descend d'autant. Le
// catalogue caviste global reprend cette couverture (classe .couverture-salon) : même bande.
const SALON_D = EDITION !== 'general';
blocs.push({ photo: true, nom: 'couv-ciel', l: 216, h: SALON_D ? 157 : 117, html:
  `<img src="${photoRegion('Sud-Ouest')}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
   <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(42,57,66,.5) 0%, rgba(42,57,66,.12) 40%, rgba(42,57,66,0) 70%),
     linear-gradient(90deg, rgba(42,57,66,.45) 0%, rgba(42,57,66,0) 55%)"></div>` });
blocs.push({ nom: 'coupe-titree', l: 216, h: SALON_D ? 111 : 151, html:
  `<div style="position:absolute;inset:0">${coupeElegante({ style: 'fine' })}</div>` });
blocs.push({ nom: 'coupe-nue', l: 170, h: 34, html:
  `<div style="position:absolute;inset:0;border-radius:1.5mm;overflow:hidden">
     ${coupeElegante({ largeur: 600, hauteur: 110, style: 'fine', etiquettes: false })}</div>` });
// page 2 A : la photo du Beaujolais ; dans le catalogue caviste global, les vignes au
// coucher de soleil du Drive de l'agence, comme dans le PDF
const PHOTO_PAGE2 = EDITION === 'global' || EDITION === 'restaurant'
  ? '../src/photos/agence/page2-vignes-coucher-de-soleil.jpg' : photoRegion('Beaujolais');
blocs.push({ photo: true, nom: 'agence-photo', l: 170, h: 62, html:
  `<div style="position:absolute;inset:0;border-radius:1.5mm;overflow:hidden">
     <img src="${PHOTO_PAGE2}" style="width:100%;height:100%;object-fit:cover;display:block"></div>` });
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
.etiq-nb{font:400 11px 'IBM Plex Sans',sans-serif}
.etiq-strate-el{font:500 9.6px 'IBM Plex Sans',sans-serif;letter-spacing:1.6px}
.etiq-nb-el{font:400 12px 'Young Serif',serif}</style></head><body>
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
  // une photo s'exporte en JPEG (le .pptx en répète certaines sur plusieurs diapositives :
  // en PNG, il dépassait 50 Mo) ; le reste en PNG transparent
  if (b.photo) {
    fs.rmSync(path.join(DECO, `${b.nom}.png`), { force: true });
    await el.screenshot({ path: path.join(DECO, `${b.nom}.jpg`), type: 'jpeg', quality: 82 });
  } else await el.screenshot({ path: path.join(DECO, `${b.nom}.png`), omitBackground: true });
}
await nav.close();
fs.writeFileSync(path.join(DECO, 'tailles.json'),
  JSON.stringify(Object.fromEntries(blocs.map((b) => [b.nom, { l: b.l, h: b.h }])), null, 1));
console.log(`${blocs.length} éléments → build/deco-${BASE}/`);
