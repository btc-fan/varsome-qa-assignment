"""Germline variant classification on VarSome (TC-BRAF-V600E-001).

Confirms a germline variant is classified as its expected verdict (in red) with a
score, interpretation and evidence rules, after submitting the Optional Sample
Information. Data-driven over GERMLINE_SCENARIOS (BRAF:V600E on hg38 and hg19).

The test reads as the six documented steps: each line is one action or one check,
all logic lives in the page objects, and every step logs what it did.
"""

from __future__ import annotations

import pytest

from config.test_data import EXPECTED_CARD_CONTENT, GERMLINE_SCENARIOS, GermlineSample
from locators.locators import ResultsLocators
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.sample_info_modal import SampleInfoModal

SCENARIO_PARAMS = [
    pytest.param(GERMLINE_SCENARIOS[0], marks=(pytest.mark.smoke, pytest.mark.regression)),
    pytest.param(GERMLINE_SCENARIOS[1], marks=(pytest.mark.regression,)),
]


@pytest.mark.germline
@pytest.mark.parametrize("scenario", SCENARIO_PARAMS, ids=[s.case_id for s in GERMLINE_SCENARIOS])
def test_germline_classification(driver, scenario: GermlineSample):
    # Step 1 — launch VarSome and select the reference genome build.
    home = HomePage(driver).load()
    home.select_genome(scenario.genome)
    assert home.shows_genome(scenario.genome), f"Genome is not set to {scenario.genome}"

    # Step 2 — search for the variant.
    home.search_variant(scenario.variant)

    # Step 3 — complete the Optional Sample Information (Germline) modal and submit.
    modal = SampleInfoModal(driver).wait_until_open()
    assert modal.is_germline_tab_active(), "Germline tab is not selected"
    modal.fill_germline_form(scenario)
    modal.submit()
    assert modal.wait_closed(), "Sample information modal did not close after submit"

    # Step 4 — the results page shows every information card, each with its content.
    results = ResultsPage(driver).wait_loaded()
    missing_cards = results.missing_sections(ResultsLocators.TOP_PANEL_SECTIONS)
    assert not missing_cards, f"Result cards missing: {missing_cards}"
    wrong_cards = results.cards_missing_expected_content(EXPECTED_CARD_CONTENT)
    assert not wrong_cards, f"Result cards with unexpected content: {wrong_cards}"

    # Step 5 — expand the Germline Classification; automated evidence rules appear.
    results.expand_germline_classification()
    assert results.has_evidence_rules(), "No automated ACMG evidence rules displayed"

    # Step 6 — the verdict is the expected classification, shown in red, with a
    # score and interpretation.
    assert results.verdict_is(scenario.expected_verdict), "Unexpected classification verdict"
    assert results.verdict_is_red(), "Verdict is not rendered in red"
    assert results.has_positive_score(), "ACMG score is missing or not positive"
    assert results.has_interpretation(), "ACMG interpretation is empty"
