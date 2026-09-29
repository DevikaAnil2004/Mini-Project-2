// Builds docs/CricketIQ_Review1.pptx — Review 1 deck at ~20% completion,
// matching the slide pattern of the reference Synapse deck (Synapse_Review1-Updated.pptx):
// title -> abstract -> tech stack -> system study -> architecture -> workflow ->
// database design -> table design -> use case -> UI (screenshots) -> completion status.
// Run: node docs/build_pptx.js

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const BASE = __dirname;
const DIAG = path.join(BASE, 'diagrams');
const SHOT = path.join(BASE, 'screenshots');
const OUT = path.join(BASE, 'CricketIQ_Review1.pptx');
const GITHUB_URL = 'https://github.com/arjuntp-397/Mini-Project-2';

// Palette — same "Floodlight" family used across the diagrams, so the deck
// and the project documentation read as one system.
const NAVY = '0F1E3D';
const NAVY2 = '1F2A44';
const INK = '1A1A1A';
const GREY = '5B6072';
const AMBER = 'F5A623';
const AMBER_DK = 'C8811A';
const CARD = 'F7F7FA';
const LINE = 'C7CBDB';
const WHITE = 'FFFFFF';

function img(name) { return path.join(DIAG, name); }
function shot(name) { return path.join(SHOT, name); }

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5 in
const PW = 13.33, PH = 7.5;

pres.defineSlideMaster({
  title: 'PLAIN',
  background: { color: WHITE },
});

function footer(slide, num) {
  slide.addText('CricketIQ — Review 1', {
    x: 0.4, y: PH - 0.42, w: 6, h: 0.3, fontSize: 9, color: GREY, fontFace: 'Calibri',
  });
  slide.addText(String(num), {
    x: PW - 0.9, y: PH - 0.42, w: 0.5, h: 0.3, fontSize: 9, color: GREY,
    align: 'right', fontFace: 'Calibri',
  });
}

function sectionHeading(slide, kicker, title) {
  slide.addText(kicker.toUpperCase(), {
    x: 0.55, y: 0.35, w: 8, h: 0.35, fontSize: 12, bold: true, color: AMBER_DK,
    fontFace: 'Calibri', charSpacing: 1,
  });
  slide.addText(title, {
    x: 0.55, y: 0.62, w: 12.2, h: 0.7, fontSize: 28, bold: true, color: NAVY,
    fontFace: 'Cambria',
  });
}

// ============================================================ 1. Title ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  s.background = { color: NAVY };
  s.addShape('rect', { x: 0, y: 0, w: PW, h: 0.09, fill: { color: AMBER } });

  s.addText('CRICKETIQ', {
    x: 0.9, y: 2.0, w: 11.5, h: 1.1, fontSize: 54, bold: true, color: WHITE, fontFace: 'Cambria',
    charSpacing: 1,
  });
  s.addText('IPL Analytics & Predictive Intelligence Platform', {
    x: 0.9, y: 3.05, w: 11, h: 0.6, fontSize: 20, color: 'CADCFC', fontFace: 'Calibri',
  });
  s.addShape('line', {
    x: 0.9, y: 3.75, w: 4.6, h: 0, line: { color: AMBER, width: 1.5 },
  });

  const people = [
    ['[Student Name 1]', 'Backend & Frontend'],
    ['[Student Name 2]', 'ML / Data'],
    ['[Student Name 3]', 'Integration & Deployment'],
  ];
  people.forEach(([name, role], i) => {
    const x = 0.9 + i * 3.9;
    s.addText(name, { x, y: 4.15, w: 3.6, h: 0.4, fontSize: 16, bold: true, color: WHITE, fontFace: 'Calibri' });
    s.addText(role, { x, y: 4.55, w: 3.6, h: 0.35, fontSize: 12.5, color: 'A9B4D0', fontFace: 'Calibri' });
  });

  s.addText('Team No: [XX]   |   Dept. of Computer Applications   |   Review 1   |   [Month Year]', {
    x: 0.9, y: 6.6, w: 11, h: 0.4, fontSize: 12.5, color: 'A9B4D0', fontFace: 'Calibri',
  });
}

// ========================================================= 2. Abstract ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Project Overview', 'Abstract');

  s.addText(
    'CricketIQ is a web analytics platform for the Indian Premier League. It unifies a full '
    + 'team / player / match database with a season analytics dashboard and four statistical '
    + 'intelligence tools behind one consistent interface.',
    { x: 0.55, y: 1.5, w: 12.2, h: 0.9, fontSize: 14, color: INK, fontFace: 'Calibri', valign: 'top' }
  );

  const colY = 2.55, colH = 2.15;
  s.addShape('roundRect', { x: 0.55, y: colY, w: 5.9, h: colH, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
  s.addText('For the Analyst', { x: 0.8, y: colY + 0.18, w: 5.4, h: 0.4, fontSize: 15, bold: true, color: NAVY2, fontFace: 'Calibri' });
  s.addText([
    { text: 'Browse the full team / player / match record\n', options: { bullet: true, breakLine: true } },
    { text: 'Season win trends & leaderboards\n', options: { bullet: true, breakLine: true } },
    { text: 'Win-probability, form forecast, XI suggestion, similarity', options: { bullet: true } },
  ], { x: 0.8, y: colY + 0.62, w: 5.4, h: colH - 0.75, fontSize: 12.5, color: INK, fontFace: 'Calibri', paraSpaceAfter: 6 });

  s.addShape('roundRect', { x: 6.65, y: colY, w: 6.15, h: colH, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
  s.addText('What Makes It Different', { x: 6.9, y: colY + 0.18, w: 5.6, h: 0.4, fontSize: 15, bold: true, color: NAVY2, fontFace: 'Calibri' });
  s.addText([
    { text: 'One design-token CSS layer, not per-page styling\n', options: { bullet: true, breakLine: true } },
    { text: 'ML models cached in-process, loaded once\n', options: { bullet: true, breakLine: true } },
    { text: 'Every list/API call has a defined empty & error state', options: { bullet: true } },
  ], { x: 6.9, y: colY + 0.62, w: 5.6, h: colH - 0.75, fontSize: 12.5, color: INK, fontFace: 'Calibri', paraSpaceAfter: 6 });

  s.addShape('roundRect', { x: 0.55, y: 4.9, w: 12.25, h: 0.85, rectRadius: 0.06, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText([
    { text: 'Current status: ', options: { bold: true, color: AMBER } },
    { text: '~20% complete — data model, seed data and the full UI/UX are built; ML endpoints run on placeholder models pending training on the full dataset (see Section 11).', options: { color: WHITE } },
  ], { x: 0.85, y: 4.9, w: 11.6, h: 0.85, fontSize: 12.5, fontFace: 'Calibri', valign: 'middle' });

  footer(s, 2);
}

// ================================================== 3. Technology Stack ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Implementation', 'Technology Stack');

  const rows = [
    ['Layer', 'Technology'],
    ['Web Frontend', 'Jinja2 templates, custom OKLCH design-token CSS, Bootstrap 5 grid, vanilla JavaScript'],
    ['Backend Framework', 'Flask (Python), Flask-SQLAlchemy, Flask-Migrate'],
    ['Database & ORM', 'SQLite (development) / MySQL (production target) via SQLAlchemy 2.0'],
    ['Matching & ML', 'scikit-learn (RandomForest / classifier), joblib for cached model persistence'],
    ['Charts', 'Chart.js, themed at runtime from the CSS token layer'],
    ['Icons', 'Inline SVG sprite (no icon web-font dependency)'],
    ['Auth & Security', 'None — the application is read-only with no accounts (by design, see Scope)'],
  ];

  const header = rows[0], body = rows.slice(1);
  const tRows = [];
  tRows.push(header.map((c) => ({
    text: c, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 13, fontFace: 'Calibri', valign: 'middle' },
  })));
  body.forEach((r, i) => {
    tRows.push(r.map((c, ci) => ({
      text: c,
      options: {
        color: INK, fontSize: 12, fontFace: ci === 0 ? 'Consolas' : 'Calibri',
        fill: { color: i % 2 === 0 ? WHITE : CARD }, valign: 'middle',
        bold: ci === 0,
      },
    })));
  });

  s.addTable(tRows, {
    x: 0.55, y: 1.55, w: 12.25, h: 4.9,
    colW: [3.0, 9.25],
    border: { type: 'solid', color: LINE, pt: 0.75 },
    autoPage: false,
  });

  footer(s, 3);
}

// ===================================================== 4. System Study ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Planning', 'System Study');

  const cols = [
    { title: 'Problem Statement', color: 'DC2626', items: [
      'Raw IPL stats sit in disconnected sources with no unified view.',
      'No single tool combines directory browsing with predictive analysis.',
      'Existing dashboards are either static tables or opaque black-box models.',
    ] },
    { title: 'Scope', color: '2563EB', items: [
      'Team, player & match directories with full detail pages.',
      'Season analytics: win trends, leaderboards.',
      'Win probability, form forecast, playing-XI, similarity search.',
      'No accounts / auth — public, read-only tool.',
    ] },
    { title: 'Solution Approach', color: '16A34A', items: [
      'Flask + SQLAlchemy relational schema, normalised to 3NF.',
      'One CSS design-token layer driving every page consistently.',
      'ML endpoints isolated behind a cached loader (lib/loaders.py).',
      'Iterative delivery: schema + UI first, model training next.',
    ] },
  ];

  cols.forEach((c, i) => {
    const x = 0.55 + i * 4.15;
    s.addShape('roundRect', { x, y: 1.5, w: 3.95, h: 5.1, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
    s.addShape('rect', { x, y: 1.5, w: 3.95, h: 0.5, fill: { color: c.color }, line: { color: c.color, width: 0 } });
    s.addText(c.title, { x: x + 0.2, y: 1.5, w: 3.55, h: 0.5, fontSize: 14.5, bold: true, color: WHITE, fontFace: 'Calibri', valign: 'middle' });
    s.addText(
      c.items.map((t) => ({ text: t, options: { bullet: { code: '2022' }, breakLine: true } })),
      { x: x + 0.22, y: 2.15, w: 3.55, h: 4.3, fontSize: 12, color: INK, fontFace: 'Calibri', paraSpaceAfter: 10, valign: 'top' }
    );
  });

  footer(s, 4);
}

// ================================================ 5. System Architecture ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Design', 'System Architecture');
  s.addText('Three-tier design: Browser — Flask API — Database', {
    x: 0.55, y: 1.32, w: 10, h: 0.35, fontSize: 13, italic: true, color: GREY, fontFace: 'Calibri',
  });
  s.addImage({ path: img('templates.png'), x: 2.43, y: 1.75, w: 8.47, h: 5.20 });
  footer(s, 5);
}

// =========================================== 6. Workflow / Process Flow ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Design', 'Prediction Workflow');
  s.addText('End-to-end process flow for the match win-prediction use case', {
    x: 0.55, y: 1.32, w: 10, h: 0.35, fontSize: 13, italic: true, color: GREY, fontFace: 'Calibri',
  });
  s.addImage({ path: img('workflow.png'), x: 1.15, y: 1.85, w: 11.0, h: 11.0 * (640 / 1400) });
  footer(s, 6);
}

// ================================================== 7. Database Design ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Data Model', 'Database Design');
  s.addText('Condensed class diagram — Team is the hub, referenced by Player and Match', {
    x: 0.55, y: 1.32, w: 11, h: 0.35, fontSize: 13, italic: true, color: GREY, fontFace: 'Calibri',
  });
  s.addImage({ path: img('classdiagram.png'), x: 2.27, y: 1.8, w: 8.79, h: 5.15 });
  footer(s, 7);
}

// ====================================================== 8. Table Design ===
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Data Model', 'Table Design');
  s.addImage({ path: img('tabledesign.png'), x: 2.02, y: 1.35, w: 9.30, h: 5.60 });
  footer(s, 8);
}

// ==================================================== 9. Use Case Diagram ==
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Requirements', 'Use Case Diagram');
  s.addImage({ path: img('usecase.png'), x: 3.14, y: 1.35, w: 7.05, h: 5.60 });
  footer(s, 9);
}

// ============================================================ 10. UI ======
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Implementation', 'UI — Overview & Directory');
  s.addShape('roundRect', { x: 0.55, y: 1.45, w: 6.0, h: 5.35, rectRadius: 0.05, fill: { color: NAVY }, line: { color: LINE, width: 0.75 } });
  s.addImage({ path: shot('home.png'), x: 0.65, y: 1.55, w: 5.8, h: 5.15, sizing: { type: 'crop', w: 5.8, h: 5.15 } });

  s.addShape('roundRect', { x: 6.75, y: 1.45, w: 6.0, h: 5.35, rectRadius: 0.05, fill: { color: NAVY }, line: { color: LINE, width: 0.75 } });
  s.addImage({ path: shot('teams.png'), x: 6.85, y: 1.55, w: 5.8, h: 5.15, sizing: { type: 'crop', w: 5.8, h: 5.15 } });
  footer(s, 10);
}

{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Implementation', 'UI — Intelligence Tools');
  s.addShape('roundRect', { x: 2.65, y: 1.45, w: 8.0, h: 5.35, rectRadius: 0.05, fill: { color: NAVY }, line: { color: LINE, width: 0.75 } });
  s.addImage({ path: shot('predictions.png'), x: 2.75, y: 1.55, w: 7.8, h: 5.15, sizing: { type: 'crop', w: 7.8, h: 5.15 } });
  footer(s, 11);
}

// ============================================ 12. Completion Status =======
{
  const s = pres.addSlide({ masterName: 'PLAIN' });
  sectionHeading(s, 'Review 1', 'Project Completion Status');

  s.addShape('roundRect', { x: 9.3, y: 0.42, w: 3.5, h: 0.9, rectRadius: 0.45, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText('~20%', { x: 9.3, y: 0.46, w: 3.5, h: 0.5, fontSize: 22, bold: true, color: AMBER, align: 'center', fontFace: 'Cambria' });
  s.addText('COMPLETE', { x: 9.3, y: 0.92, w: 3.5, h: 0.3, fontSize: 10, color: 'CADCFC', align: 'center', fontFace: 'Calibri', charSpacing: 1 });

  const doneX = 0.55, planX = 6.75, colW = 6.0, colY = 1.55;
  s.addShape('rect', { x: doneX, y: colY, w: colW, h: 0.42, fill: { color: '16A34A' }, line: { color: '16A34A', width: 0 } });
  s.addText('DONE — Demo-Ready', { x: doneX + 0.15, y: colY, w: colW - 0.3, h: 0.42, fontSize: 13.5, bold: true, color: WHITE, fontFace: 'Calibri', valign: 'middle' });

  s.addShape('rect', { x: planX, y: colY, w: colW, h: 0.42, fill: { color: 'F59E0B' }, line: { color: 'F59E0B', width: 0 } });
  s.addText('PLANNED — In Development', { x: planX + 0.15, y: colY, w: colW - 0.3, h: 0.42, fontSize: 13.5, bold: true, color: WHITE, fontFace: 'Calibri', valign: 'middle' });

  const done = [
    'Normalised schema — 6 tables, seeded with 8 teams, 88 players',
    'Full directory UI — teams, players, matches, detail pages',
    'Analytics dashboard — win-trend and leaderboard charts',
    'Design system shipped — dark/light themes, responsive shell',
  ];
  const planned = [
    'Train match win-probability model on the full historical dataset',
    'Train player run-forecasting model, replace placeholder heuristic',
    'Persist batting/bowling scorecards for every match',
    'Deploy to a production MySQL instance',
    'Add automated tests for API endpoints and ML pipeline',
  ];

  s.addText(
    done.map((t) => ({ text: t, options: { bullet: { code: '2713' }, breakLine: true } })),
    { x: doneX + 0.05, y: colY + 0.55, w: colW - 0.1, h: 4.65, fontSize: 12.5, color: INK, fontFace: 'Calibri', paraSpaceAfter: 12, valign: 'top' }
  );
  s.addText(
    planned.map((t) => ({ text: t, options: { bullet: { code: '25CB' }, breakLine: true } })),
    { x: planX + 0.05, y: colY + 0.55, w: colW - 0.1, h: 4.65, fontSize: 12.5, color: INK, fontFace: 'Calibri', paraSpaceAfter: 12, valign: 'top' }
  );

  s.addShape('roundRect', { x: 0.55, y: 6.40, w: 12.25, h: 0.5, rectRadius: 0.05, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
  s.addText([
    { text: 'Sprint plan:  ', options: { bold: true, color: NAVY2 } },
    { text: 'S1 Schema + Seed Data + UI  →  S2 Model Training + Scorecard Ingestion  →  S3 Deployment + Tests', options: { color: INK } },
  ], { x: 0.75, y: 6.40, w: 11.9, h: 0.5, fontSize: 12, fontFace: 'Calibri', valign: 'middle' });

  footer(s, 12);
}

// ============================================================ save =======
pres.writeFile({ fileName: OUT }).then(() => console.log('wrote', OUT));
