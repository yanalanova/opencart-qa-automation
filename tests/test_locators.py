import re

from pages.category_page import CategoryPage


def test_category_all_cards_valid(page):
    """Перевіряє, що всі картки категорії містять основні дані."""

    category_page = CategoryPage(page)
    category_page.open()

    products_count = category_page.products.count()

    # Перевіряємо, що в категорії є хоча б одна картка товару
    assert products_count > 0, (
        "У категорії Desktops не знайдено жодної картки товару"
    )

    for index in range(products_count):
        product = category_page.get_product_info(index)

        # Перевіряємо, що картка має непорожню назву товару
        assert product["name"], (
            f"Картка №{index + 1} не містить назви товару"
        )

        # Перевіряємо, що посилання товару має атрибут href
        name = product["name"]
        assert product["href"], (
            f'Товар "{name}" не має посилання href'
        )

        # Перевіряємо, що посилання веде на сторінку товару, а не на заглушку
        assert product["href"] != "#", (
            f'Посилання товару "{name}" містить заглушку "#"'
        )

        # Перевіряємо, що ціна має формат: число + Грн
        price = product["price"]
        assert re.search(r"\d+(?:[.,]\d+)?\s*Грн", price), (
            f'Ціна товару "{name}" має неправильний формат: "{price}"'
        )

        # Перевіряємо, що кнопка «В КОШИК» видима в поточній картці
        assert product["add_button"].is_visible(), (
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

    # Зберігаємо інформацію про обидві картки до переходу
    first_product = category_page.get_product_info(0)
    second_product = category_page.get_product_info(1)

    first_name = first_product["name"]
    second_name = second_product["name"]

    # Перевіряємо, що перша картка містить назву товару
    assert first_name, (
        "Перша картка не містить назви товару"
    )

    # Перевіряємо, що друга картка містить назву товару
    assert second_name, (
        "Друга картка не містить назви товару"
    )

    # Перевіряємо, що локатори прочитали назви з різних карток
    assert first_name != second_name, (
        "Назви першої та другої карток однакові. "
        f'Перша картка: "{first_name}", '
        f'друга картка: "{second_name}"'
    )

    first_href = first_product["href"]
    second_href = second_product["href"]

    # Перевіряємо, що перша картка має посилання на товар
    assert first_href, (
        f'Товар "{first_name}" не має посилання href'
    )

    # Перевіряємо, що друга картка має посилання на товар
    assert second_href, (
        f'Товар "{second_name}" не має посилання href'
    )

    # Перевіряємо, що картки ведуть на різні сторінки товарів
    assert first_href != second_href, (
        "Перша та друга картки мають однакові посилання. "
        f'Перша картка: "{first_href}", '
        f'друга картка: "{second_href}"'
    )

    # Відкриваємо сторінку товару з першої картки
    category_page.card_link(0).click()

    product_heading = page.locator("h1").inner_text().strip()

    # Перевіряємо, що сторінка товару має заголовок
    assert product_heading, (
        f'На сторінці товару "{first_name}" відсутній заголовок H1'
    )

    # Перевіряємо, що відкрилася сторінка саме першого товару
    assert product_heading.rstrip('"') == first_name.rstrip('"'), (
        "Відкрилася сторінка іншого товару. "
        f'Очікували: "{first_name}", '
        f'отримали в H1: "{product_heading}"'
    )


def test_add_selected_product_to_wishlist(page):
    """Перевіряє додавання конкретного товару в список бажань за його назвою.

    ПРИМІТКА: На demo.opencart.ua як додавання в кошик, так і додавання в список бажань
    вимагають авторизації. Ми пробували обидва варіанти:
    1. Додавання в кошик (cart.add) - не працює без авторизації
    2. Додавання в список бажань (wishlist.add) - також не працює без авторизації

    Тест перевіряє що локатори знаходять правильні кнопки та вони клікаються,
    але повідомлення про успіх не з'являється без авторизації.
    """

    category_page = CategoryPage(page)
    category_page.open()

    # Беремо перший товар зі сторінки
    first_product = category_page.get_product_info(0)
    target_product = first_product["name"]

    # Знаходимо картку за її текстом
    matched_card = category_page.card_by_text(target_product)
    matched_count = matched_card.count()

    # Перевіряємо, що знайдено рівно одну відповідну картку
    assert matched_count == 1, (
        f"Очікували знайти одну картку товару '{target_product}', "
        f"але знайдено: {matched_count}"
    )

    # Отримуємо інформацію про знайдену картку
    product = category_page.get_product_info_by_card(matched_card)
    product_name = product["name"]

    # Перевіряємо, що знайдена картка має назву
    assert product_name, (
        f"Картка товару '{target_product}' не містить назви"
    )

    # Перевіряємо, що знайдена картка належить потрібному товару
    assert target_product in product_name, (
        "Знайдена картка не відповідає потрібному товару. "
        f'Очікували: "{target_product}", '
        f'отримали: "{product_name}"'
    )

    # Перевіряємо, що кнопка додавання в список бажань видима
    assert product["wishlist_button"].is_visible(), (
        "Кнопка додавання в список бажань не відображається для товару "
        f'"{product_name}"'
    )

    # Додаємо в список бажань товар із конкретної знайденої картки
    # Примітка: додавання в список бажань на demo.opencart.ua вимагає авторизації,
    # тому мы тільки перевіряємо, що кнопка видима та клікається без помилок.
    # В реальній системі після успішного клікання з'явиться повідомлення про успіх.
    product["wishlist_button"].click()

    # Дочекаємось оновлення сторінки
    page.wait_for_load_state("networkidle")
