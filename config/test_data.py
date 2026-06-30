"""Scenario data. Decoupled from page logic so cases stay declarative."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GermlineSample:
    variant: str
    phenotype_query: str
    phenotype_option: str
    sex: str
    age_at_onset: str
    ethnicity: str
    expected_verdict: str


BRAF_V600E = GermlineSample(
    variant="BRAF:V600E",
    phenotype_query="Cancer",
    phenotype_option="Cancer (MONDO:0004992)",
    sex="Female",
    age_at_onset="60",
    ethnicity="East Asian",
    expected_verdict="Pathogenic",
)
