// Rend un fichier HTML local en PDF avec Chromium sans interface.
import { chromium } from 'playwright';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export async function rendrePdf(htmlPath, pdfPath, options = {}) {
  const navigateur = await chromium.launch();
  const page = await navigateur.newPage();
  await page.goto(pathToFileURL(path.resolve(htmlPath)).href, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: pdfPath, printBackground: true, preferCSSPageSize: true, ...options });
  await navigateur.close();
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const [, , entree, sortie] = process.argv;
  await rendrePdf(entree, sortie);
  console.log(sortie);
}
