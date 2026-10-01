/* Contrôle du .pptx livré à Canva : on relit le texte des diapositives dans le XML,
   sans passer par PowerPoint, et on vérifie que rien n'a été perdu en route. */
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { catalogue, euros } from '../src/gabarits/pieces.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
const FICHIER = path.join(RACINE, 'dist/catalogue-scio-2026-canva.pptx');
const plan = JSON.parse(fs.readFileSync(path.join(RACINE, 'build/plan.json'), 'utf8'));

const liste = execFileSync('unzip', ['-Z1', FICHIER], { encoding: 'utf8' })
  .split('\n').filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n));
const textes = liste.map((n) => {
  const xml = execFileSync('unzip', ['-p', FICHIER, n], { encoding: 'utf8' });
  return [...xml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)].map((m) => m[1]).join(' ')
    .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'");
});
const tout = textes.join('\n');

const ecarts = [];
const dire = (ok, texte) => { console.log(`  ${ok ? 'ok  ' : 'NON '} ${texte}`); if (!ok) ecarts.push(texte); };

console.log(`\n— contrôle du .pptx — ${liste.length} diapositives\n`);
dire(liste.length === plan.descripteurs.length,
  `${liste.length} diapositives, autant que de pages du PDF`);

let prix = 0, perdus = 0;
catalogue.domaines.forEach((d) => d.tableaux.forEach((t) => t.lignes.forEach((l) => {
  l.prix_centimes.forEach((c) => { prix += 1; if (!tout.includes(euros(c))) perdus += 1; });
})));
dire(perdus === 0, `${prix} prix du JSON retrouvés dans le texte des diapositives`);

const absents = catalogue.domaines.filter((d) => !tout.includes(d.nom));
dire(absents.length === 0, `les 40 domaines sont nommés${
  absents.length ? ` (manquent : ${absents.map((d) => d.numero).join(', ')})` : ''}`);

const AG = catalogue.agence;
[['message sanitaire', AG.message_sanitaire], ['contact Laurent', AG.contacts.laurent],
  ['contact Carline', AG.contacts.carline], ['adresse', AG.contacts.adresse],
  ['site', AG.contacts.site]].forEach(([nom, v]) => dire(tout.includes(v), `${nom} présent`));

const vides = textes.map((t, i) => [i + 1, t.trim().length]).filter(([, n]) => n < 20);
dire(vides.length === 0, `aucune diapositive quasi vide${
  vides.length ? ` (${vides.map(([i]) => i).join(', ')})` : ''}`);

// Les systèmes reconnaissent un PowerPoint en lisant le premier élément de l'archive :
// enfoui, le fichier n'est plus identifié et s'ouvre dans n'importe quel lecteur.
const premier = execFileSync('unzip', ['-Z1', FICHIER], { encoding: 'utf8' }).split('\n')[0];
dire(premier === '[Content_Types].xml',
  `archive rangée, elle commence par [Content_Types].xml (et non « ${premier} »)`);

const octets = fs.statSync(FICHIER).size;
dire(octets < 50 * 1024 * 1024, `${(octets / 1e6).toFixed(1)} Mo, sous la limite de 50 Mo`);

console.log(ecarts.length ? `\n— ${ecarts.length} écart(s) —\n` : '\n— tous les contrôles au vert —\n');
process.exit(ecarts.length ? 1 : 0);
