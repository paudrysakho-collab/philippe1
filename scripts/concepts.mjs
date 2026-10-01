// Fabrique les maquettes des concepts : HTML -> PDF (Chromium) -> PNG (pdftoppm).
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { rendrePdf } from './rendre-pdf.mjs';

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SORTIE = path.join(RACINE, 'concepts');
fs.mkdirSync(SORTIE, { recursive: true });

const CONCEPTS = [
  { id: 'c1-sous-nos-pieds', titre: 'Sous nos pieds' },
  { id: 'c2-chant-des-lunes', titre: 'Le Chant des Lunes' },
  { id: 'c3-caisse-panachee', titre: 'La Caisse Panachée' },
];

const seul = process.argv[2];
for (const c of CONCEPTS) {
  if (seul && c.id !== seul) continue;
  const mod = path.join(RACINE, 'src/concepts', `${c.id}.mjs`);
  if (!fs.existsSync(mod)) { console.log(`— ${c.id} : pas encore écrit`); continue; }
  const { construire } = await import(mod + `?v=${Date.now()}`);
  const html = path.join(SORTIE, `${c.id}.html`);
  fs.writeFileSync(html, construire());
  const pdf = path.join(SORTIE, `${c.id}.pdf`);
  await rendrePdf(html, pdf, { width: '420mm', height: '260mm' });
  execFileSync('pdftoppm', ['-r', '150', '-png', '-singlefile', pdf, path.join(SORTIE, c.id)]);
  console.log(`✓ ${c.titre} → concepts/${c.id}.png`);
}
