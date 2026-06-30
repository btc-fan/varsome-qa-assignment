"""HomePage - launch + initiate variant search (Steps 1-2)."""
from __future__ import annotations

import logging

from selenium.webdriver.common.keys import Keys

from config.settings import settings
from locators.locators import HomeLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class HomePage(BasePage):
    def load(self) -> "HomePage":
        self.open(settings.base_url)
        self.visible(L.SEARCH_INPUT)
        log.info("Homepage loaded")
        return self

    def assert_genome(self, expected: str) -> None:
        genome_text = self.text_of(L.GENOME_SELECTOR)
        assert expected in genome_text, (
            f"Genome mismatch: expected '{expected}', UI shows '{genome_text}'"
        )

    def search_variant(self, variant: str) -> None:
        self.type(L.SEARCH_INPUT, variant)
        log.info("Typed variant '%s'", variant)
        try:
            self.click(L.SEARCH_BUTTON)
        except Exception:  # noqa: BLE001 - some builds submit on Enter only
            self.visible(L.SEARCH_INPUT).send_keys(Keys.RETURN)
