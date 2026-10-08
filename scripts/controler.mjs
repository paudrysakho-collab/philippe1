/* Contrôle mécanique du catalogue construit.
   Il ne remplace pas le regard : il attrape ce que l'œil rate. */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { catalogue, BASE, EDITION } from '../src/gabarits/pieces.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
const SALON = EDITION === 'salon';
const HTML = path.join(RACINE, `build/${BASE}-ecran.html`);
const PDF = path.join(RACINE, `dist/${BASE}-ecran.pdf`);
const PDF_IMP = path.join(RACINE, `dist/${BASE}-imprimeur.pdf`);

let erreurs = 0;
const dire = (ok, texte) => { if (!ok) erreurs++; console.log(`${ok ? '  ok  ' : ' ÉCHEC'} ${texte}`); };

/* ——— 1. Débordements et corps de texte, mesurés dans Chromium ——— */
const navigateur = await chromium.launch();
const p = await navigateur.newPage();
await p.goto(pathToFileURL(HTML).href, { waitUntil: 'networkidle' });
await p.emulateMedia({ media: 'print' });

const visuel = await p.evaluate(() => {
  const MM = 96 / 25.4;
  const debordements = [], petits = [];
  document.querySelectorAll('.page').forEach((page) => {
    const n = page.dataset.page;
    const cadre = page.querySelector('.cadre');
    if (cadre) {
      const c = cadre.getBoundingClientRect();
      const signales = [];
      cadre.querySelectorAll('*').forEach((el) => {
        if (el.closest('.respire-sol, .trame, svg')) return;
        if (signales.some((a) => a.contains(el))) return;   // un seul signalement par branche
        const r = el.getBoundingClientRect();
        if (r.height === 0 && r.width === 0) return;
        const bas = (r.bottom - c.bottom) / MM;
        const droite = (r.right - c.right) / MM;
        const gauche = (c.left - r.left) / MM;
        if (bas > 0.6 || droite > 0.6 || gauche > 0.6) {
          signales.push(el);
          debordements.push({ page: n, el: el.className || el.tagName,
            bas: +bas.toFixed(1), droite: +droite.toFixed(1), gauche: +gauche.toFixed(1) });
        }
      });
    }
    page.querySelectorAll('td, .texte-dom, p, li, dd, .idx-ligne').forEach((el) => {
      if (!el.textContent.trim()) return;
      const pt = parseFloat(getComputedStyle(el).fontSize) * 0.75;
      const plancher = el.closest('table.tarif') || el.closest('.idx-flux') ? 6.5 : 7.5;
      if (pt < plancher - 0.01) petits.push({ page: n, el: el.className || el.tagName, pt: +pt.toFixed(2) });
    });
  });
  return { debordements, petits, pages: document.querySelectorAll('.page').length };
});
await navigateur.close();

console.log(`\n— contrôle du catalogue — ${visuel.pages} pages\n`);
dire(visuel.debordements.length === 0,
  `aucun débordement hors cadre${visuel.debordements.length ? ` (${visuel.debordements.length})` : ''}`);
visuel.debordements.slice(0, 12).forEach((d) =>
  console.log(`         p.${d.page} « ${d.el} » bas ${d.bas} mm · droite ${d.droite} · gauche ${d.gauche}`));
dire(visuel.petits.length === 0,
  `aucun texte sous le plancher de corps${visuel.petits.length ? ` (${visuel.petits.length})` : ''}`);
visuel.petits.slice(0, 8).forEach((d) => console.log(`         p.${d.page} « ${d.el} » ${d.pt} pt`));

/* ——— 2. Pages, polices, poids ——— */
const info = execFileSync('pdfinfo', [PDF_IMP]).toString();
const nbPages = +(/Pages:\s+(\d+)/.exec(info)?.[1] || 0);
dire(nbPages % 4 === 0, `${nbPages} pages, multiple de 4`);
const taille = /Page size:\s+([\d.]+) x ([\d.]+)/.exec(info);
dire(!!taille, `format imprimeur ${taille ? `${(taille[1] / 72 * 25.4).toFixed(1)} × ${(taille[2] / 72 * 25.4).toFixed(1)} mm (fond perdu 3 mm)` : '?'}`);

const polices = execFileSync('pdffonts', [PDF_IMP]).toString().trim().split('\n').slice(2);
const nonEmbarquees = polices.filter((l) => l.slice(0, 90).includes(' no '));
dire(nonEmbarquees.length === 0, `${polices.length} polices, toutes incorporées`);
nonEmbarquees.forEach((l) => console.log('         ' + l.trim()));

for (const f of [PDF, PDF_IMP]) {
  const mo = fs.statSync(f).size / 1e6;
  dire(mo < 50, `${path.basename(f)} : ${mo.toFixed(1)} Mo`);
}

/* ——— 3. Chaque prix du JSON se retrouve-t-il dans le texte du PDF ? ——— */
const texte = execFileSync('pdftotext', [PDF, '-']).toString();
// Au salon, un prix pas encore donné (null) est une case vide attendue, pas un prix perdu.
const manquants = [];
let total = 0, attendus = 0;
for (const d of catalogue.domaines) {
  for (const t of d.tableaux) {
    for (const l of t.lignes) {
      for (const c of l.prix_centimes) {
        if (c == null) { attendus++; continue; }
        total++;
        const s = (c / 100).toFixed(2).replace('.', ',');
        if (!texte.includes(s)) manquants.push(`n°${d.numero} ${l.cuvee || l.appellation} — ${s} €`);
      }
    }
  }
}
dire(manquants.length === 0, `${total} prix du JSON retrouvés dans le texte du PDF`
  + (attendus ? ` (${attendus} cases de prix encore vides, en attente des prix de l'agence)` : ''));
manquants.slice(0, 10).forEach((m) => console.log('         ' + m));

/* ——— 4. Les mentions obligatoires ——— */
const obligatoires = [
  ["message sanitaire", catalogue.agence.message_sanitaire.slice(0, 40)],
  ["contact Laurent", catalogue.agence.contacts.laurent],
  ["contact Carline", catalogue.agence.contacts.carline],
  ["adresse", 'Rezé'],
  ["site", catalogue.agence.contacts.site],
  ["RCS", '843 151 663'],
  ...(SALON ? [["nom du salon", catalogue.salon.evenement.nom], ["date du salon", catalogue.salon.evenement.date_texte],
    ["lieu du salon", catalogue.salon.evenement.lieu]]
    // catalogue caviste global : la couverture du salon, avec ses dates de validité (8 octobre)
    : EDITION === 'global' ? [["titre", 'Vins & Terroirs'], ["validité du tarif", "jusqu'au 31 décembre 2026"],
      ["validité des offres", 'du 5 octobre au 14 novembre 2026']]
    : [["cible", 'Vendée (85)']]),
];
obligatoires.forEach(([nom, aiguille]) =>
  dire(texte.toUpperCase().includes(aiguille.toUpperCase()), `${nom} présent dans le PDF`));

/* ——— 4 bis. La couche texte n'est-elle pas fragmentée par l'interlettrage ? ——— */
const motsEntiers = ['BORDEAUX', 'BOURGOGNE', 'LANGUEDOC', 'CHAMPAGNE', 'POSSIBILITÉ DE PANACHER',
  SALON ? 'Salon Privé' : EDITION === 'global' ? 'Vins & Terroirs' : 'Tarifs cavistes Vendée (85)', 'SUD-OUEST'];
// Les capitales sont parfois produites par CSS : on compare en majuscules.
const hautTexte = texte.toUpperCase();
const fragmentes = motsEntiers.filter((m) => !hautTexte.includes(m.toUpperCase()));
dire(fragmentes.length === 0, `couche texte non fragmentée (Ctrl+F fonctionne)`);
fragmentes.forEach((m) => console.log(`         introuvable : « ${m} »`));

/* ——— 5. Les 40 domaines sont-ils tous imprimés ? ——— */
const absents = catalogue.domaines.filter((d) => !texte.includes(d.nom.split(' /')[0]));
dire(absents.length === 0, `les ${catalogue.domaines.length} domaines sont imprimés`);
if (SALON) {
  // chaque stand du plan a sa fiche, et chaque vin dégusté est dans le PDF
  const stands = new Set(catalogue.domaines.map((d) => d.stand));
  dire(stands.size === catalogue.salon.evenement.exposants,
    `les ${catalogue.salon.evenement.exposants} stands ont leur fiche (${stands.size} trouvés)`);
  // un nom coupé en fin de ligne sur son trait d'union (« Extra-Brut ») perd ce trait dans
  // la couche texte : on compare sans espaces ni traits d'union
  const net = (t) => t.replace(/[\s\-‐]+/g, '');
  const plat = net(texte);
  const perdus = catalogue.domaines.flatMap((d) => d.tableaux.flatMap((t) => t.lignes))
    .filter((l) => !plat.includes(net(l.cuvee || l.appellation)));
  dire(perdus.length === 0, `chaque vin dégusté est imprimé${perdus.length ? ` (${perdus.length} manquent)` : ''}`);
  perdus.slice(0, 8).forEach((l) => console.log(`         ${l.cuvee || l.appellation}`));
}
absents.forEach((d) => console.log(`         n°${d.numero} ${d.nom}`));

console.log(`\n${erreurs ? `— ${erreurs} contrôle(s) en échec —` : '— tous les contrôles au vert —'}\n`);
process.exit(erreurs ? 1 : 0);
