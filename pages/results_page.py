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

    def missing_sections(self, sections: tuple[str, ...]) -> list[str]:
        # Which top-panel cards are NOT present. Non-blocking (find_elements), so the
        # test gets the full list instead of failing on the first missing one.
        missing = [s for s in sections if not self.driver.find_elements(*L.card(s))]
        log.info("Result sections present: %d/%d", len(sections) - len(missing), len(sections))
        return missing

    def cards_missing_expected_content(self, expected: dict[str, str]) -> list[str]:
        # Cards whose text does not contain the expected stable content. Returns
        # readable mismatch strings so the test can assert on one value (empty = ok).
        return [
            f"{section}: '{want}' not in '{self.text_of(L.card(section))}'"
            for section, want in expected.items()
            if want not in self.text_of(L.card(section))
        ]

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

    def verdict_is(self, expected: str) -> bool:
        actual = self.verdict_text()
        log.info("Verdict: '%s' (expected '%s')", actual, expected)
        return actual == expected

    def verdict_is_red(self) -> bool:
        red = _is_red(self.verdict_color())
        log.info("Verdict colour: %s (red=%s)", self.verdict_color(), red)
        return red

    def has_positive_score(self) -> bool:
        # The ACMG total score (e.g. "13") — the "expected score" from the objective.
        score = self.text_of(L.SCORE_TOTAL)
        log.info("ACMG score: '%s'", score)
        return score.isdigit() and int(score) > 0

    def has_interpretation(self) -> bool:
        # The ACMG summary/interpretation, e.g. "13points =13P-0B" (P = pathogenic pts).
        text = self.text_of(L.SCORE_SUMMARY)
        log.info("ACMG interpretation: '%s'", text)
        return bool(text)

    def has_evidence_rules(self) -> bool:
        # The automated ACMG evidence rules shown on expand (e.g. PS3, PM1, PP3).
        rules = self.texts_of(L.EVIDENCE_RULES)
        log.info("ACMG evidence rules: %s", rules)
        return bool(rules)
