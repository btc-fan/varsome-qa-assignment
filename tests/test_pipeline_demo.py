"""Pipeline / report demonstration tests — NOT product tests.

Used by the demo PR (branch `demo/ci-report-failing`) to exercise the CI pipeline and
the HTML report end-to-end without depending on the live VarSome site (which is IP
rate-limited). One test passes and one fails on purpose, to show that:
  - the report renders both passed and failed outcomes,
  - the failing run still publishes a report + posts the PR comment, and
  - the CI job is marked RED when any test fails (the "Fail job if tests failed" gate).
Not merged to main — this branch stays open as a living demo. See README → CI.
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
