"""Centralized, environment-driven configuration. No magic numbers in test/page code."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://varsome.com").rstrip("/")
    # Credentials for the authenticated-login test. Empty by default; set in .env
    # (never commit). The negative login test does not need them.
    varsome_user: str = os.getenv("VARSOME_USER", "")
    varsome_password: str = os.getenv("VARSOME_PASSWORD", "")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _bool("HEADLESS", True)
    page_load_timeout: int = _int("PAGE_LOAD_TIMEOUT", 45)
    explicit_wait: int = _int("EXPLICIT_WAIT", 30)
    window_size: tuple[int, int] = field(
        default_factory=lambda: tuple(  # type: ignore[arg-type]
            int(x) for x in os.getenv("WINDOW_SIZE", "1920,1080").split(",")
        )
    )


settings = Settings()
