# CricketIQ — Selenium Test Report

| | |
| --- | --- |
| Application | CricketIQ (Flask + SQLite), served on `http://127.0.0.1:5055` |
| Browser / driver | Chrome 154 headless, chromedriver auto-resolved by Selenium Manager |
| Framework | Selenium 4.50.0, pytest 9.1.1, pytest-html |
| Python | 3.13.3 (project `venv`) |
| Data under test | Live `instance/cricketiq.db` — 15 teams, 809 players, 1,243 matches |
| **Result** | **59 passed, 0 failed, 0 skipped — 65.6 s** |

## Commands used

```bash
# 1. install test tooling into the project virtual environment
venv/Scripts/python.exe -m pip install selenium pytest pytest-html

# 2. run the full suite (starts the Flask server itself, drives Chrome, writes reports)
venv/Scripts/python.exe -m pytest tests -v --tb=short \
    --html=tests/reports/selenium_report.html --self-contained-html \
    --junitxml=tests/reports/junit.xml

# optional: run a single group
venv/Scripts/python.exe -m pytest tests -k "prediction" -v
```

Outputs: `tests/reports/selenium_report.html` (open in a browser), `tests/reports/junit.xml` (CI-readable),
and `tests/reports/screenshots/FAIL_<test>.png` (written automatically on any failure).

No manual server start is needed — the `server` fixture in `tests/conftest.py` boots the app on port 5055
and stops it afterwards. The desktop browser is 1440×900; the mobile fixture emulates a 390×844 phone.

## Results by area

| Area | Tests | Result | What is verified |
| --- | ---: | --- | --- |
| Page smoke | 11 | Pass | Every page loads, title contains "CricketIQ", exactly one `<h1>` with the expected text |
| Console health | 11 | Pass | No `SEVERE` browser-console messages on any page (charts included) |
| 404 handling | 1 | Pass | Unknown route renders the custom 404 page with a way home |
| Shell / navigation | 3 | Pass | Sidebar link navigates and sets `aria-current`; skip link is first Tab stop; theme toggle switches dark↔light and persists across reload |
| Home | 1 | Pass | Stat tiles equal the values returned by `/api/stats` |
| Teams | 3 | Pass | Directory lists franchises; live filter narrows to one card; nonsense query shows the empty state; team page shows squad table |
| Players | 5 | Pass | Server search finds "Kohli"; role filter returns only that role; pagination keeps the filter; column sort toggles `aria-sort`; Kohli profile shows 9,346 runs, average, centuries |
| Matches | 2 | Pass | Season filter returns rows; match detail shows result and scorecard |
| Analytics | 2 | Pass | 3 charts render with non-zero size; legend buttons toggle `aria-pressed` |
| Intelligence | 6 | Pass | Match prediction (MI v CSK) returns probabilities summing to 100%; same-team and empty selections are rejected inline; player forecast returns a number; XI assistant returns exactly 11 players; similarity returns peers and a cluster badge |
| API validation | 6 | Pass | `/api/stats` shape; five malformed API calls each return HTTP 400 with an `error` field |
| Responsive | 2 | Pass | No horizontal overflow at 390 px on six pages; mobile drawer opens and closes with Esc |
| Accessibility | 6 | Pass | Every input/select on five pages has a label; all decorative SVG icons are `aria-hidden` |
| **Total** | **59** | **59 pass** | |

## How the first runs went (honest log)

The first run had **10 failures, all defects in the test harness, none in the application**:

| Symptom | Cause | Fix in tests |
| --- | --- | --- |
| Several `.text` assertions saw empty strings | Selenium treats `opacity: 0` as not displayed; elements were still in their 280 ms fade-in | Wait until `document.getAnimations()` is idle before asserting |
| Clicks "intercepted" on lower-page buttons | `html { scroll-behavior: smooth }` — `scrollIntoView` was still animating when the click fired | Scroll with `behavior: 'instant'` before clicking |
| Mobile test reported 494 px scroll width | Headless Chrome clamps window width to ~500 px, so the "390 px" test was not 390 px | Use Chrome mobile device emulation and assert `innerWidth == 390` |
| Home `<h1>` check failed | Test expected the product name; the h1 is the tagline "Every team, every player…" | Corrected the expectation |

After these fixes the suite passed 59/59, and the mobile test now genuinely runs at 390 px.

## Observations (not failures)

- Match-prediction and forecast calls take ~1.5 s on the first request (model load) and ~10 ms afterwards; tests allow 40 s to be safe.
- Tests that read specific data (Kohli 9,346 runs, MI/CSK names) depend on the shipped database; re-seeding with different data would require updating those literals.
- The XI assistant is tested for *shape* (11 players, reasoning text), not for selection quality.

## Limits of this test run

- Chrome only (no Firefox/Edge/Safari), headless, on Windows.
- No load/performance testing and no visual-regression comparison.
- Accessibility checks are structural (labels, aria attributes, focus order); a full audit with axe-core or a screen reader was not run.

## Files

```
tests/
├── conftest.py              # server + Chrome fixtures, screenshot-on-failure hook
├── test_cricketiq_ui.py     # 59 test cases
├── export_report.py         # renders this Markdown report to reports/TEST_REPORT.html
├── pytest.ini
└── reports/                 # selenium_report.html, junit.xml, TEST_REPORT.html
```
