"""LoginPage - VarSome sign-in (`/sign-in/`, OIDC).

Exposes navigation + credential submission and lets the test decide pass/fail.
Selectors for the credential fields are best-effort (see LoginLocators) and need a
one-time live verification.
"""

from __future__ import annotations

import logging

from config.settings import settings
from locators.locators import LoginLocators as L
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class LoginPage(BasePage):
    PATH = "/sign-in/"

    def load(self) -> LoginPage:
        self.open(f"{settings.base_url}{self.PATH}")
        self.dismiss_overlays()
        self.visible(L.FORM)
        log.info("Sign-in page loaded")
        return self

    def login(self, username: str, password: str) -> None:
        self.type(L.USERNAME_INPUT, username)
        self.type(L.PASSWORD_INPUT, password)
        self.click(L.SUBMIT)
        log.info("Submitted login for '%s'", username)

    def is_login_form_present(self) -> bool:
        """True while the sign-in form is still shown — i.e. login has not succeeded.
        A successful login redirects away from the form (OIDC callback)."""
        return self.is_displayed(L.FORM)

    def error_message(self) -> str:
        text = self.text_of(L.ERROR_MESSAGE)
        log.info("Login error: '%s'", text)
        return text
