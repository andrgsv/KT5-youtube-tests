from __future__ import annotations

from typing import Iterable, Tuple

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]


class BasePage:
    """Базовый класс страницы с общими Selenium-действиями."""

    CONSENT_BUTTONS: Iterable[Locator] = (
        (By.XPATH, "//button//*[contains(text(), 'Accept all')]/ancestor::button"),
        (By.XPATH, "//button//*[contains(text(), 'I agree')]/ancestor::button"),
        (By.XPATH, "//button//*[contains(text(), 'Принять все')]/ancestor::button"),
        (By.XPATH, "//button//*[contains(text(), 'Согласиться')]/ancestor::button"),
        (By.XPATH, "//button//*[contains(text(), 'Aceptar todo')]/ancestor::button"),
    )

    def __init__(self, driver: WebDriver, timeout: int = 15) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)
        self.accept_cookies_if_present()

    def wait_visible(self, locator: Locator, timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_present(self, locator: Locator, timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator: Locator, timeout: int | None = None) -> WebElement:
        return WebDriverWait(self.driver, timeout or self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator: Locator, timeout: int | None = None) -> None:
        self.wait_clickable(locator, timeout).click()

    def type_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        element = self.wait_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.driver.find_elements(*locator)

    def current_url(self) -> str:
        return self.driver.current_url

    def title(self) -> str:
        return self.driver.title

    def accept_cookies_if_present(self) -> None:
        """Закрывает окно согласия YouTube/Google, если оно появилось."""
        for locator in self.CONSENT_BUTTONS:
            try:
                button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(locator))
                button.click()
                return
            except (TimeoutException, WebDriverException):
                continue

    def is_element_visible(self, locator: Locator, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
