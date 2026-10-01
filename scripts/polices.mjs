// Copie les polices OFL depuis node_modules/@fontsource vers src/fonts/ et écrit src/fonts/polices.css.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DEST = path.join(RACINE, 'src/fonts');

// Les deux sous-ensembles couvrent tous les glyphes français :
// « latin » porte déjà é è ê ë à â ç ô û ù î ï œ Œ É À Ç ’ « » € ° ; « latin-ext » complète (Ÿ…).
const PLAGES = {
  latin: "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD",
  'latin-ext': "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
};

const POLICES = [
  { paquet: 'young-serif', nom: 'Young Serif', graisses: [400] },
  { paquet: 'spectral', nom: 'Spectral', graisses: [400, 600], italiques: [400] },
  { paquet: 'ibm-plex-sans', nom: 'IBM Plex Sans', graisses: [400, 500, 600] },
  { paquet: 'fraunces', nom: 'Fraunces', graisses: [400, 600, 700] },
  { paquet: 'faustina', nom: 'Faustina', graisses: [400, 600], italiques: [400] },
  { paquet: 'archivo', nom: 'Archivo', graisses: [400, 500, 600] },
  { paquet: 'bricolage-grotesque', nom: 'Bricolage Grotesque', graisses: [400, 600, 700] },
  { paquet: 'literata', nom: 'Literata', graisses: [400, 600], italiques: [400] },
  { paquet: 'hanken-grotesk', nom: 'Hanken Grotesk', graisses: [400, 500, 600] },
];

fs.mkdirSync(DEST, { recursive: true });
let css = `/* Polices libres (licence OFL), copiées depuis les paquets npm @fontsource.
   Elles sont dans le dépôt : la fabrication du PDF ne dépend d'aucun accès réseau. */\n`;
let copiees = 0;

for (const p of POLICES) {
  const base = path.join(RACINE, 'node_modules/@fontsource', p.paquet, 'files');
  for (const [style, liste] of [['normal', p.graisses], ['italic', p.italiques || []]]) {
    for (const g of liste) {
      for (const sous of Object.keys(PLAGES)) {
        const fichier = `${p.paquet}-${sous}-${g}-${style}.woff2`;
        const src = path.join(base, fichier);
        if (!fs.existsSync(src)) continue;
        fs.copyFileSync(src, path.join(DEST, fichier));
        copiees++;
        css += `@font-face{font-family:'${p.nom}';font-style:${style};font-weight:${g};`
             + `src:url('./${fichier}') format('woff2');unicode-range:${PLAGES[sous]};}\n`;
      }
    }
  }
}
fs.writeFileSync(path.join(DEST, 'polices.css'), css);
console.log(`${copiees} fichiers de police copiés dans src/fonts/`);
