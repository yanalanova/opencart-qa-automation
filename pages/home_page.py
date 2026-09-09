import re

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = ""

    def __init__(self, page):
        super().__init__(page)

        # Search
        self.search_input = page.locator("input[name='search']")

        # Featured products
        self.featured_cards = page.locator("#content .product-thumb")

        # Notifications
        self.success_alert = page.locator(".alert-success")

        # Cart
        self.cart_total = page.locator("#cart-total")
        self.cart_link = page.locator("#top-links a[href*='route=checkout/cart']")

        # Header navigation
        top_links = page.locator("#top-links")

        self.account_menu = top_links.get_by_role("link", name="Обліковий запис")
        self.register_link = top_links.get_by_role("link", name="Реєстрація")
        self.login_link = top_links.get_by_role("link", name="Вхід")
        self.wishlist_link = page.locator("#wishlist-total")

    def open(self):
        """Open the home page."""
        super().open(self.PATH)

    def card(self, index):
        """Return a featured product card by index."""
        return self.featured_cards.nth(index)

    def card_link(self, index):
        """Return the product link from a card."""
        return self.card(index).locator("h4 a")

    def card_price(self, index):
        """Return the product price from a card."""
        return self.card(index).locator("p.price")

    def card_add_button(self, index):
        """Return the Add to Cart button from a card."""
        return self.card(index).locator("button[onclick^='cart.add']")

    def open_product(self, index):
        """Open a product from the featured products list."""
        self.card_link(index).click()

    def add_card_to_cart(self, index):
        """Add a featured product to the cart."""
        self.card_add_button(index).click()

    def cart_count(self):
        """Return the current number of products in the cart."""
        cart_text = self.cart_total.inner_text()
        match = re.search(r"\d+", cart_text)

        return int(match.group()) if match else 0

    def wait_for_cart_update(self, previous_count):
        """Wait until the cart product count changes."""
        self.page.wait_for_function(
            """
            previousCount => {
                const cartTotal = document.querySelector("#cart-total");

                if (!cartTotal) {
                    return false;
                }

                const match = cartTotal.textContent.match(/\\d+/);

                return match !== null
                    && Number(match[0]) !== previousCount;
            }
            """,
            arg=previous_count,
        )

    def open_category(self, name):
        """Open the 'View All' page for the selected category."""
        menu = self.page.locator("#menu")

        category_link = menu.get_by_role("link", name=name, exact=True)
        category_link.hover()

        view_all_link = menu.get_by_role(
            "link",
            name=f"Переглянути всі {name}",
            exact=True,
        )
        view_all_link.click()