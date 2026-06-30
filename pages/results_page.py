"""ResultsPage - results load, expand, verdict verification (Steps 4-6)."""
from __future__ import annotations

import logging

from locators.locators import ResultsLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)

# Common red-text representations a 'Pathogenic' verdict may use.
_RED_HINTS = ("rgb(2", "rgba(2", "#d", "#e", "#c", "rgb(1")


class ResultsPage(BasePage):
    def wait_loaded(self) -> "ResultsPage":
        self.visible(L.GENERAL_INFORMATION)
        self.visible(L.GERMLINE_CLASSIFICATION_CARD)
        log.info("Results page loaded with Germline Classification card")
        return self

    def expand_germline_classification(self) -> None:
        self.scroll_into_view(L.GERMLINE_CLASSIFICATION_CARD)
        try:
            self.click(L.GERMLINE_EXPAND_TOGGLE)
        except Exception:  # noqa: BLE001 - some builds expand on card click
            self.click(L.GERMLINE_CLASSIFICATION_CARD)
        self.visible(L.CLASSIFICATION_SECTION)
        log.info("Germline Variant Classification section expanded")

    def verdict_text(self) -> str:
        self.scroll_into_view(L.VERDICT)
        return self.text_of(L.VERDICT)

    def verdict_color(self) -> str:
        return self.css_value(L.VERDICT, "color")

    def verdict_is_red(self) -> bool:
        color = self.verdict_color().lower().replace(" ", "")
        return any(color.startswith(h) for h in _RED_HINTS)
