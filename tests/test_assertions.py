import re

from pages.product_page import ProductPage
from urllib.parse import urlparse
from pages.category_page import CategoryPage


PRICE_RE = re.compile(r"\d+(?:[.,]\d+)?\s*Грн")


def test_product_page_structural_contract(page):
    """Перевіряє основну структуру сторінки товару."""

    product_page = ProductPage(page)
    product_page.open()

    # Зчитуємо дані зі сторінки
    product_name = product_page.heading.inner_text().strip()
    price_text = product_page.price.inner_text().strip()
    quantity_value = product_page.quantity_input.input_value().strip()

    tabs_count = product_page.tabs.count()
    tab_labels = [
        product_page.tabs.nth(index).inner_text().strip()
        for index in range(tabs_count)
    ]

    # Перевіряємо, що назва товару не порожня
    assert product_name, (
        "Назва товару порожня: елемент h1 не містить тексту"
    )

    # Перевіряємо, що ціна має правильний формат
    assert PRICE_RE.search(price_text), (
        f"Ціна має неправильний формат: отримано {price_text!r}"
    )

    # Перевіряємо, що поле кількості має значення
    assert quantity_value, (
        "Поле кількості товару не має початкового значення"
    )

    # Перевіряємо, що кількість є цілим числом
    assert quantity_value.isdigit(), (
        f"Кількість товару повинна бути цілим числом: "
        f"отримано {quantity_value!r}"
    )

    # Перевіряємо, що початкова кількість товару не менша за 1
    assert int(quantity_value) >= 1, (
        f"Початкова кількість товару повинна бути не меншою за 1: "
        f"отримано {quantity_value!r}"
    )

    # Перевіряємо, що кнопка додавання в кошик активна
    assert product_page.add_to_cart_button.is_enabled(), (
        "Кнопка додавання товару в кошик неактивна"
    )

    # Перевіряємо, що на сторінці є рівно три вкладки
    assert len(tab_labels) == 3, (
        f"Очікували 3 вкладки, але отримали {len(tab_labels)}: "
        f"{tab_labels}"
    )

    # Перевіряємо, що вкладки не дублюються
    assert len(set(tab_labels)) == len(tab_labels), (
        f"На сторінці знайдено дублікати вкладок: {tab_labels}"
    )

    # Перевіряємо наявність вкладки «Опис»
    assert any("Опис" in label for label in tab_labels), (
        f"Не знайдено вкладку «Опис». Отримані вкладки: {tab_labels}"
    )

    # Перевіряємо наявність вкладки «Специфікація»
    assert any("Специфікація" in label for label in tab_labels), (
        f"Не знайдено вкладку «Специфікація». "
        f"Отримані вкладки: {tab_labels}"
    )

    # Перевіряємо наявність вкладки «Відгуки»
    assert any("Відгуки" in label for label in tab_labels), (
        f"Не знайдено вкладку «Відгуки». Отримані вкладки: {tab_labels}"
    )
    

def test_product_data_consistency_between_pages(page):
    """Перевіряє відповідність даних картки сторінці товару."""

    category_page = CategoryPage(page)
    category_page.open()

    # Отримуємо локатори назви та ціни першої картки
    first_card = category_page.card(0)
    name_link = category_page.card_link(first_card)
    price = category_page.card_price(first_card)

    # Зчитуємо дані картки до переходу на сторінку товару
    card_name = name_link.inner_text().strip()
    card_price = price.inner_text().strip()
    product_href = name_link.get_attribute("href")

    # Перевіряємо, що картка має посилання на товар
    assert product_href, (
        f"Картка товару {card_name!r} не містить посилання href"
    )

    # Відкриваємо сторінку вибраного товару
    name_link.click()

    product_page = ProductPage(page)

    # Зчитуємо дані зі сторінки товару
    product_page_name = product_page.heading.inner_text().strip()
    product_page_price = product_page.price.inner_text().strip()

    # Перевіряємо, що відкрилася сторінка того самого товару
    assert product_page_name == card_name, (
        f"Назва товару не збігається: у картці {card_name!r}, "
        f"на сторінці товару {product_page_name!r}"
    )

    # Перевіряємо формат ціни у картці товару
    assert PRICE_RE.search(card_price), (
        f"Ціна у картці має неправильний формат: {card_price!r}"
    )

    # Перевіряємо формат ціни на сторінці товару
    assert PRICE_RE.search(product_page_price), (
        f"Ціна на сторінці товару має неправильний формат: "
        f"{product_page_price!r}"
    )

    # Отримуємо шлях із посилання картки та поточного URL
    expected_path = urlparse(product_href).path
    actual_path = urlparse(page.url).path

    # Перевіряємо, що відкрилася сторінка за посиланням із картки
    assert actual_path == expected_path, (
        f"Відкрився неправильний URL: очікували шлях "
        f"{expected_path!r}, отримали {actual_path!r}. "
        f"Повний URL сторінки: {page.url!r}"
    )