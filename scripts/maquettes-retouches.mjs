/* Les modèles de retouches demandés par l'agence (3 octobre 2026) : couverture, page 2, bas de
   fiche, ouverture de région. Chaque modèle part de la VRAIE page du catalogue (build/*.html,
   après `npm run build` et `npm run salon`), avec ses retouches, rendue en PNG dans
   concepts/retouches-oct/. Rien n'est changé dans les catalogues livrés tant que l'agence n'a
   pas choisi. Usage : node scripts/maquettes-retouches.mjs */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';
import { C, bouteille, feuille, lune, soleil, cep, paysage } from '../src/gabarits/dessins.mjs';

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SORTIE = path.join(RACINE, 'concepts/retouches-oct');
fs.mkdirSync(SORTIE, { recursive: true });

const lire = (f) => fs.readFileSync(path.join(RACINE, 'build', f), 'utf8');
const GEN = lire('catalogue-scio-2026-ecran.html');
const SAL = lire('salon-prive-2026-ecran.html');
const tete = (h) => h.slice(0, h.indexOf('<section'));
function section(h, id) {
  const i = h.indexOf(`id="${id}"`);
  const s = h.lastIndexOf('<section', i);
  return h.slice(s, h.indexOf('</section>', i) + 10);
}
const PHOTO = (f) => `../../src/photos/regions/${f}`;

/* le style commun aux modèles */
const CSS = `
.dessin { display: block; overflow: visible; }
.m-abs { position: absolute; }
.photo-region { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.credit-m { position: absolute; right: 2mm; bottom: 1.2mm; font: 400 5.6pt var(--technique);
  color: rgba(251,248,241,.85); }
`;

const modeles = [];
function modele(nom, source, id, css, transformer) {
  let s = section(source, id);
  s = transformer(s);
  const html = tete(source).replace('</head>', `<style>${CSS}${css}</style></head>`)
    + s + '</body></html>';
  // les fichiers sont un niveau plus bas que build/ : les chemins relatifs remontent d'un cran de plus
  const html2 = html.replaceAll('"../src/', '"../../src/');
  const f = path.join(SORTIE, `${nom}.html`);
  fs.writeFileSync(f, html2);
  modeles.push({ nom, f });
}

/* ——————————————————————————————————— couverture ——— */
const COUPE_HAUT = 112; // mm : le haut des strates sur la couverture (260 − 148)

modele('couverture-A-paysage-dessine', GEN, 'p1', `
  .m-paysage { left: 78mm; right: 0; top: ${COUPE_HAUT - 50}mm; height: 52mm;
    -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 22%); mask-image: linear-gradient(90deg, transparent 0, #000 22%); }
  .m-paysage svg { width: 100%; height: 100%; }
  .m-cep { right: 26mm; top: ${COUPE_HAUT - 44}mm; width: 26mm; z-index: 3; }
  .couverture .coupe { z-index: 2; }
`, (s) => s.replace('<svg viewBox="0 0 600 430"',
  `<div class="m-abs m-paysage">${paysage({ graineN: 11, largeur: 600, hauteur: 160,
    palette: ['#C9D2CF', '#A9B8A9', '#E2C089', '#C98F8F'], astre: 'soleil' })}</div>
   <div class="m-abs m-cep">${cep({ racines: 70 })}</div>
   <svg viewBox="0 0 600 430"`));

modele('couverture-B-photo-arche', GEN, 'p1', `
  .m-arche { right: 18mm; top: 40mm; width: 74mm; height: ${COUPE_HAUT - 40 + 6}mm; border-radius: 37mm 37mm 0 0;
    overflow: hidden; box-shadow: 0 0 0 .8mm var(--craie); }
  .couverture .coupe { z-index: 2; }
`, (s) => s.replace('<svg viewBox="0 0 600 430"',
  `<div class="m-abs m-arche"><img class="photo-region" src="${PHOTO('Loire-16.jpg')}" alt=""></div>
   <svg viewBox="0 0 600 430"`));

modele('couverture-C-petits-dessins', GEN, 'p1', `
  .m-b { bottom: ${148 - 1}mm; z-index: 3; }
  .couverture .coupe { z-index: 2; }
  .m-astre { width: 13mm; }
  .m-f { width: 11mm; opacity: .95; }
`, (s) => s.replace('<svg viewBox="0 0 600 430"',
  `<div class="m-abs m-astre" style="right:30mm; top:52mm">${lune()}</div>
   <div class="m-abs m-astre" style="right:58mm; top:62mm; width:10mm">${soleil()}</div>
   <div class="m-abs m-f" style="left:120mm; top:84mm">${feuille({ rotation: -18 })}</div>
   <div class="m-abs m-b" style="right:22mm; width:9mm">${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}</div>
   <div class="m-abs m-b" style="right:33mm; width:7.6mm">${bouteille('flute', { vin: C.or, capsule: C.violet })}</div>
   <div class="m-abs m-b" style="right:42mm; width:10mm">${bouteille('champenoise', { vin: C.amphibolite, capsule: C.or })}</div>
   <div class="m-abs m-b" style="right:54mm; width:9mm">${bouteille('bourguignonne', { vin: C.silex, capsule: C.gneiss })}</div>
   <svg viewBox="0 0 600 430"`));

/* ——————————————————————————————————— page 2, l'agence ——— */
const CREDO_POSE = `
  .credo { font-family: var(--courant); font-size: 14.5pt; line-height: 1.55; color: var(--encre);
    max-width: 140mm; padding-left: 5mm; border-left: 1.2pt solid var(--or); }
  .credo strong { font-weight: 500; color: inherit; }
  .contact .tel { font-size: 15pt; }
`;
modele('page2-A-texte-pose-photo', GEN, 'p2', CREDO_POSE + `
  .bandeau-coupe { height: 62mm; }
`, (s) => s.replace(/<div class="bandeau-coupe">[\s\S]*?<\/svg><\/div>/,
  `<div class="bandeau-coupe"><img class="photo-region" src="${PHOTO('Bordeaux-07.jpg')}" alt=""></div>`));

modele('page2-B-italique-paysage', GEN, 'p2', CREDO_POSE + `
  .credo { font-style: italic; font-size: 15pt; border-left: 0; padding-left: 0; }
  .bandeau-coupe { height: 58mm; background: var(--craie); }
  .bandeau-coupe svg { position: absolute; inset: 0; width: 100%; height: 100%; }
`, (s) => s.replace(/<div class="bandeau-coupe">[\s\S]*?<\/svg><\/div>/,
  `<div class="bandeau-coupe">${paysage({ graineN: 4, largeur: 600, hauteur: 200, astre: 'lune',
    palette: [C.silex, C.amphibolite, C.sables, C.gneiss] })}</div>`));

modele('page2-C-deux-colonnes', GEN, 'p2', CREDO_POSE + `
  .m-deux { display: grid; grid-template-columns: 1fr 50mm; gap: 10mm; align-items: start; }
  .m-capsule { position: relative; width: 50mm; height: 92mm; border-radius: 25mm; overflow: hidden;
    box-shadow: 0 0 0 .8mm var(--craie), 0 0 0 1.4mm rgba(70,96,110,.25); }
  .m-btl { display: flex; gap: 2mm; align-items: flex-end; margin-top: 5mm; justify-content: center; }
  .m-btl .dessin { width: 8mm; }
  .credo { margin-bottom: 9mm; }
`, (s) => s.replace(/(<p class="credo">[\s\S]*?<\/p>)([\s\S]*?<div class="coordonnees">[\s\S]*?<\/div>)/,
  `<div class="m-deux"><div>$1$2</div><div><div class="m-capsule"><img class="photo-region" src="${PHOTO('Loire-16.jpg')}" alt=""></div>
   <div class="m-btl">${bouteille('flute', { vin: C.or, capsule: C.violet })}${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}${bouteille('champenoise', { vin: C.amphibolite, capsule: C.or })}</div></div></div>`));

/* ——————————————————————————————————— bas de fiche (salon, Château Balac) ——— */
const BAS = /<div class="respire-sol">[\s\S]*?<\/div><\/div><\/div>/;
modele('bas-de-fiche-A-photo-region', SAL, 'p31', '', (s) => s.replace(BAS,
  `<div class="respire-sol"><img class="photo-region" src="${PHOTO('Bordeaux-03.jpg')}" alt=""></div></div>`));

modele('bas-de-fiche-B-paysage-dessine', SAL, 'p31', `.respire-sol { background: var(--craie); }`, (s) => s.replace(BAS,
  `<div class="respire-sol">${paysage({ graineN: 29, largeur: 600, hauteur: 140, astre: 'soleil',
    palette: ['#C9B3B8', C.gneiss, '#8C3F4C', C.amphibolite] })}</div></div>`));

modele('bas-de-fiche-C-photo-sol-bouteille', SAL, 'p31', `
  .m-liseré { position: absolute; left: 0; right: 0; bottom: 0; height: 5mm; }
  .m-btl-bas { position: absolute; right: 6mm; bottom: 1mm; width: 9mm; height: 27mm; z-index: 2; }
  .m-btl-bas svg { width: 100%; height: 100%; }
`, (s) => s.replace(BAS,
  `<div class="respire-sol"><img class="photo-region" src="${PHOTO('Bordeaux-03.jpg')}" alt="">
   <div class="m-liseré" style="background:var(--gneiss)"><div class="trame trame-galets" style="opacity:.4"></div></div>
   <div class="m-btl-bas">${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}</div></div></div>`));

/* ——————————————————————————————————— ouverture de région (salon, Loire) ——— */
modele('ouverture-A-photo', SAL, 'p4', `
  .ouverture .ouv-fond { background: #2E3F48; }
  .ouverture .ouv-fond .photo-region { opacity: 1; }
  .ouverture .ouv-fond::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(70,96,110,0) 0%, rgba(70,96,110,.25) 45%, rgba(46,63,72,.88) 66%, rgba(46,63,72,.95) 100%); }
`, (s) => s.replace('<div class="ouv-trame trame trame-ecailles"></div>',
  `<img class="photo-region" src="${PHOTO('Loire-16.jpg')}" alt="">`));

modele('ouverture-B-paysage-dessine', SAL, 'p4', `
  .m-pays { position: absolute; left: 0; right: 0; top: 70mm; height: 70mm; opacity: .9; }
  .m-pays svg { width: 100%; height: 100%; }
`, (s) => s.replace('<div class="ouv-trame trame trame-ecailles"></div>',
  `<div class="ouv-trame trame trame-ecailles"></div><div class="m-pays">${paysage({ graineN: 3, largeur: 600, hauteur: 200,
    astre: 'lune', palette: ['#6E8693', '#5C7A86', '#8FA6B0', '#B9C8CC'] })}</div>`));

/* ——————————————————————————————————— rendu ——— */
const nav = await chromium.launch();
const p = await nav.newPage({ deviceScaleFactor: 2 });
for (const m of modeles) {
  await p.goto('file://' + m.f);
  await p.waitForLoadState('networkidle');
  await p.evaluate(() => document.fonts.ready);
  const el = await p.$('section.page');
  await el.screenshot({ path: m.f.replace('.html', '.png') });
  console.log('✓', path.relative(RACINE, m.f.replace('.html', '.png')));
}
await nav.close();
