from __future__ import annotations

from urllib.parse import parse_qs, urlparse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class YouTubeResultsPage(BasePage):
    SEARCH_INPUT = (By.CSS_SELECTOR, "input#search")
    VIDEO_ITEMS = (By.CSS_SELECTOR, "ytd-video-renderer, ytd-rich-item-renderer")
    VIDEO_TITLE_LINKS = (By.CSS_SELECTOR, "ytd-video-renderer a#video-title, a#video-title")
    FILTER_BUTTON = (
        By.XPATH,
        "//button[contains(@aria-label,'Search filters') or contains(@aria-label,'Фильтры')]"
        " | //button//yt-formatted-string[contains(., 'Filters') or contains(., 'Фильтры')]/ancestor::button",
    )
    LOGO = (By.CSS_SELECTOR, "a#logo, ytd-topbar-logo-renderer a")

    def wait_loaded(self) -> None:
        self.wait_visible(self.SEARCH_INPUT)

    def get_query_from_url(self) -> str:
        parsed = urlparse(self.current_url())
        params = parse_qs(parsed.query)
        return params.get("search_query", [""])[0]

    def has_video_results(self) -> bool:
        try:
            self.wait_present(self.VIDEO_ITEMS, timeout=20)
            return len(self.find_all(self.VIDEO_ITEMS)) > 0
        except Exception:
            return False

    def is_filter_button_visible(self) -> bool:
        return self.is_element_visible(self.FILTER_BUTTON, timeout=10)

    def open_first_video(self) -> None:
        links = self.find_all(self.VIDEO_TITLE_LINKS)
        if not links:
            self.wait_present(self.VIDEO_TITLE_LINKS, timeout=20)
            links = self.find_all(self.VIDEO_TITLE_LINKS)
        links[0].click()

    def search_again(self, query: str) -> None:
        self.type_text(self.SEARCH_INPUT, query)
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)

    def click_logo(self) -> None:
        self.click(self.LOGO)
