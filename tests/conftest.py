"""Selenium fixtures: boots the Flask app on a spare port and drives headless Chrome."""
import os
import subprocess
import sys
import time
import urllib.request

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 5055
BASE = f"http://127.0.0.1:{PORT}"
SHOTS = os.path.join(ROOT, "tests", "reports", "screenshots")


@pytest.fixture(scope="session")
def server():
    """Start the app once for the whole session; stop it afterwards."""
    env = dict(os.environ, FLASK_ENV="development")
    code = f"from app import app; app.run(host='127.0.0.1', port={PORT}, debug=False)"
    proc = subprocess.Popen([sys.executable, "-c", code], cwd=ROOT, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.time() + 40
    while time.time() < deadline:
        try:
            urllib.request.urlopen(BASE + "/", timeout=2)
            break
        except Exception:
            time.sleep(0.5)
    else:
        proc.kill()
        pytest.fail("Flask server did not start")
    yield BASE
    proc.terminate()


def _make_driver(width, height, mobile=False):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={width},{height}")
    if mobile:  # headless Chrome clamps windows to ~500px, so emulate a real phone viewport
        opts.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": width, "height": height, "pixelRatio": 2.0}})
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--log-level=3")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return webdriver.Chrome(options=opts)


@pytest.fixture(scope="session")
def driver(server):
    d = _make_driver(1440, 900)
    d.implicitly_wait(0)
    yield d
    d.quit()


@pytest.fixture()
def mobile(server):
    d = _make_driver(390, 844, mobile=True)
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def reset_state(request, server):
    """Each desktop test starts from a clean theme + storage."""
    if "driver" in request.fixturenames:
        d = request.getfixturevalue("driver")
        d.get(server + "/")
        d.execute_script("localStorage.clear()")
        d.set_window_size(1440, 900)
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        for name in ("driver", "mobile"):
            d = item.funcargs.get(name)
            if d:
                os.makedirs(SHOTS, exist_ok=True)
                d.save_screenshot(os.path.join(SHOTS, f"FAIL_{item.name}.png"))
