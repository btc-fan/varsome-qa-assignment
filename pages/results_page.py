"""ResultsPage - results load, expand, verdict verification (Steps 4-6)."""

from __future__ import annotations

import logging
import re

from locators.locators import ResultsLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


def _is_red(css_color: str) -> bool:
    """True when an rgb()/rgba() string is a dominantly-red colour. The verdict is
    white text on a red pill, so this is applied to the pill's background-color."""
    nums = re.findall(r"\d+", css_color)
    if len(nums) < 3:
        return False
    r, g, b = (int(n) for n in nums[:3])
    return r >= 150 and g <= 90 and b <= 90


class ResultsPage(BasePage):
    def wait_loaded(self) -> ResultsPage:
        self.clear_security_interstitial()
        self.dismiss_overlays()
        self.visible(L.GENERAL_INFORMATION)
        self.visible(L.GERMLINE_CLASSIFICATION_CARD)
        log.info("Results page loaded with Germline Classification card")
        return self

    def section_present(self, locator) -> bool:
        # Non-blocking presence check so a test can assert a Step-4 section is rendered
        # without throwing when the page is still settling.
        return bool(self.driver.find_elements(*locator))

    def expand_germline_classification(self) -> None:
        self.dismiss_overlays()
        self.scroll_into_view(L.GERMLINE_CLASSIFICATION_CARD)
        self.click(L.GERMLINE_EXPAND_TOGGLE)
        self.visible(L.CLASSIFICATION_SECTION)
        log.info("Germline Variant Classification section expanded")

    def verdict_text(self) -> str:
        self.scroll_into_view(L.VERDICT)
        return self.text_of(L.VERDICT)

    def verdict_color(self) -> str:
        # The verdict pill's background carries the classification colour.
        return self.css_value(L.VERDICT, "background-color")

    def verdict_is_red(self) -> bool:
        return _is_red(self.verdict_color())

    def classification_score(self) -> str:
        # The ACMG total score (e.g. "13") — the "expected score" from the objective.
        return self.text_of(L.SCORE_TOTAL)

    def classification_interpretation(self) -> str:
        # The ACMG summary/interpretation, e.g. "13points =13P-0B" (P = pathogenic pts).
        return self.text_of(L.SCORE_SUMMARY)

    def evidence_rules(self) -> list[str]:
        # The automated ACMG evidence rules shown on expand (e.g. PS3, PM1, PP3).
        return self.texts_of(L.EVIDENCE_RULES)
