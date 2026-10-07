// Mini Project Evaluation deck (14 required slides + 1 extra system-design slide).
// Numbers come straight from instance/cricketiq.db and the model-evaluation run in this session.
// Run: node docs/build_evaluation_ppt.js
const path = require('path');
const pptxgen = require('pptxgenjs');

const DIAG = path.join(__dirname, 'diagrams');
const SHOT = path.join(__dirname, 'shots');
const OUT = path.join(__dirname, 'CricketIQ_Mini_Project_Evaluation.pptx');

const NAVY = '0F1E3D', NAVY2 = '1F2A44', INK = '1A1A1A', GREY = '5B6072';
const AMBER = 'F5A623', AMBER_DK = 'B45309', CARD = 'F7F7FA', LINE = 'C7CBDB', WHITE = 'FFFFFF';
const BLUE = '3B82F6', PURPLE = '8B5CF6', GREEN = '22C55E', ORANGE = 'F59E0B', RED = 'EF4444';

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5
const PW = 13.33, PH = 7.5;
pres.defineSlideMaster({ title: 'PLAIN', background: { color: WHITE } });

let n = 0;
function slide(kicker, title) {
  const s = pres.addSlide({ masterName: 'PLAIN' });
  n += 1;
  s.addText(kicker.toUpperCase(), { x: 0.55, y: 0.32, w: 8, h: 0.3, fontSize: 11, bold: true, color: AMBER_DK, fontFace: 'Calibri', charSpacing: 1 });
  s.addText(title, { x: 0.55, y: 0.58, w: 12.2, h: 0.7, fontSize: 28, bold: true, color: NAVY, fontFace: 'Cambria' });
  s.addText('CricketIQ - Mini Project Evaluation', { x: 0.4, y: PH - 0.42, w: 6, h: 0.3, fontSize: 9, color: GREY, fontFace: 'Calibri' });
  s.addText(String(n), { x: PW - 0.9, y: PH - 0.42, w: 0.5, h: 0.3, fontSize: 9, color: GREY, align: 'right', fontFace: 'Calibri' });
  return s;
}

function bullets(s, items, o) {
  s.addText(
    items.map((t) => ({ text: t, options: { bullet: { code: '2022' }, breakLine: true } })),
    Object.assign({ fontSize: 14, color: INK, fontFace: 'Calibri', paraSpaceAfter: 9, valign: 'top' }, o)
  );
}

function card(s, x, y, w, h, title, color, items, fs) {
  s.addShape('roundRect', { x, y, w, h, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
  s.addShape('rect', { x, y, w, h: 0.45, fill: { color }, line: { color, width: 0 } });
  s.addText(title, { x: x + 0.15, y, w: w - 0.3, h: 0.45, fontSize: 14, bold: true, color: WHITE, fontFace: 'Calibri', valign: 'middle' });
  bullets(s, items, { x: x + 0.15, y: y + 0.58, w: w - 0.3, h: h - 0.7, fontSize: fs || 12.5, paraSpaceAfter: 6 });
}

// 1 ───────────────────────────── Title
{
  const s = pres.addSlide({ masterName: 'PLAIN' }); n += 1;
  s.background = { color: NAVY };
  s.addShape('rect', { x: 0, y: 0, w: PW, h: 0.09, fill: { color: AMBER }, line: { color: AMBER, width: 0 } });
  s.addText('MINI PROJECT EVALUATION', { x: 0.9, y: 0.9, w: 11, h: 0.4, fontSize: 13, bold: true, color: AMBER, fontFace: 'Calibri', charSpacing: 2 });
  s.addText('CricketIQ', { x: 0.9, y: 1.35, w: 11.5, h: 1.1, fontSize: 56, bold: true, color: WHITE, fontFace: 'Cambria' });
  s.addText('IPL Data Analytics & Predictive Intelligence Platform', { x: 0.9, y: 2.45, w: 11.5, h: 0.55, fontSize: 21, color: 'CADCFC', fontFace: 'Calibri' });
  s.addShape('line', { x: 0.9, y: 3.2, w: 4.6, h: 0, line: { color: AMBER, width: 1.5 } });

  const team = [['Ahana Saji', '[Roll No.]'], ['Arjun T P', '[Roll No.]'], ['Devika Anil', '[Roll No.]']];
  s.addText('TEAM MEMBERS  (Team No. 08)', { x: 0.9, y: 3.5, w: 6, h: 0.3, fontSize: 11, bold: true, color: 'A9B4D0', fontFace: 'Calibri', charSpacing: 1 });
  team.forEach(([nm, roll], i) => {
    const x = 0.9 + i * 3.2;
    s.addText(nm, { x, y: 3.85, w: 3.0, h: 0.4, fontSize: 18, bold: true, color: WHITE, fontFace: 'Calibri' });
    s.addText(roll, { x, y: 4.25, w: 3.0, h: 0.3, fontSize: 12.5, color: 'A9B4D0', fontFace: 'Calibri' });
  });
  s.addText('GUIDE', { x: 10.4, y: 3.5, w: 2.6, h: 0.3, fontSize: 11, bold: true, color: 'A9B4D0', fontFace: 'Calibri', charSpacing: 1 });
  s.addText('Dr. Amritha Priya K', { x: 10.0, y: 3.85, w: 3.0, h: 0.4, fontSize: 18, bold: true, color: WHITE, fontFace: 'Calibri' });
  s.addText('Department of Computer Applications  |  [Institution Name]  |  [Academic Year]', { x: 0.9, y: 6.5, w: 11.5, h: 0.4, fontSize: 13, color: 'A9B4D0', fontFace: 'Calibri' });
}

// 2 ───────────────────────────── Introduction
{
  const s = slide('Overview', 'Introduction');
  bullets(s, [
    'The Indian Premier League (IPL) produces a huge volume of cricket data every season.',
    'CricketIQ is a web platform that collects this data in one place and makes it easy to explore.',
    'It stores ball-by-ball records of 1,243 IPL matches in a relational database.',
    'It adds an analytics dashboard and four machine-learning tools on top of the data.',
    'Built with Python, Flask and scikit-learn; usable by fans, analysts and students.',
  ], { x: 0.55, y: 1.55, w: 7.3, h: 5.2, fontSize: 16, paraSpaceAfter: 14 });
  const tiles = [['1,243', 'matches'], ['809', 'players'], ['15', 'franchises'], ['18,842', 'batting innings']];
  tiles.forEach(([big, small], i) => {
    const x = 8.35 + (i % 2) * 2.3, y = 1.7 + Math.floor(i / 2) * 2.2;
    s.addShape('roundRect', { x, y, w: 2.1, h: 1.95, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    s.addText(big, { x, y: y + 0.35, w: 2.1, h: 0.8, fontSize: 32, bold: true, color: AMBER, align: 'center', fontFace: 'Cambria' });
    s.addText(small, { x, y: y + 1.15, w: 2.1, h: 0.4, fontSize: 13, color: 'CADCFC', align: 'center', fontFace: 'Calibri' });
  });
}

// 3 ───────────────────────────── Problem Statement
{
  const s = slide('Overview', 'Problem Statement');
  s.addShape('roundRect', { x: 0.55, y: 1.55, w: 12.25, h: 1.5, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  s.addText('IPL statistics are scattered across many sources, mostly static, and offer no single place to explore history or get data-driven predictions.',
    { x: 0.85, y: 1.55, w: 11.65, h: 1.5, fontSize: 18, color: WHITE, fontFace: 'Calibri', valign: 'middle' });
  card(s, 0.55, 3.3, 3.95, 3.5, 'Scattered Data', 'DC2626', ['Records spread across sites and broadcasts', 'No unified, queryable history', 'Player aliases cause duplicates']);
  card(s, 4.69, 3.3, 3.95, 3.5, 'Static Analysis', '2563EB', ['Tables and PDFs, not interactive', 'Hard to filter by season or team', 'Toss / venue effects not shown']);
  card(s, 8.83, 3.3, 3.97, 3.5, 'No Prediction Aid', '16A34A', ['No quick win-probability view', 'No form forecast for a player', 'Squad selection done by gut feel']);
}

// 4 ───────────────────────────── Objectives
{
  const s = slide('Overview', 'Objectives');
  const objs = [
    ['1', 'Build a clean relational database of all IPL teams, players and matches'],
    ['2', 'Ingest ball-by-ball data and compute career statistics automatically'],
    ['3', 'Provide searchable directories and detailed player / match pages'],
    ['4', 'Visualise season trends and leaderboards in an analytics dashboard'],
    ['5', 'Add ML tools: match prediction, run forecast, playing XI, player similarity'],
    ['6', 'Deliver a fast, accessible, responsive web interface'],
  ];
  objs.forEach(([k, t], i) => {
    const col = i % 2, row = Math.floor(i / 2);
    const x = 0.55 + col * 6.2, y = 1.6 + row * 1.7;
    s.addShape('roundRect', { x, y, w: 6.0, h: 1.5, rectRadius: 0.08, fill: { color: CARD }, line: { color: LINE, width: 0.75 } });
    s.addShape('ellipse', { x: x + 0.25, y: y + 0.4, w: 0.7, h: 0.7, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    s.addText(k, { x: x + 0.25, y: y + 0.4, w: 0.7, h: 0.7, fontSize: 20, bold: true, color: AMBER, align: 'center', valign: 'middle', fontFace: 'Cambria' });
    s.addText(t, { x: x + 1.15, y, w: 4.7, h: 1.5, fontSize: 14, color: INK, fontFace: 'Calibri', valign: 'middle' });
  });
}

// 5 ───────────────────────────── Existing System
{
  const s = slide('Analysis', 'Existing System');
  card(s, 0.55, 1.55, 5.9, 5.2, 'How it works today', '5B6072', [
    'IPL stats read from sports websites and broadcast graphics',
    'Raw datasets downloaded as CSV / JSON, analysed by hand in spreadsheets',
    'Each source covers only a slice: scores, or players, or standings',
    'Any prediction is expert opinion, not computed from history',
  ], 14);
  card(s, 6.85, 1.55, 5.95, 5.2, 'Limitations / Drawbacks', 'DC2626', [
    'No single unified view of teams, players and matches',
    'Manual and time-consuming; results are static',
    'No structured database to query historical trends',
    'Same player appears under several name variants',
    'No data-backed win probability or form forecast',
    'Poor usability on mobile and in low light',
  ], 14);
}

// 6 ───────────────────────────── Proposed System
{
  const s = slide('Solution', 'Proposed System');
  card(s, 0.55, 1.55, 5.9, 5.2, 'Proposed Solution', '2563EB', [
    'Automated pipeline loads 1,243 ball-by-ball fixtures into one SQLite database',
    'Flask web app with directories, detail pages and an analytics dashboard',
    'Four ML tools served as JSON APIs and cached for speed',
    'One design system: dark and light themes, responsive layout',
  ], 14);
  card(s, 6.85, 1.55, 5.95, 5.2, 'Advantages', '16A34A', [
    'One place for the complete IPL record',
    'Career stats (average, strike rate, 100s, 50s) computed automatically',
    'Interactive: filter, search, sort and chart without reloads',
    'Predictions in under a second after first load',
    'Normalised (3NF) schema keeps data consistent',
    'Open-source stack, no licence cost',
  ], 14);
}

// 7 ───────────────────────────── Methodology / System Design
{
  const s = slide('Design', 'Methodology / System Architecture');
  s.addImage({ path: path.join(DIAG, 'architecture.png'), x: 0.55, y: 1.45, w: 8.3, h: 8.3 * (940 / 1500) });
  card(s, 9.1, 1.45, 3.7, 5.3, 'Approach Followed', NAVY2, [
    'Collect: Cricsheet JSON + player registers',
    'Clean: resolve aliases, validate fixtures',
    'Store: 6-table normalised schema',
    'Model: train 3 scikit-learn models',
    'Serve: Flask routes + JSON APIs',
    'Present: Jinja2 pages with Chart.js',
  ], 12.5);
}

// 8 ───────────────────────────── System Design (contd.)
{
  const s = slide('Design', 'System Design - Workflow and Database');
  s.addImage({ path: path.join(DIAG, 'workflow.png'), x: 0.45, y: 1.75, w: 6.2, h: 6.2 * (640 / 1400) });
  s.addImage({ path: path.join(DIAG, 'tabledesign.png'), x: 6.75, y: 1.75, w: 6.1, h: 6.1 * (1060 / 1760) });
  s.addText('Match-prediction process flow', { x: 0.45, y: 4.75, w: 6.2, h: 0.3, fontSize: 12, italic: true, color: GREY, align: 'center', fontFace: 'Calibri' });
  s.addText('Database table design (6 tables, 3NF)', { x: 6.75, y: 5.5, w: 6.1, h: 0.3, fontSize: 12, italic: true, color: GREY, align: 'center', fontFace: 'Calibri' });
  bullets(s, [
    'Teams are the hub: referenced by players, matches and season statistics.',
    'Batting and bowling statistics are one row per (player, match) - no repeating columns.',
  ], { x: 0.55, y: 5.35, w: 6.0, h: 1.6, fontSize: 12.5 });
}

// 9 ───────────────────────────── Technologies Used
{
  const s = slide('Implementation', 'Technologies Used');
  const rows = [
    ['Category', 'Technology'],
    ['Language', 'Python 3, JavaScript, HTML5, CSS3'],
    ['Backend framework', 'Flask, Flask-SQLAlchemy (SQLAlchemy 2.0), Jinja2'],
    ['Database', 'SQLite (cricketiq.db); MySQL-ready via configuration'],
    ['Data processing', 'pandas, NumPy, Cricsheet ball-by-ball JSON'],
    ['Machine learning', 'scikit-learn: Random Forest (classifier, regressor), K-Means, StandardScaler; joblib'],
    ['Frontend', 'Custom CSS design tokens, Bootstrap 5 grid, Chart.js, vanilla JS'],
    ['Tools / platform', 'Git + GitHub, VS Code, Chromium (testing); runs on Windows / Linux'],
  ];
  const t = rows.map((r, i) => r.map((c, ci) => ({
    text: c,
    options: i === 0
      ? { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 14, fontFace: 'Calibri', valign: 'middle' }
      : { color: INK, fontSize: 13, fontFace: ci === 0 ? 'Calibri' : 'Calibri', bold: ci === 0, fill: { color: i % 2 ? WHITE : CARD }, valign: 'middle' },
  })));
  s.addTable(t, { x: 0.55, y: 1.55, w: 12.25, h: 5.0, colW: [2.9, 9.35], border: { type: 'solid', color: LINE, pt: 0.75 } });
}

// 10 ──────────────────────────── Modules / Major Features
{
  const s = slide('Implementation', 'Modules / Major Features');
  const mods = [
    ['Data Ingestion', ORANGE, ['Parses 1,243 fixtures', 'Resolves player aliases', 'Builds standings']],
    ['Team Directory', BLUE, ['15 franchises', 'Squad and season record', 'Live search filter']],
    ['Player Profiles', PURPLE, ['809 players', 'Average, SR, 100s, 50s', 'Match-by-match log']],
    ['Matches & Scorecards', GREEN, ['Filter by season', 'Full batting / bowling card', 'Result and toss info']],
    ['Analytics Dashboard', RED, ['Wins-per-season trends', 'Run / wicket leaderboards', 'Themed Chart.js charts']],
    ['Intelligence Tools', NAVY2, ['Match win probability', 'Run forecast, playing XI', 'Player similarity (K-Means)']],
  ];
  mods.forEach(([t, c, items], i) => {
    card(s, 0.55 + (i % 3) * 4.15, 1.55 + Math.floor(i / 3) * 2.7, 3.95, 2.5, t, c, items, 13);
  });
}

// 11 ──────────────────────────── Implementation / Screenshots
{
  const s = slide('Implementation', 'Screenshots of the Working Project');
  const shots = [['home.png', 'Overview dashboard'], ['player.png', 'Player profile (V Kohli)'], ['analytics.png', 'Season analytics'], ['prediction.png', 'Match prediction (MI vs CSK)']];
  shots.forEach(([f, cap], i) => {
    const x = 0.55 + (i % 2) * 6.2, y = 1.4 + Math.floor(i / 2) * 2.85;
    s.addShape('roundRect', { x, y, w: 6.0, h: 2.45, rectRadius: 0.05, fill: { color: NAVY }, line: { color: LINE, width: 0.75 } });
    s.addImage({ path: path.join(SHOT, f), x: x + 0.08, y: y + 0.06, w: 3.76, h: 2.35 });
    s.addText(cap, { x: x + 3.95, y: y + 0.1, w: 1.95, h: 2.25, fontSize: 12, bold: true, color: WHITE, fontFace: 'Calibri', valign: 'middle' });
  });
}

// 12 ──────────────────────────── Results / Output
{
  const s = slide('Results', 'Results / Output');
  s.addChart(pres.charts.BAR, [{ name: 'Runs', labels: ['V Kohli', 'R Sharma', 'S Dhawan', 'D Warner', 'KL Rahul'], values: [9346, 7331, 6769, 6567, 5828] }], {
    x: 0.55, y: 1.4, w: 6.0, h: 2.85, barDir: 'bar', chartColors: [AMBER], showValue: true, dataLabelFontSize: 10, dataLabelColor: INK,
    showTitle: true, title: 'Top 5 run scorers (IPL career)', titleFontSize: 13, titleColor: NAVY,
    catAxisLabelFontSize: 10, valAxisHidden: true, valGridLine: { style: 'none' }, showLegend: false, catAxisOrientation: 'maxMin',
  });
  s.addChart(pres.charts.BAR, [{ name: 'Wickets', labels: ['Y Chahal', 'B Kumar', 'S Narine', 'P Chawla', 'J Bumrah'], values: [233, 226, 209, 192, 190] }], {
    x: 6.8, y: 1.4, w: 6.0, h: 2.85, barDir: 'bar', chartColors: [BLUE], showValue: true, dataLabelFontSize: 10, dataLabelColor: INK,
    showTitle: true, title: 'Top 5 wicket takers (IPL career)', titleFontSize: 13, titleColor: NAVY,
    catAxisLabelFontSize: 10, valAxisHidden: true, valGridLine: { style: 'none' }, showLegend: false, catAxisOrientation: 'maxMin',
  });
  const stats = [['155', 'wins by MI - the most of any franchise'], ['54.7%', 'toss winners who chose to field won'], ['55.7%', 'match-predictor accuracy (held-out 20%)'], ['< 1 s', 'prediction response once model is cached']];
  stats.forEach(([big, small], i) => {
    const x = 0.55 + i * 3.1;
    s.addShape('roundRect', { x, y: 4.45, w: 2.95, h: 1.15, rectRadius: 0.08, fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
    s.addText(big, { x, y: 4.5, w: 2.95, h: 0.55, fontSize: 24, bold: true, color: AMBER, align: 'center', fontFace: 'Cambria' });
    s.addText(small, { x: x + 0.1, y: 5.02, w: 2.75, h: 0.55, fontSize: 10.5, color: 'CADCFC', align: 'center', fontFace: 'Calibri', valign: 'top' });
  });
  bullets(s, [
    'Choosing to field after winning the toss pays off: 443 of 810 matches won (54.7%) vs 185 of 408 (45.3%) when batting first.',
    'Win-probability model beats a 50% coin-flip but only modestly - cricket outcomes are noisy.',
    'Run forecaster (MAE 17.1 runs) is no better than a plain average (16.9) - not reliable for single innings.',
  ], { x: 0.55, y: 5.75, w: 12.25, h: 1.3, fontSize: 12, paraSpaceAfter: 4 });
}

// 13 ──────────────────────────── Conclusion
{
  const s = slide('Wrap-up', 'Conclusion');
  card(s, 0.55, 1.55, 6.0, 5.2, 'Work Completed', '2563EB', [
    'Full IPL history loaded: 1,243 matches, 809 players, 15 franchises',
    'Normalised 6-table database with computed career statistics',
    '11 web pages and 6 JSON APIs with a consistent, accessible UI',
    'Three trained models plus a squad-balancing assistant',
  ], 14);
  card(s, 6.8, 1.55, 6.0, 5.2, 'Key Outcomes', '16A34A', [
    'Single platform replaces scattered sources',
    'Data answers real questions: toss effect, top performers, team trends',
    'Match predictor reaches 55.7% accuracy',
    'Honest evaluation: forecaster needs richer features',
    'Reusable codebase on GitHub for future work',
  ], 14);
}

// 14 ──────────────────────────── Future Scope
{
  const s = slide('Wrap-up', 'Future Scope');
  card(s, 0.55, 1.55, 6.0, 5.2, 'Possible Improvements', ORANGE, [
    'Richer model features: venue form, head-to-head, batting order, pitch type',
    'Compare models (gradient boosting, logistic regression) with cross-validation',
    'Smarter XI assistant using form and opposition matchups',
    'Add automated tests and a CI pipeline',
  ], 14);
  card(s, 6.8, 1.55, 6.0, 5.2, 'Future Enhancements', PURPLE, [
    'Live-score ingestion during the season',
    'Deploy on a cloud host with MySQL / PostgreSQL',
    'Player comparison and head-to-head pages',
    'Exportable reports (CSV / PDF)',
    'User accounts for saved teams and favourites',
  ], 14);
}

// 15 ──────────────────────────── References
{
  const s = slide('Wrap-up', 'References');
  bullets(s, [
    'Cricsheet - Free structured cricket data (ball-by-ball IPL JSON). https://cricsheet.org',
    'Breiman, L. (2001). Random Forests. Machine Learning, 45(1), 5-32.',
    'Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.',
    'Flask Documentation. https://flask.palletsprojects.com',
    'SQLAlchemy 2.0 Documentation. https://docs.sqlalchemy.org',
    'pandas and NumPy Documentation. https://pandas.pydata.org  |  https://numpy.org',
    'Chart.js Documentation. https://www.chartjs.org/docs',
    'Bootstrap 5 Documentation. https://getbootstrap.com/docs/5.3',
    'Project source code. https://github.com/arjuntp-397/Mini-Project-2',
  ], { x: 0.7, y: 1.6, w: 12.0, h: 5.2, fontSize: 15, paraSpaceAfter: 12 });
}

pres.writeFile({ fileName: OUT }).then(() => console.log('wrote', OUT));
