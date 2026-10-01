/* Les gabarits de page du catalogue « Sous nos pieds ». */
import {
  catalogue, REGIONS, STRATES, esc, euros, coupe, carotte, carotteRonde, defsTrames, graine,
  picto, famille, famillesDe, nbReferences, legendeHtml, tableauHtml, groupes, groupeDe,
  NOM_FAMILLE, effectifs,
} from './pieces.mjs';

const AG = catalogue.agence;
const SANITAIRE = AG.message_sanitaire;

/* ——————————————————————————————————————————————— enveloppe ——— */

export function page({ corps, region = null, folio = null, classe = '', sanitaire = true }) {
  return { region, folio, classe, corps, sanitaire };
}

export function rendrePage(p, numero) {
  const verso = numero % 2 === 0;
  const cls = ['page', verso ? 'verso' : 'recto', p.classe].filter(Boolean).join(' ');
  const bande = p.region
    ? `<div class="carotte">${carotte(p.region)}</div><div class="carotte-nom">${esc(p.region)}</div>`
    : '';
  const folio = p.folio === false ? '' : `<div class="folio">${numero}</div>`;
  const san = p.sanitaire ? `<div class="sanitaire">${esc(SANITAIRE)}</div>` : '';
  return `<section class="${cls}" id="p${numero}" data-page="${numero}">${bande}${p.corps}${folio}${san}</section>`;
}

export function document({ pages, ecran }) {
  const corps = pages.map((p, i) => rendrePage(p, i + 1)).join('\n');
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8">
<title>Agence SCIO — Sous nos pieds — Tarifs cavistes Vendée (85) 2026</title>
<link rel="stylesheet" href="../src/styles/systeme.css">
<link rel="stylesheet" href="../src/styles/pages.css">
<style>:root { --fond-perdu: ${ecran ? '0mm' : '3mm'}; }
@page { size: ${ecran ? '210mm 260mm' : '216mm 266mm'}; margin: 0; }
.page { ${ecran ? '' : 'margin: 3mm; box-shadow: 0 0 0 .2mm rgba(0,0,0,.25);'} }
${ecran ? '' : '.traits-coupe { display: block; }'}
</style></head><body class="${ecran ? 'ecran' : 'imprimeur'}">
${defsTrames()}
${corps}
</body></html>`;
}

/* ——————————————————————————————————————————————— couverture ——— */

export function couverture() {
  return page({
    classe: 'couverture', folio: false, sanitaire: false,
    corps: `
      <img class="logo-couv" src="../src/images/logo-agence-scio-detoure.png"
           alt="Agence SCIO Vins &amp; Spirits">
      <h1 class="titre-couv">Sous<br>nos<br><em>pieds</em></h1>
      <p class="sous-couv">Quarante domaines, dix régions,<br>et la terre qu'ils ont sous les pieds.</p>
      ${coupe({ largeur: 600, hauteur: 430 })}
      <div class="pied-couv">
        <span class="cible">${esc(AG.cible)}</span>
        <span class="annee">${esc(AG.edition)}</span>
      </div>
      <div class="sanitaire sanitaire-couv">${esc(SANITAIRE)}</div>`,
  });
}

/* ——————————————————————————————————————————————— l'agence ——— */

export function pageAgence() {
  const c = AG.contacts;
  return page({
    classe: 'agence',
    corps: `<div class="cadre">
      <img class="logo-agence" src="../src/images/logo-agence-scio-detoure.png"
           alt="Agence SCIO Vins &amp; Spirits">
      <p class="credo">L'Agence SCIO, c'est <strong>partager notre savoir et notre passion</strong>
        en vous proposant des vignerons de tous horizons, avant-gardistes et respectueux de la nature.
        Découvrez notre sélection. Laissez-vous guider et conseiller.</p>
      <div class="contacts">
        <div class="contact"><span class="prenom">Laurent</span>
          <a href="tel:+33680880755" class="tel">${esc(c.laurent)}</a></div>
        <div class="contact"><span class="prenom">Carline</span>
          <a href="tel:+33649191675" class="tel">${esc(c.carline)}</a></div>
      </div>
      <div class="coordonnees">
        <p>${esc(c.adresse)}</p>
        <p><a href="mailto:${esc(c.email)}">${esc(c.email)}</a></p>
        <p><a href="https://${esc(c.site)}">${esc(c.site)}</a></p>
      </div>
      <div class="chiffres">
        <div><strong>40</strong> domaines</div>
        <div><strong>10</strong> régions</div>
        <div><strong>${catalogue.domaines.reduce((n, d) => n + nbReferences(d), 0)}</strong> références</div>
      </div>
    </div>`,
  });
}

/* ——————————————————————————————————— comment lire ce catalogue ——— */

export function modeEmploi() {
  const toutes = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux'];
  return page({
    classe: 'mode-emploi',
    corps: `<div class="cadre">
      <h2 class="titre-section">Comment lire ce catalogue</h2>
      <div class="me-grille">
        <div class="me-item"><div class="me-fig me-fig-tranche">${coupe({ largeur: 60, hauteur: 300, graineN: 3, etiquettes: false })}
            <span class="me-doigt">Dix bandes sur la tranche, une par région. Celle où vous êtes
              est pleine et marquée d'or.</span></div>
          <h3>La tranche vous emmène</h3>
          <p>Dix régions, dix strates. Sur le bord de chaque page, la strate de la région où vous
            êtes est pleine et marquée d'or. Catalogue fermé, la tranche affiche les dix bandes :
            vous ouvrez directement à la bonne région.</p></div>
        <div class="me-item"><div class="me-fig me-fig-prix">
            <div class="demo-bloc"><span>jusqu'à&nbsp;36</span><span>dès&nbsp;48</span><span>dès&nbsp;120</span></div>
            <div class="demo-bloc demo-prix"><span>14,75&nbsp;€</span><span>13,25&nbsp;€</span><span>12,25&nbsp;€</span></div>
          </div>
          <h3>Le prix tombe toujours au même endroit</h3>
          <p>Le bloc de prix a la même largeur sur les quarante fiches, divisé en autant de parts
            qu'il y a de paliers. Les paliers, eux, sont ceux de chaque domaine : nous ne les avons
            pas harmonisés. Un domaine à tarif unique n'a qu'une part.</p></div>
        <div class="me-item"><div class="me-fig me-fig-pictos">
            ${toutes.map((f) => picto(f, 'picto gros')).join('')}</div>
          <h3>Les pictos sont les nôtres</h3>
          <p>Une forme par type : bulles, blanc, rosé, rouge, doux, sans alcool, jus de cépages,
            bière, spiritueux. Ce sont <strong>nos</strong> pictos, dessinés pour ce catalogue :
            ce ne sont pas les logos officiels des organismes certificateurs.</p>
          <div class="me-legende">${toutes.map((f) =>
            `<span>${picto(f)} ${esc(NOM_FAMILLE[f])}</span>`).join('')}</div></div>
        <div class="me-item"><div class="me-fig me-fig-jetons">
            <span class="jeton bio">Bio</span><span class="jeton alloc">Allocation</span>
            <span class="jeton panachage">Panachage</span><span class="jeton consulter">Consultez-nous</span></div>
          <h3>Les mentions</h3>
          <p><strong>Allocation</strong> : quantités limitées, à réserver. <strong>Panachage</strong> :
            vous pouvez mélanger à l'intérieur du domaine, et parfois entre plusieurs domaines —
            les quatre alliances sont page 7. <strong>Consultez-nous</strong> : le domaine
            communique ses tarifs et ses offres au cas par cas.</p></div>
        <div class="me-item"><div class="me-fig me-fig-paliers">
            <span>jusqu'à 36 bts</span><span>à partir de 198 bts</span><span>Palette</span>
            <span>120 cols</span><span>50 BIB demi pal</span><span>Plus de 300 bts</span>
            <span>Tarif unique</span></div>
          <h3>Les paliers sont ceux du domaine</h3>
          <p>Treize notations différentes dans cette sélection, toutes recopiées telles quelles :
            bouteilles, cols, bag-in-box, demi-palette, palette, ou tarif unique.
            <strong>Nous n'avons harmonisé aucun seuil</strong> — une quantité approximative
            serait une erreur de commande.</p></div>
        <div class="me-item"><div class="me-fig me-fig-pied">
            <span class="demo-note">* Prix de la bouteille H.T. franco de port.</span>
            <span class="demo-dep"><strong>Distribution</strong> 35 · 44 · 49 · 53 · 56 · 85</span></div>
          <h3>Le bas de page dit le reste</h3>
          <p>À gauche, les conditions exactes du domaine : hors transport, franco de port,
            départ chai, départ cave, ou franco à partir d'une quantité. À droite, les
            départements où ce domaine est distribué. Les deux changent d'une fiche à l'autre.</p></div>
      </div>
      <p class="me-pied">Tous les prix sont <strong>hors taxes, par bouteille</strong>. Les conditions
        de port diffèrent d'un domaine à l'autre : elles sont écrites en bas de chaque fiche, avec
        les départements de distribution.</p>
    </div>`,
  });
}

/* ——————————————————————————————————————————— l'entrée visuelle ——— */

export function sommaire(pagesParDomaine) {
  const eff = effectifs();
  const bandes = REGIONS.map((nom, i) => {
    const doms = catalogue.domaines.filter((d) => d.region === nom);
    const s = STRATES[nom];
    const clair = nom === 'Champagne';
    return `<div class="som-strate ${clair ? 'claire' : ''} ${doms.length >= 5 ? 'dense' : ''}"
      style="--strate:${s.hex}; flex-grow:${Math.max(eff[i], 2.6)}">
      <div class="som-trame trame trame-${s.t}"></div>
      <div class="som-tete"><span class="som-nom">${esc(nom)}</span>
        <span class="som-mot">${esc(s.mot)}</span>
        <span class="som-nb">${eff[i]}</span></div>
      <ul class="som-liste">${doms.map((d) =>
        `<li><a href="#p${pagesParDomaine.get(d.numero)}"><span class="n">${d.numero}</span>
          <span class="nom">${esc(d.nom)}</span>
          <span class="pg">${pagesParDomaine.get(d.numero)}</span></a></li>`).join('')}</ul>
    </div>`;
  });
  return [page({
    classe: 'sommaire',
    corps: `<div class="cadre">
      <h2 class="titre-section">La coupe<span>sommaire des dix régions</span></h2>
      <div class="som-colonne">${bandes.join('')}</div>
    </div>`,
  })];
}

/* ——————————————————————————————————————————— les alliances ——— */

export function alliances(pagesParDomaine) {
  const bloc = (g) => {
    const doms = g.domaines.map((n) => catalogue.domaines.find((d) => d.numero === n));
    return `<div class="all-bloc">
      <h3>${esc(g.libelle)}</h3>
      <div class="all-doms">${doms.map((d) => `<a class="all-dom" href="#p${pagesParDomaine.get(d.numero)}">
        <span class="n">${d.numero}</span><span class="nom">${esc(d.nom)}</span>
        <span class="reg">${esc(d.region)}</span><span class="pg">p.&nbsp;${pagesParDomaine.get(d.numero)}</span>
      </a>`).join('')}</div>
      <p class="all-mention">${esc(doms[0].mentions.find((m) => m.toLowerCase().includes('panacher')) || '')}</p>
    </div>`;
  };
  return [page({
    classe: 'alliances',
    corps: `<div class="cadre">
      <h2 class="titre-section">Les quatre alliances<span>ce que l'on peut mélanger entre domaines</span></h2>
      <p class="all-intro">Partout ailleurs, « Possibilité de panacher » vaut <strong>à l'intérieur
        d'un domaine</strong>. Ces quatre groupes-là se panachent <strong>entre eux</strong> :
        une commande peut mélanger leurs vins pour atteindre un palier.</p>
      ${groupes.map(bloc).join('')}
      <p class="all-pied">Les paliers restent ceux de chaque domaine : le panachage permet
        d'atteindre la quantité, il ne change pas le tarif de la bouteille.</p></div>`,
  })];
}

/* ——————————————————————————————————————— ouverture de région ——— */

export function ouvertureRegion(nom, pagesParDomaine) {
  const doms = catalogue.domaines.filter((d) => d.region === nom);
  const s = STRATES[nom];
  const refs = doms.reduce((n, d) => n + nbReferences(d), 0);
  const parType = {};
  doms.forEach((d) => d.tableaux.forEach((t) => t.lignes.forEach((l) => {
    const f = famille(l, t); parType[f] = (parType[f] || 0) + 1;
  })));
  const ordre = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux', 'autre'];
  const types = ordre.filter((f) => parType[f]).map((f) =>
    `<span>${picto(f)} <b>${parType[f]}</b> ${esc(NOM_FAMILLE[f].toLowerCase())}</span>`).join('');
  return page({
    region: nom, classe: `ouverture ${nom === 'Champagne' ? 'claire' : ''}`,
    corps: `
      <div class="ouv-fond" style="--strate:${s.hex}">
        <div class="ouv-trame trame trame-${s.t}"></div>
      </div>
      <div class="ouv-carotte">${solRegion(nom, REGIONS.indexOf(nom) + 1)}</div>
      <div class="cadre">
        <div class="ouv-haut"><span class="ouv-rang">${REGIONS.indexOf(nom) + 1} / 10</span></div>
        <h2 class="ouv-nom">${esc(nom)}</h2>
        <p class="ouv-mot">${esc(s.mot)}</p>
        <div class="ouv-chiffres">
          <span><strong>${doms.length}</strong> domaine${doms.length > 1 ? 's' : ''}</span>
          <span><strong>${refs}</strong> références</span>
        </div>
        <div class="ouv-types">${types}</div>
        <ul class="ouv-liste">${doms.map((d) =>
          `<li><a href="#p${pagesParDomaine.get(d.numero)}"><span class="n">${d.numero}</span>
            <span class="nom">${esc(d.nom)}</span><span class="pg">${pagesParDomaine.get(d.numero)}</span></a></li>`).join('')}</ul>
      </div>`,
  });
}

/* ——————————————————————————————————————————— fiche domaine ——— */

export function enteteDomaine(d, suite = false) {
  const g = groupeDe(d);
  const consulter = d.mentions.find((m) => m.toLowerCase().includes('consultez-nous'));
  const jetons = [
    ...d.labels.map((l) => `<span class="jeton bio">${esc(l.label)}</span>`),
    d.allocation ? '<span class="jeton alloc">Allocation</span>' : '',
    g ? `<span class="jeton panachage">Panachage entre domaines</span>`
      : `<span class="jeton panachage">Panachage dans le domaine</span>`,
    consulter ? '<span class="jeton consulter">Consultez-nous</span>' : '',
    `<span class="jeton">${nbReferences(d)} références</span>`,
  ].filter(Boolean).join('');
  return `<div class="entete-dom">
      <div class="num">${d.numero}</div>
      <h1>${esc(d.nom)}${suite ? ' <span class="suite">(suite)</span>' : ''}</h1>
      <div class="region">${esc(d.region)}</div>
    </div>
    <div class="jetons">${jetons}</div>`;
}

export function hautDomaine(d) {
  const t = esc(d.texte_source);
  const texte = t
    ? `<div class="texte-dom"><span class="lettrine">${t.slice(0, 1)}</span>${t.slice(1)}</div>`
    : `<div class="texte-dom sans-texte">Le tarif de l'Agence SCIO ne donne pas de présentation
         pour ce domaine. Nous n'en inventons pas.</div>`;
  return `<div class="haut-dom">${carotteRonde(d)}${texte}</div>`;
}

/** Quand une fiche courte laisse un vide, on y pose le sol de sa région, en coupe. */
export function respireSol(d, hauteurMm) {
  const s = STRATES[d.region];
  return `<div class="respire" style="height:${hauteurMm.toFixed(1)}mm">
    <div class="legende-sol">${esc(d.region)} — ${esc(s.mot)}</div>
    <div class="respire-sol">${solRegion(d.region, d.numero)}</div></div>`;
}

/** Le sol d'une région : quatre couches dans sa palette, tirées d'une graine fixe. */
export function solRegion(region, graineN) {
  const r = graine(graineN * 17 + 3);
  const s = STRATES[region];
  const palette = [s.hex, '#D08C3C', '#46606E', '#A8515F', '#3C5B47']
    .filter((c, i, a) => a.indexOf(c) === i).slice(0, 4);
  let y = 0, out = '';
  palette.forEach((col, i) => {
    const h = 100 / palette.length + (r() - 0.5) * 8;
    const pts = [];
    for (let x = 0; x <= 620; x += 100) pts.push(`${x} ${(y + (r() - 0.5) * 6).toFixed(1)}`);
    const d = `M-20 ${y.toFixed(1)} ${pts.map((q) => 'L' + q).join(' ')} L620 ${y.toFixed(1)}
               L620 ${(y + h + 2).toFixed(1)} L-20 ${(y + h + 2).toFixed(1)} Z`;
    out += `<path d="${d}" fill="${col}" opacity="${(0.82 + i * 0.05).toFixed(2)}"/>`;
    y += h;
  });
  return `<svg viewBox="0 0 600 100" preserveAspectRatio="none" aria-hidden="true">${out}</svg>
    <div class="trame trame-${s.t}" style="opacity:.45"></div>`;
}

export function piedDomaine(d, pagesParDomaine) {
  const g = groupeDe(d);
  const alliance = g
    ? `<div class="alliance"><strong>Se panache avec</strong> <em>${esc(g.libelle)}</em> —
        ${g.domaines.filter((n) => n !== d.numero).map((n) =>
          `n°${n} p.&nbsp;${pagesParDomaine.get(n)}`).join(' · ')}</div>`
    : '';
  const note = d.note_prix
    ? esc(d.note_prix)
    : 'Conditions de port non précisées par le domaine — nous consulter.';
  const dep = d.departements.length
    ? d.departements.join(' · ')
    : 'non précisés par le domaine — nous consulter';
  return `${alliance}
    <div class="pied-dom"><div>${note}</div>
      <div><strong>Distribution</strong> ${dep}</div></div>
    ${legendeHtml(famillesDe(d))}`;
}

/* ——————————————————————————————————————————————— index ——— */

const ORDRE_FAMILLES = ['bulles', 'blanc', 'rose', 'rouge', 'doux', 'sansalcool', 'jus', 'biere', 'spiritueux', 'autre'];

/** Toutes les références, rangées par type de vin. */
export function entreesIndex(pagesParDomaine) {
  const par = {};
  catalogue.domaines.forEach((d) => {
    // Une cuvée partagée par plusieurs lignes du même domaine n'identifie rien :
    // on bascule alors sur l'appellation, puis sur la contenance ou le millésime.
    const toutes = d.tableaux.flatMap((t) => t.lignes.map((l) => ({ l, t })));
    const compte = (cle) => toutes.filter(({ l }) => (l[cle] || '') === '').length;
    const occurrences = {};
    toutes.forEach(({ l }) => {
      const c = l.cuvee || l.appellation;
      occurrences[c] = (occurrences[c] || 0) + 1;
    });
    toutes.forEach(({ l, t }) => {
      const cuv = l.cuvee || l.appellation;
      let nom = cuv, prec = null;
      if (l.cuvee && occurrences[cuv] > 1) {
        const appsDifferentes = toutes.filter(({ l: x }) => (x.cuvee || x.appellation) === cuv)
          .map(({ l: x }) => x.appellation);
        if (new Set(appsDifferentes).size > 1) nom = l.appellation;
        else prec = l.contenance || l.millesime || null;
      } else if (!l.cuvee && occurrences[cuv] > 1) {
        prec = l.contenance || l.millesime || null;
      }
      (par[famille(l, t)] ||= []).push({
        nom, prec, dom: d.numero, pg: pagesParDomaine.get(d.numero),
      });
    });
  });
  return ORDRE_FAMILLES.filter((f) => par[f]).map((f) => ({
    famille: f,
    entrees: par[f].sort((a, b) => a.nom.localeCompare(b.nom, 'fr')),
  }));
}

/** Les pages d'index : un flux en trois colonnes, coupé en autant de pages qu'il faut. */
export function pagesIndex(groupesIndex, parPage, poidsTitre = 3) {
  const blocs = [];
  groupesIndex.forEach((g) => {
    blocs.push({ type: 'titre', famille: g.famille, poids: poidsTitre });
    g.entrees.forEach((e) => blocs.push({ type: 'entree', e, famille: g.famille, poids: 1 }));
  });
  const pages = [];
  let i = 0, premiere = true;
  while (i < blocs.length) {
    let reste = parPage - (premiere ? 18 : 0);   // la première page porte le titre de section
    const bloc = [];
    while (i < blocs.length && reste - blocs[i].poids >= 0) {
      reste -= blocs[i].poids;
      bloc.push(blocs[i++]);
    }
    if (!bloc.length) bloc.push(blocs[i++]);
    const html = bloc.map((b) => b.type === 'titre'
      ? `<h3 class="idx-titre">${picto(b.famille)} ${esc(NOM_FAMILLE[b.famille])}</h3>`
      : `<a class="idx-ligne" href="#p${b.e.pg}"><span class="idx-nom">${esc(b.e.nom)}</span>
          ${b.e.prec ? `<span class="idx-prec">${esc(b.e.prec)}</span>` : ''}
          <span class="idx-dom">${b.e.dom}</span><span class="idx-pg">${b.e.pg}</span></a>`).join('');
    pages.push(page({
      classe: 'index',
      corps: `<div class="cadre">
        ${premiere ? `<h2 class="titre-section">Index des vins<span>par type, de A à Z</span></h2>
          <p class="idx-intro">Le numéro en violet est celui du domaine, le dernier chiffre est la page.</p>` : ''}
        <div class="idx-flux">${html}</div></div>`,
    }));
    premiere = false;
  }
  return pages;
}

/* ——————————————————————————————————————————— page finale ——— */

export function pageFinale(nbPhotos) {
  const c = AG.contacts;
  return page({
    classe: 'finale', sanitaire: false,
    corps: `<div class="cadre">
      <img class="logo-finale" src="../src/images/logo-agence-scio-detoure.png"
           alt="Agence SCIO Vins &amp; Spirits">
      <div class="fin-contacts">
        <div class="contact"><span class="prenom">Laurent</span>
          <a href="tel:+33680880755" class="tel">${esc(c.laurent)}</a></div>
        <div class="contact"><span class="prenom">Carline</span>
          <a href="tel:+33649191675" class="tel">${esc(c.carline)}</a></div>
      </div>
      <p class="fin-adresse">${esc(c.adresse)}<br>
        <a href="mailto:${esc(c.email)}">${esc(c.email)}</a> ·
        <a href="https://${esc(c.site)}">${esc(c.site)}</a></p>

      <div class="fin-cols">
        <div><h3>Lexique</h3>
          <dl class="lexique">${AG.lexique.map((l) =>
            `<dt>${esc(l.sigle)}</dt><dd>${esc(l.definition)}</dd>`).join('')}</dl>
        </div>
        <div><h3>Mentions légales</h3>
          <p class="fin-mentions">${esc(AG.mentions_legales)}</p>
        </div>
        <div><h3>Crédits</h3>
          <p class="fin-mentions">Conception, maquette et illustrations : Agence SCIO.
            Les pictogrammes de ce catalogue sont les nôtres ; ils ne reproduisent aucun logo
            officiel d'organisme certificateur.
            ${nbPhotos ? `Photographies : voir <em>credits.md</em>.`
              : `Ce catalogue ne contient aucune photographie : toutes les illustrations sont dessinées.`}</p>
        </div>
      </div>
      <p class="fin-sanitaire">${esc(SANITAIRE)}</p>
    </div>`,
  });
}

/* ——————————————————————————————————————————— page de respiration ——— */

export function respiration(region) {
  const s = STRATES[region];
  return page({
    region, classe: 'respiration',
    corps: `<div class="resp-fond" style="--strate:${s.hex}">
      <div class="ouv-trame trame trame-${s.t}"></div></div>
      <div class="cadre"><p class="resp-mot">${esc(s.mot)}</p></div>`,
  });
}
