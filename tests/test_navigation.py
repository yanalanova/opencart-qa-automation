from urllib.parse import urlparse

import pytest

from pages.category_page import CategoryPage
from pages.home_page import HomePage


@pytest.mark.parametrize(
    "menu_name, expected_route, expected_heading",
    [
        (
            "Настільні комп'ютери",
            "/desktops",
            "Настільні комп'ютери",
        ),
        (
            "Нетбуки та Ноутбуки",
            "/laptop-notebook",
            "Нетбуки та Ноутбуки",
        ),
    ],
)
def test_main_category_navigation(
    page,
    menu_name,
    expected_route,
    expected_heading,
):
    """Перевіряє навігацію на сторінки головних категорій."""

    # Відкриваємо головну сторінку
    home = HomePage(page)
    home.open()

    # Відкриваємо сторінку "Переглянути всі" для вибраної категорії
    home.open_category(menu_name)

    # Створюємо об'єкт CategoryPage
    category = CategoryPage(page)

    # Зчитуємо дані зі сторінки категорії
    heading_text = category.heading.inner_text().strip()
    breadcrumb_text = category.breadcrumb.inner_text()
    home_href = category.breadcrumb_home.get_attribute("href")

    # Перевіряємо, що відкрилася правильна сторінка категорії
    assert heading_text == expected_heading
    assert expected_route in page.url

    # Перевіряємо breadcrumb
    assert home_href
    assert "route=common/home" in home_href
    assert expected_heading in breadcrumb_text

    # Перевіряємо, що в категорії є товари
    assert category.products.count() > 0


def test_header_navigation(page):
    """Перевіряє навігацію через основні посилання в header."""

    # Відкриваємо головну сторінку
    home = HomePage(page)
    home.open()

    # Зберігаємо URL головної сторінки
    home_url = page.url

    # Посилання, очікуваний маршрут і title сторінки
    header_links = [
        (
            home.register_link,
            "account/register",
            "Зареєструватися",
        ),
        (
            home.login_link,
            "account/login",
            "Авторизація",
        ),
        (
            home.wishlist_link,
            "account/login",
            "Авторизація",
        ),
        (
            home.cart_link,
            "checkout/cart",
            "Кошик",
        ),
    ]

    for link, expected_route, expected_title in header_links:

        # Для Реєстрації та Входу відкриваємо dropdown "Обліковий запис"
        if link == home.register_link or link == home.login_link:
            home.account_menu.click()

        # Зчитуємо href перед переходом
        href = link.get_attribute("href")

        # Перевіряємо, що посилання існує і не є placeholder
        assert href
        assert href != "#"
        assert not href.startswith("javascript:")

        # Переходимо за посиланням
        link.click()

        # Перевіряємо маршрут і title сторінки
        assert expected_route in page.url
        assert page.title() == expected_title

        # Повертаємося на головну сторінку
        page.go_back()

        # Перевіряємо, що повернулися назад
        assert page.url == home_url


def test_multilevel_category_navigation(page):
    """Перевіряє перехід у підкатегорію та повернення до батьківської категорії через breadcrumb."""

    # Відкриваємо головну сторінку
    home = HomePage(page)
    home.open()

    # Відкриваємо головну категорію
    home.open_category("Настільні комп'ютери")

    category = CategoryPage(page)

    # Знаходимо підкатегорію Mac та зчитуємо її href
    mac_link = category.subcategory_link("Mac")
    mac_href = mac_link.get_attribute("href")

    assert mac_href

    # Отримуємо очікуваний route з реального href
    expected_subcategory_route = urlparse(mac_href).path

    # Відкриваємо підкатегорію Mac
    category.open_subcategory("Mac")

    # Зчитуємо дані сторінки підкатегорії
    heading_text = category.heading.inner_text().strip()
    breadcrumb_text = category.breadcrumb.inner_text()

    # Перевіряємо, що відкрилася правильна підкатегорія
    assert heading_text == "Mac"
    assert expected_subcategory_route in page.url

    # Перевіряємо ієрархію breadcrumb
    assert "Настільні комп'ютери" in breadcrumb_text
    assert "Mac" in breadcrumb_text

    # Перевіряємо правильний порядок:
    # Настільні комп'ютери -> Mac
    assert breadcrumb_text.index(
        "Настільні комп'ютери"
    ) < breadcrumb_text.index("Mac")

    # Повертаємося до батьківської категорії через breadcrumb
    category.click_breadcrumb("Настільні комп'ютери")

    # Зчитуємо дані батьківської сторінки
    parent_heading = category.heading.inner_text().strip()
    parent_breadcrumb = category.breadcrumb.inner_text()

    # Перевіряємо, що повернулися до батьківської категорії
    assert parent_heading == "Настільні комп'ютери"
    assert "/desktops" in page.url

    # Перевіряємо, що підкатегорії Mac більше немає в breadcrumb
    assert "Mac" not in parent_breadcrumb