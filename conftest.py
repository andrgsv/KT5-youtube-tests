from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


PROJECT_ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Браузер для запуска тестов: chrome, firefox или edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск браузера в headless-режиме",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.youtube.com/",
        help="Базовый URL тестируемого сайта",
    )


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--base-url")).rstrip("/") + "/"


@pytest.fixture
def driver(pytestconfig: pytest.Config):
    browser = pytestconfig.getoption("--browser")
    headless = bool(pytestconfig.getoption("--headless"))

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-notifications")
        options.add_argument("--lang=ru-RU")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        web_driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.set_preference("intl.accept_languages", "ru-RU, ru")
        if headless:
            options.add_argument("-headless")
        web_driver = webdriver.Firefox(options=options)
        web_driver.set_window_size(1366, 900)

    else:
        options = EdgeOptions()
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        web_driver = webdriver.Edge(options=options)

    web_driver.set_page_load_timeout(45)
    web_driver.implicitly_wait(0)

    yield web_driver

    web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        web_driver = item.funcargs.get("driver")
        if web_driver is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{item.name}_{timestamp}.png"
            path = ARTIFACTS_DIR / filename
            try:
                web_driver.save_screenshot(str(path))
                report.extra = getattr(report, "extra", []) + [str(path)]
            except Exception:
                pass
