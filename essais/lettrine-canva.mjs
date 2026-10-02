/* Essai : quelle forme de lettrine Canva garde-t-il à l'import d'un .pptx ?
   Six variantes, une par diapositive, sur le texte du n°2. */
import fs from 'node:fs';
import pptxgen from 'pptxgenjs';

const mm = (v) => v / 25.4;
const V = '67067C', S = '46606E';
const t = JSON.parse(fs.readFileSync('data/fiches/02.json', 'utf8')).texte_source;
const pres = new pptxgen();
pres.defineLayout({ name: 'SCIO', width: mm(210), height: mm(260) });
pres.layout = 'SCIO';
const boite = { x: mm(70), y: mm(40), w: mm(95), h: mm(60), margin: 0, fontFace: 'Spectral',
  fontSize: 13, color: S, lineSpacingMultiple: 1.42, valign: 'middle' };
const titre = (s, txt) => s.addText(txt, { x: mm(20), y: mm(12), w: mm(170), h: mm(10), margin: 0,
  fontFace: 'IBM Plex Sans', fontSize: 14, bold: true, color: '000000' });
const run = (o) => [{ text: t.slice(0, 1), options: { color: V, ...o } }, { text: t.slice(1) }];

let s = pres.addSlide(); titre(s, '1. Morceau : Young Serif, 23,5 pt, violet (actuel)');
s.addText(run({ fontFace: 'Young Serif', fontSize: 23.5 }), boite);
s = pres.addSlide(); titre(s, '2. Morceau : même police, 23,5 pt, violet');
s.addText(run({ fontSize: 23.5 }), boite);
s = pres.addSlide(); titre(s, '3. Morceau : IBM Plex Sans (connue de Canva), 23,5 pt, violet');
s.addText(run({ fontFace: 'IBM Plex Sans', fontSize: 23.5 }), boite);
s = pres.addSlide(); titre(s, '4. Morceau : Young Serif, 23,5 pt, violet, gras');
s.addText(run({ fontFace: 'Young Serif', fontSize: 23.5, bold: true }), boite);
s = pres.addSlide(); titre(s, '5. Lettrine dans sa propre boîte + retrait de 1re ligne, ancré en haut');
s.addText(t.slice(0, 1), { x: mm(70), y: mm(40) - mm(4), w: mm(9), h: mm(12), margin: 0,
  fontFace: 'Young Serif', fontSize: 30, color: V, valign: 'bottom' });
s.addText(t.slice(1), { ...boite, valign: 'top', indent: 0, paraSpaceBefore: 0,
  // pptxgenjs : indentLevel non ; retrait de première ligne par espaces insécables
});
s = pres.addSlide(); titre(s, '6. Morceau : Young Serif, 23,5 pt, violet, sans interligne');
s.addText(run({ fontFace: 'Young Serif', fontSize: 23.5 }), { ...boite, lineSpacingMultiple: undefined });
await pres.writeFile({ fileName: 'essais/lettrine-canva.pptx' });
console.log('ok');
