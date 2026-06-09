# КТ №5. Тестирование функционала сайта YouTube

Учебный проект по предмету **«Модульное тестирование веб-приложений»**.

Сайт для тестирования: **https://www.youtube.com/**  
Тип сайта: видеохостинг / медиаплатформа.

## Структура проекта

```text
youtube_selenium_tests/
├── docs/                    # тестовая документация
│   ├── checklist.md
│   ├── jira_cards.md
│   ├── test_cases.md
│   ├── test_data.md
│   ├── test_plan.md
│   ├── test_report.md
│   └── traceability_matrix.md
├── pages/                   # Page Object Model
│   ├── __init__.py
│   ├── base_page.py
│   ├── video_page.py
│   ├── youtube_home_page.py
│   └── youtube_results_page.py
├── tests/                   # автотесты pytest
│   └── test_youtube_functional.py
├── conftest.py              # фикстуры pytest и настройки браузера
├── pytest.ini               # конфигурация pytest
├── requirements.txt         # зависимости
├── .gitignore
└── README.md
```

В архиве только **3 основные папки**, как в примере: `docs`, `pages`, `tests`.

## Что проверяется

- открытие главной страницы YouTube;
- наличие логотипа и строки поиска;
- поиск по валидному запросу;
- поиск с пустым запросом;
- поиск со спецсимволами;
- отображение фильтров результатов;
- открытие первого видео из результатов поиска;
- повторный поиск;
- переход на главную страницу через логотип.

## Установка

1. Установить Python 3.10 или выше.
2. Установить Google Chrome.
3. Открыть папку проекта:

```bash
cd youtube_selenium_tests
```

4. Создать виртуальное окружение:

```bash
python -m venv .venv
```

5. Активировать виртуальное окружение.

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

6. Установить зависимости:

```bash
pip install -r requirements.txt
```

## Запуск тестов

Запуск всех тестов:

```bash
pytest
```

Запуск smoke-тестов:

```bash
pytest -m smoke
```

Запуск тестов поиска:

```bash
pytest -m search
```

Запуск в headless-режиме:

```bash
pytest --headless
```

Запуск с HTML-отчетом:

```bash
pytest --html=artifacts/report.html --self-contained-html
```

Папка `artifacts` создается автоматически во время запуска и не хранится в архиве.

## Тестовая документация

Документы для сдачи находятся в папке `docs`:

- `test_plan.md` — тест-план;
- `test_cases.md` — тест-кейсы;
- `checklist.md` — чек-лист;
- `test_data.md` — тестовые данные;
- `test_report.md` — отчет о тестировании;
- `jira_cards.md` — примеры карточек дефектов для Jira / YouGile;
- `traceability_matrix.md` — матрица соответствия требований и тестов.
- 
