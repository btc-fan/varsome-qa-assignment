"""Pytest fixtures and failure hooks."""

from __future__ import annotations

import datetime as dt
import logging
import pathlib

import pytest

from utils.driver_factory import build_driver

log = logging.getLogger(__name__)
_SCREENSHOT_DIR = pathlib.Path("reports/screenshots")


@pytest.fixture
def driver():
    drv = build_driver()
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On a failed test, save a screenshot and embed it in the HTML report."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and not report.passed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            _SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
            stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            path = _SCREENSHOT_DIR / f"FAIL_{item.name}_{stamp}.png"
            try:
                drv.save_screenshot(str(path))
                log.error("Saved failure screenshot: %s", path)
                # Embed inline (base64) so the self-contained HTML report shows it.
                import pytest_html

                extras.append(pytest_html.extras.image(drv.get_screenshot_as_base64()))
            except Exception as exc:  # noqa: BLE001
                log.error("Could not capture screenshot: %s", exc)

    report.extras = extras
