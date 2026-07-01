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


# Expected STABLE content per top-panel card for BRAF:V600E (holds on hg38 and hg19).
# Values are variant identity, section labels, and premium/no-data states — NOT the
# volatile numbers (frequencies, publication counts, scores) which change as VarSome's
# source databases update. Each entry: card section (data-testid) -> required substring.
EXPECTED_CARD_CONTENT = {
    "variantDetails": "p.(Val600Glu)",  # protein change (General Information)
    "genes": "BRAF",
    "transcripts": "MANE Select",
    "pathogenicityScores": "Pathogenic",  # In-Silico Predictors (PP3)
    "uniprotVariants": "Pathogenic",
    "expressionData": "testis",  # top-expressed tissue
    "frequencies": "exomes",  # label present (value is volatile)
    "conservationScores": "phyloP",  # label present (value is volatile)
    "publications": "Variant:",  # label present (count is volatile)
    "communityContributions": "Classifications:",  # label present (counts volatile)
    "spliceVault": "SpliceVault",
    "clinVar": "ClinVar",  # significance/counts vary; assert the section renders
    "pharmGKB": "Premium",  # premium-gated
    "lovd": "Premium",
    "omim": "Premium",
    "mitomap": "No data available",
    "dvd": "No data available",
    "clinGen": "No data available",
    "gwas": "No data available",
}
