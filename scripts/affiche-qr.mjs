/* Affiche A4 du QR code : il mène au catalogue du Salon Privé (Drive de l'agence).
   Version sobre en encre (l'agence) : fond blanc, logo, titre, QR code, une ligne.
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
  html, body { margin: 0; background: #fff; }
  .a { width: 210mm; height: 297mm; box-sizing: border-box; padding: 22mm 18mm 10mm;
    display: flex; flex-direction: column; align-items: center; text-align: center; background: #fff; }
  .logo { width: 70mm; display: block; }
  h1 { margin: 16mm 0 0; font: 400 40pt/1 var(--titre); color: var(--violet); }
  .sous { margin-top: 5mm; font: 400 20pt var(--titre); color: var(--encre); }
  .qr { display: block; margin-top: 14mm; width: 120mm; height: 120mm; }
  .qr img { width: 100%; height: 100%; display: block; image-rendering: pixelated; }
  .scan { margin-top: 10mm; font: 400 20pt var(--titre); color: var(--violet); }
  .sanitaire-a { margin-top: auto; font: 400 7pt var(--technique); color: var(--encre);
    text-transform: uppercase; letter-spacing: .04em; }
</style></head><body><div class="a">
  <img class="logo" src="../src/images/logo-agence-scio-detoure.png" alt="Agence SCIO Vins &amp; Spirits">
  <h1>Salon Privé<br>Vins &amp; Terroirs</h1>
  <div class="sous">Le catalogue du salon</div>
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
