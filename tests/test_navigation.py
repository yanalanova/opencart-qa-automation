from urllib.parse import urlparse

import pytest

from pages.category_page import CategoryPage
from pages.home_page import HomePage


@pytest.mark.parametrize(
    "menu_name, expected_route, expected_heading",
    [
        ("Настільні комп'ютери", "/desktops", "Настільні комп'ютери"),
        ("Нетбуки та Ноутбуки", "/laptop-notebook", "Нетбуки та Ноутбуки"),
    ],
)
def test_main_category_navigation(
    page,
    menu_name,
    expected_route,
    expected_heading,
):
    """Перевіряє навігацію на сторінки головних категорій."""

    home = HomePage(page)
    home.open()
    home.open_category(menu_name)

    category = CategoryPage(page)

    heading_text = category.heading.inner_text().strip()
    breadcrumb_text = category.breadcrumb.inner_text()
    home_href = category.breadcrumb_home.get_attribute("href")

    assert heading_text == expected_heading, (
        f"Expected heading {expected_heading!r}, got {heading_text!r}"
    )
    assert expected_route in page.url, (
        f"Expected route {expected_route!r} in URL, got {page.url!r}"
    )
    assert home_href, "Home breadcrumb has no href"
    assert "route=common/home" in home_href, f"Unexpected Home href: {home_href!r}"
    assert expected_heading in breadcrumb_text, (
        f"{expected_heading!r} is missing in breadcrumb: {breadcrumb_text!r}"
    )
    assert category.products.count() > 0, (
        f"Category {expected_heading!r} has no products"
    )


@pytest.mark.parametrize(
    "link_name, expected_route, expected_title, open_account_menu",
    [
        ("register_link", "account/register", "Зареєструватися", True),
        ("login_link", "account/login", "Авторизація", True),
        ("wishlist_link", "account/login", "Авторизація", False),
        ("cart_link", "checkout/cart", "Кошик", False),
    ],
    ids=["register", "login", "wishlist", "cart"],
)
def test_header_navigation(
    page,
    link_name,
    expected_route,
    expected_title,
    open_account_menu,
):
    """Перевіряє навігацію через основні посилання в header."""

    home = HomePage(page)
    home.open()

    home_url = page.url

    if open_account_menu:
        home.account_menu.click()

    link = getattr(home, link_name)
    href = link.get_attribute("href")

    assert href, f"{link_name} has no href"
    assert href != "#", f"{link_name} has placeholder href '#'"
    assert not href.startswith("javascript:"), (
        f"{link_name} uses JavaScript href: {href!r}"
    )

    link.click()

    assert expected_route in page.url, (
        f"Expected route {expected_route!r} in URL, got {page.url!r}"
    )
    assert page.title() == expected_title, (
        f"Expected title {expected_title!r}, got {page.title()!r}"
    )

    page.go_back()

    assert page.url == home_url, (
        f"Expected to return to {home_url!r}, got {page.url!r}"
    )


def test_multilevel_category_navigation(page):
    """Перевіряє навігацію в підкатегорію та повернення через breadcrumb."""

    home = HomePage(page)
    home.open()
    home.open_category("Настільні комп'ютери")

    category = CategoryPage(page)

    mac_link = category.subcategory_link("Mac")
    mac_href = mac_link.get_attribute("href")

    assert mac_href, "Mac subcategory has no href"

    expected_subcategory_route = urlparse(mac_href).path

    category.open_subcategory("Mac")

    heading_text = category.heading.inner_text().strip()
    breadcrumb_text = category.breadcrumb.inner_text()

    assert heading_text == "Mac", f"Expected heading 'Mac', got {heading_text!r}"
    assert expected_subcategory_route in page.url, (
        f"Expected route {expected_subcategory_route!r} in URL, got {page.url!r}"
    )
    assert "Настільні комп'ютери" in breadcrumb_text, (
        f"Parent category is missing in breadcrumb: {breadcrumb_text!r}"
    )
    assert "Mac" in breadcrumb_text, (
        f"'Mac' is missing in breadcrumb: {breadcrumb_text!r}"
    )
    assert breadcrumb_text.index("Настільні комп'ютери") < breadcrumb_text.index("Mac"), (
        f"Wrong breadcrumb order: {breadcrumb_text!r}"
    )

    category.click_breadcrumb("Настільні комп'ютери")

    parent_heading = category.heading.inner_text().strip()
    parent_breadcrumb = category.breadcrumb.inner_text()

    assert parent_heading == "Настільні комп'ютери", (
        f"Expected parent heading 'Настільні комп'ютери', got {parent_heading!r}"
    )
    assert "/desktops" in page.url, f"Expected '/desktops' in URL, got {page.url!r}"
    assert "Mac" not in parent_breadcrumb, (
        f"'Mac' should not be in parent breadcrumb: {parent_breadcrumb!r}"
    )