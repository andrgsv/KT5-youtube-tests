from __future__ import annotations

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class YouTubeVideoPage(BasePage):
    PLAYER = (By.CSS_SELECTOR, ".html5-video-player")
    VIDEO = (By.CSS_SELECTOR, "video")
    TITLE = (By.CSS_SELECTOR, "h1.ytd-watch-metadata, h1.title")
    PLAY_BUTTON = (By.CSS_SELECTOR, "button.ytp-play-button")

    def wait_loaded(self) -> None:
        self.wait_present(self.PLAYER, timeout=20)
        self.wait_present(self.VIDEO, timeout=20)

    def has_player(self) -> bool:
        return self.is_element_visible(self.PLAYER, timeout=20)

    def get_title_text(self) -> str:
        return self.wait_visible(self.TITLE, timeout=20).text.strip()
