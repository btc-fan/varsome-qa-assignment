"""Authentication tests for VarSome sign-in.

- Negative: invalid credentials must be rejected (form stays / error shown).
- Positive: valid credentials sign in (form gone). Runs only when creds are set.

Both are skipped until the login selectors are verified against the live DOM and the
site is reachable (see LoginLocators / TODO.md). The negative test needs no account.
"""

import pytest

from config.settings import settings
from pages.login_page import LoginPage


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.skip(reason="Login selectors need one-time live verification; unskip after verifying.")
def test_login_rejects_invalid_credentials(driver):
    login = LoginPage(driver).load()
    login.login("not-a-real-user@example.com", "wrong-password")

    # Login must NOT succeed: the sign-in form is still shown (no redirect).
    assert login.is_login_form_present(), "Invalid credentials unexpectedly signed in"


@pytest.mark.login
@pytest.mark.skipif(
    not (settings.varsome_user and settings.varsome_password),
    reason="Set VARSOME_USER and VARSOME_PASSWORD in .env to run the valid-login test.",
)
def test_login_with_valid_credentials(driver):
    login = LoginPage(driver).load()
    login.login(settings.varsome_user, settings.varsome_password)

    # Successful login redirects away from the sign-in form.
    assert not login.is_login_form_present(), "Valid credentials did not sign in"
