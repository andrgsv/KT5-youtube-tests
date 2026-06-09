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

    assert "youtube" in home.current_url().lower()
    assert "youtube" in home.title().lower()
    assert home.is_opened(), "На главной странице должен отображаться логотип и поле поиска"


@pytest.mark.smoke
@pytest.mark.search
def test_search_valid_query_opens_results_page(driver, base_url):
    """TC-002: Поиск по валидному текстовому запросу."""
    query = "selenium python"
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)

    home.open_home(base_url)
    home.search(query)
    results.wait_loaded()

    assert "results" in results.current_url()
    assert results.get_query_from_url().lower() == query
    assert results.has_video_results(), "По валидному запросу должны отображаться результаты поиска"


@pytest.mark.search
@pytest.mark.ui
def test_search_empty_query_does_not_open_results_page(driver, base_url):
    """TC-003: Проверка поведения поиска при пустом запросе."""
    home = YouTubeHomePage(driver)

    home.open_home(base_url)
    home.search("")

    WebDriverWait(driver, 5).until(lambda d: "youtube" in d.current_url.lower())

    assert "results?search_query=" not in home.current_url()
    assert home.is_opened(), "При пустом поиске пользователь должен остаться на странице с доступным поиском"


@pytest.mark.search
@pytest.mark.regression
def test_search_special_characters_query(driver, base_url):
    """TC-004: Поиск с цифрами, пробелами и спецсимволами."""
    query = "тест selenium 123 !@#"
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)

    home.open_home(base_url)
    home.search(query)
    results.wait_loaded()

    assert "results" in results.current_url()
    assert results.get_query_from_url() != ""
    assert results.has_video_results(), "Поиск не должен ломаться при вводе спецсимволов"


@pytest.mark.regression
@pytest.mark.search
def test_filter_button_visible_on_results_page(driver, base_url):
    """TC-005: Проверка отображения кнопки фильтров на странице результатов."""
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)

    home.open_home(base_url)
    home.search("qa automation")
    results.wait_loaded()

    assert results.is_filter_button_visible(), "На странице результатов должна быть доступна кнопка фильтров"


@pytest.mark.video
@pytest.mark.regression
def test_open_first_video_from_search_results(driver, base_url):
    """TC-006: Открытие первого видео из результатов поиска."""
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)
    video = YouTubeVideoPage(driver)

    home.open_home(base_url)
    home.search("python selenium tutorial")
    results.wait_loaded()
    assert results.has_video_results(), "Для открытия видео должны быть результаты поиска"

    results.open_first_video()
    video.wait_loaded()

    assert "watch" in video.current_url(), "После клика должен открыться URL страницы просмотра"
    assert video.has_player(), "На странице просмотра должен отображаться видеоплеер"


@pytest.mark.regression
@pytest.mark.search
def test_repeated_search_changes_query(driver, base_url):
    """TC-007: Повторный поиск с новым запросом."""
    first_query = "manual testing"
    second_query = "automation testing"
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)

    home.open_home(base_url)
    home.search(first_query)
    results.wait_loaded()
    assert results.get_query_from_url().lower() == first_query

    results.search_again(second_query)
    results.wait_loaded()

    assert results.get_query_from_url().lower() == second_query


@pytest.mark.ui
@pytest.mark.regression
def test_logo_navigation_returns_to_home_page(driver, base_url):
    """TC-008: Переход на главную страницу по клику на логотип YouTube."""
    home = YouTubeHomePage(driver)
    results = YouTubeResultsPage(driver)

    home.open_home(base_url)
    home.search("web testing")
    results.wait_loaded()
    assert "results" in results.current_url()

    results.click_logo()
    WebDriverWait(driver, 10).until(lambda d: d.current_url.rstrip("/") == base_url.rstrip("/"))

    assert home.is_opened(), "После клика на логотип должна открываться главная страница"
