import re

from pages.category_page import CategoryPage
from pages.product_page import ProductPage


def test_category_all_cards_valid(page):
    """Перевіряє, що всі картки категорії містять основні дані."""

    category_page = CategoryPage(page)
    category_page.open()

    products_count = category_page.products.count()

    assert products_count > 0, (
        "У категорії Desktops не знайдено жодної картки товару"
    )

    for index in range(products_count):
        card = category_page.card(index)
        product = category_page.get_product_info(card)
        name = product["name"]

        assert name, f"Картка №{index + 1} не містить назви товару"
        assert product["href"], f'Товар "{name}" не має посилання href'
        assert product["href"] != "#", (
            f'Посилання товару "{name}" містить заглушку "#"'
        )

        # Ціна має відповідати формату "число + Грн"
        price = product["price"]
        assert re.search(r"\d+(?:[.,]\d+)?\s*Грн", price), (
            f'Ціна товару "{name}" має неправильний формат: "{price}"'
        )

        assert category_page.card_add_button(card).is_visible(), (
            f'Кнопка "В КОШИК" не відображається для товару "{name}"'
        )


def test_two_cards_are_independent(page):
    """Перевіряє незалежність локаторів двох карток товарів."""

    category_page = CategoryPage(page)
    category_page.open()

    products_count = category_page.products.count()

    # Перевіряємо, що в категорії є щонайменше дві картки
    assert products_count >= 2, (
        "Для порівняння потрібно щонайменше 2 картки товарів, "
        f"але знайдено: {products_count}"
    )

    first_card = category_page.card(0)
    second_card = category_page.card(1)

    first_product = category_page.get_product_info(first_card)
    second_product = category_page.get_product_info(second_card)

    first_name = first_product["name"]
    second_name = second_product["name"]

    assert first_name, "Перша картка не містить назви товару"
    assert second_name, "Друга картка не містить назви товару"

    # Локатори мають читати назви саме з "своєї" картки, а не з однієї й тієї ж
    assert first_name != second_name, (
        "Назви першої та другої карток однакові. "
        f'Перша картка: "{first_name}", '
        f'друга картка: "{second_name}"'
    )

    first_href = first_product["href"]
    second_href = second_product["href"]

    assert first_href, f'Товар "{first_name}" не має посилання href'
    assert second_href, f'Товар "{second_name}" не має посилання href'
    assert first_href != second_href, (
        "Перша та друга картки мають однакові посилання. "
        f'Перша картка: "{first_href}", '
        f'друга картка: "{second_href}"'
    )

    category_page.card_link(first_card).click()

    product_page = ProductPage(page)
    product_heading = product_page.heading.inner_text().strip()

    assert product_heading, (
        f'На сторінці товару "{first_name}" відсутній заголовок H1'
    )
    assert product_heading.rstrip('"') == first_name.rstrip('"'), (
        "Відкрилася сторінка іншого товару. "
        f'Очікували: "{first_name}", '
        f'отримали в H1: "{product_heading}"'
    )


def test_add_selected_product_to_wishlist(page):
    """Перевіряє додавання конкретного товару в список бажань за його назвою.

    ПРИМІТКА: На demo.opencart.ua додавання в список бажань вимагає авторизації,
    тому неавторизований клік завершується попередженням "потрібно увійти",
    а не повідомленням про успіх. Саме це попередження і перевіряє тест.
    """

    category_page = CategoryPage(page)
    category_page.open()

    first_card = category_page.card(0)
    target_product = category_page.get_product_info(first_card)["name"]

    matched_card = category_page.card_by_text(target_product)
    matched_count = matched_card.count()

    assert matched_count == 1, (
        f"Очікували знайти одну картку товару '{target_product}', "
        f"але знайдено: {matched_count}"
    )

    product = category_page.get_product_info(matched_card)
    product_name = product["name"]

    assert product_name, f"Картка товару '{target_product}' не містить назви"
    assert target_product in product_name, (
        "Знайдена картка не відповідає потрібному товару. "
        f'Очікували: "{target_product}", '
        f'отримали: "{product_name}"'
    )

    wishlist_button = category_page.card_wishlist_button(matched_card)
    assert wishlist_button.is_visible(), (
        f'Кнопка додавання в список бажань не відображається для товару "{product_name}"'
    )

    wishlist_button.click()
    category_page.success_alert.wait_for()

    alert_text = category_page.success_alert.inner_text()
    assert "увійти" in alert_text.lower(), (
        "Без авторизації очікували попередження про необхідність увійти, "
        f'отримали: "{alert_text}"'
    )
    assert product_name in alert_text, (
        f'Попередження не згадує товар "{product_name}": "{alert_text}"'
    )
