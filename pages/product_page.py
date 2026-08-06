from pages.base_page import BasePage


class ProductPage(BasePage):
    # Reached by clicking a product card, so there is no PATH to open directly.

    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("h1")
        self.add_to_cart_button = page.locator("#button-cart")
        self.quantity_input = page.locator("#input-quantity")
        self.success_alert = page.locator(".alert-success")

    def add_to_cart(self):
        self.add_to_cart_button.click()
