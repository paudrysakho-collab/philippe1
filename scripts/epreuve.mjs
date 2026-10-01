// Épreuve de contrôle des tarifs : pour chaque domaine, le tableau d'origine
// recadré face à sa version recomposée depuis data/catalogue.json.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { rendrePdf } from './rendre-pdf.mjs';

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const cat = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/catalogue.json'), 'utf8'));
const index = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/recadrages/index.json'), 'utf8'));

const euros = (c) => (c / 100).toFixed(2).replace('.', ',') + ' €';
const esc = (s) => String(s ?? '').replace(/[&<>]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[ch]));

function tableau(t) {
  const cols = ['appellation', 'cuvee', 'couleur', 'millesime', 'contenance'];
  const utiles = cols.filter((c) => t.lignes.some((l) => l[c]));
  const entetes = utiles.map((c) => `<th>${{ appellation: 'Appellation', cuvee: 'Cuvée', couleur: 'Couleur', millesime: 'Millésime', contenance: 'Contenance' }[c]}</th>`).join('');
  const paliers = t.paliers.map((p) => `<th class="p">${esc(p)}</th>`).join('');
  const lignes = t.lignes.map((l) => {
    const cells = utiles.map((c) => `<td>${esc(l[c] ?? '—')}</td>`).join('');
    const prix = l.prix_centimes.map((p) => `<td class="p">${euros(p)}</td>`).join('');
    const note = l.note ? `<span class="note" title="${esc(l.note)}">●</span>` : '';
    return `<tr>${cells}${prix}<td class="n">${note}</td></tr>`;
  }).join('');
  return `<table><caption>${esc(t.intitule)}${t.famille ? ' — ' + esc(t.famille) : ''}</caption>
    <thead><tr>${entetes}${paliers}<th></th></tr></thead><tbody>${lignes}</tbody></table>`;
}

const sections = cat.domaines.map((d) => {
  const crops = (index[d.numero] || []).map(
    (f) => `<img src="../data/recadrages/${f}" alt="tableau d'origine">`).join('');
  const notes = d.tableaux.flatMap((t) => t.lignes.filter((l) => l.note).map(
    (l) => `<li><strong>${esc(l.cuvee || l.appellation)}</strong> : ${esc(l.note)}</li>`)).join('');
  return `<section>
    <h2><span class="num">${d.numero}</span> ${esc(d.nom)} <small>${esc(d.region)} · page ${d.page_source} du PDF source</small></h2>
    <div class="paire">
      <div class="col"><h3>Tableau d'origine (rendu 200 dpi)</h3>${crops || '<p>aucun recadrage</p>'}</div>
      <div class="col"><h3>Version recomposée depuis <code>data/catalogue.json</code></h3>${d.tableaux.map(tableau).join('')}
        <p class="pied">${esc(d.note_prix || 'aucune note de prix dans la source')}<br>
        Départements : ${d.departements.length ? d.departements.join(', ') : 'aucun dans la source'}</p>
        ${notes ? `<ul class="notes">${notes}</ul>` : ''}</div>
    </div></section>`;
}).join('');

const html = `<!doctype html><html lang="fr"><meta charset="utf-8"><title>Épreuve des tarifs</title>
<style>
@page { size: 420mm 297mm; margin: 12mm; }
body { font: 10pt/1.4 "DejaVu Sans", sans-serif; color: #1a1a1a; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 2mm; }
.intro { margin-bottom: 8mm; font-size: 9pt; max-width: 180mm; }
section { break-inside: avoid; break-after: page; }
h2 { font-size: 13pt; margin: 0 0 3mm; border-bottom: 1.5pt solid #67067C; padding-bottom: 1.5mm; }
h2 small { font-weight: normal; font-size: 9pt; color: #555; }
.num { display: inline-block; min-width: 9mm; background: #67067C; color: #fff; text-align: center; border-radius: 2mm; }
h3 { font-size: 8.5pt; text-transform: uppercase; letter-spacing: .04em; color: #666; margin: 0 0 2mm; font-weight: 600; }
.paire { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; align-items: start; }
.col img { width: 100%; display: block; margin-bottom: 3mm; border: .5pt solid #ccc; }
table { border-collapse: collapse; width: 100%; font-size: 7.5pt; margin-bottom: 4mm; }
caption { text-align: left; font-weight: 600; padding-bottom: 1mm; color: #67067C; }
th, td { border: .4pt solid #bbb; padding: .8mm 1.4mm; text-align: left; }
thead th { background: #E1C853; }
th.p, td.p { text-align: right; white-space: nowrap; }
td.n, th:last-child { width: 4mm; text-align: center; }
.note { color: #c0392b; }
.pied { font-size: 7.5pt; color: #444; }
.notes { font-size: 7.5pt; color: #c0392b; padding-left: 4mm; }
</style>
<h1>Épreuve de contrôle des tarifs — Agence SCIO ${esc(cat.edition)}</h1>
<p class="intro">À gauche, le tableau tel qu'il figure dans <code>sources/tarif-septembre-2026.pdf</code>, recadré
depuis le rendu à 200 dpi. À droite, la même matière recomposée depuis <code>data/catalogue.json</code>.
Les deux colonnes doivent dire exactement la même chose : appellation, cuvée, couleur, millésime, contenance,
et autant de prix que de paliers. Un point rouge signale une remarque reportée dans <code>QUESTIONS.md</code>.</p>
${sections}</html>`;

fs.mkdirSync(path.join(RACINE, 'epreuves'), { recursive: true });
const htmlPath = path.join(RACINE, 'epreuves/epreuve-tarifs.html');
fs.writeFileSync(htmlPath, html);
await rendrePdf(htmlPath, path.join(RACINE, 'epreuves/epreuve-tarifs.pdf'));
console.log('epreuves/epreuve-tarifs.pdf');
