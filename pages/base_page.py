"""BasePage: thin, reusable Selenium interaction layer built on explicit waits.
No time.sleep anywhere. Every interaction waits on a concrete condition."""

from __future__ import annotations

import contextlib
import logging

from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings
from locators.locators import OverlayLocators, SecurityValidationLocators

Locator = tuple[str, str]
log = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.explicit_wait)

    # -- navigation --------------------------------------------------------
    def open(self, url: str) -> None:
        log.info("GET %s", url)
        self.driver.get(url)

    # -- waits -------------------------------------------------------------
    def visible(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def present(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def clickable(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_displayed(self, locator: Locator) -> bool:
        try:
            return self.visible(locator).is_displayed()
        except TimeoutException:
            return False

    # -- actions -----------------------------------------------------------
    def click(self, locator: Locator) -> None:
        el = self.clickable(locator)
        try:
            el.click()
        except Exception:  # noqa: BLE001 - fall back to JS click on intercept
            self.driver.execute_script("arguments[0].click();", el)

    def click_visible(self, locator: Locator) -> None:
        """Click an element that is visible but whose container re-renders rapidly
        (e.g. async react-select options). element_to_be_clickable polls can hit a
        transient None mid-render and crash, so wait on visibility and JS-click."""
        el = self.visible(locator)
        self.driver.execute_script("arguments[0].click();", el)

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        el = self.visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def type_into_combobox(self, control: Locator, text: str) -> None:
        """Open a react-select control and type a query into it. Clicking the control
        focuses its hidden autosize <input>; we wait for that input to hold focus, then
        send keys (the async option list only loads on real key events). If the
        release-notes popup grabs focus first, we close it and re-click the control."""

        def _react_select_input_focused(drv):
            el = drv.switch_to.active_element
            if (el.get_attribute("id") or "").startswith("react-select"):
                return el
            self.dismiss_overlays()
            for ctrl in drv.find_elements(*control):
                with contextlib.suppress(WebDriverException):
                    ctrl.click()
            return False

        self.wait.until(_react_select_input_focused).send_keys(text)

    # -- overlays / interstitials -----------------------------------------
    def dismiss_overlays(self) -> None:
        """Close the popups that get in the way: the cookie banner and the release
        notes popup."""
        for el in self.driver.find_elements(*OverlayLocators.COOKIE_ACCEPT):
            with contextlib.suppress(WebDriverException):
                el.click()
        self.close_release_notes_popup()

    def close_release_notes_popup(self) -> None:
        """The release-notes popup is a HubSpot 'Popup CTA' iframe. Switch into it,
        click its close button like a user would, then switch back. Does nothing when
        the popup is not present."""
        frames = self.driver.find_elements(*OverlayLocators.RELEASE_NOTES_IFRAME)
        if not frames:
            return
        self.driver.switch_to.frame(frames[0])
        try:
            for close in self.driver.find_elements(*OverlayLocators.RELEASE_NOTES_CLOSE):
                with contextlib.suppress(WebDriverException):
                    self.driver.execute_script("arguments[0].click();", close)
        finally:
            self.driver.switch_to.default_content()

    def clear_security_interstitial(self) -> None:
        """Every search submit lands on the anti-bot '/security-validation/' page.
        Wait for its Proceed button and click it to continue to the results page.
        Waiting on the button (not the URL) avoids the race where this runs before the
        redirect has happened."""
        log.info("Passing security validation interstitial")
        self.dismiss_overlays()
        self.click(SecurityValidationLocators.PROCEED_BUTTON)

    def text_of(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    def texts_of(self, locator: Locator) -> list[str]:
        """Text of every element matching the locator (non-blocking, [] if none)."""
        return [el.text.strip() for el in self.driver.find_elements(*locator)]

    def scroll_into_view(self, locator: Locator) -> WebElement:
        el = self.present(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        return el

    def css_value(self, locator: Locator, prop: str) -> str:
        return self.visible(locator).value_of_css_property(prop)

    def screenshot(self, path: str) -> None:
        self.driver.save_screenshot(path)
