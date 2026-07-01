"""HomePage - launch + initiate variant search (Steps 1-2)."""

from __future__ import annotations

import logging

from selenium.webdriver.common.keys import Keys

from config.settings import settings
from locators.locators import HomeLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class HomePage(BasePage):
    def load(self) -> HomePage:
        self.open(settings.base_url)
        self.dismiss_overlays()
        self.visible(L.SEARCH_INPUT)
        log.info("Homepage loaded")
        return self

    def select_genome(self, genome: str) -> None:
        # Open the custom dropdown, then pick the matching build option.
        self.click(L.GENOME_SELECTOR)
        self.click(L.genome_option(genome))
        log.info("Selected genome '%s'", genome)

    def genome_text(self) -> str:
        return self.text_of(L.GENOME_SELECTOR)

    def search_variant(self, variant: str) -> None:
        self.type(L.SEARCH_INPUT, variant)
        log.info("Typed variant '%s'", variant)
        self.dismiss_overlays()  # HubSpot CTA overlay can intercept the click
        try:
            self.click(L.SEARCH_BUTTON)
        except Exception:  # noqa: BLE001 - some builds submit on Enter only
            self.visible(L.SEARCH_INPUT).send_keys(Keys.RETURN)
