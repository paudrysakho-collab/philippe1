/* Collecte les images du site officiel de chaque domaine.
   On ne prend que des images. Aucun texte, aucun chiffre : le contenu reste celui du PDF. */
import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const RACINE = path.resolve(import.meta.dirname, '..');
const SITES = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/sites-domaines.json'), 'utf8'));
const BRUT = path.join(RACINE, 'src/photos/brut');
fs.mkdirSync(BRUT, { recursive: true });

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
  + '(KHTML, like Gecko) Chrome/125.0 Safari/537.36';

/** Pages à visiter en plus de l'accueil : là où vivent les portraits et les bouteilles. */
const PISTES = [/vin/i, /bouteille/i, /cuv[ée]/i, /gamme/i, /domaine/i, /maison/i, /famille/i,
  /qui-sommes/i, /about/i, /histoire/i, /equipe/i, /[ée]quipe/i, /boutique/i, /shop/i,
  /produit/i, /nos-/i, /chai/i, /vigneron/i];

async function imagesDe(page) {
  return page.evaluate(() => {
    const vues = new Map();
    const pousser = (u, l, h) => {
      if (!u || u.startsWith('data:')) return;
      try { u = new URL(u, location.href).href; } catch { return; }
      const a = vues.get(u);
      if (!a || (l * h) > (a.l * a.h)) vues.set(u, { url: u, l: l || 0, h: h || 0 });
    };
    document.querySelectorAll('img').forEach((im) => {
      // srcset : on garde la plus grande variante annoncée
      let meilleure = im.currentSrc || im.src;
      let largeur = im.naturalWidth;
      (im.getAttribute('srcset') || '').split(',').forEach((p) => {
        const [u, d] = p.trim().split(/\s+/);
        const w = d && d.endsWith('w') ? parseInt(d) : 0;
        if (u && w > largeur) { meilleure = u; largeur = w; }
      });
      pousser(meilleure, largeur || im.naturalWidth, im.naturalHeight);
      pousser(im.getAttribute('data-src'), im.naturalWidth, im.naturalHeight);
    });
    document.querySelectorAll('*').forEach((el) => {
      const b = getComputedStyle(el).backgroundImage;
      const m = b && b.match(/url\(["']?(.*?)["']?\)/);
      if (m) pousser(m[1], el.clientWidth, el.clientHeight);
    });
    document.querySelectorAll('meta[property="og:image"], link[rel*="icon"]').forEach((m) =>
      pousser(m.getAttribute('content') || m.getAttribute('href'), 0, 0));
    return [...vues.values()];
  });
}

async function liens(page, origine) {
  return page.evaluate((orig) => {
    const out = new Set();
    document.querySelectorAll('a[href]').forEach((a) => {
      try {
        const u = new URL(a.href, location.href);
        if (u.origin === orig) out.add(u.href.split('#')[0]);
      } catch {}
    });
    return [...out];
  }, origine);
}

const numeros = Object.keys(SITES).filter((k) => !k.startsWith('_'));
const navigateur = await chromium.launch();
const inventaire = {};

for (const n of numeros) {
  const site = SITES[n].site;
  const dossier = path.join(BRUT, `d${String(n).padStart(2, '0')}`);
  fs.mkdirSync(dossier, { recursive: true });
  const ctx = await navigateur.newContext({ userAgent: UA, viewport: { width: 1600, height: 1200 } });
  const page = await ctx.newPage();
  const trouvees = new Map();
  let titre = '';
  try {
    await page.goto(site, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2500);
    titre = await page.title();
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1500);
    (await imagesDe(page)).forEach((i) => trouvees.set(i.url, i));

    const origine = new URL(site).origin;
    const tous = await liens(page, origine);
    const retenus = tous.filter((u) => PISTES.some((r) => r.test(u))).slice(0, 7);
    for (const u of retenus) {
      try {
        await page.goto(u, { waitUntil: 'domcontentloaded', timeout: 25000 });
        await page.waitForTimeout(1800);
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
        await page.waitForTimeout(1200);
        (await imagesDe(page)).forEach((i) => { if (!trouvees.has(i.url)) trouvees.set(i.url, i); });
      } catch {}
    }
  } catch (e) {
    console.log(`n°${n} : ${e.message.split('\n')[0]}`);
  }
  await ctx.close();

  inventaire[n] = { site, titre, images: [...trouvees.values()] };
  console.log(`n°${String(n).padStart(2)} ${titre.slice(0, 44).padEnd(46)} ${trouvees.size} images`);
}
await navigateur.close();
fs.writeFileSync(path.join(RACINE, 'data/images-moissonnees.json'),
  JSON.stringify(inventaire, null, 1));
console.log('→ data/images-moissonnees.json');
