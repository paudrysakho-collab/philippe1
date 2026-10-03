/* Affiche A4 du QR code : il mène au catalogue du Salon Privé (Drive de l'agence).
   Même univers que la couverture : photo du Sud-Ouest, titre craie et or, violet de l'agence.
   Usage : npm run affiche-qr → dist/salon-prive-2026-affiche-qr.pdf */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';

const RACINE = path.resolve(import.meta.dirname, '..');
const LIEN = 'https://drive.google.com/file/d/18jcYYdNBDIZzRgf84NML8M3eGpujcJ6b/view?usp=sharing';
const SANITAIRE = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/agence.json'), 'utf8')).message_sanitaire
  || "L'abus d'alcool est dangereux pour la santé. À consommer avec modération.";
const SORTIE = path.join(RACINE, 'dist/salon-prive-2026-affiche-qr.pdf');

const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="../src/styles/systeme.css">
<style>
  @page { size: 210mm 297mm; margin: 0; }
  html, body { margin: 0; background: var(--craie); }
  .a { position: relative; width: 210mm; height: 297mm; overflow: hidden; background: var(--craie); }
  .ciel { position: absolute; inset: 0 0 auto 0; height: 118mm; }
  .ciel img { width: 100%; height: 100%; object-fit: cover; display: block; }
  .ciel::after { content: ''; position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(42,57,66,.55) 0%, rgba(42,57,66,.15) 55%, rgba(42,57,66,.35) 100%); }
  .logo { position: absolute; z-index: 2; left: 18mm; top: 14mm; background: var(--craie);
    border-radius: 1.5mm; padding: 4mm 5mm; }
  .logo img { width: 62mm; display: block; }
  h1 { position: absolute; z-index: 2; left: 18mm; top: 52mm; margin: 0;
    font: 400 46pt/0.95 var(--titre); color: var(--craie); }
  h1 em { font-style: normal; color: var(--or); }
  .bande { position: absolute; left: 0; right: 0; top: 118mm; height: 3mm; background: var(--or); }
  .sous { position: absolute; left: 0; right: 0; top: 132mm; text-align: center;
    font: 400 22pt var(--titre); color: var(--violet); }
  .qr { position: absolute; left: 50%; top: 150mm; transform: translateX(-50%);
    width: 96mm; height: 96mm; padding: 5mm; background: #fff; border-radius: 2mm;
    border: 1.2mm solid var(--violet); }
  .qr img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
  .scan { position: absolute; left: 0; right: 0; top: 260mm; text-align: center;
    font: 400 20pt var(--titre); color: var(--encre); }
  .sanitaire-a { position: absolute; left: 0; right: 0; bottom: 8mm; text-align: center;
    font: 400 7pt var(--technique); color: var(--encre); text-transform: uppercase; letter-spacing: .04em; }
</style></head><body><div class="a">
  <div class="ciel"><img src="../src/photos/regions/Sud-Ouest.jpg" alt=""></div>
  <div class="logo"><img src="../src/images/logo-agence-scio-detoure.png" alt="Agence SCIO Vins &amp; Spirits"></div>
  <h1>Salon Privé<br><em>Vins &amp; Terroirs</em></h1>
  <div class="bande"></div>
  <div class="sous">Le catalogue du Salon Privé</div>
  <a class="qr" href="${LIEN}"><img src="../src/images/qr-catalogue-salon.png" alt="QR code du catalogue"></a>
  <div class="scan">Scannez pour découvrir le catalogue</div>
  <div class="sanitaire-a">${SANITAIRE}</div>
</div></body></html>`;

fs.mkdirSync(path.join(RACINE, 'build'), { recursive: true });
const fichier = path.join(RACINE, 'build/affiche-qr.html');
fs.writeFileSync(fichier, html);
const nav = await chromium.launch();
const p = await nav.newPage();
await p.goto(pathToFileURL(fichier).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: SORTIE, printBackground: true, preferCSSPageSize: true });
await nav.close();
console.log(`✓ ${path.relative(RACINE, SORTIE)}`);
