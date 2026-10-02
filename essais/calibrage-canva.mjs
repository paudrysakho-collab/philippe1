/* Calibrage : où Canva pose-t-il la ligne de base d'une boîte de texte ancrée en haut,
   selon le corps, l'interligne et la police ? Mesuré ensuite dans l'export PDF de Canva. */
import fs from 'node:fs';
import pptxgen from 'pptxgenjs';

const mm = (v) => v / 25.4;
const t = JSON.parse(fs.readFileSync('data/fiches/16.json', 'utf8')).texte_source.slice(1);
const pres = new pptxgen();
pres.defineLayout({ name: 'SCIO', width: mm(210), height: mm(260) });
pres.layout = 'SCIO';
const CORPS = [[13, 1.42], [11, 1.42], [9.5, 1.30], [9.5, 1.42], [11, 1.36], [9.5, 1.25]];
CORPS.forEach(([b, s]) => {
  const sl = pres.addSlide();
  sl.addText(t, { x: mm(60), y: mm(40), w: mm(96), h: mm(150), margin: 0, fontFace: 'Spectral',
    fontSize: b, color: '46606E', lineSpacingMultiple: s, valign: 'top' });
  // des lettres seules, ancrées en haut à la même hauteur, à plusieurs corps
  [[23.5, 'S'], [17, 'A'], [12.5, 'P'], [30, 'D']].forEach(([l, c], i) => {
    sl.addText(c, { x: mm(8 + i * 12), y: mm(40), w: mm(11), h: mm(14), margin: 0,
      fontFace: 'Young Serif', fontSize: l, color: '67067C', valign: 'top' });
    sl.addText(c, { x: mm(8 + i * 12), y: mm(80), w: mm(11), h: mm(14), margin: 0,
      fontFace: 'Young Serif', fontSize: l, color: '67067C', valign: 'top', lineSpacingMultiple: s });
  });
});
await pres.writeFile({ fileName: 'essais/calibrage-canva.pptx' });
console.log('ok');
