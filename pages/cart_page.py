from pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "index.php?route=checkout/cart"

    def __init__(self, page):
        super().__init__(page)
        self.heading = page.locator("h1")
        # The totals table lives in its own block, so scope the line items to
        # the responsive wrapper that holds the products table.
        self.line_items = page.locator("#content .table-responsive tbody tr")
        self.open_cart_button = page.locator("#cart > button")

    def open(self):
        super().open(self.PATH)

    def item_names(self):
        return [text.strip() for text in self.line_items.all_inner_texts()]
