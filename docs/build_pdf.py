# -*- coding: utf-8 -*-
"""Builds docs/CricketIQ_Project_Documentation.pdf from the diagram PNGs
already rendered into docs/diagrams/. Run with the project venv:
    venv/Scripts/python.exe docs/build_pdf.py
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = os.path.dirname(os.path.abspath(__file__))
DIAG = os.path.join(BASE, 'diagrams')
OUT = os.path.join(BASE, 'CricketIQ_Project_Documentation.pdf')

NAVY = colors.HexColor('#1f2a44')
AMBER = colors.HexColor('#c8811a')
GREY = colors.HexColor('#555555')
LINE = colors.HexColor('#c7cbdb')
GITHUB_URL = 'https://github.com/arjuntp-397/Mini-Project-2'

# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------
ss = getSampleStyleSheet()

styles = {
    'H1': ParagraphStyle('H1', parent=ss['Heading1'], fontName='Helvetica-Bold',
                          fontSize=16, textColor=NAVY, spaceBefore=6, spaceAfter=10, leading=20),
    'H2': ParagraphStyle('H2', parent=ss['Heading2'], fontName='Helvetica-Bold',
                          fontSize=12.5, textColor=NAVY, spaceBefore=14, spaceAfter=8, leading=16),
    'H3': ParagraphStyle('H3', parent=ss['Heading3'], fontName='Helvetica-Bold',
                          fontSize=11, textColor=NAVY, spaceBefore=10, spaceAfter=6, leading=14),
    'Body': ParagraphStyle('Body', parent=ss['Normal'], fontName='Helvetica',
                            fontSize=10, textColor=colors.HexColor('#1a1a1a'),
                            leading=15, spaceAfter=8, alignment=TA_JUSTIFY),
    'BodyLeft': ParagraphStyle('BodyLeft', parent=ss['Normal'], fontName='Helvetica',
                                fontSize=10, textColor=colors.HexColor('#1a1a1a'),
                                leading=14, alignment=TA_LEFT),
    'Cell': ParagraphStyle('Cell', parent=ss['Normal'], fontName='Helvetica',
                            fontSize=8.6, textColor=colors.HexColor('#1a1a1a'), leading=11.5),
    'CellMono': ParagraphStyle('CellMono', parent=ss['Normal'], fontName='Courier',
                                fontSize=8.2, textColor=colors.HexColor('#1a1a1a'), leading=11),
    'HeadCell': ParagraphStyle('HeadCell', parent=ss['Normal'], fontName='Helvetica-Bold',
                                fontSize=8.8, textColor=colors.white, leading=11),
    'Caption': ParagraphStyle('Caption', parent=ss['Normal'], fontName='Helvetica-Oblique',
                               fontSize=9, textColor=GREY, alignment=TA_CENTER,
                               spaceBefore=4, spaceAfter=14),
    'CoverTitle': ParagraphStyle('CoverTitle', parent=ss['Normal'], fontName='Helvetica-Bold',
                                  fontSize=30, textColor=NAVY, alignment=TA_CENTER, leading=36),
    'CoverSub': ParagraphStyle('CoverSub', parent=ss['Normal'], fontName='Helvetica',
                                fontSize=14, textColor=GREY, alignment=TA_CENTER, spaceBefore=8),
    'CoverField': ParagraphStyle('CoverField', parent=ss['Normal'], fontName='Helvetica',
                                  fontSize=11, textColor=colors.HexColor('#1a1a1a'),
                                  alignment=TA_CENTER, leading=18),
    'TOCEntry': ParagraphStyle('TOCEntry', parent=ss['Normal'], fontName='Helvetica',
                                fontSize=11, textColor=colors.HexColor('#1a1a1a'), leading=22),
}


def P(text, style='Body'):
    return Paragraph(text, styles[style])


def bullets(items, style='BodyLeft'):
    return ListFlowable(
        [ListItem(P(t, style), leftIndent=6, spaceAfter=4) for t in items],
        bulletType='bullet', start='•', leftIndent=14, bulletFontSize=8,
    )


def data_table(rows, col_widths, header=True):
    body = []
    for i, row in enumerate(rows):
        if header and i == 0:
            body.append([Paragraph(c, styles['HeadCell']) for c in row])
        else:
            out = []
            for j, c in enumerate(row):
                st = 'CellMono' if j == 0 and header else 'Cell'
                out.append(Paragraph(c, styles[st]))
            body.append(out)

    t = Table(body, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ('GRID', (0, 0), (-1, -1), 0.6, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    if header:
        style_cmds += [
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f7fa')]),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t


def diagram(name, caption, width_cm=16.5):
    path = os.path.join(DIAG, name)
    img = Image(path)
    ratio = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width_cm * cm
    img.drawHeight = width_cm * cm * ratio
    img.hAlign = 'CENTER'
    return [img, P(caption, 'Caption')]


def section_title(number, text):
    return P('%s&nbsp;&nbsp; %s' % (number, text), 'H1')


def hr():
    t = Table([['']], colWidths=[17 * cm], rowHeights=[0.6])
    t.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1, NAVY)]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(2 * cm, A4[1] - 1.4 * cm, A4[0] - 2 * cm, A4[1] - 1.4 * cm)
    canvas.setFont('Helvetica', 8.5)
    canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, A4[1] - 1.25 * cm, 'CricketIQ — IPL Analytics Platform')
    canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.25 * cm, 'Project Documentation')
    canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.drawCentredString(A4[0] / 2, 1.1 * cm, 'Page %d' % doc.page)
    canvas.restoreState()


def on_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 2.4 * cm, A4[0], 2.4 * cm, fill=1, stroke=0)
    canvas.setFillColor(AMBER)
    canvas.rect(0, A4[1] - 2.46 * cm, A4[0], 0.09 * cm, fill=1, stroke=0)
    canvas.restoreState()


pageBreak = PageBreak

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------
story = []

# ---- Cover ---------------------------------------------------------------
story.append(Spacer(1, 4.6 * cm))
story.append(P('CricketIQ', 'CoverTitle'))
story.append(P('IPL Analytics &amp; Predictive Intelligence Platform', 'CoverSub'))
story.append(Spacer(1, 1.2 * cm))
story.append(hr())
story.append(Spacer(1, 1.2 * cm))
story.append(P('Project Documentation', 'CoverField'))
story.append(Spacer(1, 0.3 * cm))
story.append(P('Requirement Gathering &middot; User Stories &middot; UI Design &middot; '
               'UML Diagrams &middot; Table Design &amp; Normalisation', 'CoverField'))
story.append(Spacer(1, 2.4 * cm))

cover_rows = [
    ['Submitted to', '[Guide Name], [Designation]'],
    ['Submitted by', '[Student Name(s)]  ·  [Register / Roll Number]'],
    ['Department', '[Department Name]'],
    ['Institution', '[Institution / College Name]'],
    ['Academic Year', '[Academic Year]'],
    ['Repository', GITHUB_URL],
]
cover_table = Table(cover_rows, colWidths=[4.2 * cm, 9.5 * cm], hAlign='CENTER')
cover_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 0), (-1, -1), 10.5),
    ('TEXTCOLOR', (0, 0), (0, -1), NAVY),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LINEBELOW', (0, 0), (-1, -2), 0.4, LINE),
]))
story.append(cover_table)
story.append(pageBreak())

# ---- TOC ------------------------------------------------------------------
story.append(section_title('', 'Table of Contents'))
for e in [
    '1.  Requirement Gathering', '2.  User Story Creation', '3.  UI Design',
    '4.  UML Diagrams', '5.  Table Design', '6.  Design: Customisation on Templates',
    '7.  Table Normalisation',
]:
    story.append(P(e, 'TOCEntry'))
story.append(pageBreak())

# ==========================================================================
# 1. Requirement Gathering (condensed)
# ==========================================================================
story.append(section_title('1.', 'Requirement Gathering'))

story.append(P('1.1&nbsp;&nbsp; Purpose', 'H2'))
story.append(P(
    'CricketIQ is a web analytics platform for the IPL: one place to browse team, '
    'player and match records, view season analytics, and run four prediction tools '
    '&mdash; win probability, player form forecast, playing-XI suggestion, and player '
    'similarity.', 'Body'))

story.append(P('1.2&nbsp;&nbsp; Scope', 'H2'))
story.append(P('In scope:', 'BodyLeft'))
story.append(bullets([
    'Team, player and match directories with detail pages.',
    'Analytics dashboard: win trends, run and wicket leaderboards.',
    'Four intelligence tools: win probability, form forecast, playing-XI, similarity.',
    'Dark/light themes, responsive from mobile to desktop.',
]))
story.append(P('Out of scope: live ball-by-ball ingestion, user accounts/login, '
               'payments.', 'BodyLeft'))

story.append(P('1.3&nbsp;&nbsp; Functional Requirements', 'H2'))
story.append(data_table([
    ['ID', 'Requirement', 'Route'],
    ['FR-01', 'Browse teams (paginated, searchable).', 'GET /teams'],
    ['FR-02', 'Team profile: squad + latest season record.', 'GET /teams/&lt;id&gt;'],
    ['FR-03', 'Browse players, filter by role.', 'GET /players'],
    ['FR-04', 'Player profile: career totals + full record.', 'GET /players/&lt;id&gt;'],
    ['FR-05', 'Browse matches, filter by season.', 'GET /matches'],
    ['FR-06', 'Match result + full scorecard.', 'GET /matches/&lt;id&gt;'],
    ['FR-07', 'Win-trend charts + leaderboards.', 'GET /analytics'],
    ['FR-08', 'Simulate a matchup, view win probability.', 'GET /api/predict/match'],
    ['FR-09', 'Forecast a player’s next-innings runs.', 'GET /api/predict/player'],
    ['FR-10', 'Suggested playing XI for a matchup.', 'GET /api/assistant/team_selection'],
    ['FR-11', 'Find statistically similar players.', 'GET /api/players/similarity'],
    ['FR-12', 'Client-side filter, search, sort on any list.', 'client JS'],
    ['FR-13', 'Persisted dark / light theme.', 'client JS'],
], [1.6 * cm, 11.2 * cm, 4.2 * cm]))

story.append(Spacer(1, 10))
story.append(P('1.4&nbsp;&nbsp; Non-Functional Requirements', 'H2'))
story.append(data_table([
    ['Category', 'Requirement'],
    ['Performance', 'ML models cached in-process; eager-loaded joins avoid N+1 queries.'],
    ['Usability', 'One component set across all pages; inline errors + toasts, no alert().'],
    ['Accessibility', 'Contrast ≥ 4.5:1 body / ≥ 3:1 large text; visible focus ring; ARIA-live regions.'],
    ['Responsiveness', 'Sidebar ≥ 1200px, drawer below; verified 390px–1440px.'],
    ['Maintainability', 'Template inheritance + shared macros; one CSS token layer.'],
    ['Reliability', 'Defined empty/error state on every list and API call.'],
], [3.4 * cm, 13.6 * cm]))
story.append(pageBreak())

# ==========================================================================
# 2. User Story Creation (condensed acceptance criteria)
# ==========================================================================
story.append(section_title('2.', 'User Story Creation'))
story.append(P(
    'Written from the perspective of an Analyst &mdash; the system’s single actor; '
    'CricketIQ has no login or roles.', 'Body'))

story.append(data_table([
    ['ID', 'User story', 'Acceptance criteria'],
    ['US-01', 'Browse all teams to see franchise details at a glance.',
     'Paginated, filterable directory; each card links to a team page.'],
    ['US-02', 'View a team’s squad and season record to assess form.',
     'Sortable squad table + season stat tiles.'],
    ['US-03', 'Filter players by role to focus on a position.',
     'Role dropdown + instant on-page search.'],
    ['US-04', 'View a player’s career totals and match record.',
     'Career tiles + batting/bowling tables; empty state if none.'],
    ['US-05', 'Browse matches for a season to review fixtures.',
     'Season filter; sortable, links to each scorecard.'],
    ['US-06', 'View a match scorecard for the full breakdown.',
     'Both innings’ tables; empty state if no scorecard.'],
    ['US-07', 'See win trends and leaderboards to spot form.',
     'Trend chart (or ranked bars for one season) + two leaderboards.'],
    ['US-08', 'Simulate a matchup for a win-probability estimate.',
     'Rejects invalid pairs inline; doughnut chart + factors on success.'],
    ['US-09', 'Forecast a player’s next-innings runs.',
     'Recent form, projected runs, confidence label.'],
    ['US-10', 'Get a suggested playing XI for a matchup.',
     '11 players with role breakdown + reasoning.'],
    ['US-11', 'Find players statistically similar to one chosen.',
     'Cluster ID + up to 5 similar players.'],
    ['US-12', 'Switch dark / light theme to match my environment.',
     'Choice persists; no flash of wrong theme.'],
], [1.6 * cm, 7.7 * cm, 7.7 * cm]))
story.append(pageBreak())

# ==========================================================================
# 3. UI Design (condensed)
# ==========================================================================
story.append(section_title('3.', 'UI Design'))
story.append(P(
    'The interface uses a custom design system, <b>"Floodlight"</b> &mdash; one CSS '
    'token layer (static/css/style.css) over the Bootstrap 5 grid, colour in OKLCH '
    'throughout. Dark is default; light mode is fully supported, both verified for '
    'contrast rather than assumed. Pitch-green and analytics-blue &mdash; the reflex '
    'choices for a cricket dashboard &mdash; were deliberately avoided in favour of a '
    'cool graphite surface with a single amber accent.', 'Body'))
story.extend(diagram('uidesign.png', 'Figure 3.1 — Colour tokens, typography and '
                                      'core components, rendered at true size.', 13))
story.append(P(
    'Type pairs three families: Inter Tight (headings), Inter (body), JetBrains Mono '
    '(every number, so table figures never jitter). Full spec in DESIGN.md.', 'Body'))
story.append(pageBreak())

# ==========================================================================
# 4. UML Diagrams
# ==========================================================================
story.append(section_title('4.', 'UML Diagrams'))

story.append(P('4.1&nbsp;&nbsp; Use Case Diagram', 'H2'))
story.append(P(
    'One actor &mdash; an unauthenticated analyst &mdash; grouped into four service '
    'areas. The three directory use cases share a single "Filter, Search &amp; Sort" '
    'behaviour via &lt;&lt;include&gt;&gt;.', 'Body'))
story.extend(diagram('usecase.png', 'Figure 4.1 — Use case diagram.', 13))

story.append(P('4.2&nbsp;&nbsp; Class Diagram', 'H2'))
story.append(P(
    'Condensed view of the six SQLAlchemy models. Team is the hub, referenced by '
    'Player and by Match in four FK roles (home, away, winner, toss winner). Batting '
    'and bowling figures live in their own tables rather than as columns on Player '
    '&mdash; see Section 7.', 'Body'))
story.extend(diagram('classdiagram.png', 'Figure 4.2 — Class diagram.', 12.5))

story.append(P('4.3&nbsp;&nbsp; Process Flow &mdash; Match Win Prediction', 'H2'))
story.append(P(
    'End-to-end flow for the win-probability use case, across Browser, Flask API and '
    'Model/Data. Errors return inline plus a toast, never a blocking alert().', 'Body'))
story.extend(diagram('workflow.png', 'Figure 4.3 — Match prediction process flow.', 14))
story.append(pageBreak())

# ==========================================================================
# 5. Table Design (diagram-led, condensed)
# ==========================================================================
story.append(section_title('5.', 'Table Design'))
story.append(P(
    'Six tables, implemented with Flask-SQLAlchemy. Full field list, types and keys '
    'below; every table also carries created_at / updated_at, omitted here for '
    'brevity.', 'Body'))
story.extend(diagram('tabledesign.png', 'Figure 5.1 — Database table design.', 16.8))
story.append(P(
    'Team is the reference point for Player (squad) and Match (home/away/winner/toss, '
    'four FK roles). BattingStatistic and BowlingStatistic each key off '
    '(player_id, match_id); TeamStatistic keys off (team_id, season).', 'Body'))
story.append(pageBreak())

# ==========================================================================
# 6. Design: Customisation on Templates
# ==========================================================================
story.append(section_title('6.', 'Design: Customisation on Templates'))
story.append(P(
    'All 13 pages extend one base layout (templates/base.html), which owns the '
    'sidebar, topbar, footer, toast region and five Jinja2 blocks. Each child '
    'template overrides only the blocks it needs.', 'Body'))
story.append(P(
    'Two macro files remove repetition further: _icons.html (one SVG sprite, no '
    'Font Awesome dependency) and _components.html (pagination, empty states, '
    'badges, filter search &mdash; shared by every listing page).', 'Body'))
story.extend(diagram('templates.png', 'Figure 6.1 — Template inheritance.', 14))

story.append(Spacer(1, 12))
story.append(P('Example child template:', 'BodyLeft'))
story.append(Spacer(1, 6))
code = (
    '{% extends "base.html" %}\n'
    '{% block title %}Teams &mdash; CricketIQ{% endblock %}\n'
    '{% block content %}\n'
    '  ... page markup, using icon() and role_badge() macros ...\n'
    '{% endblock %}'
)
code_style = ParagraphStyle('Code', parent=styles['Cell'], fontName='Courier', fontSize=8.6,
                             leading=12, backColor=colors.HexColor('#f7f7fa'),
                             borderColor=LINE, borderWidth=0.6, borderPadding=8)
story.append(Paragraph(code.replace('\n', '<br/>').replace('  ', '&nbsp;&nbsp;'), code_style))
story.append(pageBreak())

# ==========================================================================
# 7. Table Normalisation (condensed)
# ==========================================================================
story.append(section_title('7.', 'Table Normalisation'))

story.append(P('7.1&nbsp;&nbsp; 1NF', 'H2'))
story.append(P(
    'Every column is atomic; no repeating groups. A player’s many innings become '
    'rows in batting_statistics / bowling_statistics, not numbered columns on '
    'players.', 'Body'))

story.append(P('7.2&nbsp;&nbsp; 2NF', 'H2'))
story.append(P(
    'All six tables key on a single-column id, so 2NF holds automatically. The real '
    'business keys &mdash; (player_id, match_id) and (team_id, season) &mdash; have '
    'every other column depend on the full pair, never on one half.', 'Body'))

story.append(P('7.3&nbsp;&nbsp; 3NF', 'H2'))
story.append(P(
    'No column depends on another non-key column. A player’s team name is never '
    'copied onto players &mdash; only team_id, resolved via FK. Season aggregates '
    '(wins, points, run_rate) live in team_statistics, not on teams, since they '
    'describe a (team, season) pair and would otherwise be overwritten every season.',
    'Body'))

story.append(P('7.4&nbsp;&nbsp; Summary', 'H2'))
story.append(data_table([
    ['Table', '1NF', '2NF', '3NF', 'Notes'],
    ['teams', 'Yes', 'Yes', 'Yes', 'No repeating groups; no transitive dependency.'],
    ['players', 'Yes', 'Yes', 'Yes', 'team_id is an FK, not a copied team name.'],
    ['matches', 'Yes', 'Yes', 'Yes', 'Four team roles are FKs.'],
    ['batting_statistics', 'Yes', 'Yes', 'Yes', 'One row per (player, match).'],
    ['bowling_statistics', 'Yes', 'Yes', 'Yes', 'One row per (player, match).'],
    ['team_statistics', 'Yes', 'Yes', 'Yes', 'Keyed by (team, season), off teams.'],
], [3.2 * cm, 1.4 * cm, 1.4 * cm, 1.4 * cm, 9.6 * cm]))

story.append(Spacer(1, 14))
story.append(P(
    '<i>Further detail: README.md, PROJECT_OVERVIEW.md, DESIGN.md at the project '
    'root; source at %s.</i>' % GITHUB_URL, 'Body'))

# --------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
    title='CricketIQ — Project Documentation',
    author='CricketIQ Project Team',
)

doc.build(story, onFirstPage=lambda c, d: on_cover(c, d), onLaterPages=lambda c, d: on_page(c, d))
print('wrote', OUT)
