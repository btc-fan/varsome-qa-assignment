"""Scenario data. Decoupled from page logic so cases stay declarative."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GermlineSample:
    case_id: str
    variant: str
    genome: str
    phenotype_query: str
    phenotype_option: str
    sex: str
    age_at_onset: str
    ethnicity: str
    expected_verdict: str


# BRAF:V600E is classified Pathogenic on both genome builds, so the same scenario
# runs across hg38 and hg19 with only the genome field changing.
GERMLINE_SCENARIOS = [
    GermlineSample(
        case_id="BRAF-V600E-hg38",
        variant="BRAF:V600E",
        genome="hg38",
        phenotype_query="Cancer",
        phenotype_option="Cancer (MONDO:0004992)",
        sex="Female",
        age_at_onset="60",
        ethnicity="East Asian",
        expected_verdict="Pathogenic",
    ),
    GermlineSample(
        case_id="BRAF-V600E-hg19",
        variant="BRAF:V600E",
        genome="hg19",
        phenotype_query="Cancer",
        phenotype_option="Cancer (MONDO:0004992)",
        sex="Female",
        age_at_onset="60",
        ethnicity="East Asian",
        expected_verdict="Pathogenic",
    ),
]
