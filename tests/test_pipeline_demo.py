"""Pipeline / report demonstration tests — NOT product tests.

Live only on the demo branch `demo/ci-report-failing` (never merged to main). One test
passes and one fails on purpose, to demonstrate the CI pipeline end to end:
  - the report renders both passed and failed outcomes,
  - a failing run still publishes the report + posts the PR comment, and
  - the CI job is marked RED when any test fails (the "Fail job if tests failed" gate).
They do not touch the live VarSome site (which is IP rate-limited), so the demo is
deterministic. See README -> Continuous integration.
"""

import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_pipeline_reporting_pass():
    # A passing row in the report.
    assert 1 + 1 == 2


@pytest.mark.regression
def test_pipeline_reporting_fail():
    # A failing row — proves the report captures failures and the CI job goes red.
    assert 1 + 1 == 3, "intentional failure — pipeline/report demonstration only"
