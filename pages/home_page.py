import re

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = ""  # store root

    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("input[name='search']")
        self.featured_cards = page.locator("#content .product-thumb")
        self.success_alert = page.locator(".alert-success")
        self.cart_total = page.locator("#cart-total")

    def open(self):
        super().open(self.PATH)

    def card(self, index):
        return self.featured_cards.nth(index)

    def card_link(self, index):
        return self.card(index).locator("h4 a")

    def card_price(self, index):
        return self.card(index).locator("p.price")

    def card_add_button(self, index):
        # The label span is hidden below the lg breakpoint, so the cart.add()
        # handler is the stable hook for this button.
        return self.card(index).locator("button[onclick^='cart.add']")

    def open_product(self, index):
        self.card_link(index).click()

    def add_card_to_cart(self, index):
        self.card_add_button(index).click()

    def cart_count(self):
        # "0 товар(ів) - 0 Грн" -> 0, "1 товар(ри) - 500 Грн" -> 1
        match = re.search(r"\d+", self.cart_total.inner_text())
        return int(match.group()) if match else 0

    def wait_for_cart_update(self, previous_count):
        # The success alert renders before the header badge is refreshed, so the
        # alert alone is not a reliable signal that the cart has been updated.
        self.page.wait_for_function(
            r"""previous => {
                const total = document.querySelector('#cart-total');
                if (!total) return false;
                const match = total.textContent.match(/\d+/);
                return match !== null && Number(match[0]) !== previous;
            }""",
            arg=previous_count,
        )
