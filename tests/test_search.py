from urllib.parse import parse_qs, urlparse

import pytest

from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.search_results_page import NO_RESULTS_TEXT, SearchResultsPage


def test_search_results_are_relevant(page):
    """Перевіряє результати пошуку та відкриття вибраного товару."""
    term = "iPhone"

    home = HomePage(page)
    home.open()
    home.search(term)

    # Чекаємо переходу на сторінку пошуку
    page.wait_for_url("**/index.php?route=product/search&**")

    query = parse_qs(urlparse(page.url).query)

    # Перевіряємо маршрут сторінки пошуку
    assert query.get("route") == ["product/search"], (
        f"Неправильний маршрут пошуку: {page.url}"
    )

    # Перевіряємо переданий пошуковий запит
    assert query.get("search") == [term], (
        f"Пошуковий запит у URL не відповідає '{term}': {page.url}"
    )

    results = SearchResultsPage(page)
    names = results.card_names()

    # Перевіряємо, що знайдено хоча б один товар
    assert len(names) > 0, f"За запитом '{term}' не знайдено товарів"

    # Перевіряємо відповідність кожного товару запиту
    for name in names:
        assert term.lower() in name.lower(), (
            f"Товар '{name}' не відповідає запиту '{term}'"
        )

    # Зберігаємо назву першого товару та відкриваємо його
    selected_link = results.card_link(0)
    selected_name = selected_link.inner_text().strip()
    selected_link.click()

    product = ProductPage(page)
    actual_name = product.heading.inner_text().strip()

    # Перевіряємо, що відкрився саме вибраний товар
    assert actual_name == selected_name, (
        f"Очікували товар '{selected_name}', "
        f"але відкрився '{actual_name}'"
    )


@pytest.mark.parametrize(
    "initial_term, term",
    [
        pytest.param(None, "qwertyzzz", id="nonsense"),
        pytest.param(None, "", id="empty"),
        pytest.param("iPhone", "qwertyzzz", id="clear_previous_results"),
    ],
)
def test_search_no_results(page, initial_term, term):
    """Перевіряє пошук без результатів і зникнення попередніх карток."""
    home = HomePage(page)
    home.open()

    results = SearchResultsPage(page)

    # За потреби спочатку виконуємо успішний пошук
    if initial_term is not None:
        home.search(initial_term)
        results.product_cards.first.wait_for(state="visible")

        # Підтверджуємо, що до невдалого пошуку товари були
        names = results.card_names()
        assert len(names) > 0
        assert any(
            initial_term.lower() in name.lower()
            for name in names
        ), f"Не знайдено товару за початковим запитом '{initial_term}'"

    # Виконуємо пошук, який не повинен повернути товари
    home.search(term)

    message = results.no_results_message
    message.wait_for(state="visible")

    # Перевіряємо відсутність усіх карток, включно з попередніми
    assert results.product_cards.count() == 0

    # Перевіряємо точний текст повідомлення
    assert message.inner_text().strip() == NO_RESULTS_TEXT


@pytest.mark.parametrize(
    "term, expected_text",
    [
        pytest.param("iPhone", "iphone", id="exact_name"),
        pytest.param("phone", "phone", id="partial_name"),
        pytest.param("IPHONE", "iphone", id="uppercase"),
    ],
)
def test_search_matrix(page, term, expected_text):
    """Перевіряє релевантність результатів для різних варіантів запиту."""
    home = HomePage(page)
    home.open()
    home.search(term)

    results = SearchResultsPage(page)
    results.product_cards.first.wait_for(state="visible")
    names = results.card_names()

    # Перевіряємо наявність результатів
    assert len(names) > 0, f"За запитом '{term}' не знайдено товарів"

    # Перевіряємо відповідність хоча б однієї назви очікуванню
    assert any(
        expected_text.lower() in name.lower()
        for name in names
    ), f"Серед товарів немає назви з текстом '{expected_text}'"