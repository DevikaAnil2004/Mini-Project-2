// Builds docs/CricketIQ_Project_Documentation.docx from the diagram PNGs in
// docs/diagrams/. Mirrors build_pdf.py section-for-section.
// Run: node docs/build_docx.js

const fs = require('fs');
const path = require('path');
const sizeOf = require('image-size').default || require('image-size');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType, AlignmentType, ImageRun, PageBreak,
  Header, Footer, PageNumber, LevelFormat, convertInchesToTwip, VerticalAlign,
  ExternalHyperlink,
} = require('docx');

const BASE = __dirname;
const DIAG = path.join(BASE, 'diagrams');
const OUT = path.join(BASE, 'CricketIQ_Project_Documentation.docx');
const GITHUB_URL = 'https://github.com/arjuntp-397/Mini-Project-2';

const NAVY = '1F2A44';
const AMBER = 'C8811A';
const GREY = '555555';
const LINE = 'C7CBDB';
const TINT = 'F7F7FA';

function para(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts.run })],
    spacing: { after: 160, ...opts.spacing },
    alignment: opts.alignment || AlignmentType.JUSTIFIED,
    ...opts.para,
  });
}

function h1(number, text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 200, after: 240 },
    children: [new TextRun({ text: `${number}  ${text}`, bold: true, color: NAVY, size: 32 })],
  });
}

function h2(number, text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text: `${number}  ${text}`, bold: true, color: NAVY, size: 25 })],
  });
}

function bulletPara(text) {
  return new Paragraph({
    text,
    numbering: { reference: 'bullets', level: 0 },
    spacing: { after: 90 },
  });
}

function cellText(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, size: opts.size || 17, bold: !!opts.bold, color: opts.color, font: opts.mono ? 'Courier New' : undefined })],
    spacing: { after: 0 },
  });
}

function headerCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: NAVY, color: 'auto' },
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 90, bottom: 90, left: 110, right: 110 },
    children: [cellText(text, { bold: true, color: 'FFFFFF' })],
  });
}

function bodyCell(text, width, opts = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: opts.shade ? { type: ShadingType.CLEAR, fill: TINT, color: 'auto' } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    margins: { top: 90, bottom: 90, left: 110, right: 110 },
    children: [cellText(text, opts)],
  });
}

function dataTable(rows, widthsIn, opts = {}) {
  const widths = widthsIn.map((w) => convertInchesToTwip(w));
  const total = widths.reduce((a, b) => a + b, 0);
  const trs = rows.map((row, ri) => {
    const isHeader = ri === 0;
    const shade = !isHeader && ri % 2 === 0;
    return new TableRow({
      children: row.map((cell, ci) => (isHeader
        ? headerCell(cell, widths[ci])
        : bodyCell(cell, widths[ci], { shade, mono: opts.monoFirstCol && ci === 0 }))),
    });
  });
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    rows: trs,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      left: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      right: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      insideVertical: { style: BorderStyle.SINGLE, size: 4, color: LINE },
    },
  });
}

function diagram(name, caption, widthIn = 6.5) {
  const filePath = path.join(DIAG, name);
  const buf = fs.readFileSync(filePath);
  const dim = sizeOf(buf);
  const h = widthIn * (dim.height / dim.width);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 80 },
      children: [new ImageRun({
        data: buf,
        type: 'png',
        transformation: { width: Math.round(widthIn * 96), height: Math.round(h * 96) },
      })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 240 },
      children: [new TextRun({ text: caption, italics: true, color: GREY, size: 18 })],
    }),
  ];
}

function codeBlock(lines) {
  return new Table({
    width: { size: convertInchesToTwip(6.5), type: WidthType.DXA },
    columnWidths: [convertInchesToTwip(6.5)],
    rows: [new TableRow({
      children: [new TableCell({
        width: { size: convertInchesToTwip(6.5), type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: TINT, color: 'auto' },
        margins: { top: 160, bottom: 160, left: 180, right: 180 },
        children: lines.map((l) => new Paragraph({
          spacing: { after: 40 },
          children: [new TextRun({ text: l, font: 'Courier New', size: 18 })],
        })),
      })],
    })],
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      left: { style: BorderStyle.SINGLE, size: 4, color: LINE },
      right: { style: BorderStyle.SINGLE, size: 4, color: LINE },
    },
  });
}

const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

const children = [];

// ---- Cover -----------------------------------------------------------
children.push(
  new Paragraph({ spacing: { before: 2600 }, children: [] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: 'CricketIQ', bold: true, color: NAVY, size: 72 })] }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { before: 160, after: 500 },
    children: [new TextRun({ text: 'IPL Analytics & Predictive Intelligence Platform', color: GREY, size: 28 })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 1 } },
    spacing: { after: 500 }, children: [new TextRun({ text: '' })],
  }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: 'Project Documentation', size: 24 })] }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 700 },
    children: [new TextRun({
      text: 'Requirement Gathering · User Stories · UI Design · UML Diagrams · Table Design & Normalisation',
      size: 22, color: GREY,
    })],
  }),
);

const coverRows = [
  ['Submitted to', '[Guide Name], [Designation]'],
  ['Submitted by', '[Student Name(s)]  ·  [Register / Roll Number]'],
  ['Department', '[Department Name]'],
  ['Institution', '[Institution / College Name]'],
  ['Academic Year', '[Academic Year]'],
  ['Repository', GITHUB_URL],
];
children.push(new Table({
  alignment: AlignmentType.CENTER,
  width: { size: convertInchesToTwip(5.4), type: WidthType.DXA },
  columnWidths: [convertInchesToTwip(1.7), convertInchesToTwip(3.7)],
  rows: coverRows.map(([k, v], i) => new TableRow({
    children: [
      new TableCell({
        width: { size: convertInchesToTwip(1.7), type: WidthType.DXA }, margins: { top: 90, bottom: 90 },
        borders: i < coverRows.length - 1 ? { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE } } : {},
        children: [cellText(k, { bold: true, color: NAVY, size: 19 })],
      }),
      new TableCell({
        width: { size: convertInchesToTwip(3.7), type: WidthType.DXA }, margins: { top: 90, bottom: 90 },
        borders: i < coverRows.length - 1 ? { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE } } : {},
        children: [cellText(v, { size: 19 })],
      }),
    ],
  })),
  borders: {
    top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
    left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
}));
children.push(pageBreak());

// ---- TOC ---------------------------------------------------------------
children.push(new Paragraph({
  heading: HeadingLevel.HEADING_1, spacing: { after: 240 },
  children: [new TextRun({ text: 'Table of Contents', bold: true, color: NAVY, size: 32 })],
}));
[
  '1.  Requirement Gathering', '2.  User Story Creation', '3.  UI Design',
  '4.  UML Diagrams', '5.  Table Design', '6.  Design: Customisation on Templates',
  '7.  Table Normalisation',
].forEach((t) => children.push(new Paragraph({ text: t, spacing: { after: 160 } })));
children.push(pageBreak());

// ===== 1. Requirement Gathering (condensed) ================================
children.push(h1('1.', 'Requirement Gathering'));
children.push(h2('1.1', 'Purpose'));
children.push(para(
  'CricketIQ is a web analytics platform for the IPL: one place to browse team, player '
  + 'and match records, view season analytics, and run four prediction tools — win '
  + 'probability, player form forecast, playing-XI suggestion, and player similarity.',
));

children.push(h2('1.2', 'Scope'));
children.push(para('In scope:', { alignment: AlignmentType.LEFT }));
[
  'Team, player and match directories with detail pages.',
  'Analytics dashboard: win trends, run and wicket leaderboards.',
  'Four intelligence tools: win probability, form forecast, playing-XI, similarity.',
  'Dark/light themes, responsive from mobile to desktop.',
].forEach((t) => children.push(bulletPara(t)));
children.push(para('Out of scope: live ball-by-ball ingestion, user accounts/login, payments.', { alignment: AlignmentType.LEFT }));

children.push(h2('1.3', 'Functional Requirements'));
children.push(dataTable([
  ['ID', 'Requirement', 'Route'],
  ['FR-01', 'Browse teams (paginated, searchable).', 'GET /teams'],
  ['FR-02', 'Team profile: squad + latest season record.', 'GET /teams/<id>'],
  ['FR-03', 'Browse players, filter by role.', 'GET /players'],
  ['FR-04', 'Player profile: career totals + full record.', 'GET /players/<id>'],
  ['FR-05', 'Browse matches, filter by season.', 'GET /matches'],
  ['FR-06', 'Match result + full scorecard.', 'GET /matches/<id>'],
  ['FR-07', 'Win-trend charts + leaderboards.', 'GET /analytics'],
  ['FR-08', 'Simulate a matchup, view win probability.', 'GET /api/predict/match'],
  ['FR-09', 'Forecast a player’s next-innings runs.', 'GET /api/predict/player'],
  ['FR-10', 'Suggested playing XI for a matchup.', 'GET /api/assistant/team_selection'],
  ['FR-11', 'Find statistically similar players.', 'GET /api/players/similarity'],
  ['FR-12', 'Client-side filter, search, sort on any list.', 'client JS'],
  ['FR-13', 'Persisted dark / light theme.', 'client JS'],
], [0.6, 4.3, 1.6], { monoFirstCol: true }));

children.push(new Paragraph({ spacing: { after: 200 }, children: [] }));
children.push(h2('1.4', 'Non-Functional Requirements'));
children.push(dataTable([
  ['Category', 'Requirement'],
  ['Performance', 'ML models cached in-process; eager-loaded joins avoid N+1 queries.'],
  ['Usability', 'One component set across all pages; inline errors + toasts, no alert().'],
  ['Accessibility', 'Contrast ≥ 4.5:1 body / ≥ 3:1 large text; visible focus ring; ARIA-live regions.'],
  ['Responsiveness', 'Sidebar ≥ 1200px, drawer below; verified 390px–1440px.'],
  ['Maintainability', 'Template inheritance + shared macros; one CSS token layer.'],
  ['Reliability', 'Defined empty/error state on every list and API call.'],
], [1.3, 5.2]));
children.push(pageBreak());

// ===== 2. User Story Creation (condensed) ==================================
children.push(h1('2.', 'User Story Creation'));
children.push(para('Written from the perspective of an Analyst — the system’s single actor; CricketIQ has no login or roles.'));
children.push(dataTable([
  ['ID', 'User story', 'Acceptance criteria'],
  ['US-01', 'Browse all teams to see franchise details at a glance.', 'Paginated, filterable directory; each card links to a team page.'],
  ['US-02', 'View a team’s squad and season record to assess form.', 'Sortable squad table + season stat tiles.'],
  ['US-03', 'Filter players by role to focus on a position.', 'Role dropdown + instant on-page search.'],
  ['US-04', 'View a player’s career totals and match record.', 'Career tiles + batting/bowling tables; empty state if none.'],
  ['US-05', 'Browse matches for a season to review fixtures.', 'Season filter; sortable, links to each scorecard.'],
  ['US-06', 'View a match scorecard for the full breakdown.', 'Both innings’ tables; empty state if no scorecard.'],
  ['US-07', 'See win trends and leaderboards to spot form.', 'Trend chart (or ranked bars for one season) + two leaderboards.'],
  ['US-08', 'Simulate a matchup for a win-probability estimate.', 'Rejects invalid pairs inline; doughnut chart + factors on success.'],
  ['US-09', 'Forecast a player’s next-innings runs.', 'Recent form, projected runs, confidence label.'],
  ['US-10', 'Get a suggested playing XI for a matchup.', '11 players with role breakdown + reasoning.'],
  ['US-11', 'Find players statistically similar to one chosen.', 'Cluster ID + up to 5 similar players.'],
  ['US-12', 'Switch dark / light theme to match my environment.', 'Choice persists; no flash of wrong theme.'],
], [0.55, 2.85, 3.1], { monoFirstCol: true }));
children.push(pageBreak());

// ===== 3. UI Design (condensed) =============================================
children.push(h1('3.', 'UI Design'));
children.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED, spacing: { after: 160 },
  children: [
    new TextRun('The interface uses a custom design system, '),
    new TextRun({ text: '"Floodlight"', bold: true }),
    new TextRun(' — one CSS token layer (static/css/style.css) over the Bootstrap 5 grid, '
      + 'colour in OKLCH throughout. Dark is default; light mode is fully supported, both '
      + 'verified for contrast rather than assumed. Pitch-green and analytics-blue — the '
      + 'reflex choices for a cricket dashboard — were deliberately avoided in favour of a '
      + 'cool graphite surface with a single amber accent.'),
  ],
}));
children.push(...diagram('uidesign.png', 'Figure 3.1 — Colour tokens, typography and core components, rendered at true size.', 6.5));
children.push(para(
  'Type pairs three families: Inter Tight (headings), Inter (body), JetBrains Mono '
  + '(every number, so table figures never jitter). Full spec in DESIGN.md.',
));
children.push(pageBreak());

// ===== 4. UML Diagrams ======================================================
children.push(h1('4.', 'UML Diagrams'));

children.push(h2('4.1', 'Use Case Diagram'));
children.push(para(
  'One actor — an unauthenticated analyst — grouped into four service areas. The three '
  + 'directory use cases share a single "Filter, Search & Sort" behaviour via <<include>>.',
));
children.push(...diagram('usecase.png', 'Figure 4.1 — Use case diagram.', 6.5));

children.push(h2('4.2', 'Class Diagram'));
children.push(para(
  'Condensed view of the six SQLAlchemy models. Team is the hub, referenced by Player '
  + 'and by Match in four FK roles (home, away, winner, toss winner). Batting and '
  + 'bowling figures live in their own tables rather than as columns on Player — see '
  + 'Section 7.',
));
children.push(...diagram('classdiagram.png', 'Figure 4.2 — Class diagram.', 6.3));

children.push(h2('4.3', 'Process Flow — Match Win Prediction'));
children.push(para(
  'End-to-end flow for the win-probability use case, across Browser, Flask API and '
  + 'Model/Data. Errors return inline plus a toast, never a blocking alert().',
));
children.push(...diagram('workflow.png', 'Figure 4.3 — Match prediction process flow.', 6.5));
children.push(pageBreak());

// ===== 5. Table Design (diagram-led, condensed) =============================
children.push(h1('5.', 'Table Design'));
children.push(para(
  'Six tables, implemented with Flask-SQLAlchemy. Full field list, types and keys '
  + 'below; every table also carries created_at / updated_at, omitted here for brevity.',
));
children.push(...diagram('tabledesign.png', 'Figure 5.1 — Database table design.', 6.5));
children.push(para(
  'Team is the reference point for Player (squad) and Match (home/away/winner/toss, '
  + 'four FK roles). BattingStatistic and BowlingStatistic each key off (player_id, '
  + 'match_id); TeamStatistic keys off (team_id, season).',
));
children.push(pageBreak());

// ===== 6. Design: Customisation on Templates ================================
children.push(h1('6.', 'Design: Customisation on Templates'));
children.push(para(
  'All 13 pages extend one base layout (templates/base.html), which owns the sidebar, '
  + 'topbar, footer, toast region and five Jinja2 blocks. Each child template overrides '
  + 'only the blocks it needs.',
));
children.push(para(
  'Two macro files remove repetition further: _icons.html (one SVG sprite, no Font '
  + 'Awesome dependency) and _components.html (pagination, empty states, badges, filter '
  + 'search — shared by every listing page).',
));
children.push(...diagram('templates.png', 'Figure 6.1 — Template inheritance.', 6.5));

children.push(new Paragraph({ spacing: { before: 160, after: 100 }, alignment: AlignmentType.LEFT, children: [new TextRun('Example child template:')] }));
children.push(codeBlock([
  '{% extends "base.html" %}',
  '{% block title %}Teams — CricketIQ{% endblock %}',
  '{% block content %}',
  '  ... page markup, using the icon() and role_badge() macros ...',
  '{% endblock %}',
]));
children.push(pageBreak());

// ===== 7. Table Normalisation (condensed) ====================================
children.push(h1('7.', 'Table Normalisation'));

children.push(h2('7.1', '1NF'));
children.push(para(
  'Every column is atomic; no repeating groups. A player’s many innings become rows '
  + 'in batting_statistics / bowling_statistics, not numbered columns on players.',
));

children.push(h2('7.2', '2NF'));
children.push(para(
  'All six tables key on a single-column id, so 2NF holds automatically. The real '
  + 'business keys — (player_id, match_id) and (team_id, season) — have every other '
  + 'column depend on the full pair, never on one half.',
));

children.push(h2('7.3', '3NF'));
children.push(para(
  'No column depends on another non-key column. A player’s team name is never copied '
  + 'onto players — only team_id, resolved via FK. Season aggregates (wins, points, '
  + 'run_rate) live in team_statistics, not on teams, since they describe a (team, '
  + 'season) pair and would otherwise be overwritten every season.',
));

children.push(h2('7.4', 'Summary'));
children.push(dataTable([
  ['Table', '1NF', '2NF', '3NF', 'Notes'],
  ['teams', 'Yes', 'Yes', 'Yes', 'No repeating groups; no transitive dependency.'],
  ['players', 'Yes', 'Yes', 'Yes', 'team_id is an FK, not a copied team name.'],
  ['matches', 'Yes', 'Yes', 'Yes', 'Four team roles are FKs.'],
  ['batting_statistics', 'Yes', 'Yes', 'Yes', 'One row per (player, match).'],
  ['bowling_statistics', 'Yes', 'Yes', 'Yes', 'One row per (player, match).'],
  ['team_statistics', 'Yes', 'Yes', 'Yes', 'Keyed by (team, season), off teams.'],
], [1.55, 0.55, 0.55, 0.55, 3.35], { monoFirstCol: true }));

children.push(new Paragraph({ spacing: { before: 260 }, children: [] }));
children.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  children: [
    new TextRun({ text: 'Further detail: README.md, PROJECT_OVERVIEW.md, DESIGN.md at the project root; source at ', italics: true }),
    new ExternalHyperlink({ link: GITHUB_URL, children: [new TextRun({ text: GITHUB_URL, italics: true, color: '0563C1', underline: {} })] }),
    new TextRun({ text: '.', italics: true }),
  ],
}));

// ---- document assembly -----------------------------------------------
const numbering = {
  config: [{
    reference: 'bullets',
    levels: [{
      level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.18) } } },
    }],
  }],
};

const runningHeader = new Header({
  children: [new Paragraph({
    tabStops: [{ type: 'right', position: convertInchesToTwip(6.5) }],
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 6 } },
    children: [
      new TextRun({ text: 'CricketIQ — IPL Analytics Platform', size: 17, color: GREY }),
      new TextRun({ text: '\tProject Documentation', size: 17, color: GREY }),
    ],
  })],
});

const runningFooter = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 6 } },
    children: [
      new TextRun({ text: 'Page ', size: 17, color: GREY }),
      new TextRun({ children: [PageNumber.CURRENT], size: 17, color: GREY }),
    ],
  })],
});

const doc = new Document({
  creator: 'CricketIQ Project Team',
  title: 'CricketIQ — Project Documentation',
  numbering,
  sections: [{
    properties: {
      page: {
        size: { width: convertInchesToTwip(8.27), height: convertInchesToTwip(11.69) },
        margin: {
          top: convertInchesToTwip(0.8), bottom: convertInchesToTwip(0.8),
          left: convertInchesToTwip(0.8), right: convertInchesToTwip(0.8),
        },
      },
    },
    headers: { default: runningHeader },
    footers: { default: runningFooter },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log('wrote', OUT);
});
