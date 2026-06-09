# Матрица соответствия требований и тестов

| Требование | Описание | Тест-кейс | Автотест |
|---|---|---|---|
| REQ-001 | Главная страница должна открываться | TC-001 | `test_home_page_opened` |
| REQ-002 | Пользователь должен видеть строку поиска | TC-001 | `test_home_page_opened` |
| REQ-003 | Пользователь может выполнять поиск по текстовому запросу | TC-002 | `test_search_valid_query_opens_results_page` |
| REQ-004 | Сайт должен корректно обрабатывать пустой поиск | TC-003 | `test_search_empty_query_does_not_open_results_page` |
| REQ-005 | Сайт должен корректно обрабатывать спецсимволы в поиске | TC-004 | `test_search_special_characters_query` |
| REQ-006 | На странице результатов должны быть фильтры | TC-005 | `test_filter_button_visible_on_results_page` |
| REQ-007 | Пользователь может открыть видео из результатов поиска | TC-006 | `test_open_first_video_from_search_results` |
| REQ-008 | Пользователь может выполнить повторный поиск | TC-007 | `test_repeated_search_changes_query` |
| REQ-009 | Логотип должен возвращать на главную страницу | TC-008 | `test_logo_navigation_returns_to_home_page` |
