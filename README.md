# VarSome — BRAF:V600E (hg38) Germline Classification Suite

UI regression suite verifying that VarSome classifies the germline variant
**BRAF:V600E (hg38)** as **Pathogenic**, after submitting defined sample
information in the *Optional Sample Information* modal.

Stack: Python 3.10+, Selenium 4 (Selenium Manager — no manual driver binary),
pytest, Page Object Model.

## Test case

`TC-BRAF-V600E-001` in `tests/test_braf_v600e_classification.py`. The single test
maps 1:1 to the six documented steps; every step asserts independently so a
failure isolates the exact stage.

## Architecture

```
config/      settings (env-driven) + scenario data
locators/    all selectors, single source of truth
pages/       Page Objects (base, home, sample_info_modal, results)
tests/       test cases
utils/       webdriver factory
conftest.py  fixtures + screenshot-on-failure hook
reports/     html + allure output + failure screenshots (gitignored)
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
pytest                                # full suite, headless, html+allure report
pytest -m smoke                       # smoke marker only
HEADLESS=false pytest                 # watch the browser
pytest -n auto                        # parallel (pytest-xdist)
pytest --reruns 2 --reruns-delay 3    # flake guard (pytest-rerunfailures)
```

Reports: `reports/report.html`. Allure: `allure serve reports/allure-results`.

## Configuration (.env)

| Var | Default | Purpose |
|-----|---------|---------|
| BASE_URL | https://varsome.com | target |
| GENOME | hg38 | reference build asserted in Step 2 |
| BROWSER | chrome | chrome \| firefox |
| HEADLESS | true | headed when false |
| PAGE_LOAD_TIMEOUT | 45 | seconds |
| EXPLICIT_WAIT | 30 | seconds |
| WINDOW_SIZE | 1920,1080 | viewport |

## Known constraint — verify locators before first run

VarSome's live DOM was not crawlable from the build environment. Selectors in
`locators/locators.py` are resilient best-effort and the blocks marked `VERIFY`
(modal fields, verdict element) are the most likely to need a one-time
adjustment against the real DOM. Run once headed, fix any `VERIFY` selector that
misses, commit. Fix only in `locators/` — never inline.

## oh-my-claudecode (OMC) execution

OMC is a multi-agent orchestration plugin for Claude Code. Use it to drive the
locator-verification and first-green-run loop.

Install (run each slash command separately inside Claude Code):

```
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
```

Then restart Claude Code and run `/oh-my-claudecode:omc-setup`.

Drive the suite from inside a Claude Code session opened at the project root:

```
autopilot: run the BRAF:V600E pytest suite headed, inspect any selector flagged
VERIFY that fails to match the live varsome.com DOM, fix it in locators/locators.py
only, and loop until the suite is green
```

`autopilot` decomposes into architect → executor → qa-tester and iterates without
manual babysitting. For fuzzy follow-ups use `deep-interview` to force
requirement clarification before it generates changes.
