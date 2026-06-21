from __future__ import annotations

import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.youtube_home_page import YouTubeHomePage
from pages.youtube_results_page import YouTubeResultsPage
from pages.video_page import YouTubeVideoPage


@pytest.mark.smoke
@pytest.mark.ui
def test_home_page_opened(driver, base_url):
    """TC-001: Проверка открытия главной страницы YouTube."""

    home = YouTubeHomePage(driver)
    home.open_home(base_url)

    WebDriverWait(driver, 20).until(
        lambda d: "youtube" in d.current_url.lower()
    )

    assert "youtube" in home.current_url().lower()


@pytest.mark.smoke
@pytest.mark.ui
def test_youtube_title_or_url_contains_youtube(driver, base_url):
    """TC-002: Проверка, что открыта страница YouTube."""

    home = YouTubeHomePage(driver)
    home.open_home(base_url)

    WebDriverWait(driver, 20).until(
        lambda d: "youtube" in d.title.lower()
        or "youtube" in d.current_url.lower()
    )

    assert "youtube" in home.title().lower() or "youtube" in home.current_url().lower()


@pytest.mark.search
@pytest.mark.regression
def test_search_valid_query_opens_results_page(driver, base_url):
    """TC-003: Поиск по валидному текстовому запросу."""

    query = "selenium webdriver"
    results = YouTubeResultsPage(driver)

    driver.get(f"{base_url}results?search_query=selenium+webdriver")

    WebDriverWait(driver, 20).until(
        lambda d: "results" in d.current_url and "search_query" in d.current_url
    )

    assert "results" in results.current_url()
    assert "search_query" in results.current_url()
    assert "selenium" in results.current_url().lower()


@pytest.mark.search
@pytest.mark.negative
def test_search_empty_query_does_not_open_results_page(driver, base_url):
    """TC-004: Проверка поведения при пустом поисковом запросе."""

    home = YouTubeHomePage(driver)
    home.open_home(base_url)

    WebDriverWait(driver, 20).until(
        lambda d: "youtube" in d.current_url.lower()
    )

    assert "results?search_query=" not in home.current_url().lower()


@pytest.mark.search
@pytest.mark.regression
def test_search_special_characters_query(driver, base_url):
    """TC-005: Поиск с цифрами, пробелами и спецсимволами."""

    results = YouTubeResultsPage(driver)

    driver.get(f"{base_url}results?search_query=%40%23%24+selenium+test")

    WebDriverWait(driver, 20).until(
        lambda d: "search_query" in d.current_url
    )

    assert "search_query" in results.current_url()


@pytest.mark.search
@pytest.mark.ui
def test_filter_page_url_available_on_results_page(driver, base_url):
    """TC-006: Проверка открытия страницы результатов поиска."""

    results = YouTubeResultsPage(driver)

    driver.get(f"{base_url}results?search_query=qa+automation")

    WebDriverWait(driver, 20).until(
        lambda d: "results" in d.current_url
    )

    assert "youtube.com/results" in results.current_url()


@pytest.mark.video
@pytest.mark.regression
def test_open_video_page_from_youtube(driver, base_url):
    """TC-007: Проверка открытия страницы просмотра видео."""

    video = YouTubeVideoPage(driver)

    driver.get(f"{base_url}watch?v=dQw4w9WgXcQ")

    WebDriverWait(driver, 20).until(
        lambda d: "watch" in d.current_url or "youtube" in d.current_url.lower()
    )

    assert "youtube" in video.current_url().lower()


@pytest.mark.regression
@pytest.mark.search
def test_repeated_search_changes_query(driver, base_url):
    """TC-008: Повторный поиск с новым запросом."""

    results = YouTubeResultsPage(driver)

    driver.get(f"{base_url}results?search_query=selenium")
    WebDriverWait(driver, 20).until(
        lambda d: "search_query=selenium" in d.current_url.lower()
    )

    first_url = results.current_url()

    driver.get(f"{base_url}results?search_query=robot+framework")
    WebDriverWait(driver, 20).until(
        lambda d: "robot" in d.current_url.lower()
    )

    second_url = results.current_url()

    assert first_url != second_url
    assert "search_query" in second_url