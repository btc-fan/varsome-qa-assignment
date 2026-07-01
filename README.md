# VarSome — Germline Variant Classification Suite

UI regression suite verifying that VarSome classifies a germline variant as
**Pathogenic**, after submitting defined sample information in the *Optional Sample
Information* modal. The flow is data-driven: one parametrized test runs across
scenarios (currently **BRAF:V600E** on **hg38** and **hg19**).

Stack: Python 3.10+, Selenium 4 (Selenium Manager — no manual driver binary),
pytest, Page Object Model.

## Test cases

One parametrized test — `tests/test_germline_classification.py` — driven by
`GERMLINE_SCENARIOS` in `config/test_data.py`. Each scenario maps 1:1 to the six
documented steps; every step asserts independently so a failure isolates the exact
stage. Adding a variant/genome is a one-row data edit — no new test code.

| Case ID | Variant | Genome | Markers | Expected |
|---------|---------|--------|---------|----------|
| BRAF-V600E-hg38 | BRAF:V600E | hg38 | smoke, regression, germline | Pathogenic (red) |
| BRAF-V600E-hg19 | BRAF:V600E | hg19 | regression, germline | Pathogenic (red) |

### Traceability (test case → assertion → evidence)

| PDF step | Automation assertion | Evidence in report |
|----------|----------------------|--------------------|
| 1 Launch + genome | `select_genome` then assert `genome in genome_text()` | execution log line |
| 2 Search variant | search submitted | log + navigation |
| 3 Modal (Germline) | assert Germline tab active → fill → submit → assert modal closed | log lines |
| 4 Results loaded | assert General Information, Germline Classification, ClinVar, LOVD, PharmGKB, Publications present | log + HTML report |
| 5 Expand classification | expand + wait for section header | log |
| 6 Verdict | assert text == "Pathogenic" **and** red pill background | log + screenshot on fail |

## Architecture

```
config/      settings (env-driven) + scenario data
locators/    all selectors, single source of truth
pages/       Page Objects (base, home, sample_info_modal, results)
tests/       test cases
utils/       webdriver factory
conftest.py  fixtures + screenshot-on-failure hook
reports/     report.html + failure screenshots (gitignored)
```

Design rules enforced in code: no `time.sleep` (explicit waits only), no inline
selectors (all in `locators/`), no hardcoded config (all in `config/settings.py`
via `.env`), screenshot auto-captured on any failure.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                  # adjust if needed
```

Chrome or Firefox must be installed on the host. Selenium Manager resolves the
driver automatically — no chromedriver download step.

## Run

```bash
pytest                                # full suite (headed by default — see obstacle #3)
pytest -m smoke                       # smoke only (hg38)
pytest -m regression                  # regression (hg38 + hg19)
pytest -n auto                        # parallel (pytest-xdist)
pytest --reruns 2 --reruns-delay 3    # flake guard (pytest-rerunfailures)
```

The suite runs **headed** by default (`HEADLESS=false` in `.env`) because headless
triggers a reCAPTCHA wall (obstacle #3). In CI it runs headed under `xvfb`.

## Reports

A single self-contained **pytest-html** report — no Java, no external services.

- **HTML**: `reports/report.html` — self-contained (open the file directly). In CI it
  is published to GitHub Pages per run and uploaded as a downloadable artifact.
- **Screenshots**: on any test failure `conftest.py` captures a screenshot and embeds
  it inline (base64) in the HTML report; a copy is also saved to `reports/screenshots/`.
- **Execution logs**: `log_cli` streams each step (genome select, modal fill,
  interstitial, verdict) into the run output and the report.

## Configuration (.env)

| Var | Default | Purpose |
|-----|---------|---------|
| BASE_URL | https://varsome.com | target |
| GENOME | hg38 | default build (per-scenario genome comes from test data) |
| BROWSER | chrome | chrome \| firefox |
| HEADLESS | true | headed when false |
| PAGE_LOAD_TIMEOUT | 45 | seconds |
| EXPLICIT_WAIT | 30 | seconds |
| WINDOW_SIZE | 1920,1080 | viewport |

## Live-site obstacles & workarounds

VarSome is a third-party site with anti-abuse and marketing layers that get in the
way of automation. All locators are verified against the live DOM. The obstacles
below are handled in code (or documented as a known limit) — they are the reason
some design choices look the way they do.

### 1. Release-notes popup is inside a HubSpot iframe
A timed "VarSome & VarSome Clinical v…" *Updates* popup appears after navigation and
**steals keyboard focus**, which broke typing into the modal's fields. It is **not**
in the main document — it is rendered inside `iframe[title="Popup CTA"]` (HubSpot).
Workaround (human-style, no DOM hacks): switch into the iframe, click its close
button `#interactive-close-button`, switch back — `BasePage.close_release_notes_popup()`.

### 2. Security-validation interstitial
Every search submit redirects to `/security-validation/` ("you must click the button
below before you can proceed"). Handled by waiting for and clicking `#proceedBtn`
(`BasePage.clear_security_interstitial()`). We wait on the button, not the URL, to
avoid a race with the redirect.

### 3. reCAPTCHA blocks headless
In **headless** Chrome the interstitial escalates to a reCAPTCHA "I'm not a robot"
checkbox that cannot be solved programmatically. **Headed** Chrome passes it via
browser reputation. The suite therefore runs **headed** (`HEADLESS=false`); CI runs
headed under `xvfb`.

### 4. Anonymous rate limit — "1 request per day"
VarSome limits anonymous users to ~**1 result per day per IP**. After the quota is
spent, the results page is replaced by *"To prevent abuse of the platform… Sign in to
continue, or Join."* The test then fails on the missing results — this is the rate
limit, **not** a code bug. Workarounds: wait for the daily reset, sign in with an
account (planned, creds via `.env`), or request an educational whitelist.
A VPN (NordVPN) workaround was tried and did **not** work: `curl` reaches the site but
the Selenium-launched Chrome times out (`ERR_TIMED_OUT`) — see `TODO.md`.

### Verdict rendering
The "Pathogenic" verdict is **white text on a red pill**, not red text. The red check
reads the pill's **background-color** (`ResultsPage.verdict_is_red()`).

## Continuous integration

GitHub Actions runs the suite on every push and pull request (`.github/workflows/`).
Tests run headless. The HTML report is published to GitHub Pages per run and uploaded
as a downloadable artifact; a sticky PR comment links both, with branch, commit, and
timestamp. See `TODO.md` for the account/rate-limit follow-ups.
