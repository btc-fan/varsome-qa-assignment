"""BasePage: thin, reusable Selenium interaction layer built on explicit waits.
No time.sleep anywhere. Every interaction waits on a concrete condition."""
from __future__ import annotations

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings

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

    def type(self, locator: Locator, text: str, clear: bool = True) -> None:
        el = self.visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.visible(locator).text.strip()

    def scroll_into_view(self, locator: Locator) -> WebElement:
        el = self.present(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", el
        )
        return el

    def css_value(self, locator: Locator, prop: str) -> str:
        return self.visible(locator).value_of_css_property(prop)

    def screenshot(self, path: str) -> None:
        self.driver.save_screenshot(path)
