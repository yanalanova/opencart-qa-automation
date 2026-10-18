from pages.base_page import BasePage


class ProductPage(BasePage):
    PATH = "desktops/test"

    def __init__(self, page):
        super().__init__(page)

        self.heading = page.locator("h1")
        self.price = page.locator("ul.list-unstyled h2")
        self.quantity_input = page.locator("#input-quantity")
        self.add_to_cart_button = page.locator("#button-cart")
        self.tabs = page.locator("ul.nav-tabs > li")
        self.success_alert = page.locator(".alert-success")

    def open(self):
        super().open(self.PATH)

    def add_to_cart(self):
        self.add_to_cart_button.click()
