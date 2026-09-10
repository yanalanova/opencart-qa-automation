import re

from config import BASE_URL
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


PRICE_RE = re.compile(r"\d+(?:[.,]\d+)?\s*Грн")


def test_home_featured_cards_are_consistent(page):
    home = HomePage(page)
    home.open()

    cards_count = home.featured_cards.count()

    assert cards_count > 0, "Featured section has no product cards"

    for index in range(cards_count):
        name = home.card_link(index).inner_text().strip()
        price = home.card_price(index).inner_text().strip()
        href = home.card_link(index).get_attribute("href")
        add_button = home.card_add_button(index)

        assert name, f"Card {index}: product name is empty"
        assert PRICE_RE.search(price), f"Card {index}: invalid price format: {price!r}"
        assert href, f"Card {index}: product link has no href"
        assert add_button.is_visible(), f"Card {index} ({name}): Add to Cart button is hidden"


def test_card_opens_matching_product(page):
    home = HomePage(page)
    home.open()

    expected_name = home.card_link(0).inner_text().strip()

    home.open_product(0)

    product = ProductPage(page)
    actual_heading = product.heading.inner_text()

    assert expected_name in actual_heading, "Opened product does not match selected card"
    assert page.url.rstrip("/") != BASE_URL.rstrip("/"), "URL stayed on the home page"

    page.go_back()

    assert page.url.rstrip("/") == BASE_URL.rstrip("/"), "Back did not return to home page"
    assert home.featured_cards.count() > 0, "Featured products are missing after Back"


def test_home_to_cart_journey(page):
    home = HomePage(page)
    home.open()

    expected_name = home.card_link(0).inner_text().strip()
    count_before = home.cart_count()

    home.add_card_to_cart(0)
    home.success_alert.wait_for()
    home.wait_for_cart_update(count_before)

    count_after = home.cart_count()

    assert home.success_alert.is_visible(), "Success message is not visible"
    assert count_after == count_before + 1, "Cart product count was not updated"

    cart = CartPage(page)
    cart.open()

    assert "checkout/cart" in page.url, f"Unexpected cart URL: {page.url}"
    assert "Кошик" in cart.heading.inner_text(), "Cart page heading is missing"
    assert any(expected_name in item for item in cart.item_names()), (
        f"{expected_name!r} is not present in the cart"
    )