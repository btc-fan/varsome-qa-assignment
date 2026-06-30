"""SampleInfoModal - Optional Sample Information modal (Step 3)."""
from __future__ import annotations

import logging

from selenium.webdriver.support.ui import Select

from locators.locators import SampleModalLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class SampleInfoModal(BasePage):
    def wait_until_open(self) -> "SampleInfoModal":
        self.visible(L.MODAL)
        log.info("Optional Sample Information modal opened")
        return self

    def select_germline_tab(self) -> None:
        self.click(L.GERMLINE_TAB)

    def _autocomplete(self, input_locator, typed: str, option_text: str) -> None:
        """Type into an autocomplete field then pick the matching option."""
        self.type(input_locator, typed)
        self.click(L.dropdown_option(option_text))

    def _select_or_type(self, locator, value: str) -> None:
        """Handle native <select> or custom combobox uniformly."""
        el = self.visible(locator)
        if el.tag_name.lower() == "select":
            Select(el).select_by_visible_text(value)
        else:
            self.type(locator, value)
            self.click(L.dropdown_option(value))

    def fill_germline_form(
        self,
        phenotype_query: str,
        phenotype_option: str,
        sex: str,
        age_at_onset: str,
        ethnicity: str,
    ) -> None:
        self._autocomplete(L.PHENOTYPE_INPUT, phenotype_query, phenotype_option)
        self._select_or_type(L.SEX_INPUT, sex)
        self.type(L.AGE_INPUT, age_at_onset)
        self._select_or_type(L.ETHNICITY_INPUT, ethnicity)
        log.info(
            "Filled germline form: phenotype='%s', sex='%s', age='%s', ethnicity='%s'",
            phenotype_option, sex, age_at_onset, ethnicity,
        )

    def submit(self) -> None:
        self.click(L.MODAL_SEARCH_BUTTON)
        log.info("Submitted sample information modal")
