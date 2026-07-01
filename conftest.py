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
    """Attach a screenshot to the report whenever a test phase fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    drv = item.funcargs.get("driver")
    if drv is None:
        return
    _SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    path = _SCREENSHOT_DIR / f"FAIL_{item.name}_{stamp}.png"
    try:
        drv.save_screenshot(str(path))
        log.error("Saved failure screenshot: %s", path)
        try:
            import allure

            allure.attach.file(
                str(path), name=item.name, attachment_type=allure.attachment_type.PNG
            )
        except Exception:  # noqa: BLE001 - allure optional
            pass
    except Exception as exc:  # noqa: BLE001
        log.error("Could not capture screenshot: %s", exc)
