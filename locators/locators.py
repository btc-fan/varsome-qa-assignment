"""Single source of truth for selectors.

CAUTION: VarSome is a third-party app whose DOM was not crawlable from the build
environment. Selectors below are resilient best-effort (text / aria / placeholder
based) and MUST be verified against the live DOM before first green run. Each block
flagged VERIFY is the most likely to need adjustment. Update here only — never inline.
"""
from selenium.webdriver.common.by import By

Locator = tuple[str, str]


class HomeLocators:
    # VERIFY: search input placeholder text may differ slightly.
    SEARCH_INPUT: Locator = (
        By.XPATH,
        "//input[contains(@placeholder, 'gene') or contains(@placeholder, 'variant')]",
    )
    GENOME_SELECTOR: Locator = (
        By.XPATH,
        "//*[self::button or self::div or self::span]"
        "[contains(normalize-space(.), 'hg38') or contains(normalize-space(.), 'hg19')]",
    )
    SEARCH_BUTTON: Locator = (
        By.XPATH,
        "//button[@type='submit' or contains(translate(., 'SEARCH', 'search'), 'search')]",
    )


class SampleModalLocators:
    # VERIFY: the modal container + tab/field selectors are the highest-risk block.
    MODAL: Locator = (
        By.XPATH,
        "//*[contains(@class,'modal') or @role='dialog']"
        "[.//*[contains(normalize-space(.), 'Optional Sample Information')]]",
    )
    GERMLINE_TAB: Locator = (
        By.XPATH,
        "//*[self::button or self::a or @role='tab'][normalize-space()='Germline']",
    )
    PHENOTYPE_INPUT: Locator = (
        By.XPATH,
        "//label[contains(.,'Phenotype')]/following::input[1] "
        "| //input[contains(@placeholder,'henotype')]",
    )
    SEX_INPUT: Locator = (
        By.XPATH,
        "//label[contains(.,'Sex')]/following::*[self::select or @role='combobox'][1]",
    )
    AGE_INPUT: Locator = (
        By.XPATH,
        "//label[contains(.,'Age')]/following::input[1] "
        "| //input[contains(@placeholder,'ge at onset')]",
    )
    ETHNICITY_INPUT: Locator = (
        By.XPATH,
        "//label[contains(.,'Ethnicity')]/following::*[self::select or @role='combobox' or self::input][1]",
    )
    MODAL_SEARCH_BUTTON: Locator = (
        By.XPATH,
        "(//*[contains(@class,'modal') or @role='dialog']"
        "//button[contains(translate(.,'SEARCH','search'),'search')])[last()]",
    )

    @staticmethod
    def dropdown_option(text: str) -> Locator:
        # VERIFY: autocomplete option container class.
        return (
            By.XPATH,
            f"//*[@role='option' or contains(@class,'option') or contains(@class,'suggestion')]"
            f"[contains(normalize-space(.), \"{text}\")]",
        )


class ResultsLocators:
    GENERAL_INFORMATION: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'General Information')]",
    )
    GERMLINE_CLASSIFICATION_CARD: Locator = (
        By.XPATH,
        "//*[contains(@class,'card') or @role='region']"
        "[.//*[contains(normalize-space(.), 'Germline Classification')]]",
    )
    GERMLINE_EXPAND_TOGGLE: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Germline Classification')]"
        "/ancestor-or-self::*[1]//*[self::button or @role='button' or contains(@class,'expand')]",
    )
    CLASSIFICATION_SECTION: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Germline Variant Classification')]",
    )
    # VERIFY: the verdict element + its color styling.
    VERDICT: Locator = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Germline Variant Classification')]"
        "/following::*[self::span or self::div or self::h1 or self::h2 or self::h3]"
        "[normalize-space()='Pathogenic'][1]",
    )
