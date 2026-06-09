from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class YouTubeHomePage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input#search")
    LOGO = (By.CSS_SELECTOR, "a#logo, ytd-topbar-logo-renderer a")
    MENU_BUTTON = (By.CSS_SELECTOR, "button#button[aria-label], yt-icon-button#guide-button button")

    def open_home(self, base_url: str) -> None:
        self.open(base_url)

    def is_opened(self) -> bool:
        return self.is_element_visible(self.SEARCH_INPUT) and self.is_element_visible(self.LOGO)

    def search(self, query: str) -> None:
        self.wait_visible(self.SEARCH_INPUT)
        self.type_text(self.SEARCH_INPUT, query)
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)

    def get_search_placeholder(self) -> str:
        return self.wait_visible(self.SEARCH_INPUT).get_attribute("placeholder") or ""

    def click_logo(self) -> None:
        self.click(self.LOGO)
