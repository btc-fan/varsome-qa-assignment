"""Authentication tests for VarSome sign-in.

- Negative: invalid credentials are rejected — the form stays and the error banner
  shows. Needs no account.
- Positive: valid credentials sign in (form gone). Runs only when creds are set in
  `.env` (VARSOME_USER / VARSOME_PASSWORD).
"""

import pytest

from config.settings import settings
from pages.login_page import LoginPage

INVALID_CREDENTIALS_ERROR = (
    "Please enter a correct email address and password. "
    "Note that both fields may be case-sensitive."
)


@pytest.mark.login
@pytest.mark.regression
def test_login_rejects_invalid_credentials(driver):
    login = LoginPage(driver).load()
    login.login("not-a-real-user@example.com", "wrong-password")

    assert login.is_login_form_present(), "Invalid credentials unexpectedly signed in"
    assert (
        INVALID_CREDENTIALS_ERROR in login.error_message()
    ), "Expected the invalid-credentials error"


@pytest.mark.login
@pytest.mark.skipif(
    not (settings.varsome_user and settings.varsome_password),
    reason="Set VARSOME_USER and VARSOME_PASSWORD in .env to run the valid-login test.",
)
def test_login_with_valid_credentials(driver):
    login = LoginPage(driver).load()
    login.login(settings.varsome_user, settings.varsome_password)

    assert not login.is_login_form_present(), "Valid credentials did not sign in"
