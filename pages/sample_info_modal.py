"""SampleInfoModal - Optional Sample Information modal (Step 3)."""

from __future__ import annotations

import logging

from selenium.webdriver.support import expected_conditions as EC

from config.test_data import GermlineSample
from locators.locators import SampleModalLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class SampleInfoModal(BasePage):
    def wait_until_open(self) -> SampleInfoModal:
        self.dismiss_overlays()
        self.visible(L.MODAL)
        log.info("Optional Sample Information modal opened")
        return self

    def select_germline_tab(self) -> None:
        self.click(L.GERMLINE_TAB)

    def is_germline_tab_active(self) -> bool:
        # Active Germline tab carries the 'tw-bg-primary' class.
        return self.is_displayed(L.GERMLINE_TAB_ACTIVE)

    def _react_select(self, control, option_text: str, query: str | None = None) -> None:
        """Pick a value from a react-select control. For async fields a query is typed
        into the control (which fires the option fetch); static fields just open the
        menu. Then the matching option is clicked and the control is blurred."""
        if query is not None:
            self.type_into_combobox(control, query)
        else:
            self.dismiss_overlays()
            self.click(control)
        self.click_visible(L.dropdown_option(option_text))
        # The phenotype multi-select keeps its menu open after a pick, overlaying the
        # next field. Click a neutral spot to blur the control and close the menu.
        self.click(L.MODAL_TITLE)

    def fill_germline_form(self, sample: GermlineSample) -> None:
        # Phenotype is an async react-select: must type to load options.
        self._react_select(
            L.PHENOTYPE_CONTROL, sample.phenotype_option, query=sample.phenotype_query
        )
        # Sex / Ethnicity are static react-selects: open and click the option.
        self._react_select(L.SEX_CONTROL, sample.sex)
        # Age at onset is a plain text input.
        self.type(L.AGE_INPUT, sample.age_at_onset)
        self._react_select(L.ETHNICITY_CONTROL, sample.ethnicity)
        log.info(
            "Filled germline form: phenotype='%s', sex='%s', age='%s', ethnicity='%s'",
            sample.phenotype_option,
            sample.sex,
            sample.age_at_onset,
            sample.ethnicity,
        )

    def submit(self) -> None:
        self.click(L.MODAL_SEARCH_BUTTON)
        log.info("Submitted sample information modal")

    def wait_closed(self) -> bool:
        # The modal dismisses on a successful submit; wait for it to disappear.
        self.wait.until(EC.invisibility_of_element_located(L.MODAL))
        log.info("Sample information modal closed")
        return True
