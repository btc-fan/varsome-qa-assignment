"""Temporary pipeline-validation tests.

These do NOT touch VarSome. They exist only to exercise the CI/CD pipeline and the
report end-to-end (a passing case and a failing case) without depending on the live
site, which is IP rate-limited. Remove once the pipeline is verified — see TODO.md.
"""

import pytest


@pytest.mark.smoke
@pytest.mark.regression
def test_pipeline_pass():
    assert 1 + 1 == 2


@pytest.mark.regression
def test_pipeline_fail():
    # Intentional failure to confirm the report and PR comment show a red result.
    assert 1 + 1 == 3, "intentional failure to validate CI reporting"
