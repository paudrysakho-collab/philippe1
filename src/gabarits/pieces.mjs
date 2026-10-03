/* Les pièces du système : strates, trames, carotte, pictos, tableau de prix.
   Tout est dessiné ici. Aucune bibliothèque d'icônes. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const general = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/catalogue.json'), 'utf8'));

/* ——————————————————————————————————————————————— les éditions ———
   Un seul générateur, deux éditions. `EDITION=salon` fabrique le catalogue du Salon Privé :
   les mêmes fiches, mais seulement celles des exposants, et leurs tableaux réduits aux vins
   dégustés (data/salon-prive-2026.json). Les prix du salon y vivent, vides tant que
   l'agence ne les a pas donnés. */
export const EDITION = process.env.EDITION === 'salon' ? 'salon' : 'general';
export const SALON = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/salon-prive-2026.json'), 'utf8'));

/** Le mode de prix d'un stand : « paliers » (ceux du tarif du domaine) ou « unique ». */
export const modePrix = (stand) => stand?.mode_prix || SALON.mode_prix || 'paliers';

/** Le catalogue de l'édition salon, construit depuis le catalogue général et le fichier du salon. */
function editionSalon(cat) {
  const parNumero = Object.fromEntries(cat.domaines.map((d) => [d.numero, d]));
  const standDe = {};
  SALON.stands.forEach((s) => s.vins.forEach((v) => { standDe[v.fiche] = s; }));
  const domaines = cat.domaines.filter((d) => standDe[d.numero]).map((d) => {
    const s = standDe[d.numero];
    const unique = modePrix(s) === 'unique';
    // Les vins dégustés, rangés dans le tableau du tarif d'où ils viennent (le premier s'ils
    // n'y sont pas) : chacun garde son intitulé et ses paliers.
    const parTableau = new Map();
    s.vins.filter((v) => v.fiche === d.numero).forEach((v) => {
      const ti = v.tarif ? v.tarif.tableau : 0;
      if (!parTableau.has(ti)) parTableau.set(ti, []);
      parTableau.get(ti).push(v);
    });
    const tableaux = [...parTableau.keys()].sort((a, b) => a - b).map((ti) => {
      const t = d.tableaux[ti];
      // Les paliers du salon (tarifs annotés par l'agence) quand elle les a donnés, par fiche ;
      // sinon ceux du tarif de septembre.
      const paliers = s.paliers_salon?.[`${d.numero}:${ti}`] || s.paliers_salon?.[String(d.numero)]
        || (unique ? ['Prix salon'] : t.paliers);
      return {
        intitule: t.intitule, ...(t.famille ? { famille: t.famille } : {}), paliers,
        lignes: parTableau.get(ti).map((v) => ({
          appellation: v.appellation || '', cuvee: v.cuvee, couleur: v.couleur,
          millesime: v.millesime, contenance: v.contenance,
          // null : la case reste vide ; sinon autant de prix que de colonnes, ou un seul prix
          // pour toute la ligne (un magnum à prix unique dans un tableau à paliers)
          prix_centimes: Array.isArray(v.prix_centimes)
            && (v.prix_centimes.length === paliers.length || v.prix_centimes.length === 1)
            ? v.prix_centimes : paliers.map(() => null),
          note: v.note || null, ...(v.famille ? { famille: v.famille } : {}),
          ...(v.offre ? { offre: v.offre, offre_detail: v.offre_detail || null } : {}),
        })),
      };
    });
    // Au salon, le texte de présentation est celui de la carte du stand (dossier de référence de
    // Mathéo), tel quel ; une fiche sans carte à elle (Strasser-Radziwill, Cray, Guignottes)
    // garde le sien.
    const texte = s.fiche_texte === d.numero && s.texte_reference ? { texte_source: s.texte_reference } : {};
    return { ...parNumero[d.numero], ...texte, tableaux, stand: s.stand, salle: s.salle, nom_stand: s.nom_salon,
      offre_salon: s.offre_salon || null,
      // la note de prix précisée par l'agence pour le salon (Boehler : franco de port)
      ...(s.note_prix_salon ? { note_prix: s.note_prix_salon } : {}) };
  });
  const presents = new Set(domaines.map((d) => d.numero));
  const regions = cat.agence.regions.filter((r) => domaines.some((d) => d.region === r));
  return {
    ...cat, domaines,
    agence: {
      ...cat.agence, regions,
      // un groupe de panachage garde ses membres : ceux qui ne sont pas au salon restent nommés
      groupes_panachage: cat.agence.groupes_panachage.map((g) => ({ ...g, presents: g.domaines.filter((n) => presents.has(n)) })),
    },
    salon: SALON,
  };
}

export const catalogue = EDITION === 'salon' ? editionSalon(general) : general;
/** Les noms de fichiers d'une édition : dist/<base>-ecran.pdf, build/<base>-plan.json… */
export const BASE = EDITION === 'salon' ? 'salon-prive-2026' : 'catalogue-scio-2026';

/** Les photos retenues, par domaine. Un domaine sans photo garde son dessin de sol. */
const _photos = JSON.parse(fs.readFileSync(path.join(RACINE, 'data/photos-preparees.json'), 'utf8'));
export const photos = _photos.reduce((m, p) => {
  (m[p.numero] ||= {})[p.role] = p;
  return m;
}, {});
export const photoDe = (d, role) => photos[d.numero]?.[role] || null;
/** La ligne de crédit des photographies, en dernière page : elle dit d'où elles viennent,
   ou, s'il n'y en a aucune, que les emplacements attendent encore les leurs. */
export const creditPhotos = () => {
  if (!_photos.length) {
    return "Les deux emplacements d'image de chaque fiche sont livrés vides : les photographies "
      + 'qui y seront posées restent à créditer, voir credits.md.';
  }
  const sources = [];
  if (_photos.some((p) => /site officiel/.test(p.provenance || ''))) sources.push('les sites officiels des domaines');
  if (_photos.some((p) => !/site officiel/.test(p.provenance || ''))) sources.push("la photothèque de l'agence");
  return `Les photographies des fiches viennent de ${sources.join(' et de ')} ; elles sont créditées `
    + 'une à une dans credits.md.';
};
export const REGIONS = catalogue.agence.regions;

/* ——————————————————————————————— le corps du texte de présentation ———
   La bande du haut d'une fiche fait toujours la hauteur de l'emplacement bouteille.
   Un texte court y laissait un grand vide avant le tableau : le corps grandit donc
   jusqu'à ce que le texte remplisse la bande, dans une plage étroite et jamais au-delà.
   Les deux textes les plus longs (n°16, n°17) restent au corps de base. */
const METRIQUES = JSON.parse(fs.readFileSync(path.join(RACINE, 'src/fonts/metriques.json'), 'utf8'));

export const EMPLACEMENT = { rond: 40, bouteille: { l: 24, h: 62 }, ecart: 5 };
export const CORPS_DOM = { min: 9.5, max: 13, interligne: 1.5 };
/** Largeur de la colonne de texte entre le rond et la bouteille, en millimètres. */
export const COLONNE_DOM = 170 - EMPLACEMENT.rond - EMPLACEMENT.bouteille.l - 2 * EMPLACEMENT.ecart;

/* La bande du haut peut s'abaisser : une fiche qui déborde de peu sur une seconde page
   tient alors sur une seule. La bouteille rapetisse dans ses proportions, le rond garde sa
   taille, la colonne de texte s'élargit d'autant. La pagination essaie les bandes de la plus
   haute à la plus basse et garde la plus haute qui donne le moins de pages (construire.mjs). */
export const BANDES = [62, 56, 50, 46, 44];
export function emplacementPour(bande = EMPLACEMENT.bouteille.h) {
  const k = bande / EMPLACEMENT.bouteille.h;
  const bouteille = { l: +(EMPLACEMENT.bouteille.l * k).toFixed(2), h: bande };
  const rond = Math.min(EMPLACEMENT.rond, bande);
  return { rond, bouteille, ecart: EMPLACEMENT.ecart,
    colonne: +(170 - rond - bouteille.l - 2 * EMPLACEMENT.ecart).toFixed(2) };
}

/** Largeur d'une chaîne en millimètres, d'après les chasses de la police livrée. */
export function largeurTexte(texte, face, taillePt) {
  const m = METRIQUES[face] || METRIQUES.Spectral;
  let em = 0;
  for (const c of texte) em += m.chasses[c.codePointAt(0)] ?? m.defaut;
  return em * taillePt * 25.4 / 72;
}

/** Nombre de lignes qu'occupe un texte dans une colonne de `large` millimètres. */
export function lignesTexte(texte, face, taillePt, large) {
  let n = 1, courante = '';
  for (const mot of texte.split(/\s+/)) {
    const essai = courante ? `${courante} ${mot}` : mot;
    if (largeurTexte(essai, face, taillePt) > large && courante) { n += 1; courante = mot; }
    else courante = essai;
  }
  return n;
}

/** Le corps, en points, qui fait le mieux remplir la bande sans la faire grandir. */
export function corpsDomaine(d, large = COLONNE_DOM, bande = EMPLACEMENT.bouteille.h) {
  const t = d.texte_source;
  if (!t) return CORPS_DOM.min;
  // la lettrine mange la largeur des deux premières lignes : une ligne de marge suffit
  const cible = bande - 2.5;
  for (let pt = CORPS_DOM.max; pt > CORPS_DOM.min; pt -= 0.25) {
    const h = (lignesTexte(t, 'Spectral', pt, large) + 1) * pt * CORPS_DOM.interligne * 25.4 / 72;
    if (h <= cible) return pt;
  }
  return CORPS_DOM.min;
}

export const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
export const euros = (c) => (c / 100).toFixed(2).replace('.', ',');

/** Générateur à graine fixe : un même numéro donne toujours le même dessin. */
export function graine(n) {
  let a = (n * 0x9e3779b1) >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Une couleur et une trame par région. */
export const STRATES = {
  Loire:       { c: 'var(--silex)',       hex: '#46606E', t: 'ecailles',  mot: 'schistes et tuffeau' },
  Alsace:      { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'veines',    mot: 'coteaux du Bruderthal' },
  Beaujolais:  { c: 'var(--gneiss)',      hex: '#A8515F', t: 'grains',    mot: 'le Clos des Nugues' },
  Bourgogne:   { c: 'var(--sables)',      hex: '#D08C3C', t: 'pointille', mot: 'climats et terrasses' },
  'Rhône':     { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'galets',    mot: 'sables, grès et Trias' },
  'Sud-Ouest': { c: 'var(--sables)',      hex: '#D08C3C', t: 'grains',    mot: 'sables fauves et fossiles marins' },
  Bordeaux:    { c: 'var(--gneiss)',      hex: '#A8515F', t: 'galets',    mot: 'graves et argilo-calcaire' },
  Provence:    { c: 'var(--silex)',       hex: '#46606E', t: 'pointille', mot: 'la Provence Verte' },
  Languedoc:   { c: 'var(--amphibolite)', hex: '#3C5B47', t: 'ecailles',  mot: 'terrasses et garrigue' },
  Champagne:   { c: 'var(--craie)',       hex: '#FBF8F1', t: 'pointille', mot: 'la craie' },
};

/** Trames dessinées, déclarées une fois par document. */
export function defsTrames() {
  const e = 'rgba(0,0,0,.30)';
  return `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <pattern id="t-ecailles" width="14" height="9" patternUnits="userSpaceOnUse">
    <path d="M-2 9 Q5 1 12 9 M12 9 Q19 1 26 9" fill="none" stroke="${e}" stroke-width="1.1"/></pattern>
  <pattern id="t-veines" width="26" height="14" patternUnits="userSpaceOnUse">
    <path d="M0 4 C7 1 11 9 18 6 S26 3 30 7" fill="none" stroke="${e}" stroke-width="1"/>
    <path d="M-4 11 C3 8 7 15 14 12 S22 10 26 13" fill="none" stroke="${e}" stroke-width=".7"/></pattern>
  <pattern id="t-grains" width="11" height="11" patternUnits="userSpaceOnUse">
    <circle cx="2.5" cy="3" r="1.5" fill="${e}"/><circle cx="8" cy="7.5" r="1.1" fill="${e}"/>
    <circle cx="5" cy="9.5" r=".7" fill="${e}"/></pattern>
  <pattern id="t-pointille" width="9" height="9" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r=".9" fill="${e}"/><circle cx="6.5" cy="6" r=".9" fill="${e}"/></pattern>
  <pattern id="t-galets" width="22" height="14" patternUnits="userSpaceOnUse">
    <ellipse cx="6" cy="5" rx="5" ry="3.1" fill="none" stroke="${e}" stroke-width="1"/>
    <ellipse cx="17" cy="10" rx="4.2" ry="2.6" fill="none" stroke="${e}" stroke-width="1"/></pattern>
</defs></svg>`;
}

/** Ce qu'une strate compte : les domaines du catalogue, ou les stands au salon (26 en tout). */
export const effectifs = () => REGIONS.map((n) => (EDITION === 'salon'
  ? new Set(catalogue.domaines.filter((d) => d.region === n).map((d) => d.stand)).size
  : catalogue.domaines.filter((d) => d.region === n).length));

/** Épaisseurs des strates : proportionnelles, avec un plancher pour rester lisibles. */
export function poidsStrates() {
  const e = effectifs();
  const p = e.map((n) => Math.max(n, 2.6));
  const total = p.reduce((a, b) => a + b, 0);
  return { effectifs: e, poids: p, total };
}

/** La coupe : dix strates empilées, le toit de chacune ondule. */
export function coupe({ largeur = 600, hauteur = 430, graineN = 26, etiquettes = true } = {}) {
  const r = graine(graineN);
  const { effectifs: eff, poids, total } = poidsStrates();
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * hauteur;
    const s = STRATES[nom];
    const pts = [];
    for (let x = 0; x <= largeur + 40; x += largeur / 7) pts.push(`${x} ${(y + (r() - 0.5) * 7).toFixed(1)}`);
    const d = `M-20 ${y.toFixed(1)} ${pts.map((p) => 'L' + p).join(' ')} L${largeur + 20} ${y.toFixed(1)} `
            + `L${largeur + 20} ${(y + h + 2).toFixed(1)} L-20 ${(y + h + 2).toFixed(1)} Z`;
    const clair = nom === 'Champagne';
    out += `<path d="${d}" fill="${s.hex}"/><path d="${d}" fill="url(#t-${s.t})"/>`;
    if (etiquettes) {
      out += `<text x="${largeur - 14}" y="${(y + h / 2 + 4).toFixed(1)}" text-anchor="end"
                class="etiq-strate" fill="${clair ? '#46606E' : 'rgba(255,255,255,.93)'}">${esc(nom.toUpperCase())}</text>`
           + `<text x="14" y="${(y + h / 2 + 4).toFixed(1)}" class="etiq-nb"
                fill="${clair ? '#46606E' : 'rgba(255,255,255,.72)'}">${eff[i]}</text>`;
    }
    y += h;
  });
  return `<svg viewBox="0 0 ${largeur} ${hauteur}" preserveAspectRatio="none" class="coupe"
            aria-hidden="true">${out}</svg>`;
}

/** Mélange une couleur hex vers une autre (t = 0 : la première, 1 : la seconde). */
function melange(a, b, t) {
  const v = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [x, y] = [v(a), v(b)];
  return '#' + x.map((c, i) => Math.round(c + (y[i] - c) * t).toString(16).padStart(2, '0')).join('');
}

/** La coupe « élégante » de la couverture (l'agence, 3 octobre : « des traits plus droits,
    moins enfantin, plus rêver »). Strates parfaitement horizontales, sans zigzag ni grosse
    trame ; légende sobre à gauche, comme un relevé géologique.
    style : 'aquarelle' (teintes adoucies, léger dégradé), 'fine' (bandes translucides, à poser
    sous une photo), 'gravure' (ton sur ton, hachures fines, liseré or). */
export function coupeElegante({ largeur = 600, hauteur = 430, style = 'aquarelle', etiquettes = true,
  classe = 'coupe' } = {}) {
  const { effectifs: eff, poids, total } = poidsStrates();
  let y = 0, defs = '', out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * hauteur;
    const hex = STRATES[nom].hex === '#FBF8F1' ? '#D9CDB4' : STRATES[nom].hex;
    const id = `ce-${style}-${i}`;
    if (style === 'aquarelle') {
      defs += `<linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${melange(hex, '#FBF8F1', 0.42)}"/>
        <stop offset="1" stop-color="${melange(hex, '#FBF8F1', 0.22)}"/></linearGradient>`;
      out += `<rect x="0" y="${y.toFixed(2)}" width="${largeur}" height="${(h + 0.6).toFixed(2)}" fill="url(#${id})"/>`;
      if (i) out += `<rect x="0" y="${(y - 0.4).toFixed(2)}" width="${largeur}" height=".8" fill="#FBF8F1" opacity=".85"/>`;
    } else if (style === 'fine') {
      out += `<rect x="0" y="${y.toFixed(2)}" width="${largeur}" height="${(h + 0.6).toFixed(2)}" fill="${hex}" opacity=".78"/>`;
      if (i) out += `<rect x="0" y="${(y - 0.3).toFixed(2)}" width="${largeur}" height=".6" fill="#FBF8F1" opacity=".7"/>`;
    } else {
      const fond = melange(hex, '#F2EADA', 0.62);
      defs += `<pattern id="${id}" width="${5 + (i % 3)}" height="${5 + (i % 3)}" patternUnits="userSpaceOnUse"
          patternTransform="rotate(${[35, -35, 0, 90][i % 4]})">${i % 2
        ? `<circle cx="1.5" cy="1.5" r=".55" fill="${melange(hex, '#2A3942', 0.2)}" opacity=".45"/>`
        : `<path d="M0 0 V${5 + (i % 3)}" stroke="${melange(hex, '#2A3942', 0.2)}" stroke-width=".45" opacity=".45"/>`}</pattern>`;
      out += `<rect x="0" y="${y.toFixed(2)}" width="${largeur}" height="${(h + 0.6).toFixed(2)}" fill="${fond}"/>
        <rect x="0" y="${y.toFixed(2)}" width="${largeur}" height="${(h + 0.6).toFixed(2)}" fill="url(#${id})"/>`;
      if (i) out += `<rect x="0" y="${(y - 0.5).toFixed(2)}" width="${largeur}" height="1" fill="#C9AE4A"/>`;
    }
    if (etiquettes) {
      const encre = style !== 'fine' || nom === 'Champagne' ? '#2A3942' : '#FBF8F1';
      const ym = (y + h / 2 + 3.4).toFixed(1);
      out += `<text x="18" y="${ym}" class="etiq-nb-el" fill="${encre}" opacity=".9">${eff[i]}</text>`
           + `<text x="40" y="${ym}" class="etiq-strate-el" fill="${encre}">${esc(nom.toUpperCase())}</text>`;
    }
    y += h;
  });
  return `<svg viewBox="0 0 ${largeur} ${hauteur}" preserveAspectRatio="none" class="${classe}"
            aria-hidden="true"><defs>${defs}</defs>${out}</svg>`;
}

/** La carotte de tranche : la strate de la région courante est pleine, repérée en or. */
export function carotte(regionActive) {
  const { poids, total } = poidsStrates();
  let y = 0, out = '';
  REGIONS.forEach((nom, i) => {
    const h = (poids[i] / total) * 1000;
    const s = STRATES[nom];
    const actif = nom === regionActive;
    out += `<rect x="0" y="${y.toFixed(1)}" width="40" height="${h.toFixed(1)}" fill="${s.hex}"
              opacity="${actif ? 1 : 0.3}"/>`;
    if (actif) {
      out += `<rect x="0" y="${y.toFixed(1)}" width="40" height="${h.toFixed(1)}" fill="url(#t-${s.t})"/>`
           + `<rect x="0" y="${y.toFixed(1)}" width="7" height="${h.toFixed(1)}" fill="#E1C853"/>`;
    }
    out += `<rect x="0" y="${(y + h - 1).toFixed(1)}" width="40" height="1" fill="#F2EADA" opacity=".7"/>`;
    y += h;
  });
  return `<svg viewBox="0 0 40 1000" preserveAspectRatio="none" aria-hidden="true">${out}</svg>`;
}

/** Vue en coupe du sol d'un domaine : un disque de carotte, tiré de son numéro. */
export function carotteRonde(d, taille = 120) {
  const r = graine(d.numero * 7);
  const s = STRATES[d.region];
  const couches = ['#D08C3C', s.hex, '#46606E', '#A8515F'];
  let out = `<circle cx="60" cy="60" r="58" fill="#FBF8F1"/>`;
  let y = 2;
  couches.forEach((col, i) => {
    const h = 20 + r() * 18;
    out += `<path d="M2 ${y.toFixed(1)} Q30 ${(y - 5 + r() * 10).toFixed(1)} 60 ${(y + 2).toFixed(1)}
              T118 ${y.toFixed(1)} L118 ${(y + h).toFixed(1)} Q90 ${(y + h + 4).toFixed(1)} 60 ${(y + h - 2).toFixed(1)}
              T2 ${(y + h).toFixed(1)} Z" fill="${col}" opacity="${(0.55 + i * 0.12).toFixed(2)}"/>`;
    y += h;
  });
  out += `<circle cx="60" cy="60" r="58" fill="url(#t-${s.t})" opacity=".5"/>`
       + `<circle cx="60" cy="60" r="58" fill="none" stroke="#46606E" stroke-width="2.5"/>`;
  return `<svg viewBox="0 0 120 120" class="rond-sol" aria-hidden="true">${out}</svg>`;
}

/* ——— Pictos maison. Ils ne reprennent la forme d'aucun logo officiel. ——— */
export const PICTOS = {
  blanc: `<circle cx="7" cy="7" r="5.4" fill="#FBF8F1" stroke="#46606E" stroke-width="1.2"/>`,
  rouge: `<circle cx="7" cy="7" r="5.4" fill="#A8515F"/>`,
  rose: `<path d="M7 1.6 A5.4 5.4 0 0 1 7 12.4 Z" fill="#D98FA0"/><circle cx="7" cy="7" r="5.4" fill="none" stroke="#A8515F" stroke-width="1.2"/>`,
  bulles: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#46606E" stroke-width="1.2"/><circle cx="5" cy="8" r="1.3" fill="#46606E"/><circle cx="9" cy="6.4" r="1.1" fill="#46606E"/><circle cx="7.4" cy="4.2" r=".9" fill="#46606E"/>`,
  doux: `<circle cx="7" cy="7" r="5.4" fill="#E1C853"/>`,
  sansalcool: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#3C5B47" stroke-width="1.2"/><path d="M3.6 10.4 L10.4 3.6" stroke="#3C5B47" stroke-width="1.2"/>`,
  jus: `<circle cx="7" cy="7" r="5.4" fill="#3C5B47"/>`,
  biere: `<circle cx="7" cy="7" r="5.4" fill="#D08C3C"/>`,
  spiritueux: `<rect x="2.2" y="2.2" width="9.6" height="9.6" fill="#8A6230"/>`,
  autre: `<circle cx="7" cy="7" r="5.4" fill="none" stroke="#46606E" stroke-width="1.2" stroke-dasharray="2 2"/>`,
};
export const NOM_FAMILLE = {
  blanc: 'Blanc', rouge: 'Rouge', rose: 'Rosé', bulles: 'Bulles', doux: 'Doux',
  sansalcool: 'Sans alcool', jus: 'Jus de cépages', biere: 'Bière', spiritueux: 'Spiritueux', autre: 'Autre',
};
export const picto = (f, cls = 'picto') =>
  `<svg viewBox="0 0 14 14" class="${cls}" aria-hidden="true">${PICTOS[f] || PICTOS.autre}</svg>`;

/* ——— Pictos de label : une feuille, toujours la même. Le remplissage dit le label, il se
   lit en niveaux de gris, et il ne ressemble à aucun logo officiel (AB, HVE, Demeter…).
   Le libellé est toujours écrit à côté : le picto ne remplace jamais le mot. ——— */
const FEUILLE = 'M7 1.3 C11.4 3.6 11.4 10.4 7 12.7 C2.6 10.4 2.6 3.6 7 1.3 Z';
const DEMI = 'M7 1.3 C11.4 3.6 11.4 10.4 7 12.7 Z';
const V = '#3C5B47';
export const PICTOS_LABELS = {
  bio: `<path d="${FEUILLE}" fill="${V}"/>`,
  conversion: `<path d="${DEMI}" fill="${V}"/><path d="${FEUILLE}" fill="none" stroke="${V}" stroke-width="1.2"/>`,
  biodynamie: `<path d="${FEUILLE}" fill="none" stroke="${V}" stroke-width="1.2"/><circle cx="7" cy="7" r="1.9" fill="${V}"/>`,
  biobiodyn: `<path d="${FEUILLE}" fill="${V}"/><circle cx="7" cy="7" r="1.9" fill="#FBF8F1"/>`,
  hve: `<path d="${FEUILLE}" fill="none" stroke="${V}" stroke-width="1.2"/><path d="M7 3.2 V10.8" stroke="${V}" stroke-width="1.2"/>`,
  raisonnee: `<path d="${FEUILLE}" fill="none" stroke="${V}" stroke-width="1.2"/><path d="M4.6 7 H9.4" stroke="${V}" stroke-width="1.2"/>`,
  iso: `<path d="${FEUILLE}" fill="none" stroke="${V}" stroke-width="1.2" stroke-dasharray="1.6 1.2"/>`,
};
/** Le picto d'un libellé de label. AOP et IGP disent une origine, pas une pratique : pas de feuille. */
export function familleLabel(libelle) {
  const l = (libelle || '').toLowerCase();
  if (l.includes('conversion')) return 'conversion';
  if (l.includes('bio') && l.includes('biodynamie')) return 'biobiodyn';
  if (l.includes('biodynamie') || l.includes('demeter') || l.includes('biodyvin')) return 'biodynamie';
  if (l === 'bio') return 'bio';
  if (l.startsWith('hve')) return 'hve';
  if (l.includes('raisonnée')) return 'raisonnee';
  if (l.includes('iso')) return 'iso';
  return null;
}
export const pictoLabel = (libelle, cls = 'picto picto-label') => {
  const f = familleLabel(libelle);
  return f ? `<svg viewBox="0 0 14 14" class="${cls}" aria-hidden="true">${PICTOS_LABELS[f]}</svg>` : '';
};
/** Les libellés de label réellement affichés, dans l'ordre de la légende. */
export const ORDRE_LABELS = ['Bio', 'En conversion Bio', 'Biodynamie', 'Bio & Biodynamie',
  'HVE', 'HVE 3', 'Agriculture raisonnée', 'ISO 26000'];

/** Famille d'une ligne : lue dans la source, jamais devinée au-delà de ce qu'elle écrit. */
export function famille(ligne, tableau) {
  if (ligne.famille) return ligne.famille;          // donnée explicitement (édition salon)
  const f = (tableau.famille || '').toLowerCase();
  if (f.includes('jus')) return 'jus';
  if (f.includes('bière')) return 'biere';
  if (f.includes('armagnac') || f.includes('ratafia')) return 'spiritueux';
  const c = (ligne.couleur || '').toLowerCase();
  const a = (ligne.appellation || '').toLowerCase();
  if (a.includes('sans alcool')) return 'sansalcool';
  if (a.includes('armagnac') || a.includes('ratafia')) return 'spiritueux';
  if (c.includes('bulle') || c.includes('pétillant') || c.includes('effervescent') || c.includes('brut') || c.includes('champagne')
      || a.includes('champagne') || a.includes('crémant') || a.includes('méthode')) return 'bulles';
  if (c.includes('doux') || c.includes('moelleux') || c.includes('liquoreux') || c.includes('demi-sec')) return 'doux';
  if (c.includes('ros') || c.includes('clairet')) return 'rose';
  if (c.includes('rouge')) return 'rouge';
  if (c.includes('blanc')) return 'blanc';
  return 'autre';
}

export const nbReferences = (d) => d.tableaux.reduce((n, t) => n + t.lignes.length, 0);

/** Les familles présentes dans un domaine, dans l'ordre de la légende. */
export function famillesDe(d) {
  const ordre = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux', 'autre'];
  const vues = new Set();
  d.tableaux.forEach((t) => t.lignes.forEach((l) => vues.add(famille(l, t))));
  return ordre.filter((f) => vues.has(f));
}

/** Une ligne de tableau. `idx` sert au repérage lors de la passe de mesure. */
/** Une cuvée qui passe à la ligne n'y laisse jamais un mot seul : les deux derniers mots
    restent ensemble, et un mot composé (Extra-Brut, Saint-Chinian) ne se coupe pas. */
export function sansVeuve(texte) {
  const mots = String(texte ?? '').split(' ');
  const bloc = (m) => (m.includes('-') ? `<span class="insecable">${esc(m)}</span>` : esc(m));
  if (mots.length < 3) return mots.map(bloc).join(' ');
  return `${mots.slice(0, -2).map(bloc).join(' ')} ${bloc(mots.at(-2))}&nbsp;${bloc(mots.at(-1))}`;
}

export function ligneHtml(l, t, cle) {
  // Un prix absent (édition salon, avant que l'agence ne les donne) laisse une case vide.
  // Un seul prix sur une ligne à plusieurs paliers : il vaut pour toute la ligne.
  const seul = l.prix_centimes.length === 1 && t.paliers.length > 1;
  const prix = l.prix_centimes.map((p) => (p == null
    ? '<div class="cel-prix vide"></div>'
    : `<div class="cel-prix${seul ? ' seul' : ''}">${euros(p)}<span>€</span></div>`)).join('');
  const etoile = l.note === '*' ? ' <span class="etoile">*</span>' : '';
  // L'offre du salon (11+1, 5+1) suit le nom du vin.
  const offre = l.offre ? ` <span class="offre">offre&nbsp;${esc(l.offre)}${l.offre_detail
    ? ' ' + esc(l.offre_detail).replace(/ (\S+)$/, '&nbsp;$1') : ''}</span>` : '';
  return `<tr data-ligne="${cle}">
    <td class="c-picto">${picto(famille(l, t))}</td>
    <td class="c-vin"><span class="app">${esc(l.appellation)}${etoile}${l.cuvee ? '' : offre}</span>
      ${l.cuvee ? `<span class="cuv">${sansVeuve(l.cuvee)}${offre}</span>` : ''}</td>
    <td class="c-detail">${esc(l.millesime || '—')}</td>
    <td class="c-detail">${t.paliers.length > 1
      // dans un tableau à paliers, « Magnum 1,5 L » passe sur deux lignes au lieu de mordre sur les prix
      ? esc(l.contenance || '—').replace(/^Magnum /, 'Magnum<br>') : esc(l.contenance || '—')}</td>
    <td class="c-bloc"><div class="bloc-prix">${prix}</div></td></tr>`;
}

/** Un tableau, ou une tranche de tableau quand il se poursuit sur la page suivante. */
export function tableauHtml(t, lignes, { suite = false, cleTableau = '' } = {}) {
  const paliers = t.paliers.map((p) => `<div class="cel-pal">${esc(p)}</div>`).join('');
  const titre = esc(t.intitule) + (t.famille ? ' · ' + esc(t.famille) : '') + (suite ? ' (suite)' : '');
  // Quatre paliers : le bloc de prix s'élargit pour que les intitulés tiennent.
  return `<table class="tarif${t.paliers.length > 3 ? ' p4' : ''}" data-tableau="${cleTableau}">
    <colgroup><col style="width:6.5mm"><col><col style="width:17mm"><col style="width:16mm">
      <col style="width:var(--bloc-prix)"></colgroup>
    <thead><tr class="bandeau"><th colspan="4" class="intit">${titre}</th>
      <th class="c-bloc"><div class="bloc-prix entete">${paliers}</div></th></tr></thead>
    <tbody>${lignes.map((l) => ligneHtml(l.l, t, l.cle)).join('')}</tbody></table>`;
}

/** Légende des pictos, limitée aux familles réellement présentes. */
export function legendeHtml(familles) {
  return `<div class="legende">${familles.map((f) =>
    `<span>${picto(f)} ${esc(NOM_FAMILLE[f])}</span>`).join('')}
    <span class="legende-note">pictos de l'Agence SCIO, pas les logos officiels</span></div>`;
}

/** Les groupes de panachage entre domaines. */
export const groupes = catalogue.agence.groupes_panachage;
export const groupeDe = (d) => groupes.find((g) => g.id === d.panachage_groupe) || null;
