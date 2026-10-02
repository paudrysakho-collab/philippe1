/* Fabrique le catalogue : passe de mesure, pagination, puis les deux PDF.
   La pagination est MESURÉE dans Chromium, pas estimée : rien ne déborde par surprise. */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import {
  catalogue, REGIONS, esc, defsTrames, nbReferences, famillesDe, EDITION, BASE, BANDES,
} from '../src/gabarits/pieces.mjs';
import * as G from '../src/gabarits/pages.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
const BUILD = path.join(RACINE, 'build');
const DIST = path.join(RACINE, 'dist');
fs.mkdirSync(BUILD, { recursive: true });
fs.mkdirSync(DIST, { recursive: true });

const PX_PAR_MM = 96 / 25.4;
const CADRE_H = 260 - 15 - 13;          // hauteur utile d'une page, en mm
const ECART_TABLEAUX = 3.6;             // margin-top entre deux tableaux, en mm
const SECURITE = 2;                     // marge de sécurité : on ne remplit jamais au millimètre
const VIDE_MIN = 30;                    // au-delà, une fiche courte reçoit la coupe de son sol
const VIDE_MAX = 40;                    // discret : le bandeau ne doit pas devenir du papier peint

/* ———————————————————————————————————————— 1. passe de mesure ——— */

function documentMesure() {
  const blocs = catalogue.domaines.map((d) => {
    const tableaux = d.tableaux.map((t, ti) => {
      const lignes = t.lignes.map((l, li) => ({ l, cle: `${d.numero}-${ti}-${li}` }));
      return G_tableau(t, lignes, `${d.numero}-${ti}`);
    }).join('');
    return `<div class="mesure-bloc">
      <div data-m="entete-${d.numero}">${G.enteteDomaine(d, false)}</div>
      <div data-m="enteteSuite-${d.numero}">${G.enteteDomaine(d, true)}</div>
      ${BANDES.map((b) => `<div data-m="haut-${d.numero}-${b}">${G.hautDomaine(d, b)}</div>`).join('')}
      ${tableaux}
      <div data-m="note-${d.numero}">${G.noteDomaine(d)}</div>
      <div data-m="pied-${d.numero}">${G.piedDomaine(d, new Map(catalogue.domaines.map((x) => [x.numero, 99])))}</div>
    </div>`;
  }).join('');
  // Deux témoins pour calibrer l'index : une ligne et un titre de famille.
  const temoinsIndex = `<div class="mesure-bloc"><div class="idx-flux" style="columns:1">
    <h3 class="idx-titre" data-m="idx-titre">Témoin</h3>
    <a class="idx-ligne" data-m="idx-ligne"><span class="idx-nom">Témoin de calibrage</span>
      <span class="idx-dom">26</span><span class="idx-pg">44</span></a></div></div>`;
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="../src/styles/systeme.css">
<link rel="stylesheet" href="../src/styles/pages.css">
<style>body{background:var(--tuffeau)}
  .mesure-bloc{width:170mm;margin:0 auto 40mm}
  /* flow-root : sans lui les marges des enfants sortent de la boîte et la mesure ment */
  .mesure-bloc > [data-m]{display:flow-root}</style>
</head><body>${defsTrames()}${blocs}${temoinsIndex}</body></html>`;
}

/* Le même tableau que dans les pages, mais avec un identifiant de thead pour la mesure. */
function G_tableau(t, lignes, cle) {
  const html = G_tableauBase(t, lignes, cle);
  return html.replace('<thead>', `<thead data-m="thead-${cle}">`);
}
function G_tableauBase(t, lignes, cle) {
  // on réutilise strictement le composant du catalogue
  return tableauHtmlImport(t, lignes, { cleTableau: cle });
}
let tableauHtmlImport;
{
  const m = await import('../src/gabarits/pieces.mjs');
  tableauHtmlImport = m.tableauHtml;
}

async function mesurer(navigateur) {
  const fichier = path.join(BUILD, `${BASE}-mesure.html`);
  fs.writeFileSync(fichier, documentMesure());
  const p = await navigateur.newPage();
  await p.goto(pathToFileURL(fichier).href, { waitUntil: 'networkidle' });
  await p.emulateMedia({ media: 'print' });
  const brut = await p.evaluate(() => {
    const out = { blocs: {}, lignes: {} };
    document.querySelectorAll('[data-m]').forEach((el) => {
      out.blocs[el.dataset.m] = el.getBoundingClientRect().height;
    });
    document.querySelectorAll('tr[data-ligne]').forEach((el) => {
      out.lignes[el.dataset.ligne] = el.getBoundingClientRect().height;
    });
    return out;
  });
  await p.close();
  const mm = (px) => px / (96 / 25.4);
  const m = { blocs: {}, lignes: {} };
  for (const [k, v] of Object.entries(brut.blocs)) m.blocs[k] = mm(v);
  for (const [k, v] of Object.entries(brut.lignes)) m.lignes[k] = mm(v);
  fs.writeFileSync(path.join(BUILD, `${BASE}-mesures.json`), JSON.stringify(m, null, 1));
  return m;
}

/* ——————————————————————————————————————————— 2. pagination ——— */

/** Découpe un domaine. La bande du haut s'abaisse si cela épargne une page : on garde la
    plus haute des bandes qui donnent le moins de pages (voir BANDES, pieces.mjs). */
function decouper(d, m) {
  let choix = null;
  for (const bande of BANDES) {
    const essai = decouperBande(d, m, bande);
    if (!choix || essai.pages.length < choix.pages.length) choix = essai;
  }
  return choix;
}

/** Puis on rééquilibre : deux pages dont l'une est vide, c'est laid. */
function decouperBande(d, m, bande) {
  const premier = decouperAvecBudget(d, m, Infinity, bande);
  if (premier.pages.length < 2) return premier;
  // On vise des pages également remplies : on rabote le budget jusqu'à ce que ça déborde.
  let meilleur = premier;
  for (let rabot = 2; rabot <= 60; rabot += 2) {
    const essai = decouperAvecBudget(d, m, rabot, bande);
    if (essai.pages.length > premier.pages.length) break;
    meilleur = essai;
  }
  return meilleur;
}

/** `rabot` retire des millimètres au budget de chaque page pour répartir les lignes. */
function decouperAvecBudget(d, m, rabot, bande) {
  const entete = m.blocs[`entete-${d.numero}`];
  const enteteSuite = m.blocs[`enteteSuite-${d.numero}`];
  const haut = m.blocs[`haut-${d.numero}-${bande}`];
  const pied = m.blocs[`pied-${d.numero}`];

  const tableaux = d.tableaux.map((t, ti) => ({
    t, ti,
    thead: m.blocs[`thead-${d.numero}-${ti}`],
    lignes: t.lignes.map((l, li) => ({ l, cle: `${d.numero}-${ti}-${li}`, h: m.lignes[`${d.numero}-${ti}-${li}`] })),
  }));
  // La note de prix suit le dernier tableau : elle voyage collée à sa dernière ligne,
  // jamais seule en haut d'une page.
  const derniere = tableaux.at(-1).lignes.at(-1);
  derniere.h += m.blocs[`note-${d.numero}`];

  const pages = [];
  let courante = { morceaux: [], premiere: true };
  const rab = Number.isFinite(rabot) ? rabot : 0;
  let reste = CADRE_H - SECURITE - rab - entete - haut - pied;

  const nouvellePage = () => {
    courante.reste = reste + rab;   // le rabot n'est pas du vide : il revient à la page
    pages.push(courante);
    courante = { morceaux: [], premiere: false };
    reste = CADRE_H - SECURITE - rab - enteteSuite - pied;
  };

  for (const tb of tableaux) {
    let i = 0, suite = false;
    while (i < tb.lignes.length) {
      const ecart = courante.morceaux.length ? ECART_TABLEAUX : 0;
      let dispo = reste - ecart - tb.thead;
      // Un en-tête de tableau doit être suivi d'au moins deux lignes sur la même page.
      const deuxPremieres = (tb.lignes[i]?.h || 0) + (tb.lignes[i + 1]?.h || 0);
      if (dispo < Math.min(deuxPremieres, tb.lignes[i].h)) { nouvellePage(); continue; }

      const prises = [];
      while (i < tb.lignes.length && dispo - tb.lignes[i].h >= 0) {
        dispo -= tb.lignes[i].h;
        prises.push(tb.lignes[i++]);
      }
      // Jamais une ligne seule sous son en-tête : on repousse le tableau entier.
      if (prises.length === 1 && tb.lignes.length > 1 && courante.morceaux.length) {
        i -= prises.length;
        nouvellePage();
        continue;
      }
      // Pas d'orpheline non plus de l'autre côté : une dernière ligne seule part avec sa voisine.
      if (tb.lignes.length - i === 1 && prises.length > 1) {
        i--; dispo += prises.pop().h;
      }
      courante.morceaux.push({ t: tb.t, lignes: prises, suite, cle: `${d.numero}-${tb.ti}` });
      reste = dispo;
      suite = true;
      if (i < tb.lignes.length) nouvellePage();
    }
  }
  courante.reste = reste + rab;
  pages.push(courante);
  return { pages, entete, enteteSuite, haut, pied, bande };
}

function pagesDomaine(d, m, pagesParDomaine, descripteurs) {
  const { pages, bande } = decouper(d, m);
  pages.forEach((pg, i) => descripteurs.push({
    type: 'fiche', domaine: d.numero, premiere: pg.premiere, reste: pg.reste, bande,
    note: i === pages.length - 1,
    morceaux: pg.morceaux.map((mo) => ({
      tableau: Number(mo.cle.split('-')[1]), suite: mo.suite,
      lignes: mo.lignes.map((l) => Number(l.cle.split('-')[2])),
    })),
  }));
  return pages.map((pg, i) => G.page({
    region: d.region, classe: 'fiche',
    corps: `<div class="cadre">
      ${G.enteteDomaine(d, !pg.premiere)}
      ${pg.premiere ? G.hautDomaine(d, bande) : ''}
      <div class="corps-tableaux">${pg.morceaux.map((mo) =>
        tableauHtmlImport(mo.t, mo.lignes, { suite: mo.suite, cleTableau: mo.cle })).join('')}
        ${i === pages.length - 1 ? G.noteDomaine(d) : ''}
        ${pg.reste >= VIDE_MIN
          ? G.respireSol(d, Math.min(pg.reste - 5, Math.max(VIDE_MAX, pg.reste * 0.6)))
          : ''}</div>
      ${G.piedDomaine(d, pagesParDomaine)}
    </div>`,
  }));
}

/* ———————————————————————————————————————————— 3. le plan ——— */

const SALON = EDITION === 'salon';
const AVANT = 3;   // couverture, agence, sommaire

function plan(m) {
  // Premier passage : on compte les pages de chaque domaine pour connaître les folios.
  const parDomaine = new Map();
  let n = AVANT + 1;
  for (const region of REGIONS) {
    if (G.ED.ouvertures) n += 1;              // l'ouverture de région
    for (const d of catalogue.domaines.filter((x) => x.region === region)) {
      parDomaine.set(d.numero, n);
      n += decouper(d, m).pages.length;
    }
  }
  return { parDomaine, apresDomaines: n };
}

/* ————————————————————————————————————————— 4. construction ——— */

function construirePages(m) {
  const { parDomaine, apresDomaines } = plan(m);

  // Le descripteur décrit chaque page : il sert à fabriquer le PPTX à l'identique.
  const descripteurs = [{ type: 'couverture' }, { type: 'agence' }, { type: 'sommaire' }];
  const pages = [
    G.couverture(),
    G.pageAgence(),
    ...G.sommaire(parDomaine),
  ];
  for (const region of REGIONS) {
    if (G.ED.ouvertures) {
      pages.push(G.ouvertureRegion(region, parDomaine));
      descripteurs.push({ type: 'ouverture', region });
    }
    for (const d of catalogue.domaines.filter((x) => x.region === region)) {
      pages.push(...pagesDomaine(d, m, parDomaine, descripteurs));
    }
  }

  // Index : on réserve les folios, puis on remplit.
  const entrees = G.entreesIndex(parDomaine);
  // Budget mesuré : trois colonnes de la hauteur utile, en « unités de ligne ».
  const hLigne = m.blocs['idx-ligne'];
  const hTitre = m.blocs['idx-titre'] + 5;          // marge haute du titre, hors boîte
  const poidsTitre = Math.ceil(hTitre / hLigne);
  const parPage = Math.floor(3 * (CADRE_H - SECURITE - 24) / hLigne);
  const pagesIdx = G.pagesIndex(entrees, parPage, poidsTitre);
  const blocsIdx = G.blocsIndex(entrees, parPage, poidsTitre);
  pages.push(...pagesIdx);
  blocsIdx.forEach((b, i) => descripteurs.push({ type: 'index-vins', premiere: i === 0, blocs: b }));
  // Au salon, les produits à part se comptent sur les doigts d'une main : pas de page pour eux.
  if (!SALON) { pages.push(G.produitsAPart(parDomaine)); descripteurs.push({ type: 'produits' }); }
  if (G.ED.indexDomaines) { pages.push(G.indexDomaines(parDomaine)); descripteurs.push({ type: 'index-domaines' }); }

  // Un multiple de 4, en ajoutant des respirations avant la page finale.
  let total = pages.length + 1;
  const manque = (4 - (total % 4)) % 4;
  // Des pages de notes, puis la planche en coupe juste avant la page finale :
  // trois fois la même planche se lisait comme une erreur d'impression.
  for (let i = 0; i < manque; i++) {
    if (i === manque - 1) { pages.push(G.planche(0)); descripteurs.push({ type: 'planche' }); }
    else { pages.push(G.pageNotes()); descripteurs.push({ type: 'notes' }); }
  }
  pages.push(G.pageFinale());
  descripteurs.push({ type: 'finale' });

  return { pages, parDomaine, apresDomaines, descripteurs };
}

/* ——————————————————————————————————————————————— 5. rendu ——— */

async function rendre(navigateur, html, sortie, { ecran }) {
  const fichier = path.join(BUILD, path.basename(sortie).replace('.pdf', '.html'));
  fs.writeFileSync(fichier, html);
  const p = await navigateur.newPage();
  await p.goto(pathToFileURL(fichier).href, { waitUntil: 'networkidle' });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({
    path: sortie, printBackground: true, preferCSSPageSize: true,
    tagged: ecran, outline: false,
  });
  await p.close();
}

const navigateur = await chromium.launch();
console.log('· mesure des blocs dans Chromium…');
const m = await mesurer(navigateur);
console.log('· pagination…');
const { pages, parDomaine, descripteurs } = construirePages(m);
console.log(`· ${pages.length} pages (multiple de 4 : ${pages.length % 4 === 0 ? 'oui' : 'NON'})`);
console.log('· rendu écran…');
await rendre(navigateur, G.document({ pages, ecran: true }),
  path.join(DIST, `${BASE}-ecran.pdf`), { ecran: true });
console.log('· rendu imprimeur…');
await rendre(navigateur, G.document({ pages, ecran: false }),
  path.join(DIST, `${BASE}-imprimeur.pdf`), { ecran: false });
await navigateur.close();

fs.writeFileSync(path.join(BUILD, `${BASE}-plan.json`), JSON.stringify({
  pages: pages.length,
  domaines: Object.fromEntries(parDomaine),
  descripteurs,
}, null, 1));
console.log(`✓ dist/${BASE}-ecran.pdf`);
console.log(`✓ dist/${BASE}-imprimeur.pdf`);
