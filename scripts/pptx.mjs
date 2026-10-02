/* Fabrique le catalogue en .pptx, importable dans Canva, texte et tableaux modifiables.
   Même contenu, même pagination et même maquette que le PDF : tout vient de build/plan.json.
   Les deux emplacements d'image prennent l'image préparée quand il y en a une
   (data/photos-preparees.json) ; sinon ce sont des formes vides, à remplacer dans Canva. */
import fs from 'node:fs';
import path from 'node:path';
import PptxGenJS from 'pptxgenjs';
import {
  catalogue, REGIONS, STRATES, euros, famille, famillesDe, nbReferences, NOM_FAMILLE,
  groupes, groupeDe, corpsDomaine, EMPLACEMENT, COLONNE_DOM, photoDe, creditPhotos,
} from '../src/gabarits/pieces.mjs';
import { entreesIndex, figuresModeEmploi, BLOCS_MODE_EMPLOI, PIED_MODE_EMPLOI }
  from '../src/gabarits/pages.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
const DECO = path.join(RACINE, 'build/deco');
const plan = JSON.parse(fs.readFileSync(path.join(RACINE, 'build/plan.json'), 'utf8'));
/* Les hauteurs mesurées dans Chromium pendant la fabrication du PDF : la diapositive
   reprend exactement la même géométrie, sans jamais estimer une hauteur de ligne. */
const mesures = JSON.parse(fs.readFileSync(path.join(RACINE, 'build/mesures.json'), 'utf8'));
/* Les chasses des polices livrées : de quoi savoir si un titre tient sur une ligne. */
const metriques = JSON.parse(fs.readFileSync(path.join(RACINE, 'src/fonts/metriques.json'), 'utf8'));
const AG = catalogue.agence;
const parNumero = Object.fromEntries(catalogue.domaines.map((d) => [d.numero, d]));
const pageDe = plan.domaines;

/* ———————————————————————————————————————— repères ——— */
const mm = (v) => v / 25.4;
const C = {
  tuffeau: 'F2EADA', craie: 'FBF8F1', silex: '46606E', gneiss: 'A8515F',
  amphibolite: '3C5B47', sables: 'D08C3C', violet: '67067C', or: 'E1C853', encre: '2A3942',
};
const F = { titre: 'Young Serif', courant: 'Spectral', tech: 'IBM Plex Sans' };

/* `node scripts/pptx.mjs --recadrable` : les ronds photo sont posés en image entière sous un
   masque rond (recadrage du fichier, pas des pixels). Dans PowerPoint, et dans Canva s'il
   garde ce recadrage à l'import, on déplace l'image dans son rond. La version par défaut
   pose le rond déjà découpé, qui ne dépend de rien. */
const RECADRABLE = process.argv.includes('--recadrable');

/* La taille de la lettrine, domaine par domaine, en multiple du corps du texte, et au besoin
   un interligne un peu resserré : réglés par scripts/regler-lettrines.py, qui rend le .pptx
   et ne réduit que là où le texte déborderait de sa bande. */
const FICHIER_LETTRINES = path.join(RACINE, 'src/gabarits/lettrines-pptx.json');
const LETTRINES = fs.existsSync(FICHIER_LETTRINES)
  ? JSON.parse(fs.readFileSync(FICHIER_LETTRINES, 'utf8')) : {};
const LETTRINE_DEFAUT = 1.8;
const BOITES = {};   // n° → place du texte, pour regler-lettrines.py

const PAGE_L = 210, PAGE_H = 260;
const MARGE = { haut: 15, bas: 13, int: 17, ext: 14 };
const CAROTTE = 9;
const CADRE_L = PAGE_L - MARGE.int - MARGE.ext - CAROTTE;   // 170 mm
const CADRE_H = PAGE_H - MARGE.haut - MARGE.bas;            // 232 mm

const cle = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^A-Za-z0-9]+/g, '-').toLowerCase();
const img = (nom) => path.join(DECO, `${nom}.png`);
/** Largeur et hauteur d'un PNG, lues dans son en-tête IHDR. */
const taillePng = (f) => { const b = fs.readFileSync(f); return [b.readUInt32BE(16), b.readUInt32BE(20)]; };

/** Largeur d'une chaîne en millimètres, d'après les chasses de la police livrée. */
function largeur(texte, face, taillePt) {
  const m = metriques[face] || metriques['IBM Plex Sans'];
  let em = 0;
  for (const c of texte) em += m.chasses[c.codePointAt(0)] ?? m.defaut;
  return em * taillePt * 25.4 / 72;
}

/** Nombre de lignes qu'occupe un texte dans une boîte de `large` mm. */
function lignesDe(texte, face, taillePt, large) {
  const mots = texte.split(' ');
  let n = 1, courante = '';
  for (const mot of mots) {
    const essai = courante ? `${courante} ${mot}` : mot;
    if (largeur(essai, face, taillePt) > large && courante) { n += 1; courante = mot; }
    else courante = essai;
  }
  return n;
}

const debordements = [];

const pres = new PptxGenJS();
pres.defineLayout({ name: 'SCIO', width: mm(PAGE_L), height: mm(PAGE_H) });
pres.layout = 'SCIO';
pres.author = 'Agence SCIO Vins & Spirits';
pres.title = 'Sous nos pieds — Tarifs cavistes Vendée (85) 2026';

/** Marge intérieure d'une page : à droite sur un recto, à gauche sur un verso. */
function geo(numero) {
  const verso = numero % 2 === 0;
  const gauche = verso ? MARGE.ext + CAROTTE : MARGE.int;
  return { verso, gauche, largeur: CADRE_L, haut: MARGE.haut };
}

function nouvelle(numero, { fond = C.tuffeau } = {}) {
  const s = pres.addSlide();
  s.background = { color: fond };
  return s;
}

/** La bande de tranche indexée, côté extérieur. */
function poserCarotte(s, numero, region) {
  const { verso } = geo(numero);
  s.addImage({ path: img(`carotte-${cle(region)}`),
    x: verso ? 0 : mm(PAGE_L - CAROTTE), y: 0, w: mm(CAROTTE), h: mm(PAGE_H) });
  s.addText(region.toUpperCase(), {
    x: verso ? mm(-PAGE_H / 2 + CAROTTE / 2) : mm(PAGE_L - CAROTTE / 2 - PAGE_H / 2),
    y: mm(PAGE_H / 2 - CAROTTE / 2), w: mm(PAGE_H), h: mm(CAROTTE),
    rotate: verso ? 90 : 270, align: 'center', valign: 'middle', margin: 0,
    fontFace: F.tech, fontSize: 6.6, bold: true, color: C.craie, charSpacing: 0.4,
  });
}

function folio(s, numero, { clair = false } = {}) {
  const { verso } = geo(numero);
  s.addText(String(numero), {
    x: verso ? mm(MARGE.ext + CAROTTE) : mm(PAGE_L - MARGE.ext - CAROTTE - 15),
    y: mm(PAGE_H - 11), w: mm(15), h: mm(5), margin: 0,
    align: verso ? 'left' : 'right', fontFace: F.tech, fontSize: 7.5,
    color: clair ? C.craie : C.silex, transparency: 28,
  });
  s.addText(AG.message_sanitaire, {
    x: verso ? mm(PAGE_L - MARGE.int - 95) : mm(MARGE.int), y: mm(PAGE_H - 11),
    w: mm(95), h: mm(5), margin: 0, align: verso ? 'right' : 'left',
    fontFace: F.tech, fontSize: 5.6, color: clair ? C.craie : C.silex, transparency: 45,
  });
}

/** Les <strong> des textes partagés avec le HTML deviennent des passages en gras. */
function riches(html, couleur) {
  return html.split(/<\/?strong>/).map((bout, i) => ({
    text: bout, options: i % 2 ? { bold: true, ...(couleur ? { color: couleur } : {}) } : {},
  })).filter((r) => r.text);
}

/* ———————————————————————————————————————— fiche domaine ——— */

const PICTO = {
  blanc: ['FBF8F1', C.silex], rouge: [C.gneiss, C.gneiss], rose: ['D98FA0', C.gneiss],
  bulles: ['FFFFFF', C.silex], doux: [C.or, C.or], sansalcool: ['FFFFFF', C.amphibolite],
  jus: [C.amphibolite, C.amphibolite], biere: [C.sables, C.sables],
  spiritueux: ['8A6230', '8A6230'], autre: ['FFFFFF', C.silex],
};

function tableauDonnees(t, lignes, hauteurs) {
  const n = t.paliers.length;
  const largeurs = [mm(6), mm(CADRE_L - 6 - 15 - 14 - 52), mm(15), mm(14),
    ...Array(n).fill(mm(52 / n))];
  const bordure = [{ type: 'solid', color: 'C7D1D6', pt: 0.3 }];

  const entete = [
    { text: `${t.intitule}${t.famille ? ' · ' + t.famille : ''}`.toUpperCase(),
      options: { colspan: 4, fill: C.violet, color: C.or, fontFace: F.tech, fontSize: 7.2,
        bold: true, valign: 'bottom', margin: [4, 4, 4, 6], charSpacing: 0.3 } },
    ...t.paliers.map((p) => ({ text: p, options: {
      fill: C.violet, color: C.craie, fontFace: F.tech, fontSize: 6.4, bold: true,
      align: 'right', valign: 'bottom', margin: [4, 5, 4, 3] } })),
  ];

  const corps = lignes.map((l, i) => {
    const f = famille(l, t);
    const [remplissage] = PICTO[f] || PICTO.autre;
    const fondLigne = i % 2 === 0 ? C.craie : C.tuffeau;
    const commun = { fill: fondLigne, valign: 'middle', margin: [3, 3, 3, 3] };
    return [
      { text: '●', options: { ...commun, color: remplissage === 'FFFFFF' ? C.silex : remplissage,
        fontSize: 9, align: 'center' } },
      { text: [
          { text: l.appellation + (l.note === '*' ? ' *' : ''),
            options: { fontFace: F.tech, fontSize: 7.2, color: C.gneiss, breakLine: true } },
          ...(l.cuvee ? [{ text: l.cuvee, options: { fontFace: F.tech, fontSize: 8.5, bold: true, color: C.silex } }] : []),
        ], options: { ...commun, margin: [3, 3, 3, 4] } },
      { text: l.millesime || '—', options: { ...commun, fontFace: F.tech, fontSize: 7.2,
        color: C.silex, align: 'right' } },
      { text: l.contenance || '—', options: { ...commun, fontFace: F.tech, fontSize: 7.2,
        color: C.silex, align: 'right' } },
      ...l.prix_centimes.map((p) => ({ text: [
          { text: euros(p), options: { fontFace: F.tech, fontSize: 8.8, bold: true, color: C.silex } },
          { text: ' €', options: { fontFace: F.tech, fontSize: 6.4, color: C.silex } },
        ], options: { ...commun, align: 'right' } })),
    ];
  });

  return { rows: [entete, ...corps], largeurs, bordure, hauteurs };
}

function slideFiche(s, numero, desc) {
  const d = parNumero[desc.domaine];
  const { gauche } = geo(numero);
  const x = mm(gauche);
  let y = mm(MARGE.haut);
  poserCarotte(s, numero, d.region);

  // ——— en-tête. Un nom long réduit le corps du titre plutôt que de passer à la ligne :
  // le filet et les jetons restent où la pagination mesurée les attend.
  const LARGEUR_TITRE = CADRE_L - 34;
  const RETRAIT = largeur(`${d.numero}   `, F.titre, 27);
  const SUITE = desc.premiere ? 0 : largeur('  (suite)', 'Spectral', 11);
  const dispo = LARGEUR_TITRE - RETRAIT - SUITE;
  const pleine = largeur(d.nom, F.titre, 20);
  const taille = pleine <= dispo ? 20
    : Math.max(15, Math.floor(20 * dispo / pleine * 2) / 2);
  const nbLignes = Math.max(1, lignesDe(d.nom, F.titre, taille, dispo));
  const hTitre = 11 + (nbLignes - 1) * 8.4;
  s.addText([
    { text: String(d.numero), options: { fontFace: F.titre, fontSize: 27, color: C.violet } },
    { text: `   ${d.nom}`, options: { fontFace: F.titre, fontSize: taille, color: C.silex } },
    ...(desc.premiere ? [] : [{ text: '  (suite)', options: {
      fontFace: F.courant, fontSize: 11, italic: true, color: C.gneiss } }]),
  ], { x, y, w: mm(LARGEUR_TITRE), h: mm(hTitre), margin: 0, valign: 'middle',
    lineSpacingMultiple: 1.04 });
  s.addText(d.region.toUpperCase(), {
    x: mm(gauche + CADRE_L - 40), y, w: mm(40), h: mm(11), margin: 0,
    align: 'right', valign: 'middle', fontFace: F.tech, fontSize: 8, bold: true,
    color: C.gneiss, charSpacing: 0.3,
  });
  y += mm(hTitre + 0.5);
  s.addShape(pres.ShapeType.line, { x, y, w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 1.4 } });
  y += mm(2.6);

  // ——— jetons
  const jetons = [
    ...d.labels.map((l) => [l.label, C.amphibolite, null]),
    ...(d.allocation ? [['Allocation', C.violet, C.violet]] : []),
    [groupeDe(d) ? 'Panachage entre domaines' : 'Panachage dans le domaine', C.gneiss, null],
    ...(d.mentions.some((m) => m.toLowerCase().includes('consultez-nous'))
      ? [['Consultez-nous', C.sables, C.sables]] : []),
    [`${nbReferences(d)} références`, C.silex, null],
  ];
  let jx = gauche;
  jetons.forEach(([texte, couleur, fond]) => {
    const l = largeur(texte, 'IBM Plex Sans Bold', 7.2) + 5.6;
    s.addShape(pres.ShapeType.roundRect, { x: mm(jx), y, w: mm(l), h: mm(5),
      fill: fond ? { color: fond } : { color: C.tuffeau },
      line: { color: couleur, width: 0.7 }, rectRadius: 0.02 });
    s.addText(texte, { x: mm(jx), y, w: mm(l), h: mm(5), margin: 0, align: 'center',
      valign: 'middle', fontFace: F.tech, fontSize: 7.2, bold: true,
      color: fond ? C.craie : couleur });
    jx += l + 2.2;
  });
  y += mm(8.6);

  if (desc.premiere) {
    // ——— les deux emplacements, et le texte entre les deux. L'image prend la place de
    // la forme pointillée quand il y en a une ; sinon l'emplacement reste réservé.
    // La bande fait la hauteur mesurée dans Chromium : la même que dans le PDF.
    const { rond, bouteille, ecart } = EMPLACEMENT;
    const bande = (mesures.blocs[`haut-${d.numero}`] ?? 66.5) - 4.5;
    const phRond = photoDe(d, 'rond');
    if (phRond && RECADRABLE && phRond.entiere) {
      // l'image entière, à l'échelle du rond ; le carré choisi est un recadrage, le cercle
      // un masque : on peut faire glisser l'image dans son rond
      const [cx, cy, cl, ch] = phRond.carre;
      const [W, H] = [mm(rond) / cl, mm(rond) / ch];
      s.addImage({ path: path.join(RACINE, phRond.entiere), x, y, w: W, h: H, rounding: true,
        sizing: { type: 'crop', x: cx * W, y: cy * H, w: mm(rond), h: mm(rond) },
        altText: `${phRond.sujet} — ${d.nom}` });
    } else if (phRond) {
      // déjà masquée en cercle par preparer-photos.py : rien ne dépend de l'import
      s.addImage({ path: path.join(RACINE, phRond.fichier.replace(/\.jpg$/, '-cercle.png')),
        x, y, w: mm(rond), h: mm(rond), altText: `${phRond.sujet} — ${d.nom}` });
    } else {
      s.addShape(pres.ShapeType.ellipse, { x, y, w: mm(rond), h: mm(rond),
        fill: { color: C.tuffeau }, line: { color: C.silex, width: 1, dashType: 'dash' } });
      s.addText('ROND\nVIGNERON\nOU LOGO', { x, y, w: mm(rond), h: mm(rond), margin: 0,
        align: 'center', valign: 'middle', fontFace: F.tech, fontSize: 6.2, bold: true,
        color: C.silex, transparency: 50, lineSpacingMultiple: 1.25 });
    }

    const xb = gauche + CADRE_L - bouteille.l;
    const phBout = photoDe(d, 'bouteille');
    if (phBout) {
      // contenue dans 24 × 62 mm, proportions gardées, posée sur le bas comme dans le PDF
      const fichier = path.join(RACINE, phBout.fichier);
      const [lpx, hpx] = taillePng(fichier);
      const k = Math.min(bouteille.l / lpx, bouteille.h / hpx);
      const [lb, hb] = [lpx * k, hpx * k];
      s.addImage({ path: fichier, x: mm(xb + (bouteille.l - lb) / 2), y: y + mm(bouteille.h - hb),
        w: mm(lb), h: mm(hb), altText: `Une bouteille du domaine ${d.nom}` });
    } else {
      s.addShape(pres.ShapeType.roundRect, { x: mm(xb), y, w: mm(bouteille.l), h: mm(bouteille.h),
        fill: { color: C.tuffeau }, line: { color: C.silex, width: 1, dashType: 'dash' },
        rectRadius: 0.02 });
      s.addText('BOUTEILLE', { x: mm(xb), y, w: mm(bouteille.l), h: mm(bouteille.h), margin: 0,
        align: 'center', valign: 'middle', fontFace: F.tech, fontSize: 6.2, bold: true,
        color: C.silex, transparency: 50 });
    }

    // le corps grandit pour remplir la bande, et le texte s'y centre : voir corpsDomaine()
    const texte = d.texte_source
      || "Le tarif de l'Agence SCIO ne donne pas de présentation pour ce domaine. Nous n'en inventons pas.";
    // La lettrine, comme dans le PDF : la première lettre en Young Serif violette. Un .pptx ne
    // sait pas faire tomber une lettre sur deux lignes ; elle monte donc au-dessus de la
    // première ligne (lettrine montante), deux fois le corps du texte : corpsDomaine() garde
    // déjà une ligne de marge pour elle.
    const corps = d.texte_source ? corpsDomaine(d) : 9;
    const reglage = LETTRINES[d.numero] ?? {};
    const facteur = reglage.lettrine ?? LETTRINE_DEFAUT;
    const interligne = reglage.interligne ?? 1.42;
    const morceaux = d.texte_source
      ? [{ text: texte.slice(0, 1), options: { fontFace: F.titre, fontSize: Math.round(corps * facteur * 2) / 2,
        color: C.violet } }, { text: texte.slice(1) }]
      : texte;
    BOITES[d.numero] = { diapo: pres.slides.length, x: gauche + rond + ecart,
      y: y / mm(1), w: COLONNE_DOM, h: bande };
    s.addText(morceaux, { x: mm(gauche + rond + ecart), y, w: mm(COLONNE_DOM), h: mm(bande),
      margin: 0, fontFace: F.courant, fontSize: corps,
      color: C.silex, lineSpacingMultiple: interligne, italic: !d.texte_source, valign: 'middle' });
    y += mm(bande + 4.5);
  }

  // ——— tableaux
  desc.morceaux.forEach((mo, k) => {
    const t = d.tableaux[mo.tableau];
    const lignes = mo.lignes.map((i) => t.lignes[i]);
    const hEntete = mesures.blocs[`thead-${d.numero}-${mo.tableau}`] ?? 8.8;
    const hLignes = mo.lignes.map((i) => mesures.lignes[`${d.numero}-${mo.tableau}-${i}`] ?? 10.7);
    const { rows, largeurs, bordure, hauteurs } = tableauDonnees(
      { ...t, intitule: t.intitule + (mo.suite ? ' (suite)' : '') }, lignes,
      [hEntete, ...hLignes]);
    s.addTable(rows, { x, y, w: mm(CADRE_L), colW: largeurs, border: bordure,
      rowH: hauteurs.map(mm), autoPage: false, fontFace: F.tech });
    y += mm(hEntete + hLignes.reduce((a, b) => a + b, 0))
      + mm(k < desc.morceaux.length - 1 ? 4.5 : 0);
  });

  // ——— quand la fiche est courte, le sol de sa région comble le vide, comme dans le PDF
  const VIDE_MIN = 30, VIDE_MAX = 40;
  if (desc.reste >= VIDE_MIN) {
    const h = Math.min(desc.reste - 5, Math.max(VIDE_MAX, desc.reste * 0.6));
    const yl = y + mm(4);
    s.addText(`${d.region} — ${STRATES[d.region].mot}`.toUpperCase(), {
      x, y: yl, w: mm(CADRE_L), h: mm(3.5), margin: 0, fontFace: F.tech, fontSize: 7.2,
      color: C.gneiss, charSpacing: 0.3 });
    s.addImage({ path: img(`sol-${cle(d.region)}`), x, y: yl + mm(4.1),
      w: mm(CADRE_L), h: mm(h - 8.1) });
  }

  // ——— pied de fiche
  const yPied = mm(PAGE_H - MARGE.bas - 14);
  const g = groupeDe(d);
  const plafond = yPied - mm(g ? 8 : 1.5);
  if (y > plafond) {
    debordements.push(`diapo ${numero} (n°${d.numero} ${d.nom}) : `
      + `${((y - plafond) * 25.4).toFixed(1)} mm de trop sous les tableaux`);
  }
  if (g) {
    const autres = g.domaines.filter((n) => n !== d.numero)
      .map((n) => `n°${n} p. ${pageDe[n]}`).join(' · ');
    s.addText([
      { text: 'Se panache avec ', options: { bold: true, color: C.gneiss } },
      { text: `${g.libelle} — ${autres}`, options: { color: C.silex } },
    ], { x, y: yPied - mm(7), w: mm(CADRE_L), h: mm(5.5), margin: [2, 3, 2, 3],
      fill: { color: 'F4E7E9' }, fontFace: F.tech, fontSize: 7.4, valign: 'middle' });
  }
  s.addShape(pres.ShapeType.line, { x, y: yPied, w: mm(CADRE_L), h: 0,
    line: { color: C.silex, width: 0.7 } });
  s.addText(d.note_prix || 'Conditions de port non précisées par le domaine — nous consulter.', {
    x, y: yPied + mm(1), w: mm(CADRE_L * 0.55), h: mm(5), margin: 0,
    fontFace: F.tech, fontSize: 7.2, color: C.silex });
  s.addText([
    { text: 'Distribution ', options: { bold: true, color: C.violet } },
    { text: d.departements.length ? d.departements.join(' · ')
      : 'non précisés par le domaine — nous consulter', options: { color: C.silex } },
  ], { x: mm(gauche + CADRE_L * 0.45), y: yPied + mm(1), w: mm(CADRE_L * 0.55), h: mm(5),
    margin: 0, align: 'right', fontFace: F.tech, fontSize: 7.2 });
  s.addText(famillesDe(d).map((f) => `● ${NOM_FAMILLE[f]}`).join('    ')
    + '     pictos de l’Agence SCIO, pas les logos officiels', {
    x, y: yPied + mm(5.6), w: mm(CADRE_L), h: mm(4), margin: 0,
    fontFace: F.tech, fontSize: 6.5, color: C.silex, transparency: 25 });

  folio(s, numero);
}


/* ———————————————————————————————————————— pages d'appareil ——— */

function titreSection(s, numero, titre, sous) {
  const { gauche } = geo(numero);
  s.addText(titre, { x: mm(gauche), y: mm(MARGE.haut), w: mm(CADRE_L), h: mm(12), margin: 0,
    fontFace: F.titre, fontSize: 24, color: C.violet, valign: 'bottom' });
  if (sous) {
    s.addText(sous.toUpperCase(), { x: mm(gauche), y: mm(MARGE.haut + 12.5), w: mm(CADRE_L),
      h: mm(5), margin: 0, fontFace: F.tech, fontSize: 8, bold: true, color: C.gneiss,
      charSpacing: 0.3 });
  }
  return MARGE.haut + (sous ? 21 : 15);
}

function slideCouverture(s, numero) {
  s.addImage({ path: img('coupe-titree'), x: 0, y: mm(PAGE_H - 148), w: mm(PAGE_L), h: mm(148) });
  s.addImage({ path: path.join(RACINE, 'src/images/logo-agence-scio-detoure.png'),
    x: mm(MARGE.int), y: mm(17), w: mm(62), h: mm(62 * 251 / 1030) });
  s.addText([
    { text: 'Sous', options: { breakLine: true } },
    { text: 'nos', options: { breakLine: true } },
    { text: 'pieds', options: { color: C.violet } },
  ], { x: mm(MARGE.int), y: mm(42), w: mm(150), h: mm(50), margin: 0,
    fontFace: F.titre, fontSize: 46, color: C.silex, lineSpacingMultiple: 0.92 });
  s.addText("Quarante domaines, dix régions,\net la terre qu'ils ont sous les pieds.", {
    x: mm(MARGE.int), y: mm(95), w: mm(120), h: mm(14), margin: 0,
    fontFace: F.courant, fontSize: 10.5, color: C.silex, lineSpacingMultiple: 1.4 });
  s.addShape(pres.ShapeType.roundRect, { x: mm(-6), y: mm(PAGE_H - 44), w: mm(78), h: mm(24),
    fill: { color: C.tuffeau }, line: { color: C.tuffeau, width: 0 }, rectRadius: 0.03 });
  s.addText(AG.cible.toUpperCase(), { x: mm(MARGE.int), y: mm(PAGE_H - 42), w: mm(60), h: mm(5),
    margin: 0, fontFace: F.tech, fontSize: 9, bold: true, color: C.silex, charSpacing: 0.3 });
  s.addText(AG.edition, { x: mm(MARGE.int), y: mm(PAGE_H - 36), w: mm(60), h: mm(14), margin: 0,
    fontFace: F.titre, fontSize: 34, color: C.violet });
  s.addText(AG.message_sanitaire, { x: mm(MARGE.int), y: mm(PAGE_H - 13), w: mm(140), h: mm(5),
    margin: 0, fontFace: F.tech, fontSize: 5.6, color: C.craie });
}

function slideAgence(s, numero) {
  const { gauche } = geo(numero);
  const x = mm(gauche);
  s.addImage({ path: path.join(RACINE, 'src/images/logo-agence-scio-detoure.png'),
    x, y: mm(MARGE.haut), w: mm(74), h: mm(74 * 251 / 1030) });
  s.addText([
    { text: "L'Agence SCIO, c'est " },
    { text: 'partager notre savoir et notre passion', options: { color: C.violet } },
    { text: ' en vous proposant des vignerons de tous horizons, avant-gardistes et respectueux '
        + 'de la nature. Découvrez notre sélection. Laissez-vous guider et conseiller.' },
  ], { x, y: mm(MARGE.haut + 32), w: mm(150), h: mm(40), margin: 0,
    fontFace: F.titre, fontSize: 17, color: C.silex, lineSpacingMultiple: 1.3 });

  [['Laurent', AG.contacts.laurent], ['Carline', AG.contacts.carline]].forEach(([p, t], i) => {
    const cx = gauche + i * 55;
    s.addText(p.toUpperCase(), { x: mm(cx), y: mm(MARGE.haut + 76), w: mm(50), h: mm(5),
      margin: 0, fontFace: F.tech, fontSize: 8, bold: true, color: C.gneiss, charSpacing: 0.3 });
    s.addText(t, { x: mm(cx), y: mm(MARGE.haut + 81), w: mm(50), h: mm(9), margin: 0,
      fontFace: F.titre, fontSize: 17, color: C.violet });
  });
  s.addText(`${AG.contacts.adresse}\n${AG.contacts.email}\n${AG.contacts.site}`, {
    x, y: mm(MARGE.haut + 94), w: mm(120), h: mm(20), margin: 0,
    fontFace: F.courant, fontSize: 10, color: C.silex, lineSpacingMultiple: 1.6 });
  s.addImage({ path: img('coupe-nue'), x, y: mm(MARGE.haut + 120), w: mm(CADRE_L),
    h: mm(CADRE_L * 42 / 176) });
  const yc = MARGE.haut + 172;
  s.addShape(pres.ShapeType.line, { x, y: mm(yc), w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 0.8 } });
  const refs = catalogue.domaines.reduce((n, d) => n + nbReferences(d), 0);
  [['40', 'domaines'], ['10', 'régions'], [String(refs), 'références']].forEach(([n, l], i) => {
    s.addText(n, { x: mm(gauche + i * 42), y: mm(yc + 3), w: mm(40), h: mm(11), margin: 0,
      fontFace: F.titre, fontSize: 26, color: C.violet });
    s.addText(l, { x: mm(gauche + i * 42), y: mm(yc + 14), w: mm(40), h: mm(5), margin: 0,
      fontFace: F.tech, fontSize: 9, color: C.silex });
  });
  folio(s, numero);
}

function slideModeEmploi(s, numero) {
  const { gauche } = geo(numero);
  const y = titreSection(s, numero, 'Comment lire ce catalogue');
  const figures = figuresModeEmploi();
  const COL = CADRE_L / 2 - 4.5;
  // Mêmes règles que la grille CSS : chaque rangée fait la hauteur du plus haut des deux blocs.
  const H_TITRE = 4.7, H_LIGNE = 4.2, ECART = 5.5;
  const taille = BLOCS_MODE_EMPLOI.map(([t, p], i) => {
    const hFig = figures[i].hauteur;
    const nT = lignesDe(t, F.titre, 11.5, COL);
    const nP = lignesDe(p.replace(/<\/?strong>/g, ''), F.courant, 8.2, COL);
    return { hFig, hT: nT * H_TITRE, hP: nP * H_LIGNE };
  });
  const rangs = [0, 1, 2].map((r) => Math.max(
    ...[0, 1].map((c) => { const b = taille[r * 2 + c]; return b.hFig + 1.8 + b.hT + 1.4 + b.hP; })));
  BLOCS_MODE_EMPLOI.forEach(([t, p], i) => {
    const col = i % 2, rang = Math.floor(i / 2);
    const bx = gauche + col * (CADRE_L / 2 + 4.5);
    const by = y + rangs.slice(0, rang).reduce((a, b) => a + b + ECART, 0);
    const b = taille[i];
    s.addImage({ path: img(figures[i].nom), x: mm(bx), y: mm(by), w: mm(COL), h: mm(b.hFig) });
    const yT = by + b.hFig + 1.8;
    s.addText(t, { x: mm(bx), y: mm(yT), w: mm(COL), h: mm(b.hT), margin: 0,
      fontFace: F.titre, fontSize: 11.5, color: C.violet, valign: 'top',
      lineSpacingMultiple: 1.05 });
    s.addText(riches(p), { x: mm(bx), y: mm(yT + b.hT + 1.4), w: mm(COL), h: mm(b.hP + 2),
      margin: 0, fontFace: F.courant, fontSize: 8.2, color: C.silex,
      lineSpacingMultiple: 1.28, valign: 'top' });
  });
  const yPied = PAGE_H - MARGE.bas - 17;
  s.addShape(pres.ShapeType.line, { x: mm(gauche), y: mm(yPied), w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 0.8 } });
  s.addText(riches(PIED_MODE_EMPLOI, C.violet),
    { x: mm(gauche), y: mm(yPied + 1.6), w: mm(CADRE_L), h: mm(11), margin: 0,
      fontFace: F.courant, fontSize: 8.6, color: C.silex });
  folio(s, numero);
}

function slideSommaire(s, numero) {
  const { gauche } = geo(numero);
  const y0 = titreSection(s, numero, 'La coupe', 'sommaire des dix régions');
  const eff = REGIONS.map((n) => catalogue.domaines.filter((d) => d.region === n).length);
  const poids = eff.map((n) => Math.max(n, 2.6));
  const total = poids.reduce((a, b) => a + b, 0);
  const dispo = PAGE_H - MARGE.bas - y0 - 9 * 1.2;
  let y = y0;
  REGIONS.forEach((r, i) => {
    const st = STRATES[r];
    const h = (poids[i] / total) * dispo;
    const clair = r === 'Champagne';
    s.addShape(pres.ShapeType.roundRect, { x: mm(gauche), y: mm(y), w: mm(CADRE_L), h: mm(h),
      fill: { color: st.hex.slice(1) }, line: { color: st.hex.slice(1), width: 0 },
      rectRadius: 0.015 });
    s.addText(r, { x: mm(gauche + 3), y: mm(y + 1.6), w: mm(50), h: mm(6), margin: 0,
      fontFace: F.titre, fontSize: 11.5, color: clair ? C.silex : C.craie, valign: 'middle' });
    s.addText(st.mot, { x: mm(gauche + 36), y: mm(y + 1.6), w: mm(70), h: mm(6), margin: 0,
      fontFace: F.courant, fontSize: 7, italic: true, color: clair ? C.silex : C.craie,
      valign: 'middle', transparency: 18 });
    s.addText(String(eff[i]), { x: mm(gauche + CADRE_L - 12), y: mm(y + 1.6), w: mm(9), h: mm(6),
      margin: 0, align: 'center', valign: 'middle', fontFace: F.tech, fontSize: 7.5, bold: true,
      color: clair ? C.silex : C.craie });
    const doms = catalogue.domaines.filter((d) => d.region === r);
    const cols = doms.length >= 5 ? 3 : 2;
    const lc = (CADRE_L - 8) / cols;
    doms.forEach((d, k) => {
      const col = Math.floor(k / Math.ceil(doms.length / cols));
      const rang = k % Math.ceil(doms.length / cols);
      s.addText([
        { text: `${d.numero}  `, options: { bold: true } },
        { text: d.nom },
        { text: `   ${pageDe[d.numero]}`, options: { bold: true } },
      ], { x: mm(gauche + 4 + col * lc), y: mm(y + 8 + rang * 3.6), w: mm(lc - 2), h: mm(3.6),
        margin: 0, fontFace: F.tech, fontSize: 7.4, color: clair ? C.silex : C.craie,
        valign: 'middle' });
    });
    y += h + 1.2;
  });
  folio(s, numero);
}

function slideAlliances(s, numero) {
  const { gauche } = geo(numero);
  let y = titreSection(s, numero, 'Les quatre alliances',
    "ce que l'on peut mélanger entre domaines");
  s.addText([
    { text: 'Partout ailleurs, « Possibilité de panacher » vaut ' },
    { text: "à l'intérieur d'un domaine", options: { bold: true, color: C.violet } },
    { text: '. Ces quatre groupes-là se panachent ' },
    { text: 'entre eux', options: { bold: true, color: C.violet } },
    { text: ' : une commande peut mélanger leurs vins pour atteindre un palier.' },
  ], { x: mm(gauche), y: mm(y), w: mm(CADRE_L), h: mm(12), margin: 0,
    fontFace: F.courant, fontSize: 9.5, color: C.silex });
  y += 14;
  groupes.forEach((g) => {
    const doms = g.domaines.map((n) => parNumero[n]);
    const h = 13 + Math.ceil(doms.length / 2) * 7;
    s.addShape(pres.ShapeType.roundRect, { x: mm(gauche), y: mm(y), w: mm(CADRE_L), h: mm(h),
      fill: { color: C.craie }, line: { color: C.gneiss, width: 1.2 }, rectRadius: 0.012 });
    s.addText(g.libelle, { x: mm(gauche + 4), y: mm(y + 2), w: mm(CADRE_L - 8), h: mm(7),
      margin: 0, fontFace: F.titre, fontSize: 13, color: C.gneiss, valign: 'middle' });
    doms.forEach((d, k) => {
      s.addText([
        { text: `${d.numero}  `, options: { fontFace: F.titre, fontSize: 11, color: C.violet } },
        { text: `${d.nom}  `, options: { bold: true } },
        { text: `${d.region}   `, options: { color: C.gneiss, fontSize: 7 } },
        { text: `p. ${pageDe[d.numero]}`, options: { bold: true } },
      ], { x: mm(gauche + 5 + (k % 2) * (CADRE_L / 2)), y: mm(y + 10 + Math.floor(k / 2) * 7),
        w: mm(CADRE_L / 2 - 6), h: mm(6), margin: 0, fontFace: F.tech, fontSize: 8,
        color: C.silex, valign: 'middle' });
    });
    y += h + 5;
  });
  s.addText('Les paliers restent ceux de chaque domaine : le panachage permet d’atteindre la '
    + 'quantité, il ne change pas le tarif de la bouteille.', {
    x: mm(gauche), y: mm(PAGE_H - MARGE.bas - 12), w: mm(CADRE_L), h: mm(8), margin: 0,
    fontFace: F.courant, fontSize: 8.6, color: C.silex });
  folio(s, numero);
}

function slideOuverture(s, numero, region) {
  s.addImage({ path: img(`ouverture-${cle(region)}`), x: 0, y: 0, w: mm(PAGE_L), h: mm(PAGE_H) });
  poserCarotte(s, numero, region);
  const { gauche } = geo(numero);
  const clair = region === 'Champagne';
  const encre = clair ? C.silex : C.craie;
  const doms = catalogue.domaines.filter((d) => d.region === region);
  const refs = doms.reduce((n, d) => n + nbReferences(d), 0);
  s.addText(`${REGIONS.indexOf(region) + 1} / 10`, { x: mm(gauche), y: mm(MARGE.haut),
    w: mm(22), h: mm(6), margin: 0, align: 'center', valign: 'middle',
    fontFace: F.tech, fontSize: 8, bold: true, color: encre });
  s.addText(region, { x: mm(gauche), y: mm(142), w: mm(140), h: mm(22), margin: 0,
    fontFace: F.titre, fontSize: 46, color: encre });
  s.addText(STRATES[region].mot, { x: mm(gauche), y: mm(166), w: mm(120), h: mm(7), margin: 0,
    fontFace: F.courant, fontSize: 12, italic: true, color: encre });
  s.addText(String(doms.length), { x: mm(gauche), y: mm(176), w: mm(24), h: mm(9), margin: 0,
    fontFace: F.titre, fontSize: 20, color: encre });
  s.addText(doms.length > 1 ? 'domaines' : 'domaine', { x: mm(gauche), y: mm(185), w: mm(24),
    h: mm(5), margin: 0, fontFace: F.tech, fontSize: 8.5, color: encre });
  s.addText(String(refs), { x: mm(gauche + 28), y: mm(176), w: mm(24), h: mm(9), margin: 0,
    fontFace: F.titre, fontSize: 20, color: encre });
  s.addText('références', { x: mm(gauche + 28), y: mm(185), w: mm(26), h: mm(5), margin: 0,
    fontFace: F.tech, fontSize: 8.5, color: encre });
  doms.forEach((d, k) => {
    const col = k % 2, rang = Math.floor(k / 2);
    s.addText([
      { text: `${d.numero}   `, options: { fontFace: F.titre, fontSize: 11 } },
      { text: d.nom },
      { text: `   ${pageDe[d.numero]}`, options: { bold: true } },
    ], { x: mm(gauche + col * (CADRE_L / 2)), y: mm(198 + rang * 7), w: mm(CADRE_L / 2 - 4),
      h: mm(6), margin: 0, fontFace: F.tech, fontSize: 8.6, color: encre, valign: 'middle' });
  });
  folio(s, numero, { clair: !clair });
}

function slideIndexVins(s, numero, desc) {
  const { gauche } = geo(numero);
  let y = MARGE.haut;
  if (desc.premiere) {
    y = titreSection(s, numero, 'Index des vins', 'par type, de A à Z') + 2;
    s.addText('Le numéro en violet est celui du domaine, le dernier chiffre est la page.', {
      x: mm(gauche), y: mm(y), w: mm(CADRE_L), h: mm(5), margin: 0,
      fontFace: F.courant, fontSize: 8.6, color: C.silex });
    y += 7;
  }
  const lc = CADRE_L / 3;
  const parCol = Math.ceil(desc.blocs.length / 3);
  desc.blocs.forEach((b, k) => {
    const col = Math.floor(k / parCol), rang = k % parCol;
    const bx = gauche + col * lc, by = y + rang * 3.5;
    if (by > PAGE_H - MARGE.bas - 4) return;
    if (b.type === 'titre') {
      s.addText(NOM_FAMILLE[b.famille].toUpperCase(), { x: mm(bx), y: mm(by), w: mm(lc - 3),
        h: mm(3.5), margin: 0, fontFace: F.tech, fontSize: 8, bold: true, color: C.violet,
        charSpacing: 0.3, valign: 'middle' });
    } else {
      s.addText([
        { text: b.e.nom + (b.e.prec ? `  ${b.e.prec}` : '') },
        { text: `  ${b.e.dom}`, options: { bold: true, color: C.violet } },
        { text: `  ${b.e.pg}` },
      ], { x: mm(bx), y: mm(by), w: mm(lc - 3), h: mm(3.5), margin: 0,
        fontFace: F.tech, fontSize: 6.9, color: C.silex, valign: 'middle' });
    }
  });
  folio(s, numero);
}

function slideProduits(s, numero) {
  const { gauche } = geo(numero);
  let y = titreSection(s, numero, 'Les produits à part', "ce qui n'est pas une bouteille de 75 cl");
  const bacs = { bib: ['Bag-in-box', []], sansalcool: ['Vins sans alcool', []],
    jus: ['Jus de cépages', []], biere: ['Bières', []], spiritueux: ['Armagnacs et ratafias', []] };
  catalogue.domaines.forEach((d) => d.tableaux.forEach((t) => t.lignes.forEach((l) => {
    const litres = /(\d+(?:[.,]\d+)?)\s*L\b/.exec(l.contenance || '');
    const estBib = /bib/i.test(t.intitule) || /bib/i.test(t.famille || '') || /bib/i.test(l.contenance || '')
      || (!!litres && !/magnum/i.test(l.contenance || '') && parseFloat(litres[1].replace(',', '.')) >= 3);
    const f = famille(l, t);
    const bac = estBib ? 'bib' : (bacs[f] ? f : null);
    if (bac) bacs[bac][1].push({ l, t, d });
  })));
  Object.entries(bacs).forEach(([k, [titre, lignes]]) => {
    if (!lignes.length) return;
    s.addText(`${titre}   (${lignes.length})`, { x: mm(gauche), y: mm(y), w: mm(CADRE_L),
      h: mm(6), margin: 0, fontFace: F.titre, fontSize: 12, color: C.violet, valign: 'middle' });
    s.addShape(pres.ShapeType.line, { x: mm(gauche), y: mm(y + 6), w: mm(CADRE_L), h: 0,
      line: { color: C.violet, width: 0.8 } });
    const parCol = Math.ceil(lignes.length / 2);
    lignes.forEach(({ l, t, d }, i) => {
      const col = Math.floor(i / parCol), rang = i % parCol;
      s.addText([
        { text: `${d.numero}  `, options: { bold: true, color: C.violet } },
        { text: `${l.cuvee || l.appellation}  `, options: { bold: true } },
        { text: `${d.nom}  `, options: { fontSize: 6.8, color: C.silex } },
        { text: `${l.contenance || t.paliers.join(' · ')}   p. ${pageDe[d.numero]}`,
          options: { fontSize: 6.8, color: C.gneiss } },
      ], { x: mm(gauche + col * (CADRE_L / 2)), y: mm(y + 8 + rang * 4), w: mm(CADRE_L / 2 - 3),
        h: mm(4), margin: 0, fontFace: F.tech, fontSize: 7.4, color: C.silex, valign: 'middle' });
    });
    y += 10 + parCol * 4 + 3;
  });
  folio(s, numero);
}

function slideIndexDomaines(s, numero) {
  const { gauche } = geo(numero);
  const y = titreSection(s, numero, 'Les quarante domaines', 'de A à Z');
  const tries = [...catalogue.domaines].sort((a, b) =>
    a.nom.localeCompare(b.nom, 'fr', { sensitivity: 'base' }));
  const parCol = Math.ceil(tries.length / 2);
  tries.forEach((d, i) => {
    const col = Math.floor(i / parCol), rang = i % parCol;
    s.addText([
      { text: `${d.numero}   `, options: { fontFace: F.titre, fontSize: 11, color: C.violet } },
      { text: `${d.nom}   `, options: { bold: true } },
      { text: `${d.region}   `, options: { color: C.gneiss, fontSize: 7 } },
      { text: `${nbReferences(d)}   `, options: { fontSize: 7, color: C.silex } },
      { text: String(pageDe[d.numero]), options: { bold: true } },
    ], { x: mm(gauche + col * (CADRE_L / 2)), y: mm(y + rang * 8), w: mm(CADRE_L / 2 - 4),
      h: mm(7), margin: 0, fontFace: F.tech, fontSize: 8.4, color: C.silex, valign: 'middle' });
  });
  s.addText('Le chiffre avant la page est le nombre de références au tarif.', {
    x: mm(gauche), y: mm(PAGE_H - MARGE.bas - 8), w: mm(CADRE_L), h: mm(5), margin: 0,
    fontFace: F.courant, fontSize: 8, color: C.silex });
  folio(s, numero);
}

function slidePlanche(s, numero) {
  s.addImage({ path: img('coupe-pleine'), x: 0, y: 0, w: mm(PAGE_L), h: mm(PAGE_H) });
  const { gauche } = geo(numero);
  s.addText('Dix régions,\ndix sols,\nquarante domaines.', {
    x: mm(gauche), y: mm(PAGE_H - MARGE.bas - 60), w: mm(120), h: mm(42), margin: 0,
    fontFace: F.titre, fontSize: 26, color: C.craie, lineSpacingMultiple: 1.12 });
  folio(s, numero, { clair: true });
}

/** Page réglée : le caviste note ses quantités en lisant les tarifs. */
function slideNotes(s, numero) {
  const { gauche } = geo(numero);
  const x = mm(gauche);
  s.addText('Vos notes', { x, y: mm(MARGE.haut), w: mm(CADRE_L), h: mm(9), margin: 0,
    fontFace: F.titre, fontSize: 20, color: C.violet, valign: 'bottom' });
  s.addText('QUANTITÉS, PALIERS, DATES DE LIVRAISON', {
    x, y: mm(MARGE.haut + 9.5), w: mm(CADRE_L), h: mm(5), margin: 0,
    fontFace: F.tech, fontSize: 7.5, bold: true, color: C.gneiss, charSpacing: 0.3 });
  for (let i = 0; i < 23; i += 1) {
    s.addShape(pres.ShapeType.line, { x, y: mm(MARGE.haut + 25 + i * 8.5), w: mm(CADRE_L), h: 0,
      line: { color: 'B4C2C9', width: 0.6 } });
  }
  folio(s, numero);
}

function slideFinale(s, numero) {
  const { gauche } = geo(numero);
  const x = mm(gauche);
  s.addImage({ path: path.join(RACINE, 'src/images/logo-agence-scio-detoure.png'),
    x, y: mm(MARGE.haut), w: mm(70), h: mm(70 * 251 / 1030) });
  [['Laurent', AG.contacts.laurent], ['Carline', AG.contacts.carline]].forEach(([p, t], i) => {
    const cx = gauche + i * 55;
    s.addText(p.toUpperCase(), { x: mm(cx), y: mm(MARGE.haut + 28), w: mm(50), h: mm(5),
      margin: 0, fontFace: F.tech, fontSize: 8, bold: true, color: C.gneiss, charSpacing: 0.3 });
    s.addText(t, { x: mm(cx), y: mm(MARGE.haut + 33), w: mm(50), h: mm(9), margin: 0,
      fontFace: F.titre, fontSize: 17, color: C.violet });
  });
  s.addText(`${AG.contacts.adresse}\n${AG.contacts.email} · ${AG.contacts.site}`, {
    x, y: mm(MARGE.haut + 46), w: mm(130), h: mm(14), margin: 0,
    fontFace: F.courant, fontSize: 10, color: C.silex, lineSpacingMultiple: 1.5 });
  s.addImage({ path: img('coupe-nue'), x, y: mm(MARGE.haut + 66), w: mm(CADRE_L),
    h: mm(CADRE_L * 42 / 176) });

  const yc = MARGE.haut + 118;
  s.addShape(pres.ShapeType.line, { x, y: mm(yc), w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 0.8 } });
  const colonnes = [
    ['Lexique', AG.lexique.map((l) => `${l.sigle} — ${l.definition}`).join('\n')],
    ['Mentions légales', AG.mentions_legales],
    ['Crédits', 'Conception, maquette et illustrations : Agence SCIO. Les pictogrammes de ce '
      + "catalogue sont les nôtres ; ils ne reproduisent aucun logo officiel d'organisme "
      + 'certificateur. ' + creditPhotos()],
  ];
  colonnes.forEach(([t, p], i) => {
    const cx = gauche + i * (CADRE_L / 3);
    s.addText(t.toUpperCase(), { x: mm(cx), y: mm(yc + 4), w: mm(CADRE_L / 3 - 5), h: mm(5),
      margin: 0, fontFace: F.tech, fontSize: 7.6, bold: true, color: C.gneiss, charSpacing: 0.3 });
    s.addText(p, { x: mm(cx), y: mm(yc + 10), w: mm(CADRE_L / 3 - 5), h: mm(48), margin: 0,
      fontFace: F.courant, fontSize: 7.8, color: C.silex, lineSpacingMultiple: 1.3 });
  });
  s.addShape(pres.ShapeType.roundRect, { x, y: mm(PAGE_H - MARGE.bas - 14), w: mm(CADRE_L),
    h: mm(10), fill: { color: C.violet }, line: { color: C.violet, width: 0 }, rectRadius: 0.02 });
  s.addText(AG.message_sanitaire, { x, y: mm(PAGE_H - MARGE.bas - 14), w: mm(CADRE_L), h: mm(10),
    margin: 0, align: 'center', valign: 'middle', fontFace: F.tech, fontSize: 8.5, bold: true,
    color: C.craie });
}

/* ———————————————————————————————————————— montage ——— */

plan.descripteurs.forEach((desc, i) => {
  const numero = i + 1;
  const sombre = desc.type === 'ouverture' || desc.type === 'planche';
  const s = nouvelle(numero, { fond: sombre ? C.silex : C.tuffeau });
  switch (desc.type) {
    case 'couverture': slideCouverture(s, numero); break;
    case 'agence': slideAgence(s, numero); break;
    case 'mode-emploi': slideModeEmploi(s, numero); break;
    case 'sommaire': slideSommaire(s, numero); break;
    case 'alliances': slideAlliances(s, numero); break;
    case 'ouverture': slideOuverture(s, numero, desc.region); break;
    case 'fiche': slideFiche(s, numero, desc); break;
    case 'index-vins': slideIndexVins(s, numero, desc); break;
    case 'produits': slideProduits(s, numero); break;
    case 'index-domaines': slideIndexDomaines(s, numero); break;
    case 'planche': slidePlanche(s, numero); break;
    case 'notes': slideNotes(s, numero); break;
    case 'finale': slideFinale(s, numero); break;
  }
});

const sortie = path.join(RACINE, RECADRABLE ? 'dist/catalogue-scio-2026-canva-recadrable.pptx'
  : 'dist/catalogue-scio-2026-canva.pptx');
await pres.writeFile({ fileName: sortie });
fs.writeFileSync(path.join(RACINE, 'build/pptx-textes.json'), JSON.stringify(BOITES, null, 1));
console.log(`✓ ${path.relative(RACINE, sortie)} — ${plan.descripteurs.length} diapositives`);
if (debordements.length) {
  console.error('\n⚠ débordements sous les tableaux :');
  debordements.forEach((l) => console.error('  · ' + l));
  process.exit(1);
}
