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
import { coupeElegante } from '../src/gabarits/pieces.mjs';

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
  `<div class="m-abs m-arche"><img class="photo-region" src="${PHOTO('Loire.jpg')}" alt=""></div>
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

/* ——— couverture, deuxième série (l'agence : « dans l'esprit de l'ouverture de région ») ——— */
modele('couverture-D-paysage-et-sols', GEN, 'p1', `
  .m-ciel { left: 0; right: 0; top: 0; height: ${COUPE_HAUT + 8}mm; overflow: hidden; }
  .m-ciel::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(42,57,66,.55) 0%, rgba(42,57,66,.25) 38%, rgba(42,57,66,0) 60%),
      linear-gradient(90deg, rgba(42,57,66,.5) 0%, rgba(42,57,66,0) 55%); }
  .couverture .coupe { z-index: 2; }
  .couverture .titre-couv, .couverture .sous-couv, .edition-couv { z-index: 3; }
  .couverture .titre-couv { color: var(--craie); }
  .couverture .titre-couv em { color: var(--or); }
  .couverture .sous-couv { color: var(--craie); opacity: 1; text-shadow: 0 0 2mm rgba(42,57,66,.6); }
  .edition-couv .cible, .edition-couv .annee { color: var(--craie); }
  .m-reserve { position: absolute; z-index: 3; left: calc(var(--marge-int) - 4mm); top: 13mm; width: 70mm; height: 24mm;
    background: var(--craie); border-radius: 1.5mm; }
  .logo-couv { z-index: 4; }
`, (s) => s.replace('<img class="logo-couv"', `<div class="m-abs m-ciel"><img class="photo-region" src="${PHOTO('Sud-Ouest.jpg')}" alt=""></div>
   <div class="m-reserve"></div><img class="logo-couv"`));

modele('couverture-E-capsule', GEN, 'p1', `
  .couverture .coupe { display: none; }
  .m-caps { right: 20mm; top: 40mm; width: 78mm; height: 200mm; border-radius: 39mm; overflow: hidden;
    box-shadow: 0 0 0 1mm var(--craie), 0 0 0 1.8mm rgba(70,96,110,.25); background: var(--silex); }
  .m-caps .photo-region { height: 46%; }
  .m-caps .coupe { position: absolute !important; display: block !important; left: 0; right: 0; bottom: 0; top: 44%;
    width: 100%; height: 56% !important; }
  .couverture .sous-couv { width: 85mm; }
  .couverture .sanitaire-couv { color: var(--silex); }
  .m-btl-c { left: calc(var(--marge-int)); bottom: 22mm; display: flex; gap: 2.2mm; align-items: flex-end; }
  .m-btl-c .dessin { width: 9mm; }
`, (s) => {
  const coupe = s.match(/<svg viewBox="0 0 600 430"[\s\S]*?<\/svg>/)[0];
  return s.replace(coupe, `<div class="m-abs m-caps"><img class="photo-region" src="${PHOTO('Champagne.jpg')}" alt="">${coupe}</div>
    <div class="m-abs m-btl-c">${bouteille('bourguignonne', { vin: C.silex, capsule: C.gneiss })}${bouteille('flute', { vin: C.or, capsule: C.violet })}${bouteille('champenoise', { vin: C.amphibolite, capsule: C.or })}${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}</div>`);
});

modele('couverture-F-fenetres', GEN, 'p1', `
  .couverture .coupe { z-index: 2; }
  .m-fen { position: absolute; top: 56mm; width: 30mm; height: ${COUPE_HAUT - 56 + 4}mm; border-radius: 15mm 15mm 0 0;
    overflow: hidden; box-shadow: 0 0 0 .8mm var(--craie); }
  .m-fen span { position: absolute; left: 0; right: 0; bottom: 5.5mm; text-align: center; z-index: 2;
    font: 600 6.6pt var(--technique); letter-spacing: var(--interlettre); text-transform: uppercase; color: var(--craie);
    text-shadow: 0 0 1.5mm rgba(42,57,66,.8); }
  .m-lune { right: 18mm; top: 40mm; width: 10mm; }
`, (s) => s.replace('<svg viewBox="0 0 600 430"',
  [['Loire.jpg', 'Loire', 108], ['Bourgogne.jpg', 'Bourgogne', 141], ['Rhone.jpg', 'Rhône', 174]].map(([f, n, x], k) =>
    `<div class="m-fen" style="left:${x - 8}mm; top:${56 + (k === 1 ? -8 : 0)}mm; height:${COUPE_HAUT - 56 + 4 + (k === 1 ? 8 : 0)}mm">
      <img class="photo-region" src="${PHOTO(f)}" alt=""><span>${n}</span></div>`).join('')
  + `<div class="m-abs m-lune">${lune()}</div><svg viewBox="0 0 600 430"`));

/* ——— couverture, troisième série : des strates droites, sobres (3 octobre, soir) ——— */
const ETIQ = `
  .couverture .sanitaire-couv { left: auto; right: calc(var(--marge-int) + var(--fp)); text-align: right;
    color: var(--encre) !important; opacity: .75; z-index: 5; }
  .etiq-strate-el { font: 500 9.6px 'IBM Plex Sans', sans-serif; letter-spacing: 1.6px; }
  .etiq-nb-el { font: 400 12px 'Young Serif', serif; }
`;
const COUPE_SVG = /<svg viewBox="0 0 600 430"[\s\S]*?<\/svg>/;

modele('couverture-G-aquarelle', GEN, 'p1', ETIQ + `
  .couverture .sanitaire-couv { color: var(--silex); }
`, (s) => s.replace(COUPE_SVG, coupeElegante({ style: 'aquarelle' })));

modele('couverture-H-photo-et-strates', GEN, 'p1', ETIQ + `
  .m-ciel { left: 0; right: 0; top: 0; height: ${COUPE_HAUT + 2}mm; overflow: hidden; }
  .m-ciel::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(42,57,66,.5) 0%, rgba(42,57,66,.12) 40%, rgba(42,57,66,0) 70%),
      linear-gradient(90deg, rgba(42,57,66,.45) 0%, rgba(42,57,66,0) 55%); }
  .couverture .coupe { z-index: 2; }
  .couverture .titre-couv, .couverture .sous-couv, .edition-couv { z-index: 3; }
  .couverture .titre-couv { color: var(--craie); }
  .couverture .titre-couv em { color: var(--or); }
  .couverture .sous-couv { color: var(--craie); opacity: 1; }
  .edition-couv .cible, .edition-couv .annee { color: var(--craie); }
  .m-reserve { position: absolute; z-index: 3; left: calc(var(--marge-int) - 4mm); top: 13mm; width: 70mm; height: 24mm;
    background: var(--craie); border-radius: 1.5mm; }
  .logo-couv { z-index: 4; }
`, (s) => s.replace('<img class="logo-couv"', `<div class="m-abs m-ciel"><img class="photo-region" src="${PHOTO('Sud-Ouest.jpg')}" alt=""></div>
   <div class="m-reserve"></div><img class="logo-couv"`).replace(COUPE_SVG, coupeElegante({ style: 'fine' })));

modele('couverture-I-gravure', GEN, 'p1', ETIQ + `
  .couverture .sanitaire-couv { color: var(--silex); }
  .couverture .coupe { border-top: 1.2pt solid #C9AE4A; }
`, (s) => s.replace(COUPE_SVG, coupeElegante({ style: 'gravure' })));

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
  `<div class="bandeau-coupe"><img class="photo-region" src="${PHOTO('Beaujolais.jpg')}" alt=""></div>`));

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
  `<div class="m-deux"><div>$1$2</div><div><div class="m-capsule"><img class="photo-region" src="${PHOTO('Loire.jpg')}" alt=""></div>
   <div class="m-btl">${bouteille('flute', { vin: C.or, capsule: C.violet })}${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}${bouteille('champenoise', { vin: C.amphibolite, capsule: C.or })}</div></div></div>`));

/* ——————————————————————————————————— bas de fiche (salon, Château Balac) ——— */
const BAS = /<div class="respire-sol">[\s\S]*?<\/div><\/div><\/div>/;
modele('bas-de-fiche-A-photo-region', SAL, 'p31', '', (s) => s.replace(BAS,
  `<div class="respire-sol"><img class="photo-region" src="${PHOTO('Bordeaux.jpg')}" alt=""></div></div>`));

modele('bas-de-fiche-B-paysage-dessine', SAL, 'p31', `.respire-sol { background: var(--craie); }`, (s) => s.replace(BAS,
  `<div class="respire-sol">${paysage({ graineN: 29, largeur: 600, hauteur: 140, astre: 'soleil',
    palette: ['#C9B3B8', C.gneiss, '#8C3F4C', C.amphibolite] })}</div></div>`));

modele('bas-de-fiche-C-photo-sol-bouteille', SAL, 'p31', `
  .m-liseré { position: absolute; left: 0; right: 0; bottom: 0; height: 5mm; }
  .m-btl-bas { position: absolute; right: 6mm; bottom: 1mm; width: 9mm; height: 27mm; z-index: 2; }
  .m-btl-bas svg { width: 100%; height: 100%; }
`, (s) => s.replace(BAS,
  `<div class="respire-sol"><img class="photo-region" src="${PHOTO('Bordeaux.jpg')}" alt="">
   <div class="m-liseré" style="background:var(--gneiss)"><div class="trame trame-galets" style="opacity:.4"></div></div>
   <div class="m-btl-bas">${bouteille('bordelaise', { vin: C.gneiss, capsule: C.or })}</div></div></div>`));

/* ——————————————————————————————————— ouverture de région (salon, Loire) ——— */
modele('ouverture-A-photo', SAL, 'p4', `
  .ouverture .ouv-fond { background: #2E3F48; }
  .ouverture .ouv-fond .photo-region { opacity: 1; }
  .ouverture .ouv-fond::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(70,96,110,0) 0%, rgba(70,96,110,.25) 45%, rgba(46,63,72,.88) 66%, rgba(46,63,72,.95) 100%); }
`, (s) => s.replace('<div class="ouv-trame trame trame-ecailles"></div>',
  `<img class="photo-region" src="${PHOTO('Loire.jpg')}" alt="">`));

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
