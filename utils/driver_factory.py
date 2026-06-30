"""WebDriver factory. Relies on Selenium Manager (bundled in Selenium >=4.6),
so no chromedriver/geckodriver binary needs to be installed manually."""
from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings


def _chrome() -> WebDriver:
    opts = ChromeOptions()
    if settings.headless:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={settings.window_size[0]},{settings.window_size[1]}")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--lang=en-US")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    return webdriver.Chrome(options=opts)


def _firefox() -> WebDriver:
    opts = FirefoxOptions()
    if settings.headless:
        opts.add_argument("-headless")
    opts.add_argument(f"--width={settings.window_size[0]}")
    opts.add_argument(f"--height={settings.window_size[1]}")
    return webdriver.Firefox(options=opts)


def build_driver() -> WebDriver:
    factory = {"chrome": _chrome, "firefox": _firefox}.get(settings.browser)
    if factory is None:
        raise ValueError(f"Unsupported BROWSER='{settings.browser}'. Use chrome or firefox.")
    driver = factory()
    driver.set_page_load_timeout(settings.page_load_timeout)
    driver.maximize_window()
    return driver
