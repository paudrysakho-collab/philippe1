/* La liste des vins dégustés au Salon Privé, stand par stand : deux à trois pages.
   Même DA que le catalogue (polices, couleurs de strate, pictos), mêmes données que l'édition
   du salon (data/salon-prive-2026.json), sans prix. Les stands suivent l'ordre du plan ; un
   stand n'est jamais coupé entre deux colonnes. La répartition est MESURÉE dans Chromium.

   Format : A4 par défaut, pour une impression au bureau ; LISTE_FORMAT=catalogue la sort au
   format du catalogue (210 × 260 mm). */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';

process.env.EDITION = 'salon';
const { SALON, STRATES, esc, picto, famille, NOM_FAMILLE, catalogue } = await import('../src/gabarits/pieces.mjs');

const RACINE = path.resolve(import.meta.dirname, '..');
const BUILD = path.join(RACINE, 'build');
const CATALOGUE = process.env.LISTE_FORMAT === 'catalogue';
const PAGE = CATALOGUE ? { l: 210, h: 260 } : { l: 210, h: 297 };
const MARGE = { haut: 13, bas: 14, cote: 13 };
const ECART_COL = 8;
const COL = (PAGE.l - 2 * MARGE.cote - ECART_COL) / 2;
const ENTETE_P1 = 38;          // le bandeau de titre de la première page, en mm
const SORTIE = path.join(RACINE, `dist/salon-prive-2026-liste-des-vins${CATALOGUE ? '-format-catalogue' : ''}.pdf`);
const EV = SALON.evenement;
const parNumero = Object.fromEntries(catalogue.domaines.map((d) => [d.numero, d]));

/** Le type de vin affiché : la couleur du tarif (ou de la liste), sinon la famille du picto. */
function typeDe(v, f) {
  if (v.couleur) return v.couleur;
  return f === 'autre' ? '—' : NOM_FAMILLE[f];
}

function blocStand(s) {
  const st = STRATES[s.region];
  const clair = s.region === 'Champagne';
  const plusieurs = new Set(s.vins.map((v) => v.fiche)).size > 1;
  let fichePrec = null;
  const lignes = s.vins.map((v) => {
    const f = famille(v, {});
    const sous = plusieurs && v.fiche !== fichePrec
      ? `<div class="lv-sous">${esc(parNumero[v.fiche].nom)}</div>` : '';
    fichePrec = v.fiche;
    const titre = v.cuvee || v.appellation;
    return `${sous}<div class="lv-vin">
      <span class="lv-picto">${picto(f)}</span>
      <span class="lv-nom"><b>${esc(titre)}</b>${v.cuvee && v.appellation
        ? `<i>${esc(v.appellation)}</i>` : ''}</span>
      <span class="lv-coul">${esc(typeDe(v, f))}</span>
      <span class="lv-mil">${esc(v.millesime && v.millesime !== '—' ? v.millesime : '—')}</span></div>`;
  }).join('');
  return `<section class="lv-stand" data-stand="${s.stand}">
    <header><span class="lv-n${clair ? ' claire' : ''}" style="--strate:${st.hex}">${s.stand}</span>
      <span class="lv-titre">${esc(s.nom_salon)}</span>
      <span class="lv-reg">${esc(s.region)}, ${esc(s.salle)}</span></header>
    ${lignes}</section>`;
}

const STYLE = `
@page { size: ${PAGE.l}mm ${PAGE.h}mm; margin: 0; }
body { margin: 0; background: var(--craie); }
.lv-page { position: relative; width: ${PAGE.l}mm; height: ${PAGE.h}mm; overflow: hidden;
  background: var(--craie); break-after: page; }
.lv-page:last-child { break-after: auto; }
.lv-entete { position: absolute; left: ${MARGE.cote}mm; right: ${MARGE.cote}mm; top: ${MARGE.haut}mm;
  height: ${ENTETE_P1 - 6}mm; display: flex; align-items: flex-start; justify-content: space-between;
  border-bottom: 1.4pt solid var(--violet); }
.lv-entete h1 { font-family: var(--titre); font-weight: 400; font-size: 22pt; line-height: 1.05;
  color: var(--violet); margin: 0 0 1.6mm; }
.lv-entete p { margin: 0; font: 400 9.5pt var(--courant); color: var(--silex); }
.lv-entete p b { font-family: var(--titre); font-weight: 400; color: var(--silex); font-size: 11pt; }
.lv-entete img { width: 46mm; margin-top: 1mm; }
.lv-col { position: absolute; width: ${COL}mm; }
.lv-stand { break-inside: avoid; margin-bottom: 3.4mm; }
.lv-stand header { display: flex; align-items: center; gap: 2.2mm; padding-bottom: 1mm;
  border-bottom: .6pt solid var(--silex); margin-bottom: .6mm; }
.lv-n { flex: none; width: 6.4mm; height: 6.4mm; border-radius: 50%; background: var(--strate);
  color: var(--craie); font: 600 8.5pt var(--technique); display: flex; align-items: center;
  justify-content: center; font-variant-numeric: tabular-nums; }
.lv-n.claire { color: var(--silex); box-shadow: inset 0 0 0 .6pt var(--silex); }
.lv-titre { flex: 1; font-family: var(--titre); font-size: 10.5pt; line-height: 1.1; color: var(--encre); }
.lv-reg { font: 500 7.5pt var(--technique); color: var(--gneiss); white-space: nowrap; }
.lv-sous { font: 600 7.6pt var(--technique); color: var(--violet); margin: 1.4mm 0 .2mm 6mm; }
.lv-vin { display: grid; grid-template-columns: 4.2mm 1fr 20mm 10mm; column-gap: 1.2mm;
  align-items: baseline; padding: .45mm 0; border-bottom: .25pt solid rgba(70,96,110,.2);
  font-family: var(--technique); font-variant-numeric: tabular-nums; }
.lv-picto { align-self: center; }
.lv-picto .picto { width: 2.9mm; height: 2.9mm; display: block; }
.lv-nom { font-size: 8pt; line-height: 1.25; }
.lv-nom b { font-weight: 500; color: var(--encre); margin-right: 1.6mm; }
.lv-nom i { font-style: normal; font-size: 7.5pt; color: var(--gneiss); }
.lv-coul, .lv-mil { font-size: 7.5pt; line-height: 1.25; color: var(--silex); }
.lv-mil { text-align: right; }
.lv-pied { position: absolute; left: ${MARGE.cote}mm; right: ${MARGE.cote}mm; bottom: 6mm;
  display: flex; justify-content: space-between; align-items: baseline;
  font: 400 6.6pt var(--technique); color: var(--silex); }
.lv-pied .san { text-transform: uppercase; letter-spacing: .03em; }
.lv-legende { display: flex; gap: 3mm; flex-wrap: wrap; margin-top: 2.2mm;
  font: 400 7.5pt var(--technique); color: var(--silex); }
.lv-legende span { display: inline-flex; align-items: center; gap: .9mm; }
.lv-legende .picto { width: 2.4mm; height: 2.4mm; }
`;

const tete = (corps) => `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>${esc(EV.nom)} — les vins à la dégustation</title>
<link rel="stylesheet" href="../src/styles/systeme.css">
<style>${STYLE}</style></head><body>${corps}</body></html>`;

const stands = [...SALON.stands].sort((a, b) => a.stand - b.stand);
const navigateur = await chromium.launch();

// 1. mesure de chaque bloc, à la largeur d'une colonne
const mesure = path.join(BUILD, 'liste-vins-mesure.html');
fs.mkdirSync(BUILD, { recursive: true });
fs.writeFileSync(mesure, tete(`<div style="width:${COL}mm">${stands.map(blocStand).join('')}</div>`));
const p = await navigateur.newPage();
await p.goto(pathToFileURL(mesure).href, { waitUntil: 'networkidle' });
await p.emulateMedia({ media: 'print' });
const hauteurs = await p.evaluate(() => Object.fromEntries([...document.querySelectorAll('.lv-stand')]
  .map((el) => [el.dataset.stand, (el.getBoundingClientRect().height / (96 / 25.4)) + 4.2])));
await p.close();

// 2. répartition : colonne après colonne, page après page, sans couper un stand
const utile = (premiere) => PAGE.h - MARGE.haut - MARGE.bas - (premiere ? ENTETE_P1 : 0) - 3;
const colonnes = [];
let courante = [], reste = utile(true);
for (const s of stands) {
  const h = hauteurs[s.stand];
  if (h > reste && courante.length) {
    colonnes.push(courante);
    courante = [];
    reste = utile(colonnes.length < 2);
  }
  courante.push(s);
  reste -= h;
}
colonnes.push(courante);
// équilibrer la dernière page : si sa seconde colonne est vide, on partage
const pages = [];
for (let i = 0; i < colonnes.length; i += 2) pages.push([colonnes[i], colonnes[i + 1] || []]);

const legende = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'jus', 'autre'].map((f) =>
  `<span>${picto(f)} ${esc(f === 'autre' ? 'Non précisé' : NOM_FAMILLE[f])}</span>`).join('');
const corps = pages.map(([g, d], i) => {
  const haut = MARGE.haut + (i === 0 ? ENTETE_P1 : 0);
  return `<div class="lv-page">
    ${i === 0 ? `<div class="lv-entete"><div>
        <h1>Les vins à la dégustation</h1>
        <p><b>${esc(EV.nom)}</b> — ${esc(EV.date_texte)}<br>${esc(EV.lieu)}, ${esc(EV.commune)}.
          Les ${SALON.stands.length} stands, dans l'ordre du plan des exposants.</p>
        <div class="lv-legende">${legende}</div></div>
        <img src="../src/images/logo-agence-scio-detoure.png" alt="Agence SCIO Vins &amp; Spirits"></div>` : ''}
    <div class="lv-col" style="left:${MARGE.cote}mm;top:${haut}mm">${g.map(blocStand).join('')}</div>
    <div class="lv-col" style="left:${MARGE.cote + COL + ECART_COL}mm;top:${haut}mm">${d.map(blocStand).join('')}</div>
    <div class="lv-pied"><span class="san">${esc(catalogue.agence.message_sanitaire)}</span>
      <span>${i + 1} / ${pages.length}</span></div>
  </div>`;
}).join('');

const html = path.join(BUILD, 'liste-vins.html');
fs.writeFileSync(html, tete(corps));
const q = await navigateur.newPage();
await q.goto(pathToFileURL(html).href, { waitUntil: 'networkidle' });
await q.emulateMedia({ media: 'print' });
// contrôle : rien ne descend sous la marge du bas
const depasse = await q.evaluate((bas) => [...document.querySelectorAll('.lv-col')].filter((c) =>
  c.getBoundingClientRect().bottom > c.closest('.lv-page').getBoundingClientRect().bottom - bas * 96 / 25.4)
  .length, MARGE.bas);
await q.pdf({ path: SORTIE, printBackground: true, preferCSSPageSize: true, tagged: true });
await navigateur.close();

const nbVins = stands.reduce((n, s) => n + s.vins.length, 0);
console.log(`✓ ${path.relative(RACINE, SORTIE)} — ${pages.length} pages, ${stands.length} stands, ${nbVins} vins`);
if (depasse) { console.error(`⚠ ${depasse} colonne(s) dépassent la marge du bas`); process.exit(1); }
if (stands.length !== EV.exposants) { console.error('⚠ il manque des stands'); process.exit(1); }
