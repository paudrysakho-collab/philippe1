/* Fabrique le catalogue en .pptx, importable dans Canva, texte et tableaux modifiables.
   Même contenu, même pagination et même maquette que le PDF : tout vient de build/plan.json.
   Les deux emplacements d'image prennent l'image préparée quand il y en a une
   (data/photos-preparees.json) ; sinon ce sont des formes vides, à remplacer dans Canva. */
import fs from 'node:fs';
import path from 'node:path';
import PptxGenJS from 'pptxgenjs';
import {
  catalogue, REGIONS, STRATES, euros, famille, famillesDe, nbReferences, NOM_FAMILLE,
  groupes, groupeDe, corpsDomaine, EMPLACEMENT, emplacementPour, photoDe, creditPhotos,
  largeurTexte, lignesTexte, familleLabel, ORDRE_LABELS, BASE, EDITION, poidsStrates,
} from '../src/gabarits/pieces.mjs';
import { entreesIndex, colonnesSommaire, SOMMAIRE, mentionSommaire, texteNotePrix, SALON_ED, ED, NB_VINS,
  numero as numeroAffiche }
  from '../src/gabarits/pages.mjs';

const RACINE = path.resolve(import.meta.dirname, '..');
const DECO = path.join(RACINE, `build/deco-${BASE}`);
const plan = JSON.parse(fs.readFileSync(path.join(RACINE, `build/${BASE}-plan.json`), 'utf8'));
/* Les hauteurs mesurées dans Chromium pendant la fabrication du PDF : la diapositive
   reprend exactement la même géométrie, sans jamais estimer une hauteur de ligne. */
const mesures = JSON.parse(fs.readFileSync(path.join(RACINE, `build/${BASE}-mesures.json`), 'utf8'));
const EV = catalogue.salon?.evenement;
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
// un réglage par édition : au salon, les textes sont ceux des cartes de stand
const FICHIER_LETTRINES = path.join(RACINE, `src/gabarits/lettrines-pptx${EDITION === 'salon' ? '-salon' : ''}.json`);
const LETTRINES = fs.existsSync(FICHIER_LETTRINES)
  ? JSON.parse(fs.readFileSync(FICHIER_LETTRINES, 'utf8')) : {};
const LETTRINE_DEFAUT = 1.8;
const BOITES = {};   // n° → place du texte, pour regler-lettrines.py

/* Où tombe la ligne de base de la première ligne d'une boîte ancrée en haut, en fraction du
   corps. Mesuré sur une planche importée dans Canva et rendue par LibreOffice
   (essais/calibrage-canva.mjs) :
   - LibreOffice, comme PowerPoint : l'ascendante de la police, plus le supplément
     d'interligne, posé AU-DESSUS de la ligne (1,2 × corps × (interligne − 1)) ;
   - Canva : l'ascendante seule, quel que soit l'interligne (0,854 pour Spectral, que Canva
     remplace par Arimo tant qu'elle n'est pas téléversée ; 0,92 pour Young Serif). */
const BASE_LIGNE = { lo: { courant: 0.998, titre: 0.999, sus: 1.2 }, canva: { courant: 0.854, titre: 0.92 } };
const PT = 25.4 / 72;   // un point, en mm

/** Place la lettrine et le texte dans la bande, en mm, depuis le haut de la bande.
    Horizontalement : des espaces insécables réservent la place de la lettrine en tête de la
    première ligne, et la lettrine prend le corps exact qui remplit cette place (à quelques
    pour cent de la taille visée) ; alignée à droite dans sa boîte, elle reste collée à son
    mot même quand Canva la remplace par une police plus étroite.
    Verticalement : deux logiciels, deux façons de poser la première ligne. On cale la
    lettrine pour Canva, et son interligne à elle (que Canva ignore, et que LibreOffice
    applique) la recale pour LibreOffice et PowerPoint. Le bloc, de la tête de la lettrine
    au pied de la dernière ligne, se centre dans la bande comme le texte du PDF. */
function placerLettrine(texte, corps, interligne, visee, lignes, bande) {
  const { lo, canva } = BASE_LIGNE;
  const JOINT = 0.25;                                                       // mm avant la 2e lettre
  const chasse = largeurTexte(texte.slice(0, 1), F.titre, 1);               // mm par point de corps
  const insecable = largeurTexte('\u00a0', F.courant, corps);
  const nombre = Math.max(1, Math.round((chasse * visee + JOINT) / insecable));
  const taille = Math.round((nombre * insecable - JOINT) / chasse * 100) / 100;
  const baseLo = corps * (lo.courant + lo.sus * (interligne - 1));         // pt sous le haut du texte
  const lettre = (corps * canva.courant - taille * canva.titre) * PT;        // haut de la lettrine
  const interligneLettre = 1 + (baseLo - corps * canva.courant - taille * (lo.titre - canva.titre))
    / (lo.sus * taille);
  // le bloc (rendu LibreOffice) : la capitale de la lettrine (0,75 du corps) au-dessus de la
  // première ligne de base, les jambages (0,25) sous la dernière
  const tete = (baseLo - 0.75 * taille) * PT;
  const pied = (baseLo + (lignes - 1) * lo.sus * interligne * corps + 0.25 * corps) * PT;
  const largeur = chasse * taille + 1.5;                                    // la boîte, un peu d'aise à gauche
  return {
    haut: (bande - (pied - tete)) / 2 - tete, lettre, taille, largeur,
    gauche: nombre * insecable - JOINT - largeur, hauteur: taille * 1.6 * PT,
    interligneLettre: Math.round(interligneLettre * 1000) / 1000,
    reserve: '\u00a0'.repeat(nombre),
  };
}

const PAGE_L = 210, PAGE_H = 260;
const MARGE = { haut: 15, bas: 13, int: 17, ext: 14 };
const CAROTTE = 9;
const CADRE_L = PAGE_L - MARGE.int - MARGE.ext - CAROTTE;   // 170 mm
const CADRE_H = PAGE_H - MARGE.haut - MARGE.bas;            // 232 mm

const cle = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '')
  .replace(/[^A-Za-z0-9]+/g, '-').toLowerCase();
const img = (nom) => {
  const jpg = path.join(DECO, `${nom}.jpg`);
  return fs.existsSync(jpg) ? jpg : path.join(DECO, `${nom}.png`);
};
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
pres.title = SALON_ED ? `${EV.nom} — ${EV.date_texte}` : 'Sous nos pieds — Tarifs cavistes Vendée (85) 2026';

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
    // toujours à droite (l'agence, 3 octobre au soir), comme .folio du PDF
    x: verso ? mm(PAGE_L - MARGE.int - 15) : mm(PAGE_L - MARGE.ext - CAROTTE - 15),
    y: mm(PAGE_H - 11), w: mm(15), h: mm(5), margin: 0,
    align: 'right', fontFace: F.tech, fontSize: 7.5,
    color: clair ? C.craie : C.silex, transparency: 28,
  });
  s.addText(AG.message_sanitaire, {
    x: verso ? mm(MARGE.ext + CAROTTE) : mm(MARGE.int), y: mm(PAGE_H - 11),
    w: mm(95), h: mm(5), margin: 0, align: 'left',
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
  // comme le PDF (table.tarif.p4) : à quatre paliers, le bloc de prix passe de 52 à 66 mm
  const BLOC = n > 3 ? 66 : 52;
  const largeurs = [mm(6.5), mm(CADRE_L - 6.5 - 17 - 16 - BLOC), mm(17), mm(16),
    ...Array(n).fill(mm(BLOC / n))];
  const bordure = [{ type: 'solid', color: 'C7D1D6', pt: 0.3 }];

  const entete = [
    { text: `${t.intitule}${t.famille ? ' · ' + t.famille : ''}`.toUpperCase(),
      options: { colspan: 4, fill: C.violet, color: C.or, fontFace: F.tech, fontSize: 8,
        bold: true, valign: 'bottom', margin: [3, 4, 3, 6], charSpacing: 0.3 } },
    ...t.paliers.map((p) => ({ text: p, options: {
      fill: C.violet, color: C.craie, fontFace: F.tech, fontSize: 7.2, bold: true,
      align: 'right', valign: 'bottom', margin: [3, 5, 3, 3] } })),
  ];

  const corps = lignes.map((l, i) => {
    const f = famille(l, t);
    const [remplissage] = PICTO[f] || PICTO.autre;
    const fondLigne = i % 2 === 0 ? C.craie : C.tuffeau;
    // marges et interligne serrés, comme le PDF : l'écriture est grande, la ligne ne grandit pas
    const commun = { fill: fondLigne, valign: 'middle', margin: [1.6, 3, 1.6, 3] };
    return [
      { text: '●', options: { ...commun, color: remplissage === 'FFFFFF' ? C.silex : remplissage,
        fontSize: 10, align: 'center' } },
      { text: [
          { text: l.appellation + (l.note === '*' ? ' *' : ''),
            // sans cuvée, l'offre reste sur la ligne de l'appellation, comme dans le PDF
            options: { fontFace: F.tech, fontSize: 8, color: C.gneiss, breakLine: !!l.cuvee || !l.offre, lineSpacingMultiple: 0.9 } },
          // comme le PDF : les deux derniers mots de la cuvée restent ensemble (espace insécable)
          ...(l.cuvee ? [{ text: l.cuvee.replace(/ (\S+)$/, '\u00a0$1'), options: { fontFace: F.tech, fontSize: 9.6, bold: true, color: C.encre,
            lineSpacingMultiple: 0.9 } }] : []),
          // l'offre du salon (11+1, 5+1), juste après le nom du vin, comme .offre du PDF
          ...(l.offre ? [{ text: `  offre\u00a0${l.offre}${l.offre_detail ? ' ' + l.offre_detail.replace(/ (\S+)$/, '\u00a0$1') : ''}`,
            options: { fontFace: F.tech, fontSize: 7.4, bold: true, color: C.violet, highlight: 'F0E3A6',
              lineSpacingMultiple: 0.9 } }] : []),
        ], options: { ...commun, margin: [1.6, 3, 1.6, 4] } },
      { text: l.millesime || '—', options: { ...commun, fontFace: F.tech, fontSize: 8,
        color: C.silex, align: 'right' } },
      { text: l.contenance || '—', options: { ...commun, fontFace: F.tech, fontSize: 8,
        color: C.silex, align: 'right' } },
      // un prix pas encore donné (édition salon) : une case vide, à remplir dans Canva
      // un seul prix pour une ligne à plusieurs paliers : une case fusionnée, comme .cel-prix.seul
      ...(l.prix_centimes.length === 1 && n > 1 && l.prix_centimes[0] != null ? [{ text: [
          { text: euros(l.prix_centimes[0]), options: { fontFace: F.tech, fontSize: 10, bold: true, color: C.encre } },
          { text: ' €', options: { fontFace: F.tech, fontSize: 7.2, color: C.encre } },
        ], options: { ...commun, align: 'center', colspan: n } }] : l.prix_centimes.map((p) => (p == null
        ? { text: '', options: { ...commun, align: 'right', fontFace: F.tech, fontSize: 10, bold: true,
          color: C.encre } }
        : { text: [
          { text: euros(p), options: { fontFace: F.tech, fontSize: 10, bold: true, color: C.encre } },
          { text: ' €', options: { fontFace: F.tech, fontSize: 7.2, color: C.encre } },
        ], options: { ...commun, align: 'right' } }))),
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
  // au salon, la pastille du stand (19 mm) remplace le numéro du tarif
  const RETRAIT = SALON_ED ? 23 : largeur(`${d.numero}   `, F.titre, 27);
  const SUITE = desc.premiere ? 0 : largeur('  (suite)', 'Spectral', 11);
  const dispo = LARGEUR_TITRE - RETRAIT - SUITE;
  const pleine = largeur(d.nom, F.titre, 20);
  const taille = pleine <= dispo ? 20
    : Math.max(15, Math.floor(20 * dispo / pleine * 2) / 2);
  const nbLignes = Math.max(1, lignesDe(d.nom, F.titre, taille, dispo));
  const hTitre = 11 + (nbLignes - 1) * 8.4;
  const suiteTxt = desc.premiere ? [] : [{ text: '  (suite)', options: {
    fontFace: F.courant, fontSize: 11, italic: true, color: C.gneiss } }];
  if (SALON_ED) {
    // la hauteur de l'en-tête vient de la mesure du PDF : la pastille y tient, centrée
    const hEnt = (mesures.blocs[`entete-${d.numero}`] ?? 26) - 11.7;
    const hP = 14.4, yP = y + mm((hEnt - hP) / 2);
    s.addShape(pres.ShapeType.roundRect, { x, y: yP, w: mm(19), h: mm(hP), fill: { color: C.or },
      line: { color: C.or, width: 0 }, rectRadius: 0.06 });
    s.addText([
      { text: 'STAND', options: { fontFace: F.tech, fontSize: 7, bold: true, breakLine: true, charSpacing: 0.3 } },
      { text: String(d.stand), options: { fontFace: F.titre, fontSize: 22, breakLine: true } },
      { text: d.salle, options: { fontFace: F.tech, fontSize: 7 } },
    ], { x, y: yP, w: mm(19), h: mm(hP), margin: 0, align: 'center', valign: 'middle',
      color: C.violet, lineSpacingMultiple: 0.95 });
    s.addText([{ text: d.nom, options: { fontFace: F.titre, fontSize: taille, color: C.silex } }, ...suiteTxt],
      { x: x + mm(RETRAIT), y, w: mm(LARGEUR_TITRE - RETRAIT), h: mm(hEnt), margin: 0, valign: 'middle',
        lineSpacingMultiple: 1.04 });
  } else {
  s.addText([
    { text: String(d.numero), options: { fontFace: F.titre, fontSize: 27, color: C.violet } },
    { text: `   ${d.nom}`, options: { fontFace: F.titre, fontSize: taille, color: C.silex } },
    ...suiteTxt,
  ], { x, y, w: mm(LARGEUR_TITRE), h: mm(hTitre), margin: 0, valign: 'middle',
    lineSpacingMultiple: 1.04 });
  }
  const hRegion = SALON_ED ? (mesures.blocs[`entete-${d.numero}`] ?? 26) - 11.7 : 11;
  s.addText(d.region.toUpperCase(), {
    x: mm(gauche + CADRE_L - 40), y, w: mm(40), h: mm(hRegion), margin: 0,
    align: 'right', valign: 'middle', fontFace: F.tech, fontSize: 8, bold: true,
    color: C.gneiss, charSpacing: 0.3,
  });
  y += SALON_ED ? mm(hRegion + 0.1) : mm(hTitre + 0.1);
  s.addShape(pres.ShapeType.line, { x, y, w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 1.4 } });
  y += mm(1.8);

  // ——— jetons
  const jetons = [
    ...d.labels.map((l) => [l.label, C.amphibolite, null, familleLabel(l.label)]),
    ...(d.allocation ? [['Allocation', C.violet, C.violet]] : []),
    [groupeDe(d) ? 'Panachage entre domaines' : 'Panachage dans le domaine', C.gneiss, null],
    ...(d.mentions.some((m) => m.toLowerCase().includes('consultez-nous'))
      ? [['Consultez-nous', C.sables, C.sables]] : []),
    [`${nbReferences(d)} ${nbReferences(d) > 1 ? ED.motVins : ED.motVin}`, C.silex, null],
  ];
  let jx = gauche;
  jetons.forEach(([texte, couleur, fond, pictoLabel]) => {
    // le picto de label (une feuille maison) se pose dans le jeton, avant le mot
    const p = pictoLabel ? 4.1 : 0;
    const l = largeur(texte, 'IBM Plex Sans Bold', 7.2) + 5.6 + p;
    s.addShape(pres.ShapeType.roundRect, { x: mm(jx), y, w: mm(l), h: mm(5),
      fill: fond ? { color: fond } : { color: C.tuffeau },
      line: { color: couleur, width: 0.7 }, rectRadius: 0.02 });
    if (pictoLabel) {
      s.addImage({ path: img(`label-${pictoLabel}`), x: mm(jx + 2), y: y + mm(1), w: mm(3), h: mm(3) });
    }
    s.addText(texte, { x: mm(jx + p), y, w: mm(l - p), h: mm(5), margin: 0, align: 'center',
      valign: 'middle', fontFace: F.tech, fontSize: 7.2, bold: true,
      color: fond ? C.craie : couleur });
    jx += l + 2.2;
  });
  y += mm(8.0);

  if (desc.premiere) {
    // ——— les deux emplacements, et le texte entre les deux. L'image prend la place de
    // la forme pointillée quand il y en a une ; sinon l'emplacement reste réservé.
    // La bande fait la hauteur mesurée dans Chromium : la même que dans le PDF.
    // la bande du haut peut avoir été abaissée par la pagination (desc.bande) : la bouteille
    // rapetisse, la colonne de texte s'élargit, comme dans le PDF
    const hBande = desc.bande ?? EMPLACEMENT.bouteille.h;
    const { rond, bouteille, ecart, colonne } = emplacementPour(hBande);
    const bande = (mesures.blocs[`haut-${d.numero}-${hBande}`] ?? 65.6) - 3.6;
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
      // contenue dans sa case (24 × 62 mm au plus), proportions gardées, posée sur le bas comme dans le PDF
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
    // La lettrine, comme dans le PDF : la première lettre en Young Serif violette, montante
    // (un .pptx ne sait pas faire tomber une lettre sur deux lignes). Elle a SA boîte de texte :
    // à l'import, Canva ramène tout un paragraphe à une seule police et une seule taille, et une
    // lettrine écrite dans le texte n'y gardait que sa couleur. Des espaces insécables lui
    // réservent sa place en tête de la première ligne ; sa ligne de base est calée sur celle
    // du texte, dans Canva comme dans LibreOffice ou PowerPoint (voir placerLettrine()).
    const corps = d.texte_source ? corpsDomaine(d, colonne, hBande) : 9;
    const xt = gauche + rond + ecart;
    if (d.texte_source) {
      const reglage = LETTRINES[d.numero] ?? {};
      const interligne = reglage.interligne ?? 1.42;
      const lignes = reglage.lignes ?? lignesTexte(texte, F.courant, corps, colonne);
      const p = placerLettrine(texte, corps, interligne, corps * (reglage.lettrine ?? LETTRINE_DEFAUT),
        lignes, bande);
      const taille = p.taille;
      const yTexte = y / mm(1) + p.haut;
      s.addText(texte.slice(0, 1), { x: mm(xt + p.gauche), y: mm(yTexte + p.lettre), w: mm(p.largeur),
        h: mm(p.hauteur), margin: 0, fontFace: F.titre, fontSize: taille, color: C.violet,
        lineSpacingMultiple: p.interligneLettre, align: 'right', valign: 'top' });
      s.addText(p.reserve + texte.slice(1), { x: mm(xt), y: mm(yTexte), w: mm(colonne),
        h: mm(bande - p.haut), margin: 0, fontFace: F.courant, fontSize: corps, color: C.silex,
        lineSpacingMultiple: interligne, valign: 'top' });
      BOITES[d.numero] = { diapo: pres.slides.length, x: xt, y: y / mm(1), w: colonne, h: bande,
        corps, interligne, lettrine: taille };
    } else {
      s.addText(texte, { x: mm(xt), y, w: mm(colonne), h: mm(bande), margin: 0,
        fontFace: F.courant, fontSize: corps, color: C.silex, lineSpacingMultiple: 1.42,
        italic: true, valign: 'middle' });
    }
    y += mm(bande + 3.6);
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
      + mm(k < desc.morceaux.length - 1 ? 3.6 : 0);
  });

  // ——— la note de prix, juste sous le dernier tableau, en grand (comme .note-prix du PDF)
  if (desc.note) {
    const hNote = mesures.blocs[`note-${d.numero}`] ?? 9;
    s.addShape(pres.ShapeType.line, { x, y: y + mm(2), w: 0, h: mm(hNote - 2),
      line: { color: C.violet, width: 1.4 } });
    // au salon, l'offre du stand suit la note de prix, en violet (comme .offre-salon du PDF)
    // l'offre d'abord, la note de prix dessous (l'agence, 3 octobre au soir)
    s.addText([
      ...(d.offre_salon ? [{ text: d.offre_salon, options: { color: C.violet, bold: true, breakLine: true } }] : []),
      { text: texteNotePrix(d), options: { color: C.encre, italic: !d.note_prix } },
    ], { x: x + mm(3), y: y + mm(2), w: mm(CADRE_L - 3), h: mm(hNote - 2),
      margin: 0, valign: 'middle', fontFace: F.tech, fontSize: 10.5, lineSpacingMultiple: 1.1 });
    y += mm(hNote);
  }

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
  // calé sur le pied du PDF (.pied-dom, .legende, .alliance) : le filet à 11 mm du bas du cadre
  const yPied = mm(PAGE_H - MARGE.bas - 11);
  const g = groupeDe(d);
  const plafond = yPied - mm(g ? 9.9 : 1.5);
  if (y > plafond) {
    debordements.push(`diapo ${numero} (n°${d.numero} ${d.nom}) : `
      + `${((y - plafond) * 25.4).toFixed(1)} mm de trop sous les tableaux`);
  }
  if (g) {
    const autres = (g.presents || g.domaines).filter((n) => n !== d.numero)
      .map((n) => (SALON_ED ? `${parNumero[n].nom}, stand ${parNumero[n].stand} p. ${pageDe[n]}`
        : `n°${n} p. ${pageDe[n]}`)).join(' · ');
    s.addText([
      { text: 'Se panache avec ', options: { bold: true, color: C.gneiss } },
      { text: `${g.libelle}${autres ? ` — ${autres}` : ''}`, options: { color: C.silex } },
    ], { x, y: yPied - mm(8.4), w: mm(CADRE_L), h: mm(6.6), margin: [2, 3, 2, 3],
      fill: { color: 'F4E7E9' }, fontFace: F.tech, fontSize: 7.4, valign: 'middle' });
  }
  s.addShape(pres.ShapeType.line, { x, y: yPied, w: mm(CADRE_L), h: 0,
    line: { color: C.silex, width: 0.7 } });
  s.addText([
    { text: 'Distribution ', options: { bold: true, color: C.violet } },
    { text: d.departements.length ? d.departements.join(' · ')
      : 'non précisés par le domaine — nous consulter', options: { color: C.silex } },
  ], { x, y: yPied + mm(1.2), w: mm(CADRE_L), h: mm(4.5),
    margin: 0, align: 'left', fontFace: F.tech, fontSize: 7.2 });
  s.addText(famillesDe(d).map((f) => `● ${NOM_FAMILLE[f]}`).join('    ')
    + '     pictos de l’Agence SCIO, pas les logos officiels', {
    x, y: yPied + mm(5.8), w: mm(CADRE_L), h: mm(4), margin: 0,
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
  // couverture H : le ciel en photo, les strates droites dessous, une réserve claire sous le logo
  const HC = SALON_ED ? 108 : 148;   // hauteur de la bande de strates (plus basse au salon)
  s.addImage({ path: img('couv-ciel'), x: 0, y: 0, w: mm(PAGE_L), h: mm(PAGE_H - HC + 2) });
  s.addImage({ path: img('coupe-titree'), x: 0, y: mm(PAGE_H - HC), w: mm(PAGE_L), h: mm(HC) });
  s.addShape(pres.ShapeType.roundRect, { x: mm(MARGE.int - 4), y: mm(13), w: mm(70), h: mm(24),
    fill: { color: C.craie }, line: { color: C.craie, width: 0 }, rectRadius: 0.05 });
  s.addImage({ path: path.join(RACINE, 'src/images/logo-agence-scio-detoure.png'),
    x: mm(MARGE.int), y: mm(17), w: mm(62), h: mm(62 * 251 / 1030) });
  const sousTitre = ED.sousTitre.replace('<br>', '\n');
  if (SALON_ED) {
    s.addText([
      { text: 'Salon Privé', options: { breakLine: true } },
      { text: 'Vins & Terroirs', options: { color: C.or } },
    ], { x: mm(MARGE.int), y: mm(42), w: mm(165), h: mm(34), margin: 0,
      fontFace: F.titre, fontSize: 44, color: C.craie, lineSpacingMultiple: 0.92 });
    s.addText(sousTitre, { x: mm(MARGE.int), y: mm(89), w: mm(120), h: mm(14), margin: 0,
      fontFace: F.courant, fontSize: 10.5, color: C.craie, lineSpacingMultiple: 1.4 });
    // la validité du tarif et des offres, bien visible sous le titre (comme .validite-couv) ;
    // la date et le lieu ne sont plus en couverture (l'agence, 3 octobre au soir)
    s.addShape(pres.ShapeType.roundRect, { x: mm(MARGE.int), y: mm(110), w: mm(140), h: mm(27),
      fill: { color: C.violet }, line: { color: C.violet, width: 0 }, rectRadius: 0.05 });
    s.addShape(pres.ShapeType.rect, { x: mm(MARGE.int), y: mm(110), w: mm(1.6), h: mm(27),
      fill: { color: C.or }, line: { color: C.or, width: 0 } });
    s.addText([
      { text: 'Tarif et offres valables', options: { color: C.or, breakLine: true } },
      { text: 'du 5 octobre au 14 novembre 2026', options: { color: C.craie } },
    ], { x: mm(MARGE.int + 6), y: mm(110), w: mm(132), h: mm(27), margin: 0, valign: 'middle',
      fontFace: F.titre, fontSize: 21, lineSpacingMultiple: 1.0 });
  } else {
  s.addText([
    { text: 'Sous', options: { breakLine: true } },
    { text: 'nos', options: { breakLine: true } },
    { text: 'pieds', options: { color: C.or } },
  ], { x: mm(MARGE.int), y: mm(42), w: mm(150), h: mm(50), margin: 0,
    fontFace: F.titre, fontSize: 46, color: C.craie, lineSpacingMultiple: 0.92 });
  s.addText(sousTitre, {
    x: mm(MARGE.int), y: mm(95), w: mm(120), h: mm(14), margin: 0,
    fontFace: F.courant, fontSize: 10.5, color: C.craie, lineSpacingMultiple: 1.4 });
  // la cible et l'année, en haut, en face du logo (comme .edition-couv du PDF)
  s.addText(AG.cible.toUpperCase(), { x: mm(PAGE_L - MARGE.int - 80), y: mm(17), w: mm(80), h: mm(5),
    margin: 0, align: 'right', fontFace: F.tech, fontSize: 9, bold: true, color: C.craie, charSpacing: 0.3 });
  s.addText(AG.edition, { x: mm(PAGE_L - MARGE.int - 60), y: mm(22.5), w: mm(60), h: mm(13), margin: 0,
    align: 'right', valign: 'top', fontFace: F.titre, fontSize: 34, color: C.craie });
  }
  s.addText(AG.message_sanitaire, { x: mm(PAGE_L - MARGE.int - 140), y: mm(PAGE_H - 13), w: mm(140), h: mm(5),
    margin: 0, align: 'right', fontFace: F.tech, fontSize: 5.6, color: C.encre });
}

function slideAgence(s, numero) {
  const { gauche } = geo(numero);
  const x = mm(gauche);
  s.addImage({ path: path.join(RACINE, 'src/images/logo-agence-scio-detoure.png'),
    x, y: mm(MARGE.haut), w: mm(74), h: mm(74 * 251 / 1030) });
  // page 2 A : texte posé en Spectral, filet or à gauche (comme .credo du PDF)
  s.addShape(pres.ShapeType.line, { x, y: mm(MARGE.haut + 32), w: 0, h: mm(32),
    line: { color: C.or, width: 1.2 } });
  s.addText("L'Agence SCIO, c'est partager notre savoir et notre passion en vous proposant des "
    + 'vignerons de tous horizons, avant-gardistes et respectueux de la nature. Découvrez notre '
    + 'sélection. Laissez-vous guider et conseiller.',
  { x: x + mm(5), y: mm(MARGE.haut + 32), w: mm(140), h: mm(32), margin: 0, valign: 'top',
    fontFace: F.courant, fontSize: 14.5, color: C.encre, lineSpacingMultiple: 1.45 });

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
  if (SALON_ED) {
    // l'encart du salon prend la place de la coupe : nom, date, lieu, organisateur
    const ye = MARGE.haut + 122;
    s.addShape(pres.ShapeType.rect, { x, y: mm(ye), w: mm(CADRE_L), h: mm(36),
      fill: { color: C.craie }, line: { color: C.craie, width: 0 } });
    s.addShape(pres.ShapeType.line, { x, y: mm(ye), w: 0, h: mm(36), line: { color: C.or, width: 2 } });
    s.addText([
      { text: EV.nom, options: { fontFace: F.titre, fontSize: 18, color: C.violet, breakLine: true } },
      { text: EV.date_texte, options: { fontFace: F.titre, fontSize: 13, color: C.silex, breakLine: true } },
      { text: `${EV.lieu}, ${EV.commune}`, options: { fontFace: F.courant, fontSize: 10, color: C.silex, breakLine: true } },
      { text: `Organisé par l'${EV.organisateur}`, options: { fontFace: F.tech, fontSize: 8, color: C.gneiss } },
    ], { x: x + mm(6), y: mm(ye), w: mm(CADRE_L - 12), h: mm(36), margin: 0, valign: 'middle',
      lineSpacingMultiple: 1.25 });
  } else {
    s.addImage({ path: img('agence-photo'), x, y: mm(MARGE.haut + 118), w: mm(CADRE_L),
      h: mm(CADRE_L * 46 / 176) });
  }
  const yc = MARGE.haut + 172;
  s.addShape(pres.ShapeType.line, { x, y: mm(yc), w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 0.8 } });
  [[String(ED.acteurs), ED.motActeurs], [String(REGIONS.length), 'régions'],
    [String(NB_VINS), ED.motVins]].forEach(([n, l], i) => {
    s.addText(n, { x: mm(gauche + i * 42), y: mm(yc + 3), w: mm(40), h: mm(11), margin: 0,
      fontFace: F.titre, fontSize: 26, color: C.violet });
    s.addText(l, { x: mm(gauche + i * 42), y: mm(yc + 14), w: mm(40), h: mm(5), margin: 0,
      fontFace: F.tech, fontSize: 9, color: C.silex });
  });
  folio(s, numero);
}

/** Le sommaire, liste par région sur deux colonnes : la géométrie de SOMMAIRE, comme le PDF. */
function slideSommaire(s, numero) {
  const { gauche } = geo(numero);
  const y0 = SALON_ED
    ? titreSection(s, numero, 'Sommaire', 'par région ; le premier chiffre est le numéro du stand') + 0.5
    : MARGE.haut + 8.5 + 6;
  if (!SALON_ED) {
    s.addText('Sommaire', { x: mm(gauche), y: mm(MARGE.haut), w: mm(CADRE_L), h: mm(9), margin: 0,
      fontFace: F.titre, fontSize: 24, color: C.violet, valign: 'top' });
  }
  const { bande, ligne, apresBande, entreRegions, colonne } = SOMMAIRE;
  colonnesSommaire().forEach((blocs, c) => {
    const cx = gauche + c * (CADRE_L - colonne);
    let y = y0;
    blocs.forEach((b) => {
      const st = STRATES[b.nom];
      // version sobre (pour l'impression) : une pastille de strate, le nom en violet, un filet
      s.addShape(pres.ShapeType.rect, { x: mm(cx), y: mm(y + (bande - 3.2) / 2), w: mm(3.2), h: mm(3.2),
        fill: { color: st.hex.slice(1) },
        line: { color: b.nom === 'Champagne' ? C.silex : st.hex.slice(1), width: 0.6 } });
      s.addText(b.nom, { x: mm(cx + 5.4), y: mm(y), w: mm(colonne - 6), h: mm(bande), margin: 0,
        fontFace: F.titre, fontSize: 13, color: C.violet, valign: 'middle' });
      s.addShape(pres.ShapeType.line, { x: mm(cx), y: mm(y + bande), w: mm(colonne), h: 0,
        line: { color: C.violet, width: 0.9 } });
      y += bande + apresBande;
      b.doms.forEach((d) => {
        // un domaine d'un groupe : la mention en petit sous le nom, comme dans le PDF
        const mention = mentionSommaire(d);
        const hl = mention ? SOMMAIRE.ligneMention : ligne;
        if (mention) {
          s.addText(`(${mention})`, { x: mm(cx + 8.5), y: mm(y + ligne - 0.6), w: mm(colonne - 18), h: mm(3.2),
            margin: 0, valign: 'middle', fontFace: F.tech, fontSize: 7.2, color: C.gneiss });
        }
        s.addText(String(numeroAffiche(d)), { x: mm(cx), y: mm(y), w: mm(6.1), h: mm(ligne), margin: 0,
          align: 'right', valign: 'middle', fontFace: F.tech, fontSize: 8.5, bold: true, color: C.violet });
        s.addText(d.nom, { x: mm(cx + 8.5), y: mm(y), w: mm(colonne - 18), h: mm(ligne), margin: 0,
          valign: 'middle', fontFace: F.courant, fontSize: 10, color: C.encre });
        s.addText(String(pageDe[d.numero]), { x: mm(cx + colonne - 10), y: mm(y), w: mm(9), h: mm(ligne),
          margin: 0, align: 'right', valign: 'middle', fontFace: F.tech, fontSize: 9, bold: true,
          color: C.silex });
        s.addShape(pres.ShapeType.line, { x: mm(cx), y: mm(y + hl), w: mm(colonne), h: 0,
          line: { color: 'C9CFC9', width: 0.3 } });
        y += hl;
      });
      y += entreRegions;
    });
  });
  // la légende complète des pictos, en bas de page, comme dans le PDF
  const familles = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux'];
  const labels = ORDRE_LABELS.filter((l) => catalogue.domaines.some((d) => d.labels.some((x) => x.label === l)));
  const yl = PAGE_H - MARGE.bas - 17;
  s.addShape(pres.ShapeType.line, { x: mm(gauche), y: mm(yl), w: mm(CADRE_L), h: 0,
    line: { color: C.violet, width: 0.8 } });
  s.addText([
    { text: 'Types    ', options: { bold: true, color: C.violet } },
    ...familles.flatMap((f) => {
      const [remplissage] = PICTO[f] || PICTO.autre;
      return [{ text: '●', options: { color: remplissage === 'FFFFFF' ? C.silex : remplissage } },
        { text: `\u00a0${NOM_FAMILLE[f]}    ` }];
    }),
  ], { x: mm(gauche), y: mm(yl + 2), w: mm(CADRE_L), h: mm(4.5), margin: 0,
    fontFace: F.tech, fontSize: 7.4, color: C.silex, valign: 'middle' });
  let lx = gauche + 13;
  s.addText('Labels', { x: mm(gauche), y: mm(yl + 7), w: mm(13), h: mm(4.5), margin: 0,
    fontFace: F.tech, fontSize: 7.4, bold: true, color: C.violet, valign: 'middle' });
  labels.forEach((l) => {
    const w = largeur(l, 'IBM Plex Sans', 7.4) + 1.5;
    s.addImage({ path: img(`label-${familleLabel(l)}`), x: mm(lx), y: mm(yl + 7.75), w: mm(3), h: mm(3) });
    s.addText(l, { x: mm(lx + 4.1), y: mm(yl + 7), w: mm(w), h: mm(4.5), margin: 0,
      fontFace: F.tech, fontSize: 7.4, color: C.silex, valign: 'middle' });
    lx += 4.1 + w + 3;
  });
  s.addText("Ces pictos sont ceux de l'Agence SCIO, dessinés pour ce catalogue : ce ne sont pas "
    + 'les logos officiels des organismes certificateurs.', { x: mm(gauche), y: mm(yl + 12), w: mm(CADRE_L),
    h: mm(4), margin: 0, fontFace: F.tech, fontSize: 7.6, italic: true, color: C.silex });
  folio(s, numero);
}

function slideOuverture(s, numero, region) {
  s.addImage({ path: img(`ouverture-${cle(region)}`), x: 0, y: 0, w: mm(PAGE_L), h: mm(PAGE_H) });
  poserCarotte(s, numero, region);
  const { gauche } = geo(numero);
  const clair = false;   // ouverture A : la photo assombrie porte toujours un texte clair
  const encre = C.craie;
  const doms = catalogue.domaines.filter((d) => d.region === region);
  const refs = doms.reduce((n, d) => n + nbReferences(d), 0);
  s.addText(`${REGIONS.indexOf(region) + 1} / ${REGIONS.length}`, { x: mm(gauche), y: mm(MARGE.haut),
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
  s.addText(refs > 1 ? ED.motVins : ED.motVin, { x: mm(gauche + 28), y: mm(185), w: mm(45), h: mm(5), margin: 0,
    fontFace: F.tech, fontSize: 8.5, color: encre });
  doms.forEach((d, k) => {
    const col = k % 2, rang = Math.floor(k / 2);
    s.addText([
      { text: `${numeroAffiche(d)}   `, options: { fontFace: F.titre, fontSize: 11 } },
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
    s.addText(ED.introIndexVins, {
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
  const y = titreSection(s, numero, ED.titreIndexDomaines, 'de A à Z');
  const tries = [...catalogue.domaines].sort((a, b) =>
    a.nom.localeCompare(b.nom, 'fr', { sensitivity: 'base' }));
  const parCol = Math.ceil(tries.length / 2);
  tries.forEach((d, i) => {
    const col = Math.floor(i / parCol), rang = i % parCol;
    s.addText([
      { text: `${numeroAffiche(d)}   `, options: { fontFace: F.titre, fontSize: 11, color: C.violet } },
      { text: `${d.nom}   `, options: { bold: true } },
      { text: `${d.region}   `, options: { color: C.gneiss, fontSize: 7 } },
      { text: `${nbReferences(d)}   `, options: { fontSize: 7, color: C.silex } },
      { text: String(pageDe[d.numero]), options: { bold: true } },
    ], { x: mm(gauche + col * (CADRE_L / 2)), y: mm(y + rang * 8), w: mm(CADRE_L / 2 - 4),
      h: mm(7), margin: 0, fontFace: F.tech, fontSize: 8.4, color: C.silex, valign: 'middle' });
  });
  s.addText(ED.piedIndexDomaines, {
    x: mm(gauche), y: mm(PAGE_H - MARGE.bas - 8), w: mm(CADRE_L), h: mm(5), margin: 0,
    fontFace: F.courant, fontSize: 8, color: C.silex });
  folio(s, numero);
}

/** Comme dans le PDF : la légende se pose au-dessus de la strate de craie, trop claire. */
function margePlanche() {
  const { poids, total } = poidsStrates();
  return Math.max(18, (poids[poids.length - 1] / total) * PAGE_H - MARGE.bas + 6);
}

function slidePlanche(s, numero) {
  s.addImage({ path: img('coupe-pleine'), x: 0, y: 0, w: mm(PAGE_L), h: mm(PAGE_H) });
  const { gauche } = geo(numero);
  const n = { 9: 'neuf', 10: 'dix', 26: 'vingt-six', 40: 'quarante' };
  const mot = (k) => n[k] || String(k);
  s.addText(`${mot(REGIONS.length).replace(/^./, (c) => c.toUpperCase())} régions,\n${mot(REGIONS.length)} sols,\n`
    + `${mot(ED.acteurs)} ${ED.motActeurs}.`, {
    x: mm(gauche), y: mm(PAGE_H - MARGE.bas - margePlanche() - 42), w: mm(120), h: mm(42), margin: 0,
    fontFace: F.titre, fontSize: 26, color: C.craie, lineSpacingMultiple: 1.12 });
  folio(s, numero, { clair: true });
}

/** Page réglée : le caviste note ses quantités en lisant les tarifs. */
function slideNotes(s, numero) {
  const { gauche } = geo(numero);
  const x = mm(gauche);
  s.addText('Vos notes', { x, y: mm(MARGE.haut), w: mm(CADRE_L), h: mm(9), margin: 0,
    fontFace: F.titre, fontSize: 20, color: C.violet, valign: 'bottom' });
  s.addText(ED.notesSous.toUpperCase(), {
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
  if (SALON_ED) {
    s.addText(`${EV.nom}\n${EV.date_texte}, ${EV.lieu}, ${EV.commune}`, {
      x, y: mm(MARGE.haut + 46), w: mm(CADRE_L), h: mm(11), margin: 0,
      fontFace: F.titre, fontSize: 12, color: C.violet, lineSpacingMultiple: 1.2 });
  }
  s.addText(`${AG.contacts.adresse}\n${AG.contacts.email} · ${AG.contacts.site}`, {
    x, y: mm(MARGE.haut + (SALON_ED ? 59 : 46)), w: mm(130), h: mm(14), margin: 0,
    fontFace: F.courant, fontSize: 10, color: C.silex, lineSpacingMultiple: 1.5 });
  // au salon, la ligne du salon décale l'adresse : la coupe descend d'autant et s'aplatit
  const dy = SALON_ED ? 14 : 0;
  s.addImage({ path: img('coupe-nue'), x, y: mm(MARGE.haut + 66 + dy), w: mm(CADRE_L),
    h: mm(CADRE_L * 42 / 176 - dy) });

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
    case 'sommaire': slideSommaire(s, numero); break;
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

const sortie = path.join(RACINE, `dist/${BASE}-canva${RECADRABLE ? '-recadrable' : ''}.pptx`);
await pres.writeFile({ fileName: sortie });
fs.writeFileSync(path.join(RACINE, `build/${BASE}-pptx-textes.json`), JSON.stringify(BOITES, null, 1));
console.log(`✓ ${path.relative(RACINE, sortie)} — ${plan.descripteurs.length} diapositives`);
if (debordements.length) {
  console.error('\n⚠ débordements sous les tableaux :');
  debordements.forEach((l) => console.error('  · ' + l));
  process.exit(1);
}
