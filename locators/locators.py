"""Single source of truth for selectors.

All locators below were verified against the live VarSome DOM (hg38) by walking the
six documented steps via the selenium MCP. Anchor priority used: stable `id` >
`data-testid` > scoped CSS / label-text XPath. Volatile hashes (CSS-module suffixes,
react-select `css-*` and styled-components `-sc-*` suffixes) are never used as the
sole anchor — only stable name prefixes (`ColoredPill__StyledPill`) or section ids.

Update here only — never inline a selector in a page object or test.
"""

from selenium.webdriver.common.by import By

Locator = tuple[str, str]


class HomeLocators:
    # id="search" name="query" — stable id anchor (placeholder text is volatile).
    SEARCH_INPUT: Locator = (By.ID, "search")
    # Custom dropdown widget; the selected value div renders "hg38" / "hg19".
    # Scoped to the search form so it survives other ".select-selected" widgets.
    GENOME_SELECTOR: Locator = (
        By.CSS_SELECTOR,
        "#variant-search-form .select-selected",
    )
    SEARCH_BUTTON: Locator = (By.ID, "varsome-search-btn")

    @staticmethod
    def genome_option(genome: str) -> Locator:
        # Option inside the open custom dropdown; scoped to the search form so it
        # never matches another '.select-item' widget. Exact text isolates hg38/hg19.
        return (
            By.XPATH,
            "//*[@id='variant-search-form']"
            f"//div[contains(@class,'select-item')][normalize-space(text())='{genome}']",
        )


class SecurityValidationLocators:
    """Anti-bot interstitial shown after submitting the search. Must click Proceed
    to continue to the results page (reCAPTCHA-protected, but the button proceeds)."""

    PROCEED_BUTTON: Locator = (By.ID, "proceedBtn")


class LoginLocators:
    """Sign-in page (`/sign-in/`, OIDC). Form `#login-form` posts to `/auth/login/`.

    URL, form and submit are verified from the served page. The username/password
    inputs and the error banner are rendered after the OIDC step and were NOT
    live-verifiable from this environment (Chrome could not reach the site) — they are
    best-effort Django `/auth/login/` conventions and are marked VERIFY: confirm the
    exact selectors against the live DOM before relying on the positive-login test.
    """

    FORM: Locator = (By.ID, "login-form")
    SUBMIT: Locator = (By.CSS_SELECTOR, "#login-form button[type='submit']")
    # VERIFY: Django /auth/login/ default field names; confirm live.
    USERNAME_INPUT: Locator = (By.CSS_SELECTOR, "#login-form input[name='username']")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "#login-form input[name='password']")
    # VERIFY: invalid-credentials banner; confirm the real error container live.
    ERROR_MESSAGE: Locator = (
        By.CSS_SELECTOR,
        "#login-form .alert-danger, #login-form .errorlist, .alert-danger",
    )


class SampleModalLocators:
    # Modal container, anchored on its title so it never matches another VarSome modal.
    MODAL: Locator = (
        By.XPATH,
        "//div[contains(@class,'modal-container-window')]"
        "[.//*[contains(normalize-space(.),'Optional Sample Information')]]",
    )
    # Neutral element inside the modal; clicked to blur a react-select and close its
    # menu (the phenotype multi-select keeps its menu open after a pick).
    MODAL_TITLE: Locator = (
        By.XPATH,
        "//*[normalize-space(text())='Optional Sample Information']",
    )
    # Germline / Somatic toggle. Active tab carries 'tw-bg-primary'; exact text isolates it.
    GERMLINE_TAB: Locator = (
        By.XPATH,
        "//div[contains(@class,'tw-cursor-pointer') and normalize-space(text())='Germline']",
    )
    # The active Germline tab specifically — same element when it carries 'tw-bg-primary'.
    GERMLINE_TAB_ACTIVE: Locator = (
        By.XPATH,
        "//div[contains(@class,'tw-cursor-pointer') and contains(@class,'tw-bg-primary')"
        " and normalize-space(text())='Germline']",
    )
    # Each field is a react-select scoped by a stable section id. Selecting requires
    # clicking the control first (see page object).
    PHENOTYPE_CONTROL: Locator = (
        By.CSS_SELECTOR,
        "#germline-modal-phenotypes [class*='-control']",
    )
    SEX_CONTROL: Locator = (By.CSS_SELECTOR, "#germline-modal-sex [class*='-control']")
    # Plain text input (NOT a react-select). Label-anchored because the section id
    # `germline-modal-onset-age` is reused by the Family Segregation block.
    AGE_INPUT: Locator = (
        By.XPATH,
        "//*[normalize-space(text())='Age at onset']/following::input[1]",
    )
    ETHNICITY_CONTROL: Locator = (
        By.CSS_SELECTOR,
        "#germline-modal-ethnicity [class*='-control']",
    )
    # Bottom "Search" submit; last() avoids any in-field search control.
    MODAL_SEARCH_BUTTON: Locator = (
        By.XPATH,
        "(//div[contains(@class,'modal-container-window')]"
        "//button[normalize-space()='Search'])[last()]",
    )

    @staticmethod
    def dropdown_option(text: str) -> Locator:
        # react-select option: class ends in '-option' (e.g. css-yt9ioa-option),
        # no role attribute. Exact text match avoids partial hits (e.g. "Cancer of...").
        return (
            By.XPATH,
            f"//div[contains(@class,'-option')][normalize-space()=\"{text}\"]",
        )


class OverlayLocators:
    """Nuisance overlays that intercept clicks / steal focus; dismiss when present."""

    COOKIE_ACCEPT: Locator = (By.ID, "onetrust-accept-btn-handler")
    # The release-notes popup ("VarSome & VarSome Clinical v...") is a HubSpot CTA
    # rendered inside this iframe; its close button lives INSIDE the iframe.
    RELEASE_NOTES_IFRAME: Locator = (By.CSS_SELECTOR, 'iframe[title="Popup CTA"]')
    RELEASE_NOTES_CLOSE: Locator = (By.ID, "interactive-close-button")


class ResultsLocators:
    # "General Information" header leaf inside the variantDetails card.
    GENERAL_INFORMATION: Locator = (
        By.XPATH,
        "//*[normalize-space(text())='General Information']",
    )
    # Germline Classification card in the top info panel = the ACMG card.
    GERMLINE_CLASSIFICATION_CARD: Locator = (By.CSS_SELECTOR, '[data-testid="acmg"]')
    # Step-4 evidence sections, anchored on stable data-testid cards.
    CLINVAR: Locator = (By.CSS_SELECTOR, '[data-testid="clinVar"]')
    LOVD: Locator = (By.CSS_SELECTOR, '[data-testid="lovd"]')
    PHARMGKB: Locator = (By.CSS_SELECTOR, '[data-testid="pharmGKB"]')
    PUBLICATIONS: Locator = (By.CSS_SELECTOR, '[data-testid="publications"]')
    # Clicking the ACMG card expands the detailed Germline Variant Classification view.
    GERMLINE_EXPAND_TOGGLE: Locator = (By.CSS_SELECTOR, '[data-testid="acmg"]')
    # Header of the expanded detailed section.
    CLASSIFICATION_SECTION: Locator = (
        By.XPATH,
        "//a[normalize-space()='Germline Variant Classification']",
    )
    # Verdict pill. styled-components prefix 'ColoredPill__StyledPill' is stable; the
    # '-sc-*' suffix is not, so we match by prefix. Unique on the page. Red rendering is
    # the pill BACKGROUND color rgb(199,7,0) (text is white) — see ResultsPage.verdict_is_red.
    VERDICT: Locator = (By.CSS_SELECTOR, "[class*='ColoredPill__StyledPill']")
    # ACMG score of the germline classification (the "expected score" in the objective).
    # ACMG_scores_total_score = the total (e.g. "13"); ACMG_scores = summary "13points =13P-0B".
    SCORE_TOTAL: Locator = (By.CSS_SELECTOR, '[data-testid="ACMG_scores_total_score"]')
    SCORE_SUMMARY: Locator = (By.CSS_SELECTOR, '[data-testid="ACMG_scores"]')
    # Automated ACMG evidence rules (Step 5): links like PS3, PM1, PP3 — each points to
    # the rule docs anchor (…/germline-implementation/#pp3), which isolates them from
    # other links in the section.
    EVIDENCE_RULES: Locator = (
        By.CSS_SELECTOR,
        "a[href*='germline-implementation/#']",
    )
