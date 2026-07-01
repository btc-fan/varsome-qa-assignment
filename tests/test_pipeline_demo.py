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
def test_pipeline_second_pass():
    # Previously an intentional failure to prove red reporting; now green to prove the
    # PR comment + report update on retrigger.
    assert 2 + 2 == 4
