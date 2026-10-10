import { chromium } from 'playwright';
import { pathToFileURL } from 'url';

const src = pathToFileURL('build/note-restaurant.html').href;
const out = 'epreuves/catalogue-restaurant-note.pdf';
const navigateur = await chromium.launch();
const page = await navigateur.newPage();
await page.goto(src, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, format: 'A4', printBackground: true });
await navigateur.close();
console.log(`✓ ${out}`);
