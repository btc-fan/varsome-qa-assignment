"""Pipeline / report demonstration tests — NOT product tests.

These exist ONLY to exercise the CI pipeline and the HTML report end-to-end (a
passing case and a failing case) without depending on the live VarSome site, which is
IP rate-limited. They prove that:
  - the report renders both passed and failed outcomes, and
  - the CI job goes RED when a test fails (the "Fail job if tests failed" gate).
Remove them once the live suite can run in CI. See README / TODO.md.
"""

import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_pipeline_reporting_pass():
    # Demonstrates a passing row in the report.
    assert 1 + 1 == 2


@pytest.mark.regression
def test_pipeline_reporting_fail():
    # Demonstrates a failing row + proves the CI job fails on test failure.
    assert 1 + 1 == 3, "intentional failure — pipeline/report demonstration only"
