import re

from config import BASE_URL
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.product_page import ProductPage

# Prices render as "500 Грн"; validate the FORMAT, never the amount.
PRICE_RE = re.compile(r"\d+(?:[.,]\d+)?\s*Грн")


def test_home_featured_cards_are_consistent(page):
    home = HomePage(page)
    home.open()

    count = home.featured_cards.count()
    assert count > 0, "Featured section renders no product cards"

    for i in range(count):
        name = home.card_link(i).inner_text().strip()
        price = home.card_price(i).inner_text().strip()
        href = home.card_link(i).get_attribute("href")

        assert name, f"card {i}: product name is empty"
        assert PRICE_RE.search(
            price
        ), f"card {i}: price {price!r} has an invalid format"
        assert href, f"card {i}: product link has no href"
        assert home.card_add_button(
            i
        ).is_visible(), f"card {i} ({name}): add-to-cart control is not visible"


def test_card_opens_matching_product(page):
    home = HomePage(page)
    home.open()

    # Remember the name while still on the home page — it is read, not hardcoded.
    expected_name = home.card_link(0).inner_text().strip()

    home.open_product(0)

    product = ProductPage(page)
    assert (
        expected_name in product.heading.inner_text()
    ), f"opened product heading does not match the card name {expected_name!r}"
    assert page.url.rstrip("/") != BASE_URL.rstrip("/"), "URL stayed on the home page"

    page.go_back()

    assert page.url.rstrip("/") == BASE_URL.rstrip("/"), "Back did not return home"
    assert home.featured_cards.count() > 0, "Featured block is missing after Back"


def test_home_to_cart_journey(page):
    home = HomePage(page)
    home.open()

    # The first featured product has no required options, so it adds in one click.
    expected_name = home.card_link(0).inner_text().strip()
    count_before = home.cart_count()

    home.add_card_to_cart(0)
    home.success_alert.wait_for()
    home.wait_for_cart_update(count_before)

    assert home.success_alert.is_visible(), "no success message after adding to cart"
    assert (
        home.cart_count() == count_before + 1
    ), f"cart badge did not go from {count_before} to {count_before + 1}"

    cart = CartPage(page)
    cart.open()

    assert "checkout/cart" in page.url, f"unexpected cart URL: {page.url}"
    assert "Кошик" in cart.heading.inner_text(), "cart page title is missing"
    assert any(
        expected_name in item for item in cart.item_names()
    ), f"{expected_name!r} is not listed in the cart"
