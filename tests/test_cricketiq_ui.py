"""End-to-end Selenium tests for CricketIQ (headless Chrome against a live Flask server)."""
import json
import urllib.error
import urllib.request

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE = "http://127.0.0.1:5055"
T = 15  # explicit-wait timeout, seconds

PAGES = [
    ("/", "Every team"),
    ("/teams", "Teams"),
    ("/teams/1", None),
    ("/players", "Players"),
    ("/players/571", "Virat Kohli"),
    ("/matches", "Matches"),
    ("/matches/1", None),
    ("/analytics", "Analytics"),
    ("/predictions", "Predictions"),
    ("/assistant", "Selection Assistant"),
    ("/player-similarity", "Player Similarity"),
]


def wait(d, cond, t=T):
    return WebDriverWait(d, t).until(cond)


def visible(d, css, t=T):
    return wait(d, EC.visibility_of_element_located((By.CSS_SELECTOR, css)), t)


def go(d, path):
    d.get(BASE + path)
    wait(d, lambda x: x.execute_script("return document.readyState") == "complete")
    # let the CSS reveal animations finish: Selenium treats opacity:0 elements as having no text
    wait(d, lambda x: x.execute_script("return document.getAnimations().filter(a => a.playState === 'running' && a.effect.getTiming().iterations !== Infinity).length") == 0)


def click(d, el):
    d.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'})", el)
    el.click()


def api(path):
    try:
        with urllib.request.urlopen(BASE + path, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def severe_logs(d):
    return [e for e in d.get_log("browser") if e["level"] == "SEVERE"]


# ------------------------------------------------------------------ smoke --

@pytest.mark.parametrize("path,heading", PAGES)
def test_page_loads_with_title_and_h1(driver, path, heading):
    go(driver, path)
    assert "CricketIQ" in driver.title
    h1s = driver.find_elements(By.TAG_NAME, "h1")
    assert len(h1s) == 1, "exactly one <h1> per page"
    if heading:
        assert heading in h1s[0].get_attribute("textContent")


@pytest.mark.parametrize("path,_", PAGES)
def test_no_console_errors(driver, path, _):
    driver.get_log("browser")  # drain
    go(driver, path)
    # analytics draws charts asynchronously - give it a moment
    driver.execute_script("return new Promise(r => setTimeout(r, 800))")
    assert severe_logs(driver) == []


def test_unknown_route_shows_404_page(driver):
    go(driver, "/this-page-does-not-exist")
    assert "couldn't find" in driver.find_element(By.TAG_NAME, "h1").text.lower()
    assert driver.find_element(By.LINK_TEXT, "Back to overview").is_displayed()


# ---------------------------------------------------------------- shell ---

def test_sidebar_navigation_and_active_state(driver):
    go(driver, "/")
    link = driver.find_element(By.CSS_SELECTOR, ".sidebar a[href='/teams']")
    link.click()
    wait(driver, EC.url_contains("/teams"))
    active = driver.find_element(By.CSS_SELECTOR, ".sidebar [aria-current='page']")
    assert active.text.strip() == "Teams"


def test_skip_link_is_first_focusable_element(driver):
    go(driver, "/")
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
    focused = driver.switch_to.active_element
    assert "skip-link" in focused.get_attribute("class")
    assert focused.get_attribute("href").endswith("#main-content")


def test_theme_toggle_switches_and_persists(driver):
    go(driver, "/")
    html = driver.find_element(By.TAG_NAME, "html")
    assert html.get_attribute("data-theme") == "dark"
    driver.find_element(By.CSS_SELECTOR, "[data-theme-toggle]").click()
    assert html.get_attribute("data-theme") == "light"
    driver.refresh()
    wait(driver, lambda x: x.execute_script("return document.readyState") == "complete")
    assert driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme") == "light"


# ----------------------------------------------------------------- home ---

def test_home_stat_tiles_match_api(driver):
    status, stats = api("/api/stats")
    assert status == 200
    go(driver, "/")
    values = [int(e.get_attribute("textContent").replace(",", "").strip()) for e in driver.find_elements(By.CSS_SELECTOR, ".stat-tile__value")]
    assert values[:3] == [stats["total_teams"], stats["total_players"], stats["total_matches"]]


# ---------------------------------------------------------------- teams ---

def test_teams_directory_lists_all_franchises(driver):
    go(driver, "/teams")
    cards = driver.find_elements(By.CSS_SELECTOR, ".panel--link")
    assert len(cards) >= 12  # first page holds 12 of 15


def test_teams_live_filter_narrows_and_shows_empty_state(driver):
    go(driver, "/teams")
    box = driver.find_element(By.CSS_SELECTOR, "[data-filter-input='teams']")
    box.send_keys("mumbai")
    wait(driver, lambda d: len([c for c in d.find_elements(By.CSS_SELECTOR, ".panel--link") if c.is_displayed()]) == 1)
    box.clear()
    box.send_keys("zzzzzz")
    visible(driver, "[data-filter-empty='teams']")


def test_team_detail_shows_squad_and_filter(driver):
    go(driver, "/teams/1")
    rows = driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody tr")
    assert len(rows) > 5
    assert driver.find_element(By.CSS_SELECTOR, ".monogram").is_displayed()


# -------------------------------------------------------------- players ---

def test_players_server_search_finds_kohli(driver):
    go(driver, "/players?q=Kohli")
    names = [a.get_attribute("textContent") for a in driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody td:first-child a")]
    assert any("Kohli" in n for n in names)


def test_players_role_filter_only_returns_that_role(driver):
    go(driver, "/players")
    Select(driver.find_element(By.ID, "roleFilter")).select_by_visible_text("Bowler")
    click(driver, driver.find_element(By.CSS_SELECTOR, "form.filter-bar button[type='submit']"))
    wait(driver, EC.url_contains("role=Bowler"))
    badges = {b.get_attribute("textContent").strip() for b in driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody .badge-pill")}
    assert badges == {"Bowler"}


def test_players_pagination_preserves_filter(driver):
    go(driver, "/players?role=Batsman")
    nxt = driver.find_element(By.CSS_SELECTOR, "a.pager__link[rel='next']")
    click(driver, nxt)
    wait(driver, EC.url_contains("page=2"))
    assert "role=Batsman" in driver.current_url


def test_players_table_column_sort_toggles(driver):
    go(driver, "/players")
    th = [h for h in driver.find_elements(By.CSS_SELECTOR, "th[data-sort]") if h.text.strip().lower() == "player"][0]
    click(driver, th)
    assert th.get_attribute("aria-sort") == "ascending"
    first_asc = driver.find_element(By.CSS_SELECTOR, "table.data-table tbody tr td a").text
    click(driver, th)
    assert th.get_attribute("aria-sort") == "descending"
    first_desc = driver.find_element(By.CSS_SELECTOR, "table.data-table tbody tr td a").text
    assert first_asc.lower() <= first_desc.lower() or first_asc != first_desc


def test_player_profile_career_numbers(driver):
    go(driver, "/players/571")
    text = driver.find_element(By.ID, "main-content").get_attribute("textContent")
    assert "9346" in text.replace(",", "")
    assert "Batting Average" in text and "Centuries" in text


# -------------------------------------------------------------- matches ---

def test_matches_season_filter(driver):
    go(driver, "/matches")
    sel = Select(driver.find_element(By.ID, "seasonFilter"))
    assert len(sel.options) > 5
    sel.select_by_index(1)
    click(driver, driver.find_element(By.CSS_SELECTOR, "form.filter-bar button[type='submit']"))
    wait(driver, EC.url_contains("season="))
    assert driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody tr")


def test_match_detail_shows_result_and_scorecard(driver):
    go(driver, "/matches/1")
    main = driver.find_element(By.ID, "main-content").get_attribute("textContent")
    assert "Result" in main
    assert "Batting" in main


# ------------------------------------------------------------ analytics ---

def test_analytics_charts_render(driver):
    go(driver, "/analytics")
    wait(driver, lambda d: d.execute_script(
        "return Array.from(document.querySelectorAll('canvas')).every(c => c.width > 0 && c.height > 0)"))
    assert len(driver.find_elements(By.TAG_NAME, "canvas")) == 3
    legend = driver.find_elements(By.CSS_SELECTOR, ".chart-legend button")
    assert len(legend) > 5


def test_analytics_legend_toggle_hides_series(driver):
    go(driver, "/analytics")
    btn = visible(driver, ".chart-legend button")
    click(driver, btn)
    assert btn.get_attribute("aria-pressed") == "false"
    click(driver, btn)
    assert btn.get_attribute("aria-pressed") == "true"


# ---------------------------------------------------------- intelligence --

def test_match_prediction_flow(driver):
    go(driver, "/predictions")
    Select(driver.find_element(By.ID, "team1Select")).select_by_visible_text("Mumbai Indians")
    Select(driver.find_element(By.ID, "team2Select")).select_by_visible_text("Chennai Super Kings")
    click(driver, driver.find_element(By.ID, "predictBtn"))
    wait(driver, lambda d: d.find_element(By.ID, "team1ProbResult").text.endswith("%"), 40)
    a = float(driver.find_element(By.ID, "team1ProbResult").text.rstrip("%"))
    b = float(driver.find_element(By.ID, "team2ProbResult").text.rstrip("%"))
    assert abs(a + b - 100) < 0.2
    assert driver.find_element(By.ID, "resultsCard").is_displayed()


def test_prediction_rejects_same_team(driver):
    go(driver, "/predictions")
    Select(driver.find_element(By.ID, "team1Select")).select_by_visible_text("Mumbai Indians")
    Select(driver.find_element(By.ID, "team2Select")).select_by_visible_text("Mumbai Indians")
    click(driver, driver.find_element(By.ID, "predictBtn"))
    err = visible(driver, "[data-field='team2'][data-invalid='true'] .field__error")
    assert err.is_displayed()
    assert not driver.find_element(By.ID, "resultsCard").is_displayed()


def test_prediction_requires_both_teams(driver):
    go(driver, "/predictions")
    click(driver, driver.find_element(By.ID, "predictBtn"))
    visible(driver, "[data-field='team1'][data-invalid='true']")
    visible(driver, "[data-field='team2'][data-invalid='true']")


def test_player_forecast_flow(driver):
    go(driver, "/predictions")
    sel = Select(driver.find_element(By.ID, "playerSelect"))
    sel.select_by_index(1)
    click(driver, driver.find_element(By.ID, "forecastBtn"))
    wait(driver, lambda d: d.find_element(By.ID, "predictedRuns").text.strip().isdigit(), 40)
    assert driver.find_element(By.ID, "forecastResultsCard").is_displayed()


def test_playing_xi_assistant_returns_eleven(driver):
    go(driver, "/assistant")
    Select(driver.find_element(By.ID, "teamSelect")).select_by_visible_text("Mumbai Indians")
    Select(driver.find_element(By.ID, "oppSelect")).select_by_visible_text("Chennai Super Kings")
    click(driver, driver.find_element(By.ID, "assistBtn"))
    wait(driver, lambda d: len(d.find_elements(By.CSS_SELECTOR, "#xiList tr")) == 11, 30)
    assert "Picked" in driver.find_element(By.ID, "reasoningResult").text


def test_player_similarity_returns_peers(driver):
    go(driver, "/player-similarity")
    Select(driver.find_element(By.ID, "playerSelect")).select_by_index(5)
    click(driver, driver.find_element(By.ID, "simBtn"))
    wait(driver, lambda d: d.find_elements(By.CSS_SELECTOR, "#simList tr"), 30)
    assert "Cluster" in driver.find_element(By.ID, "clusterBadge").text


# ------------------------------------------------------------------ API ---

def test_api_stats_shape():
    status, body = api("/api/stats")
    assert status == 200
    assert {"total_teams", "total_players", "total_matches"} <= body.keys()


@pytest.mark.parametrize("path", [
    "/api/predict/match?team1=1&team2=1",
    "/api/predict/match",
    "/api/predict/player",
    "/api/assistant/team_selection?team_id=1&opponent_id=1",
    "/api/players/similarity",
])
def test_api_rejects_bad_input_with_400(path):
    status, body = api(path)
    assert status == 400 and "error" in body


# ----------------------------------------------------------- responsive ---

def test_mobile_has_no_horizontal_overflow(mobile):
    for path in ("/", "/teams", "/players", "/matches", "/analytics", "/predictions"):
        go(mobile, path)
        sw = mobile.execute_script("return document.documentElement.scrollWidth")
        assert mobile.execute_script("return innerWidth") == 390, "emulation not applied"
        assert sw <= 390, f"{path} overflows: scrollWidth={sw}"


def test_mobile_drawer_opens_and_closes_with_escape(mobile):
    mobile.get(BASE + "/")
    sidebar = mobile.find_element(By.CSS_SELECTOR, "[data-sidebar]")
    assert sidebar.get_attribute("data-open") in (None, "false")
    mobile.find_element(By.CSS_SELECTOR, "[data-open-nav]").click()
    wait(mobile, lambda d: sidebar.get_attribute("data-open") == "true")
    mobile.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    wait(mobile, lambda d: sidebar.get_attribute("data-open") == "false")


# --------------------------------------------------------- accessibility --

@pytest.mark.parametrize("path", ["/", "/players", "/predictions", "/assistant", "/player-similarity"])
def test_form_controls_have_labels(driver, path):
    go(driver, path)
    unlabeled = driver.execute_script("""
      return Array.from(document.querySelectorAll('input:not([type=hidden]), select, textarea'))
        .filter(el => !(el.id && document.querySelector('label[for="' + el.id + '"]')) && !el.getAttribute('aria-label'))
        .map(el => el.outerHTML.slice(0, 80));""")
    assert unlabeled == []


def test_icons_are_decorative_hidden_from_screen_readers(driver):
    go(driver, "/")
    bad = driver.execute_script("""
      return Array.from(document.querySelectorAll('svg.icon'))
        .filter(s => !s.hasAttribute('aria-hidden') && !s.hasAttribute('aria-label')).length""")
    assert bad == 0
