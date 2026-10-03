/* Les petits dessins du catalogue : bouteilles, feuille de vigne, cep, astres, paysage de
   coteaux. Dessinés ici en SVG, au trait encre sur des aplats de la palette des sols ; aucune
   bibliothèque. Génératifs à graine fixe : une même entrée donne toujours le même dessin.
   Loi Évin : des bouteilles, des vignes, des ciels ; jamais de verre levé, jamais de grappe
   clipart. */

export const C = {
  tuffeau: '#F2EADA', craie: '#FBF8F1', silex: '#46606E', gneiss: '#A8515F',
  amphibolite: '#3C5B47', sables: '#D08C3C', violet: '#67067C', or: '#E1C853', encre: '#2A3942',
};

/** Un générateur pseudo-aléatoire à graine fixe (mulberry32). */
export function graine(n) {
  let a = n >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const T = 'stroke="#2A3942" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"';

/* ——— bouteilles : un profil par forme, dans une boîte de 40 × 120 ——— */
const PROFILS = {
  // bordelaise : épaules franches
  bordelaise: 'M16 2 H24 V30 C24 36 33 37 33 46 V112 Q33 117 28 117 H12 Q7 117 7 112 V46 C7 37 16 36 16 30 Z',
  // bourguignonne : épaules tombantes
  bourguignonne: 'M16.5 2 H23.5 V24 C24 40 34 44 34 60 V112 Q34 117 29 117 H11 Q6 117 6 112 V60 C6 44 16 40 16.5 24 Z',
  // flûte d'Alsace : haute et fine
  flute: 'M17 2 H23 V30 C23.5 50 30 52 30 66 V113 Q30 117 26 117 H14 Q10 117 10 113 V66 C10 52 16.5 50 17 30 Z',
  // champenoise : large, épaules rondes
  champenoise: 'M15.5 4 H24.5 V26 C25 40 35.5 44 35.5 62 V112 Q35.5 117 30 117 H10 Q4.5 117 4.5 112 V62 C4.5 44 15 40 15.5 26 Z',
};
const ETIQUETTE = { bordelaise: [60, 34], bourguignonne: [66, 30], flute: [72, 26], champenoise: [68, 30] };

/** Une bouteille dessinée. `vin` : couleur du verre ; `capsule` : couleur du col. */
export function bouteille(forme = 'bordelaise', { vin = C.amphibolite, capsule = C.gneiss, etiquette = C.craie,
  largeur = null, hauteur = null, classe = 'dessin' } = {}) {
  const [y, h] = ETIQUETTE[forme];
  const w = forme === 'flute' ? 16 : forme === 'champenoise' ? 26 : 22;
  const capH = forme === 'champenoise' ? 22 : 14;
  return `<svg viewBox="0 0 40 120" class="${classe}" ${largeur ? `width="${largeur}"` : ''} ${hauteur ? `height="${hauteur}"` : ''} aria-hidden="true">
    <path d="${PROFILS[forme]}" fill="${vin}" ${T}/>
    <rect x="${20 - (forme === 'champenoise' ? 5 : 4)}" y="${forme === 'champenoise' ? 3 : 1.5}" width="${forme === 'champenoise' ? 10 : 8}" height="${capH}" rx="1.2" fill="${capsule}" ${T}/>
    <rect x="${20 - w / 2}" y="${y}" width="${w}" height="${h * 0.62}" rx="1.5" fill="${etiquette}" ${T}/>
    <path d="M${20 - w / 2 + 3} ${y + h * 0.24} H${20 + w / 2 - 3} M${20 - w / 2 + 5} ${y + h * 0.4} H${20 + w / 2 - 5}" ${T} stroke-width=".8" fill="none"/>
    <path d="M${forme === 'flute' ? 12.5 : 9.5} ${forme === 'flute' ? 72 : 66} V108" stroke="rgba(255,255,255,.45)" stroke-width="1.6" stroke-linecap="round"/>
  </svg>`;
}

/** Une feuille de vigne, cinq lobes. */
export function feuille({ couleur = C.amphibolite, classe = 'dessin', rotation = 0 } = {}) {
  return `<svg viewBox="0 0 60 60" class="${classe}" aria-hidden="true"><g transform="rotate(${rotation} 30 30)">
    <path d="M30 56 C29 50 28 46 27 44 C20 47 11 46 6 40 C11 37 14 35 15 32 C9 30 4 24 4 17 C11 18 16 20 19 23
      C18 15 20 8 26 3 C29 9 30 14 30 19 C31 13 34 8 40 4 C42 11 41 17 40 22 C44 19 50 17 56 18 C55 25 50 30 44 32
      C46 35 50 37 54 40 C49 46 40 47 33 44 C32 46 31 50 30 56 Z" fill="${couleur}" ${T}/>
    <path d="M30 54 V20 M30 40 L14 30 M30 40 L46 30 M30 30 L19 21 M30 30 L41 21" ${T} stroke-width=".9" fill="none" opacity=".7"/>
  </g></svg>`;
}

/** Les astres : la lune (Chant de Lune) et le soleil (Chant de Lumière). */
export function lune({ couleur = C.or, classe = 'dessin' } = {}) {
  return `<svg viewBox="0 0 40 40" class="${classe}" aria-hidden="true">
    <path d="M26 5 A15 15 0 1 0 35 27 A12 12 0 1 1 26 5 Z" fill="${couleur}" ${T}/></svg>`;
}
export function soleil({ couleur = C.or, classe = 'dessin' } = {}) {
  const r = [...Array(12)].map((_, i) => {
    const a = (i * Math.PI) / 6;
    return `M${20 + 12 * Math.cos(a)} ${20 + 12 * Math.sin(a)} L${20 + 17 * Math.cos(a)} ${20 + 17 * Math.sin(a)}`;
  }).join(' ');
  return `<svg viewBox="0 0 40 40" class="${classe}" aria-hidden="true">
    <circle cx="20" cy="20" r="8.5" fill="${couleur}" ${T}/><path d="${r}" ${T} fill="none"/></svg>`;
}

/** Un cep de vigne, tronc noueux, deux bras, quelques feuilles. `racines` : il plonge sous terre. */
export function cep({ racines = 0, classe = 'dessin', couleurFeuille = C.amphibolite } = {}) {
  const h = 120 + racines;
  const rac = racines ? `<path d="M30 118 C28 ${118 + racines * 0.3} 20 ${118 + racines * 0.5} 14 ${118 + racines * 0.9}
      M31 118 C33 ${118 + racines * 0.4} 34 ${118 + racines * 0.7} 33 ${118 + racines}
      M32 118 C38 ${118 + racines * 0.25} 46 ${118 + racines * 0.55} 52 ${118 + racines * 0.8}
      M29 ${118 + racines * 0.35} C24 ${118 + racines * 0.45} 22 ${118 + racines * 0.55} 18 ${118 + racines * 0.6}"
      stroke="#2A3942" stroke-width="1.5" stroke-linecap="round" fill="none"/>` : '';
  const f = (x, y, r, c) => `<g transform="translate(${x} ${y}) scale(.42) rotate(${r})">${feuilleBrute(c)}</g>`;
  return `<svg viewBox="0 0 64 ${h}" class="${classe}" aria-hidden="true">${rac}
    <path d="M29 118 C27 100 33 92 30 76 C28 66 32 60 31 52 C24 44 14 46 9 38 M31 52 C38 44 50 46 55 36"
      stroke="#5A4636" stroke-width="5" stroke-linecap="round" fill="none"/>
    <path d="M29 118 C27 100 33 92 30 76 C28 66 32 60 31 52 C24 44 14 46 9 38 M31 52 C38 44 50 46 55 36"
      ${T} fill="none" stroke-width="1"/>
    ${f(-4, 16, -20, couleurFeuille)}${f(12, 6, 10, C.amphibolite)}${f(34, 10, 25, couleurFeuille)}${f(42, 22, -10, C.amphibolite)}
  </svg>`;
}
function feuilleBrute(c) {
  return `<path d="M30 56 C29 50 28 46 27 44 C20 47 11 46 6 40 C11 37 14 35 15 32 C9 30 4 24 4 17 C11 18 16 20 19 23
      C18 15 20 8 26 3 C29 9 30 14 30 19 C31 13 34 8 40 4 C42 11 41 17 40 22 C44 19 50 17 56 18 C55 25 50 30 44 32
      C46 35 50 37 54 40 C49 46 40 47 33 44 C32 46 31 50 30 56 Z" fill="${c}" stroke="#2A3942" stroke-width="2.6" stroke-linejoin="round"/>`;
}

/** Un paysage de coteaux plantés de vigne : collines en aplats, rangs en pointillés, quelques
    arbres, un astre. `palette` : couleurs des collines du fond vers l'avant. */
export function paysage({ graineN = 7, largeur = 600, hauteur = 220, palette = [C.silex, C.amphibolite, C.sables, C.gneiss],
  astre = 'soleil', classe = 'dessin paysage', ciel = null } = {}) {
  const r = graine(graineN);
  const n = palette.length;
  let out = ciel ? `<rect width="${largeur}" height="${hauteur}" fill="${ciel}"/>` : '';
  if (astre === 'soleil') {
    out += `<circle cx="${largeur * 0.78}" cy="${hauteur * 0.24}" r="${hauteur * 0.09}" fill="${C.or}" ${T}/>`;
  } else if (astre === 'lune') {
    const x = largeur * 0.8, y = hauteur * 0.22, R = hauteur * 0.08;
    out += `<path d="M${x} ${y - R} A${R} ${R} 0 1 0 ${x + R * 0.95} ${y + R * 0.45} A${R * 0.8} ${R * 0.8} 0 1 1 ${x} ${y - R} Z" fill="${C.or}" ${T}/>`;
  }
  for (let k = 0; k < n; k++) {
    const base = hauteur * (0.36 + (k * 0.6) / n);
    const amp = hauteur * (0.12 - k * 0.015);
    const ph = r() * 6.28, fr = 1.2 + r() * 1.4;
    const pts = [];
    for (let i = 0; i <= 24; i++) {
      const x = (i / 24) * (largeur + 40) - 20;
      pts.push([x, base - amp * Math.sin(ph + (fr * i) / 6) * (0.6 + 0.4 * Math.sin(i / 3 + k))]);
    }
    const d = `M${pts.map((p) => p.map((v) => v.toFixed(1)).join(' ')).join(' L')} L${largeur + 20} ${hauteur + 5} L-20 ${hauteur + 5} Z`;
    out += `<path d="${d}" fill="${palette[k]}" ${T}/>`;
    // les rangs de vigne : des pointillés qui suivent la pente
    const rangs = 3 + k * 2;
    for (let j = 1; j <= rangs; j++) {
      const dy = (j / (rangs + 1)) * (hauteur - base + amp) * 0.8 + 4;
      const rang = pts.map((p) => `${p[0].toFixed(1)} ${(p[1] + dy).toFixed(1)}`).join(' L');
      out += `<path d="M${rang}" stroke="rgba(42,57,66,.55)" stroke-width="${1.2 + k * 0.5}" stroke-dasharray="${1 + k} ${3 + k * 1.5}" stroke-linecap="round" fill="none"/>`;
    }
    // quelques arbres ronds sur la crête du fond
    if (k < 2) {
      for (let t = 0; t < 3; t++) {
        const i = 2 + Math.floor(r() * 20), [x, y] = pts[i];
        out += `<path d="M${x} ${y} V${y - 9}" ${T}/><circle cx="${x}" cy="${y - 13}" r="${5 + r() * 3}" fill="${C.amphibolite}" ${T}/>`;
      }
    }
  }
  return `<svg viewBox="0 0 ${largeur} ${hauteur}" preserveAspectRatio="xMidYMax slice" class="${classe}" aria-hidden="true">${out}</svg>`;
}

/** Une rangée de bouteilles posées, formes et couleurs variées (pour une couverture, une fin). */
export function rangeeBouteilles({ classe = 'dessin', formes = ['bordelaise', 'flute', 'champenoise', 'bourguignonne'],
  vins = [C.amphibolite, C.or, C.silex, C.gneiss] } = {}) {
  return formes.map((f, i) => bouteille(f, { vin: vins[i % vins.length], capsule: [C.gneiss, C.violet, C.or, C.amphibolite][i % 4], classe })).join('');
}
