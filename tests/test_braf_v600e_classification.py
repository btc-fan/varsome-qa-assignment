"""TC-BRAF-V600E-001 — Germline classification of BRAF:V600E (hg38) is 'Pathogenic'.

Maps 1:1 to the six documented steps. Each step carries its own assertion so a
failure pinpoints the exact stage that broke.
"""
from __future__ import annotations

import pytest

from config.settings import settings
from config.test_data import BRAF_V600E as S
from pages.home_page import HomePage
from pages.results_page import ResultsPage
from pages.sample_info_modal import SampleInfoModal


@pytest.mark.smoke
@pytest.mark.germline
@pytest.mark.braf
def test_braf_v600e_germline_classification_is_pathogenic(driver):
    # Step 1 — launch
    home = HomePage(driver).load()

    # Step 2 — initiate search + verify genome
    home.assert_genome(settings.genome)
    home.search_variant(S.variant)

    # Step 3 — complete the Optional Sample Information modal
    modal = SampleInfoModal(driver).wait_until_open()
    modal.select_germline_tab()
    modal.fill_germline_form(
        phenotype_query=S.phenotype_query,
        phenotype_option=S.phenotype_option,
        sex=S.sex,
        age_at_onset=S.age_at_onset,
        ethnicity=S.ethnicity,
    )
    modal.submit()

    # Step 4 — results page populated
    results = ResultsPage(driver).wait_loaded()

    # Step 5 — expand germline classification
    results.expand_germline_classification()

    # Step 6 — verdict
    verdict = results.verdict_text()
    assert verdict == S.expected_verdict, (
        f"Verdict mismatch: expected '{S.expected_verdict}', got '{verdict}'"
    )
    assert results.verdict_is_red(), (
        f"Verdict '{verdict}' is not rendered in red (color={results.verdict_color()})"
    )
